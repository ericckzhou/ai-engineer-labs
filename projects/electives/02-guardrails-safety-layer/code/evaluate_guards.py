"""evaluate_guards.py — [provided] Score the guard layer on the labeled dataset.

Reports THREE numbers (lesson §8) — never just attack-catch rate:
  - attack-catch rate (recall): fraction of attack rows your scan blocks,
  - benign false-positive rate: fraction of benign rows your scan wrongly blocks,
  - PII leak rate: fraction of PII-bearing outputs that escape un-redacted.

Per-class breakdown so a 0%-caught attack kind can't hide behind an overall mean (cf. P09).

Run AFTER implementing guards.py:  python evaluate_guards.py
On the starter it will raise NotImplementedError from the guards — that is expected.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from config import load_config
from guards import redact_output, scan_input

DATASET = Path(__file__).parent / "datasets" / "attacks.jsonl"


def load_rows() -> list[dict]:
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    cfg = load_config()
    rows = load_rows()

    attacks = [r for r in rows if r["label"] == "attack"]
    benign = [r for r in rows if r["label"] == "benign"]
    pii_rows = [r for r in rows if r.get("pii_types") is not None and "pii_output" in r]

    # --- Input scanning ---
    caught = 0
    by_kind: dict[str, list[int]] = defaultdict(lambda: [0, 0])  # kind -> [caught, total]
    for r in attacks:
        v = scan_input(r["text"], retrieved=r.get("retrieved", ""), cfg=cfg)
        hit = 1 if v.blocked else 0
        caught += hit
        by_kind[r["kind"]][0] += hit
        by_kind[r["kind"]][1] += 1

    false_pos = 0
    for r in benign:
        v = scan_input(r["text"], retrieved=r.get("retrieved", ""), cfg=cfg)
        if v.blocked:
            false_pos += 1

    # --- PII redaction ---
    leaked = 0
    for r in pii_rows:
        clean, _hits = redact_output(r["pii_output"], cfg=cfg)
        # A leak = any expected entity's raw value still recoverable. We approximate by checking
        # that the obvious raw tokens are gone.
        raw_present = _raw_pii_present(r["pii_output"], clean, r["pii_types"])
        if raw_present:
            leaked += 1

    print("=== Guard Evaluation ===")
    print(f"attack-catch rate (recall):   {caught}/{len(attacks)} = {_pct(caught, len(attacks))}")
    for kind, (c, t) in sorted(by_kind.items()):
        print(f"    - {kind:10s}: {c}/{t} = {_pct(c, t)}")
    print(f"benign false-positive rate:   {false_pos}/{len(benign)} = {_pct(false_pos, len(benign))}")
    print(f"PII leak rate:                {leaked}/{len(pii_rows)} = {_pct(leaked, len(pii_rows))}")
    print()
    print("Read all three. High recall + high false-positive = rules too broad. A guard that")
    print("blocks everything has 100% recall and is useless (lesson §8).")


def _raw_pii_present(original: str, clean: str, types: list[str]) -> bool:
    """Heuristic leak check: did a clearly-PII token survive redaction?"""
    import re

    if not types:
        return False
    if "EMAIL" in types and re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", clean):
        return True
    if "SSN" in types and re.search(r"\b\d{3}-\d{2}-\d{4}\b", clean):
        return True
    if "PHONE" in types and re.search(r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b", clean):
        return True
    if "CREDIT_CARD" in types and re.search(r"\b(?:\d[ -]?){15,16}\b", clean):
        return True
    return False


def _pct(n: int, d: int) -> str:
    return f"{(100.0 * n / d):.0f}%" if d else "n/a"


if __name__ == "__main__":
    main()
