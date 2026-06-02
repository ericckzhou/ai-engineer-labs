"""[provided] Guiding tests for the TOOL layer (memory_tools.py). OFFLINE. M1–M2.

Schema tests fail by assertion until you fill TOOL_DEFINITIONS; handler tests fail with
NotImplementedError until you implement them. The schema you write IS the contract the model
sees — these tests pin its required shape, not its wording.
"""
import pytest

import memory_tools
from memory_tools import TOOL_DEFINITIONS, handle_save, handle_search


# ---- M1: schemas (the contract the model sees) -----------------------------------
def test_tool_definitions_present_and_shaped():
    names = {d["name"] for d in TOOL_DEFINITIONS}
    assert {"memory_search", "memory_save"} <= names
    for d in TOOL_DEFINITIONS:
        assert isinstance(d.get("description"), str) and d["description"]
        schema = d["inputSchema"]
        assert schema["type"] == "object"
        assert "properties" in schema


def test_search_schema_requires_query():
    search = next(d for d in TOOL_DEFINITIONS if d["name"] == "memory_search")
    assert "query" in search["inputSchema"]["properties"]
    assert "query" in search["inputSchema"].get("required", [])


def test_save_schema_has_kind_enum():
    save = next(d for d in TOOL_DEFINITIONS if d["name"] == "memory_save")
    kind = save["inputSchema"]["properties"]["kind"]
    assert set(kind["enum"]) == {"episodic", "semantic", "procedural"}


# ---- M1/M2: handlers -------------------------------------------------------------
def test_handle_search(populated_backend):
    # 'demo' appears only in m0.
    out = handle_search({"query": "demo"}, populated_backend)
    assert out["text"] == "[m0] (episodic) the StarcallOS demo is on June 20"


def test_handle_search_no_hits(populated_backend):
    assert handle_search({"query": "kangaroo"}, populated_backend)["text"] == "No matching memories."


def test_handle_save_then_search(fresh_backend):
    saved = handle_save({"text": "the demo is on June 20"}, fresh_backend)
    assert saved["text"] == "Saved m0."
    found = handle_search({"query": "demo"}, fresh_backend)
    assert "m0" in found["text"]


def test_dispatch_routes_to_handler(fresh_backend):
    # dispatch is provided plumbing; it should route a known name to the handler.
    memory_tools.dispatch("memory_save", {"text": "hello world"}, fresh_backend)
    with pytest.raises(KeyError):
        memory_tools.dispatch("no_such_tool", {}, fresh_backend)
