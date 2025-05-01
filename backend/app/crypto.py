# app/crypto.py
from typing import List, Dict

ALPHABET_SIZE = 256  # full extended ASCII range


def _shift_char(ch: str, shift: int, *, decrypt: bool = False) -> str:
    if len(ch) != 1:
        raise ValueError("Expected single character")
    offset = -shift if decrypt else shift
    return chr((ord(ch) + offset) % ALPHABET_SIZE)


# ── Caesar ──────────────────────────────────────────────────────────────────────
def caesar_encrypt(plaintext: str, shift: int) -> str:
    return ''.join(_shift_char(c, shift) for c in plaintext)


def caesar_decrypt(ciphertext: str, shift: int) -> str:
    return ''.join(_shift_char(c, shift, decrypt=True) for c in ciphertext)


def caesar_attack(ciphertext: str) -> List[Dict[str, str]]:
    """Returns a list of {'shift': k, 'plaintext': guess} for all 256 shifts."""
    return [
        {
            "shift": k,
            "plaintext": caesar_decrypt(ciphertext, k)
        }
        for k in range(ALPHABET_SIZE)
    ]


# ── “Mono-alphabetic” (simple shift variant) ────────────────────────────────────
# NOTE: A true mono-alphabetic cipher uses a *permutation* key.  Because your spec
# asks for a shift parameter we replicate the Caesar logic but call it “mono”.
def mono_encrypt(plaintext: str, shift: int) -> str:
    return caesar_encrypt(plaintext, shift)


def mono_decrypt(ciphertext: str, shift: int) -> str:
    return caesar_decrypt(ciphertext, shift)
