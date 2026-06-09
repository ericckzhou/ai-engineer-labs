"""[provided] Test fixtures for the Cost & Latency elective. Offline; no provider/network.

On the STARTER, tests that exercise the learner cores fail with NotImplementedError. They go
green as you implement cache → cascade → budget. test_config.py passes today (drift guard).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from config import load_config


@pytest.fixture
def cfg():
    return load_config()
