"""[provided] Guiding tests for Milestone M4 — retriever.retrieve(). Fully OFFLINE.

Fails (NotImplementedError) until retrieve() (and the scoring.py functions it composes) are
implemented. Memories use hand-built embeddings + timestamps, so no provider is needed. The docstring
example in retriever.py mirrors test_recency_and_importance_break_a_relevance_tie.
Run: python -m pytest tests/test_retriever.py
"""
import pytest

from memory_store import Memory, MemoryStore
from retriever import retrieve

NOW = 1_000_000.0


def _store_with_tie() -> MemoryStore:
    """Two memories with the SAME embedding [1,0,0]: trivial+old vs important+fresh."""
    store = MemoryStore()
    store.add(Memory("m0", "brushed teeth", kind="episodic", created_at=NOW - 1e6,
                     last_accessed=NOW - 1e6, importance=1, embedding=[1.0, 0.0, 0.0]))
    store.add(Memory("m1", "decided to default to Groq", kind="semantic", created_at=NOW - 10,
                     last_accessed=NOW - 10, importance=8, embedding=[1.0, 0.0, 0.0]))
    return store


def test_recency_and_importance_break_a_relevance_tie():
    store = _store_with_tie()
    top = retrieve(store, [1.0, 0.0, 0.0], now=NOW, k=1, weights=(1.0, 1.0, 1.0), decay_rate=0.995)
    assert [m.id for m in top] == ["m1"]  # relevance ties; recency + importance pick the right one


def test_returns_at_most_k_ranked_descending():
    store = _store_with_tie()
    top = retrieve(store, [1.0, 0.0, 0.0], now=NOW, k=1)
    assert len(top) == 1  # respects the budget (MemGPT paging)


def test_retrieve_touches_last_accessed():
    store = _store_with_tie()
    top = retrieve(store, [1.0, 0.0, 0.0], now=NOW, k=1)
    # The returned memory's recency clock was reset to `now` (retrieval refreshes recency).
    assert top[0].last_accessed == pytest.approx(NOW)


def test_relevance_separates_topics_when_no_tie():
    store = MemoryStore()
    store.add(Memory("m0", "about cats", kind="episodic", created_at=NOW, last_accessed=NOW,
                     importance=5, embedding=[1.0, 0.0, 0.0]))
    store.add(Memory("m1", "about finance", kind="episodic", created_at=NOW, last_accessed=NOW,
                     importance=5, embedding=[0.0, 1.0, 0.0]))
    top = retrieve(store, [0.0, 1.0, 0.0], now=NOW, k=1)  # query points at the finance memory
    assert top[0].id == "m1"
