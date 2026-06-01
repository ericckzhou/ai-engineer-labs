# Project 7: AI Evaluation Framework

## What We're Building

A reusable evaluation harness for measuring AI system quality. It supports LLM-as-judge evaluation, custom metrics, regression testing, cost tracking, and structured result reporting — applicable to any of the previous projects.

## Why We're Building It

You can't improve what you can't measure. Most AI developers ship based on vibes and demo impressions. Production failures happen because no one built evals. This project teaches you to measure before you ship, and to detect regressions when you update models or prompts.

## Learning Objectives

- [ ] Design evaluation datasets for AI tasks (what makes a good test case?)
- [ ] Implement LLM-as-judge evaluation and understand its biases
- [ ] Build custom metrics: faithfulness, relevance, correctness, coherence
- [ ] Write regression tests that catch prompt changes that degrade quality
- [ ] Track cost, latency, and token usage per eval run
- [ ] Interpret evaluation results and make decisions from them

## Key Concepts

LLM-as-judge, evaluation dataset design, faithfulness, relevance, groundedness, regression testing, eval harness, benchmark contamination

## Core Engineering Problem

**Problem:** You changed your system prompt. How do you know if it got better or worse? How do you measure the quality of a text response that has no single right answer?

## Time Estimate

**Total:** 8–12 hours

## Startup Lens

Evaluation infrastructure is the invisible moat. Companies that invest in evals ship faster with fewer regressions. This is also a standalone product category — Braintrust, LangSmith, and others are built on selling evaluation infrastructure.

## Key Files

```
code/
  dataset.py            — Test case management
  llm_judge.py          — LLM-as-judge implementation
  metrics.py            — Faithfulness, relevance, correctness
  regression_runner.py  — Regression test harness
  cost_tracker.py       — Per-run cost/latency tracking
  report.py             — Structured result reporting
  evaluate_rag.py       — Evaluate Project 4's RAG system
  requirements.txt
  README.md
```
