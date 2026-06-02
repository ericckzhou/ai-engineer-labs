# Sources

The ground truth layer. Highest epistemic authority in this repo.

See OPERATING_RULES.md: sources outrank all other layers.

## Directory Structure

```
sources/
├── papers/          ← Academic papers (notes + links, with key claims)
├── books/           ← Book chapter notes and summaries
├── videos/          ← Video lecture notes and timestamps
├── articles/        ← Engineering blog posts and articles
└── official-docs/   ← Official API and library documentation excerpts
```

## Source Entry Format

Every source gets its own file with this format:

```markdown
# [Title]

**Type:** paper | book | video | article | official-doc
**Tier:** 1 (Official Doc) | 2 (Paper) | 3 (Engineering Blog) | 4 (Educational)
**Author(s):**
**Date:**
**URL:**
**Accessed:**

## Why This Source Matters

One paragraph on why this source is authoritative and what it establishes.

## Key Claims

- Claim 1 (page/section reference if applicable)
- Claim 2
- Claim 3

## Relevant To

- concepts: [concept-1, concept-2]
- projects: [01-ai-chatbot, ...]

## Notes

Any caveats, limitations, or context about this source.
```

## Tier Definitions

| Tier | Type | Authority Level |
|------|------|----------------|
| 1 | Official Documentation | Definitive for that specific system |
| 2 | Foundational Paper | Establishes the concept |
| 3 | Engineering Blog | Practical usage, often by the builders |
| 4 | Educational | Explanation-focused; cites primary sources |

Always cite the highest-tier source available.

## Rule

Never cite a source that isn't in this directory. If you need to cite something, add it here first.

## Rendered Source Views

Markdown is canonical. Generated HTML exists only for human browsing:

```
catalogs/rendered/source-map.html
sources/rendered/<category>/<source-name>.html
```

Regenerate the HTML after source-map or source-note edits:

```bash
python scripts/render_sources.py
python scripts/render_sources.py --check
```

Do not hand-edit files under `catalogs/rendered/` or `sources/rendered/`.
