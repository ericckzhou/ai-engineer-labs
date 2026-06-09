"""evaluate_rag.py — [provided] Prove which transforms help, PER TRANSFORM (lesson §8).

Runs the frozen QA set through each transform (none / rewrite / hyde / decompose) and reports,
per transform:
  - retrieval-hit  : were ALL gold chunks retrieved?
  - context-prec.  : fraction of fused contexts that are gold (the distractor-dilution / faithfulness
                     proxy — naive concatenation tanks this)
  - answer-rel.    : did the answer contain the expected keyword(s)?

"More retrieved" is not the metric — a transform with higher hit but lower context-precision can be
a regression. Run AFTER implementing the cores: python evaluate_rag.py
"""
from __future__ import annotations

import json
from pathlib import Path

import advanced_rag
from config import load_config

EVAL = Path(__file__).parent / "eval_set.jsonl"
TRANSFORMS = ["none", "rewrite", "hyde", "decompose"]


def load_rows() -> list[dict]:
    return [json.loads(line) for line in EVAL.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    cfg = load_config()
    rows = load_rows()

    print(f"{'transform':12}{'hit':>8}{'ctx-prec':>10}{'ans-rel':>9}")
    for t in TRANSFORMS:
        hits = precs = rels = 0.0
        for r in rows:
            res = advanced_rag.answer(r["query"], transform=t, cfg=cfg)
            ids = [c.id for c in res.contexts]
            gold = set(r["gold_ids"])
            hits += 1.0 if gold.issubset(ids) else 0.0
            precs += (sum(1 for i in ids if i in gold) / len(ids)) if ids else 0.0
            rels += 1.0 if all(kw.lower() in res.answer.lower() for kw in r["answer_keywords"]) else 0.0
        n = len(rows)
        print(f"{t:12}{_pct(hits, n):>8}{_pct(precs, n):>10}{_pct(rels, n):>9}")

    print("\nRead per transform. Rewrite should rescue the paraphrase case; decompose the multi-hop;")
    print("factual needs neither. A transform that raises hit but lowers ctx-prec is a regression (§8).")


def _pct(x: float, n: int) -> str:
    return f"{(100.0 * x / n):.0f}%" if n else "n/a"


if __name__ == "__main__":
    main()
