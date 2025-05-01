# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, conint
from app import crypto

app = FastAPI(
    title="Security Algorithms – Sub-project 1 API",
    version="0.1.0"
)


class ShiftPayload(BaseModel):
    text: str
    shift: conint(ge=0, le=255)  # validate 0-255 inclusive


class TextPayload(BaseModel):
    text: str


# ── Caesar endpoints ────────────────────────────────────────────────────────────
@app.post("/caesar/encrypt")
def caesar_encrypt(payload: ShiftPayload):
    return {"ciphertext": crypto.caesar_encrypt(payload.text, payload.shift)}


@app.post("/caesar/decrypt")
def caesar_decrypt(payload: ShiftPayload):
    return {"plaintext": crypto.caesar_decrypt(payload.text, payload.shift)}


@app.post("/caesar/attack")
def caesar_attack(payload: TextPayload):
    return {"candidates": crypto.caesar_attack(payload.text)}


# ── Mono-alphabetic endpoints (shift variant) ───────────────────────────────────
@app.post("/mono/encrypt")
def mono_encrypt(payload: ShiftPayload):
    return {"ciphertext": crypto.mono_encrypt(payload.text, payload.shift)}


@app.post("/mono/decrypt")
def mono_decrypt(payload: ShiftPayload):
    return {"plaintext": crypto.mono_decrypt(payload.text, payload.shift)}
