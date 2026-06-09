"""guards.py — [REFERENCE SOLUTION] verified copy (solns branch).

The completed learner core. The spoiler-free starter (NotImplementedError cores) is on main.
See source/lesson.agent.md. Verified green offline (tests/ + evaluate_guards.py).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass

from config import Config, load_config


class GuardError(Exception):
    """Hard guard failure. Callers must treat this as a BLOCK (fail closed)."""


@dataclass
class InputVerdict:
    decision: str
    reason: str
    matched_rule: str | None = None
    span: str | None = None

    @property
    def blocked(self) -> bool:
        return self.decision == "block"


@dataclass
class OutputVerdict:
    decision: str
    reason: str
    text: str

    @property
    def refused(self) -> bool:
        return self.decision == "refuse"


_INJECTION_RULES: list[tuple[str, re.Pattern]] = [
    ("instruction_override", re.compile(
        r"\b(ignore|disregard|forget)\b.{0,30}\b(previous|above|prior|all|your)\b.{0,25}\b(instruction|instructions|rules|prompt)\b",
        re.I)),
    ("role_switch", re.compile(
        r"(you are now|\bact as\b|pretend to be|developer mode|jailbreak|\bDAN\b|unfiltered|no restrictions|without restrictions)",
        re.I)),
    ("system_extraction", re.compile(
        r"\b(reveal|print|show|repeat|output)\b.{0,25}(system prompt|your instructions|your prompt|initial prompt)",
        re.I)),
    ("exfiltration", re.compile(
        r"\b(send|email|post|forward|upload|exfiltrate)\b.{0,40}\bto\b.{0,25}(https?://|@|attacker|evil)",
        re.I)),
]

_PII_RECOGNIZERS: dict[str, re.Pattern] = {
    "EMAIL": re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
    "PHONE": re.compile(r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"),
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "CREDIT_CARD": re.compile(r"\b(?:\d[ -]?){13,16}\b"),
}


def scan_input(user_input: str, *, retrieved: str = "", cfg: Config | None = None) -> InputVerdict:
    cfg = cfg or load_config()
    try:
        if len(f"{user_input}{retrieved}") > cfg.max_input_chars:
            return InputVerdict("block", "input exceeds max length", "length")
        for rule, pat in _INJECTION_RULES:
            for channel, text in (("user", user_input), ("retrieved", retrieved)):
                m = pat.search(text)
                if m:
                    return InputVerdict("block", f"{rule} in {channel}", rule, m.group(0)[:80])
        return InputVerdict("allow", "no injection pattern matched")
    except Exception as e:  # FAIL CLOSED
        return InputVerdict("block", f"scan error (fail closed): {e}", "error")


def _apply_operator(value: str, entity: str, operator: str) -> str:
    if operator == "redact":
        return ""
    if operator == "replace":
        return f"<{entity}>"
    if entity == "CREDIT_CARD":
        last4 = re.sub(r"\D", "", value)[-4:]
        return f"****-****-****-{last4}"
    last4 = value[-4:]
    return "*" * max(0, len(value) - 4) + last4


def redact_output(text: str, *, cfg: Config | None = None) -> tuple[str, list[str]]:
    cfg = cfg or load_config()
    if not isinstance(text, str):
        return "", []
    hits: list[str] = []
    out = text
    for entity in cfg.pii_entities:
        pat = _PII_RECOGNIZERS.get(entity)
        if pat is None:
            continue

        def _sub(m: re.Match, _entity=entity) -> str:
            val = m.group(0)
            if _entity == "CREDIT_CARD" and not luhn_valid(val):
                return val
            if _entity not in hits:
                hits.append(_entity)
            return _apply_operator(val, _entity, cfg.pii_operator)

        out = pat.sub(_sub, out)
    return out, hits


def enforce_policy(output: str, *, cfg: Config | None = None) -> OutputVerdict:
    cfg = cfg or load_config()
    try:
        if not isinstance(output, str):
            return OutputVerdict("refuse", "non-string output", cfg.refusal_text)
        if len(output) > cfg.output_max_chars:
            return OutputVerdict("refuse", "output exceeds max length", cfg.refusal_text)
        for bad in cfg.forbidden_output_substrings:
            if bad in output:
                return OutputVerdict("refuse", "forbidden content (possible leak)", cfg.refusal_text)
        stripped = output.strip()
        if stripped.startswith("{"):
            try:
                obj = json.loads(stripped)
                if isinstance(obj, dict):
                    for k in obj:
                        if k not in cfg.allowed_output_keys:
                            return OutputVerdict("refuse", f"key '{k}' not in allow-list", cfg.refusal_text)
            except json.JSONDecodeError:
                pass
        return OutputVerdict("pass", "conforms to policy", output)
    except Exception as e:  # FAIL CLOSED
        return OutputVerdict("refuse", f"policy error (fail closed): {e}", cfg.refusal_text)


def luhn_valid(digits: str) -> bool:
    nums = [int(c) for c in re.sub(r"\D", "", digits)]
    if len(nums) < 12:
        return False
    checksum = 0
    parity = len(nums) % 2
    for i, n in enumerate(nums):
        if i % 2 == parity:
            n *= 2
            if n > 9:
                n -= 9
        checksum += n
    return checksum % 10 == 0
