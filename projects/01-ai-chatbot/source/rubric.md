# Assessment Rubric — Project 01: AI Chatbot

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Descriptors below are specific to this project's concepts (see lesson.agent.md §3, §8, §9).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

**Concept checklist this dimension probes:** statelessness → client-side resend; what concretely gives the bot memory; `input_tokens` growth per turn; system prompt vs. first user message; why streaming complicates cost.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains statelessness in own words (ELI12 *and* ELI-Engineer) and correctly names "appending the assistant reply + resending full history" as what gives memory. Predicts quadratic-ish `input_tokens` growth *before* measuring. Original, accurate analogy. Answers diagnostic follow-ups (lesson §Instructor Notes). | 25 |
| 3 — Good | Correct on statelessness and history, minor gaps (e.g. fuzzy on system-prompt placement or why streaming complicates cost). | 20 |
| 2 — Developing | Some correct understanding but a live misconception present (e.g. "the API remembers," "tokens are words"). | 15 |
| 1 — Beginning | Restates lesson language without internalizing; cannot say what concretely gives the bot memory. | 10 |

**Score: ___ / 25** &nbsp;&nbsp; **Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md against source/project.md contracts.

**Milestone coverage (lesson §7):** M1 one-shot · M2 multi-turn · M3 system prompt · M4 streaming · M5 cost. **Contract checks:** `cost_of` matches the I/O table; full history resent every call; system message at the right place for the interface used.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | All five milestones demonstrated. Multi-turn memory correct (pronoun-resolution test passes). Streaming renders incrementally AND final token counts are captured (or the fallback is documented). Cost derived from real `usage`. Clean module separation per project.md. No magic — every line explainable. | 30 |
| 3 — Good | Core loop correct (M1–M3 + one of M4/M5). Minor style/architecture issues or a documented streaming-usage gap. | 24 |
| 2 — Developing | Partial: multi-turn works but streaming or cost missing/incorrect; or history handling subtly wrong. | 18 |
| 1 — Beginning | Does not run, or only sends the latest message (amnesiac bot), or cost is hardcoded/guessed. | 12 |

**Score: ___ / 30** &nbsp;&nbsp; **Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md against the Intentional Breakage Menu (project.md).

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments from the menu. Each *precisely* diagnoses cause (e.g. "dropped assistant append → thread breaks at turn 2 because the model can't see its own prior answer"). States the production implication. | 20 |
| 3 — Good | 2+ experiments with correct diagnosis. | 16 |
| 2 — Developing | 1 experiment, or breakage observed without naming the mechanism. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without analysis. | 8 |

**Score: ___ / 20** &nbsp;&nbsp; **Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md. **Quantitative means real numbers**, not "it seemed to work."

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Reports actual token counts and per-turn cost; hand-verifies one turn against `usage` and it matches. Shows `input_tokens` rising across turns with numbers. Honest production-readiness call with a cost projection at scale. | 15 |
| 3 — Good | Most criteria measured with real numbers; minor gaps (e.g. no scale projection). | 12 |
| 2 — Developing | Mostly qualitative; few numbers; no hand-check of cost. | 9 |
| 1 — Beginning | No meaningful quantitative evaluation. | 6 |

**Score: ___ / 15** &nbsp;&nbsp; **Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 2+ concrete, non-obvious StarcallOS patterns with mechanism + implementation path (e.g. "resend-cost is quadratic → StarcallOS needs retrievable memory, not an ever-growing array; here's where it slots in"). | 10 |
| 3 — Good | 1 concrete applicable pattern, well explained. | 8 |
| 2 — Developing | Generic or surface-level connection. | 6 |
| 1 — Beginning | No meaningful StarcallOS connection. | 4 |

**Score: ___ / 10** &nbsp;&nbsp; **Evidence:**

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

## Red Flags (auto-cap Implementation at Level 2 if present)

- Only the latest user message is sent (no history resend). [lesson §9]
- Cost is hardcoded or guessed rather than read from `usage`. [lesson §9]
- Learner cannot explain why `input_tokens` grows each turn.
- Streaming "works" but final token counts are never captured.

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
