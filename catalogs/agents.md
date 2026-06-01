# Agents Catalog

Index of agent roles in this repository. Agents are reasoning roles, not code modules.

| Agent | Role | Primary Skills | Scope |
|-------|------|---------------|-------|
| [Architect](../agents/architect.md) | Design and evaluate system structure | repository-architect, architecture-review, repository-intelligence | ARCHITECTURE.md, projects/*/PROJECT.md, decisions |
| [Teacher](../agents/teacher.md) | Explain concepts progressively | lesson-generator, learning-design, source-grounding | docs/, rendered lessons |
| [Reviewer](../agents/reviewer.md) | Review learner work for correctness | mentor-reviewer, misconception-detection, source-grounding | UNDERSTANDING.md, code/, FAILURE_ANALYSIS.md |
| [Researcher](../agents/researcher.md) | Find and catalog primary sources | source-grounding | sources/, catalogs/source-map.md |
| [Grader](../agents/grader.md) | Evaluate against rubrics | assessment-design | evaluations/rubrics/, memory/learner/assessments/ |
| [Curriculum Designer](../agents/curriculum-designer.md) | Maintain curriculum coherence | learning-design, assessment-design | catalogs/learning-objectives.md, docs/curriculum/ |
| [Source Librarian](../agents/source-librarian.md) | Maintain source library integrity | source-grounding | sources/, catalogs/source-map.md |
| [Misconception Analyst](../agents/misconception-analyst.md) | Detect and document misconceptions | misconception-detection | UNDERSTANDING.md, memory/learner/misconceptions/ |

## Activation Guide

| Situation | Use This Agent |
|-----------|---------------|
| Learner asks for an explanation | Teacher |
| Learner submits UNDERSTANDING.md for review | Reviewer |
| Need to find a source for a concept | Researcher |
| Grading a project | Grader |
| Planning curriculum changes | Curriculum Designer |
| Adding sources to the library | Source Librarian |
| Learner shows a persistent misconception | Misconception Analyst |
| Proposing an architecture change | Architect |

## Rules

- Agents do not overlap in scope by design
- If two agents are both relevant, activate them sequentially (not simultaneously)
- Agent outputs go to their defined output locations — never mix them
