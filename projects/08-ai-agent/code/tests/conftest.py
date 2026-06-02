"""[provided] Test fixtures for Project 08.

Makes code/ importable from tests/, and builds a tiny throwaway repo on disk so the provided tool
layer (read/list/search) and the loop can be tested fully OFFLINE — no provider, no network. The
learner cores tested here are pure control-flow + accounting logic; a scripted fake `complete`
stands in for the model.
"""
import sys
from pathlib import Path
from types import SimpleNamespace

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


def make_tool_call(call_id, name, arguments):
    """Build a fake OpenAI-style tool_call (arguments is a JSON *string*, as LiteLLM returns)."""
    return SimpleNamespace(id=call_id, function=SimpleNamespace(name=name, arguments=arguments))


def scripted_completer(turns):
    """Return a `complete(messages, tools)` that yields each message in `turns`, in order.

    Records every `messages` list it was called with on `complete.seen` so a test can assert the
    tool results were fed back. After the script is exhausted it keeps returning the last turn.
    """
    it = iter(turns)
    last = {"msg": None}

    def complete(messages, tools):
        complete.seen.append(list(messages))
        try:
            last["msg"] = next(it)
        except StopIteration:
            pass
        return last["msg"]

    complete.seen = []
    return complete
