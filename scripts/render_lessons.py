#!/usr/bin/env python3
"""render_lessons.py — generate rendered/lesson.html from a project's source/lesson.agent.md.

The agent version (`source/lesson.agent.md`) is canonical (ARCHITECTURE.md, Documentation
Contract). The human version is *derived*: this script converts the canonical Markdown to a
styled, readable HTML page so the two never drift by hand.

Zero dependencies (stdlib only). Supports the Markdown subset the lessons use: ATX headings,
paragraphs, unordered/ordered lists, GitHub pipe tables, fenced code blocks, blockquotes,
horizontal rules, and inline **bold** / `code` / [links](url).

Usage:
    python scripts/render_lessons.py [PROJECT_DIR ...]     # render given projects
    python scripts/render_lessons.py                       # render every project that has a
                                                           # lesson.agent.md but no lesson.html
    python scripts/render_lessons.py --all                 # (re)render every lesson it can find
    python scripts/render_lessons.py --check               # verify rendered HTML is current

By default it will NOT overwrite an existing rendered/lesson.html (so hand-authored lessons such
as Elective 01 are preserved). Pass --all to force.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
  :root {{ --fg:#1a1a2e; --muted:#5a5a72; --accent:#4f46e5; --bg:#fbfbfe; --code:#0f172a;
           --codebg:#f1f5f9; --border:#e2e8f0; --quote:#eef2ff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--fg);
          font:16px/1.7 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }}
  .wrap {{ max-width:820px; margin:0 auto; padding:48px 24px 96px; }}
  .banner {{ background:linear-gradient(135deg,#4f46e5,#7c3aed); color:#fff; border-radius:14px;
             padding:14px 20px; font-size:14px; margin-bottom:32px; }}
  .banner b {{ font-weight:700; }}
  h1 {{ font-size:30px; line-height:1.25; margin:8px 0 24px; }}
  h2 {{ font-size:23px; margin:40px 0 12px; padding-bottom:6px; border-bottom:2px solid var(--border); }}
  h3 {{ font-size:18px; margin:28px 0 10px; color:var(--accent); }}
  h4 {{ font-size:16px; margin:22px 0 8px; }}
  p {{ margin:12px 0; }}
  a {{ color:var(--accent); }}
  ul,ol {{ margin:12px 0; padding-left:26px; }}
  li {{ margin:5px 0; }}
  blockquote {{ margin:16px 0; padding:12px 18px; background:var(--quote);
                border-left:4px solid var(--accent); border-radius:0 8px 8px 0; }}
  blockquote p {{ margin:6px 0; }}
  code {{ background:var(--codebg); color:var(--code); padding:2px 6px; border-radius:5px;
          font:13.5px/1.5 "SF Mono",Menlo,Consolas,monospace; }}
  pre {{ background:var(--code); color:#e2e8f0; padding:16px 18px; border-radius:10px;
         overflow:auto; margin:16px 0; }}
  pre code {{ background:none; color:inherit; padding:0; }}
  table {{ border-collapse:collapse; width:100%; margin:18px 0; font-size:14.5px; }}
  th,td {{ border:1px solid var(--border); padding:8px 11px; text-align:left; vertical-align:top; }}
  th {{ background:#f8fafc; }}
  hr {{ border:none; border-top:1px solid var(--border); margin:32px 0; }}
  .meta {{ color:var(--muted); font-size:13px; }}
</style>
</head>
<body>
<div class="wrap">
<div class="banner"><b>Human (derived) version.</b> Generated from
<code>source/lesson.agent.md</code> by <code>scripts/render_lessons.py</code> — the agent
version is canonical. If they conflict, the agent version wins.</div>
{body}
</div>
</body>
</html>
"""

_INLINE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)"), r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
]


def _inline(text: str) -> str:
    """Escape HTML, then apply inline markdown. `code` spans are protected from escaping twice."""
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) >= 2:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
        else:
            esc = html.escape(part)
            for pat, repl in _INLINE:
                esc = pat.sub(repl, esc)
            out.append(esc)
    return "".join(out)


def _render_table(rows: list[str]) -> str:
    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    header = cells(rows[0])
    body = rows[2:]  # rows[1] is the --- separator
    html_rows = ["<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in header) + "</tr>"]
    for r in body:
        html_rows.append("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in cells(r)) + "</tr>")
    return "<table>" + "".join(html_rows) + "</table>"


def md_to_html(md: str) -> tuple[str, str]:
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    title = "Lesson"
    i = 0
    n = len(lines)
    list_stack: list[str] = []  # "ul" | "ol"

    def close_lists():
        while list_stack:
            out.append(f"</{list_stack.pop()}>")

    while i < n:
        line = lines[i]

        # fenced code
        if line.lstrip().startswith("```"):
            close_lists()
            code: list[str] = []
            i += 1
            while i < n and not lines[i].lstrip().startswith("```"):
                code.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>")
            continue

        # table (header line followed by a |---| separator)
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|[\s:|-]+$", lines[i + 1]):
            close_lists()
            tbl = [line, lines[i + 1]]
            i += 2
            while i < n and "|" in lines[i] and lines[i].strip():
                tbl.append(lines[i])
                i += 1
            out.append(_render_table(tbl))
            continue

        stripped = line.strip()

        if not stripped:
            close_lists()
            i += 1
            continue

        if stripped == "---":
            close_lists()
            out.append("<hr>")
            i += 1
            continue

        # headings
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            close_lists()
            level = len(m.group(1))
            text = _inline(m.group(2))
            if level == 1 and title == "Lesson":
                title = re.sub(r"<[^>]+>", "", text)
            out.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        # blockquote (possibly multi-line)
        if stripped.startswith(">"):
            close_lists()
            quote: list[str] = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = " ".join(q for q in quote if q.strip())
            out.append(f"<blockquote><p>{_inline(inner)}</p></blockquote>")
            continue

        # unordered list
        m = re.match(r"^(\s*)[-*]\s+(.*)$", line)
        if m:
            if not list_stack or list_stack[-1] != "ul":
                close_lists()
                list_stack.append("ul")
                out.append("<ul>")
            out.append(f"<li>{_inline(m.group(2))}</li>")
            i += 1
            continue

        # ordered list
        m = re.match(r"^(\s*)\d+\.\s+(.*)$", line)
        if m:
            if not list_stack or list_stack[-1] != "ol":
                close_lists()
                list_stack.append("ol")
                out.append("<ol>")
            out.append(f"<li>{_inline(m.group(2))}</li>")
            i += 1
            continue

        # paragraph
        close_lists()
        out.append(f"<p>{_inline(stripped)}</p>")
        i += 1

    close_lists()
    return title, "\n".join(out)


def render_project(project_dir: Path, force: bool) -> str | None:
    agent = project_dir / "source" / "lesson.agent.md"
    if not agent.exists():
        return None
    target = project_dir / "rendered" / "lesson.html"
    if target.exists() and not force:
        return f"skip (exists): {target.relative_to(REPO)}"
    title, body = md_to_html(agent.read_text(encoding="utf-8"))
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_TEMPLATE.format(title=html.escape(title), body=body), encoding="utf-8")
    return f"rendered: {target.relative_to(REPO)}"


def find_projects() -> list[Path]:
    return [p.parent.parent for p in REPO.glob("projects/**/source/lesson.agent.md")]


def main(argv: list[str]) -> int:
    force = "--all" in argv
    check = "--check" in argv
    paths = [Path(a) for a in argv if not a.startswith("--")]
    projects = [p if p.is_absolute() else (REPO / p) for p in paths] or find_projects()

    if check:
        stale = []
        for proj in projects:
            agent = proj / "source" / "lesson.agent.md"
            target = proj / "rendered" / "lesson.html"
            if not agent.exists():
                continue
            if not target.exists():
                stale.append(f"missing: {target}")
                continue
            _, body = md_to_html(agent.read_text(encoding="utf-8"))
            if body not in target.read_text(encoding="utf-8"):
                stale.append(f"stale: {target}")
        if stale:
            print("\n".join(stale))
            return 1
        print("All rendered lessons are up to date.")
        return 0

    # Default (no explicit paths): only render projects lacking a lesson.html (don't clobber).
    force = force or bool(paths)
    for proj in projects:
        msg = render_project(proj, force=force)
        if msg:
            print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
