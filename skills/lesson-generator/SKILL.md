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

## Post-Generation Checklist

- [ ] All 10 lesson sections present in `lesson.agent.md`
- [ ] All claims sourced — no `[SOURCE NEEDED]` remaining (or explicitly deferred)
- [ ] `lesson.html` contains everything from `lesson.agent.md`
- [ ] `catalogs/concept-map.md` updated with new concepts
- [ ] `catalogs/source-map.md` updated with new sources
- [ ] `source/resources.md` annotated with all sources used
