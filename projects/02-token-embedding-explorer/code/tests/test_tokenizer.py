"""[provided] Guiding tests for Milestone M1 — tokenizer_explorer.

The lossless round-trip is the property that proves tokenization is a reversible codec. These call
the real tiktoken encoder, which needs the encoding file (cached after first download). If the
encoding can't be loaded (no network on a cold machine), the whole module skips rather than failing
spuriously. Otherwise the tests fail (NotImplementedError) until you implement M1.

Run:  python -m pytest tests/test_tokenizer.py
"""
import pytest

import tokenizer_explorer

# Skip the whole module if the encoding file isn't available (offline + cold cache).
try:
    tokenizer_explorer.get_encoder()
except Exception as exc:  # pragma: no cover - environment-dependent
    pytest.skip(f"tiktoken encoding unavailable ({exc})", allow_module_level=True)


ROUND_TRIP_SAMPLES = [
    "Tokenization is not magic.",
    "unbelievable",
    "  leading and  inner   spaces",
    "emoji 🚀 and ünïcöde",
    "",
]


@pytest.mark.parametrize("text", ROUND_TRIP_SAMPLES)
def test_round_trip_is_lossless(text):
    assert tokenizer_explorer.decode(tokenizer_explorer.encode(text)) == text


@pytest.mark.parametrize("text", ROUND_TRIP_SAMPLES)
def test_count_equals_number_of_ids(text):
    assert tokenizer_explorer.count(text) == len(tokenizer_explorer.encode(text))


def test_encode_returns_ints():
    ids = tokenizer_explorer.encode("hello world")
    assert isinstance(ids, list)
    assert all(isinstance(i, int) for i in ids)


def test_token_pieces_align_with_ids():
    ids = tokenizer_explorer.encode("Tokenization is not magic.")
    pieces = tokenizer_explorer.token_pieces(ids)
    assert len(pieces) == len(ids)
    assert "".join(pieces) == "Tokenization is not magic."
