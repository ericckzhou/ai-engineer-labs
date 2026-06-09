"""agent_backend.py — [reference] A condensed Project-08 agent to instrument.

Offline + deterministic. Exposes model/tool calls that return the fields a span needs
(model, tokens, finish_reason, cost) — and one that deliberately fails, so a span can carry
error=true. The instrumentation (tracing.py) and the monitor (monitor.py) are the learner's job;
this is just something to wrap.
"""
from __future__ import annotations


def call_model(prompt: str, *, route: str = "chat") -> dict:
    """A deterministic 'model call' result with the fields a GenAI span records."""
    out_tokens = min(200, 20 + len(prompt) // 4)
    return {
        "model": "cheap-llm",
        "input_tokens": max(1, len(prompt) // 4),
        "output_tokens": out_tokens,
        "finish_reason": "stop",
        "cost": 0.000002 * out_tokens,
        "text": f"[answer to: {prompt[:40]}]",
    }


def call_tool(name: str, ok: bool = True) -> dict:
    """A deterministic 'tool call'. With ok=False it raises — so a span records error=true."""
    if not ok:
        raise RuntimeError(f"tool {name} failed")
    return {
        "model": "tool",
        "input_tokens": 0,
        "output_tokens": 0,
        "finish_reason": "tool_result",
        "cost": 0.0,
        "text": f"[result of {name}]",
    }
