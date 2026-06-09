# Architecture

This document describes the repository structure and the reasoning behind it.

Structural changes require a decision record in `memory/project/decisions/`. See OPERATING_RULES.md, rule 8.

---

## Core Principle

```
Sources establish truth.
Docs teach truth.
Projects apply truth.
Evaluations judge the application.
Memory records what changed in the learner.
```

Each layer has a distinct role. No layer does another's job.

---

## Directory Map

```
ai-engineering-lab/
│
├── PHILOSOPHY.md          ← What we believe (beliefs, never instructions)
├── OPERATING_RULES.md     ← How Claude reasons (rules, never beliefs)
├── ARCHITECTURE.md        ← This file (structure, never content)
│
├── catalogs/              ← Navigation indexes (pointers, never truth)
│   ├── concept-map.md
│   ├── source-map.md
│   ├── skills.md
│   ├── agents.md
│   └── learning-objectives.md
│
├── skills/                ← Reusable reasoning methods
│   ├── repository-intelligence/
│   ├── source-grounding/
│   ├── learning-design/
│   ├── misconception-detection/
│   ├── assessment-design/
│   ├── architecture-review/
│   └── documentation-synthesis/
│
├── agents/                ← Named reasoning roles
│   ├── architect.md
│   ├── teacher.md
│   ├── reviewer.md
│   ├── researcher.md
│   ├── grader.md
│   ├── curriculum-designer.md
│   ├── source-librarian.md
│   └── misconception-analyst.md
│
├── docs/                  ← Teaching materials derived from sources
│   ├── meta/              ← Lab philosophy and methodology
│   ├── curriculum/        ← Curriculum overview and sequencing
│   └── experiments/       ← Ad-hoc explorations
│
├── projects/              ← Learning projects
│   ├── electives/         ← Off-spine projects (see "The Project Spine and Electives")
│   │   ├── 01-mcp-interface-layer/   ← Standalone elective
│   │   └── 0X-.../                   ← Production & Hardening track (E2–E5)
│   │                      ← Every project (spine or elective) has this structure:
│   └── XX-project-name/
│       ├── PROJECT.md     ← What we're building and why
│       ├── source/
│       │   ├── lesson.agent.md        ← Canonical lesson (agent-optimized)
│       │   ├── project.md             ← Detailed project spec
│       │   ├── rubric.md              ← Assessment criteria
│       │   ├── resources.md           ← Sources for this lesson
│       │   └── reflection.template.md ← Template for UNDERSTANDING.md
│       ├── rendered/
│       │   └── lesson.html            ← Human-readable lesson (generated from agent.md)
│       ├── UNDERSTANDING.md           ← Learner fills in (before implementation)
│       ├── UNDERSTANDING_FEEDBACK.md  ← Mentor/AI feedback on understanding
│       ├── IMPLEMENTATION.md          ← Learner documents their build process
│       ├── FAILURE_ANALYSIS.md        ← Intentional breakage experiments
│       ├── EVALUATION.md              ← Quantitative evaluation results
│       ├── DECISIONS.md               ← Engineering decisions log
│       ├── PROJECT_JOURNAL.md         ← Running notes
│       ├── STARCALLOS_REFLECTION.md   ← Patterns applicable to StarcallOS
│       ├── PROMPTS.md                 ← Prompts designed for this project
│       └── code/                      ← Implementation
│
├── evaluations/           ← Evaluation infrastructure (separate from docs)
│   ├── rubrics/           ← Rubric definitions
│   ├── checkpoints/       ← Progress checkpoint records
│   ├── grader-prompts/    ← LLM-as-judge prompts for evaluation
│   └── project-criteria/  ← Per-project success criteria
│
├── memory/                ← Accumulated knowledge (split by type)
│   ├── project/           ← What happened in this repo
│   │   ├── decisions/     ← Architecture and structural decisions
│   │   ├── retrospectives/← Project retrospectives
│   │   └── lessons-learned/ ← Cross-project insights
│   └── learner/           ← What changed in the learner
│       ├── misconceptions/ ← Documented and corrected misconceptions
│       ├── reflections/    ← Learner reflections across projects
│       ├── projects/       ← Per-project completion records
│       ├── assessments/    ← Assessment results and scores
│       └── skill-map.md    ← Current skill level across all domains
│
├── sources/               ← Ground truth source material
│   ├── papers/            ← Academic papers (notes + links)
│   ├── books/             ← Book notes and chapter summaries
│   ├── videos/            ← Video lecture notes and links
│   ├── articles/          ← Engineering blog articles
│   └── official-docs/     ← Official documentation excerpts and links
│
├── README.md              ← Entry point for new users
├── SETUP.md               ← Environment setup
├── pyproject.toml         ← Base Python dependencies
├── .env.example           ← Environment variable template
└── .gitignore
```

---

## The Project Spine and Electives

Projects come in two kinds.

**The build spine (Projects 1–9)** is a single, ordered narrative: each project introduces a
*new capability*, escalating from a model call (P01) to autonomous agents (P08) to a composition
**capstone (P09)**. Spine projects are taken in order; each assumes the prior ones.

**Electives** live under `projects/electives/` and sit *off* the numbered spine. They apply,
harden, or extend capabilities the spine already built, and are order-independent after their
prerequisite project. There are two groupings:

- **Standalone electives** — e.g. `01-mcp-interface-layer` (wraps P05 as an MCP server).
- **The Production & Hardening track (E2–E5)** — a *named, sequenced-as-a-group* elective track,
  recommended **after** the P09 capstone. It covers what separates a demo from a production
  system: Guardrails & Safety (E2), Cost & Latency (E3), Observability & Ops (E4), and Advanced
  RAG (E5). Each attaches to a spine prerequisite (E2→P08, E3→P07, E4→P07/P08, E5→P04).

The track keeps the capstone at P09 (it does not move into the numbered spine) while still
framing production work as the real next stage rather than optional fluff. This grouping was a
deliberate structural decision:
`memory/project/decisions/2026-06-09-production-hardening-elective-track.md`.

---

## The Two Memory Types Explained

### `memory/project/` — What happened in this repo

Records of events, decisions, and learnings at the repository level.

- `decisions/` — Every structural decision with rationale (see OPERATING_RULES.md rule 8)
- `retrospectives/` — Post-project retrospectives across the curriculum
- `lessons-learned/` — Cross-project engineering insights

These answer: "What happened here? What did we decide and why?"

### `memory/learner/` — What changed in the learner

Records of the learner's growth, struggles, and development.

- `misconceptions/` — Documented misconceptions and their corrections
- `reflections/` — Synthesized reflections across multiple projects
- `projects/` — Completion status and notes per project
- `assessments/` — Rubric scores over time
- `skill-map.md` — Current skill level across all AI engineering domains

These answer: "Who is the learner becoming? What do they know? What do they still struggle with?"

**Key constraint:** Learner memory informs personalization. It never overrides source truth.

---

## The Catalogs Explained

Catalogs are navigation maps, not content stores. They answer: "Where should I look for X?"

- `catalogs/concept-map.md` — Maps concepts to sources, lessons, and known learner issues
- `catalogs/source-map.md` — Maps topics to sources by tier
- `catalogs/skills.md` — Index of available skills and when to use them
- `catalogs/agents.md` — Index of available agents and their responsibilities
- `catalogs/learning-objectives.md` — All learning objectives across the curriculum

A catalog entry looks like:
```markdown
## Cosine Similarity
Sources: sources/papers/attention-is-all-you-need.md
Lesson: projects/02-token-embedding-explorer/source/lesson.agent.md#cosine-similarity
Known learner issues: memory/learner/misconceptions/2026-06-01-cosine-vs-dot-product.md
```

---

## Skills vs. Agents

**Skills = methods.** A skill is a reusable reasoning procedure.
Example: `skills/source-grounding/` contains the procedure for verifying a claim against primary sources.

**Agents = roles.** An agent is a named persona with defined responsibilities and scope.
Example: `agents/grader.md` defines what the grader role does, what it can judge, and what rubrics it uses.

An agent uses skills. A skill is not an agent.

---

## The Dual-Format Lesson Contract

Every lesson exists in two formats, derived from a single canonical source:

```
source/lesson.agent.md → (derived) → rendered/lesson.html
```

**lesson.agent.md** is the canonical truth layer:
- Dense, structured, complete
- Optimized for AI reasoning
- Contains all requirements, rubrics, objectives, instructor notes

**lesson.html** is the learner experience:
- Visual, readable, progressive
- Derived from lesson.agent.md
- Never introduces requirements not in the agent version

If they conflict, lesson.agent.md wins.

---

## Separation of Concerns

| Layer | Question It Answers | Changes Via |
|-------|--------------------|-----------| 
| PHILOSOPHY.md | What do we believe? | Deliberate revision |
| OPERATING_RULES.md | What must Claude do? | Deliberate revision |
| ARCHITECTURE.md | What is the structure? | Decision record |
| sources/ | What is true? | Adding/updating sources |
| docs/ | How do we teach it? | Lesson authoring |
| projects/ | How do we apply it? | Project completion |
| evaluations/ | How do we judge it? | Rubric authoring |
| memory/project/ | What happened? | Event recording |
| memory/learner/ | Who is the learner? | Assessment + reflection |
| catalogs/ | Where do I find X? | Index updates |
