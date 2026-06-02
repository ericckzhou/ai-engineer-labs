"""Validate the curriculum structure and obvious project catalog drift.

Run from the repository root:
    python scripts/validate_curriculum.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = ROOT / "projects"

REQUIRED_PROJECT_FILES = [
    "PROJECT.md",
    "IMPLEMENTATION.md",
    "EVALUATION.md",
    "FAILURE_ANALYSIS.md",
    "PROMPTS.md",
    "PROJECT_JOURNAL.md",
    "UNDERSTANDING.md",
    "UNDERSTANDING_FEEDBACK.md",
    "STARCALLOS_REFLECTION.md",
    "source/project.md",
    "source/lesson.agent.md",
    "source/rubric.md",
    "source/resources.md",
    "source/reflection.template.md",
    "rendered/lesson.html",
    "code/README.md",
    "code/requirements.txt",
    "code/.env.example",
]

MOJIBAKE_MARKERS = [
    "\u00e2",  # common UTF-8-as-Windows-1252 lead byte: â
    "\u00c2",  # stray non-breaking-space marker: Â
]


def project_dirs() -> list[Path]:
    return sorted(
        path
        for path in PROJECTS.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name)
    )


def check_required_files(errors: list[str]) -> None:
    for project in project_dirs():
        for relative in REQUIRED_PROJECT_FILES:
            candidate = project / relative
            if not candidate.exists():
                errors.append(f"missing: {candidate.relative_to(ROOT)}")


def check_mojibake(errors: list[str]) -> None:
    text_files = [
        *ROOT.glob("*.md"),
        *PROJECTS.rglob("*.md"),
        *PROJECTS.rglob("*.html"),
        *PROJECTS.rglob("*.py"),
    ]
    for path in text_files:
        text = path.read_text(encoding="utf-8")
        for marker in MOJIBAKE_MARKERS:
            if marker in text:
                errors.append(f"possible mojibake: {path.relative_to(ROOT)}")
                break


def check_catalog_links(errors: list[str]) -> None:
    catalog = PROJECTS / "index.html"
    if not catalog.exists():
        errors.append("missing: projects/index.html")
        return

    html = catalog.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"]+)"', html):
        if href.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = (catalog.parent / href).resolve()
        if not target.exists():
            errors.append(f"broken catalog link: projects/index.html -> {href}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_mojibake(errors)
    check_catalog_links(errors)

    if errors:
        print("Curriculum validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Curriculum validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
