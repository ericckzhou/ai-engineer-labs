# ReAct: Synergizing Reasoning and Acting in Language Models

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, Yuan Cao
**Date:** 2022 (submitted 2022-10-06)
**URL:** https://arxiv.org/abs/2210.03629
**Accessed:** 2026-06-01

## Why This Source Matters

ReAct is the foundational paper for **the tool-use loop with reasoning** — the structure underneath every modern coding copilot and agent. Before ReAct, prompting split into two camps: *reasoning-only* (chain-of-thought, which thinks but can't look anything up, so it hallucinates) and *acting-only* (call tools, but with no plan). ReAct's contribution is to **interleave** the two: the model alternates between a *thought* (reasoning trace) and an *action* (a tool call), observing each action's result before the next thought. This is exactly the loop Project 06 builds — think about what file to read, read it, observe, think again, answer — and it is the direct conceptual ancestor of Anthropic-style tool use.

## Key Claims

### The central idea: interleave reasoning and acting
- "We explore the use of LLMs to generate both **reasoning traces** and **task-specific actions** in an interleaved manner." The model produces a **Thought → Action → Observation** trajectory, repeated until it can answer.

### The two directions reinforce each other
- "**Reasoning traces help the model induce, track, and update action plans** as well as handle exceptions, **while actions allow it to interface with external sources**, such as knowledge bases or environments, to gather additional information." Reasoning makes acting purposeful; acting grounds reasoning in real observations.

### The action space includes external tools
- Actions interface with external systems — in the paper, "a simple Wikipedia API" and interactive environments — letting the model "retrieve real information rather than relying solely on parametric knowledge." (In Project 06, the action space is `read_file`, `list_directory`, `search_code`.)

### It beats reasoning-only and acting-only
- ReAct surpasses both baselines. On decision-making benchmarks ALFWorld and WebShop it achieves "34% and 10% absolute success rate" improvements over imitation/RL methods, "with one or two in-context examples."

### It reduces hallucination and is more interpretable
- ReAct "overcomes issues of hallucination and error propagation prevalent in chain-of-thought reasoning" (because actions fetch ground truth), and it generates "human-like task-solving trajectories that are more interpretable than baselines" (you can read the thoughts).

## Relevant To

- concepts: [react, agentic-loop, tool-use, reasoning-trace, hallucination-reduction, observation-action]
- projects: [06-ai-coding-copilot, 08-ai-agent]

## Notes

- **ReAct = the loop's grammar.** Thought (reason about what's needed) → Action (call a tool) → Observation (tool result) → repeat → Answer. Project 06's `run_agent` is a minimal ReAct loop; the model's "thought" is whatever text it emits alongside (or before) a tool call.
- **Why acting reduces hallucination:** a chain-of-thought-only model asked "what does `config.py` set the default model to?" will *guess*; a ReAct model reads the file first. This is the single best argument for tool use over a clever prompt — and the failure mode the learner should reproduce in M6.
- **Why reasoning makes acting terminate:** acting-only loops thrash (call the same tool, never decide they're done). The reasoning trace is what lets the model conclude "I now have enough to answer" — connects to why the loop needs both a reasoning step and a `max_steps` cap (`sources/official-docs/anthropic-tool-use.md`).
- Modern tool-use APIs (Anthropic `tool_use`/`tool_result`, OpenAI `tool_calls`) are ReAct operationalized as a protocol: the "Action" is the structured tool call, the "Observation" is the `tool_result` you feed back.
