"""cache.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (NotImplementedError) on main."""
from __future__ import annotations

from config import Config, load_config
from feature_backend import cosine, embed


class SemanticCache:
    def __init__(self) -> None:
        self._entries: list[tuple[dict, str, str]] = []

    def lookup(self, query: str, *, cfg: Config | None = None) -> str | None:
        cfg = cfg or load_config()
        if not self._entries:
            return None
        qv = embed(query)
        best_ans, best_sim = None, -1.0
        for ev, _q, ans in self._entries:
            s = cosine(qv, ev)
            if s > best_sim:
                best_sim, best_ans = s, ans
        return best_ans if best_sim >= cfg.cache_threshold else None

    def store(self, query: str, answer: str, *, cfg: Config | None = None) -> None:
        self._entries.append((embed(query), query, answer))
