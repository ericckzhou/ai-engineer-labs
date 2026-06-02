"""[provided] Guiding tests for agent.py — M3 (run_agent). OFFLINE.

A fake `complete` (no network) scripts the model's turns so the loop is fully deterministic. These
exercise the four behaviors that distinguish a RELIABLE loop from P06's: it answers, it RECOVERS
from a raising tool, it detects a STUCK agent, and it stops on BUDGET. Implement safety.py (M1, M2)
first — run_agent depends on detect_stuck and BudgetTracker.
"""
from types import SimpleNamespace

import agent
from agent import run_agent
from safety import BudgetTracker
from conftest import make_tool_call, scripted_completer


def _tool_msg(call_id, name, arguments, content=None):
    return SimpleNamespace(content=content, tool_calls=[make_tool_call(call_id, name, arguments)])


def _answer_msg(text):
    return SimpleNamespace(content=text, tool_calls=None)


# ---- answers after using a tool ----------------------------------------------
def test_run_agent_answers_after_tool(fixture_repo):
    complete = scripted_completer([
        _tool_msg("c1", "read_file", '{"path": "config.py"}'),
        _answer_msg("It defaults to groq/llama-3.3-70b-versatile (config.py)."),
    ])
    result = run_agent([{"role": "user", "content": "default model?"}],
                       fixture_repo, complete, BudgetTracker(max_steps=5, max_tokens=100_000))
    assert result.stop_reason == "answered"
    assert "groq" in (result.answer or "")
    # the tool result was fed back into the conversation before the final answer:
    assert any(isinstance(m, dict) and m.get("role") == "tool" for m in complete.seen[-1])


# ---- recovers from a tool that RAISES ----------------------------------------
def test_run_agent_recovers_from_raising_tool(fixture_repo, monkeypatch):
    calls = {"n": 0}

    def exploding_dispatch(name, arguments, repo_root):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("network down")
        return "ok"

    monkeypatch.setattr(agent, "dispatch_tool", exploding_dispatch)

    complete = scripted_completer([
        _tool_msg("c1", "read_file", '{"path": "config.py"}'),  # this dispatch RAISES
        _answer_msg("Recovered and answered."),                  # model adapts on the next step
    ])
    result = run_agent([{"role": "user", "content": "go"}],
                       fixture_repo, complete, BudgetTracker(max_steps=5, max_tokens=100_000))
    assert result.stop_reason == "answered"          # the raise did NOT kill the run
    assert result.answer == "Recovered and answered."
    # the error was fed back as an OBSERVATION (a tool message containing "Error"):
    fed_back = [m for m in complete.seen[-1]
                if isinstance(m, dict) and m.get("role") == "tool" and "Error" in str(m.get("content"))]
    assert fed_back, "a raising tool must be fed back as an error observation, not swallowed"


# ---- detects a stuck (no-progress) agent -------------------------------------
def test_run_agent_detects_stuck(fixture_repo):
    # A model that ALWAYS asks for the exact same tool call and never answers.
    def always_same(messages, tools):
        return _tool_msg("c", "read_file", '{"path": "config.py"}')

    result = run_agent([{"role": "user", "content": "hi"}],
                       fixture_repo, always_same, BudgetTracker(max_steps=20, max_tokens=10_000_000))
    assert result.stop_reason == "stuck"


# ---- stops on the step budget ------------------------------------------------
def test_run_agent_stops_on_budget(fixture_repo):
    # A model that always calls a tool with DIFFERENT args (never stuck) and never answers.
    n = {"i": 0}

    def always_new_tool(messages, tools):
        n["i"] += 1
        return _tool_msg(f"c{n['i']}", "read_file", f'{{"path": "f{n["i"]}.py"}}')

    result = run_agent([{"role": "user", "content": "hi"}],
                       fixture_repo, always_new_tool, BudgetTracker(max_steps=4, max_tokens=10_000_000))
    assert result.stop_reason in {"budget", "max_steps"}   # ran out of resources, did not answer
    assert result.answer is None
    assert result.steps <= 8                                # the loop is bounded, not infinite


# ---- stops on the TOKEN budget specifically ----------------------------------
def test_run_agent_stops_on_token_budget(fixture_repo):
    # Few steps, but each one is huge -> the TOKEN ceiling must catch what a step cap would miss.
    n = {"i": 0}

    def huge_tool(messages, tools):
        n["i"] += 1
        return SimpleNamespace(content="x" * 8_000,  # ~2000 tokens/step
                               tool_calls=[make_tool_call(f"c{n['i']}", "read_file",
                                                          f'{{"path": "f{n["i"]}.py"}}')])

    result = run_agent([{"role": "user", "content": "hi"}],
                       fixture_repo, huge_tool, BudgetTracker(max_steps=100, max_tokens=3_000))
    assert result.stop_reason == "budget"
    assert result.steps < 5   # the token ceiling stopped it long before 100 steps
