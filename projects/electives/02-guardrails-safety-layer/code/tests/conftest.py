"""[provided] Test fixtures for the Guardrails & Safety Layer elective.

Makes code/ importable from tests/. Every guiding test here is OFFLINE: it imports only the
learner module (guards), the composition (guarded_agent), the reference agent backend, and
config — no provider and no network. The agent backend is deterministic, so tests are stable.

On the STARTER, tests that exercise the learner cores fail with NotImplementedError — that is
the guiding signal. They go green as you implement scan_input → redact_output → enforce_policy.
test_config.py passes today (it is a drift guard, not a learner target).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from config import load_config

DATASET = Path(__file__).resolve().parent.parent / "datasets" / "attacks.jsonl"


@pytest.fixture
def cfg():
    return load_config()


@pytest.fixture
def rows() -> list[dict]:
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]
