"""[provided] Guiding tests for safety.py — M1 (detect_stuck) and M2 (BudgetTracker). OFFLINE.

These fail with NotImplementedError until you implement the learner cores. Pure logic — no repo, no
network. The point of these guards: catch a no-progress agent (stuck) and a runaway agent (budget)
that a bare `max_steps` cap would miss or only catch too late.
"""
from safety import Action, BudgetTracker, detect_stuck


# ---- M1: detect_stuck --------------------------------------------------------
def test_detect_stuck_false_for_different_actions():
    history = [Action("search_code", {"query": "x"}),
               Action("read_file", {"path": "a.py"}),
               Action("read_file", {"path": "b.py"})]
    assert detect_stuck(history, window=3) is False


def test_detect_stuck_true_for_identical_actions():
    history = [Action("search_code", {"query": "foo"})] * 3
    assert detect_stuck(history, window=3) is True


def test_detect_stuck_false_when_history_too_short():
    history = [Action("read_file", {"path": "a.py"})]
    assert detect_stuck(history, window=3) is False


def test_detect_stuck_only_considers_last_window():
    # The first three are identical, but the LAST three are not -> not stuck.
    history = [Action("read_file", {"path": "a.py"})] * 3 + [Action("search_code", {"query": "z"})]
    assert detect_stuck(history, window=3) is False


def test_detect_stuck_compares_arguments_not_just_tool_name():
    # Same tool, DIFFERENT arguments -> the agent is making progress, not stuck.
    history = [Action("read_file", {"path": "a.py"}),
               Action("read_file", {"path": "b.py"}),
               Action("read_file", {"path": "c.py"})]
    assert detect_stuck(history, window=3) is False


# ---- M2: BudgetTracker -------------------------------------------------------
def test_budget_tick_accumulates_steps_and_tokens():
    b = BudgetTracker(max_steps=5, max_tokens=10_000)
    b.tick(2_000)
    b.tick(3_000)
    assert b.steps == 2
    assert b.tokens == 5_000


def test_budget_within_returns_none():
    b = BudgetTracker(max_steps=5, max_tokens=10_000)
    b.tick(2_000)
    b.tick(2_000)
    assert b.over_budget() is None


def test_budget_over_tokens_returns_reason():
    b = BudgetTracker(max_steps=5, max_tokens=10_000)
    b.tick(4_000)
    b.tick(7_000)  # 11_000 > 10_000
    reason = b.over_budget()
    assert reason  # a non-empty string (truthy)
    assert "token" in reason.lower()


def test_budget_over_steps_returns_reason():
    b = BudgetTracker(max_steps=3, max_tokens=1_000_000)
    for _ in range(3):
        b.tick(10)
    reason = b.over_budget()
    assert reason
    assert "step" in reason.lower()
