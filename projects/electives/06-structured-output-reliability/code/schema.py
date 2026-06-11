"""schema.py — [provided] The target schema the model must fill. NOT the learning target.

The task: turn a free-text support message into a structured `Ticket`. This file provides the
CONTRACT (what a valid object looks like) as data; YOU write the code in structured_output.py that
ENFORCES it (validate) and REPAIRS violations (coerce). Keeping the schema as a plain spec — not a
third-party model — is deliberate: it makes the validation rules visible so you implement them.

A `TICKET_SCHEMA` field spec:
  type     — the required Python type (note: bool is a subclass of int — check bool BEFORE int)
  required — must be present
  enum     — (optional) allowed values
  min/max  — (optional) inclusive integer bounds
"""
from __future__ import annotations

from dataclasses import dataclass

# The structured contract the model output must satisfy. structured_output.validate() enforces this.
TICKET_SCHEMA: dict[str, dict] = {
    "category": {"type": str, "required": True, "enum": ["billing", "technical", "account", "other"]},
    "priority": {"type": int, "required": True, "min": 1, "max": 5},
    "needs_human": {"type": bool, "required": True},
    "summary": {"type": str, "required": True},
}


@dataclass(frozen=True)
class Ticket:
    """The typed target object. `to_ticket` builds one from a validated dict."""
    category: str
    priority: int
    needs_human: bool
    summary: str


def to_ticket(obj: dict) -> Ticket:
    """Build a Ticket from an already-VALIDATED dict (call validate() first)."""
    return Ticket(
        category=obj["category"],
        priority=obj["priority"],
        needs_human=obj["needs_human"],
        summary=obj["summary"],
    )
