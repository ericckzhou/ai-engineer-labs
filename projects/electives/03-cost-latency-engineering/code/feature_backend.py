"""feature_backend.py — [reference] The feature + models being optimized. Provided whole.

OFFLINE and deterministic so the whole elective is gradeable with no provider:
  - a CHEAP model (right on easy queries, wrong + low-confidence on hard ones),
  - a STRONG model (the expensive ground truth — right on everything it knows),
  - a local EMBEDDER + cosine for the semantic cache (Project 02/03, deterministic).

The caching and routing are NOT here — that's the learner's job (cache.py, cascade.py).
"""
from __future__ import annotations

import math
import re

_WORD = re.compile(r"[a-z0-9]+")


def _norm(text: str) -> str:
    return " ".join(_WORD.findall(text.lower()))


# The "world" the models know. eval_set.jsonl is authored to match strong_answer() exactly.
# difficulty: "easy" → cheap model gets it right; "hard" → cheap model returns cheap_wrong.
_WORLD: dict[str, dict] = {
    "what is the capital of france": {"answer": "Paris", "difficulty": "easy"},
    "what is the capital of france please": {"answer": "Paris", "difficulty": "easy"},
    "what is 2 2": {"answer": "4", "difficulty": "easy"},
    "what is the boiling point of water in celsius": {"answer": "100", "difficulty": "easy"},
    "who wrote pride and prejudice": {"answer": "Jane Austen", "difficulty": "easy"},
    "what color is the sky on a clear day": {"answer": "blue", "difficulty": "easy"},
    "what is the capital of austria": {"answer": "Vienna", "difficulty": "easy"},
    "explain the halting problem": {
        "answer": "Whether an arbitrary program halts is undecidable.",
        "difficulty": "hard", "cheap_wrong": "Every program eventually halts."},
    "what is the status of the riemann hypothesis": {
        "answer": "It is an unsolved conjecture.",
        "difficulty": "hard", "cheap_wrong": "It was proven in 1998."},
    "summarize the theory of relativity": {
        "answer": "Spacetime is relative and gravity curves spacetime.",
        "difficulty": "hard", "cheap_wrong": "Everything is relative to personal opinion."},
}


def embed(text: str) -> dict[str, int]:
    """Deterministic local embedding: a term-count vector. Same function for store and lookup."""
    v: dict[str, int] = {}
    for w in _WORD.findall(text.lower()):
        v[w] = v.get(w, 0) + 1
    return v


def cosine(a: dict[str, int], b: dict[str, int]) -> float:
    """Cosine similarity of two term-count vectors. Provided plumbing for the cache."""
    if not a or not b:
        return 0.0
    dot = sum(cnt * b.get(term, 0) for term, cnt in a.items())
    na = math.sqrt(sum(c * c for c in a.values()))
    nb = math.sqrt(sum(c * c for c in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def strong_answer(query: str) -> str:
    """The expensive, correct model."""
    item = _WORLD.get(_norm(query))
    return item["answer"] if item else "I don't know."


def cheap_answer(query: str) -> tuple[str, float]:
    """The cheap model: (answer, confidence). Right + confident on easy; wrong + unsure on hard."""
    item = _WORLD.get(_norm(query))
    if not item:
        return "I don't know.", 0.2
    if item["difficulty"] == "easy":
        return item["answer"], 0.9
    return item.get("cheap_wrong", "(uncertain)"), 0.35
