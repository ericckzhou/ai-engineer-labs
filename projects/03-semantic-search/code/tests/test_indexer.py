"""[provided] Guiding test for Milestone M1 — indexer.build_index() idempotency.

Uses a fake embed and an in-memory Chroma client (offline; skips if chromadb absent). Fails
(NotImplementedError) until build_index is implemented. Mirrors the docstring example in indexer.py.
Run: python -m pytest tests/test_indexer.py
"""
import pytest

import indexer
from conftest import fake_embed_many

pytest.importorskip("chromadb")


@pytest.fixture
def in_memory_indexer(monkeypatch):
    import chromadb
    client = chromadb.Client()  # in-memory
    monkeypatch.setattr(indexer, "embed_many", fake_embed_many)
    monkeypatch.setattr(indexer, "get_client", lambda: client)
    return indexer


def test_build_index_count(in_memory_indexer):
    docs = ["The central bank raised interest rates this quarter.",
            "A young wizard discovers he has magical powers and attends a school of magic."]
    col = in_memory_indexer.build_index(docs, ["d0", "d1"], collection_name="t1")
    assert col.count() == 2


def test_build_index_is_idempotent(in_memory_indexer):
    docs = ["The central bank raised interest rates this quarter.",
            "A young wizard discovers he has magical powers and attends a school of magic."]
    in_memory_indexer.build_index(docs, ["d0", "d1"], collection_name="t2")
    col = in_memory_indexer.build_index(docs, ["d0", "d1"], collection_name="t2")  # re-run
    assert col.count() == 2  # not 4 — no duplicates
