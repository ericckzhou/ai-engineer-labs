"""config.py — [provided] Settings & provider/environment loading. NOT the learning target.

CANONICAL TEMPLATE — source of truth: skills/lesson-generator/templates/config.py
The PROVIDER-RESOLUTION BLOCK below is canonical: keep it identical across every project.
The `Config` dataclass is PER-PROJECT.

For THIS elective the core runs OFFLINE (deterministic cheap/strong "models" + a local embedder).
The PRICES and THRESHOLDS in `Config` ARE used by cache.py/cascade.py/budget.py — read them from
here, do not hardcode. The prices are illustrative per-call stand-ins; the live extension wires
the real per-MTok table from sources/official-docs/anthropic-pricing.md.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()

# ---- CANONICAL: provider resolution (do not edit per project) ----------------
PROVIDER_DEFAULTS: list[tuple[str, str]] = [
    ("GROQ_API_KEY", "groq/llama-3.3-70b-versatile"),
    ("ANTHROPIC_API_KEY", "claude-sonnet-4-6"),
    ("OPENAI_API_KEY", "gpt-4o-mini"),
]
OLLAMA_CHAT_DEFAULT = "ollama/qwen3.5:4b"
OLLAMA_EMBED_DEFAULT = "ollama/nomic-embed-text"  # 768-dim


def _use_ollama() -> bool:
    return os.getenv("USE_OLLAMA", "").strip().lower() in {"1", "true", "yes", "on"}


def default_model() -> str:
    explicit = os.getenv("LLM_MODEL") or os.getenv("CHATBOT_MODEL")
    if explicit:
        return explicit
    if _use_ollama():
        return os.getenv("OLLAMA_MODEL", OLLAMA_CHAT_DEFAULT)
    for env_key, model in PROVIDER_DEFAULTS:
        if os.getenv(env_key):
            return model
    return PROVIDER_DEFAULTS[0][1]


def default_embedding_model() -> str:
    explicit = os.getenv("EMBEDDING_MODEL")
    if explicit:
        return explicit
    if _use_ollama() or not os.getenv("OPENAI_API_KEY"):
        return os.getenv("OLLAMA_EMBEDDING_MODEL", OLLAMA_EMBED_DEFAULT)
    return "text-embedding-3-small"
# ---- end canonical block -----------------------------------------------------


@dataclass(frozen=True)
class Config:
    # PER-PROJECT: cost tiers, thresholds, and the budget ceiling.
    model: str = field(default_factory=default_model)

    # Cascade tiers (live extension maps these to real models).
    cheap_model: str = "cheap"
    strong_model: str = "strong"
    # Illustrative per-call costs (offline). Live: derive from per-MTok prices x tokens.
    cheap_price: float = 0.001
    strong_price: float = 0.015

    # Semantic cache: a hit requires similarity >= cache_threshold.
    # Tuned so a re-asked question hits but a different "capital of X" question does NOT.
    cache_threshold: float = 0.90

    # Cascade: accept the cheap answer when its confidence >= cascade_threshold, else escalate.
    cascade_threshold: float = 0.60

    # Budget ceiling for a run (in the same units as the prices above).
    budget_ceiling: float = 1.00


def load_config() -> Config:
    return Config()
