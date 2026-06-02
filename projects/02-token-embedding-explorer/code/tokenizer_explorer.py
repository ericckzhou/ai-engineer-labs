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

    Steps:
      1. return get_encoder().encode(text)   (one line — the encoder does the work).

    Example (mirrors tests/test_tokenizer.py::test_encode_returns_ints — exact IDs are
    model-specific, so the test asserts the SHAPE, not the values):
        ids = encode("hello world")
        isinstance(ids, list) and all(isinstance(i, int) for i in ids)   # -> True
        # e.g. ids might be [24912, 2375] for the o200k_base encoding
    """
    return get_encoder().encode(text)


def decode(ids: list[int]) -> str:
    """[learner] Inverse of encode: token IDs back to the exact original text (lossless).

    Steps:
      1. return get_encoder().decode(ids).

    Example (mirrors tests/test_tokenizer.py::test_round_trip_is_lossless — the round-trip is
    the property that proves tokenization is a reversible codec):
        decode(encode("Tokenization is not magic."))  -> "Tokenization is not magic."
        decode(encode("emoji 🚀 and ünïcöde"))         -> "emoji 🚀 and ünïcöde"
        decode(encode(""))                             -> ""
    """
    return get_encoder().decode(ids)


def token_pieces(ids: list[int]) -> list[str]:
    """[learner] The decoded text chunk for EACH id individually, so boundaries are visible.

    Steps:
      1. decode ONE id at a time: [get_encoder().decode([i]) for i in ids].
      2. notice spaces attach to the *front* of words (" is", " not") — that's the tokenizer,
         not a bug. The pieces must rejoin to the original text exactly.

    Example (mirrors tests/test_tokenizer.py::test_token_pieces_align_with_ids):
        ids = encode("Tokenization is not magic.")
        pieces = token_pieces(ids)
        len(pieces) == len(ids)                      # -> True (one piece per id)
        "".join(pieces) == "Tokenization is not magic."   # -> True (lossless concatenation)
        # e.g. pieces ≈ ['Token', 'ization', ' is', ' not', ' magic', '.']
    """
    enc = get_encoder()
    return [enc.decode([i]) for i in ids]


def count(text: str) -> int:
    """[learner] Token count. Must equal len(encode(text)) — this is what you are billed on.

    Steps:
      1. return len(encode(text))   (count the IDs — don't estimate from characters).

    Example (mirrors tests/test_tokenizer.py::test_count_equals_number_of_ids):
        count("Tokenization is not magic.") == len(encode("Tokenization is not magic."))  # -> True
        count("") == 0
    """
    return len(encode(text))


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
