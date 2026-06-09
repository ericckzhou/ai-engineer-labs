# Microsoft Presidio — PII Detection and De-identification

**Type:** official-docs (open-source SDK)
**Tier:** 1 (Official Doc)
**URL:** https://microsoft.github.io/presidio/
**Accessed:** 2026-06-09
**Publisher:** Microsoft
**Link:** https://microsoft.github.io/presidio/
**Repo:** https://github.com/microsoft/presidio

> Primary source for **Elective 02 — Guardrails & Safety Layer** (the PII-redaction component,
> M2). Concrete, production-grade reference for *how* redaction is structured.

---

## What it is

An open-source SDK for identifying and de-identifying PII in text (and images). It is the
concrete, named approach behind the elective's `redact_output` — the learner builds a small
version of this two-stage pipeline, with Presidio's design as the reference (and optionally as a
real backend in an extension).

## Architecture — two stages

**1. Analyzer (detect).** Finds PII entities using multiple, composable techniques:
- **Pattern matching** (regex) — e.g. credit-card numbers, SSNs, phone numbers.
- **Named Entity Recognition (NER)** — model-based detection of names, locations, orgs.
- **Context words** — rule-based boosting when nearby tokens raise confidence.
- **Checksum validation** — e.g. Luhn check for card numbers to cut false positives.

**2. Anonymizer (transform).** Replaces detected entities with one of several **operators**:
- `replace` — swap with a placeholder (e.g. `<PERSON>`).
- `mask` — partially hide (e.g. `****-****-****-1234`).
- `redact` — remove entirely.
- `hash` — deterministic non-reversible token.
- `encrypt` — reversible with a key.

## Supported entity types (examples)

Names, locations, credit-card numbers, SSNs, phone numbers, crypto wallet addresses, financial
data — and **custom recognizers** for domain-specific PII.

## Why This Source Matters

It models the right decomposition for `redact_output`: **detect (recognizers) → transform
(operators)**, with the entity list and operator choice driven by config — not a single
hardcoded regex. The learner's offline core can be regex + checksum recognizers with a `mask`
operator; the extension swaps in Presidio for NER-based detection.

## Key Claims

- Two-stage pipeline: an Analyzer detects PII (regex patterns, NER, context-word boosting, checksum validation) and an Anonymizer transforms it (replace, mask, redact, hash, encrypt).
- Entity list and operator choice are config-driven, not a single hardcoded regex; custom recognizers extend it to domain-specific PII.
- Microsoft states plainly there is no guarantee Presidio finds all sensitive information — redaction is risk reduction, not a guarantee.

## Relevant To

- Elective 02 — Guardrails & Safety Layer (the PII-redaction component, M2).
- Related: owasp-llm-top10-2025.md (LLM02). The learner's offline core is regex + checksum recognizers with a mask operator; Presidio NER is the extension backend.

## Known issues / cautions

- Microsoft states plainly: "because it is using automated detection mechanisms, there is **no
  guarantee** that Presidio will find all sensitive information." Redaction is risk reduction,
  not a guarantee — the same humility the whole elective teaches.
- Masking inside structured output (JSON / tool arguments) can corrupt structure; redact at the
  right layer.
