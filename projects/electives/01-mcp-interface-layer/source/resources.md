# Resources & Sources — Elective 01: MCP Interface Layer

> All sources used for this lesson, organized by tier.
> Every claim in lesson.agent.md traces back to one of these.
> This elective teaches an **interface protocol**. The two new MCP sources are the
> authority for the protocol's concepts and the Python server mechanics; the carried-over
> sources connect MCP back to the hand-wired tool use of the spine (Projects 06/08).

---

## Tier 1: Official Documentation / Engineering Guidance

> Primary sources. Check these first.

- **Model Context Protocol — Architecture** — `sources/official-docs/mcp-architecture.md`
  - URL: https://modelcontextprotocol.io/specification/2025-06-18/architecture
    (companion overview: https://modelcontextprotocol.io/docs/learn/architecture)
  - What to read: the **client-host-server** architecture (one client per server, the host
    aggregates context and enforces consent/security); **JSON-RPC** + stateful sessions with
    **capability negotiation**; the two **layers** (data vs transport); the two **transports**
    (stdio = local/single-client; Streamable HTTP = remote/multi-client + auth); and the three
    **server primitives** — tools, resources, prompts — with their control models. The
    conceptual spine of the whole elective and the basis for "MCP is a protocol, not an agent
    framework."

- **Model Context Protocol — Build an MCP Server** — `sources/official-docs/mcp-build-server.md`
  - URL: https://modelcontextprotocol.io/docs/develop/build-server
    (companion: https://modelcontextprotocol.io/docs/develop/build-client)
  - What to read: building a server in Python with the `mcp` SDK / **FastMCP** (type hints +
    docstrings → tool definition); registering tools, resources, prompts; running over
    **stdio** (`mcp.run(transport="stdio")`); the **stdout-corruption** hazard (log to
    stderr); and configuring a host (Claude Desktop `mcpServers`) — the practical scaffolding
    that the project provides and the learner fills in. Treat as implementation scaffolding;
    the architecture/spec page is the conceptual authority.

- **Anthropic — Tool Use (Function Calling) Overview** — `sources/official-docs/anthropic-tool-use.md`
  - URL: https://platform.claude.com/docs/en/docs/build-with-claude/tool-use/overview
  - What to read: the **hand-wired** tool loop (tool = name + description + JSON-schema input;
    `tool_use` → execute → `tool_result`) that this elective **generalizes** into a protocol.
    MCP is the portable, cross-host version of exactly this. (Carried from Projects 06/08.)

- **Anthropic — Building Effective Agents** — `sources/articles/building-effective-agents.md`
  - URL: https://www.anthropic.com/engineering/building-effective-agents
  - What to read: the **augmented LLM** (retrieval + tools + memory) and the **agent-computer
    interface** ("invest just as much effort in good agent-computer interfaces"; "the
    description is the API"). MCP makes the ACI **portable** — the same schema/description
    discipline, now the contract every host's model sees. (Carried from Project 06.)

---

## Tier 2: Foundational Papers

> None new for this elective. MCP is a protocol/engineering standard, not a research result.
> The wrapped capability (memory) is grounded in Project 05's sources
> (`sources/papers/generative-agents.md`, `sources/papers/memory-systems-taxonomy.md`,
> `sources/papers/memgpt.md`) — carried over, not re-taught here.

---

## Tier 3: Engineering Guides

> The Anthropic engineering guidance in Tier 1 ("Building Effective Agents") doubles as the
> engineering source for the ACI/"description is the API" framing the protocol surface relies on.
> The **MCP Inspector** (https://github.com/modelcontextprotocol/inspector) and the official
> **reference servers** (https://github.com/modelcontextprotocol/servers) are practical
> references for exercising and modeling a server.

---

## Tier 4: Educational Sources

> The prior projects are the conceptual prerequisites: Project 05 built the memory system you
> wrap; Projects 06 and 08 built the hand-wired tool loops MCP generalizes. Re-read those
> lessons rather than a generic MCP tutorial.

---

## A note on the M×N → M+N framing (truth-rules disclosure)

The official docs establish that any compliant server is consumable by any compliant host and
that a host creates one client per server. The **M×N → M+N** integration argument is the
standard *engineering interpretation* of that documented property — it is presented as an
interpretation in `lesson.agent.md` and `sources/official-docs/mcp-architecture.md`, **not**
asserted as a verbatim protocol claim (per `OPERATING_RULES.md` Truth Rules 3–4). If a primary
source that states the M×N argument directly is later added, register it here and cite it.

---

## Recommended Reading Order

For a learner new to MCP (after Projects 05/06/08):

1. `sources/official-docs/mcp-architecture.md` — participants, layers, transports, primitives.
   Read before any code; it defines the whole mental model.
2. `sources/official-docs/anthropic-tool-use.md` — recall the hand-wired loop MCP generalizes.
3. `sources/official-docs/mcp-build-server.md` — the Python/FastMCP mechanics you'll fill in.
4. Reference: `sources/articles/building-effective-agents.md` — why the schema/description is
   the API, now portable.

---

## Further Reading

- The MCP **specification** (https://modelcontextprotocol.io/specification/latest) — lifecycle,
  the full primitive schemas, and the client primitives (sampling, elicitation, logging).
- **Streamable HTTP** transport + auth (OAuth/bearer) — the remote, multi-client deployment.
- The **MCP Inspector** and **reference servers** — exercise a server with no client code; model
  your design on the filesystem/database servers.
- Building an **MCP client / host** (`/docs/develop/build-client`) — the inverse role; how an
  agent (Project 08) becomes a consumer of servers.
