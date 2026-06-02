"""subsystems.py — [provided] The capability kernel: offline stand-ins for P01/P03/P05/P08.

These are the "workers" the orchestrator routes to. You ALREADY BUILT each of them in an earlier
project — so here they are provided in full, and your effort goes to the COMPOSITION (the router,
the orchestrator, the graph, the system-level eval). Everything here runs OFFLINE: the memory store
is in-memory with keyword-overlap recall, and the model call is injected as `chat` (the real app
passes a LiteLLM-backed one; tests pass a fake).

What's here:
  - Item / MemoryStore        — the personal store (save + keyword recall)   [stands in for P03/P05]
  - SubsystemResult           — what every worker returns: (answer, sources used)
  - the four workers          — save / recall / task / chat
  - make_subsystems(...)      — builds the route→worker DISPATCH TABLE the orchestrator uses

PROVIDED in full. Read it; do not edit it to do your milestones. Re-read projects 05 and 08 if any
worker is unfamiliar.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Callable

from knowledge import KnowledgeGraph

# A tiny stopword list so tag extraction / recall key off content words, not filler.
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "to", "of", "in", "on", "for", "with", "that", "this",
    "is", "are", "was", "were", "be", "been", "it", "its", "i", "me", "my", "we", "you", "your",
    "about", "what", "did", "do", "does", "have", "has", "had", "remember", "note", "save", "saved",
    "store", "keep", "find", "search", "recall", "summarize", "summarise", "everything", "all",
    "go", "through", "draft", "make", "please", "can", "could", "would", "tell", "show", "give",
    "from", "by", "as", "at", "so", "if", "then", "than", "into", "out", "up", "down", "over",
}


def _tokens(text: str) -> list[str]:
    """Lowercase word tokens (alphanumeric runs)."""
    return re.findall(r"[a-z0-9]+", text.lower())


def extract_tags(text: str, limit: int = 8) -> set[str]:
    """Content words of `text` as tags: lowercased, stopwords + 2-char words dropped, deduped."""
    tags = [t for t in _tokens(text) if len(t) > 2 and t not in _STOPWORDS]
    # preserve first-seen order, cap the count
    seen: list[str] = []
    for t in tags:
        if t not in seen:
            seen.append(t)
    return set(seen[:limit])


@dataclass
class Item:
    """[provided] One stored memory: an id, the text, its tags, and when it was created."""
    id: int
    text: str
    tags: set
    created_at: float


class MemoryStore:
    """[provided] An in-memory personal store. Stands in for the P05 memory system (P03 retrieval).

    save(text, tags) -> Item        : append a new item, return it (with a fresh id).
    recall(query, k) -> list[Item]  : keyword-overlap ranking — items sharing the most query words,
                                      ties broken by recency. Items with no overlap are excluded.
    """

    def __init__(self) -> None:
        self._items: list[Item] = []
        self._next_id = 1

    def save(self, text: str, tags: set | None = None) -> Item:
        item = Item(id=self._next_id, text=text.strip(),
                    tags=set(tags) if tags else extract_tags(text), created_at=time.time())
        self._items.append(item)
        self._next_id += 1
        return item

    def recall(self, query: str, k: int = 5) -> list[Item]:
        q = set(_tokens(query)) - _STOPWORDS
        scored: list[tuple[int, float, Item]] = []
        for item in self._items:
            words = set(_tokens(item.text)) | {t.lower() for t in item.tags}
            overlap = len(q & words)
            if overlap:
                scored.append((overlap, item.created_at, item))
        scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
        return [item for _, _, item in scored[:k]]

    def get(self, item_id: int) -> Item | None:
        return next((it for it in self._items if it.id == item_id), None)

    def all(self) -> list[Item]:
        return list(self._items)


@dataclass
class SubsystemResult:
    """[provided] What every worker returns: the answer text + the sources (item ids) it used."""
    answer: str
    sources: list = field(default_factory=list)


# ---- the four workers (each: (query) -> SubsystemResult) ----------------------
# Built by make_subsystems(), which closes over the store, graph, and injected `chat`.

def _strip_save_trigger(text: str) -> str:
    """Drop a leading 'remember that' / 'note:' / 'save this' so we store the CONTENT, not the verb."""
    patterns = [
        r"^\s*(please\s+)?remember(\s+that|\s+to)?\s*[:,-]?\s*",
        r"^\s*note(\s+that)?\s*[:,-]?\s*",
        r"^\s*(save|store|keep)(\s+this|\s+that)?\s*[:,-]?\s*",
        r"^\s*don'?t\s+forget(\s+that|\s+to)?\s*[:,-]?\s*",
        r"^\s*(jot\s+down|make\s+a\s+note(\s+of)?)\s*[:,-]?\s*",
    ]
    out = text.strip()
    for p in patterns:
        out = re.sub(p, "", out, flags=re.IGNORECASE)
    return out.strip() or text.strip()


def make_subsystems(store: MemoryStore, graph: KnowledgeGraph,
                    chat: Callable[[list], str]) -> dict[str, Callable[[str], SubsystemResult]]:
    """[provided] Build the route → worker DISPATCH TABLE the orchestrator dispatches through.

    Each worker fully OWNS its capability:
      - SAVE  : persist the item AND link it into the knowledge graph (so handle never touches them).
      - RECALL: keyword-recall from the store.
      - TASK  : a small bounded multi-recall + synthesis shim (stands in for P08's agent).
      - CHAT  : a single model call (P01).
    """

    def save_worker(query: str) -> SubsystemResult:
        content = _strip_save_trigger(query)
        tags = extract_tags(content)
        item = store.save(content, tags)
        graph.add(item.id, item.tags, min_shared=1)  # the SAVE worker owns the graph link
        return SubsystemResult(answer=f"Saved (#{item.id}): {item.text}", sources=[item.id])

    def recall_worker(query: str) -> SubsystemResult:
        items = store.recall(query, k=5)
        if not items:
            return SubsystemResult(answer="I don't have anything saved about that.", sources=[])
        lines = [f"  - (#{it.id}) {it.text}" for it in items]
        return SubsystemResult(answer="Here's what you saved:\n" + "\n".join(lines),
                               sources=[it.id for it in items])

    def task_worker(query: str) -> SubsystemResult:
        # A bounded shim for P08's agent: gather context from the store, then synthesize with one call.
        items = store.recall(query, k=5)
        context = "\n".join(f"(#{it.id}) {it.text}" for it in items) or "(no relevant saved items)"
        messages = [
            {"role": "system", "content": "Synthesize a concise answer from the user's saved notes. "
                                          "Cite item ids like (#3) you used."},
            {"role": "user", "content": f"Task: {query}\n\nSaved notes:\n{context}"},
        ]
        answer = chat(messages)
        return SubsystemResult(answer=answer, sources=[it.id for it in items])

    def chat_worker(query: str) -> SubsystemResult:
        answer = chat([{"role": "user", "content": query}])
        return SubsystemResult(answer=answer, sources=[])

    return {"SAVE": save_worker, "RECALL": recall_worker, "TASK": task_worker, "CHAT": chat_worker}
