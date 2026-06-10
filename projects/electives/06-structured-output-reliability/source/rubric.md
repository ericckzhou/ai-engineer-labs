# Assessment Rubric — Elective 06: Structured Output & Reliability

> Self-assessment first, mentor review second. Grades the **reliability core** (extract / validate /
> repair loop, failing closed, measured) — not the schema (provided) or the backend (provided).

---

## Dimension 1: Understanding (25%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Names the three failure modes (format / syntax / schema-violation), explains why extraction (format) and validation (contract) are different stages, why the layer must **fail closed**, and why repair must carry the **specific** errors. Knows the `bool`/`int` trap. Original analogy. | 25 |
| 3 — Good | Explains the loop and fail-closed with minor gaps. | 20 |
| 2 — Developing | "Parse the JSON and retry" — conflates extraction with validation, or misses that valid JSON can still violate the schema. | 15 |
| 1 — Beginning | Surface-level; "json.loads and hope". | 10 |

**Score: ___ / 25**

---

## Dimension 2: Implementation (30%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | `extract_json` strips fences/prose via balanced-brace scan; `validate` flags missing/type/enum/range and **rejects bool-as-int**, returning usable error strings; `coerce` repairs with the errors, respects `max_attempts`, and **raises `StructuredOutputError`** (never returns an unvalidated object). All guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (extraction misses a prose case, or one validation class). | 24 |
| 2 — Developing | Happy path works but doesn't fail closed, or repair is a blind retry, or the bool trap slips through; some tests fail. | 18 |
| 1 — Beginning | Doesn't run, or returns unvalidated objects. | 12 |

**Score: ___ / 30**

---

## Dimension 3: Failure Analysis (20%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ experiments **including** (a) a **blind retry** (no error feedback) failing to converge on the schema case, and (b) the **`bool`/`int` trap** letting an invalid object pass a naive check. Each diagnosed with the implication. | 20 |
| 3 — Good | 2+ experiments, at least one of the two required. | 16 |
| 2 — Developing | 1 shallow experiment. | 12 |
| 1 — Beginning | No intentional breakage. | 8 |

**Score: ___ / 20**

---

## Dimension 4: Evaluation (15%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Reports success **per failure kind** (clean/fenced/prose/schema/unfixable), naive vs robust, **and the repair cost** (extra generations). Correctly states the unfixable case **should** stay failed (fail closed), and that naive "parse success" on schema cases is a false positive. | 15 |
| 3 — Good | Per-kind success reported; minor gaps (e.g. no cost). | 12 |
| 2 — Developing | Only an overall "it's more reliable" without per-kind numbers. | 9 |
| 1 — Beginning | No real measurement. | 6 |

**Score: ___ / 15**

---

## Dimension 5: StarcallOS Reflection (10%)

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 2+ concrete StarcallOS chains where one unreliable hop poisons the rest (mis-parsed action runs the wrong tool; mis-typed route mis-classifies), with the mechanism and where coerce sits. | 10 |
| 3 — Good | 1 concrete pattern, well explained. | 8 |
| 2 — Developing | Generic ("more reliable"). | 6 |
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

- [ ] `extract_json` handles fences AND prose, raises on no-JSON
- [ ] `validate` rejects **bool where int is required**
- [ ] `validate` returns usable error strings (fed into the repair prompt)
- [ ] `coerce` repairs with the **specific** errors (not a blind retry)
- [ ] `coerce` **fails closed** — raises `StructuredOutputError`, never returns an unvalidated object
- [ ] Attempt budget (`max_attempts`) is respected
- [ ] EVALUATION reports success **per failure kind** + repair cost
- [ ] All guiding tests pass offline

---

## Mentor Notes
**Overall:** · **Strongest:** · **Needs work:** · **Next steps:**
