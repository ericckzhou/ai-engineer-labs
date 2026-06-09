# ADR: Production & Hardening elective track (E2–E5)

**Date:** 2026-06-09
**Status:** accepted
**Decided by:** Eric (user), proposed by Claude

## Context

The curriculum's 1–9 spine teaches learners to **build** AI systems, escalating to a
composition **capstone at Project 09**. It does not systematically cover the concerns that
separate a demo from a production system: hardening against untrusted input, optimizing
cost/latency, and operating systems online. Four new projects were proposed to fill that gap
(Guardrails, Cost & Latency, Observability & Ops, Advanced RAG). A classification decision was
needed: do they join the numbered spine, become loose standalone electives, or form a grouped
track?

## Options Considered

### Option A: Core spine P10–P13
Add to the numbered build spine after P09.
Pros: signals these are required, central to "AI Systems Engineering."
Cons: moves/dilutes the P09 capstone; forces a linear order on cross-cutting concerns that are
naturally order-independent; large restructure.

### Option B: Loose electives (like E1 MCP)
Each a standalone, unsequenced elective taken any time after its prereq.
Pros: minimal change; matches the existing E1 precedent.
Cons: under-sells production readiness as "optional fluff"; no narrative that these belong
together as the next stage of the journey.

### Option C: Named "Production & Hardening" track (chosen)
Group E2–E5 as a named elective track, off the 1–9 spine, presented as the strongly-recommended
path **after** the P09 capstone.
Pros: keeps the capstone-at-9 structure intact; frames production work as the real next stage
without making it block the build arc; each project still attaches to a specific prereq.
Cons: introduces a new organizing unit ("track") not previously in ARCHITECTURE.md.

## Decision

**Option C.** E2–E5 form a named **"Production & Hardening" elective track**, located under
`projects/electives/`, off the numbered 1–9 spine, recommended after Project 09. Each project
hardens/optimizes/operates a capability the spine already built:

- **E2 Guardrails & Safety Layer** — hardens P08 (and P04) against untrusted input.
- **E3 Cost & Latency Engineering** — optimizes P01/P08, gated by P07's eval.
- **E4 Observability & Ops** — instruments P08, closing P07's offline→online loop.
- **E5 Advanced RAG / Query Engineering** — extends P04 retrieval (depth elective).

## Tradeoff Accepted

These remain *electives*, not required spine — a learner can finish the curriculum at P09
without them. We accept that production concerns are presented as recommended-next rather than
mandatory, in exchange for preserving the build arc's capstone structure and the
order-independence of cross-cutting concerns.

## Consequences

- `ARCHITECTURE.md` and the catalog should reference a "Production & Hardening" track grouping
  under electives (E1 MCP remains a standalone elective; E2–E5 are the track).
- Each project is authored via Workflow A with its own primary sources fetched into `sources/`
  first; concept-map.md and source-map.md updated per project.
- The capstone remains P09. The build spine stays 1–9.

## Revisit If

- The track grows beyond ~4–5 projects (may warrant its own top-level section, not "electives").
- User feedback shows learners treat the track as skippable when it should be required — then
  reconsider promoting it to a required post-capstone tier.
