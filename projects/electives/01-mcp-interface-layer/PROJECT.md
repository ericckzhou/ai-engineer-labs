# Elective 01: MCP Interface Layer

> **Elective** — off the numbered 1–9 spine. It teaches no new model capability; it teaches how
> to *expose* one. Prerequisite skills: Projects 05, 06, 08. It gates nothing.

## What We're Building

An **MCP server** that exposes **Project 05's Personal Memory System** as a reusable protocol
surface — tools (`memory_search`, `memory_save`), resources (`memory://entries/{id}`), and a
prompt (`reflect_on`) — and then consuming that **one server from two different hosts**.

## Why We're Building It

In Projects 06, 08, and 09 you hand-wired tools into a single app loop. That tool is trapped in
that app. This elective teaches the **provider/consumer split**: turn a capability into a
**server** behind the Model Context Protocol so that *many* AI applications (**hosts**) can
consume it through their own **clients** — without importing your code. It is the
**M×N → M+N** integration pattern made concrete, and the connective tissue between the
capabilities the spine built.

## Learning Objectives

- [ ] Explain MCP as an **interface protocol, not an agent framework**
- [ ] Distinguish **host, client, and server**
- [ ] Distinguish **tools vs. resources vs. prompts** (by control model)
- [ ] Explain **stdio vs. Streamable HTTP** transport conceptually
- [ ] Define **JSON schemas** for tool inputs and validate against them
- [ ] Implement **safe handlers** for memory search/save
- [ ] Expose **memory entries as resources**
- [ ] Provide **one reusable prompt**
- [ ] **Consume the same server from two clients/hosts**
- [ ] Analyze the **trust boundary** and security risks

## Key Concepts

Model Context Protocol, provider/consumer split, host/client/server, capability negotiation,
JSON-RPC, tools/resources/prompts, stdio vs Streamable HTTP transport, input schemas, the trust
boundary, M×N → M+N integration.

## Core Engineering Problem

**Problem:** You have a working capability (memory) trapped inside one app. How do you expose it
once, behind a standard protocol, so that any AI application can consume it — safely — without
re-implementing it per app?

## Time Estimate

**Total:** 10–14 hours

## Startup Lens

This is how StarcallOS exposes its own memory **once** as a server (reusable by any host,
including third-party AI apps) and consumes external capabilities without bespoke glue. The
capability is the commodity; the reusable, governed interface is the leverage.

## Key Files

```
code/
  server.py            — Provided: FastMCP/stdio adapter over your modules (no loop here)
  memory_backend.py    — Reference: the Project 05 memory store being wrapped (complete)
  memory_tools.py      — Learner: TOOL_DEFINITIONS (schemas) + search/save handlers (M1–M2)
  security.py          — Learner: the trust boundary — validate args + contain URIs (M1–M3)
  memory_resources.py  — Learner: expose entries as memory://entries/{id} resources (M3)
  prompts.py           — Learner: one reusable reflect_on prompt (M4)
  client_smoke_test.py — Provided: consumer #1, a programmatic stdio client (M5)
  tests/               — Provided: offline guiding tests for each learner-owned milestone
  config.py            — Provider config + the trust-boundary bounds
  requirements.txt · .env.example · pytest.ini · README.md
```

## Definition of Done

The same MCP server is consumed by **two different hosts** (the stdio smoke-test client and
Claude Desktop / the MCP Inspector), with the protocol surface (tools + resources + prompt +
trust boundary) implemented and the offline guiding tests passing. See `source/project.md` for
the full contract.
