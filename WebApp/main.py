from fastapi import FastAPI, HTTPException, Request, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, constr
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import json
import os
import hmac
from typing import Dict, List

# 1. Advanced Rate Limiting using Slowapi
limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Secure JSON Loading (Read-Only and Validation)
def load_master_data():
    try:
        if not os.path.exists('questions.json'):
            raise FileNotFoundError("questions.json is missing")
        with open('questions.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Basic schema validation could be added here
            return data
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"CRITICAL: Could not load lab data: {e}")
        return []

MASTER_DATA = load_master_data()

# 3. Prevent Directory Traversal
LABS_DIR = os.path.abspath("Labs")
if not os.path.exists(LABS_DIR):
    os.makedirs(LABS_DIR)

app.mount("/Labs", StaticFiles(directory=LABS_DIR), name="Labs")

# 4. Hardened CORS (Only allow specific, trusted origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# 5. Robust Input Validation with Pydantic
class Submission(BaseModel):
    # Limits length to prevent ReDoS or memory exhaustion attacks
    challenge_id: constr(min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")
    attempt: constr(min_length=1, max_length=255)

@app.get("/")
async def read_index():
    return FileResponse('index.html')

@app.get("/labs")
@limiter.limit("10/minute")
async def get_labs(request: Request):
    clean_data = []
    for lab in MASTER_DATA:
        # We explicitly keep the lab-level metadata (id, title, download_url)
        lab_copy = {
            "id": lab.get("id"),
            "title": lab.get("title"),
            "download_url": lab.get("download_url"), # Ensure this is sent!
            "challenges": [
                {k: v for k, v in c.items() if k not in ["answer", "secret_hint"]} 
                for c in lab.get("challenges", [])
            ]
        }
        clean_data.append(lab_copy)
    return clean_data

@app.post("/verify")
@limiter.limit("5/minute") # Strict limit on brute-force attempts
async def verify(request: Request, data: Submission):
    user_attempt = data.attempt.lower().strip().encode()
    
    for lab in MASTER_DATA:
        for c in lab.get("challenges", []):
            if c["id"] == data.challenge_id:
                correct_answer = c["answer"].lower().strip().encode()
                
                # 6. Constant Time Comparison 
                # Prevents "Timing Attacks" where an attacker guesses letters based on server response time
                if hmac.compare_digest(user_attempt, correct_answer):
                    return {"status": "correct"}
                    
    return {"status": "wrong"}