"""cache.py — [learner] The semantic cache. This is a learning target (M2).

Return a stored answer when a *semantically similar* query was seen before — without calling a
model. Reuse the provided embedder + cosine (feature_backend); the decision you own is the
THRESHOLD GATE: a hit only when the nearest stored query's similarity >= cfg.cache_threshold.

The failure mode to understand (and demonstrate in FAILURE_ANALYSIS): a too-loose threshold
returns a stored answer for a DIFFERENT question (the false hit). See lesson §5,
sources/official-docs/gptcache-semantic-caching.md.
"""
from __future__ import annotations

from config import Config, load_config
from feature_backend import cosine, embed


class SemanticCache:
    def __init__(self) -> None:
        # Each entry: (embedding, query, answer). (A list is fine at this scale; a real cache
        # uses an ANN index — Project 03 — and an eviction policy.)
        self._entries: list[tuple[dict, str, str]] = []

    def lookup(self, query: str, *, cfg: Config | None = None) -> str | None:
        """Return the cached answer if a stored query is similar enough, else None.

        Steps:
          1. embed(query)
          2. find the stored entry with the highest cosine to it
          3. if that similarity >= cfg.cache_threshold → return its answer (a HIT), else None.

        Examples (with default cfg.cache_threshold = 0.90):
            store("what is the capital of france", "Paris"); lookup("what is the capital of france")
                -> "Paris"               # cosine 1.0
            lookup("what is the capital of france please") -> "Paris"   # near-duplicate, ~0.93
            lookup("who wrote pride and prejudice") -> None             # unrelated
            lookup("what is the capital of austria") -> None            # ~0.83 < 0.90 (correct miss)
        """
        cfg = cfg or load_config()
        raise NotImplementedError("M2: implement lookup — embed, find nearest, gate on cfg.cache_threshold.")

    def store(self, query: str, answer: str, *, cfg: Config | None = None) -> None:
        """Add (embedding, query, answer) to the cache."""
        cfg = cfg or load_config()
        raise NotImplementedError("M2: implement store — append (embed(query), query, answer).")
