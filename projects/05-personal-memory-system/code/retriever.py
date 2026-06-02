"""retriever.py — [learner] Milestone M4 — page the top-k memories into the prompt budget.

This is MemGPT's paging step (sources/papers/memgpt.md): the memory stream is large ("external
context"); the prompt is small ("main context"). retrieve() picks the few memories worth loading by
scoring every memory with scoring.py and taking the best `k`. It takes the query EMBEDDING (a vector),
not text, so it stays pure and offline-testable — the orchestrator (chat_with_memory.py) embeds the
query and hands you the vector.

The one easy-to-miss step: retrieval must TOUCH each returned memory's last_accessed (= now). Recency
is measured from last access, so using a memory should keep it fresh (sources/papers/generative-agents.md).

PROVIDED: nothing — retrieve() is yours. (It composes the four functions you wrote in scoring.py.)
LEARNER: retrieve(). Pure logic; tests/test_retriever.py runs offline with hand-built vectors + timestamps.

Run:  python -m pytest tests/test_retriever.py
"""
from __future__ import annotations

from memory_store import Memory, MemoryStore
from scoring import importance_score, recency_score, relevance_score, retrieval_score


def retrieve(
    store: MemoryStore,
    query_embedding: list[float],
    now: float,
    k: int = 5,
    weights: tuple[float, float, float] = (1.0, 1.0, 1.0),
    decay_rate: float = 0.995,
) -> list[Memory]:
    """[learner] Return the top-`k` memories for a query, ranked by the three-signal score.

    Steps:
      1. For each memory m in store.all(), compute its three components:
           rel = relevance_score(query_embedding, m.embedding)
           rec = recency_score(now, m.last_accessed, decay_rate)
           imp = importance_score(m.importance)
         then score = retrieval_score(rel, rec, imp, weights).
      2. Sort the memories by score, DESCENDING.
      3. Take the top `k` (slice [:k]).
      4. TOUCH each returned memory: set m.last_accessed = now (retrieval refreshes recency — the
         step that's easy to forget, and the whole reason recency is from "last access" not "created").
      5. Return the list of Memory objects, highest score first.
    Notes / traps:
      - Touch AFTER scoring, not before — otherwise every memory looks maximally recent and recency
        stops discriminating.
      - Ties on relevance (e.g. identical embeddings) are broken by recency + importance — that is the
        point of the system (see Example).

    Example (mirrors tests/test_retriever.py::test_recency_and_importance_break_a_relevance_tie):
        now = 1_000_000.0
        store has two memories with the SAME embedding [1,0,0]:
          m0 "brushed teeth"   imp=1, last_accessed = now - 1e6   (trivial + old)
          m1 "chose Groq"      imp=8, last_accessed = now - 10    (important + fresh)
        retrieve(store, [1,0,0], now=now, k=1)  ->  [m1]      # relevance ties; recency+importance win
        # and afterwards m1.last_accessed == now  (it was touched)
    """
    scored: list[tuple[float, Memory]] = []
    for m in store.all():
        rel = relevance_score(query_embedding, m.embedding)
        rec = recency_score(now, m.last_accessed, decay_rate)
        imp = importance_score(m.importance)
        scored.append((retrieval_score(rel, rec, imp, weights), m))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    top = [m for _, m in scored[:k]]

    # Touch AFTER scoring so retrieval refreshes recency without skewing this turn's ranking.
    for m in top:
        m.last_accessed = now
    return top


def main() -> None:
    now = 1_000_000.0
    store = MemoryStore()
    store.add(Memory("m0", "brushed teeth", kind="episodic", created_at=now - 1e6,
                     last_accessed=now - 1e6, importance=1, embedding=[1.0, 0.0, 0.0]))
    store.add(Memory("m1", "decided to default to Groq", kind="semantic", created_at=now - 10,
                     last_accessed=now - 10, importance=8, embedding=[1.0, 0.0, 0.0]))
    print("Project 05 — Retriever")
    hits = retrieve(store, [1.0, 0.0, 0.0], now=now, k=2)
    for m in hits:
        print(f"  {m.id}  imp={m.importance}  {m.text!r}")


if __name__ == "__main__":
    main()
