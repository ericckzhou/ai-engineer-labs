"""context_selector.py — [provided] Context injection: retrieve the top-k relevant files.

This is Project 02 (cosine similarity) + Project 03/04 (retrieval) applied to source files —
PROVIDED so this lesson spends the learner's effort on the genuinely new thing (the tool loop). It
embeds the question and each file, ranks by cosine similarity, and returns the top-k as starting
context for the prompt. Needs an embeddings provider (config.py). NOT the learning target.

Used by copilot.py. If the embeddings provider is unavailable, copilot.py falls back to tools only.
"""
from __future__ import annotations

import math
from pathlib import Path

import litellm

from config import load_config

_SKIP = {".git", "__pycache__", ".venv", "node_modules"}
_EXT = {".py", ".md", ".txt", ".js", ".ts", ".json", ".toml", ".cfg", ".yaml", ".yml"}


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def _embed(texts: list[str], model: str) -> list[list[float]]:
    resp = litellm.embedding(model=model, input=texts)
    return [d["embedding"] for d in resp["data"]]


def select_context(repo_root, query: str, k: int = 4) -> list[tuple[str, str]]:
    """Return up to k (relative_path, file_text) pairs most relevant to `query`.

    Embeds the query and each text file with the SAME model (config.embedding_model — the
    same-model rule carried from Projects 02–04), ranks by cosine similarity, and returns the top-k.
    """
    cfg = load_config()
    base = Path(repo_root).resolve()
    files = [p for p in sorted(base.rglob("*"))
             if p.is_file() and p.suffix in _EXT
             and not any(part in _SKIP for part in p.parts)]
    kept: list[Path] = []
    texts: list[str] = []
    for p in files:
        try:
            texts.append(p.read_text(encoding="utf-8", errors="strict")[:4000])
            kept.append(p)
        except (UnicodeDecodeError, OSError):
            continue
    if not kept:
        return []
    q_emb = _embed([query], cfg.embedding_model)[0]
    f_embs = _embed(texts, cfg.embedding_model)
    scored = sorted(
        zip(kept, texts, (_cosine(q_emb, e) for e in f_embs)),
        key=lambda t: t[2], reverse=True,
    )
    return [(str(p.relative_to(base)), text) for p, text, _ in scored[:k]]
