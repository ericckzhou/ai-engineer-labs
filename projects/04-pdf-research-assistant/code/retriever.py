"""retriever.py — [provided] The "R" in RAG — index chunks and retrieve top-k. This is Project 03, reused.

You already built this in Project 03 (persistent cosine collection, distance->similarity, top-k query),
so it is provided here complete: the friction in Project 04 is the NEW work — chunking, grounding,
citation, and faithfulness — not re-deriving retrieval. Read it to see how the chunk ids flow through;
the ids you set in chunker.py are what come back here and what you cite/verify against later.

PROVIDED (all of it): build_index(), retrieve().
LEARNER: nothing here — focus on chunker.py, generator.py, faithfulness.py.

Run:  python retriever.py     (needs an embedding provider: USE_OLLAMA=1 or a cloud key)
"""
from __future__ import annotations

from chunker import Chunk
from embedding_helpers import embed_many, embed_one


def build_index(chunks: list[Chunk], collection_name: str = "pdf"):
    """[provided] Build an in-memory Chroma collection from chunks (cosine space). Returns the collection.

    Uses an in-memory client so the lab demo needs no disk; swap to PersistentClient (Project 03) to
    persist. Chunk.id becomes the Chroma id; Chunk.source is stored as metadata for citations.
    """
    import chromadb

    client = chromadb.Client()
    col = client.create_collection(collection_name, metadata={"hnsw:space": "cosine"})
    col.add(
        ids=[c.id for c in chunks],
        embeddings=embed_many([c.text for c in chunks]),
        documents=[c.text for c in chunks],
        metadatas=[{"source": c.source} for c in chunks],
    )
    return col


def retrieve(collection, query: str, k: int = 4) -> list[Chunk]:
    """[provided] Retrieve the top-k chunks for `query`, nearest first. Returns Chunk objects.

    distance->similarity is handled in Project 03; here we just return the chunks in rank order so the
    generator can stuff them into the prompt with their ids.
    """
    res = collection.query(query_embeddings=[embed_one(query)], n_results=k)
    ids = res["ids"][0]
    docs = res["documents"][0]
    metas = res["metadatas"][0] or [{} for _ in ids]
    return [Chunk(id=i, text=d, source=(m or {}).get("source", "doc")) for i, d, m in zip(ids, docs, metas)]


def main() -> None:
    from chunker import chunk_text
    from pdf_loader import SAMPLE_DOC

    chunks = chunk_text(SAMPLE_DOC, chunk_size=12, overlap=3)
    col = build_index(chunks)
    hits = retrieve(col, "What was Q3 revenue?", k=2)
    print("Project 04 — Retriever")
    for c in hits:
        print(f"  {c.id}  {c.text!r}")


if __name__ == "__main__":
    main()
