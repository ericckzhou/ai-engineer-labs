"""[provided] Test fixtures for the Observability & Ops elective. Offline; no provider/network.

On the STARTER, tests exercising the learner cores fail with NotImplementedError. They go green
as you implement build_span/traced (tracing.py) and aggregate/detect_drift (monitor.py).
test_config.py passes today.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from config import load_config
from exporter import load_spans

FIX = Path(__file__).resolve().parent.parent / "fixtures"


@pytest.fixture
def cfg():
    return load_config()


@pytest.fixture
def baseline_spans() -> list[dict]:
    return load_spans(FIX / "baseline.jsonl")


@pytest.fixture
def window_spans() -> list[dict]:
    return load_spans(FIX / "window_regressed.jsonl")
