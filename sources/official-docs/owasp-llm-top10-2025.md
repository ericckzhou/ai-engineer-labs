# OWASP Top 10 for LLM Applications (2025)

**Type:** official-docs (industry standard / threat taxonomy)
**Tier:** 1 (Industry Standard)
**URL:** https://owasp.org/www-project-top-10-for-large-language-model-applications/
**Accessed:** 2026-06-09
**Publisher:** OWASP Foundation — GenAI Security Project
**Version:** v2025 (released Nov 2024)
**Link:** https://owasp.org/www-project-top-10-for-large-language-model-applications/
**Canonical PDF:** https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-v2025.pdf

> Primary source for **Elective 02 — Guardrails & Safety Layer**. Pointers and faithful
> summary only; the canonical text is the OWASP PDF above. Where OWASP's exact mitigation
> wording matters, quote from the PDF.

---

## What it is

A community-built, periodically-revised list of the ten most critical security risks specific to
applications that integrate large language models. The 2025 edition reorders the list and
reworks several categories based on community feedback. It is the de-facto industry checklist for
LLM application security and the threat taxonomy this elective hardens against.

## The two categories this elective targets

### LLM01:2025 — Prompt Injection

User- or content-supplied input manipulates the model's behavior, overriding the developer's
original instructions to extract data or trigger unintended actions. The defining property is
that LLMs do not have a hard boundary between *instructions* and *data* — both arrive as text.

- **Direct injection** — the attacker manipulates the user prompt itself (e.g. "ignore previous
  instructions and …").
- **Indirect injection** — hidden instructions are embedded in *external content the app
  retrieves* (documents, web pages, emails). The user never typed the attack; it rode in on the
  data. (See `sources/papers/indirect-prompt-injection.md`.)

**OWASP-recommended mitigations (paraphrased):** constrain model behavior with explicit system
instructions; validate and filter inputs; enforce output formats/allow-lists; apply least
privilege to downstream actions the model can trigger; require human approval for high-impact
operations. OWASP is explicit that system-prompt restrictions "may not always be honored and
could be bypassed via prompt injection" — i.e. prompt-level defenses are necessary but not
sufficient, which is why an external guard layer exists.

### LLM02:2025 — Sensitive Information Disclosure

The model reveals data it should not — PII, credentials, proprietary algorithms, or other
confidential content — either from its training data, its context window (retrieved docs), or
prior turns.

**OWASP-recommended mitigations (paraphrased):** automated detection and **redaction** of
confidential/PII data in inputs and generated responses; data minimization; access controls on
what enters the context; output scanning before the response leaves the system.

## Why This Source Matters

LLM01 motivates the **input scan** (catch injection before it reaches the model) and LLM02
motivates **output redaction + policy enforcement** (catch PII/leaks before the response reaches
the user). OWASP's own framing — that prompt-level instructions can be bypassed — is the
argument for a separate, fail-closed guard layer rather than "just put it in the system prompt."

## Key Claims

- The 2025 edition is the de-facto industry checklist for LLM-application security, reordered and reworked from community feedback.
- LLM01:2025 Prompt Injection (direct and indirect) exploits the lack of a hard instruction/data boundary; OWASP's own mitigations (system instructions, input validation, output allow-lists, least privilege, human approval) are necessary but can be bypassed.
- LLM02:2025 Sensitive Information Disclosure is countered by automated PII detection/redaction, data minimization, and output scanning before responses leave the system.

## Relevant To

- Elective 02 — Guardrails & Safety Layer (the threat taxonomy the layer hardens against).
- Related: indirect-prompt-injection.md (LLM01 indirect), presidio-pii.md (LLM02 redaction), llama-guard.md.

## Known issues / cautions

- The list is a *taxonomy of risks*, not a library of solutions. Mitigations are directional;
  the engineering is the learner's.
- Detection (injection heuristics, PII recognizers) is inherently incomplete — defense in depth,
  not a solved problem. Pair every guard with an eval that exposes its gaps.
