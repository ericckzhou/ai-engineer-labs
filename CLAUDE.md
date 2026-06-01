# CLAUDE.md

This is the entry point for any Claude instance entering this repository.

Read this first. Then follow the navigation order below. Do not skip layers.

---

## Mission

This repository exists to create project-based learning experiences for AI Systems Engineering.

The goal is not content generation.

The goal is durable understanding through:

- Reading
- Reflection
- Building
- Testing
- Revisiting

Projects are the primary learning vehicle.

Every concept is introduced because it solves a real engineering problem.

---

## Repository Navigation

Read documents in this order when entering the repository cold:

1. `PHILOSOPHY.md` — What we believe. Never overridden.
2. `OPERATING_RULES.md` — What Claude must do. Overrides everything below.
3. `ARCHITECTURE.md` — How the repository is structured. Change only via decision record.
4. `catalogs/` — Navigation indexes. Where to find anything. Read before exploring.
5. `skills/` — Reusable reasoning methods. How to do things.
6. `agents/` — Named reasoning roles. Who does what and what scope they own.
7. `docs/` — Teaching materials derived from sources.
8. `memory/` — History. What happened. What the learner knows. Personalizes, never overrides.
9. `sources/` — Ground truth. Highest epistemic authority.

Higher layers override lower layers when they conflict.

When in doubt about layer authority, consult `OPERATING_RULES.md`.

---

## Knowledge Flow

Knowledge flows in one direction:

```
sources/
  ↓
docs/ + projects/
  ↓
projects/*/UNDERSTANDING.md (learner reflections)
  ↓
memory/learner/
```

Never derive source material from memory.

**Sources contain truth. Memory records outcomes.**

If a claim in `memory/` contradicts a claim in `sources/`, the source wins.
If you cannot find a source for a claim, say so. Do not invent one.

---

## Learning Principles

Do not optimize for content generation.

Optimize for understanding.

Before introducing solutions:

1. Build intuition — analogy before terminology.
2. Ask for predictions — what does the learner expect to happen?
3. Require explanation — the learner states it in their own words before seeing code.
4. Require implementation — reading is not learning; building is.
5. Require reflection — what broke? what surprised? what would you do differently?

Projects are mandatory whenever practical.

Passive learning experiences are insufficient.

A learner who can recite a definition but cannot build, break, or evaluate a system has not learned.

---

## Documentation Contract

Every lesson produces two outputs derived from a single canonical source.

### Agent Version (Canonical)

- File: `source/lesson.agent.md`
- Format: Markdown
- Purpose: Source of truth. Structured for LLMs. Dense and complete.
- Contains: learning objectives, prerequisites, core concepts, rubrics, assessment criteria, sources, instructor notes.

### Human Version (Derived)

- File: `rendered/lesson.html`
- Format: HTML
- Purpose: Learner-facing experience. Progressive. Visual. Readable.
- Generated from the Agent Version.

**The Human Version must not introduce requirements absent from the Agent Version.**

**If they conflict, the Agent Version wins.**

---

## Workflows

There are two distinct workflows in this repository. Do not conflate them.

### Workflow A: Lesson Generation (Claude as content author)

When generating or updating lesson content for a concept:

1. Find the relevant sources in `sources/` — do not proceed without primary sources.
2. Consult `catalogs/concept-map.md` for what already exists.
3. Generate `source/lesson.agent.md` using `skills/lesson-generator/SKILL.md` (which covers sourcing, structure, and HTML rendering).
4. Generate learner reflection prompts for `UNDERSTANDING.md`.
5. Generate the project assignment for `source/project.md`.
6. Generate project milestones (4–6 incremental checkpoints).
7. Generate the assessment rubric for `source/rubric.md`.
8. Generate `code/` starter scaffolding per the Scaffolding Boundary below — and label every file.
9. Generate `rendered/lesson.html` from the agent version.
10. Update `catalogs/concept-map.md` with any new concepts and sources.

Do not generate lesson content from memory. Gather evidence from `sources/` first.

#### Scaffolding Boundary (see `OPERATING_RULES.md` §Scaffolding Rules)

Remove accidental friction; preserve essential struggle.

- **Setup is solved; the learning target is incomplete.** Provide deps, `.env.example` (when env vars are needed), one-command run + test workflows, starter files with clear interfaces, and guiding tests. Do **not** provide the finished core component, copy-paste answers, hidden "magic," or so much scaffolding that the main design decision disappears.
- **Label every file or section** as `provided`, `partial`, `learner`, or `reference`. Mark learner-owned work with `TODO`, `raise NotImplementedError`, failing tests, or empty functions/classes.
- **Pick the incomplete component from the objective:** API wiring → model-call/message construction; prompt design → prompt construction; conversation memory → history management; evaluation → eval design/instrumentation.

### Workflow B: Learning Support (Claude as mentor/guide)

When a learner is actively working through a project:

```
Learner reads lesson
  ↓
Learner explains concept in their own words (→ UNDERSTANDING.md)
  ↓
Claude reviews understanding (using Reviewer agent + mentor-reviewer skill)
  ↓
Learner predicts how implementation should work
  ↓
Learner builds (→ code/)
  ↓
Learner intentionally breaks it (→ FAILURE_ANALYSIS.md)
  ↓
Learner evaluates results (→ EVALUATION.md)
  ↓
Learner reflects (→ PROJECT_JOURNAL.md, STARCALLOS_REFLECTION.md)
  ↓
Claude grades (using Grader agent + master rubric)
  ↓
Memory updated (→ memory/learner/)
```

Never skip directly from reading to showing a solution.

If the learner asks for the answer before attempting: ask them to predict first, attempt first, or explain their current thinking first.

---

## What Does Not Belong in This File

- Architecture details → `ARCHITECTURE.md`
- Operating constraints → `OPERATING_RULES.md`
- Lesson content → `projects/*/source/lesson.agent.md`
- Source material → `sources/`
- Engineering decisions → `memory/project/decisions/`
- Learner history → `memory/learner/`
- Prompts → `projects/*/PROMPTS.md`

This file stays small. If it grows past 300 lines, something has been misplaced.
