# Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Author(s):** Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica
**Date:** 2023 (submitted 2023-06-09)
**URL:** https://arxiv.org/abs/2306.05685
**Accessed:** 2026-06-01

## Why This Source Matters

This is the primary source for **LLM-as-a-judge** — the central learning target of Project 07. The core problem of evaluation is that a text response often has *no single right answer*: how do you score "is this answer good?" at scale, without paying humans for every example? This paper establishes that a strong LLM (GPT-4) can stand in for a human judge — and, crucially, it **measures how well that works and where it fails**. It is both the justification for using an LLM as a grader and the catalog of biases you must design around. Project 07 implements a judge and then reproduces these biases as its failure analysis.

## Key Claims

### LLM-as-a-judge
- The paper explores "using strong LLMs as judges to evaluate these models on more open-ended questions" — i.e. having a capable model score or compare chat-assistant answers, in place of a fixed metric or a human rater.
- Two judging modes are used in practice: **pairwise comparison** (which of two answers is better) and **single-answer grading** (assign a score, e.g. 1–10, to one answer). Project 07 builds the single-answer grader.

### It agrees with humans ~80% of the time
- "Strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over **80% agreement**, the same level of agreement between humans." This is the empirical license to use an LLM judge: it is about as consistent with a human as two humans are with each other.

### The biases — why a judge is not a free oracle
The paper names specific, reproducible failure modes of LLM judges:
- **Position bias** — the judge favors an answer based on its *order* in the prompt (e.g. the first one), not its quality.
- **Verbosity bias** — the judge prefers **longer** answers, even when length adds no correctness.
- **Self-enhancement bias** — a judge tends to favor answers from **its own model family** / its own style.
- **Limited reasoning ability** — judges are weak at grading **math and reasoning** problems, where they may confidently endorse a wrong answer.

### Mitigations
- **Swapping positions** (run both orders and require agreement, or average) to cancel position bias.
- **Few-shot** judging and **chain-of-thought** (make the judge reason *before* scoring).
- **Reference-guided** judging: give the judge a reference/solution to compare against — especially for math, this sharply improves agreement.

### The benchmarks
- **MT-Bench:** a set of multi-turn, open-ended questions with expert evaluations. **Chatbot Arena:** a crowdsourced "battle" platform collecting human pairwise preferences. The authors released MT-Bench questions, ~3K expert votes, and ~30K human-preference conversations.

## Relevant To

- concepts: [llm-as-judge, evaluation, position-bias, verbosity-bias, self-enhancement-bias, reference-guided-judging, chain-of-thought-judging, pairwise-vs-single-grading, regression-testing]
- projects: [07-ai-evaluation-framework]

## Notes

- **The headline for Project 07:** an LLM judge is good enough to be useful (~80% human agreement) **and** biased enough to be dangerous if you trust it naively. The lesson is to build the judge *and* design around its biases.
- **Chain-of-thought / reasoning-before-score is the cheapest, highest-leverage mitigation** and the one Project 07 bakes into the judge prompt: ask for the reasoning first, then the score. This both improves agreement and gives you an auditable justification.
- **Reference-guided judging** connects to RAGAS (`sources/papers/ragas.md`): when you have a reference answer or a retrieved context, give it to the judge — grading against something concrete beats grading from the judge's parametric memory.
- **Single-answer grading** (score 1–N) is what Project 07 implements; **pairwise** is the extension. Pairwise is more robust to a judge's poorly-calibrated absolute scale but needs position-swap to cancel position bias.
- **Regression testing is the engineering application:** freeze an eval dataset, score your system today (the baseline), and re-score after a prompt/model change; a case whose score drops is a regression. The judge supplies the score; the harness supplies the before/after comparison.
- **Verbosity bias is a trap for your own metrics:** if "better" correlates with "longer" in your judge, a prompt change that just makes answers wordier will look like an improvement. Watch length alongside score.
