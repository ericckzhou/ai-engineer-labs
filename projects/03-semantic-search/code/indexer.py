"""indexer.py — [partial] Milestone M1 — build a PERSISTENT Chroma collection from a corpus.

This is the "build once" half of semantic search. You embed each document a single time and store the
vectors in a Chroma collection on disk, so queries later are fast and survive restarts. The collection
must use cosine space (text embeddings) and must be IDEMPOTENT — re-running must not duplicate records.

PROVIDED: PERSIST_DIR, get_client() (a PersistentClient), SAMPLE_DOCS/SAMPLE_IDS, main().
LEARNER: build_index(). One function; the concept (persist + cosine + idempotent) is the work.

Run:  python indexer.py     (builds the index, prints collection.count())
"""
from __future__ import annotations

import os

from embedding_helpers import embed_many

PERSIST_DIR = os.path.join(os.path.dirname(__file__), ".chroma")
COLLECTION_NAME = "corpus"

# [provided] A small, deliberately mixed sample corpus (topic in metadata for filtering demos).
SAMPLE_DOCS = [
    "The central bank raised interest rates this quarter.",
    "Inflation eroded the purchasing power of household savings.",
    "A young wizard discovers he has magical powers and attends a school of magic.",
    "Photosynthesis converts sunlight into chemical energy in plants.",
    "The striker scored a last-minute goal to win the championship.",
    "The mitochondria is the powerhouse of the cell.",
]
SAMPLE_IDS = [f"d{i}" for i in range(len(SAMPLE_DOCS))]
SAMPLE_META = [{"topic": t} for t in ["finance", "finance", "fiction", "biology", "sports", "biology"]]


def get_client():
    """[provided] A PersistentClient so the index is written to disk and reused across runs."""
    import chromadb  # lazy: importing this module shouldn't require chromadb installed

    return chromadb.PersistentClient(path=PERSIST_DIR)


def build_index(
    docs: list[str],
    ids: list[str],
    metadatas: list[dict] | None = None,
    collection_name: str = COLLECTION_NAME,
) -> "chromadb.Collection":
    """[learner] Build (or update) a persistent Chroma collection and return it.

    Steps:
      1. client = get_client(); get-or-create a collection named `collection_name` with
         metadata={"hnsw:space": "cosine"}  (text embeddings → cosine, NOT the l2 default).
      2. embeddings = embed_many(docs)   (embed once, here — not per query later).
      3. add/upsert ids + embeddings + documents + metadatas. Use `upsert` (or skip ids already
         present) so re-running does NOT duplicate records.
      4. return the collection.

    Example (mirrors tests/test_indexer style — re-run is idempotent):
        col = build_index(["a", "b"], ["d0", "d1"])
        col.count()                      # -> 2
        col = build_index(["a", "b"], ["d0", "d1"])
        col.count()                      # -> 2  (still 2; no duplicates)
    """
    client = get_client()
    collection = client.get_or_create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )
    embeddings = embed_many(docs)
    collection.upsert(
        ids=ids, embeddings=embeddings, documents=docs, metadatas=metadatas
    )
    return collection


def main() -> None:
    col = build_index(SAMPLE_DOCS, SAMPLE_IDS, SAMPLE_META)
    print(f"Project 03 — Indexer. Collection '{COLLECTION_NAME}' count = {col.count()}")


if __name__ == "__main__":
    main()
