# Skill: Documentation Synthesis

**Type:** Method  
**Used by:** Teacher, Curriculum Designer

## Purpose

Transform a dense agent-optimized document (`lesson.agent.md`) into a clear,
progressive, human-readable experience (`lesson.html`) without adding or removing content.

## Contract

The HTML version must:
- Contain all concepts from the agent version
- Not introduce requirements absent from the agent version
- Use progressive disclosure (simple → complex)
- Include callout boxes for important distinctions
- Include knowledge check sections
- Include working code examples
- Link to source material

The HTML version must not:
- Contradict the agent version
- Omit learning objectives
- Skip the reflection section
- Make grading criteria ambiguous

## Synthesis Procedure

1. Read `lesson.agent.md` in full
2. Identify the teaching arc (motivation → intuition → depth → application)
3. Map each agent section to the corresponding HTML section
4. Simplify language for ELI12 sections without losing accuracy
5. Add visual structure (callouts, milestones, tables) where it aids comprehension
6. Add concrete code examples for each abstract concept
7. Verify the HTML contains all required sections

## Quality Check

After synthesis, compare:
- All learning objectives present? ✓/✗
- All concepts from concept-map entry present? ✓/✗
- All rubric criteria covered? ✓/✗
- Code examples runnable? ✓/✗
