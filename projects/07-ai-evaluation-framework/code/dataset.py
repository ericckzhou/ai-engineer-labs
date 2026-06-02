"""dataset.py — [provided] The eval dataset: test cases, frozen.

A test case is (id, question, optional reference). The dataset must be FROZEN between a baseline and
a candidate run — comparing runs over different cases measures nothing. Provided: a TestCase model,
a JSONL loader, and a tiny inline sample so the harness runs out of the box.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TestCase:
    id: str
    question: str
    reference: str | None = None


_SAMPLE = [
    TestCase("c1", "What is the capital of France?", reference="Paris"),
    TestCase("c2", "Summarize what an LLM-as-a-judge does in one sentence."),
    TestCase("c3", "Explain why a list of raw scores is not an evaluation."),
    TestCase("c4", "What is 17 * 23?", reference="391"),
]


def load_sample_cases() -> list[TestCase]:
    """Return the built-in sample dataset (no file needed)."""
    return list(_SAMPLE)


def load_jsonl(path: str | Path) -> list[TestCase]:
    """Load test cases from a JSONL file, one object per line: {"id", "question", "reference"?}."""
    cases: list[TestCase] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        obj = json.loads(line)
        cases.append(TestCase(obj["id"], obj["question"], obj.get("reference")))
    return cases
