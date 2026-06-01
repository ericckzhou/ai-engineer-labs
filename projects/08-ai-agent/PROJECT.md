# Project 8: AI Agent

## What We're Building

An autonomous AI agent that can plan multi-step tasks, use tools (web search, file system, code execution, APIs), recover from failures, and produce structured final outputs. The agent will include an evaluation harness and a "reflection" loop.

## Why We're Building It

Agents are where AI engineering gets genuinely hard. The failure modes multiply — the model can get stuck in loops, use tools incorrectly, fail silently, or hallucinate tool results. This project teaches you to build agents that fail gracefully, and — more importantly — when NOT to use an agent.

## Learning Objectives

- [ ] Implement the ReAct (Reason + Act) agent loop
- [ ] Build and register custom tools with schemas
- [ ] Handle tool errors and agent recovery strategies
- [ ] Implement structured output for final agent responses
- [ ] Detect and break agent loops (stuck patterns)
- [ ] Evaluate agent performance: task completion, efficiency, cost
- [ ] Define when an agent is overkill and a simpler solution suffices

## Key Concepts

ReAct pattern, tool use, function calling, agent loops, planning, structured output, failure recovery, agent evaluation, token budget management

## Core Engineering Problem

**Problem:** Simple tasks need one LLM call. Complex tasks need many — with decisions made along the way. How do you give an LLM the ability to act in the world, then check its own work, without it spinning into expensive infinite loops?

## Time Estimate

**Total:** 12–16 hours

## Startup Lens

Autonomous agents are the highest-value AI product category. A coding agent that saves 2 hours per day at $100/hour is worth $500/month to a developer. The challenge is reliability — users forgive bad suggestions, but not autonomous actions that cause damage.

## Key Files

```
code/
  agent.py              — Core ReAct agent loop
  tools/
    web_search.py       — Web search tool
    file_tools.py       — File read/write tools
    code_runner.py      — Safe code execution
  tool_registry.py      — Tool registration and schema
  planner.py            — Task decomposition
  reflection.py         — Agent self-check loop
  safety.py             — Loop detection, budget limits
  evaluate_agent.py     — Task completion evaluation
  requirements.txt
  README.md
```
