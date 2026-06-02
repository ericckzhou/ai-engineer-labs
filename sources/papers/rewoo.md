# ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Binfeng Xu, Quan Wang, Yajuan Lyu, Yong Zhu, Zhendong Mao
**Date:** 2023
**URL:** https://arxiv.org/abs/2305.18323
**Accessed:** 2026-06-02

## Why This Source Matters

ReWOO is useful because it contrasts with ReAct. Instead of interleaving reasoning and observation at every step, it plans tool calls up front, executes them, then solves with observations. This gives Project 08 a concrete architecture comparison.

## Key Claims

- ReWOO stands for Reasoning WithOut Observation.
- The method decouples a planner from tool execution and final solving.
- Planning first can reduce repeated prompt growth from interleaved observation-heavy loops.
- Decoupling parametric reasoning from non-parametric tool calls can improve efficiency in some augmented-language-model settings.
- The architecture trades adaptability for efficiency: if the plan is wrong, the system may need replanning or fail with stale assumptions.

## Relevant To

- concepts: [rewoo, plan-execute, agent-planning, tool-use-efficiency, reasoning-without-observation]
- projects: [08-ai-agent, 07-ai-evaluation-framework]

## Notes

Use ReWOO to teach architecture tradeoffs, not as a universal upgrade over ReAct. ReAct adapts after each observation; ReWOO can be more efficient when the plan is reliable.
