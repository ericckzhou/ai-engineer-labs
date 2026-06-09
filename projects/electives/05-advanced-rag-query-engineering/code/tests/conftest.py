"""[provided] Test fixtures for the Advanced RAG elective. Offline; no provider/network.

On the STARTER, tests exercising the learner cores fail with NotImplementedError. They go green
as you implement the transforms (query_transforms.py) and the fusion (advanced_rag.answer).
test_config.py passes today.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from config import load_config

PARAPHRASE = "how do I get my money back?"
FACTUAL = "what year was the company founded?"
MULTIHOP = "Did any founder attend the same school as our chief technology officer?"


@pytest.fixture
def cfg():
    return load_config()
