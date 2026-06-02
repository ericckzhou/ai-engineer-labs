"""chat_with_memory.py — [provided] The end-to-end loop that wires the memory system together.

This orchestrator is provided so you can see the whole flow at once. It calls the functions YOU
implement (scoring.py via retriever.retrieve) and will raise NotImplementedError until they're done —
that is the point: fill in scoring.py then retriever.py and watch this come alive.

Loop (per user turn):
    embed query ─► RETRIEVE top-k memories ─► inject into the prompt (main context) ─► LLM answers
                                                                                          │
                          store the new turn back into the stream (write-back) ◄──────────┘

  retrieve  → retriever.py (you)        inject/answer → here (provided, Project 01 message construction)
  score     → scoring.py (you)          write-back    → here (provided, memory_store.remember)

Run:  python chat_with_memory.py            (interactive; needs a provider: USE_OLLAMA=1 or a cloud key)
      python chat_with_memory.py --seed     (preload a few memories, ask one question, exit)
"""
from __future__ import annotations

import sys
import time

from config import load_config
from embedding_helpers import embed_one
from memory_store import EPISODIC, SEMANTIC, MemoryStore
from retriever import retrieve

_SYSTEM = (
    "You are a personal assistant with long-term memory. Use the RELEVANT MEMORIES below to answer "
    "as if you genuinely remember the user. If the memories don't cover the question, just answer "
    "normally — do not invent memories."
)


def _build_messages(query: str, memories) -> list[dict]:
    """[provided] Project 01 message construction: system + retrieved memories as context + the question."""
    if memories:
        block = "\n".join(f"- ({m.kind}) {m.text}" for m in memories)
    else:
        block = "(no relevant memories yet)"
    user = f"RELEVANT MEMORIES:\n{block}\n\nUser: {query}"
    return [{"role": "system", "content": _SYSTEM}, {"role": "user", "content": user}]


def answer_with_memory(query: str, store: MemoryStore, cfg, now: float | None = None) -> str:
    """[provided] One turn: embed → retrieve → inject → answer → write the turn back."""
    import litellm

    ts = time.time() if now is None else now
    q_vec = embed_one(query)
    memories = retrieve(store, q_vec, now=ts, k=cfg.top_k, weights=cfg.weights, decay_rate=cfg.decay_rate)

    messages = _build_messages(query, memories)
    resp = litellm.completion(model=cfg.model, messages=messages,
                              temperature=cfg.temperature, max_tokens=cfg.max_tokens)
    reply = resp["choices"][0]["message"]["content"]

    # Write-back: remember the user's turn so the stream grows (importance default is neutral; rating
    # it 1–10 with the model is the lesson's extension).
    store.remember(query, q_vec, kind=EPISODIC, importance=5.0, now=ts)
    return reply


def _seed(store: MemoryStore, now: float) -> None:
    """[provided] A few starter memories so --seed shows retrieval working without a long chat."""
    for text, kind, imp in [
        ("The user prefers the Groq API as the default provider.", SEMANTIC, 8),
        ("The user is building StarcallOS.", SEMANTIC, 7),
        ("The user had coffee this morning.", EPISODIC, 1),
    ]:
        store.remember(text, embed_one(text), kind=kind, importance=imp, now=now)


def main() -> None:
    cfg = load_config()
    store = MemoryStore()
    print(f"Project 05 — Chat with Memory   (model: {cfg.model}, top_k={cfg.top_k})")

    if "--seed" in sys.argv:
        now = time.time()
        _seed(store, now)
        q = "Which API should I default to, and what am I building?"
        print(f"\nUser: {q}")
        print(f"Assistant: {answer_with_memory(q, store, cfg, now=now)}")
        return

    print("Type a message (Ctrl-C to exit). The assistant remembers across turns.\n")
    try:
        while True:
            q = input("You: ").strip()
            if not q:
                continue
            print(f"Assistant: {answer_with_memory(q, store, cfg)}\n")
    except (KeyboardInterrupt, EOFError):
        print("\n(bye)")


if __name__ == "__main__":
    main()
