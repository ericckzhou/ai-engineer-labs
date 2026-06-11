"""structured_output.py — REFERENCE SOLUTION (solns branch). The reliability core (M1–M4).

Verified reference: all guiding tests pass offline (17/17); evaluate.py reports naive 17% -> robust
83% with the unfixable case correctly failing closed. On `main` this file is the learner stub
(NotImplementedError). See source/lesson.agent.md §3–§7.
"""
from __future__ import annotations

import json
import re

from config import Config, load_config
from schema import TICKET_SCHEMA


class StructuredOutputError(Exception):
    """Raised when coerce() cannot produce a schema-valid object within the attempt budget."""


def parse_strict(text: str) -> dict:
    """M1 — strict json.loads; no cleanup. Raises json.JSONDecodeError on non-bare-JSON."""
    return json.loads(text)


def extract_json(text: str) -> dict:
    """M2 — strip fences/prose, return the first balanced {...} object. Raises ValueError if none."""
    s = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", s, re.DOTALL)
    if m:
        s = m.group(1).strip()
    start = s.find("{")
    if start == -1:
        raise ValueError("no JSON object found")
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(s)):
        ch = s[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        else:
            if ch == '"':
                in_str = True
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return json.loads(s[start:i + 1])
    raise ValueError("no balanced JSON object found")


def validate(obj: dict, schema: dict = TICKET_SCHEMA, *, cfg: Config | None = None) -> list[str]:
    """M3 — return a list of error strings ([] = valid). bool is checked before int (bool ⊂ int)."""
    cfg = cfg or load_config()
    if not isinstance(obj, dict):
        return ["output is not a JSON object"]
    errors: list[str] = []
    for field, spec in schema.items():
        if field not in obj:
            if spec.get("required"):
                errors.append(f"{field}: required field missing")
            continue
        val = obj[field]
        typ = spec["type"]
        if typ is bool:
            if not isinstance(val, bool):
                errors.append(f"{field}: expected bool, got {type(val).__name__}")
                continue
        elif typ is int:
            if isinstance(val, bool) or not isinstance(val, int):
                errors.append(f"{field}: expected int, got {type(val).__name__}")
                continue
        elif not isinstance(val, typ):
            errors.append(f"{field}: expected {typ.__name__}, got {type(val).__name__}")
            continue
        if "enum" in spec and cfg.strict_enum and val not in spec["enum"]:
            errors.append(f"{field}: {val!r} not in {spec['enum']}")
        if "min" in spec and val < spec["min"]:
            errors.append(f"{field}: {val} below min {spec['min']}")
        if "max" in spec and val > spec["max"]:
            errors.append(f"{field}: {val} exceeds max {spec['max']}")
    return errors


def build_repair_prompt(message: str, bad_output: str, errors: list[str]) -> str:
    """M4a — repair prompt carrying the message, the bad output, and the SPECIFIC errors."""
    return (
        "Your previous response was not valid. Fix it.\n"
        f"Original support message: {message}\n"
        f"Your previous output: {bad_output}\n"
        "Validation errors:\n" + "\n".join(f"- {e}" for e in errors) +
        "\nReturn ONLY a valid JSON object, no prose, no code fences."
    )


def _task_prompt(message: str) -> str:
    return f"Extract a support ticket as JSON from this message: {message}"


def coerce(message: str, *, backend=None, schema: dict = TICKET_SCHEMA, cfg: Config | None = None) -> dict:
    """M4 — extract -> validate -> repair -> retry within cfg.max_attempts; fail closed on exhaustion."""
    cfg = cfg or load_config()
    if backend is None:
        import fake_backend
        backend = fake_backend
    prompt = _task_prompt(message)
    last_errors: list[str] = ["no valid output produced"]
    for attempt in range(cfg.max_attempts):
        raw = backend.generate(prompt)
        try:
            obj = extract_json(raw)
            errors = validate(obj, schema, cfg=cfg)
        except ValueError:
            obj, errors = None, ["output was not valid JSON"]
        if obj is not None and not errors:
            return obj
        last_errors = errors
        if not (cfg.allow_repair and attempt < cfg.max_attempts - 1):
            break
        prompt = build_repair_prompt(message, raw, errors)
    raise StructuredOutputError(f"could not coerce after {cfg.max_attempts} attempt(s): {last_errors}")
