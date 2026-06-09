"""guarded_agent.py — [REFERENCE SOLUTION] verified copy (solns branch). Starter (TODOs) on main."""
from __future__ import annotations

from dataclasses import dataclass, field

from agent_backend import run_agent
from config import Config, load_config
from guards import enforce_policy, redact_output, scan_input


@dataclass
class GuardedResult:
    text: str
    blocked: bool
    stage: str | None = None
    evidence: dict = field(default_factory=dict)


def run_guarded(user_input: str, *, retrieved: str = "", cfg: Config | None = None) -> GuardedResult:
    cfg = cfg or load_config()
    try:
        v = scan_input(user_input, retrieved=retrieved, cfg=cfg)
        if v.blocked:
            return GuardedResult(cfg.refusal_text, True, "input",
                                 {"reason": v.reason, "rule": v.matched_rule})
        result = run_agent(user_input, context=retrieved)
        clean, hits = redact_output(result.text, cfg=cfg)
        ov = enforce_policy(clean, cfg=cfg)
        if ov.refused:
            return GuardedResult(ov.text, True, "output_policy", {"reason": ov.reason})
        return GuardedResult(ov.text, False, None, {"pii": hits})
    except Exception as e:  # FAIL CLOSED
        return GuardedResult(cfg.refusal_text, True, "error", {"error": str(e)})
