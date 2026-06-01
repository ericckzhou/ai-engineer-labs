# Skill: Assessment Design

**Type:** Method  
**Used by:** Grader, Curriculum Designer

## Purpose

Design assessments that reveal genuine understanding, not surface pattern-matching.

## Principles

1. Assess the process, not just the output
   - A working implementation that the learner cannot explain reveals shallow understanding
   - An incorrect implementation with clear reasoning reveals learning in progress

2. Use diagnostic questions, not verification questions
   - Bad: "What is cosine similarity?" (can be looked up)
   - Good: "Why does cosine similarity behave differently from Euclidean distance for high-dimensional vectors?"

3. Require evidence, not claims
   - Bad: "I understood the RAG pipeline"
   - Good: "I chunked the PDF using X strategy because Y, and the retrieval precision was Z"

4. Assess understanding at multiple levels
   - Can they recall? (reproduce a definition)
   - Can they apply? (use it in code)
   - Can they analyze? (explain why it fails)
   - Can they evaluate? (compare alternatives)

## Rubric Construction Rules

- 4 levels per dimension (4 = excellent, 3 = good, 2 = developing, 1 = beginning)
- Each level has observable, specific criteria — not vague descriptors
- The target for "passing" is level 3 — level 4 is excellence, not the floor
- Scores are based on evidence, not effort
