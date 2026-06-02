# Self-Refine: Iterative Refinement with Self-Feedback

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, Peter Clark
**Date:** 2023
**URL:** https://arxiv.org/abs/2303.17651
**Accessed:** 2026-06-02

## Why This Source Matters

Self-Refine is a practical source for iterative generate-feedback-revise loops. It strengthens Project 07 and Project 08 by separating first-pass output from critique and revision.

## Key Claims

- Self-Refine uses the same LLM to generate an initial output, produce feedback on that output, and revise it.
- The method does not require supervised training data, additional training, or reinforcement learning.
- The loop can improve outputs when the model can identify actionable flaws and apply feedback.
- The paper evaluates the approach across multiple generation tasks.
- The method can fail when feedback is vague, self-confirming, or when the model cannot reliably judge the task.

## Relevant To

- concepts: [self-refine, iterative-refinement, feedback-loop, evaluator-optimizer, critique-and-revise]
- projects: [08-ai-agent, 07-ai-evaluation-framework]

## Notes

This source should be taught as an evaluator-optimizer pattern, not as a replacement for external tests. It pairs naturally with Project 07's regression checks.
