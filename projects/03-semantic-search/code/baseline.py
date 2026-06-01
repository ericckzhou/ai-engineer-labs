"""baseline.py — [partial] Milestones M4 + M5 — the EXACT baseline that validates the ANN index.

Chroma's HNSW search is APPROXIMATE: fast, but it can occasionally miss a true nearest neighbor. The
only way to know it is good enough is to compare against an EXACT brute-force cosine ranking (Project
02 style) and measure recall@k. This module is that exact baseline + the recall metric.

PROVIDED: main() demo.
LEARNER: cosine_similarity() (carry from Project 02), exact_rank(), recall_at_k().
These are pure numpy — the guiding tests in tests/test_baseline.py run fully offline.

Run:  python baseline.py
"""
from __future__ import annotations

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """[learner] Cosine similarity from scratch (no library helper). Range [-1, 1].

    cos(a,b) = (a·b) / (‖a‖·‖b‖)

    Example (mirrors tests/test_baseline.py::test_cosine_*):
        cosine_similarity(np.array([1,0]), np.array([3,4]))  -> 0.6
        cosine_similarity(v, v)   -> 1.0
        cosine_similarity(v, -v)  -> -1.0
    """
    raise NotImplementedError("M4: implement cosine_similarity() from scratch")


def exact_rank(query_vec: np.ndarray, doc_vecs: list[np.ndarray], k: int) -> list[int]:
    """[learner] Return the indices of the top-k docs by EXACT cosine, similarity descending.

    Example (mirrors tests/test_baseline.py::test_exact_rank — q points at index 0):
        docs = [np.array([1,0]), np.array([0,1]), np.array([0.9,0.1])]
        exact_rank(np.array([1,0]), docs, k=2)  -> [0, 2]   # doc0 then doc2; doc1 (orthogonal) excluded
    """
    raise NotImplementedError("M4: implement exact_rank() - top-k indices by cosine, desc")


def recall_at_k(approx_ids: list[int], exact_ids: list[int], k: int) -> float:
    """[learner] Fraction of the exact top-k that the approximate (ANN) top-k also found. [0, 1].

    recall@k = |set(approx[:k]) ∩ set(exact[:k])| / k

    Example (mirrors tests/test_baseline.py::test_recall_at_k):
        recall_at_k([0, 2, 5], [0, 2, 9], k=3)  -> 0.6667   # two of three overlap
        recall_at_k([0, 1, 2], [0, 1, 2], k=3)  -> 1.0
    """
    raise NotImplementedError("M5: implement recall_at_k() - overlap of approx vs exact top-k")


def main() -> None:
    docs = [np.array([1.0, 0.0]), np.array([0.0, 1.0]), np.array([0.9, 0.1])]
    q = np.array([1.0, 0.0])
    print("Project 03 — Exact Baseline")
    print("exact_rank(q, docs, 2) =", exact_rank(q, docs, 2))
    print("recall_at_k([0,2,5],[0,2,9],3) =", round(recall_at_k([0, 2, 5], [0, 2, 9], 3), 4))


if __name__ == "__main__":
    main()
