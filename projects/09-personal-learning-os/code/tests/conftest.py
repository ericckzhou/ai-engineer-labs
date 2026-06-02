"""[provided] Test fixtures for Project 09.

Makes code/ importable from tests/, and provides fakes so the orchestrator can be tested fully
OFFLINE — no provider, no network. A fake `chat` stands in for the model; recording fake workers
stand in for the subsystem kernel so `LearningOS.handle` is tested as pure routing + dispatch logic.

Tests build up in milestone order: M1 (router) → M2 (graph) → M3 (orchestrator, uses the router) →
M4 (evaluate_routing). The learner cores raise NotImplementedError until implemented, then pass.
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from subsystems import SubsystemResult  # noqa: E402  (after sys.path insert)


def fake_chat(reply: str = "(fake answer)"):
    """Return a `chat(messages) -> str` that ignores its input and returns a fixed reply."""
    def chat(messages: list) -> str:
        return reply
    return chat


class RecordingWorker:
    """A fake subsystem worker: records every query it's called with and returns a fixed result."""
    def __init__(self, result: SubsystemResult):
        self.result = result
        self.calls: list[str] = []

    def __call__(self, query: str) -> SubsystemResult:
        self.calls.append(query)
        return self.result


@pytest.fixture
def fake_subsystems():
    """A dispatch table of recording fake workers — one per route, each with distinct provenance."""
    return {
        "SAVE": RecordingWorker(SubsystemResult("saved", [101])),
        "RECALL": RecordingWorker(SubsystemResult("recalled", [101, 102])),
        "TASK": RecordingWorker(SubsystemResult("synthesized", [101])),
        "CHAT": RecordingWorker(SubsystemResult("chatted", [])),
    }
