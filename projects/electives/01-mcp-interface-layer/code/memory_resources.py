"""memory_resources.py — [learner] The RESOURCE layer (application-controlled context). Milestone M3.

Resources are the primitive the HOST/APP reads for context (`resources/list`, `resources/read`),
addressed by URI — NOT actions the model invokes. A saved memory entry is read-only context, so
it belongs here, not as a tool. Choosing this primitive (vs. a tool) is the design decision M3
tests.

Each entry is exposed at `memory://entries/{id}`. SDK-agnostic: no `mcp` import; plain dicts only.

PROVIDED: nothing to fill beyond the two functions; security.validate_resource_uri does the
containment.
LEARNER: list_resources + read_resource (M3).

Run:  python -m pytest tests/test_resources.py
"""
from __future__ import annotations

from config import load_config
from security import SecurityError, validate_resource_uri

cfg = load_config()


def _uri_for(entry_id: str) -> str:
    """[provided] Build the canonical resource URI for an entry id."""
    return f"{cfg.resource_scheme}://entries/{entry_id}"


def list_resources(backend) -> list[dict]:
    """[learner] List every stored entry as a resource descriptor. (M3)

    Steps:
      1. For each entry in backend.all_entries(), build a descriptor dict:
           {"uri": _uri_for(m.id), "name": <short label, e.g. f"Memory {m.id}">,
            "description": <e.g. the entry's kind>, "mimeType": "text/plain"}
      2. Return the list (empty list if the store is empty — not an error).

    Example (mirrors tests/test_resources.py::test_list_resources):
      # backend has m0 (episodic), m1 (semantic)
      list_resources(backend)
        -> [{"uri": "memory://entries/m0", "name": "Memory m0", ... "mimeType": "text/plain"},
            {"uri": "memory://entries/m1", "name": "Memory m1", ... "mimeType": "text/plain"}]
    """
    return [
        {
            "uri": _uri_for(m.id),
            "name": f"Memory {m.id}",
            "description": m.kind,
            "mimeType": "text/plain",
        }
        for m in backend.all_entries()
    ]


def read_resource(uri: str, backend) -> dict:
    """[learner] Read one entry by its URI → {"text": <entry text>}. (M3)

    Steps:
      1. Parse + CONTAIN the uri with security.validate_resource_uri(uri) → entry_id. Let
         SecurityError propagate (a bad/foreign/traversal URI must fail closed, not 404 quietly).
      2. Look the entry up with backend.get(entry_id). If it does not exist, raise SecurityError
         (or KeyError) — do not return another entry.
      3. Return {"uri": uri, "text": entry.text, "mimeType": "text/plain"}.

    Example (mirrors tests/test_resources.py::test_read_resource):
      read_resource("memory://entries/m0", backend) -> {"uri": "memory://entries/m0",
                                                        "text": "the demo is on June 20", ...}
      read_resource("file:///etc/passwd", backend)  -> raises SecurityError
    """
    entry_id = validate_resource_uri(uri)
    entry = backend.get(entry_id)
    if entry is None:
        raise SecurityError(f"no such entry: {entry_id}")
    return {"uri": uri, "text": entry.text, "mimeType": "text/plain"}
