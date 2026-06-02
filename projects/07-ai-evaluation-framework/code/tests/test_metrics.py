"""[provided] Guiding tests for metrics.py — M3 (summarize). OFFLINE."""
from llm_judge import JudgeResult
from metrics import summarize


def _rs(scores):
    return [JudgeResult(f"c{i}", s, "") for i, s in enumerate(scores)]


def test_summarize_mean_and_pass_rate():
    s = summarize(_rs([5, 4, 3, 2]), pass_threshold=4)
    assert s.n == 4
    assert s.mean_score == 3.5
    assert s.pass_rate == 0.5  # two of four scored >= 4


def test_summarize_threshold_changes_pass_rate():
    s = summarize(_rs([5, 4, 3, 2]), pass_threshold=3)
    assert s.pass_rate == 0.75  # three of four scored >= 3


def test_summarize_empty_is_safe():
    s = summarize([], pass_threshold=4)
    assert s.n == 0
    assert s.mean_score == 0.0
    assert s.pass_rate == 0.0
