"""context.py — [partial] Keep messages[] within the context window.

LEARNER: implement all three functions. estimate_tokens() is the warm-up; trim_to_budget() is a
real design decision — which turns to drop, and how to keep the user/assistant roles validly
alternating after dropping them.

PROVIDED: nothing here is solved for you, but the guiding tests are. The offline checks in
tests/test_context.py tell you when each function is correct (no network). The docstring examples
below mirror those tests.

Run:  python -m pytest tests/test_context.py
"""
from __future__ import annotations


def estimate_tokens(messages: list[dict], system: str = "") -> int:
    """[learner] Rough token estimate (~4 chars/token) over all message content + system.

    Estimate only — the true count comes back in usage.input_tokens after the call.

    Steps:
      1. total_chars = len(system) + sum of len(m["content"]) for every message.
      2. return total_chars // 4   (integer division — this is an estimate, not a billing number).

    Example (mirrors tests/test_context.py::test_estimate_tokens_counts_chars_over_four):
        estimate_tokens([{"role": "user", "content": "x" * 40}])                 -> 10   # 40 // 4
        estimate_tokens([{"role": "user", "content": "x" * 40}], system="y" * 8) -> 12   # (40+8)//4
    """
    # TODO(learner): sum the character lengths of all content (+ system) and divide by ~4.
    raise NotImplementedError("Implement estimate_tokens()")


def within_budget(messages: list[dict], budget: int, system: str = "") -> bool:
    """[learner] True if the estimated token count is <= budget (inclusive).

    Steps:
      1. return estimate_tokens(messages, system) <= budget.

    Example (mirrors tests/test_context.py::test_within_budget_is_inclusive — a 40-char message
    is 10 tokens):
        within_budget([{"role": "user", "content": "x" * 40}], 10)  -> True    # 10 <= 10
        within_budget([{"role": "user", "content": "x" * 40}], 9)   -> False   # 10 > 9
    """
    # TODO(learner)
    raise NotImplementedError("Implement within_budget()")


def trim_to_budget(messages: list[dict], budget: int, system: str = "") -> list[dict]:
    """[learner] Return a NEW list trimmed to <= budget. The core design decision of the guard.

    Steps:
      1. work on a COPY — never mutate the caller's list.
      2. keep the system message (index 0 when present); drop the OLDEST user/assistant turns
         first, one at a time, until within_budget() is True.
      3. keep roles validly alternating after dropping (don't leave two user turns adjacent).
      4. if already within budget, return the messages unchanged (no-op).

    Example (mirrors tests/test_context.py::test_trim_keeps_system_and_newest_within_budget —
    [system(1 tok), u1(10), a1(10), u2(10), a2(10)] = 41 tokens, budget 25):
        result = trim_to_budget(msgs, 25)
        result[0]                       # -> the system message (never dropped)
        estimate_tokens(result) <= 25   # -> True (oldest turns u1, a1 were dropped)
        u2 in result and a2 in result   # -> True (newest turns survive)
        # msgs itself is unchanged (len still 5) — you returned a NEW list.
    """
    # TODO(learner): this is the core design decision of the context guard.
    raise NotImplementedError("Implement trim_to_budget()")
