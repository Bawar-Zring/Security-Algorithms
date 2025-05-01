from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
from collections import Counter
import random
import string

# ───────────────────────────────────────── FastAPI setup
app = FastAPI(title="Cipher API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # change if you need stricter CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ───────────────────────────────────────── Pydantic models
class CaesarBody(BaseModel):
    text: str
    shift: int

class MonoBody(BaseModel):
    text: str
    substitution_key: Dict[str, str] | None = None  # optional on encrypt

class GenericEncryptBody(BaseModel):
    plaintext: str
    key: str | Dict[str, str] | None = None         # 64-bit bin str or dict

class GenericDecryptBody(BaseModel):
    ciphertext: str
    key: str | Dict[str, str]

# ───────────────────────────────────────── Caesar helpers
def caesar_encrypt(text: str, shift: int) -> str:
    out = []
    for ch in text:
        if ch.isascii():
            out.append(chr((ord(ch) + shift) % 256))
        else:
            out.append(ch)
    return ''.join(out)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, (-shift) % 256)

def caesar_attack(text: str) -> List[Dict]:
    return [
        {"shift": s, "decrypted": caesar_decrypt(text, s)}
        for s in range(256)
    ]

# ───────────────────────────────────────── Mono-alphabetic helpers
def make_sub_key() -> Dict[str, str]:
    chars = list(string.printable)
    shuffled = chars.copy()
    random.shuffle(shuffled)
    return dict(zip(chars, shuffled))

def mono_encrypt(text: str, key: Dict[str, str] | None = None) -> tuple[str, Dict[str, str]]:
    key = key or make_sub_key()
    return ''.join(key.get(c, c) for c in text), key

def mono_decrypt(text: str, key: Dict[str, str]) -> str:
    rev = {v: k for k, v in key.items()}
    return ''.join(rev.get(c, c) for c in text)

def mono_attack(text: str) -> List[Dict]:
    # simple frequency dump – extend as you wish
    freq = Counter(c.lower() for c in text if c.isalpha())
    ordered = ''.join(ch for ch, _ in freq.most_common())
    return [{"description": "letter frequency order", "frequencies": ordered}]

# ───────────────────────────────────────── Caesar routes
@app.post("/caesar/encrypt")
def caesar_encrypt_route(body: CaesarBody):   
    if not 0 <= body.shift <= 255:
        raise HTTPException(400, "shift must be 0-255")
    return {"result": caesar_encrypt(body.text, body.shift)}

@app.post("/caesar/decrypt")
def caesar_decrypt_route(body: CaesarBody):
    if not 0 <= body.shift <= 255:
        raise HTTPException(400, "shift must be 0-255")
    return {"result": caesar_decrypt(body.text, body.shift)}

@app.post("/caesar/attack")
def caesar_attack_route(body: CaesarBody):
    return {"results": caesar_attack(body.text)}

# ───────────────────────────────────────── Mono routes
@app.post("/monoalphabetic/encrypt")
def mono_encrypt_route(body: MonoBody):
    encrypted, key = mono_encrypt(body.text, body.substitution_key)
    return {"result": encrypted, "key": key}

@app.post("/monoalphabetic/decrypt")
def mono_decrypt_route(body: MonoBody):
    if body.substitution_key is None:
        raise HTTPException(400, "substitution_key is required")
    return {"result": mono_decrypt(body.text, body.substitution_key)}

@app.post("/monoalphabetic/attack")
def mono_attack_route(body: MonoBody):
    return {"results": mono_attack(body.text)}

# ───────────────────────────────────────── Generic endpoints for the UI
@app.post("/encrypt")
def generic_encrypt(body: GenericEncryptBody):
    # 1) If key is a dict ⇒ mono-alphabetic
    if isinstance(body.key, dict):
        encrypted, key = mono_encrypt(body.plaintext, body.key)
        return {"encrypted": encrypted, "key": key}

    # 2) Else treat key (or None) as 64-bit binary for Caesar
    shift = int(body.key, 2) % 256 if body.key else random.randint(0, 255)
    key_bin = format(shift, "064b")  # always return key so UI can display
    encrypted = caesar_encrypt(body.plaintext, shift)
    return {"encrypted": encrypted, "key": key_bin}

@app.post("/decrypt")
def generic_decrypt(body: GenericDecryptBody):
    # 1) Dict key ⇒ mono
    if isinstance(body.key, dict):
        return {"decrypted": mono_decrypt(body.ciphertext, body.key)}

    # 2) Binary str key ⇒ Caesar
    if not isinstance(body.key, str) or not len(body.key) == 64 or not set(body.key) <= {"0", "1"}:
        raise HTTPException(400, "Key must be 64-bit binary")
    shift = int(body.key, 2) % 256
    return {"decrypted": caesar_decrypt(body.ciphertext, shift)}

# ───────────────────────────────────────── Root
@app.get("/")
def root():
    return {
        "message": "Cipher API - unified version",
        "ui_endpoints": { "encrypt": "/encrypt", "decrypt": "/decrypt" },
        "advanced": {
            "caesar": ["/caesar/encrypt", "/caesar/decrypt", "/caesar/attack"],
            "monoalphabetic": ["/monoalphabetic/encrypt", "/monoalphabetic/decrypt", "/monoalphabetic/attack"]
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
