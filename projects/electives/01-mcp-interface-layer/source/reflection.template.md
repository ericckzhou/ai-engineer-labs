# Reflection Template

> This is source/reflection.template.md — the canonical structure for UNDERSTANDING.md.
> The learner fills in UNDERSTANDING.md (root level), not this file.

---

## Pre-Implementation Section

Fill this out BEFORE writing any code.

### 1. Core Concept (ELI12)

**Prompt:** Explain MCP like you would to a curious 12-year-old. Use an analogy (the "standard
plug" / USB-C idea is a start — make it your own). Avoid jargon.

*Learner writes here.*

---

### 2. Core Concept (ELI-Engineer)

**Prompt:** Now with technical depth. What is MCP actually doing — the data layer vs. the
transport, the JSON-RPC handshake, the three primitives? Assume the reader knows software
engineering and has done Projects 06/08, but not MCP.

*Learner writes here.*

---

### 3. Real-World Analogy

**Prompt:** What does the provider/consumer split remind you of outside AI (drivers/USB,
power sockets, an API contract)? The analogy should explain the *mechanism* (and the trust
boundary), not just the surface.

*Learner writes here.*

---

### 4. Why It Exists

**Prompt:** In Projects 06/08 you hand-wired tools into one loop. What broke about that, and
what is the M×N → M+N problem MCP solves? Use your memory server as the concrete example —
who are the M and the N?

*Learner writes here.*

---

### 5. What Breaks Without It

**Prompt:** If a vendor (or StarcallOS) had no protocol like MCP, what would integrating
capabilities cost? Name two specific failures (duplication/drift, no discovery, transport
lock-in, untyped inputs, stdout corruption, over-broad capability).

*Learner writes here.*

---

### 6. My Mental Model

**Prompt:** Draw the boxes — host, client, server, model, your memory store — and the flow of
`initialize`, `tools/list`, `tools/call`, `resources/read`. **Where is the agent loop?**
**Where is the trust boundary?**

*Learner writes here.*

---

### 7. My Prediction

**Prompt:** Before you implement: what will be hardest — keeping the loop *out* of the server,
classifying tool vs. resource vs. prompt, or the trust-boundary checks? What will surprise you?

*Learner writes here.*

---

### 8. Open Questions

**Prompt:** What do you still not fully understand about MCP? (stdio vs HTTP? capability
negotiation? client primitives like sampling/elicitation?)

*Learner lists questions here.*

---

## Post-Implementation Section

Fill this out AFTER building, breaking, and demonstrating two consumers.

### 9. What Changed

**Prompt:** What did wrapping P05 teach you that the lesson didn't? Where was your mental model
of "what a server is" wrong?

*Learner writes here.*

---

### 10. Biggest Surprise

**Prompt:** What surprised you most — running one server from two hosts, the stdout bug, how
little the server "does," or something else?

*Learner writes here.*

---

### 11. What I Got Wrong Initially

**Prompt:** What did you believe about MCP before that turned out incorrect or incomplete?
(e.g. "MCP is an agent framework," "everything is a tool," "the schema is just docs".)

*Learner writes here.*

---

### 12. Updated Mental Model

**Prompt:** Update your diagram from section 6 based on what you learned. What moved?

*Learner writes here.*

---

### 13. The One Thing

**Prompt:** If you could tell your past self one thing before starting this elective, what
would it be?

*Learner writes here.*
