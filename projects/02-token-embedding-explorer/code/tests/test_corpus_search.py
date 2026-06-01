"""[provided] Guiding test for Milestone M5 — corpus_search.search().

Runs with NO network: it replaces embed() with a deterministic fake so the RANKING LOGIC is tested
in isolation (depends on a correct cosine_similarity from M4). Fails until both search() and
cosine_similarity() are implemented. Run:  python -m pytest tests/test_corpus_search.py
"""
import numpy as np
import pytest

import corpus_search

# Hand-built vectors: the query points almost exactly at "near", less at "mid", away from "far".
_VECTORS = {
    "query":  np.array([1.0, 0.0, 0.0]),
    "near":   np.array([0.9, 0.1, 0.0]),
    "mid":    np.array([0.5, 0.5, 0.0]),
    "far":    np.array([0.0, 0.0, 1.0]),
}


@pytest.fixture
def fake_embed(monkeypatch):
    monkeypatch.setattr(corpus_search, "embed", lambda text: _VECTORS[text])


def test_ranks_by_meaning(fake_embed):
    results = corpus_search.search("query", ["far", "near", "mid"], k=3)
    ranked = [text for text, _ in results]
    assert ranked == ["near", "mid", "far"]


def test_returns_text_score_pairs_sorted_desc(fake_embed):
    results = corpus_search.search("query", ["far", "near", "mid"], k=3)
    scores = [score for _, score in results]
    assert scores == sorted(scores, reverse=True)
    assert all(isinstance(t, str) for t, _ in results)


def test_respects_k(fake_embed):
    results = corpus_search.search("query", ["far", "near", "mid"], k=1)
    assert len(results) == 1
    assert results[0][0] == "near"


def test_empty_corpus_returns_empty(fake_embed):
    assert corpus_search.search("query", [], k=3) == []
