"""corpus_search.py — [learner] Milestone M5 — a minimal SEMANTIC search.

Embed a small corpus, then rank it against a query by cosine similarity and return the nearest
neighbors. The top result should be the one closest in MEANING — not the one with the most shared
words. This is the literal engine of Project 03 (semantic search) and Project 04 (RAG).

PROVIDED: a sample CORPUS and main().
LEARNER: search(). Reuse embed() (M3) and cosine_similarity() (M4) — do not re-derive them.

Run:  python corpus_search.py    (needs an embedding provider)
"""
from __future__ import annotations

from embedding_explorer import embed
from similarity_calculator import cosine_similarity

# [provided] A small, deliberately mixed corpus. Note the query below shares few/no words with the
# best semantic match — that is the point.
CORPUS = [
    "The mitochondria is the powerhouse of the cell.",
    "Interest rates were raised by the central bank this quarter.",
    "A young wizard discovers he has magical powers and attends a school of magic.",
    "Photosynthesis converts sunlight into chemical energy in plants.",
    "The striker scored a last-minute goal to win the championship.",
    "Inflation eroded the purchasing power of household savings.",
]


def search(query: str, corpus: list[str], k: int = 3) -> list[tuple[str, float]]:
    """[learner] Return the top-k (text, score) pairs from `corpus`, ranked by cosine to `query`.

    Steps:
      1. embed the query ONCE.
      2. for each item in corpus: embed it, score cosine_similarity(query_vec, item_vec).
      3. sort by score descending, return the first k as (text, score) tuples.
    Edge case: an empty corpus returns []. Return at most len(corpus) results.

    Example (mirrors tests/test_corpus_search.py::test_ranks_by_meaning, which uses a fake embed
    where the query points almost exactly at "near", less at "mid", away from "far"):
        search("query", ["far", "near", "mid"], k=3)
        -> [("near", 0.99), ("mid", 0.71), ("far", 0.0)]   # ranked by cosine DESCENDING
        search("query", ["far", "near", "mid"], k=1)        -> [("near", 0.99)]   # respects k
        search("query", [], k=3)                            -> []                 # empty corpus
    """
    raise NotImplementedError("M5: implement search() - embed corpus, rank by cosine, return top-k")


# ----------------------------------------------------------------------------------------------
# [provided] Harness.
# ----------------------------------------------------------------------------------------------
def main() -> None:
    print("Project 02 — Corpus Search")
    query = "monetary policy and the economy"   # lexically unlike the finance sentences
    print(f"query: {query!r}\n")
    for rank, (text, score) in enumerate(search(query, CORPUS, k=3), start=1):
        print(f"{rank}. ({score:.3f})  {text}")


if __name__ == "__main__":
    main()
