# Assessment Rubric — Elective 01: MCP Interface Layer

> Used to evaluate the learner's completed elective.
> Self-assessment first. Mentor review second.
> This elective grades the **provider/consumer split**: turning a subsystem into a reusable
> protocol surface (tools/resources/prompt + a trust boundary) and consuming it from two
> hosts — **not** rebuilding the memory system (that is provided) or building an agent loop
> (that belongs to the host).

---

## Dimension 1: Understanding (25%)

Evaluated by reviewing UNDERSTANDING.md and UNDERSTANDING_FEEDBACK.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Explains MCP as an **interface protocol, not an agent framework**, and can say exactly where the agent loop now lives (the host). Distinguishes host/client/server and tool/resource/prompt by **control model**. Articulates M×N→M+N with their own memory server as the example, and locates the trust boundary in their code. Original analogy. | 25 |
| 3 — Good | Explains the split, the three participants, and the three primitives correctly with minor gaps (e.g. states the primitives but fuzzy on one control model). | 20 |
| 2 — Developing | Describes "a server exposes tools" but conflates MCP with an agent framework, or can't say where the loop lives, or treats all primitives as tools. | 15 |
| 1 — Beginning | Surface-level; leans on lesson language; can't distinguish provider from consumer. | 10 |

**Score: ___ / 25**  **Evidence:**

---

## Dimension 2: Implementation (30%)

Evaluated by reviewing code/ and IMPLEMENTATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Learner modules are **SDK-agnostic**; `memory_search`/`memory_save` have correct JSON schemas (`required`, bounds, `kind` enum) **and** re-validate in the handler; entries exposed as `memory://entries/{id}` **resources** with list+read; one **prompt** injects recalled memories; `security.py` bounds every input and **contains** the URI, failing closed; server logs to stderr. Clean, no agent loop in the server, all guiding tests pass. | 30 |
| 3 — Good | Core works; minor issues (e.g. validation present but a bound missing, or resource read works but list is partial). | 24 |
| 2 — Developing | Tools work but resources/prompt or the trust boundary is missing/partial; or a learner module imports `mcp`; some tests fail. | 18 |
| 1 — Beginning | Does not run, or no real protocol surface (everything crammed as one tool / loop in the server). | 12 |

**Score: ___ / 30**  **Evidence:**

---

## Dimension 3: Failure Analysis (20%)

Evaluated by reviewing FAILURE_ANALYSIS.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | 3+ intentional experiments, **including** the stdout-corruption bug and a trust-boundary breach (removed bound + hostile input, or a traversal URI). Each correctly diagnoses the failure and states the production implication. | 20 |
| 3 — Good | 2+ experiments with good analysis (at least one of stdout-corruption / trust-boundary). | 16 |
| 2 — Developing | 1 experiment with shallow analysis. | 12 |
| 1 — Beginning | No intentional breakage, or breakage without diagnosis. | 8 |

**Score: ___ / 20**  **Evidence:**

---

## Dimension 4: Evaluation (15%)

Evaluated by reviewing EVALUATION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Demonstrates the **two consumers** explicitly (stdio client + a second host), with what each saw — including a cross-consumer round-trip (save in one, read in the other). Honest read of what the schema/description quality did to tool selection. | 15 |
| 3 — Good | Two consumers shown; minor gaps (no cross-consumer round-trip, or only a screenshot). | 12 |
| 2 — Developing | Only one consumer demonstrated ("it worked in the smoke test"). | 9 |
| 1 — Beginning | No meaningful demonstration. | 6 |

**Score: ___ / 15**  **Evidence:**

---

## Dimension 5: StarcallOS Reflection (10%)

Evaluated by reviewing STARCALLOS_REFLECTION.md.

| Level | Description | Points |
|-------|-------------|--------|
| 4 — Excellent | Identifies 2+ concrete, non-obvious patterns this elective gives StarcallOS (expose its own memory once as a server, consume third-party servers without bespoke glue, the trust boundary as a governance layer, transport choice per deployment) with a mechanism and an implementation path. | 10 |
| 3 — Good | Identifies 1 concrete applicable pattern with a good explanation. | 8 |
| 2 — Developing | Reflection is generic ("StarcallOS could use MCP"). | 6 |
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
| Below 60 | Return to the lesson and rebuild the protocol surface |

---

## Elective-Specific Checks (quick pass/fail before scoring)

- [ ] No learner module imports `mcp` (only `server.py` / `client_smoke_test.py` do)
- [ ] `memory_search`/`memory_save` schemas have `required` + bounds + a `kind` enum, and the handler re-validates
- [ ] Entries are **resources** (`memory://entries/{id}`), not tools; `reflect_on` is a **prompt**
- [ ] `validate_resource_uri` rejects a foreign scheme and a `..` traversal (fails closed)
- [ ] Every input is bounded (`k`, text length, importance, `kind`)
- [ ] Server logs to **stderr**; no `print` to stdout
- [ ] **Two consumers** of the one server are demonstrated; a save in one is read in the other
- [ ] All guiding tests pass offline (`python -m pytest`)
- [ ] No agent loop lives in the server

---

## Mentor Notes

**Overall assessment:**

**Strongest dimension:**

**Area most needing work:**

**Recommended next steps:**
