"""[provided] Test fixtures for Project 03.

Makes code/ importable from tests/ and provides OFFLINE fakes so retrieval/ranking logic can be
tested without a network or an embedding provider. Hand-built 3-D vectors stand in for real
embeddings; a fake embed maps known texts/queries to those vectors deterministically.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Deterministic stand-in "embeddings" (3-D). Direction encodes topic:
#   finance ≈ x-axis, fiction ≈ y-axis, biology ≈ z-axis.
FAKE_VECTORS = {
    # documents
    "The central bank raised interest rates this quarter.": [1.0, 0.0, 0.0],
    "Inflation eroded the purchasing power of household savings.": [0.9, 0.1, 0.0],
    "A young wizard discovers he has magical powers and attends a school of magic.": [0.0, 1.0, 0.0],
    "Photosynthesis converts sunlight into chemical energy in plants.": [0.0, 0.0, 1.0],
    # queries
    "monetary policy and the economy": [0.95, 0.10, 0.0],
    "a story about wizards and magic": [0.0, 1.0, 0.0],
    "how cells produce energy": [0.0, 0.0, 1.0],
    "interest rates": [1.0, 0.0, 0.0],
    "magic school": [0.0, 1.0, 0.0],
}


def fake_embed_one(text: str) -> list[float]:
    return list(FAKE_VECTORS[text])


def fake_embed_many(texts: list[str]) -> list[list[float]]:
    return [list(FAKE_VECTORS[t]) for t in texts]


@pytest.fixture
def cosine_collection():
    """An in-memory Chroma collection (cosine space) seeded with the finance/fiction/biology docs.
    Skips if chromadb is not installed."""
    chromadb = pytest.importorskip("chromadb")
    docs = [
        "The central bank raised interest rates this quarter.",
        "A young wizard discovers he has magical powers and attends a school of magic.",
        "Photosynthesis converts sunlight into chemical energy in plants.",
    ]
    ids = ["d0", "d1", "d2"]
    client = chromadb.Client()  # in-memory, offline
    col = client.create_collection("test", metadata={"hnsw:space": "cosine"})
    col.add(ids=ids, embeddings=fake_embed_many(docs), documents=docs,
            metadatas=[{"topic": "finance"}, {"topic": "fiction"}, {"topic": "biology"}])
    return col, docs, ids
