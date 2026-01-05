# Which one is the malware ?
- Upload the files on https://www.virustotal.com/gui/ and analyze.

# task1
```bash
gdb -q ./task1
(gdb) set disassembly-flavor intel
(gdb) disassemble main
```
## script
```python
def hex_to_string(hex_val):
    bytes_val = bytes.fromhex(hex_val.replace('0x', ''))
    return bytes_val[::-1].decode('ascii')

rax1 = "0x6d30737b67616c66" # rbp-0x30
rdx1 = "0x6331707375735f33" # rbp-0x28
rax2 = "0x7274735f73753031" # rbp-0x20
dwrd = "0x7d676e31"         # rbp-0x18 (DWORD)

flag = hex_to_string(rax1) + hex_to_string(rdx1) + hex_to_string(rax2) + hex_to_string(dwrd)

print(f"Flag : {flag}")
# flag{s0m3_susp1c10us_str1ng}
```
# task2
- The binary requires two "Magic Numbers" to trigger a XOR decryption loop that reveals the flag
```bash
gdb -q ./task2
(gdb) set disassembly-flavor intel
(gdb) disassemble hmmm
```

## analysis
```bash
0x00000000000011df <+22>:	cmp    $0x17,%eax # 23
0x000000000000121a <+81>:	cmp    $0x539,%eax # 1337
0x0000000000001257 <+142>:	cmp    $0xfc,%eax # 252
```

```bash
ltrace ./task2
# 23
# 1337
# 252
# flag{sup3r_s1mpl3_x0r}
```

# task3
```bash
❯ file task3
# task3: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=3fd61e74839dcafbd57f6a76b724b1488522b449, for GNU/Linux 3.2.0, not stripped
❯ ltrace ./task3 2>&1 | grep "putchar" | awk -F'(' '{print $2}' | awk -F',' '{printf "%c", $1}' && echo ""
# nothing
❯ gdb -q ./task3 << 'EOF'
break *do_shenanigans+362
run
dump binary memory alphabet.bin $rbp-0x30 $rbp
dump binary memory indexes.bin $rbp-0xb0 $rbp-0x30
quit
EOF
```
## script
```py
import struct

# Load the raw alphabet string from GDB dump
with open("alphabet.bin", "rb") as f:
    raw_alphabet = f.read().decode('ascii', errors='ignore')

# --- LEETSPEAK CORRECTION LAYER ---
mapping = str.maketrans("02", "13")
alphabet = raw_alphabet.translate(mapping)

# Load the indexes (stored as 4-byte integers)
with open("indexes.bin", "rb") as f:
    data = f.read()
    # Unpack binary data into a list of integers (Little-Endian)
    indices = [struct.unpack("<I", data[i:i+4])[0] for i in range(0, len(data), 4)]

# Reconstruct the flag
flag = ""
for idx in indices:
    if idx < len(alphabet):
        char = alphabet[idx]
        flag += char
        if char == '}':
            break

print(f"[*] Original Alphabet: {raw_alphabet[:40]}...")
print(f"[*] Modified Alphabet: {alphabet[:40]}...")
print(f"\n[+] Corrected Flag: {flag}")
# flag{r3v3rs3_3ng1n33r1ng_1z1}
```

# task4.py
- Decompressed : 

```py
import zlib
import base64
import codecs
from Crypto.Cipher import AES

# --- STAGE 1: HEX DATA ---
m = "789cad53df739a40107ef7aff08d38cd74ce4330ccb49d395011f911114af1262f781002825845e0f8eb73674cda3cf4ad0f3bc7ee7efbedb7cb6c561eab533ddc45e7449edc0f491527e43c28a33423c3ef43011f56cdce5367e450b4b1fe707161d1467a400dbda889aed05853d54d603b5af9e137a405e6ccad58ac2e120f29866e64440c5a5b5c3d93dec949ee80109efbc43318c601c60ca446bed9dbbd0bec1ebf6c4b57140645d5245c81dd1b14435ca2d2a3a8dd88768b28f29763ab5fe6761be4d8b724d5473dea6725723bc9f603867624ec7680e500729763ecd2de5a5922763dcae210b918a8bad761b891109c5f50493b5c620995c7316e02b4ae41280cd22ae602128d8f505cc83200a6b65aec0e9b82646abb0d9d3e860ac5b32a35b2bda3a5c08c7e6"
a_hex = "d538e5f7bea0987fb0bd6837c073785a9ed65b692d4d050ba7d5f211bdbfd19f8562915317de17825828164696acd6b84419c9cebec40b9086de979cb42423a987b2630dc59d3a175e3d4c1fab1b357b8d6168fedc17cdcd966f062fb467b8c68fe7b7d694ee69c1e0ba93ff64a7af08d49e823102e3e6a33962b4f2602f60aec78ddb69f530b2a9dbda84938e35bc8abab80a76e0a9f3af999bd93a74e1c33633fa93e5dce354b274d54dc318c1c33633979ca4c61260aa3e1973f69f18d426614b2f4e64f99c1e473ec6f0c7c602fb9b5966f31e643c0bea35b9cb582cae7565cc195e6ff28b87d732c5fc075385673edfc0f35836b535295c7ac48eede2eeceb4e9eb00b635776f72e89d3f1dd4e3fe885d1e85ef876ae4fd921fd21dc0b49971061347a05d05b2f77"

# --- DECODING LAYER 1 (ZLIB) ---
w = bytes.fromhex(m + a_hex)
decompressed = zlib.decompress(w).decode()

# --- DECODING LAYER 2 (BASE64 & ROT13) ---
magic = 'ZnJvbSBDcnlwdG8uQ2lwaGVyIGltcG9ydCBBRVMNCmltcG9ydCBvcw0KDQoNCmtleSA9IGIic3VwM3JfczNjcjN0X2szeSINCmN0ID0gIjRkMzQ0MzZhYmQ3'
love = 'MzIyZ2ZmAmSyAwR3MwAyATH1LzHjMwVjZTL5BTAzAzDmAQx5MTV2ZmN5ZQx0ZTL0AQH1ZQyzLJL3ZQSyZQx2AQZ0BGSxZ2R5A2EuAmyxZmZ5Amp1ZvVAPt0X'
god = 'eCA9IGlucHV0KCJFbnRlciBwYXNzd29yZDogIikNCg0KaWYgeCA9PSBrZXkuZGVjb2RlKCk6DQogICAgY2lwaGVyID0gQUVTLm5ldyhrZXk9a2V5LCBtb2Rl'
destiny = 'CHSSHl5AG0ESK0IQDvxAPvNtVPOxMJZtCFOwnKObMKVhMTIwpayjqPuvrKEypl5zpz9gnTI4XTA0XFxAPvNtVPOipl5mrKA0MJ0bMTIwYzEyL29xMFtcXD0X'

trust_b64 = magic + codecs.decode(love, 'rot13') + god + codecs.decode(destiny, 'rot13')
malware_script = base64.b64decode(trust_b64).decode()

print("### DE-OBFUSCATED MALWARE SCRIPT ###")
print("-" * 50)
print(malware_script)
print("-" * 50)

# --- DECODING LAYER 3 (AES DECRYPTION) ---
key = b"sup3r_s3cr3t_k3y"
ct = "4d34436abd7fee3c371e617f3e4e5be0f200f98cf6d3499db63090940f445509faf701e09643491d3a97da79d3397752"

cipher = AES.new(key=key, mode=AES.MODE_ECB)
decrypted_bytes = cipher.decrypt(bytes.fromhex(ct))
flag_command = decrypted_bytes.decode(errors='ignore').strip()

print("\n### FLAG ###")
print(f"{flag_command}")
```