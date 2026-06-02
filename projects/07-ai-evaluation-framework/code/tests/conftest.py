"""[provided] Test fixtures for Project 07.

Makes code/ importable from tests/. The learner cores tested here — build_judge_prompt,
parse_judge_score, summarize, compare_runs — are pure (prompt construction, text parsing,
aggregation) and need no network or provider. The live judge call is not tested here.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
