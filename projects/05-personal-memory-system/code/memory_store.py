"""memory_store.py — [provided] The memory data model + an in-memory stream. NOT the learning target.

This is the "external context" / "disk" of the system (sources/papers/memgpt.md): a growing list of
memory objects you retrieve from. It's provided so your effort goes into the SCORING and RETRIEVAL
(scoring.py, retriever.py), not the bookkeeping. The one method you may want to touch is how importance
is assigned at write time (a fixed default here; LLM-rated poignancy is an extension — see the lesson).

A `Memory` carries everything the retrieval score needs:
  - embedding      → relevance  (cosine vs the query)
  - last_accessed  → recency    (exponential decay; retrieval refreshes this)
  - importance     → importance (salience 1–10, set once at write time)
  - kind           → episodic / semantic / procedural (sources/papers/memory-systems-taxonomy.md)

Run:  python memory_store.py     (builds a tiny stream and prints it)
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field

# Memory kinds (sources/papers/memory-systems-taxonomy.md). Episodic decays; semantic/procedural are durable.
EPISODIC = "episodic"     # a dated event / observation ("you told me X on Tuesday")
SEMANTIC = "semantic"     # a durable fact ("you prefer dark mode")
PROCEDURAL = "procedural"  # a skill / standing instruction ("format commits like this")


@dataclass
class Memory:
    """[provided] One entry in the memory stream. `embedding`, `last_accessed`, and `importance`
    are the three inputs to the retrieval score. `last_accessed` is mutable on purpose — retrieval
    touches it (sources/papers/generative-agents.md)."""
    id: str
    text: str
    kind: str                       # EPISODIC / SEMANTIC / PROCEDURAL
    created_at: float               # epoch seconds, set at write time
    last_accessed: float            # epoch seconds, refreshed every time this memory is retrieved
    importance: float               # salience 1..10, assigned once at write time
    embedding: list[float] = field(default_factory=list)


class MemoryStore:
    """[provided] An append-only, in-memory memory stream. Persistence (disk / Chroma) is an extension."""

    def __init__(self) -> None:
        self._memories: list[Memory] = []
        self._counter: int = 0

    def add(self, memory: Memory) -> Memory:
        """Append a fully-formed Memory (you built it elsewhere) and return it."""
        self._memories.append(memory)
        self._counter = max(self._counter, _id_num(memory.id) + 1)
        return memory

    def remember(
        self,
        text: str,
        embedding: list[float],
        *,
        kind: str = EPISODIC,
        importance: float = 5.0,
        now: float | None = None,
    ) -> Memory:
        """Convenience writer: build a Memory with an auto id and now-stamps, append it, return it.

        importance defaults to a neutral 5.0 — assigning a real 1–10 salience (LLM-rated) is the
        extension in the lesson. created_at == last_accessed == now at birth.
        """
        ts = time.time() if now is None else now
        mem = Memory(
            id=f"m{self._counter}",
            text=text,
            kind=kind,
            created_at=ts,
            last_accessed=ts,
            importance=importance,
            embedding=list(embedding),
        )
        return self.add(mem)

    def all(self) -> list[Memory]:
        """Every memory in the stream (insertion order). The retriever scores over this."""
        return list(self._memories)

    def get(self, memory_id: str) -> Memory | None:
        return next((m for m in self._memories if m.id == memory_id), None)

    def __len__(self) -> int:
        return len(self._memories)


def _id_num(memory_id: str) -> int:
    """Parse the trailing integer of an id like 'm3' -> 3; -1 if it doesn't match."""
    digits = memory_id[1:] if memory_id[:1] == "m" else ""
    return int(digits) if digits.isdigit() else -1


def main() -> None:
    store = MemoryStore()
    store.remember("you prefer dark mode", [1.0, 0.0, 0.0], kind=SEMANTIC, importance=7, now=1_000_000.0)
    store.remember("brushed teeth", [0.0, 1.0, 0.0], kind=EPISODIC, importance=1, now=1_000_000.0)
    print(f"Project 05 — MemoryStore ({len(store)} memories)")
    for m in store.all():
        print(f"  {m.id}  [{m.kind:10}] imp={m.importance:<4} {m.text!r}")


if __name__ == "__main__":
    main()
