# Assessment Rubric — Elective 02: Guardrails & Safety Layer

> Used to evaluate the learner's completed elective.
> Self-assessment first. Mentor review second.
> This elective grades the **trust boundary**: scanning untrusted input (user + retrieved),
> redacting PII, enforcing output policy, and **failing closed** — proven against a labeled
> dataset that reports the precision/recall tradeoff. It does **not** grade rebuilding the agent
> (provided) or the evaluator (provided).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains *why a working feature is not a safe one* and the **data/instruction boundary collapse** (why injection is structural, not a bug). Distinguishes direct vs. **indirect** injection and says where the latter arrives (retrieved content). States **fail closed** precisely and why fail-open is worse than no guard. Frames guardrails as **risk reduction, not a guarantee**, citing the sources. Original analogy. | 25 |
| 3 — Good | Explains injection, the input/output split, and fail-closed correctly with minor gaps (e.g. fuzzy on indirect injection's channel). | 20 |
| 2 — Developing | Describes "scan for bad words" but treats injection as a patchable bug, or can't explain fail-closed, or thinks a system-prompt instruction solves it. | 15 |
| 1 — Beginning | Surface-level; leans on lesson language; believes the guard makes the system "safe". | 10 |

**Score: ___ / 25**  **Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Three guards return **structured verdicts**; `scan_input` inspects **user + retrieved** and catches direct/indirect/jailbreak while passing benign; `redact_output` is **detect→transform**, config-driven, structure-safe; `enforce_policy` **fails closed on violation and on its own error**; `run_guarded` composes in the right order and a blocked input never reaches the agent. Every guard fails closed. All guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (e.g. a guard returns a bool, or one bound missing, or redaction misses one entity). | 24 |
| 2 — Developing | Input scan works but redaction or policy is missing/partial; or a guard fails **open**; or only `user_input` is scanned (indirect blind); some tests fail. | 18 |
| 1 — Beginning | Does not run, or no real boundary (guards are no-ops / cosmetic). | 12 |

**Score: ___ / 30**  **Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments, **including** (a) a **fail-open** bug (remove a fail-closed default, feed hostile input, show the breach) and (b) an **indirect-injection** case (attack in `retrieved`, not the prompt). Each correctly diagnoses the failure and states the production implication. | 20 |
| 3 — Good | 2+ experiments with good analysis (at least one of fail-open / indirect-injection). | 16 |
| 2 — Developing | 1 experiment with shallow analysis. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without diagnosis. | 8 |

**Score: ___ / 20**  **Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Reports **all three** numbers — attack-catch rate, **benign false-positive rate**, PII leak rate — per class, on the frozen set. Makes one **tuning move** (change a threshold/rule) and shows the precision/recall tradeoff shift. Honest read: names what still gets through. | 15 |
| 3 — Good | Two of three numbers; tradeoff acknowledged; minor gaps. | 12 |
| 2 — Developing | Only "we block attacks" — recall without the false-positive rate (the metric trap). | 9 |
| 1 — Beginning | No meaningful measurement. | 6 |

**Score: ___ / 15**  **Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Identifies 2+ concrete, non-obvious patterns this elective gives StarcallOS (the guard as the precondition for touching real email/files; the boundary as the governance layer for *what may act on whose authority*; indirect-injection defense on every retrieved source) with a mechanism and an implementation path. | 10 |
| 3 — Good | Identifies 1 concrete applicable pattern with a good explanation. | 8 |
| 2 — Developing | Generic ("StarcallOS should be secure"). | 6 |
| 1 — Beginning | No meaningful StarcallOS connection. | 4 |

**Score: ___ / 10**  **Evidence:**

---

## Total Score

**___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Elective complete to standard |
| 75–89 | Complete with minor gaps — document them |
| 60–74 | Revisit the weak dimensions before considering it done |
| Below 60 | Return to the lesson and rebuild the guard layer |

---

## Elective-Specific Checks (quick pass/fail before scoring)

- [ ] Every guard **fails closed** (error/uncertainty → refusal, never pass-through)
- [ ] `scan_input` inspects **retrieved content**, not just the user prompt
- [ ] Guards return **structured verdicts** (decision + reason + evidence), not bare bools
- [ ] `redact_output` is **detect→transform**, config-driven, and structure-safe
- [ ] `enforce_policy` refuses on violation **and** on its own internal error
- [ ] A blocked input **never reaches the agent/tools**
- [ ] EVALUATION reports attack-catch **and** benign-false-positive **and** PII-leak
- [ ] Reflections frame guardrails as **risk reduction, not a guarantee**
- [ ] All guiding tests pass offline (`python -m pytest`)

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
