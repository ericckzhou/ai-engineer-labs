"""config.py — [provided] Settings & provider/environment loading. NOT the learning target.

CANONICAL TEMPLATE — source of truth: skills/lesson-generator/templates/config.py
Stamped into each project's code/ by the lesson-generator skill.

The PROVIDER-RESOLUTION BLOCK below is canonical: keep it identical across every project so
it never drifts. It makes the LLM provider swappable by key/string. Order of preference:
explicit model > local Ollama (USE_OLLAMA, free, no key) > cloud key (Groq > Anthropic > OpenAI).
The `Config` dataclass is PER-PROJECT — add or remove fields for this project's needs.

For THIS elective the live LLM is optional: the agent backend runs offline with a deterministic
canned-response model, so the provider block matters only for the live-agent / LLM-guard
extensions. The BOUNDS and POLICY in `Config` ARE used by `guards.py` — read them from here,
do not hardcode them.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()  # reads code/.env into the environment (API keys + optional overrides)

# ---- CANONICAL: provider resolution (do not edit per project) ----------------
# Cloud provider preference order → (env key, default model via LiteLLM).
# Groq is the preferred cloud provider: it has a free tier. First key present wins.
PROVIDER_DEFAULTS: list[tuple[str, str]] = [
    ("GROQ_API_KEY", "groq/llama-3.3-70b-versatile"),
    ("ANTHROPIC_API_KEY", "claude-sonnet-4-6"),
    ("OPENAI_API_KEY", "gpt-4o-mini"),
]

# Local Ollama defaults (no API key, $0). Opt in with USE_OLLAMA=1. Requires a running
# Ollama server (localhost:11434) with these models pulled. LiteLLM routes "ollama/..."
# (use "ollama_chat/<model>" for higher-quality chat output if you prefer).
OLLAMA_CHAT_DEFAULT = "ollama/qwen3.5:4b"
OLLAMA_EMBED_DEFAULT = "ollama/nomic-embed-text"  # 768-dim


def _use_ollama() -> bool:
    return os.getenv("USE_OLLAMA", "").strip().lower() in {"1", "true", "yes", "on"}


def default_model() -> str:
    """Pick a default chat model. Explicit LLM_MODEL/CHATBOT_MODEL always wins.

    Then: local Ollama if USE_OLLAMA is set; else the first cloud provider whose key is
    present (Groq preferred). If nothing is configured, fall back to the Groq default so
    the resulting error clearly points at the intended provider.
    """
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
    """Pick a default embedding model. Explicit EMBEDDING_MODEL always wins.

    Groq/Anthropic have no embedding endpoint, so local Ollama is the natural keyless
    default: used when USE_OLLAMA is set or when no OPENAI_API_KEY is present. With an
    OpenAI key (and no USE_OLLAMA), default to OpenAI's small embedding model.
    """
    explicit = os.getenv("EMBEDDING_MODEL")
    if explicit:
        return explicit
    if _use_ollama() or not os.getenv("OPENAI_API_KEY"):
        return os.getenv("OLLAMA_EMBEDDING_MODEL", OLLAMA_EMBED_DEFAULT)
    return "text-embedding-3-small"
# ---- end canonical block -----------------------------------------------------


@dataclass(frozen=True)
class Config:
    # PER-PROJECT: the guard layer's bounds, PII policy, and output policy.
    # guards.py reads everything from here so there is one source of truth — do not
    # hardcode these values in guards.py.
    model: str = field(default_factory=default_model)

    # --- Input scanning ---
    max_input_chars: int = 8000          # hard cap on untrusted input length (incl. retrieved)

    # --- PII redaction (LLM02) ---
    # The entity types redact_output must detect. The recognizer for each is the learner's
    # to write (regex + checksum); the list and operator are policy, set here.
    pii_entities: tuple[str, ...] = ("EMAIL", "PHONE", "CREDIT_CARD", "SSN")
    pii_operator: str = "mask"            # one of: mask | replace | redact

    # --- Output policy enforcement ---
    output_max_chars: int = 4000
    # If the agent's structured output is JSON, only these keys may appear (allow-list).
    # For free-text output, this is unused; the length + forbidden-content checks still apply.
    allowed_output_keys: tuple[str, ...] = ("answer", "citations")
    # Substrings that must never appear in output (e.g. a system-prompt canary). Extend in
    # the canary extension.
    forbidden_output_substrings: tuple[str, ...] = ("SYSTEM PROMPT:", "BEGIN SYSTEM")

    # --- Fail-closed default ---
    refusal_text: str = (
        "I can't help with that request. (Blocked by the safety guard.)"
    )


def load_config() -> Config:
    """Return a frozen Config. API keys are loaded into the environment by load_dotenv()."""
    return Config()
