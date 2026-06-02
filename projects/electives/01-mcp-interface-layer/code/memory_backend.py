"""memory_backend.py — [reference] The subsystem being wrapped. COMPLETE — not the learning target.

This is Project 05's personal memory system, condensed to a single self-contained file. You
already built this; here it is provided whole so your effort goes into the MCP INTERFACE
(tools/resources/prompt/security), not into rebuilding memory.

It is plain Python — it knows NOTHING about MCP. That is exactly the point: a capability and
the protocol surface that exposes it are different things. `server.py` wraps this backend; the
backend never imports `mcp`.

Offline by design
-----------------
Relevance uses a deterministic bag-of-words embedding (a token-count vector) and exact cosine,
so the server, the smoke-test client, and every test run with NO provider and NO network. This
elective is about the protocol, not embeddings — swapping in real LiteLLM/Ollama embeddings
(Project 02's "same model both sides" rule) is an extension noted in source/project.md.

Run:  python memory_backend.py     (builds a tiny store and prints a search)
"""
from __future__ import annotations

import math
import re
import time
from dataclasses import dataclass, field

# Memory kinds (Project 05 — sources/papers/memory-systems-taxonomy.md).
EPISODIC = "episodic"      # a dated event / observation
SEMANTIC = "semantic"      # a durable fact
PROCEDURAL = "procedural"  # a skill / standing instruction


@dataclass
class Memory:
    """One entry in the memory store. Faithful to Project 05's Memory, except `embedding` is a
    bag-of-words token-count map (the deterministic offline stand-in for a real vector)."""
    id: str
    text: str
    kind: str
    created_at: float
    last_accessed: float
    importance: float
    embedding: dict[str, float] = field(default_factory=dict)


def _bag_of_words(text: str) -> dict[str, float]:
    """Deterministic offline 'embedding': lowercase token counts. No hashing → no collisions."""
    counts: dict[str, float] = {}
    for tok in re.findall(r"[a-z0-9]+", text.lower()):
        counts[tok] = counts.get(tok, 0.0) + 1.0
    return counts


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    """Exact cosine similarity over two sparse token-count maps. 0.0 if either is empty."""
    if not a or not b:
        return 0.0
    dot = sum(weight * b.get(tok, 0.0) for tok, weight in a.items())
    na = math.sqrt(sum(w * w for w in a.values()))
    nb = math.sqrt(sum(w * w for w in b.values()))
    return dot / (na * nb) if na and nb else 0.0


class MemoryBackend:
    """[reference] An append-only personal memory store with relevance search. Complete.

    This is the capability your MCP server exposes. The MCP layer (tools/resources/prompt)
    calls these methods; it does not reimplement them.
    """

    def __init__(self) -> None:
        self._memories: list[Memory] = []
        self._counter: int = 0

    def save(
        self,
        text: str,
        *,
        kind: str = EPISODIC,
        importance: float = 5.0,
        now: float | None = None,
    ) -> Memory:
        """Create, store, and return a new Memory with an auto id and now-stamps."""
        ts = time.time() if now is None else now
        mem = Memory(
            id=f"m{self._counter}",
            text=text,
            kind=kind,
            created_at=ts,
            last_accessed=ts,
            importance=importance,
            embedding=_bag_of_words(text),
        )
        self._memories.append(mem)
        self._counter += 1
        return mem

    def search(self, query: str, *, k: int = 5, now: float | None = None) -> list[Memory]:
        """Return the top-k entries by relevance to `query` (exact token cosine), ranked
        descending. Entries with zero overlap are excluded. Touches `last_accessed` on the
        returned entries (Project 05's retrieval-refresh behavior)."""
        q = _bag_of_words(query)
        scored = [(m, _cosine(q, m.embedding)) for m in self._memories]
        hits = [m for m, score in sorted(scored, key=lambda p: p[1], reverse=True) if score > 0.0]
        hits = hits[: max(0, k)]
        ts = time.time() if now is None else now
        for m in hits:
            m.last_accessed = ts
        return hits

    def get(self, entry_id: str) -> Memory | None:
        return next((m for m in self._memories if m.id == entry_id), None)

    def all_entries(self) -> list[Memory]:
        """Every entry in insertion order."""
        return list(self._memories)

    def __len__(self) -> int:
        return len(self._memories)


def main() -> None:
    backend = MemoryBackend()
    backend.save("the StarcallOS demo is on June 20", kind=EPISODIC, importance=8)
    backend.save("I prefer dark mode", kind=SEMANTIC, importance=6)
    backend.save("format commit messages in imperative mood", kind=PROCEDURAL, importance=7)
    print(f"MemoryBackend — {len(backend)} entries")
    for m in backend.search("when is the demo", k=3):
        print(f"  {m.id} [{m.kind:10}] imp={m.importance:<4} {m.text!r}")


if __name__ == "__main__":
    main()
