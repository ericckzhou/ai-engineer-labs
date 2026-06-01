"""[provided] Guiding tests for cost tracking.

These FAIL until you implement code/cost_tracker.py. Make them pass — no network needed.
Run from the code/ directory:  python -m pytest
"""
import pytest

from cost_tracker import CostTracker, cost_of


def test_input_only():
    # 1M input tokens at $3/MTok = $3.00
    assert cost_of("claude-sonnet-4-6", 1_000_000, 0) == pytest.approx(3.0)


def test_output_only():
    # 1M output tokens at $15/MTok = $15.00
    assert cost_of("claude-sonnet-4-6", 0, 1_000_000) == pytest.approx(15.0)


def test_unknown_model_raises():
    with pytest.raises(KeyError):
        cost_of("no-such-model", 100, 100)


def test_tracker_accumulates():
    t = CostTracker()
    first = t.record("claude-sonnet-4-6", 1_000_000, 0)
    assert first == pytest.approx(3.0)
    t.record("claude-sonnet-4-6", 0, 1_000_000)
    assert t.total == pytest.approx(18.0)
    assert t.turns == 2
