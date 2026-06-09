# Llama Guard: LLM-based Input-Output Safeguard for Human-AI Conversations

**Type:** paper
**Tier:** 2 (Foundational Paper)
**URL:** https://arxiv.org/abs/2312.06674
**Accessed:** 2026-06-09
**Authors:** Inan, Upasani, Chi, Rungta, Iyer, Mao, Tontchev, Hu, Fuller, Testuggine, Khabsa (Meta)
**Year:** 2023
**arXiv:** 2312.06674 — https://arxiv.org/abs/2312.06674

> Primary source for **Elective 02 — Guardrails & Safety Layer** (the "LLM-as-classifier"
> guard, the M5/extension path). Faithful summary; the arXiv PDF is canonical.

---

## Core idea

A safety guard does not have to be a regex. Llama Guard is an LLM (fine-tuned Llama2-7b) used as
a **content-moderation classifier** that sits on both sides of a conversation:

- **Prompt classification** — judge the *user input* for safety before it reaches the main model.
- **Response classification** — judge the *model's output* before it reaches the user.

These are **separate tasks**, because what makes a prompt unsafe differs from what makes a
response unsafe. This is exactly the input-guard / output-guard split the elective builds.

## Safety risk taxonomy

The model is prompted with an explicit **taxonomy** of risk categories (violence, hate, sexual
content, illegal activity, etc.). Classification is performed *against that taxonomy*, so the
policy is data, not baked into weights.

## Instruction-tuning → adaptability

Because it is instruction-tuned, Llama Guard supports **zero-shot and few-shot** prompting with
*custom* taxonomies: an organization can swap in its own categories and output format without
retraining. The policy is a prompt, not a fixed model.

## Output format

Produces a **binary safe/unsafe decision** plus, when unsafe, the **specific violated
category/categories** — a structured verdict, not a bare bool. This is the shape the elective's
`InputVerdict` / `OutputVerdict` mirror (decision + reason, not just true/false).

## Why This Source Matters

It is the upgrade path from heuristic guards: M1–M4 build cheap, fast, deterministic heuristic
scanners; the extension swaps in an LLM-judge guard (Llama-Guard-style) and compares
catch-rate vs false-positive-rate vs latency/cost. It also models the right *output contract* for
a guard: a categorized verdict the caller can act on.

## Key Claims

- A safety guard can be an LLM classifier rather than a regex; Llama Guard classifies the user input and the model output as two *separate* tasks (input guard vs. output guard).
- Classification runs against an explicit, swappable risk taxonomy — policy is prompt data, not baked into weights — supporting zero-/few-shot custom taxonomies without retraining.
- Output is a structured safe/unsafe verdict plus the specific violated category — a decision with a reason, not a bare boolean.

## Relevant To

- Elective 02 — Guardrails & Safety Layer (the LLM-as-classifier guard, M5/extension).
- Related: owasp-llm-top10-2025.md, indirect-prompt-injection.md; the verdict shape mirrors the elective's InputVerdict / OutputVerdict (decision + reason).

## Known issues / cautions

- An LLM guard is slower and costlier than a heuristic, and is itself fallible (and itself
  injectable) — it is a layer, not a guarantee.
- The taxonomy must be chosen deliberately; a guard only catches what its policy names.
