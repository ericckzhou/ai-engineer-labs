"""semantic_search.py — [learner] Milestones M2 + M3 — the CORE of Project 03.

Query the vector DB and return human-readable ranked results. Two traps to get right:
  1. Chroma returns DISTANCES, not similarities — lower distance = MORE similar. Sorting the wrong
     way returns your WORST matches with no error (the silent inversion bug).
  2. With space="cosine", cosine distance is in [0, 2]; similarity = 1 - distance, in [-1, 1].

PROVIDED: main() (builds/loads the index and prints ranked results for a sample query).
LEARNER: to_similarity() and search().

Run:  python semantic_search.py      (needs an embedding provider; USE_OLLAMA=1 or a cloud key)
"""
from __future__ import annotations

from embedding_helpers import embed_one


def to_similarity(distance: float) -> float:
    """[learner] Convert a Chroma cosine DISTANCE into a cosine SIMILARITY.

    For space="cosine": similarity = 1 - distance.

    Example (mirrors tests/test_search.py::test_to_similarity):
        to_similarity(0.0)  -> 1.0     # identical direction
        to_similarity(0.3)  -> 0.7
        to_similarity(1.0)  -> 0.0     # orthogonal
    """
    return 1.0 - distance


def search(collection, query: str, k: int = 5) -> list[tuple[str, float, dict]]:
    """[learner] Return the top-k results for `query`, ranked by SIMILARITY DESCENDING.

    Steps:
      1. qv = embed_one(query)                         (embed the query once)
      2. res = collection.query(query_embeddings=[qv], n_results=k)
      3. zip res["documents"][0], res["distances"][0], res["metadatas"][0]
      4. convert each distance with to_similarity(), and return
         [(document, similarity, metadata)] sorted by similarity DESCENDING
         (equivalently: distance ascending — Chroma already returns nearest first).
    Edge case: an empty collection / no results -> return [].

    Example (mirrors tests/test_search.py::test_search_ranks_by_meaning — a cosine collection with
    d0≈finance, d1≈fiction, d2≈biology and a finance-leaning query):
        search(col, "monetary policy and the economy", k=2)
        -> [("The central bank raised interest rates this quarter.", 0.99, {"topic": "finance"}),
            ("Inflation eroded the purchasing power of household savings.", 0.61, {"topic": "finance"})]
        # finance doc first; similarities DESCENDING; values are 1 - distance (NOT raw distances)
    """
    qv = embed_one(query)
    res = collection.query(query_embeddings=[qv], n_results=k)
    docs = res["documents"][0]
    distances = res["distances"][0]
    metadatas = res["metadatas"][0]
    if not docs:
        return []
    results = [
        (doc, to_similarity(dist), meta)
        for doc, dist, meta in zip(docs, distances, metadatas)
    ]
    results.sort(key=lambda triple: triple[1], reverse=True)
    return results


def main() -> None:
    from indexer import build_index, SAMPLE_DOCS, SAMPLE_IDS, SAMPLE_META

    col = build_index(SAMPLE_DOCS, SAMPLE_IDS, SAMPLE_META)
    query = "monetary policy and the economy"
    print(f"Project 03 — Semantic Search\nquery: {query!r}\n")
    for rank, (doc, sim, meta) in enumerate(search(col, query, k=3), start=1):
        print(f"{rank}. (sim {sim:+.3f}) [{meta.get('topic','?')}]  {doc}")


if __name__ == "__main__":
    main()
