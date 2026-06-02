"""[provided] Guiding tests for regression_runner.py — M4 (compare_runs). OFFLINE."""
import pytest

from llm_judge import JudgeResult
from regression_runner import compare_runs


def test_compare_runs_flags_regression_and_improvement():
    base = [JudgeResult("a", 4, ""), JudgeResult("b", 5, ""), JudgeResult("c", 3, "")]
    cand = [JudgeResult("a", 4, ""), JudgeResult("b", 2, ""), JudgeResult("c", 5, "")]
    r = compare_runs(base, cand, tolerance=0)
    assert r.regressions == ["b"]      # 5 -> 2
    assert r.improvements == ["c"]     # 3 -> 5
    assert round(r.baseline_mean, 2) == 4.0
    assert round(r.candidate_mean, 2) == 3.67
    assert round(r.mean_delta, 2) == -0.33


def test_compare_runs_hidden_regression_in_flat_mean():
    # A per-case drop (b: 5->2) and rise (c: 2->5) cancel exactly in the mean — but b regressed.
    base = [JudgeResult("b", 5, ""), JudgeResult("c", 2, "")]
    cand = [JudgeResult("b", 2, ""), JudgeResult("c", 5, "")]
    r = compare_runs(base, cand, tolerance=0)
    assert "b" in r.regressions
    assert abs(r.mean_delta) < 0.001   # mean is unchanged, yet a regression exists


def test_compare_runs_tolerance_suppresses_small_drops():
    base = [JudgeResult("a", 5, "")]
    cand = [JudgeResult("a", 4, "")]
    assert compare_runs(base, cand, tolerance=1).regressions == []   # drop of 1 within tolerance
    assert compare_runs(base, cand, tolerance=0).regressions == ["a"]


def test_compare_runs_only_common_cases():
    base = [JudgeResult("a", 4, ""), JudgeResult("x", 1, "")]
    cand = [JudgeResult("a", 5, ""), JudgeResult("y", 1, "")]
    r = compare_runs(base, cand, tolerance=0)
    # only "a" is in both runs; x/y are ignored (not comparable)
    assert r.improvements == ["a"]
    assert r.regressions == []
