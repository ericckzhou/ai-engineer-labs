"""evaluate.py — [learner] Milestone M5 — measure the ANN index, don't eyeball it.

Run several queries through BOTH paths — the Chroma ANN index and the exact brute-force baseline over
the same vectors — and report recall@k. "It seemed to work" is not evaluation; a recall number is.

PROVIDED: sample QUERIES, main() printing a recall table.
LEARNER: evaluate().

Run:  python evaluate.py      (needs an embedding provider)
"""
from __future__ import annotations

import numpy as np

from baseline import exact_rank, recall_at_k
from embedding_helpers import embed_many, embed_one

QUERIES = [
    "monetary policy and the economy",
    "a story about wizards and magic",
    "how cells produce energy",
]


def evaluate(collection, docs: list[str], ids: list[str], queries: list[str], k: int = 3) -> dict:
    """[learner] Return {'per_query': {query: recall}, 'mean_recall': float}.

    For each query:
      1. ANN: collection.query(query_embeddings=[embed_one(query)], n_results=k) -> ann ids ->
         map each returned id back to its index in `ids` to get ann_idx.
      2. Exact: embed the docs (embed_many(docs)), exact_rank(embed_one(query), doc_vecs, k) -> exact_idx.
      3. recall_at_k(ann_idx, exact_idx, k).
    Then average across queries for 'mean_recall'.

    Example (mirrors tests/test_evaluate.py — tiny corpus, ANN matches exact):
        evaluate(col, docs, ids, ["interest rates", "magic school"], k=1)
        -> {"per_query": {"interest rates": 1.0, "magic school": 1.0}, "mean_recall": 1.0}
    """
    raise NotImplementedError("M5: implement evaluate() - recall@k of ANN vs exact baseline per query")


def main() -> None:
    from indexer import build_index, SAMPLE_DOCS, SAMPLE_IDS, SAMPLE_META

    col = build_index(SAMPLE_DOCS, SAMPLE_IDS, SAMPLE_META)
    report = evaluate(col, SAMPLE_DOCS, SAMPLE_IDS, QUERIES, k=3)
    print("Project 03 — Evaluation (recall@3, ANN vs exact baseline)")
    for q, r in report["per_query"].items():
        print(f"  {r:.2f}  {q}")
    print(f"  mean recall = {report['mean_recall']:.3f}")


if __name__ == "__main__":
    main()
