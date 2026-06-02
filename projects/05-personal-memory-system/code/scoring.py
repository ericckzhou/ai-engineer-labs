"""scoring.py — [learner] Milestones M1–M3 — the retrieval score. THIS is the core of Project 05.

A memory system is more than RAG-over-your-history. RAG ranks by ONE signal (relevance). A memory
system ranks by THREE — relevance (is it about this?), recency (is it fresh?), importance (does it
matter?) — and sums them (sources/papers/generative-agents.md). These four pure functions ARE that
score. Get them right and the retriever (retriever.py) is just "score all, sort, take k."

  relevance  = cosine(query_embedding, memory_embedding)          (Project 02 machinery)
  recency    = decay_rate ** (hours since the memory was last accessed)   ← exponential decay
  importance = salience / 10                                       (1–10, set at write time)
  score      = w_rel*relevance + w_rec*recency + w_imp*importance

PROVIDED: nothing here is solved — all four are yours. (config.py supplies decay_rate + weights.)
LEARNER: recency_score, importance_score, relevance_score, retrieval_score. Pure math; tests run offline.

Run:  python -m pytest tests/test_scoring.py
"""
from __future__ import annotations

import math

_SECONDS_PER_HOUR = 3600.0


def recency_score(now: float, last_accessed: float, decay_rate: float = 0.995,
                  unit_seconds: float = _SECONDS_PER_HOUR) -> float:
    """[learner] Exponential time decay: how "fresh" a memory is, in [0, 1].

    Steps:
      1. elapsed = now - last_accessed        (epoch seconds; both args are timestamps)
      2. hours   = elapsed / unit_seconds     (convert to the decay unit — default hours)
      3. return decay_rate ** hours
    Notes / traps:
      - At elapsed == 0 this is decay_rate ** 0 == 1.0 (a just-touched memory is maximally fresh).
      - decay_rate is in (0, 1): smaller forgets faster. The paper uses 0.995 (sources/papers/generative-agents.md).
      - Guard the degenerate case elapsed < 0 (clock skew) by clamping hours to >= 0, so recency never
        exceeds 1.0.
      - This is measured from LAST ACCESS, not creation — retriever.retrieve() must touch last_accessed
        so frequently-used memories stay fresh. (That touch lives in retriever.py, not here.)

    Example (mirrors tests/test_scoring.py::test_recency_decays_by_the_hour):
        now = 1_000_000.0;  hour = 3600.0
        recency_score(now, now)             -> 1.0        # 0 hours
        recency_score(now, now - hour)      -> 0.995      # 1 hour,  0.995 ** 1
        recency_score(now, now - 2 * hour)  -> 0.990025   # 2 hours, 0.995 ** 2
    """
    elapsed = now - last_accessed
    hours = max(elapsed, 0.0) / unit_seconds  # clamp clock skew so recency never exceeds 1.0
    return decay_rate ** hours


def importance_score(importance: float, max_scale: float = 10.0) -> float:
    """[learner] Normalize a salience rating (1–10) to [0, 1].

    Steps:
      1. return importance / max_scale
      2. clamp into [0, 1] so an out-of-range rating can't dominate the sum.
    Notes:
      - Importance is set ONCE, at write time (mundane=1 ... core=10) — not recomputed per query
        (sources/papers/generative-agents.md). This function only rescales it.

    Example (mirrors tests/test_scoring.py::test_importance_normalizes_1_to_10):
        importance_score(10) -> 1.0
        importance_score(5)  -> 0.5
        importance_score(1)  -> 0.1
    """
    return max(0.0, min(1.0, importance / max_scale))


def relevance_score(query_vec: list[float], mem_vec: list[float]) -> float:
    """[learner] Semantic relevance = cosine similarity between the query and the memory embedding.

    Steps:
      1. dot   = sum(a*b for a, b in zip(query_vec, mem_vec))
      2. norms = sqrt(sum(a*a)) * sqrt(sum(b*b))
      3. return dot / norms   (guard norms == 0 -> return 0.0)
    Notes / traps:
      - This is Project 02's cosine similarity, unchanged. cos in [-1, 1]; for related normalized
        embeddings it sits in ~[0, 1].
      - Both vectors must come from the SAME embedding model (config.py) or the number is meaningless
        — the silent bug carried from Project 02.

    Example (mirrors tests/test_scoring.py::test_relevance_is_cosine):
        relevance_score([1, 0, 0], [1, 0, 0]) -> 1.0    # identical direction
        relevance_score([1, 0, 0], [0, 1, 0]) -> 0.0    # orthogonal
    """
    dot = sum(a * b for a, b in zip(query_vec, mem_vec))
    norms = math.sqrt(sum(a * a for a in query_vec)) * math.sqrt(sum(b * b for b in mem_vec))
    if norms == 0:
        return 0.0
    return dot / norms


def retrieval_score(rel: float, rec: float, imp: float,
                    weights: tuple[float, float, float] = (1.0, 1.0, 1.0)) -> float:
    """[learner] Combine the three signals into one rank-able number.

    Steps:
      1. unpack w_rel, w_rec, w_imp = weights        (order: relevance, recency, importance)
      2. return w_rel*rel + w_rec*rec + w_imp*imp
    Notes:
      - Equal weights (1,1,1) is the paper's default (sources/papers/generative-agents.md). The weights
        are the design knob: raise w_rec for a chat assistant, raise w_imp to never forget core facts.
      - The paper min-max normalizes each component across the candidate set before summing; here each
        component is already bounded in [0,1], so a plain weighted sum is the lab simplification.

    Example (mirrors tests/test_scoring.py::test_combined_score_needs_all_three):
        retrieval_score(rel=0.8, rec=0.9, imp=0.7)            -> 2.4    # equal weights
        retrieval_score(0.9, 0.1, 0.3)                        -> 1.3    # relevant but old
        retrieval_score(0.1, 1.0, 0.2)                        -> 1.3    # fresh but off-topic
        # → the 2.4 memory (relevant AND fresh AND important) wins.
    """
    w_rel, w_rec, w_imp = weights
    return w_rel * rel + w_rec * rec + w_imp * imp


def main() -> None:
    print("Project 05 — scoring (implement the four functions, then this prints real numbers)")
    now = 1_000_000.0
    for label, fn in (
        ("recency(0h)", lambda: recency_score(now, now)),
        ("importance(10)", lambda: importance_score(10)),
        ("relevance(parallel)", lambda: relevance_score([1, 0, 0], [1, 0, 0])),
        ("score(.8,.9,.7)", lambda: retrieval_score(0.8, 0.9, 0.7)),
    ):
        try:
            print(f"  {label:22} = {fn()}")
        except NotImplementedError as e:
            print(f"  {label:22} -> TODO ({e})")


if __name__ == "__main__":
    # math is imported for learners who reach for math.sqrt in relevance_score.
    _ = math
    main()
