# Assessment Rubric — Project 08: AI Agent

> Used to evaluate the learner's completed project.
> Self-assessment first. Mentor review second.
> Dimensions and weights are the lab-standard master rubric; the **Project-08 evidence prompts**
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

**Project-08 evidence prompts — look for whether the learner can:**
- Draw the **workflow vs. agent** line, and say what an agent gains *control of* that makes it both more capable and more dangerous.
- Explain why `max_steps` alone is insufficient — what **stuck detection** catches early and what a **token budget** catches that a step cap misses.
- Describe **recovery** correctly: catch a raising tool, feed the error back as an *observation*, and why `except: pass` is worse than crashing.
- Justify **"use the simplest thing that works"** with a concrete task they would *not* solve with an agent.

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

**Project-08 evidence prompts — look for whether the implementation:**
- `safety.detect_stuck` flags only **identical** repeated actions (tool **and** args) and not different productive steps. (M1)
- `safety.BudgetTracker` enforces a **steps** ceiling **and** a **tokens** ceiling; `over_budget()` returns a *reason string*, not just a bool. (M2)
- `agent.run_agent` catches a **raising** tool and feeds the error back (recovery), appends the assistant turn **before** the tool results, and returns a distinct `stop_reason`. (M3)
- `evaluate.evaluate_run` reports completion (keyed off `stop_reason` **and** the expected substring), steps, tool calls, and efficiency. (M4)
- The live agent (M5) runs a multi-step task and prints a trace + the eval summary.
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

**Project-08 evidence prompts — strong analyses typically include:**
- A **no-budget ablation** (remove the token/step ceiling) with a model/task that runs away, showing the cost blow-up.
- A **no-stuck-detection ablation** showing an agent oscillating on identical actions until `max_steps`, wasting the budget.
- A **no-recovery ablation** (let a tool raise) showing one bad tool call discard the whole multi-step run.
- The **"agent where a single call would do" ablation**: a task solved with the loop *and* with one call, with the numbers (steps, tokens, latency) showing the loop is measurably worse — the "use the simplest thing that works" lesson made concrete.

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

**Project-08 evidence prompts — quantitative means actual numbers/traces, e.g.:**
- A **run table** across several tasks: `stop_reason`, steps, tool calls, efficiency, token cost per run (via `evaluate_run`).
- **Stop-reason distribution**: how often the agent `answered` vs. hit `stuck` / `budget` / `max_steps`, and what that says about the task set or the prompt.
- **Efficiency** numbers (steps vs. optimal) and how a prompt or model change moved them — the regression discipline from Project 07 applied to runs.
- An honest production note: token cost per task, and which tasks did not need an agent at all.

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

**Project-08 evidence prompts — concrete connections include:**
- A StarcallOS capability that **acts autonomously on the user's behalf**, framed with the four guards — budget, stuck detection, recovery, and an auditable run log — naming the ceiling each enforces.
- How the **judgment** to route a simple request to a single call (not the loop) keeps StarcallOS fast and cheap — mechanism + implementation path, not "we could add an agent."

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
