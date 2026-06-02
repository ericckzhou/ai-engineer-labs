"""[provided] Guiding tests for the PROMPT layer (prompts.py). OFFLINE. M4.

Fail with NotImplementedError until implemented. They assert the reusable prompt injects the
recalled memories for the requested topic, and that an unknown prompt name is rejected.
"""
import pytest

from prompts import PROMPT_DEFINITIONS, get_prompt


def test_prompt_definitions_present():
    names = {d["name"] for d in PROMPT_DEFINITIONS}
    assert "reflect_on" in names
    reflect = next(d for d in PROMPT_DEFINITIONS if d["name"] == "reflect_on")
    arg_names = {a["name"] for a in reflect.get("arguments", [])}
    assert "topic" in arg_names


def test_reflect_on_injects_memories(populated_backend):
    out = get_prompt("reflect_on", {"topic": "StarcallOS"}, populated_backend)
    assert out.get("description")
    text = out["text"]
    assert "StarcallOS" in text          # the topic
    assert "June 20" in text             # the recalled memory m0


def test_get_prompt_unknown_name(populated_backend):
    with pytest.raises((KeyError, ValueError)):
        get_prompt("no_such_prompt", {"topic": "x"}, populated_backend)
