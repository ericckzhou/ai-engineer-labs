"""safety.py — [partial] Milestones M1 + M2 — the reliability primitives that make a loop safe.

Project 06 bounded its loop with a single `max_steps` cap. That is not enough for an AUTONOMOUS,
multi-step agent: a step cap stops a runaway *eventually*, but it misses two common failures —
(1) the agent gets STUCK, repeating the same action with no new information, and (2) the agent
runs away on TOKENS (few steps, but huge ones). This file is the two guards that catch those:
loop/stuck detection and a steps+tokens budget. They are the heart of what Project 08 teaches.

PROVIDED: the Action record, and the BudgetTracker dataclass FIELDS.
LEARNER:  detect_stuck (M1), BudgetTracker.tick + BudgetTracker.over_budget (M2).

Run:  python -m pytest tests/test_safety.py
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Action:
    """[provided] One recorded step in the agent's history: which tool, with which arguments."""
    tool: str
    arguments: dict = field(default_factory=dict)

    def __eq__(self, other) -> bool:  # dict args compare by value; frozen dataclass needs explicit eq
        return isinstance(other, Action) and self.tool == other.tool and self.arguments == other.arguments

    def __hash__(self) -> int:  # hashable despite the dict field (hash the tool + sorted items)
        return hash((self.tool, tuple(sorted(self.arguments.items()))))


def detect_stuck(history: list[Action], window: int = 3) -> bool:
    """[learner] True iff the agent is making no progress — the last `window` actions are IDENTICAL. (M1)

    A `max_steps` cap stops a runaway agent only at the very end; stuck detection stops a no-progress
    agent immediately. "No progress" = the model keeps emitting the SAME action (same tool AND the
    same arguments) and getting the same observation, so it can never advance.

    Steps:
      1. If len(history) < window: return False  (not enough history to judge — give it room).
      2. Take the last `window` actions: recent = history[-window:].
      3. Return True iff they are ALL equal to each other (e.g. all == recent[0]); else False.

    The trap: compare the WHOLE action (tool AND arguments), not just the tool name. An agent that
    reads ten DIFFERENT files is working, not stuck — comparing only `.tool` would wrongly kill it.
    (Action.__eq__ already compares tool + arguments, so `a == b` is the right check.)

    Example (mirrors tests/test_safety.py::test_detect_stuck_*):
        progress = [Action("search_code", {"query": "x"}),
                    Action("read_file", {"path": "a.py"}),
                    Action("read_file", {"path": "b.py"})]
        detect_stuck(progress, window=3)   -> False   (three different actions)

        spinning = [Action("search_code", {"query": "foo"})] * 3
        detect_stuck(spinning, window=3)   -> True    (three identical actions)

        detect_stuck([Action("read_file", {"path": "a.py"})], window=3)  -> False  (too short)
    """
    raise NotImplementedError("M1: return True iff the last `window` actions are all identical")


@dataclass
class BudgetTracker:
    """[partial] A live ceiling on what the agent may spend. Fields provided; tick/over_budget are M2.

    The model controls the loop, so "autonomous" must not mean "unbounded." This is the seatbelt:
    construct it before a run, `tick()` it once per step, and check `over_budget()` after each step.
    """
    max_steps: int
    max_tokens: int
    steps: int = 0
    tokens: int = 0

    def tick(self, tokens_used: int) -> None:
        """[learner] Record one step's spend. (M2)

        Steps:
          1. self.steps += 1
          2. self.tokens += tokens_used

        Example (mirrors tests/test_safety.py::test_budget_*):
            b = BudgetTracker(max_steps=5, max_tokens=10_000)
            b.tick(2000); b.tick(2000)     # -> b.steps == 2, b.tokens == 4000
        """
        raise NotImplementedError("M2: increment steps by 1 and add tokens_used to tokens")

    def over_budget(self) -> str | None:
        """[learner] Return a reason STRING if a ceiling was crossed, else None. (M2)

        The loop uses the truthiness: a non-empty string means "stop, and here's why"; None means
        "keep going." Returning a reason (not just True) is what lets the run record WHY it stopped.

        Steps:
          1. If self.steps >= self.max_steps:
                 return f"step budget exhausted ({self.steps}/{self.max_steps})"
          2. If self.tokens >= self.max_tokens:
                 return f"token budget exhausted ({self.tokens}/{self.max_tokens})"
          3. Otherwise return None.

        Example (mirrors tests/test_safety.py::test_budget_*):
            b = BudgetTracker(max_steps=5, max_tokens=10_000)
            b.tick(2000); b.tick(2000); b.over_budget()   -> None
            b.tick(7000); b.over_budget()                 -> "token budget exhausted (11000/10000)"
        """
        raise NotImplementedError("M2: return a reason string when steps or tokens cross the ceiling")
