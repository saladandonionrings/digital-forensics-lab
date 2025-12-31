from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_index():
    return FileResponse('index.html')

def load_data():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.get("/labs")
def get_labs():
    data = load_data()
    for lab in data:
        for c in lab["challenges"]:
            if "answer" in c: del c["answer"]
    return data

class Submission(BaseModel):
    challenge_id: str
    attempt: str

@app.post("/verify")
def verify(data: Submission):
    all_data = load_data()
    for lab in all_data:
        for c in lab["challenges"]:
            if c["id"] == data.challenge_id:
                if c["answer"].lower().strip() == data.attempt.lower().strip():
                    return {"status": "correct"}
    return {"status": "wrong"}
