"""[provided] Guiding tests for M4 CostTracker. Fail with NotImplementedError until implemented."""
from budget import CostTracker


def test_accumulates():
    t = CostTracker()
    t.add(0.5)
    t.add(0.3)
    assert abs(t.total - 0.8) < 1e-9
    assert t.calls == 2


def test_over_budget():
    t = CostTracker()
    t.add(0.5)
    t.add(0.3)
    assert t.over_budget(0.7) is True
    assert t.over_budget(1.0) is False
