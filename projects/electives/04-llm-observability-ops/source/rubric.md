# Assessment Rubric — Elective 04: LLM Observability & Ops

> Self-assessment first, mentor review second. Grades **instrumentation with standard telemetry +
> a per-route drift monitor** — not rebuilding the agent (provided) or a dashboard (extension).

---

## Dimension 1: Understanding (25%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains **observability ≠ evaluation** (telemetry = what happened; judge = was it good), why drift must be **per route not a global mean**, why standard `gen_ai.*` names matter, and why a production judge runs **async on a sample**. Articulates the offline→online loop. Original analogy. | 25 |
| 3 — Good | Explains the distinction + per-route drift with minor gaps. | 20 |
| 2 — Developing | Conflates observability with evaluation, or watches a global average, or thinks the judge runs on every request. | 15 |
| 1 — Beginning | Surface-level; "add logging". | 10 |

**Score: ___ / 25**

---

## Dimension 2: Implementation (30%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Spans use the **standard** `gen_ai.*` attributes; `traced` instruments model + tool calls and records errors as attributes; `aggregate` rolls up **per route**; `detect_drift` flags the regressed route vs a baseline using config thresholds, without false-alarming a healthy window. All guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (one attribute misnamed, or a metric off). | 24 |
| 2 — Developing | Tracing OR monitor works but not both; or aggregation is global; some tests fail. | 18 |
| 1 — Beginning | Doesn't run, or no real per-route drift detection. | 12 |

**Score: ___ / 30**

---

## Dimension 3: Failure Analysis (20%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ experiments **including** a **global-mean blind spot** (a dead route hidden by the average) and a **swallowed error** (tool error not recorded → monitor blind). Each diagnosed with the production implication. | 20 |
| 3 — Good | 2+ experiments, at least one of the two required. | 16 |
| 2 — Developing | 1 shallow experiment. | 12 |
| 1 — Beginning | No intentional breakage. | 8 |

**Score: ___ / 20**

---

## Dimension 4: Evaluation (15%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Runs the fixtures: monitor **catches the seeded regression** AND stays **quiet on the baseline**; reports per-route metrics; makes one **threshold-tuning** move and shows the alert sensitivity change. | 15 |
| 3 — Good | Catches the regression; minor gaps (no false-alarm check, or no tuning). | 12 |
| 2 — Developing | Flags "something changed" globally, not per route. | 9 |
| 1 — Beginning | No meaningful detection demonstrated. | 6 |

**Score: ___ / 15**

---

## Dimension 5: StarcallOS Reflection (10%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 2+ concrete capabilities StarcallOS must trace to run **unattended** (which spans, which drift signal, what alert), with a mechanism and implementation path. | 10 |
| 3 — Good | 1 concrete pattern, well explained. | 8 |
| 2 — Developing | Generic ("add monitoring"). | 6 |
| 1 — Beginning | No meaningful connection. | 4 |

**Score: ___ / 10**

---

## Total Score — **___ / 100**

| Range | Level |
|-------|-------|
| 90–100 | Complete to standard |
| 75–89 | Minor gaps |
| 60–74 | Revisit weak dimensions |
| Below 60 | Return to the lesson |

---

## Elective-Specific Checks (quick pass/fail)

- [ ] Spans use the **standard** `gen_ai.*` attribute names
- [ ] Errors are recorded as **span attributes**, not swallowed
- [ ] `aggregate` is **per route**, not a global mean
- [ ] `detect_drift` flags the regressed route and **not** the healthy baseline
- [ ] EVALUATION shows both: caught regression **and** no false alarm
- [ ] Understanding states **observability ≠ evaluation** and the **async sampled judge** rule
- [ ] All guiding tests pass offline

---

## Mentor Notes
**Overall:** · **Strongest:** · **Needs work:** · **Next steps:**
