"""budget.py — [partial] Cost accounting. Reuses the Project 08 budget pattern.

PROVIDED: the class + state. LEARNER (TODOs, M4): the accumulation and the ceiling check, so
"feels cheaper" becomes a number you can put next to the quality number.
"""
from __future__ import annotations


class CostTracker:
    def __init__(self) -> None:
        self.total: float = 0.0
        self.calls: int = 0

    def add(self, cost: float) -> None:
        """Accumulate one call's cost (and increment the call count)."""
        # TODO(M4): self.total += cost ; self.calls += 1
        raise NotImplementedError("M4: implement add — accumulate cost and call count.")

    def over_budget(self, ceiling: float) -> bool:
        """Return True once the accumulated total exceeds the ceiling."""
        # TODO(M4): return self.total > ceiling
        raise NotImplementedError("M4: implement over_budget — compare total to ceiling.")
