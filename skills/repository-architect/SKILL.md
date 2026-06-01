# Skill: Repository Architect

**Type:** Method  
**Used by:** Architect, Curriculum Designer

## Purpose

Review the repository structure and curriculum holistically. Identify gaps, redundancies, and ordering problems. Generate actionable recommendations.

## Governing Documents

Read these before beginning any review:

1. `CLAUDE.md` — mission and knowledge flow
2. `PHILOSOPHY.md` — beliefs and principles
3. `OPERATING_RULES.md` — constraints that apply during this review
4. `ARCHITECTURE.md` — the intended structure being evaluated

## Review Sources

| Document | What It Reveals |
|----------|----------------|
| `docs/curriculum/overview.md` | Intended project sequence and rationale |
| `catalogs/concept-map.md` | Which concepts are taught, sourced, and known to be difficult |
| `catalogs/learning-objectives.md` | All learning objectives and their completion status |
| `catalogs/source-map.md` | Which concepts have source backing vs. are unsourced |
| `projects/*/source/lesson.agent.md` | Actual lesson content and concept coverage |
| `memory/project/decisions/` | Prior structural decisions and their rationale |
| `memory/learner/skill-map.md` | Where the learner currently is — informs what needs attention |

## Evaluation Criteria

For each project in the curriculum, assess:

- **Progression** — Does complexity grow at an appropriate rate?
- **Dependency ordering** — Are prerequisites taught before they're needed?
- **Concept coverage** — Are the essential concepts present? Are any missing?
- **Redundancy** — Is any concept taught multiple times without added depth?
- **Concept gaps** — Is anything assumed that hasn't been introduced?
- **Educational effectiveness** — Does the project actually teach what it claims to?
- **Source coverage** — Are the key concepts backed by sources in `sources/`?

## Diagnostic Questions

Answer these for every review:

1. Are projects ordered correctly? What would break if two were swapped?
2. Are all prerequisites satisfied before they're needed?
3. What concepts are present in `catalogs/concept-map.md` but missing from any lesson?
4. What concepts appear in multiple lessons without deepening?
5. What should be simplified (complexity exceeds educational value)?
6. What should be expanded (concept is used but not adequately taught)?
7. What should be removed (doesn't serve the mission)?

## Lenses to Apply

Apply each lens to each project:

- **Build vs. Buy** — Is the project teaching the learner to build something they should buy, or vice versa?
- **Resource** — Is the engineering cost of this project proportionate to its educational value?
- **Startup** — Does the concept have commercial relevance? Would users pay for a system built with this skill?
- **Architecture** — Does the project reinforce good system design thinking?

## Principles

Favor:
- Simplicity — the minimum complexity that achieves the learning objective
- Practicality — concepts that appear in real production systems
- Educational value — things the learner will use within 6 months
- Maintainability — lessons that won't be outdated in 12 months

Avoid:
- Curriculum bloat — adding projects because they're interesting, not essential
- Tool chasing — teaching a framework instead of the principle it implements
- Research rabbit holes — depth that serves academic curiosity but not engineering judgment
- Unnecessary complexity — architectures the learner isn't ready to understand

## Output

Recommendations go to `memory/project/decisions/` using the ADR template.

For each recommendation, produce:
- **Finding**: What the issue is
- **Impact**: What it affects (learning, sequencing, coverage)
- **Recommendation**: Specific action (add, remove, reorder, expand, simplify)
- **Priority**: High / Medium / Low
