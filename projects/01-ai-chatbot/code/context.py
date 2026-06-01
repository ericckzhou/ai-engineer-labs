"""context.py — [partial] Keep messages[] within the context window.

LEARNER TODO: implement all three functions. estimate_tokens() is the warm-up;
trim_to_budget() is a real design decision — which turns to drop, and how to keep
the user/assistant roles validly alternating after dropping them.
"""
from __future__ import annotations


def estimate_tokens(messages: list[dict], system: str = "") -> int:
    """Rough token estimate (~4 chars/token) over all message content + system.

    Estimate only — the true count comes back in usage.input_tokens after the call.
    """
    # TODO(learner): sum the character lengths of all content (+ system) and divide by ~4.
    raise NotImplementedError("Implement estimate_tokens()")


def within_budget(messages: list[dict], budget: int, system: str = "") -> bool:
    """True if the estimated token count is <= budget."""
    # TODO(learner)
    raise NotImplementedError("Implement within_budget()")


def trim_to_budget(messages: list[dict], budget: int, system: str = "") -> list[dict]:
    """Return a NEW list trimmed to <= budget.

    Constraints: never drop the system message; drop the OLDEST user/assistant turns
    first; keep roles validly alternating. Do not mutate the caller's list.
    """
    # TODO(learner): this is the core design decision of the context guard.
    raise NotImplementedError("Implement trim_to_budget()")
