# Skills Catalog

Index of reusable reasoning skills. Skills are methods — they define *how* to do something.

| Skill | Purpose | Used By | When to Use |
|-------|---------|---------|------------|
| [Repository Architect](../skills/repository-architect/SKILL.md) | Review curriculum structure and generate actionable recommendations | Architect, Curriculum Designer | When auditing the full curriculum or proposing structural changes |
| [Repository Intelligence](../skills/repository-intelligence/SKILL.md) | Navigate repo without reading everything | Architect, Curriculum Designer | Before making structural claims or recommendations |
| [Lesson Generator](../skills/lesson-generator/SKILL.md) | Generate complete lesson content (agent.md + HTML + project spec) | Teacher, Curriculum Designer | When writing or updating a lesson from scratch |
| [Mentor Reviewer](../skills/mentor-reviewer/SKILL.md) | Review UNDERSTANDING.md and produce coaching feedback | Reviewer, Misconception Analyst | After learner submits UNDERSTANDING.md |
| [Source Grounding](../skills/source-grounding/SKILL.md) | Verify claims against primary sources | Teacher, Reviewer, Researcher | Before stating any factual claim |
| [Learning Design](../skills/learning-design/SKILL.md) | Structure explanations progressively | Teacher, Curriculum Designer | When creating or reviewing lesson content |
| [Misconception Detection](../skills/misconception-detection/SKILL.md) | Find incorrect beliefs in learner writing | Reviewer, Misconception Analyst | When reviewing UNDERSTANDING.md |
| [Assessment Design](../skills/assessment-design/SKILL.md) | Design assessments that reveal understanding | Grader, Curriculum Designer | When writing rubrics or diagnostic questions |
| [Architecture Review](../skills/architecture-review/SKILL.md) | Evaluate system design | Architect | When reviewing project designs or structural changes |
| [Documentation Synthesis](../skills/documentation-synthesis/SKILL.md) | Transform agent.md → lesson.html | Teacher, Curriculum Designer | When generating the human-readable lesson version |

## Skill Composition

Skills can be combined:

- **To audit the curriculum**: Repository Architect → produces recommendations → Architect files ADRs
- **To write a lesson**: Lesson Generator (wraps: Source Grounding + Learning Design + Documentation Synthesis)
- **To review understanding**: Mentor Reviewer (wraps: Misconception Detection + Source Grounding)
- **To review code**: Architecture Review + Misconception Detection (check both design and conceptual errors)
- **To add a source**: Source Grounding → Source Librarian files it in `sources/`
