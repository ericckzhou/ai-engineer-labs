"""[provided] Guiding tests for evaluate.py — M4 (evaluate_run). OFFLINE.

Pure scoring logic over a RunResult — no repo, no network. The key behaviors: completion is keyed
off the stop_reason AND the expected substring (a stuck run that carries text is NOT complete), and
efficiency is capped at 1.0.
"""
from agent import RunResult
from safety import Action
from evaluate import evaluate_run


def _answered(answer, history, steps, tokens=900):
    return RunResult(answer=answer, history=history, steps=steps, tokens=tokens, stop_reason="answered")


def test_evaluate_run_completed_and_optimal():
    run = _answered("It defaults to groq/llama-3.3-70b-versatile",
                    history=[Action("search_code", {"query": "model"}),
                             Action("read_file", {"path": "config.py"})],
                    steps=3)
    out = evaluate_run(run, {"answer_contains": "groq", "optimal_steps": 3})
    assert out["completed"] is True
    assert out["steps"] == 3
    assert out["tool_calls"] == 2
    assert out["efficiency"] == 1.0
    assert out["stop_reason"] == "answered"


def test_evaluate_run_not_completed_when_substring_missing():
    run = _answered("I could not determine the model.",
                    history=[Action("read_file", {"path": "config.py"})], steps=2)
    out = evaluate_run(run, {"answer_contains": "groq", "optimal_steps": 2})
    assert out["completed"] is False


def test_evaluate_run_not_completed_when_stuck():
    run = RunResult(answer=None,
                    history=[Action("search_code", {"query": "x"})] * 3,
                    steps=3, tokens=600, stop_reason="stuck")
    out = evaluate_run(run, {"answer_contains": "x", "optimal_steps": 2})
    assert out["completed"] is False
    assert out["tool_calls"] == 3
    assert out["stop_reason"] == "stuck"
    assert abs(out["efficiency"] - (2 / 3)) < 1e-9


def test_evaluate_run_efficiency_capped_at_one():
    # Solved in FEWER steps than "optimal" -> efficiency clamps to 1.0 (never > 1).
    run = _answered("groq", history=[Action("read_file", {"path": "config.py"})], steps=2)
    out = evaluate_run(run, {"answer_contains": "groq", "optimal_steps": 5})
    assert out["efficiency"] == 1.0


def test_evaluate_run_handles_none_answer():
    run = RunResult(answer=None, history=[], steps=1, tokens=100, stop_reason="answered")
    out = evaluate_run(run, {"answer_contains": "groq", "optimal_steps": 1})
    assert out["completed"] is False   # no answer text -> substring can't be present
