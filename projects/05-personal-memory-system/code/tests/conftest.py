"""[provided] Test fixtures for Project 05.

Makes code/ importable from tests/. The learner cores tested offline here — the four scoring functions
and retrieve() — are pure logic and need no network or provider. Memories are hand-built with fixed
embeddings and timestamps so the tests are fully deterministic.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
