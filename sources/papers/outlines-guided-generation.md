# Efficient Guided Generation for Large Language Models

**Type:** paper
**Tier:** 2 (Foundational Paper)
**Authors:** Brandon T. Willard, Rémi Louf (Normal Computing; the Outlines library)
**Year:** 2023
**arXiv:** 2307.09702 — https://arxiv.org/abs/2307.09702
**URL:** https://arxiv.org/abs/2307.09702
**Accessed:** 2026-06-09

> Primary source for **Elective 06 — Structured Output & Reliability** (the constrained-decoding
> extension, §8). Faithful summary; arXiv PDF is canonical.

---

## Why This Source Matters

The reliability core of Elective 06 makes structured output trustworthy *after* generation —
extract, validate, and repair what the model produced. This paper is the other half: prevent invalid
output *at* generation. It grounds the claim that the most robust fix is **constrained decoding** —
making schema-violating output impossible by construction rather than catching it afterward — and is
the basis for the elective's "forced structure" extension.

## Key Claims

- Guided/structured generation can be reframed as walking a **finite-state machine (FSM)** built from
  a regular expression (and, by extension, a context-free grammar or JSON schema): each FSM state
  defines which next tokens keep the output valid.
- A **precomputed index** maps FSM states to the set of allowed vocabulary tokens, so at each decoding
  step the logits of disallowed tokens are masked — the model can only sample tokens that keep the
  output schema-valid. Output therefore **matches the schema by construction**.
- The indexed approach adds **near-zero per-token overhead** (it avoids re-scanning the whole
  vocabulary each step), making guaranteed-valid generation practical, not just theoretically possible.
- The method is implemented in the open-source **Outlines** library and applies to regex, CFGs, and
  JSON-schema-shaped output.

## Relevant To

- Elective 06 — Structured Output & Reliability (constrained decoding as the alternative to the
  validate-and-repair loop, §8 / the extension).
- Related: anthropic-tool-use.md (`tool_choice` to force a provider-native schema — the same "constrain
  the shape" idea via the API), mcp-tools.md (`outputSchema` / structured results). Elective 03 (no
  repair generations means lower cost).

## Known issues / cautions

- Requires access to the decoder's **logits** to mask tokens; many hosted APIs don't expose this, so
  it's most directly available on local/open models or providers that implement it server-side.
- Guarantees **structural** validity only — a JSON object that matches the schema can still be
  semantically wrong. Constrained decoding does not replace evaluation.
- An over-tight grammar can prevent the model from expressing uncertainty or refusal (it's forced to
  emit *something* schema-shaped); the schema must leave room for "unknown"/"needs human".
- Building the FSM index has an upfront cost; it amortizes across many generations with the same schema.
