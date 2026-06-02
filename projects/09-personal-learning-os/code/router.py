"""router.py — [learner] Milestone M1 — the system's FRONT DOOR: classify a request into one route.

This is the heart of the capstone. The Personal Learning OS has one entrypoint, but four specialists
behind it (SAVE, RECALL, TASK, CHAT). `route_query` decides which one a request belongs to. Routing
"classifies an input and directs it to a specialized followup task" and buys "separation of concerns"
— each subsystem gets a narrower, more reliable job (sources/articles/building-effective-agents.md).

Two things make this a DESIGN decision, not a string match:
  1. PRECEDENCE. The routes are checked in order of the *cost of a mistake*: SAVE ▸ RECALL ▸ TASK.
     A dropped "remember this" is silent DATA LOSS, so SAVE is checked before the generic routes.
  2. THE SAFE DEFAULT. When no route shows a strong enough signal, fall back to CHAT — the cheapest,
     least-destructive route. Never default to TASK (burns agent cost) or SAVE (stores junk).

PROVIDED: the Route record and the marker tables (starter lists — extend them as you find gaps).
LEARNER:  route_query (M1).

Run:  python -m pytest tests/test_router.py
"""
from __future__ import annotations

from dataclasses import dataclass

# Precedence order — checked first to last. This ORDER is the correctness decision (see module docstring).
PRECEDENCE: tuple[str, ...] = ("SAVE", "RECALL", "TASK")
DEFAULT_ROUTE = "CHAT"  # the safe default when nothing else clears the threshold

# [provided] Intent markers per route. Starter lists — extend them; the SHAPE is what's provided.
SAVE_MARKERS: list[str] = [
    "remember", "note that", "note:", "save this", "save that", "store this", "keep track",
    "don't forget", "dont forget", "i learned", "today i", "make a note", "jot down", "add to my notes",
]
RECALL_MARKERS: list[str] = [
    "what did i", "did i", "what do i know", "find my", "search my notes", "recall", "look up my",
    "what have i", "show me my", "retrieve", "what's saved", "whats saved",
]
TASK_MARKERS: list[str] = [
    "summarize", "summarise", "compare", "research", "go through", "across all", "everything i",
    "draft a", "draft me", "organize", "organise", "synthesize", "synthesise", "review all", "analyze all",
]

_MARKERS: dict[str, list[str]] = {"SAVE": SAVE_MARKERS, "RECALL": RECALL_MARKERS, "TASK": TASK_MARKERS}


@dataclass(frozen=True)
class Route:
    """[provided] A routing decision: which route, WHY (reason), and HOW strong the signal was."""
    name: str           # one of SAVE / RECALL / TASK / CHAT
    reason: str         # human-readable justification (which markers fired, or "safe default")
    confidence: float   # signal strength in [0, 1] for the chosen route


def _score(query_lower: str, markers: list[str]) -> tuple[int, list[str]]:
    """[provided] Count how many of `markers` appear in the query; return (count, the matched ones)."""
    hit = [m for m in markers if m in query_lower]
    return len(hit), hit


def route_query(query: str, threshold: float = 0.0) -> Route:
    """[learner] Classify `query` into SAVE / RECALL / TASK / CHAT. (M1)

    The rule (precedence-ordered, with a safe default):
      1. Lowercase the query.
      2. For each route in PRECEDENCE order (SAVE, then RECALL, then TASK):
           score, matched = _score(query_lower, that route's markers)
           if score >= 1:
               confidence = min(1.0, score / 2.0)     # 1 marker -> 0.5, 2+ -> 1.0
               if confidence >= threshold:
                   return Route(route_name, reason=f"matched {route} markers: {matched}", confidence)
         -> the FIRST route in precedence order that fires (and clears the threshold) wins. This is
            why SAVE is listed first: a "remember this" must never be shadowed by a generic match.
      3. If no route fired (or none cleared the threshold), return the SAFE DEFAULT:
           Route("CHAT", reason="no strong save/recall/task signal — safe default", confidence=0.0)

    The traps:
      - Do NOT check CHAT first or treat it as a positive match — it's the FALLBACK, returned only
        when nothing else fires. Checking it first would swallow saves/recalls as small talk.
      - The safe default must be CHAT, never TASK (cost) or SAVE (junk).
      - Respect precedence: iterate PRECEDENCE in order and return on the first hit; don't, e.g.,
        pick the alphabetically-first or last-matched route.

    Example (mirrors tests/test_router.py::test_route_*):
        route_query("remember the demo is June 20").name   -> "SAVE"
        route_query("what did I save about the demo?").name -> "RECALL"
        route_query("summarize everything I saved").name    -> "TASK"
        route_query("explain cosine similarity").name       -> "CHAT"   (no signal -> safe default)
        route_query("note: buy milk").reason                -> "matched SAVE markers: ['note:']"
    """
    raise NotImplementedError(
        "M1: classify by precedence (SAVE ▸ RECALL ▸ TASK), else the safe default CHAT")
