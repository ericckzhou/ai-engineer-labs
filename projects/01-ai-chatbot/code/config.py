"""config.py — [provided] Settings & provider/environment loading. NOT the learning target.

CANONICAL TEMPLATE — source of truth: skills/lesson-generator/templates/config.py
The PROVIDER-RESOLUTION BLOCK below is canonical: keep it identical across every project.
It makes the LLM provider swappable by key (Groq free tier preferred). The `Config`
dataclass is PER-PROJECT — this project (chatbot) adds system_prompt + context_budget.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()  # reads code/.env into the environment (API keys + optional overrides)

# ---- CANONICAL: provider resolution (do not edit per project) ----------------
# Provider preference order → (env key, default model via LiteLLM).
# Groq is first: it offers a free tier. The first provider whose key is present wins.
PROVIDER_DEFAULTS: list[tuple[str, str]] = [
    ("GROQ_API_KEY", "groq/llama-3.3-70b-versatile"),
    ("ANTHROPIC_API_KEY", "claude-sonnet-4-6"),
    ("OPENAI_API_KEY", "gpt-4o-mini"),
]


def default_model() -> str:
    """Pick a default model from whichever provider key is present (Groq preferred).

    An explicit CHATBOT_MODEL always wins. If no known key is set, fall back to the Groq
    default so the resulting error clearly points at the intended provider.
    """
    explicit = os.getenv("CHATBOT_MODEL")
    if explicit:
        return explicit
    for env_key, model in PROVIDER_DEFAULTS:
        if os.getenv(env_key):
            return model
    return PROVIDER_DEFAULTS[0][1]
# ---- end canonical block -----------------------------------------------------


@dataclass(frozen=True)
class Config:
    # PER-PROJECT (chatbot): provider fields are canonical; the rest are this project's.
    model: str = field(default_factory=default_model)
    temperature: float = field(default_factory=lambda: float(os.getenv("CHATBOT_TEMPERATURE", "0.7")))
    max_tokens: int = field(default_factory=lambda: int(os.getenv("CHATBOT_MAX_TOKENS", "1024")))
    context_budget: int = field(default_factory=lambda: int(os.getenv("CHATBOT_CONTEXT_BUDGET", "100000")))
    system_prompt: str = field(
        default_factory=lambda: os.getenv("CHATBOT_SYSTEM_PROMPT", "You are a concise, helpful assistant.")
    )


def load_config() -> Config:
    """Return a frozen Config. API keys are loaded into the environment by load_dotenv()."""
    return Config()
