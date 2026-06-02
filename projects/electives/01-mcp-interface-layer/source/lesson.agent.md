# Lesson (Agent Version): MCP Interface Layer — Turning a Subsystem into a Reusable Protocol Surface

> **Canonical source of truth.** This is the dense, LLM-facing version. The human version
> (`rendered/lesson.html`) is derived from this file. If they conflict, this file wins.
> **Elective.** Not part of the numbered 1–9 spine. Prerequisite skills come from
> Projects 05, 06, and 08; it does not gate any other project.

---

## Metadata

- **Project:** Elective 01 — MCP Interface Layer
- **Track:** Elective (advanced, off-spine)
- **Estimated time:** 10–14 hours
- **Prerequisites:** Project 05 (Personal Memory System — the subsystem you will wrap),
  Project 06 (Tool Use / agent-computer interface), Project 08 (reliable agent loop).
  Strongly recommended; this lesson assumes you have already hand-wired tools into a loop.
- **Wrapped subsystem:** Project 05's memory store (search + save over a memory stream).
- **Primary sources:**
  - `sources/official-docs/mcp-architecture.md` (participants, layers, JSON-RPC, transports, primitives)
  - `sources/official-docs/mcp-build-server.md` (FastMCP server in Python, stdio, host config)
  - `sources/official-docs/anthropic-tool-use.md` (the hand-wired tool loop this lesson generalizes)
  - `sources/articles/building-effective-agents.md` (the augmented LLM; "the description is the API")

---

## Learning Objectives

By the end of this elective, the learner will be able to:

1. **Explain MCP as an interface protocol, not an agent framework** — articulate that MCP
   standardizes *how an AI app obtains context and actions from external programs*, and
   says nothing about the agent loop, prompting, or model choice. (`mcp-architecture.md` —
   "MCP focuses solely on the protocol for context exchange.")
2. **Distinguish host, client, and server** — name what each is, and explain "one client
   per server" and why the host fans out to many servers.
3. **Distinguish tools vs. resources vs. prompts** — give the definition and control model
   of each (model-controlled / application-controlled / user-controlled) and decide which
   primitive a given capability belongs to.
4. **Explain stdio vs. Streamable HTTP transport conceptually** — local single-client over
   stdin/stdout vs. remote multi-client over HTTP with auth — and why the same data-layer
   surface runs over either.
5. **Define JSON schemas for tool inputs** — write an `inputSchema` (types, required,
   bounds, enums) that is the contract the model sees, and validate against it.
6. **Implement safe handlers for memory search/save** — wrap Project 05's store behind
   tool handlers that validate, execute, and return MCP content.
7. **Expose memory entries as resources** — serve entries by URI with discovery + read,
   and contain the URI namespace.
8. **Provide one reusable prompt** — a parameterized template that pulls memory context
   into a structured message.
9. **Consume the same server from two clients/hosts** — prove the M×N → M+N decoupling by
   running one server against (a) a programmatic stdio client and (b) a second host
   (Claude Desktop / MCP Inspector).
10. **Analyze the trust boundary and security risks** — explain that tool arguments and
    resource URIs are untrusted model/host input crossing a process boundary, and the
    failure modes (path/URI escape, unbounded inputs, stdout corruption, over-broad
    capability).

---

## 1. Motivation

### Why this exists

In Projects 06, 08, and 09 you built tools the only way you knew how: a Python function
(`read_file`, `search_memory`, `run_tests`), a hand-written JSON schema next to it, and a
dispatch block inside *your* agent loop that matched the model's tool call to the function
and fed the result back. It worked. But every one of those tools is **trapped inside the
app that defined it.** Your copilot's `read_file` cannot be used by your agent without
copy-pasting it; neither can be used by Claude Desktop, Cursor, or a teammate's app at all.

You have built the same handful of capabilities — search a store, save a note, read a file
— several times, once per app, because there was no shared way to *expose* a capability so
that *any* AI application could consume it. That missing shared way is the **Model Context
Protocol (MCP)**: an open, client-server protocol that standardizes how an AI application
("host") obtains context and actions from an external program ("server"). MCP "focuses
solely on the protocol for context exchange—it does not dictate how AI applications use
LLMs or manage the provided context" (`mcp-architecture.md`). It is a **plug**, not a brain.

This elective's single new idea is the **provider/consumer split**: stop hand-wiring tools
*into* one loop, and instead turn a capability into a **server** that lives behind a
standard protocol surface, so that many independent **hosts** can consume it through their
own **clients**. You will take the memory system you built in Project 05 and expose it as
an MCP server, then consume that one server from two different hosts.

### The integration problem it solves (M×N → M+N)

Before a standard, connecting *M* AI applications to *N* capabilities is an *M×N* problem:
every app needs a bespoke adapter for every capability (your copilot's file tool, your
agent's file tool, the next app's file tool — all different code). With one protocol, each
host speaks MCP **once** and each capability is exposed **once**: the integration surface
collapses to *M+N*. (This is the standard engineering articulation of the documented "any
server, any host" property — see the truth note in `mcp-architecture.md`; it is an
interpretation, not a protocol quote.)

### What breaks without it

Without a protocol you live in the *M×N* world: capabilities are duplicated per app, drift
out of sync, and can't be shared or swapped. A vendor who wants their service usable from
"any AI app" has to write and maintain an integration for each one. And inside a single
team, the memory system you spent Project 05 building stays locked to the one script that
imported it — the moment a second app wants memory, you copy code.

> **Startup lens (StarcallOS).** A personal OS is exactly a host that wants to consume many
> capabilities — memory, calendar, files, search — ideally without re-implementing each.
> MCP is how StarcallOS would expose its memory once and consume third-party capabilities
> without bespoke glue. The capability is the commodity; the **reusable, governed interface**
> is the leverage.

---

## 2. ELI12

Imagine every kind of plug and socket in your house was different: the toaster only fit one
special outlet, the lamp another, the phone charger a third. Buying a new lamp would mean
rewiring the wall. That's how AI apps used to talk to tools — every app and every tool had
its own private shape, so nothing fit anything else.

Then someone invented a **standard plug** (think of USB-C). Now the wall socket doesn't care
*what* you plug in, and the device doesn't care *which* wall it's in — as long as both speak
"USB-C," they just work. MCP is that standard plug for AI. Your memory system becomes a
device with a USB-C plug; any AI app with a USB-C socket can use it, and you only had to add
the plug **once.**

The plug carries three kinds of things: **buttons the AI can press** (tools — "save this,"
"search that"), **things the AI can read** (resources — your saved notes), and **ready-made
question cards** (prompts — "help me remember everything about ___"). Your job in this
project isn't to invent a new gadget — you already built the memory gadget. Your job is to
put the right plug on it so anything can use it.

---

## 3. ELI-Engineer

MCP is a **JSON-RPC 2.0** protocol with a clean **two-layer** design (`mcp-architecture.md`):

- **Data layer** (inner): the message semantics — lifecycle/capability negotiation, and the
  primitives **tools**, **resources**, **prompts**, plus notifications. This is the surface
  *you* design.
- **Transport layer** (outer): how bytes move — **stdio** (subprocess, stdin/stdout, one
  client, no network) or **Streamable HTTP** (remote, many clients, HTTP POST + optional
  SSE, auth via bearer/OAuth). "The transport layer abstracts communication details … 
  enabling the same JSON-RPC 2.0 message format across all transport mechanisms."

Three participants:

- **Host** — the AI application (Claude Desktop, VS Code, Claude Code). It "coordinates and
  manages one or multiple MCP clients."
- **Client** — a connection manager inside the host; **one client per server**, dedicated
  connection.
- **Server** — "a program that provides context to MCP clients," local or remote. *This is
  what you build.*

A connection begins with an **`initialize`** handshake that does **capability negotiation**:
each side declares what it supports (e.g. the server declares `tools` and `resources`)
*before* anyone calls anything, so unsupported operations are never attempted. Then the
client **discovers** primitives with `*/list`, **retrieves**/**executes** with
`*/read`/`tools/call`.

The three **server primitives** and their control models:

| Primitive | What it is | Who drives it | MCP methods |
|-----------|------------|---------------|-------------|
| **Tool** | An executable function that performs an action | **Model** decides to call (host gates w/ user approval) | `tools/list`, `tools/call` |
| **Resource** | A data source providing context, addressed by URI | **Application** reads it as context | `resources/list`, `resources/read` |
| **Prompt** | A reusable, parameterized message template | **User** invokes it | `prompts/list`, `prompts/get` |

The connection to Project 06: there you learned "the description is the API" — the model
picks a tool from its name, description, and JSON schema alone. MCP makes that literal and
*portable*. In the Python SDK, **FastMCP** derives the `inputSchema` from your function's
type hints and the tool `description` from its docstring (`mcp-build-server.md`). So the
exact ACI discipline from Project 06 — precise schema, an honest description — is now the
contract every host's model sees, not just your own loop's.

The new mental shift: you are no longer writing *the loop that calls tools*. You are writing
*the tools (and resources and prompts) that any loop can call.* The loop — the host — is
someone else's program now.

---

## 4. Real-World Analogy

**MCP is the device-driver / USB model for AI capabilities.**

Before standardized drivers, every printer shipped with bespoke software for every operating
system, and an OS could only talk to hardware it had custom code for — an *M×N* mess of
combinations. A **driver model** plus a **bus standard** (USB) inverted this: the OS speaks
the bus protocol once; each device ships one driver that exposes a standard interface
(enumerate capabilities, read, write). Now any OS works with any compliant device, and the
device maker writes their integration *once*.

Map it:

- **USB bus / driver contract** → MCP (the protocol + the primitive contract).
- **Operating system** → the **host** (the AI app).
- **The OS's USB controller, one per device** → the **client** (one per server).
- **A peripheral (printer, webcam)** → the **server** (your memory capability).
- **Device enumeration** ("what can you do?") → **capability negotiation** + `*/list`.
- **Plugging a printer into two different laptops** → consuming one server from two hosts.

The analogy also carries the **trust boundary**: a USB device can be malicious (BadUSB), so
the OS mediates and the user grants access. Likewise an MCP server's tools run *real code*
the host's model can invoke — the host asks for user approval, and the server must treat
every incoming argument as untrusted.

---

## 5. What Problem It Solves (before vs. after)

**Before (Projects 06/08/09):**

```python
# Inside YOUR agent loop — the tool is welded to this app.
TOOLS = [{"name": "search_memory", "description": "...",
          "input_schema": {...}}]                 # schema hand-written here
def dispatch(name, args):
    if name == "search_memory":
        return memory.search(args["query"])        # only THIS process can call it
# ... your loop matches the model's tool_use block to dispatch() ...
```

The capability and the consumer are the same program. To reuse `search_memory` elsewhere you
copy the function, the schema, and the dispatch wiring.

**After (this elective):**

```python
# server.py — the capability is a standalone protocol surface.
@mcp.tool()
def memory_search(query: str, k: int = 5) -> str:
    """Search the personal memory store and return the top-k entries."""
    ...                       # schema + description derived by the SDK; ANY host can call it
mcp.run(transport="stdio")    # the loop lives in the host, not here
```

Now the memory capability is consumable by your agent, Claude Desktop, the MCP Inspector,
and a teammate's app — **without any of them importing your code.** You wrote the plug once.

What the split buys, concretely:

- **Reuse:** one server, many hosts (the *M+N* collapse).
- **Separation of concerns:** the server owns the capability + its safety; the host owns the
  loop, the prompt, and the model. Each can evolve independently.
- **Swappability:** a host can swap your memory server for another that speaks the same
  primitives, with zero host code changes — the symmetric benefit of provider abstraction
  (cf. LiteLLM swapping model *providers* in Project 01, now applied to *capabilities*).

---

## 6. What Breaks Without It

Specific failure modes that motivate each piece of the protocol:

1. **Capability duplication & drift.** Without a server boundary, every app re-implements
   "search my memory." Three copies → three behaviors → silent inconsistency. *MCP gives one
   authoritative server.*
2. **No discovery.** Without `*/list` + capability negotiation, a host can't learn what a
   capability offers; you hard-code assumptions and break on change. *Negotiation makes the
   surface self-describing and versioned.*
3. **Transport lock-in.** Hand-wired tools assume in-process calls. The day you need the
   capability on another machine, you rewrite everything. *The data/transport split means
   stdio→HTTP is a one-line change, not a rewrite.*
4. **Untyped, unguarded inputs.** An in-process call trusts its caller. Across a protocol
   boundary the arguments come from a model in someone else's host — untrusted. Without a
   schema and validation, a malformed or hostile argument reaches your store. *`inputSchema`
   + handler validation is the airlock.*
5. **The stdout corruption bug.** On stdio the protocol *is* stdin/stdout; a stray
   `print("debug")` injects bytes into the JSON-RPC stream and "will corrupt the JSON-RPC
   messages and break your server" (`mcp-build-server.md`). Without understanding the
   transport, your server mysteriously dies. *Log to stderr.*
6. **Over-broad capability (the confused-deputy risk).** Expose a too-powerful tool (e.g.
   "run any shell command," or memory `save` with no limits) and you've handed every
   connected host's model that power. *Minimal, well-scoped primitives + a trust-boundary
   review.*

---

## 7. Production Usage

MCP is how real AI applications integrate external capabilities today:

- **Hosts:** Claude Desktop, Claude Code, and VS Code all act as MCP hosts that launch/connect
  to servers and merge their tools into the model's available toolset
  (`mcp-architecture.md`, `mcp-build-server.md`). (This very environment exposes dozens of MCP
  servers to the assistant — GitHub, Notion, Playwright, memory, etc.)
- **Local (stdio) servers:** the reference **filesystem** server, launched as a subprocess by
  the host — single client, no network. The canonical shape you will build.
- **Remote (Streamable HTTP) servers:** e.g. the hosted **Sentry** server — many clients,
  HTTP, OAuth/bearer auth. The same primitives, a different transport.
- **Tooling:** the **MCP Inspector** is the standard zero-code way to exercise a server's
  tools/resources/prompts during development; **reference servers** and per-language SDKs
  (Python `mcp`, TypeScript `@modelcontextprotocol/sdk`, and others) are published officially.
- **The pattern at scale:** a server exposes **tools** for actions, **resources** for context
  (e.g. a DB server exposes query tools, the schema as a resource, and a few-shot prompt for
  using them — the canonical example in `mcp-architecture.md`), and the host composes many
  such servers behind one model.

What separates this from a plain REST API: MCP is **AI-native** — capability negotiation, the
tool/resource/prompt control models, and a content format built for feeding an LLM, plus
client primitives (sampling, elicitation) that let a *server* ask the host's model or user
for help while staying model-independent.

---

## 8. Code Example (minimal, runnable shape)

A complete-but-minimal memory server. (In the project you implement the handlers, schemas,
resources, prompt, and security; the SDK wiring below is `provided` in `server.py`.)

```python
# server.py — the transport boilerplate + registration is PROVIDED.
import sys
from mcp.server.fastmcp import FastMCP
from memory_backend import MemoryBackend
import memory_tools, memory_resources, prompts   # learner-owned, SDK-agnostic

mcp = FastMCP("personal-memory")
backend = MemoryBackend()

@mcp.tool()
def memory_search(query: str, k: int = 5) -> str:
    """Search the personal memory store; return the top-k most relevant entries."""
    return memory_tools.handle_search({"query": query, "k": k}, backend)["text"]

@mcp.tool()
def memory_save(text: str, kind: str = "episodic", importance: float = 5.0) -> str:
    """Save a new memory entry. kind ∈ {episodic, semantic, procedural}."""
    return memory_tools.handle_save(
        {"text": text, "kind": kind, "importance": importance}, backend)["text"]

@mcp.resource("memory://entries/{entry_id}")
def read_entry(entry_id: str) -> str:
    """Expose one stored memory entry as a readable resource."""
    return memory_resources.read_resource(f"memory://entries/{entry_id}", backend)["text"]

@mcp.prompt()
def reflect_on(topic: str) -> str:
    """A reusable template: recall what I know about a topic and reflect."""
    return prompts.get_prompt("reflect_on", {"topic": topic}, backend)["text"]

if __name__ == "__main__":
    print("personal-memory MCP server starting on stdio", file=sys.stderr)  # NEVER stdout
    mcp.run(transport="stdio")
```

The learner-owned modules are **pure** (no SDK import) so they're offline-testable; the SDK
adapter above turns plain returns into MCP content. A handler sketch (the learner fills the
core):

```python
# memory_tools.py  [learner]
from security import validate_search_args
def handle_search(args: dict, backend) -> dict:
    q, k = validate_search_args(args)           # untrusted input crosses the boundary here
    hits = backend.search(q, k=k)               # wraps Project 05's retrieve()
    lines = [f"[{m.id}] ({m.kind}) {m.text}" for m in hits]
    return {"text": "\n".join(lines) or "No matching memories."}
```

And the two consumers that satisfy the definition of done:

```python
# client_smoke_test.py (PROVIDED): consumer #1 — a programmatic stdio client
async with stdio_client(StdioServerParameters(command="python", args=["server.py"])) as (r, w):
    async with ClientSession(r, w) as session:
        await session.initialize()                       # capability negotiation
        print(await session.list_tools())                # discovery
        print(await session.call_tool("memory_save", {"text": "demo on June 20"}))
        print(await session.call_tool("memory_search", {"query": "demo"}))
```

```jsonc
// consumer #2 — Claude Desktop (claude_desktop_config.json), no code
{ "mcpServers": { "personal-memory": {
    "command": "python", "args": ["C:\\ABSOLUTE\\PATH\\TO\\code\\server.py"] } } }
```

One server. Two hosts. Zero shared code. That is the whole lesson in five files.

---

## 9. Common Mistakes

| Mistake | Why it happens | Consequence | Fix |
|---------|----------------|-------------|-----|
| Treating MCP as an agent framework ("where's the loop?") | Coming from Projects 06/08 where you owned the loop | You try to put planning/looping in the server; it belongs in the host | The server only *exposes* capabilities; the host owns the loop, prompt, model |
| `print()` to stdout in a stdio server | Habit; debugging | Corrupts the JSON-RPC stream — server "breaks" mysteriously | Log to **stderr** (`print(..., file=sys.stderr)` or `logging`) |
| Putting everything in tools | Tools are the familiar primitive | A read-only note becomes a model-invoked action; wrong control model | Data the host should read = **resource**; an action the model takes = **tool**; a template a user runs = **prompt** |
| Vague tool description / loose schema | "The function name says it all" | The model mis-calls or can't choose the tool; bad inputs slip through | The description + JSON schema **are the API** (Project 06); be precise, set `required`, bounds, enums |
| Trusting tool arguments / resource URIs | In-process habit — callers were trusted | Untrusted model/host input reaches your store; URI escapes the namespace | Validate every argument; contain the URI (scheme + known-id allow-list), fail closed |
| Unbounded inputs | No limits on `k`, `text`, importance | A huge `k` or megabyte `text` exhausts memory/latency | Clamp `k`, cap text length, range-check importance — in `security.py` |
| Hardcoding a transport assumption | Only ever ran stdio | Can't move the capability off-box without a rewrite | Keep handlers transport-agnostic; transport is a one-line `mcp.run(...)` choice |
| Skipping capability negotiation / discovery in the client | "I know the tools" | Brittle to change; not how hosts actually work | Always `initialize()` then `list_*` before calling |

---

## 10. Production-Level Understanding

What separates a novice from an expert on MCP:

- **The split is the point.** A novice asks "how do I add a loop to my server?" An expert
  knows the server is *inert* — it exposes a governed surface; the *host* supplies the
  intelligence. The value is the decoupling, not the cleverness of any one tool.
- **Primitive choice is a design decision with a control model.** Experts choose tool vs.
  resource vs. prompt by *who should drive it* (model / app / user), not by convenience.
  Mis-classifying (e.g. a destructive action as a resource, or read-only data as a tool) is
  a design smell.
- **The schema/description is the contract, and it's adversarial.** The same precision the
  ACI lesson taught (Project 06) now faces *untrusted* callers. An expert writes schemas
  that constrain (bounds, enums, `required`) and validates again in the handler, because the
  schema is advisory to a model that can ignore or be wrong.
- **Transport is a deployment choice, not an architecture choice.** stdio for local/single,
  Streamable HTTP for remote/multi with auth — same surface either way. Experts design the
  data layer once and pick the transport per deployment.
- **The trust boundary is real and bidirectional.** Tool args and resource URIs flowing *in*
  are untrusted (validate, contain, fail closed). And exposing a capability *out* hands its
  power to every connected host — minimal scope and least privilege apply. This is the
  Project 06 sandboxing lesson, now across a *process* boundary.
- **It composes with everything you built.** MCP doesn't replace Projects 01–09 — it's how
  their capabilities get *exposed and consumed*. Memory (P05) becomes a server; an agent
  (P08) becomes a host that consumes servers; the Learning OS (P09) could route to MCP
  servers instead of in-process workers. MCP is the connective tissue, not a new brain.

> **Truth note.** MCP itself introduces no model technique; it is a protocol. The lightweight
> claims about *which* primitive fits *which* use, and the M×N→M+N framing, are engineering
> interpretations grounded in the official docs' definitions and control models (see
> `sources/official-docs/mcp-architecture.md`), not invented protocol features.

---

## Guided Examples

### Simple case — one tool, one host

Expose `memory_search` only; connect the programmatic client; `initialize` → `list_tools`
→ `call_tool("memory_search", {"query": "France", "k": 3})`. Observe: the client never
imports `memory_backend`; it learns the tool from discovery and calls it over the protocol.
*Lesson:* the consumer is fully decoupled from the provider.

### Real-world case — tools + resources + prompt, two hosts

Add `memory_save`, expose entries as `memory://entries/{id}` resources, and a `reflect_on`
prompt. Run the same server from (a) the stdio smoke-test client and (b) Claude Desktop (or
the MCP Inspector). Save a note in one session; read it as a resource in the other. *Lesson:*
one governed surface, multiple independent consumers — the M+N collapse, made concrete.

### Failure case — the trust boundary

Send `memory_search` a `k` of 10_000_000 and a 5 MB `text` to `memory_save`; request
`memory://entries/../../etc/passwd` and `file:///secret`. A naive handler hangs, stores junk,
or escapes the namespace. With `security.py` validating bounds and containing the URI scheme
+ id allow-list, each is rejected and fails closed. *Lesson:* across a protocol boundary,
every input is hostile until validated.

---

## Reflection Prompts (for `UNDERSTANDING.md`)

1. In your own words, why is "MCP is a protocol, not an agent framework" the single most
   important framing of this elective? What did you *stop* writing that you wrote in P06/P08?
2. Explain host vs. client vs. server to someone who knows P08 but not MCP. Where did the
   agent loop go?
3. You have a capability "the current weather," "my saved notes," and "a draft-a-summary
   template." Which is a tool, which a resource, which a prompt — and why (use the control
   models)?
4. Why does the same server run unchanged over stdio and over Streamable HTTP? What *does*
   change between them, and when would you pick each?
5. Where exactly is the trust boundary in your server? Name two inputs that cross it and the
   specific check that guards each.
6. Restate the M×N → M+N argument with your memory server as the concrete example. Who are
   the M and the N?
7. The schema/description "is the API." How is that claim *stronger* here than in Project 06?
8. What did wrapping P05 (rather than building memory again) teach you about the difference
   between a *capability* and an *interface to a capability*?

---

## Project Milestones

Build in order; each is runnable/inspectable before the next.

- **M1 — Tool schemas + the search handler.** Define the `inputSchema` for `memory_search`
  and `memory_save` (types, `required`, bounds, enums for `kind`), and implement
  `handle_search` wrapping the provided backend. *Validation:* offline test calls
  `handle_search` and gets ranked entries; a malformed arg is rejected.
- **M2 — The save handler + the trust boundary.** Implement `handle_save` and the
  `security.py` validators (clamp `k`, cap text length, range-check `importance`, whitelist
  `kind`). *Validation:* offline tests for valid + hostile inputs; save then search
  round-trips.
- **M3 — Resources.** Implement `list_resources` and `read_resource` exposing entries as
  `memory://entries/{id}`, with URI containment (scheme + id allow-list). *Validation:*
  offline test lists saved entries and reads one by URI; a traversal/foreign-scheme URI is
  rejected.
- **M4 — A reusable prompt.** Implement `get_prompt("reflect_on", {topic})` returning a
  parameterized message that injects recalled memories about the topic. *Validation:* offline
  test returns a message containing the topic and the recalled entries.
- **M5 — Two consumers (definition of done).** Run the provided stdio smoke-test client
  against `server.py` (consumer #1); then connect a second host — Claude Desktop or the MCP
  Inspector — using the documented config (consumer #2). *Validation:* the same server's
  tools/resources/prompt work from both; save in one, read in the other.
- **M6 — Break it.** Corrupt the stream with a stdout `print`; remove a schema bound and send
  a hostile input; expose memory `save` with no validation; classify a read-only entry as a
  tool. Record each in `FAILURE_ANALYSIS.md`.

---

## Self-Evaluation Criteria

The learner's implementation should:

- [ ] Keep the learner modules (`memory_tools`, `memory_resources`, `prompts`, `security`)
      **SDK-agnostic** (no `mcp` import) so they're pure and offline-testable.
- [ ] Define **JSON input schemas** with `required`, bounds, and an enum for `kind` — and
      validate again in the handler (the schema is advisory).
- [ ] Choose the **right primitive** for each capability: search/save = **tools**, entries =
      **resources**, reflect-on = **prompt**; and justify each by control model.
- [ ] **Contain** the resource URI namespace (scheme + known-id allow-list); reject
      traversal/foreign schemes; fail closed.
- [ ] **Bound** every input (`k`, text length, importance range, `kind` whitelist).
- [ ] Log only to **stderr** in the stdio server; never `print` to stdout.
- [ ] Demonstrate **two consumers** of the one server (stdio client + a second host) — the
      M+N proof.
- [ ] Articulate, in `UNDERSTANDING.md`, that MCP is an **interface protocol** and where the
      agent loop now lives.

---

## Instructor Notes

**Common misconceptions to probe:**

- *"The server should plan / loop / call the model."* No — that's the host. Diagnostic: "If
  Claude Desktop is the host, who runs the loop — your server or Claude Desktop?" (Answer:
  the host.) A learner who puts the loop in the server has missed the entire point.
- *"Everything is a tool."* Push on the control models: a read-only note is a **resource**
  (app reads it), not a tool (model invokes it). Ask them to classify three capabilities.
- *"The schema is just documentation."* It's the contract the model uses to call you *and*
  the first line of input validation — but it's advisory, so the handler must validate too.
- *"In-process habits transfer."* They don't: across the boundary the caller is untrusted.
  Diagnostic: "Where does the `query` string come from, and do you trust it?" (From a model
  in someone else's host — no.)

**Signs of genuine understanding:**

- The learner can state the provider/consumer split without prompting and point to *where*
  in their code the boundary is.
- They chose tool/resource/prompt deliberately and can defend each by control model.
- Their `security.py` treats inputs as adversarial (bounds + containment + fail-closed), and
  they can explain the stdout-corruption bug from the transport, not from memory.
- In the StarcallOS reflection they identify MCP as the way to expose StarcallOS's own
  capabilities once and consume external ones without bespoke glue — and name a concrete
  capability to expose first.

**Diagnostic questions:**

1. "Draw the boxes: host, client, server, model, your memory store. Where does each MCP
   method (`initialize`, `tools/list`, `tools/call`, `resources/read`) flow?"
2. "You need this capability on another machine tomorrow. What changes in your code?"
   (Ideally: one line — the transport.)
3. "A connected host's model calls `memory_save` with 5 MB of text. What happens, and which
   file stops it?"
