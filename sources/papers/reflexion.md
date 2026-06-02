# Reflexion: Language Agents with Verbal Reinforcement Learning

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, Shunyu Yao
**Date:** 2023
**URL:** https://arxiv.org/abs/2303.11366
**Accessed:** 2026-06-02

## Why This Source Matters

Reflexion is a key paper for agent self-improvement without weight updates. It gives Project 08 an extension path: an agent can use feedback from a failed run to write a verbal lesson, store it, and condition the next attempt.

## Key Claims

- Reflexion uses verbal feedback as a reinforcement signal for language agents.
- The agent reflects on feedback from an environment, evaluator, or internal signal and stores the reflection in memory for future attempts.
- The method can incorporate scalar feedback or free-form natural-language feedback.
- The paper evaluates Reflexion across sequential decision-making, coding, and reasoning tasks.
- Reflection can improve future action plans, but gains depend on task setup, feedback quality, memory content, and benchmark conditions.

## Relevant To

- concepts: [reflexion, agent-self-improvement, verbal-feedback, episodic-agent-memory, run-reflection]
- projects: [08-ai-agent, 07-ai-evaluation-framework]

## Notes

Do not present Reflexion as guaranteed autonomous learning. In this curriculum it is best used as an optional Project 08 extension and as a bridge from failure analysis to future-run behavior.
