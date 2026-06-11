import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest  # noqa: E402

import fake_backend  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_backend():
    """The fake backend tracks per-case attempt counts; reset around every test for determinism."""
    fake_backend.reset()
    yield
    fake_backend.reset()
