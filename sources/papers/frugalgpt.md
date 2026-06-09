# FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance

**Type:** paper
**Authors:** Lingjiao Chen, Matei Zaharia, James Zou (Stanford)
**Year:** 2023
**arXiv:** 2305.05176 — https://arxiv.org/abs/2305.05176

> Primary source for **Elective 03 — Cost & Latency Engineering** (the model-cascade lever, M3).
> Faithful summary; arXiv PDF is canonical.

---

## Core idea

You do not have to send every query to your most expensive model. FrugalGPT studies how to use
LLMs while cutting cost, and names three strategies:

1. **Prompt adaptation** — make the prompt cheaper (e.g. fewer/shorter few-shot examples).
2. **LLM approximation** — substitute a cheaper model or a cache for some queries.
3. **LLM cascade** — query a **cheap model first**, and **escalate** to a stronger (costlier)
   model only when the cheap answer isn't trusted.

The cascade is the centerpiece and the one the elective builds.

## How the cascade decides

Send the query to the cheapest model; a **scoring/reliability function** judges whether its
answer is good enough. If the score clears a threshold, **accept and stop** (cheap path). If not,
**escalate** to the next model up. The decision function — "is the cheap answer trustworthy?" —
is the hard design choice (a learned scorer in the paper; a confidence signal, self-check, or
judge in practice). The learner owns defining this signal.

## Headline result

FrugalGPT can **match the best individual LLM (e.g. GPT-4) with up to ~98% cost reduction**, or
improve accuracy at the same cost — by routing most queries to cheap models and escalating only
the hard ones.

## Why it anchors the elective

It is the cost lever with a *quality risk*: unlike caching, a cascade can return a worse (cheap)
answer. That is exactly why this elective comes after Project 07 — the **eval is the gate** that
proves the cheap path didn't regress quality before you ship the savings.

## Known issues / cautions

- The cascade is only as good as the **escalation signal**; a bad "the cheap model was sure"
  judgment ships wrong answers cheaply.
- Cost claims are workload-dependent; measure on *your* eval set, don't assume 98%.
- Use the **real** per-MTok prices (`anthropic-pricing.md`) to compute savings — don't invent
  token prices.
