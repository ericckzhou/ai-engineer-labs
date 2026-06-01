"""[provided] Guiding tests for Milestones M2/M3 — semantic_search.py.

to_similarity is pure (offline). The search() test uses a real in-memory Chroma collection seeded
with hand vectors and a fake query-embed, so ranking + distance->similarity are tested without a
network (skips if chromadb is absent). The docstring examples in semantic_search.py mirror these.
Run: python -m pytest tests/test_search.py
"""
import pytest

import semantic_search
from conftest import fake_embed_one


def test_to_similarity():
    assert semantic_search.to_similarity(0.0) == pytest.approx(1.0)
    assert semantic_search.to_similarity(0.3) == pytest.approx(0.7)
    assert semantic_search.to_similarity(1.0) == pytest.approx(0.0)


def test_search_ranks_by_meaning(cosine_collection, monkeypatch):
    col, docs, _ids = cosine_collection
    monkeypatch.setattr(semantic_search, "embed_one", fake_embed_one)

    results = semantic_search.search(col, "monetary policy and the economy", k=3)

    # finance doc (x-axis) is closest to the finance-leaning query
    assert results[0][0] == "The central bank raised interest rates this quarter."
    # returns (document, similarity, metadata) triples
    assert len(results[0]) == 3
    # ranked by similarity DESCENDING (no inversion)
    sims = [sim for _doc, sim, _meta in results]
    assert sims == sorted(sims, reverse=True)
    # similarities are 1 - distance, so the top match is high and positive
    assert results[0][1] > 0.8


def test_search_empty_query_text_raises_keyerror_in_fake(cosine_collection, monkeypatch):
    # Guard: unknown text isn't in the fake map — confirms the test fake is being used, not a network call.
    col, _docs, _ids = cosine_collection
    monkeypatch.setattr(semantic_search, "embed_one", fake_embed_one)
    with pytest.raises(KeyError):
        semantic_search.search(col, "a query the fake does not know", k=2)
