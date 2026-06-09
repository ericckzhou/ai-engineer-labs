"""exporter.py — [provided] The OpenTelemetry "exporter" stand-in.

A real system exports spans to a collector (Jaeger, Tempo, an OTLP endpoint). Here a SpanCollector
holds them in memory and can read/write JSONL, so the whole elective runs offline with no infra.
Your tracing code emits spans into one of these; your monitor reads spans out of one.
"""
from __future__ import annotations

import json
from pathlib import Path


class SpanCollector:
    def __init__(self) -> None:
        self.spans: list[dict] = []

    def add(self, span: dict) -> None:
        self.spans.append(span)

    def to_jsonl(self, path: str | Path) -> None:
        Path(path).write_text(
            "\n".join(json.dumps(s) for s in self.spans) + "\n", encoding="utf-8"
        )

    @classmethod
    def from_jsonl(cls, path: str | Path) -> "SpanCollector":
        c = cls()
        text = Path(path).read_text(encoding="utf-8")
        c.spans = [json.loads(line) for line in text.splitlines() if line.strip()]
        return c


def load_spans(path: str | Path) -> list[dict]:
    """Convenience: read a JSONL span file into a list of span dicts."""
    return SpanCollector.from_jsonl(path).spans
