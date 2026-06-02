"""agent_app.py — [provided] The orchestrator: run the reliable agent on a real, multi-step task.

This wires your learner modules into a live run: it builds a system prompt + a real LiteLLM-backed
`complete` (tool_choice="auto"), constructs a BudgetTracker from config.py, runs run_agent against a
repository, then prints the ReAct trace, the final answer + stop_reason, and the evaluate_run summary.

It calls the learner cores (run_agent, detect_stuck, BudgetTracker.tick/over_budget, evaluate_run),
so it raises NotImplementedError until those are implemented — then it runs end to end (M5).

Run:  python agent_app.py "what model does this repo default to, and where is it set?" --repo .
      python agent_app.py "list the python files and summarize what config.py does" --repo .
"""
from __future__ import annotations

import argparse
import json

import litellm

from agent import RunResult, run_agent
from config import load_config
from evaluate import evaluate_run
from safety import BudgetTracker
from tools import TOOL_SCHEMAS

SYSTEM_PROMPT = (
    "You are an autonomous engineering agent working inside a single repository. You have tools to "
    "read files, list directories, and search code. Work step by step: think about what you need, "
    "call ONE tool to get it, read the result, and repeat. When you have enough to answer the task "
    "completely, reply with the final answer in plain text and DO NOT call another tool. Be concise "
    "and cite the file (and line, if known) that supports your answer."
)


def make_completer(cfg):
    """Return a `complete(messages, tools)` backed by a real LiteLLM call (tool_choice='auto')."""
    def complete(messages, tools):
        resp = litellm.completion(
            model=cfg.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=cfg.temperature,
            max_tokens=cfg.max_tokens,
        )
        return resp.choices[0].message
    return complete


def _print_trace(result: RunResult) -> None:
    print("\n--- ReAct trace (actions taken) ---")
    if not result.history:
        print("  (no tool calls — the model answered directly)")
    for i, action in enumerate(result.history, 1):
        print(f"  {i}. {action.tool}({json.dumps(action.arguments)})")
    print(f"--- stop_reason: {result.stop_reason}  |  steps: {result.steps}  |  "
          f"~tokens: {result.tokens} ---")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reliable AI agent on a task.")
    parser.add_argument("task", help="The task for the agent to accomplish.")
    parser.add_argument("--repo", default=None, help="Repo root the agent acts on (default: config).")
    parser.add_argument("--expect", default=None,
                        help="Optional substring the correct answer should contain (for evaluate_run).")
    parser.add_argument("--optimal-steps", type=int, default=3,
                        help="Optimal step count for the efficiency metric (default: 3).")
    args = parser.parse_args()

    cfg = load_config()
    repo_root = args.repo or cfg.repo_root
    print(f"Project 08 (AI Agent) — model: {cfg.model}")
    print(f"Task: {args.task}\nRepo: {repo_root}\n"
          f"Budget: max_steps={cfg.max_steps}, token_budget={cfg.token_budget}")

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": args.task},
    ]
    budget = BudgetTracker(max_steps=cfg.max_steps, max_tokens=cfg.token_budget)

    result = run_agent(messages, repo_root, make_completer(cfg), budget, tools=TOOL_SCHEMAS)

    print("\n=== FINAL ANSWER ===")
    print(result.answer if result.answer else "(no answer — see stop_reason)")
    _print_trace(result)

    if args.expect:
        summary = evaluate_run(result, {"answer_contains": args.expect,
                                         "optimal_steps": args.optimal_steps})
        print("\n--- evaluate_run ---")
        for k, v in summary.items():
            print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
