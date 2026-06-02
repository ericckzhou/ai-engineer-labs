"""[provided] Test fixtures for Project 06.

Makes code/ importable from tests/, and builds a tiny throwaway repo on disk so the file tools
(safe_resolve, dispatch_tool) and the loop can be tested fully OFFLINE — no provider, no network.
The learner cores tested here are pure control-flow + filesystem logic.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def fixture_repo(tmp_path):
    """A minimal repo: config.py + src/util.py + README.md. Returns the repo root path (str)."""
    (tmp_path / "config.py").write_text(
        'DEFAULT_MODEL = "groq/llama-3.3-70b-versatile"\n', encoding="utf-8")
    src = tmp_path / "src"
    src.mkdir()
    (src / "util.py").write_text("def add(a, b):\n    return a + b\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo repo\n", encoding="utf-8")
    return str(tmp_path)
