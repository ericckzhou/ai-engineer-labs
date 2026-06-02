# Elective 01: MCP Interface Layer — Code

Wrap **Project 05's memory system** as an **MCP server** and consume it from **two hosts**.
The memory backend (the thing being wrapped) and the transport/SDK wiring are **provided** —
the learning target is the **protocol surface**: tool schemas + handlers, resources, a prompt,
and the trust-boundary checks. There is **no agent loop here** — the loop lives in the host.

## Setup

```bash
# From this directory
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt   # mcp, litellm, python-dotenv, pytest

# .env is OPTIONAL — the backend runs offline with a deterministic local embedder.
# cp .env.example .env   # only if you want real embeddings or a live host model
```

## Test (one command)

```bash
python -m pytest          # all guiding tests are OFFLINE (no network, no provider, no SDK)
```

Tests fail with `NotImplementedError` (or a schema assertion) until you implement the learner
cores, then pass. Build in milestone order and re-run after each:

```bash
python -m pytest tests/test_security.py    # M1–M3 the trust boundary
python -m pytest tests/test_tools.py       # M1–M2 schemas + search/save handlers
python -m pytest tests/test_resources.py   # M3 resources
python -m pytest tests/test_prompts.py     # M4 the reusable prompt
```

> `client_smoke_test.py` is **not** collected by pytest (see `pytest.ini`) — it imports the
> `mcp` SDK and is the live end-to-end path, not an offline unit test.

## Run — the two consumers (the Definition of Done)

The whole point is **one server, many hosts**. Demonstrate both:

### Consumer #1 — the programmatic stdio client (provided)

```bash
python client_smoke_test.py
```

It launches `server.py`, runs `initialize` (capability negotiation), discovers the surface,
then saves, searches, reads a resource, and gets the prompt. Watch **stderr** for server logs.

### Consumer #2 — a second host (Claude Desktop or the MCP Inspector)

**MCP Inspector (no GUI host needed):**

```bash
npx @modelcontextprotocol/inspector python server.py
```

**Claude Desktop** — add to `claude_desktop_config.json`
(Windows: `%AppData%\Claude\claude_desktop_config.json`), then fully restart the app:

```jsonc
{
  "mcpServers": {
    "personal-memory": {
      "command": "python",
      "args": ["C:\\ABSOLUTE\\PATH\\TO\\code\\server.py"]
    }
  }
}
```

Prove the decoupling: **save** a note via one consumer, then **read it as a resource** via the
other. Same server, no shared code.

## Provider (swappable by key — optional here)

`config.py` carries the canonical provider block (Groq free tier preferred; Ollama for free
local; explicit `LLM_MODEL` wins). The memory backend runs **offline by default**, so you only
need a provider for the *extension* (real embeddings) or to point a host's model at the server.

## Build Milestones (the learner core)

| Milestone | File · symbol | What it does |
|-----------|---------------|--------------|
| M1 | `memory_tools.py` · `TOOL_DEFINITIONS`, `handle_search` + `security.validate_search_args` | The tool **schemas** (the contract the model sees) and the search handler |
| M2 | `memory_tools.py` · `handle_save` + `security.validate_save_args` | The save handler + the input **bounds** (trust boundary) |
| M3 | `memory_resources.py` + `security.validate_resource_uri` | Expose entries as `memory://entries/{id}` **resources**, with URI containment |
| M4 | `prompts.py` · `PROMPT_DEFINITIONS`, `get_prompt` | One reusable **prompt** that injects recalled memories |
| M5 | `client_smoke_test.py` + a second host (provided/config) | **Two consumers** of the one server — the M+N proof |
| M6 | — | Break it: stdout corruption, removed bound + hostile input, unvalidated save, wrong primitive |

## File Roles

Labeled per `OPERATING_RULES.md` §Scaffolding — `provided` (complete) · `learner` (you write
the core) · `reference` (complete, given because it's not the target):

| File | Role | You... |
|------|------|--------|
| `config.py` | `provided` | read the bounds from `Config`; don't edit the canonical provider block |
| `memory_backend.py` | `reference` | reuse — the Project 05 memory store being wrapped (complete) |
| `security.py` | `learner` | implement the three validators (M1–M3) — the trust boundary |
| `memory_tools.py` | `learner` | implement `TOOL_DEFINITIONS` + `handle_search`/`handle_save` (M1–M2) |
| `memory_resources.py` | `learner` | implement `list_resources` + `read_resource` (M3) |
| `prompts.py` | `learner` | implement `PROMPT_DEFINITIONS` + `get_prompt` (M4) |
| `server.py` | `provided` | run it — the FastMCP/stdio adapter over your modules (no loop here) |
| `client_smoke_test.py` | `provided` | run it — consumer #1 |
| `tests/` | `provided` | make these pass (offline) |
| `pytest.ini`, `requirements.txt`, `.env.example` | `provided` | setup |

Search `security.py`, `memory_tools.py`, `memory_resources.py`, and `prompts.py` for
`NotImplementedError` and `TODO(learner)` to find your work.

## Notes

- Fill in `../UNDERSTANDING.md` before writing any code here.
- Keep the learner modules **SDK-agnostic** (no `import mcp`) — only `server.py` /
  `client_smoke_test.py` import the SDK. That separation *is* the data-layer/transport split.
- On stdio, **never `print` to stdout** — it corrupts the JSON-RPC stream. Log to stderr.
- Record your M6 ablations (stdout corruption, trust-boundary breach, unvalidated save,
  wrong-primitive classification) in `../FAILURE_ANALYSIS.md`, and the two-consumer
  demonstration in `../EVALUATION.md`.
