"""rerank.py — [learner, EXTENDED/optional] Milestone M6 — two-stage retrieve-then-rerank.

First-stage retrieval (the vector DB) is fast but only approximately orders results. A cross-encoder
scores the (query, document) PAIR jointly and is more accurate — but too slow to run over a whole
corpus. So the production pattern is: retrieve top-k cheaply with search(), then re-rank ONLY those k
with the cross-encoder. (source: sources/articles/sbert-retrieve-rerank.md)

PROVIDED: get_cross_encoder() (lazy-loads a small cross-encoder), main().
LEARNER: rerank(). Optional — do this after the core M1–M5 work.

Run:  python rerank.py     (downloads a small cross-encoder model on first run)
"""
from __future__ import annotations

_CROSS_ENCODER = None


def get_cross_encoder():
    """[provided] Lazy-load a small cross-encoder (sentence-transformers)."""
    global _CROSS_ENCODER
    if _CROSS_ENCODER is None:
        from sentence_transformers import CrossEncoder

        _CROSS_ENCODER = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return _CROSS_ENCODER


def rerank(query: str, candidates: list[str]) -> list[tuple[str, float]]:
    """[learner] Re-score each (query, candidate) pair with the cross-encoder and return the
    candidates sorted by score DESCENDING. Only ever call this on the small candidate set returned
    by search() — never the whole corpus.

    Steps:
      1. model = get_cross_encoder()
      2. scores = model.predict([(query, c) for c in candidates])
      3. return [(candidate, float(score))] sorted by score descending.

    Example (mirrors tests/test_rerank.py with a stubbed model):
        rerank("interest rates", ["The central bank raised rates.", "A wizard cast a spell."])
        -> [("The central bank raised rates.", 8.2), ("A wizard cast a spell.", -6.1)]
        # the on-topic candidate is re-ranked first
    """
    raise NotImplementedError("M6 (extended): implement rerank() - cross-encoder re-score top-k")


def main() -> None:
    query = "interest rates and the economy"
    candidates = [
        "A young wizard attends a school of magic.",
        "The central bank raised interest rates this quarter.",
        "Photosynthesis converts sunlight into energy.",
    ]
    print(f"Project 03 — Re-rank\nquery: {query!r}\n")
    for rank, (doc, score) in enumerate(rerank(query, candidates), start=1):
        print(f"{rank}. ({score:+.2f})  {doc}")


if __name__ == "__main__":
    main()
