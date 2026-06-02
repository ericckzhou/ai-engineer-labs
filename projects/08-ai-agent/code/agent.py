"""agent.py — [learner] Milestone M3 — the generalized, RELIABLE agent loop. THIS is the core.

This is Project 06's tool loop, made safe to leave running on its own. The call -> dispatch ->
feed-back cycle and the tool layer are carried over and PROVIDED. Your job is the reliability:
weave in tool-error RECOVERY (a raising tool must not kill the run), the STUCK guard (stop a
no-progress agent), and the BUDGET guard (stop a runaway), and return a distinct STOP REASON so a
failure is never silently counted as success.

An agent is "an LLM using tools based on environmental feedback in a loop"
(sources/articles/building-effective-agents.md). Project 08's lesson is everything that keeps that
loop from going wrong when YOU aren't watching it.

PROVIDED: ToolCall + RunResult dataclasses; parse_tool_calls (carried from P06); estimate_tokens
          (offline token estimate); the tool layer (tools.py) and the safety primitives (safety.py).
LEARNER:  run_agent (M3).

Run:  python -m pytest tests/test_agent.py
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Callable

from safety import Action, BudgetTracker, detect_stuck
from tools import TOOL_SCHEMAS, dispatch_tool


@dataclass(frozen=True)
class ToolCall:
    """[provided] One parsed tool request from the model (carried from Project 06)."""
    id: str
    name: str
    arguments: dict


@dataclass
class RunResult:
    """[provided] The outcome of an agent run.

    `stop_reason` is the most important field: "answered" (success) vs. "stuck" / "budget" /
    "max_steps" (three distinct failures). Evaluation keys off it — never collapse it to a bool.
    """
    answer: str | None
    history: list[Action]
    steps: int
    tokens: int
    stop_reason: str  # "answered" | "stuck" | "budget" | "max_steps"


def parse_tool_calls(message) -> list[ToolCall]:
    """[provided] Extract the model's tool requests from an OpenAI-style message (carried from P06).

    `arguments` arrives as a JSON *string* — json.loads it. No tool_calls -> [] (the model answered).
    """
    calls = getattr(message, "tool_calls", None)
    if not calls:
        return []
    out: list[ToolCall] = []
    for tc in calls:
        raw = tc.function.arguments
        args = json.loads(raw) if isinstance(raw, str) and raw.strip() else (raw or {})
        out.append(ToolCall(tc.id, tc.function.name, args))
    return out


def estimate_tokens(message) -> int:
    """[provided] Rough offline token estimate for one model message (~4 chars/token).

    Real providers return `usage`; offline (and in tests) we estimate from message length so the
    budget logic is identical without a network call. Always returns >= 1 so steps accrue.
    """
    text = getattr(message, "content", None) or ""
    for tc in (getattr(message, "tool_calls", None) or []):
        fn = getattr(tc, "function", None)
        text += (getattr(fn, "name", "") or "") + (getattr(fn, "arguments", "") or "")
    return max(1, len(text) // 4)


def run_agent(messages: list, repo_root, complete: Callable, budget: BudgetTracker, *,
              tools: list = TOOL_SCHEMAS, stuck_window: int = 3) -> RunResult:
    """[learner] Run the agent loop until it answers, gets stuck, or runs out of budget. (M3)

    `complete(messages, tools)` calls the model and returns its message. It is injected so this is
    testable OFFLINE — agent_app.py passes a real LiteLLM-backed one; tests pass scripted fakes.

    Steps (track `history: list[Action]` of every action taken):
      Loop (use a defensive structural cap, e.g. while budget.steps < budget.max_steps + 25):
        1. msg = complete(messages, tools)
        2. budget.tick(estimate_tokens(msg))                       # account for this step
        3. calls = parse_tool_calls(msg)
        4. If NOT calls: the model answered ->
               return RunResult(msg.content or "", history, budget.steps, budget.tokens, "answered")
        5. Append the assistant turn FIRST: messages.append(msg)   # (carried from P06 — order matters)
        6. For each call:
             - history.append(Action(call.name, call.arguments))   # record BEFORE running it
             - RECOVERY: result = dispatch_tool(call.name, call.arguments, repo_root) inside a
               try/except; on Exception, result = f"Error: {e}"  (feed the error back, don't crash)
             - messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
        7. If detect_stuck(history, stuck_window):
               return RunResult(None, history, budget.steps, budget.tokens, "stuck")
        8. reason = budget.over_budget(); if reason:
               return RunResult(None, history, budget.steps, budget.tokens, "budget")
      If the defensive cap is ever reached (the guards should have stopped you first):
        return RunResult(None, history, budget.steps, budget.tokens, "max_steps")

    The three reliability traps this prevents:
      (1) no budget  -> a confused agent runs away, burning tokens/money (budget guard).
      (2) no stuck check -> the agent oscillates on identical actions until the cap (stuck guard).
      (3) a raising tool with no try/except -> ONE bad call discards the whole multi-step run
          (recovery). And `except: pass` is WORSE than crashing — the model never sees the error
          and repeats it; the error must become an OBSERVATION it can react to.

    Example (mirrors tests/test_agent.py::test_run_agent_*):
        # complete returns a read_file call, then (seeing the result) a final answer:
        run_agent(msgs, repo, scripted, BudgetTracker(5, 10_000)).stop_reason   -> "answered"
        # a dispatch that RAISES once, then the model adapts:
        run_agent(...).stop_reason   -> "answered"   (the raise became an observation; recovered)
        # a model that ALWAYS repeats the same call:
        run_agent(...).stop_reason   -> "stuck"
        # a model that always calls a (different) tool and never answers:
        run_agent(...).stop_reason   -> "budget"  (hit the step/token ceiling)
    """
    raise NotImplementedError(
        "M3: drive call -> dispatch (recover) -> feed back -> guard (stuck/budget) -> repeat")
