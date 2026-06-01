"""tokenizer_explorer.py — [partial] Milestone M1 of Project 02 (Token & Embedding Explorer).

Make tokenization VISIBLE: text → integer IDs → the chunk each ID maps to → count, and prove the
round-trip is lossless. Tokenization is a local, deterministic codec — no network, no meaning
attached to the *value* of an ID (it just indexes a vocabulary).

PROVIDED (do not need to change): ENCODING_NAME, get_encoder(), main() printing harness.
LEARNER: implement the four small functions marked TODO(learner). They are one-liners over the
`tiktoken` encoder — the struggle here is understanding what they show, not the code length.

Run:  python tokenizer_explorer.py
"""
from __future__ import annotations

import tiktoken

# [provided] GPT-4o-family encoding. Token counts are EXACT for OpenAI models using this encoding
# and only an ESTIMATE for other providers (each model family has its own tokenizer).
ENCODING_NAME = "o200k_base"


def get_encoder() -> tiktoken.Encoding:
    """[provided] Return the tiktoken encoder. First call may fetch+cache the encoding file."""
    return tiktoken.get_encoding(ENCODING_NAME)


def encode(text: str) -> list[int]:
    """[learner] Return the list of integer token IDs for `text`.

    Hint: get_encoder().encode(text)
    """
    raise NotImplementedError("M1: implement encode() - text to list[int] token IDs")


def decode(ids: list[int]) -> str:
    """[learner] Inverse of encode: token IDs back to the exact original text (lossless)."""
    raise NotImplementedError("M1: implement decode() - list[int] back to str")


def token_pieces(ids: list[int]) -> list[str]:
    """[learner] The decoded text chunk for EACH id individually, so boundaries are visible.

    Hint: decode one id at a time. Notice spaces attach to the *front* of words.
    """
    raise NotImplementedError("M1: implement token_pieces() - per-id decoded chunks")


def count(text: str) -> int:
    """[learner] Token count. Must equal len(encode(text)) — this is what you are billed on."""
    raise NotImplementedError("M1: implement count() - number of tokens in text")


# ----------------------------------------------------------------------------------------------
# [provided] Inspection harness. Once the four functions above are implemented this just works.
# ----------------------------------------------------------------------------------------------
SAMPLES = [
    "Tokenization is not magic.",
    "unbelievable",
    "antidisestablishmentarianism",
    "  spaces   and\tpunctuation!?",
    "emoji 🚀 and ünïcöde",
]


def _inspect(text: str) -> None:
    ids = encode(text)
    pieces = token_pieces(ids)
    print(f"\ntext        : {text!r}")
    print(f"token count : {count(text)}")
    print(f"ids         : {ids}")
    print(f"pieces      : {[p for p in pieces]}")
    roundtrip = decode(ids)
    ok = roundtrip == text
    print(f"round-trip  : {'OK (lossless)' if ok else 'MISMATCH'}  {'' if ok else repr(roundtrip)}")


def main() -> None:
    print(f"Project 02 — Tokenizer Explorer (encoding: {ENCODING_NAME})")
    for s in SAMPLES:
        _inspect(s)


if __name__ == "__main__":
    main()
