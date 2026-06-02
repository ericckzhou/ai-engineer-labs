# Tree of Thoughts: Deliberate Problem Solving with Large Language Models

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, Karthik Narasimhan
**Date:** 2023
**URL:** https://arxiv.org/abs/2305.10601
**Accessed:** 2026-06-02

## Why This Source Matters

Tree of Thoughts is a key paper for planning/search-style reasoning with LLMs. It gives Project 08 a principled optional extension beyond a single linear ReAct trajectory.

## Key Claims

- Tree of Thoughts generalizes chain-of-thought prompting by exploring coherent intermediate units called thoughts.
- The method can generate, evaluate, select, and backtrack over multiple reasoning paths.
- It treats problem solving as search over possible intermediate states rather than one left-to-right completion.
- The paper reports improvements on tasks that benefit from exploration, lookahead, and backtracking.
- The approach costs more inference and orchestration than a linear chain, so it should be reserved for tasks where search is worth the complexity.

## Relevant To

- concepts: [tree-of-thoughts, planning, search, backtracking, deliberate-reasoning, agent-orchestration]
- projects: [08-ai-agent, 07-ai-evaluation-framework]

## Notes

Use this as an extension for hard planning tasks. The base Project 08 agent should stay simpler: bounded loop, tool use, recovery, and run evaluation.
