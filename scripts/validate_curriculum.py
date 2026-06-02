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
ELECTIVES = PROJECTS / "electives"
SOURCES = ROOT / "sources"
SOURCE_MAP = ROOT / "catalogs" / "source-map.md"
RENDERED_SOURCE_MAP = ROOT / "catalogs" / "rendered" / "source-map.html"
RENDERED_SOURCES = SOURCES / "rendered"

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


REQUIRED_SOURCE_FIELDS = [
    "Type",
    "Tier",
    "URL",
    "Accessed",
]

REQUIRED_SOURCE_SECTIONS = [
    "## Why This Source Matters",
    "## Key Claims",
    "## Relevant To",
]

SOURCE_REF_RE = re.compile(r"sources/(?!rendered/)[A-Za-z0-9_.\-/]+\.md")
PLACEHOLDER_MARKERS = [
    "placeholder-content",
    "to be written",
]


def project_dirs() -> list[Path]:
    return sorted(
        path
        for path in PROJECTS.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name)
    )


def elective_dirs() -> list[Path]:
    """Elective labs live under projects/electives/<NN-slug>/ and are validated SEPARATELY
    from the numbered 1-9 core spine (they are off-spine, optional, and don't gate anything)."""
    if not ELECTIVES.exists():
        return []
    return sorted(
        path
        for path in ELECTIVES.iterdir()
        if path.is_dir() and re.match(r"^\d{2}-", path.name)
    )


def _check_files_in(dirs: list[Path], errors: list[str], label: str) -> None:
    for project in dirs:
        for relative in REQUIRED_PROJECT_FILES:
            candidate = project / relative
            if not candidate.exists():
                errors.append(f"missing ({label}): {candidate.relative_to(ROOT)}")


def check_required_files(errors: list[str]) -> None:
    # Core spine and electives share the same required-file contract but are reported separately.
    _check_files_in(project_dirs(), errors, "core")
    _check_files_in(elective_dirs(), errors, "elective")


def check_mojibake(errors: list[str]) -> None:
    text_files = [
        *ROOT.glob("*.md"),
        *(ROOT / "catalogs").rglob("*.md"),
        *(ROOT / "docs").rglob("*.md"),
        *PROJECTS.rglob("*.md"),
        *PROJECTS.rglob("*.html"),
        *PROJECTS.rglob("*.py"),
        *SOURCES.rglob("*.md"),
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


def check_source_metadata(errors: list[str]) -> None:
    if not SOURCES.exists():
        errors.append("missing: sources")
        return

    for path in sorted(SOURCES.rglob("*.md")):
        if path.name == "README.md":
            continue
        if "rendered" in path.parts:
            continue

        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(ROOT)

        for field in REQUIRED_SOURCE_FIELDS:
            if not re.search(rf"^\*\*{re.escape(field)}:\*\*", text, re.MULTILINE):
                errors.append(f"missing source field {field}: {relative}")

        for section in REQUIRED_SOURCE_SECTIONS:
            if section not in text:
                errors.append(f"missing source section {section}: {relative}")


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCES.rglob("*.md")
        if path.name != "README.md" and "rendered" not in path.parts
    )


def rendered_source_path(source_path: Path) -> Path:
    relative = source_path.relative_to(SOURCES)
    return RENDERED_SOURCES / relative.with_suffix(".html")


def source_map_refs() -> list[Path]:
    if not SOURCE_MAP.exists():
        return []
    refs = sorted(set(SOURCE_REF_RE.findall(SOURCE_MAP.read_text(encoding="utf-8"))))
    return [ROOT / ref for ref in refs]


def check_rendered_sources(errors: list[str]) -> None:
    if not RENDERED_SOURCE_MAP.exists():
        errors.append(f"missing rendered source map: {RENDERED_SOURCE_MAP.relative_to(ROOT)}")

    refs = source_map_refs()
    ref_names = {path.relative_to(ROOT).as_posix() for path in refs}

    for ref in refs:
        if not ref.exists():
            errors.append(f"source-map references missing source: {ref.relative_to(ROOT)}")
            continue
        rendered = rendered_source_path(ref)
        if not rendered.exists():
            errors.append(f"missing rendered source note: {rendered.relative_to(ROOT)}")

    for source in source_files():
        source_name = source.relative_to(ROOT).as_posix()
        if source_name not in ref_names:
            errors.append(f"source missing from source-map: {source.relative_to(ROOT)}")

    html_files = []
    if RENDERED_SOURCE_MAP.exists():
        html_files.append(RENDERED_SOURCE_MAP)
    if RENDERED_SOURCES.exists():
        html_files.extend(sorted(RENDERED_SOURCES.rglob("*.html")))

    for path in html_files:
        text = path.read_text(encoding="utf-8")
        for marker in [*MOJIBAKE_MARKERS, *PLACEHOLDER_MARKERS]:
            if marker in text:
                errors.append(f"generated source html marker {marker!r}: {path.relative_to(ROOT)}")
                break


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_mojibake(errors)
    check_catalog_links(errors)
    check_source_metadata(errors)
    check_rendered_sources(errors)

    if errors:
        print("Curriculum validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Curriculum validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
