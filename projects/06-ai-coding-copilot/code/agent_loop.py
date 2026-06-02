"""agent_loop.py — [learner] Milestones M2 + M4 — the tool-use loop (ReAct: think → act → observe).

This is the heart of the copilot and the learning target. An agent is "an LLM using tools based on
environmental feedback in a loop" (sources/articles/building-effective-agents.md) — this file IS
that loop. The model emits tool CALLS; you execute them and feed the RESULTS back; repeat until it
answers. Two learner functions: parse_tool_calls (read the model's request) and run_agent (drive
the loop). The loop's grammar is ReAct (sources/papers/react-paper.md): the model's text is the
Thought, a tool call is the Action, the tool result you feed back is the Observation.

PROVIDED: ToolCall dataclass; copilot.py wires in a real LiteLLM-backed `complete`.
LEARNER:  parse_tool_calls (M2), run_agent (M4).

Run:  python -m pytest tests/test_agent_loop.py
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from tools import TOOL_SCHEMAS, dispatch_tool


@dataclass(frozen=True)
class ToolCall:
    """[provided] One parsed tool request from the model."""
    id: str
    name: str
    arguments: dict


def parse_tool_calls(message) -> list[ToolCall]:
    """[learner] Extract the model's tool requests from a completion message. (M2)

    LiteLLM returns an OpenAI-style message. If the model wants to act, `message.tool_calls` is a
    list; each item has `.id`, `.function.name`, and `.function.arguments` — and arguments is a
    JSON *STRING*, not a dict. If the model is done, tool_calls is None/empty and the answer text is
    in `message.content`.

    Steps:
      1. calls = getattr(message, "tool_calls", None). If falsy, return []  (the model answered).
      2. For each tc: read tc.id, tc.function.name, and tc.function.arguments (a JSON string).
      3. json.loads the arguments into a dict (use {} when the string is empty/None).
      4. Return a list of ToolCall(id, name, arguments_dict).

    The trap: arguments is a STRING. Forgetting json.loads hands the tool a string instead of args.

    Example (mirrors tests/test_agent_loop.py::test_parse_tool_calls_*):
        tc  = ns(id="c1", function=ns(name="read_file", arguments='{"path": "a.py"}'))
        msg = ns(content=None, tool_calls=[tc])
        parse_tool_calls(msg) -> [ToolCall("c1", "read_file", {"path": "a.py"})]
        parse_tool_calls(ns(content="done", tool_calls=None)) -> []
    """
    raise NotImplementedError("M2: extract (id, name, args) and json.loads the arguments string")


def run_agent(messages: list, repo_root, complete: Callable, *,
              tools: list = TOOL_SCHEMAS, max_steps: int = 8) -> str:
    """[learner] Run the agentic loop until the model answers or max_steps is hit. (M4)

    `complete(messages, tools)` calls the model and returns its message. It is injected so this is
    testable OFFLINE — copilot.py passes a real LiteLLM-backed one; tests pass a scripted fake.

    Steps:
      1. Loop up to max_steps times:
         a. msg = complete(messages, tools)
         b. calls = parse_tool_calls(msg)
         c. If NOT calls:  return (msg.content or "")        # the model is done — final answer
         d. Append the assistant turn FIRST:  messages.append(msg)
            (Providers reject an orphan tool result — the assistant turn that requested the tools
            must precede them.)
         e. For each call: result = dispatch_tool(call.name, call.arguments, repo_root); then append
            {"role": "tool", "tool_call_id": call.id, "content": result}.
      2. If the loop runs out of steps, return a clear sentinel, e.g.
         f"[stopped: hit max_steps={max_steps} without a final answer]".

    The traps: (1) no cap → a confused model loops forever, burning the whole budget — max_steps is
    the seatbelt. (2) appending tool results without first appending the assistant message → the
    next call errors on an orphan tool result.

    Example (mirrors tests/test_agent_loop.py::test_run_agent_*):
        # `complete` returns a read_file call once, then a final answer:
        run_agent(msgs, repo, scripted_complete, max_steps=5) -> "...the final answer..."
        # a `complete` that ALWAYS asks for a tool stops at the cap and returns the sentinel.
    """
    raise NotImplementedError("M4: drive call -> dispatch -> feed back -> repeat, bounded by max_steps")
