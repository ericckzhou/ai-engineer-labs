"""[provided] Guiding tests for the RESOURCE layer (memory_resources.py). OFFLINE. M3.

Fail with NotImplementedError until implemented. They assert that entries are listed +
readable by URI, and that a foreign/traversal URI fails closed.
"""
import pytest

from memory_resources import list_resources, read_resource
from security import SecurityError


def test_list_resources(populated_backend):
    descriptors = list_resources(populated_backend)
    uris = [d["uri"] for d in descriptors]
    assert uris == ["memory://entries/m0", "memory://entries/m1"]
    for d in descriptors:
        assert d.get("mimeType") == "text/plain"
        assert d.get("name")


def test_list_resources_empty(fresh_backend):
    assert list_resources(fresh_backend) == []


def test_read_resource(populated_backend):
    out = read_resource("memory://entries/m0", populated_backend)
    assert out["text"] == "the StarcallOS demo is on June 20"


def test_read_resource_rejects_foreign_scheme(populated_backend):
    with pytest.raises(SecurityError):
        read_resource("file:///etc/passwd", populated_backend)
