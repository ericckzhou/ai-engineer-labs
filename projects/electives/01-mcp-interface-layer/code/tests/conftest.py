"""[provided] Test fixtures for the MCP Interface Layer elective.

Makes code/ importable from tests/. Every guiding test here is OFFLINE: it imports only the
SDK-agnostic learner modules (memory_tools, memory_resources, prompts, security) and the
reference backend — never server.py — so no `mcp` SDK, no network, and no provider are needed.
The backend's relevance is deterministic (exact token cosine), so the tests are stable.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from memory_backend import EPISODIC, SEMANTIC, MemoryBackend


@pytest.fixture
def fresh_backend() -> MemoryBackend:
    """An empty store."""
    return MemoryBackend()


@pytest.fixture
def populated_backend() -> MemoryBackend:
    """A store with two known entries: m0 (episodic, mentions 'demo'/'StarcallOS') and
    m1 (semantic, 'dark mode'). 'demo' and 'StarcallOS' appear only in m0; 'kangaroo' in neither."""
    backend = MemoryBackend()
    backend.save("the StarcallOS demo is on June 20", kind=EPISODIC, importance=8.0)
    backend.save("I prefer dark mode", kind=SEMANTIC, importance=6.0)
    return backend
