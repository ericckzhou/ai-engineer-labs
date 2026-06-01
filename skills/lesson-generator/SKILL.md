# Skill: Lesson Generator

**Type:** Method  
**Used by:** Teacher, Curriculum Designer

## Purpose

Generate complete lesson content for a project. Produces the canonical agent version and the derived human HTML version. All content must be grounded in primary sources.

## Governing Documents

Read before generating any lesson:

1. `CLAUDE.md` — mission, documentation contract, Workflow A (lesson generation)
2. `PHILOSOPHY.md` — teaching principles (intuition before terminology)
3. `skills/learning-design/SKILL.md` — the 10-section teaching pattern
4. `skills/source-grounding/SKILL.md` — source verification procedure
5. `skills/documentation-synthesis/SKILL.md` — agent.md → HTML contract

## Pre-Generation Checklist

Before writing any lesson content:

- [ ] Check `catalogs/concept-map.md` — what concepts are already mapped?
- [ ] Check `sources/` — what primary sources exist for this topic?
- [ ] Check `catalogs/source-map.md` — what tier coverage exists?
- [ ] If sources are insufficient, run `skills/source-grounding/SKILL.md` first and add them to `sources/`
- [ ] Read the project's `PROJECT.md` for scope and learning objectives

Do not generate lesson content from memory alone. Sources first.

## What This Skill Generates

### Files Created or Completed

| File | Location | Notes |
|------|----------|-------|
| `lesson.agent.md` | `projects/XX/source/` | Canonical lesson — all 10 sections |
| `lesson.html` | `projects/XX/rendered/` | Human version — derived from agent.md |
| `project.md` | `projects/XX/source/` | Detailed project spec with milestones |
| `resources.md` | `projects/XX/source/` | Annotated source list for this lesson |
| `rubric.md` | `projects/XX/source/` | Project-specific assessment criteria |
| `.env.example` | `projects/XX/code/` | `provided` — env var template when keys are needed |
| starter modules | `projects/XX/code/` | `partial`/`learner` — setup & interfaces solved, core left incomplete |
| guiding tests | `projects/XX/code/tests/` | `provided` — failing/guiding checks the learner makes pass |

### Files This Skill Does NOT Touch

The following are learner-filled templates. They exist as scaffolds. Do not overwrite them:

- `UNDERSTANDING.md` — learner writes this before building
- `UNDERSTANDING_FEEDBACK.md` — written by mentor-reviewer skill after learner submits
- `IMPLEMENTATION.md` — learner fills during build
- `FAILURE_ANALYSIS.md` — learner fills after breaking
- `EVALUATION.md` — learner fills after measuring
- `DECISIONS.md` — learner fills throughout
- `PROJECT_JOURNAL.md` — learner fills throughout
- `STARCALLOS_REFLECTION.md` — learner fills after completion
- `PROMPTS.md` — learner fills throughout

## Lesson Content Requirements (`lesson.agent.md`)

Every lesson must contain all 10 sections. Do not skip any.

### Section Structure

1. **Motivation** — Why does this exist? What problem existed before? Real engineering stakes.
2. **ELI12** — Explain the core concept to a curious 12-year-old. Use an analogy.
3. **ELI-Engineer** — Technical depth. Assume strong programming background, weak AI background.
4. **Real-World Analogy** — A concrete parallel from outside AI that explains the mechanism.
5. **What Problem It Solves** — Before vs. after. What broke without it?
6. **What Breaks Without It** — Specific failure modes in real systems.
7. **Production Usage** — How real products use this. Name actual systems when possible.
8. **Code Example** — Minimal working implementation using the lab's stack (Python, LiteLLM).
9. **Common Mistakes** — Errors the learner will likely make. Include: mistake, consequence, fix.
10. **Production-Level Understanding** — What separates a novice from an expert on this topic?

### Additional Required Sections

- **Learning Objectives** — 6–8 specific, measurable objectives (what the learner *will be able to do*)
- **Guided Examples** — Simple case, real-world case, failure case — each with code and explanation
- **Reflection Prompts** — 6–8 questions for the learner to answer in `UNDERSTANDING.md`
- **Project Milestones** — 4–6 incremental checkpoints, each runnable independently
- **Self-Evaluation Criteria** — Specific criteria the learner uses to assess their own implementation
- **Instructor Notes** — Common misconceptions, diagnostic questions, signs of genuine understanding

### Source Requirements

Every factual claim must be traceable to a source in `sources/`.

When citing: reference the source entry in `sources/` (e.g., `sources/papers/attention-is-all-you-need.md`).
When a claim lacks a source: flag it with `[SOURCE NEEDED]` — do not silently assert unsourced claims.

## Human Version Requirements (`lesson.html`)

Generated from `lesson.agent.md` using `skills/documentation-synthesis/SKILL.md`.

> **⚠️ Rendering is a REQUIRED step, not optional — and it is the one most often skipped.**
> The `rendered/lesson.html` that ships in a fresh project is the **stamped skeleton**: correct
> CSS, but every content block is a `<!-- TODO -->` / `placeholder-content` stub. A lesson is
> **not done** until those stubs are replaced with the real content from `lesson.agent.md`.
> Authoring `lesson.agent.md` and leaving the HTML as the skeleton is the default failure mode.
> **Verify before claiming done** (must print `0`):
>
> ```bash
> grep -cE "TODO|placeholder-content|to be written" projects/XX/rendered/lesson.html   # → 0
> ```
>
> If it prints anything but `0`, the HTML was not rendered — finish it before committing.

**Styling is canonical, stamped inline.** The `<style>` block is stamped from
`skills/lesson-generator/templates/lesson.css` (kept inline so the page opens standalone with
no server). Keep all `lesson.html` `<style>` blocks byte-identical to the template — edit the
template and re-stamp; do not hand-edit per project. **Render rule:** never place raw text +
inline `<code>` as direct children of a `display:flex` element (e.g. `.objectives li`) — wrap
prose in a `<span>`, or the text collapses to one word per line.

Must include:
- Sidebar navigation
- All 10 lesson sections
- Callout boxes for key distinctions (info, tip, warning, danger)
- Working code blocks with syntax highlighting
- Knowledge check section with the reflection prompts
- Milestone steps (visual progression)
- Self-evaluation table
- Source tier boxes at the bottom

Must not:
- Introduce requirements absent from `lesson.agent.md`
- Omit any learning objective
- Skip the reflection section
- Make assessment criteria ambiguous

## Project Spec Requirements (`source/project.md`)

The detailed project specification (separate from the high-level `PROJECT.md` overview).

Must include:
- Precise definition of done
- File-by-file implementation spec
- Input/output contracts for key functions
- Extended requirements (beyond core)
- Known difficulty spikes
- Suggested debugging approach

## Code Scaffolding Requirements (`code/`)

Governed by `OPERATING_RULES.md` §Scaffolding Rules (16–19). The boundary: **setup solved, interfaces clear, learning target incomplete.**

**Provider & canonical templates.** Projects are self-contained (OPERATING_RULES §15), so shared `provided` plumbing is **stamped from a canonical template, not imported**. Stamp these into each project's `code/`:

- `skills/lesson-generator/templates/config.py` — the **provider-resolution block is canonical** (keep it byte-identical across projects); the `Config` dataclass is per-project (add the fields this project needs). It makes the LLM provider **swappable by key**, defaulting to **Groq (free tier)** and falling back Groq → Anthropic → OpenAI based on which `*_API_KEY` is set. An explicit `CHATBOT_MODEL` always wins.
- `skills/lesson-generator/templates/.env.example` — lists `GROQ_API_KEY` first; other providers are optional commented entries.

Do not invent provider pricing for `cost_tracker.py` — fill `$/MTok` from the provider's official pricing page or leave it to raise on unknown models. (See memory: default-api-groq.)

**Always generate:**
- A clear brief (already in `PROJECT.md` / `source/project.md`).
- Starter files with clear interfaces — function/class signatures, type hints, docstrings stating the contract.
- Dependency setup (`requirements.txt`) and `.env.example` when environment variables are needed.
- A one-command run workflow and a one-command test workflow (document both in `code/README.md`).
- Guiding tests or checks the learner makes pass (place in `code/tests/`). Pure-logic checks (e.g. cost math) should be runnable with no network.
- Optional hints and extension tasks (extension tasks live in `source/project.md` "Extended Requirements").

**Never generate:**
- A complete working solution for the learner-owned core component.
- Copy-paste final answers or hidden "magic" that bypasses the intended learning.
- Excessive scaffolding that removes the main design decision.

**Label every file** in the `source/project.md` File Specification as `provided`, `partial`, `learner`, or `reference`. Mark learner-owned gaps with `TODO`, `raise NotImplementedError`, failing tests, or empty functions/classes.

**Pick the incomplete component from the objective** (OPERATING_RULES §19): API wiring → message construction & model call; prompt design → prompt construction; conversation memory → history management; evaluation → eval design/instrumentation.

## Post-Generation Checklist

- [ ] All 10 lesson sections present in `lesson.agent.md`
- [ ] All claims sourced — no `[SOURCE NEEDED]` remaining (or explicitly deferred)
- [ ] **`lesson.html` actually RENDERED** from `lesson.agent.md` — every section populated, **no skeleton stubs left**. Verify: `grep -cE "TODO|placeholder-content|to be written" projects/XX/rendered/lesson.html` prints `0`. (Do not mistake the pre-stamped CSS skeleton for a rendered lesson.)
- [ ] `catalogs/concept-map.md` updated with new concepts
- [ ] `catalogs/source-map.md` updated with new sources
- [ ] `source/resources.md` annotated with all sources used
- [ ] `code/` scaffolding follows the boundary: setup solved, interfaces clear, **core left incomplete**
- [ ] Every `code/` file labeled `provided`/`partial`/`learner`/`reference` in `source/project.md`
- [ ] `.env.example` present if env vars are needed; one-command run AND test workflows documented
- [ ] At least one guiding test exists that the learner must make pass
- [ ] No complete solution for the learner-owned core component is committed
