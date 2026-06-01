# Project 6: AI Coding Copilot

## What We're Building

A context-aware coding assistant that understands your codebase, uses file system tools, generates code with citations to relevant existing code, and provides explanations grounded in your actual project — not generic examples.

## Why We're Building It

Coding copilots are the most widely adopted AI product category. Building one from scratch teaches you the skills that power everything from GitHub Copilot to internal developer tools: tool use, context injection, structured output, and retrieval over code. These skills transfer directly to agent construction.

## Learning Objectives

- [ ] Implement tool use (file read, directory listing, code search)
- [ ] Build a code context injector that selects the most relevant files
- [ ] Design system prompts for consistent structured code output
- [ ] Implement a code understanding pipeline (parse, embed, retrieve)
- [ ] Evaluate copilot quality: correctness, relevance, hallucination
- [ ] Compare: when does a copilot outperform simple autocomplete?

## Key Concepts

Tool use, function calling, context injection, code embeddings, structured output, few-shot prompting for code, retrieval over code

## Core Engineering Problem

**Problem:** An LLM given "fix this bug" with no context will guess. An LLM given your entire codebase will hit context limits. How do you inject exactly the right code context to get a useful answer?

## Time Estimate

**Total:** 10–14 hours

## Startup Lens

Developer tools are the fastest category to monetize. Developers will pay for tools that save time. A good copilot reduces context switching from "writing code" to "searching docs" — that's immediately measurable value.

## Key Files

```
code/
  tools.py              — File read, search, directory tools
  context_selector.py   — Relevant file selection
  code_embedder.py      — Index codebase for retrieval
  copilot.py            — Main copilot loop
  structured_output.py  — Enforce code output format
  evaluate_copilot.py   — Quality evaluation
  requirements.txt
  README.md
```
