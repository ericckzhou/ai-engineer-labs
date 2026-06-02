# Assessment Rubric — Project 09: Personal Learning OS

> Used to evaluate the learner's completed capstone.
> Self-assessment first. Mentor review second.
> This capstone grades **composition**: routing, orchestration, the knowledge graph, and a
> system-level evaluation — not the rebuilding of any single subsystem (those are provided).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains routing as classify-then-dispatch and can justify **precedence** and the **safe default** as correctness decisions, each tied to a concrete failure (lost save, runaway cost). Explains why provenance is part of the contract and why per-route eval beats a mean. Original analogy. | 25 |
| 3 — Good | Explains routing, orchestration, and provenance correctly with minor gaps (e.g. states precedence but not the cost asymmetry). | 20 |
| 2 — Developing | Describes "a router picks a subsystem" but treats precedence/default as arbitrary, or conflates the orchestrator with a subsystem. | 15 |
| 1 — Beginning | Surface-level: lists the routes but can't say why order or the default matters. Heavy reliance on lesson language. | 10 |

**Score: ___ / 25**

**Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | `route_query` classifies by precedence with a safe default; `handle` dispatches to **exactly one** subsystem and returns a `Response` with route + provenance; saves flow into store **and** graph; `KnowledgeGraph` is incremental, symmetric, self-free; `evaluate_routing` reports overall + per-route + misroutes. Clean, no magic, all guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (e.g. provenance present but partial, or graph correct but rebuilt rather than incremental). | 24 |
| 2 — Developing | Router or orchestrator partially works; `handle` inlines worker logic, or provenance/graph is missing a property. Some tests fail. | 18 |
| 1 — Beginning | Does not run, or routes nothing correctly / orchestrator doesn't dispatch via the table. | 12 |

**Score: ___ / 30**

**Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments, **including** the mis-ordered-precedence (lost save) and route-everything-to-`TASK` (cost/latency) ablations. Each correctly diagnoses the failure and states the production implication. | 20 |
| 3 — Good | 2+ ablations with good analysis (at least one of precedence / default / provenance). | 16 |
| 2 — Developing | 1 ablation with shallow analysis. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without diagnosis. | 8 |

**Score: ___ / 20**

**Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Routing accuracy reported **overall and per route** on a frozen labeled set, with the misroutes listed; includes the measured cost/latency delta of the `TASK`-everything ablation. Honest read of where the router is weak. | 15 |
| 3 — Good | Overall + per-route numbers present; minor gaps (no misroute list or no cost delta). | 12 |
| 2 — Developing | Mostly a single overall number ("~90%, seems good"); no per-route breakdown. | 9 |
| 1 — Beginning | No meaningful evaluation. | 6 |

**Score: ___ / 15**

**Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Identifies 2+ concrete, non-obvious patterns this capstone gives StarcallOS (router as front door, dispatch registry, provenance as trust layer, system-level eval) with a mechanism and an implementation path. | 10 |
| 3 — Good | Identifies 1 concrete applicable pattern with a good explanation. | 8 |
| 2 — Developing | Reflection is generic ("StarcallOS could use routing"). | 6 |
| 1 — Beginning | No meaningful StarcallOS connection. | 4 |

**Score: ___ / 10**

**Evidence:**

---

## Total Score

**___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Capstone complete — curriculum finished to standard |
| 75–89 | Complete with minor gaps — document them |
| 60–74 | Revisit the weak dimensions before considering it done |
| Below 60 | Return to the lesson and rebuild the composition layer |

---

## Capstone-Specific Checks (quick pass/fail before scoring)

- [ ] `route_query` checks `SAVE` before `CHAT` (a "remember this" never routes to `CHAT`)
- [ ] The safe default is `CHAT`, not `TASK` or `SAVE`
- [ ] `handle` dispatches via the table to exactly one subsystem (does not retrieve/save itself)
- [ ] Every `Response` carries `route` + `provenance` (returned, not printed)
- [ ] `KnowledgeGraph`: no self-edge, symmetric edges, incremental `add`
- [ ] `evaluate_routing` returns per-route accuracy + misroutes, not just a mean
- [ ] All guiding tests pass offline (`python -m pytest`)

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
