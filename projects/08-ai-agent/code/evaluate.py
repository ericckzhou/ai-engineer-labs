"""evaluate.py — [learner] Milestone M4 — score an agent RUN (not a single answer).

"It worked when I ran it once" is an anecdote, not an evaluation. To know whether a prompt or model
change made your agent better or worse, you need NUMBERS per run: did it complete the task, in how
many steps and tool calls, and how efficiently (vs. the optimal number of steps). This is Project
07's evaluation discipline pointed at a whole run instead of one response.

A bare "did it answer?" boolean is not enough: an agent can answer correctly but WANDER (low
efficiency) — a regression a boolean hides. The stop_reason matters too: a "stuck" or "budget" run
did NOT complete, no matter what text it left behind.

PROVIDED: RunResult is defined in agent.py and passed in.
LEARNER:  evaluate_run (M4).

Run:  python -m pytest tests/test_evaluate.py
"""
from __future__ import annotations

from agent import RunResult


def evaluate_run(result: RunResult, expected: dict) -> dict:
    """[learner] Score one agent run against an expected outcome. (M4)

    `expected` = {"answer_contains": str, "optimal_steps": int}:
      - "answer_contains": a substring the correct final answer must contain.
      - "optimal_steps": the fewest steps a competent agent should need (for the efficiency ratio).

    Return a dict with EXACTLY these keys:
      - "completed":  result.stop_reason == "answered" AND answer_contains is in (result.answer or "")
                      (a run that got stuck or ran out of budget did NOT complete — even if it left text)
      - "steps":      result.steps
      - "tool_calls": len(result.history)
      - "efficiency": min(1.0, optimal_steps / max(result.steps, 1))
                      (1.0 = solved in the optimal number of steps; lower = it wandered)
      - "stop_reason": result.stop_reason   (pass it through — the reason a run ended is a result)

    Steps:
      1. answer = result.answer or ""   (guard against None)
      2. completed = (result.stop_reason == "answered") and (expected["answer_contains"] in answer)
      3. efficiency = min(1.0, expected["optimal_steps"] / max(result.steps, 1))
      4. Return the dict above.

    The trap: don't equate "has a non-empty answer" with "completed". Key completion off the
    stop_reason AND the substring, or a stuck run that happens to carry text scores as a success.

    Example (mirrors tests/test_evaluate.py::test_evaluate_run_*):
        answered = RunResult("defaults to groq/llama-3.3-70b", history=[a, b], steps=3,
                             tokens=900, stop_reason="answered")
        evaluate_run(answered, {"answer_contains": "groq", "optimal_steps": 3})
            -> {"completed": True, "steps": 3, "tool_calls": 2, "efficiency": 1.0,
                "stop_reason": "answered"}

        stuck = RunResult(None, history=[a, a, a], steps=3, tokens=600, stop_reason="stuck")
        evaluate_run(stuck, {"answer_contains": "groq", "optimal_steps": 2})
            -> {"completed": False, "steps": 3, "tool_calls": 3, "efficiency": 0.666...,
                "stop_reason": "stuck"}
    """
    raise NotImplementedError("M4: compute completed/steps/tool_calls/efficiency/stop_reason")
