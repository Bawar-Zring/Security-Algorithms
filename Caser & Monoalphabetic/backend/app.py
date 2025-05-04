# app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from collections import Counter
import random
import string
from fastapi.staticfiles import StaticFiles          
from fastapi.responses import FileResponse           
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent          
FRONT_DIR = BASE_DIR.parent / "frontend"

app = FastAPI(
    title="Cipher API",
    description="API for Caesar and Monoalphabetic cipher operations",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/assets", StaticFiles(directory=FRONT_DIR), name="assets")   # ★

@app.get("/", include_in_schema=False)
def serve_spa():
    """Return the main HTML file."""
    return FileResponse(FRONT_DIR / "index.html")

class CipherRequest(BaseModel):
    text: str
    shift: Optional[int] = None           # used only by Caesar

class DecryptRequest(BaseModel):
    text: str
    key: Optional[Dict[str, str]] = None  # used only by Monoalphabetic
    shift: Optional[int] = None           # used only by Caesar

class CipherResponse(BaseModel):
    result: str
    key: Optional[Dict[str, str]] = None

class AttackResponse(BaseModel):
    results: List[dict]

def caesar_encrypt(plaintext: str, shift: int) -> str:
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            shift_amount = shift % 256
            if char.isupper():
                new_char = chr((ord(char) - ord('A') + shift_amount) % 256 + ord('A'))
            else:
                new_char = chr((ord(char) - ord('a') + shift_amount) % 256 + ord('a'))
            encrypted_text += new_char
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(ciphertext: str, shift: int) -> str:
    return caesar_encrypt(ciphertext, -shift)

def caesar_attack(ciphertext: str) -> List[Dict[str, any]]:
    return [{"shift": s, "plaintext": caesar_decrypt(ciphertext, s)} for s in range(256)]

def create_substitution_key() -> Dict[str, str]:
    chars = list(string.ascii_letters + string.digits + string.punctuation + ' ')
    shuffled = chars.copy()
    random.shuffle(shuffled)
    return dict(zip(chars, shuffled))

def monoalphabetic_encrypt(text: str) -> tuple[str, Dict[str, str]]:
    key = create_substitution_key()
    encrypted = ''.join(key.get(c, c) for c in text)
    return encrypted, key

def monoalphabetic_decrypt(text: str, key: Dict[str, str]) -> str:
    reverse_key = {v: k for k, v in key.items()}
    return ''.join(reverse_key.get(c, c) for c in text)

@app.get("/")
async def root():
    return {
        "message": "Cipher API",
        "endpoints": {
            "/caesar/encrypt (POST)": "Caesar encryption",
            "/caesar/decrypt (POST)": "Caesar decryption",
            "/caesar/attack  (POST)": "Caesar brute-force attack",
            "/mono/encrypt   (POST)": "Monoalphabetic encryption",
            "/mono/decrypt   (POST)": "Monoalphabetic decryption"
        }
    }

# ---- Caesar ----
@app.post("/caesar/encrypt")
async def encrypt_caesar(request: CipherRequest):
    if request.shift is None or not 0 <= request.shift <= 256:
        raise HTTPException(400, "Shift must be 0-256")
    return {"result": caesar_encrypt(request.text, request.shift)}

@app.post("/caesar/decrypt")
async def decrypt_caesar(request: DecryptRequest):
    if request.shift is None or not 0 <= request.shift <= 256:
        raise HTTPException(400, "Shift must be 0-256")
    return {"result": caesar_decrypt(request.text, request.shift)}

@app.post("/caesar/attack", response_model=AttackResponse)
async def attack_caesar(request: CipherRequest):
    return AttackResponse(results=caesar_attack(request.text))

# ---- Monoalphabetic ----
@app.post("/mono/encrypt", response_model=CipherResponse)
async def encrypt_mono(request: CipherRequest):
    encrypted, key = monoalphabetic_encrypt(request.text)
    return CipherResponse(result=encrypted, key=key)

@app.post("/mono/decrypt", response_model=CipherResponse)
async def decrypt_mono(request: DecryptRequest):
    if not request.key:
        raise HTTPException(400, "Decryption key required")
    return CipherResponse(result=monoalphabetic_decrypt(request.text, request.key))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)