# Assessment Rubric — Project 07: AI Evaluation Framework

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-07 evidence prompts**
> under each dimension are specific to this lesson (`source/lesson.agent.md`).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains all concepts clearly in own words. Analogy is original and accurate. No gaps in understanding. Can answer follow-up questions. | 25 |
| 3 — Good | Explains most concepts correctly. Minor gaps or oversimplifications. | 20 |
| 2 — Developing | Some correct understanding but significant gaps or misconceptions present. | 15 |
| 1 — Beginning | Surface-level understanding only. Heavy reliance on lesson language without internalization. | 10 |

**Project-07 evidence prompts — look for whether the learner can:**
- Explain why open-ended outputs need **LLM-as-a-judge** rather than `assert ==`, and why ~80% human agreement is "usable but not gospel."
- Name ≥2 judge **biases** (position / verbosity / self-enhancement) with a concrete failure scenario and its mitigation.
- Justify **reasoning-before-score** and **temperature 0** for the judge.
- Explain why a regression can be **invisible in the mean** but visible **per case**, and why the dataset must be **frozen**.

**Score: ___ / 25**

**Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Code is correct, clean, and runnable. Architecture demonstrates understanding of the underlying concepts. No magic — learner understands every line. | 30 |
| 3 — Good | Code works correctly. Minor style or architecture issues. | 24 |
| 2 — Developing | Code partially works. Key components missing or incorrect. | 18 |
| 1 — Beginning | Code does not run or produces incorrect results. | 12 |

**Project-07 evidence prompts — look for whether the implementation:**
- `build_judge_prompt` pins a scale, asks for **reasoning before the score**, and is **reference-guided** when a reference is given. (M1)
- `parse_judge_score` handles JSON and text, **clamps** out-of-range, and **raises** on no-score (not a silent 0). (M2)
- `summarize` reports a mean **and** a pass-rate at a threshold. (M3)
- `compare_runs` flags **per-case** drops over the common cases, not just a mean delta. (M4)
- The end-to-end harness runs a dataset through a system-under-test and reports. (M5)
- Guiding tests in `code/tests/` pass.

**Score: ___ / 30**

**Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments. Each experiment correctly diagnoses why the failure occurred. Clear production implications. | 20 |
| 3 — Good | 2+ experiments with good analysis. | 16 |
| 2 — Developing | 1 experiment with shallow analysis. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without analysis. | 8 |

**Project-07 evidence prompts — strong analyses typically include:**
- A **verbosity-bias** demonstration: pad an answer with no new correctness and show the judge's score rise (source: `sources/papers/mt-bench.md`).
- A **position-bias** (or self-enhancement) demonstration in a pairwise setup, and the swap/different-judge mitigation.
- A **hidden-regression** demonstration: a per-case drop that the mean conceals, surfaced by `compare_runs`.
- A **silent-parse-failure** demonstration: show how returning `0` on an unparseable reply corrupts the mean and fakes a regression.

**Score: ___ / 20**

**Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Quantitative results for all major criteria. Honest assessment of production readiness. Cost analysis included. | 15 |
| 3 — Good | Most criteria measured quantitatively. Minor gaps. | 12 |
| 2 — Developing | Mostly qualitative ("it seemed to work"). Few numbers. | 9 |
| 1 — Beginning | No meaningful evaluation. | 6 |

**Project-07 evidence prompts — quantitative means actual numbers, e.g.:**
- **Mean + pass-rate** for a real run over a frozen dataset, and the **deltas** under a prompt/model change.
- A **judge-vs-human spot-check**: hand-label a handful of cases and report agreement (does it land near the ~80% the paper reports?) (source: `sources/papers/mt-bench.md`).
- **Length-vs-score** correlation (the verbosity audit).
- An honest production note: cost/latency per eval run (judge calls add up), and what a flaky `temperature>0` judge does to a regression gate.

**Score: ___ / 15**

**Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Identifies 2+ concrete, non-obvious patterns applicable to StarcallOS. Explains mechanism and implementation path. | 10 |
| 3 — Good | Identifies 1 concrete applicable pattern with good explanation. | 8 |
| 2 — Developing | Reflection is generic or surface-level. | 6 |
| 1 — Beginning | No meaningful StarcallOS connection made. | 4 |

**Project-07 evidence prompts — concrete connections include:**
- A **regression gate** for StarcallOS: a frozen eval dataset of real tasks + a validated judge + a pass-rate that blocks a merge on a quality drop — mechanism + where it sits in the pipeline.
- A **bias-audited judge** for a specific StarcallOS feature: which judge model, what reference, and how you'd check for verbosity/self-enhancement bias — not "we could add evals."

**Score: ___ / 10**

**Evidence:**

---

## Total Score

**___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Ready for next project |
| 75–89 | Ready with minor gaps — document them |
| 60–74 | Revisit the weak dimensions before proceeding |
| Below 60 | Return to the lesson and rebuild |

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
