"""budget.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (TODOs) on main."""
from __future__ import annotations


class CostTracker:
    def __init__(self) -> None:
        self.total: float = 0.0
        self.calls: int = 0

    def add(self, cost: float) -> None:
        self.total += cost
        self.calls += 1

    def over_budget(self, ceiling: float) -> bool:
        return self.total > ceiling
