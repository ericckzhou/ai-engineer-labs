"""[provided] Guiding tests for agent_loop.py — M2 (parse_tool_calls) and M4 (run_agent). OFFLINE.

A fake `complete` (no network) scripts the model's turns so the loop is fully deterministic. The
run_agent tests also exercise dispatch_tool (M3) and safe_resolve (M1), so finish those first.
"""
from types import SimpleNamespace

from agent_loop import parse_tool_calls, run_agent


def _tc(call_id, name, arguments):
    """Build a fake OpenAI-style tool_call (arguments is a JSON *string*, as LiteLLM returns)."""
    return SimpleNamespace(id=call_id, function=SimpleNamespace(name=name, arguments=arguments))


# ---- M2: parse_tool_calls ----------------------------------------------------
def test_parse_tool_calls_extracts_and_json_loads():
    msg = SimpleNamespace(content=None,
                          tool_calls=[_tc("c1", "read_file", '{"path": "config.py"}')])
    calls = parse_tool_calls(msg)
    assert len(calls) == 1
    assert calls[0].id == "c1"
    assert calls[0].name == "read_file"
    assert calls[0].arguments == {"path": "config.py"}  # a dict, not the JSON string


def test_parse_tool_calls_empty_when_model_answers():
    msg = SimpleNamespace(content="here is the answer", tool_calls=None)
    assert parse_tool_calls(msg) == []


def test_parse_tool_calls_handles_multiple():
    msg = SimpleNamespace(content=None, tool_calls=[
        _tc("a", "list_directory", '{"path": "."}'),
        _tc("b", "read_file", '{"path": "README.md"}'),
    ])
    calls = parse_tool_calls(msg)
    assert [c.name for c in calls] == ["list_directory", "read_file"]
    assert calls[1].arguments == {"path": "README.md"}


# ---- M4: run_agent -----------------------------------------------------------
def test_run_agent_executes_tool_then_returns_answer(fixture_repo):
    # Script: turn 1 reads config.py; turn 2 (after seeing the result) answers.
    turns = iter([
        SimpleNamespace(content=None, tool_calls=[_tc("c1", "read_file", '{"path": "config.py"}')]),
        SimpleNamespace(content="It is groq/llama-3.3-70b-versatile (config.py).", tool_calls=None),
    ])
    seen = {}

    def complete(messages, tools):
        seen["messages"] = messages
        return next(turns)

    out = run_agent([{"role": "user", "content": "default model?"}],
                    fixture_repo, complete, max_steps=5)
    assert "groq/llama-3.3-70b-versatile" in out
    # the tool result was fed back into the conversation before the final answer:
    assert any(isinstance(m, dict) and m.get("role") == "tool" for m in seen["messages"])


def test_run_agent_respects_max_steps(fixture_repo):
    # A model that ALWAYS asks for a tool and never answers must NOT loop forever.
    def always_tool(messages, tools):
        return SimpleNamespace(content=None,
                               tool_calls=[_tc("c", "read_file", '{"path": "config.py"}')])

    out = run_agent([{"role": "user", "content": "hi"}], fixture_repo, always_tool, max_steps=3)
    assert "max_steps" in out.lower() or "stopped" in out.lower()
