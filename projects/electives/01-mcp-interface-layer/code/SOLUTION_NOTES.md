# Elective 01 (MCP Interface Layer) — Reference Solution Notes (solns branch only)

> Exists only on `solns`. **Do not merge to `main`** — leaks answers.

## Implemented (learner surface)

| File | Function(s) | Milestone |
|---|---|---|
| `security.py` | `validate_search_args`, `validate_save_args`, `validate_resource_uri` | M1–M3 |
| `memory_tools.py` | `TOOL_DEFINITIONS` + `handle_search`, `handle_save` | M1/M2 |
| `memory_resources.py` | `list_resources`, `read_resource` | M3 |
| `prompts.py` | `PROMPT_DEFINITIONS` + `get_prompt` (reflect_on) | M4 |

`server.py` (MCP SDK adapter), `memory_backend.py`, `config.py` are `[provided]` — not touched.

## Offline gate — PASS

```
$ .venv/Scripts/python.exe -m pytest -q
26 passed   (0 skipped)
```
All offline (SDK-agnostic learner modules + deterministic reference backend; no `mcp`
transport, no provider). Trust-boundary checks fail closed: empty query, foreign scheme,
`../` traversal, over-long text, bad kind/importance all raise `SecurityError`.

## Live smoke (MCP transport) — PENDING

```
$ .venv/Scripts/python.exe server.py    # starts the MCP server over stdio; connect a host
```
