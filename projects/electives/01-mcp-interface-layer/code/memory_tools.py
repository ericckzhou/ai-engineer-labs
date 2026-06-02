"""memory_tools.py — [learner] The TOOL layer (model-controlled actions). Milestones M1–M2.

Tools are the primitive a host's MODEL invokes to perform an action (`tools/call`). Here:
`memory_search` and `memory_save`, each wrapping the provided backend. This module is
SDK-AGNOSTIC on purpose — it imports NO `mcp`. It deals in plain dicts; server.py adapts those
into MCP content. Keeping it SDK-free is what makes the surface testable offline and the
data-layer / transport split real.

Recall Project 06: "the description is the API." The JSON inputSchema + description below are
the contract every connected host's model sees when deciding whether and how to call you. Make
them precise (types, `required`, bounds, an `enum` for `kind`). The schema is ADVISORY though —
security.py enforces.

PROVIDED: the dispatch table; the SDK adapter lives in server.py.
LEARNER: TOOL_DEFINITIONS (the JSON schemas) and the two handlers.

Run:  python -m pytest tests/test_tools.py
"""
from __future__ import annotations

from security import validate_save_args, validate_search_args

# [learner] M1 — the tool contracts the model sees. Fill this list with one dict per tool:
#   {"name": str, "description": str, "inputSchema": {<JSON Schema>}}
# Requirements:
#   - memory_search: property "query" (string, required); "k" (integer, optional, with a
#     sensible minimum/maximum mirroring config bounds).
#   - memory_save: property "text" (string, required); "kind" (string, enum of the three
#     memory kinds, optional); "importance" (number, optional, with min/max).
# The description is the part the model reads to decide WHEN to use the tool — write it well.
TOOL_DEFINITIONS: list[dict] = []  # TODO(learner): define memory_search + memory_save schemas


def handle_search(args: dict, backend) -> dict:
    """[learner] Execute memory_search → {"text": <ranked entries>}. (M1)

    Steps:
      1. Validate/clamp args with security.validate_search_args → (query, k). Let SecurityError
         propagate (server.py turns it into an error result).
      2. Call backend.search(query, k=k) → list[Memory], already ranked.
      3. Format each hit as a line "[<id>] (<kind>) <text>"; join with newlines.
      4. If there are no hits, return {"text": "No matching memories."}.
      5. Return {"text": <the joined lines>}.

    Example (mirrors tests/test_tools.py::test_handle_search):
      # backend has m0 "the demo is on June 20", m1 "I prefer dark mode"
      handle_search({"query": "demo"}, backend)
        -> {"text": "[m0] (episodic) the demo is on June 20"}     # only the overlap matches
      handle_search({"query": "kangaroo"}, backend)
        -> {"text": "No matching memories."}
    """
    raise NotImplementedError("M1: validate, search, and format the results")


def handle_save(args: dict, backend) -> dict:
    """[learner] Execute memory_save → {"text": "Saved <id>."}. (M2)

    Steps:
      1. Validate/bound args with security.validate_save_args → (text, kind, importance).
      2. Call backend.save(text, kind=kind, importance=importance) → Memory.
      3. Return {"text": f"Saved {mem.id}."} (a short confirmation the model can relay).

    Example (mirrors tests/test_tools.py::test_handle_save_then_search):
      handle_save({"text": "the demo is on June 20"}, backend)  -> {"text": "Saved m0."}
      # afterwards handle_search({"query": "demo"}, backend) finds it.
    """
    raise NotImplementedError("M2: validate and save the entry")


# [provided] Plumbing — name → handler. server.py registers MCP tools that route here.
_HANDLERS = {
    "memory_search": handle_search,
    "memory_save": handle_save,
}


def dispatch(name: str, args: dict, backend) -> dict:
    """[provided] Route a tool call to its handler. Raises KeyError on an unknown tool name."""
    if name not in _HANDLERS:
        raise KeyError(f"unknown tool: {name!r}")
    return _HANDLERS[name](args, backend)
