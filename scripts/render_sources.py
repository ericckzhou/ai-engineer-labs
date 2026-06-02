"""Render source-map and source notes to standalone HTML.

Markdown remains canonical. This script creates generated views only:
    catalogs/rendered/source-map.html
    sources/rendered/<category>/<source>.html

Run:
    python scripts/render_sources.py
    python scripts/render_sources.py --check
"""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MAP = ROOT / "catalogs" / "source-map.md"
CATALOG_RENDERED = ROOT / "catalogs" / "rendered" / "source-map.html"
SOURCES = ROOT / "sources"
SOURCES_RENDERED = SOURCES / "rendered"
CSS_TEMPLATE = ROOT / "skills" / "lesson-generator" / "templates" / "lesson.css"

SOURCE_REF_RE = re.compile(r"sources/(?!rendered/)[A-Za-z0-9_.\-/]+\.md")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CODE_SPAN_RE = re.compile(r"`([^`]+)`")
FIELD_RE = re.compile(r"^\*\*(?P<name>[^:]+):\*\*\s*(?P<value>.*)$")


def root_relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def rendered_source_path(source_path: Path) -> Path:
    relative = source_path.relative_to(SOURCES)
    return SOURCES_RENDERED / relative.with_suffix(".html")


def href(from_file: Path, to_file: Path) -> str:
    return Path(os.path.relpath(to_file, start=from_file.parent)).as_posix()


def all_source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCES.rglob("*.md")
        if path.name != "README.md" and "rendered" not in path.parts
    )


def source_map_refs() -> list[Path]:
    text = SOURCE_MAP.read_text(encoding="utf-8")
    refs = sorted(set(SOURCE_REF_RE.findall(text)))
    return [ROOT / ref for ref in refs]


def validate_refs() -> tuple[list[Path], list[str]]:
    refs = source_map_refs()
    errors: list[str] = []

    for ref in refs:
        if not ref.exists():
            errors.append(f"source-map references missing source: {root_relative(ref)}")

    ref_set = {root_relative(path) for path in refs}
    for source in all_source_files():
        if root_relative(source) not in ref_set:
            errors.append(f"source missing from source-map: {root_relative(source)}")

    return refs, errors


def parse_metadata(markdown: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in markdown.splitlines():
        match = FIELD_RE.match(line)
        if match:
            metadata[match.group("name")] = match.group("value")
    return metadata


def slug(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return cleaned or "section"


def render_inline(text: str, current_html: Path) -> str:
    placeholders: list[str] = []

    def store(value: str) -> str:
        placeholders.append(value)
        return f"\x00{len(placeholders) - 1}\x00"

    def replace_md_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(1))
        target = match.group(2)
        if target.startswith(("http://", "https://", "#", "mailto:")):
            safe_target = html.escape(target, quote=True)
        else:
            candidate = (ROOT / target).resolve()
            if candidate.exists() and root_relative(candidate).startswith("sources/") and candidate.suffix == ".md":
                safe_target = html.escape(href(current_html, rendered_source_path(candidate)), quote=True)
            else:
                safe_target = html.escape(target, quote=True)
        return store(f'<a href="{safe_target}">{label}</a>')

    def replace_code(match: re.Match[str]) -> str:
        content = match.group(1)
        if SOURCE_REF_RE.fullmatch(content):
            target = ROOT / content
            if target.exists():
                rendered = href(current_html, rendered_source_path(target))
                return store(
                    f'<a class="src" href="{html.escape(rendered, quote=True)}">'
                    f"{html.escape(content)}</a>"
                )
        return store(f"<code>{html.escape(content)}</code>")

    text = MD_LINK_RE.sub(replace_md_link, text)
    text = CODE_SPAN_RE.sub(replace_code, text)

    escaped = html.escape(text)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)

    for idx, value in enumerate(placeholders):
        escaped = escaped.replace(f"\x00{idx}\x00", value)
    return escaped


def render_markdown(markdown: str, current_html: Path) -> tuple[str, list[tuple[str, str]]]:
    html_parts: list[str] = []
    nav: list[tuple[str, str]] = []
    lines = markdown.splitlines()
    i = 0
    in_ul = False
    in_ol = False

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            html_parts.append("</ul>")
            in_ul = False
        if in_ol:
            html_parts.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            close_lists()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            html_parts.append(f"<pre><code>{html.escape(chr(10).join(code_lines))}</code></pre>")
            i += 1
            continue

        if not line.strip():
            close_lists()
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading:
            close_lists()
            level = len(heading.group(1))
            title = heading.group(2).strip()
            ident = slug(title)
            nav.append((title, ident))
            html_parts.append(
                f'<h{level} id="{ident}">{render_inline(title, current_html)}</h{level}>'
            )
            i += 1
            continue

        if line.strip() == "---":
            close_lists()
            html_parts.append("<hr>")
            i += 1
            continue

        if line.startswith("> "):
            close_lists()
            quote_lines = [line[2:]]
            i += 1
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:])
                i += 1
            quote = " ".join(part.strip() for part in quote_lines)
            html_parts.append(f'<div class="callout info"><p>{render_inline(quote, current_html)}</p></div>')
            continue

        bullet = re.match(r"^\s*[-*]\s+(.+)$", line)
        if bullet:
            if in_ol:
                html_parts.append("</ol>")
                in_ol = False
            if not in_ul:
                html_parts.append("<ul>")
                in_ul = True
            html_parts.append(f"<li>{render_inline(bullet.group(1), current_html)}</li>")
            i += 1
            continue

        numbered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if numbered:
            if in_ul:
                html_parts.append("</ul>")
                in_ul = False
            if not in_ol:
                html_parts.append("<ol>")
                in_ol = True
            html_parts.append(f"<li>{render_inline(numbered.group(1), current_html)}</li>")
            i += 1
            continue

        close_lists()
        paragraph = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4})\s+", lines[i]):
            if lines[i].startswith(("```", "> ")) or re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                break
            paragraph.append(lines[i])
            i += 1
        html_parts.append(f"<p>{render_inline(' '.join(part.strip() for part in paragraph), current_html)}</p>")

    close_lists()
    return "\n".join(html_parts), nav


def page(title: str, badge: str, body: str, nav: list[tuple[str, str]], extra_header: str = "") -> str:
    css = CSS_TEMPLATE.read_text(encoding="utf-8")
    source_css = """
  .source-actions { display:flex; flex-wrap:wrap; gap:10px; margin-top:16px; }
  .source-actions a { background:var(--accent-bg); color:var(--accent); padding:7px 11px; border-radius:7px; text-decoration:none; font-size:13px; font-weight:600; }
  .source-actions a:hover { text-decoration:underline; }
  .metadata-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap:10px; align-items:start; margin:18px 0 28px; }
  .metadata-item { background:var(--surface); border:1px solid var(--border); border-radius:8px; padding:10px 12px; min-width:0; overflow-wrap:anywhere; word-break:normal; }
  .metadata-item strong { display:block; font-size:11px; text-transform:uppercase; letter-spacing:0.08em; color:var(--text-muted); margin-bottom:3px; }
  .metadata-item a { overflow-wrap:anywhere; word-break:break-word; }
  .metadata-item.metadata-authors { grid-column:span 2; }
  .metadata-item.metadata-url { grid-column:span 2; }
  hr { border:0; border-top:1px solid var(--border); margin:28px 0; }
  main ul, main ol { margin: 12px 0 18px 24px; }
  main li { margin-bottom: 8px; }
  @media (max-width: 900px) {
    .metadata-grid { grid-template-columns: 1fr; }
    .metadata-item.metadata-authors,
    .metadata-item.metadata-url { grid-column:auto; }
  }
"""
    nav_links = "\n".join(
        f'<li><a href="#{ident}">{html.escape(text)}</a></li>' for text, ident in nav[:40]
    )
    if not nav_links:
        nav_links = '<li><a href="#top">Top</a></li>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(title)}</title>
  <style>
{css}
{source_css}
  </style>
</head>
<body>
  <div class="layout">
    <nav class="sidebar">
      <div class="nav-brand">AI Engineering Lab</div>
      <div class="nav-project-title">{html.escape(title)}</div>
      <ul>
        {nav_links}
      </ul>
    </nav>
    <main id="top">
      <header class="lesson-header">
        <div class="lesson-badge">{html.escape(badge)}</div>
        <h1>{html.escape(title)}</h1>
        <p class="lesson-tagline">Generated HTML view. Markdown remains canonical.</p>
        {extra_header}
      </header>
      {body}
    </main>
  </div>
</body>
</html>
"""


def render_source_map() -> str:
    body, nav = render_markdown(SOURCE_MAP.read_text(encoding="utf-8"), CATALOG_RENDERED)
    header = '<div class="source-actions"><a href="../../catalogs/source-map.md">Canonical Markdown</a></div>'
    return page("Source Map", "Rendered Catalog", body, nav, header)


def render_source_note(source: Path) -> str:
    markdown = source.read_text(encoding="utf-8")
    body, nav = render_markdown(markdown, rendered_source_path(source))
    metadata = parse_metadata(markdown)
    metadata_items: list[str] = []
    for key, value in metadata.items():
        if key not in {"Type", "Tier", "Author(s)", "Date", "URL", "Accessed"}:
            continue
        class_name = "metadata-item"
        if key == "Author(s)":
            class_name += " metadata-authors"
        if key == "URL":
            class_name += " metadata-url"
            safe_value = html.escape(value, quote=True)
            rendered_value = f'<a href="{safe_value}">{html.escape(value)}</a>'
        else:
            rendered_value = render_inline(value, rendered_source_path(source))
        metadata_items.append(
            f'<div class="{class_name}"><strong>{html.escape(key)}</strong>'
            f"{rendered_value}</div>"
        )
    metadata_html = "\n".join(metadata_items)
    source_map_link = href(rendered_source_path(source), CATALOG_RENDERED)
    markdown_link = href(rendered_source_path(source), source)
    header = f"""
        <div class="source-actions">
          <a href="{html.escape(source_map_link, quote=True)}">Rendered Source Map</a>
          <a href="{html.escape(markdown_link, quote=True)}">Canonical Markdown</a>
        </div>
        <div class="metadata-grid">{metadata_html}</div>
"""
    title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else source.stem
    return page(title, "Rendered Source Note", body, nav, header)


def write_or_check(path: Path, content: str, check: bool, errors: list[str]) -> None:
    if check:
        if not path.exists():
            errors.append(f"missing generated html: {root_relative(path)}")
            return
        existing = path.read_text(encoding="utf-8")
        if existing != content:
            errors.append(f"stale generated html: {root_relative(path)}")
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def run(check: bool) -> int:
    refs, errors = validate_refs()
    if errors:
        for error in errors:
            print(error)
        return 1

    write_or_check(CATALOG_RENDERED, render_source_map(), check, errors)
    for source in refs:
        write_or_check(rendered_source_path(source), render_source_note(source), check, errors)

    if errors:
        for error in errors:
            print(error)
        return 1

    if check:
        print("Rendered source HTML is up to date.")
    else:
        print(f"Rendered source map: {root_relative(CATALOG_RENDERED)}")
        print(f"Rendered source notes: {len(refs)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Render source map and source notes to HTML.")
    parser.add_argument("--check", action="store_true", help="Fail if generated HTML is missing or stale.")
    args = parser.parse_args()
    return run(check=args.check)


if __name__ == "__main__":
    sys.exit(main())
