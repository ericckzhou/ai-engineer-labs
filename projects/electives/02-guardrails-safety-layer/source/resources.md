# Resources — Elective 02: Guardrails & Safety Layer

> Curated source material for this elective. Truth lives in `sources/`; this is a reading guide.
> Read in this order. Each entry says *why* it matters here.

---

## Read first — the threat

1. **OWASP Top 10 for LLM Applications (2025)** — `sources/official-docs/owasp-llm-top10-2025.md`
   The industry checklist. Read **LLM01 Prompt Injection** (direct vs. indirect; system-prompt
   defenses are bypassable) and **LLM02 Sensitive Information Disclosure** (detect + redact PII).
   These two are the entire target of this elective. Canonical PDF linked in the note.

2. **Not what you've signed up for (Indirect Prompt Injection)** — Greshake et al. 2023 —
   `sources/papers/indirect-prompt-injection.md`
   Why scanning the user prompt is not enough: the dangerous instruction rides in on *retrieved*
   content. Read for the threat model and the "mitigations are lacking" humility.

## Read second — the defenses

3. **Microsoft Presidio** — `sources/official-docs/presidio-pii.md`
   The detect→transform redaction pipeline: recognizers (regex/NER/checksum) → anonymizer
   operators (mask/replace/redact/hash/encrypt). The reference design for `redact_output`. Note
   the explicit "no guarantee it finds all."

4. **Llama Guard** — Inan et al. 2023 — `sources/papers/llama-guard.md`
   The upgrade path: an LLM-as-classifier guard with separate input/output tasks, a
   taxonomy-as-prompt, and a structured verdict (decision + violated categories). The M5/extension.

## Carried from prior projects (no new reading required)

- **Project 06** — `sources/official-docs/anthropic-tool-use.md`: "tool arguments are untrusted
  model input" — the seed of the whole trust-boundary idea, now generalized to all context.
- **Project 07** — `sources/papers/mt-bench.md`: evaluate with numbers; a metric without its
  counter-metric (recall without false-positive rate) lies.
- **Project 04** — `sources/papers/rag-paper.md`: the retrieval channel indirect injection exploits.

---

## How these map to the code

| Source | Code it grounds |
|--------|-----------------|
| OWASP LLM01 + Greshake | `guards.scan_input` (user **and** retrieved) |
| OWASP LLM02 + Presidio | `guards.redact_output` (detect→transform) |
| OWASP (output restrictions) | `guards.enforce_policy` (fail-closed) |
| Llama Guard | LLM-as-classifier extension |
| MT-Bench (P07) | `evaluate_guards.py` (precision/recall) |

---

## Deliberately out of scope

- **Model-level alignment / RLHF** — this elective is an *application* guard layer, not model
  training. The guard does not depend on the model being well-behaved (that's the point).
- **Network/auth/infra security** — real, but a different discipline; here the boundary is the
  text in/out of the LLM.
- **A complete injection taxonomy** — the dataset is illustrative, not exhaustive; Greshake et al.
  is the pointer for depth.
