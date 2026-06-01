# The Learning Flow

## Overview

```
Read → Understand → Mentor Review → Implement → Break → Evaluate → Decide → Reflect → Next
```

Each stage has a concrete artifact. If you haven't produced the artifact, you haven't completed the stage.

---

## Stage 1: Read

**What you do:** Work through `LESSON.md` for the current project.

**How to read:**
- Slow down on things you don't understand
- Don't skim the intuition sections — they're the most important
- Look up every term you don't recognize
- Check the sources in `SOURCES.md`

**Artifact:** Nothing yet. Just understanding.

---

## Stage 2: Understand

**What you do:** Fill in `UNDERSTANDING.md` — in your own words.

**Rules:**
- No copy-pasting from the lesson
- No relying on LLMs to write it for you (you can use LLMs to *check* your understanding)
- If you can't explain it simply, you don't understand it yet

**Artifact:** Completed `UNDERSTANDING.md`

**Guiding questions:**
- Can you explain the core concept to a smart 12-year-old?
- What is the one thing this concept *solves*?
- What breaks if you remove it?
- How does it relate to something you already know?

---

## Stage 3: Mentor Review

**What you do:** Share `UNDERSTANDING.md` with a mentor (or use the AI mentor pattern — have Claude review it critically).

**The AI mentor pattern:**
```
"You are a rigorous AI engineering mentor. 
Read my understanding below and tell me:
1. What I got right
2. What I got wrong or oversimplified
3. What important concepts I missed
4. One question that would reveal gaps in my understanding

My understanding:
[paste UNDERSTANDING.md]"
```

**Artifact:** Completed `UNDERSTANDING_FEEDBACK.md`

---

## Stage 4: Implement

**What you do:** Build the project in `code/`.

**Rules:**
- Start minimal — get the core working before adding features
- Document as you go in `IMPLEMENTATION.md`
- Commit frequently with meaningful messages
- No framework magic you don't understand

**Artifact:** Working code + completed `IMPLEMENTATION.md`

---

## Stage 5: Break

**What you do:** Intentionally break the system in `FAILURE_ANALYSIS.md`.

**Why this matters:** You don't understand a system until you know how it fails.

**Break patterns:**
- Remove a key component — what breaks?
- Feed it bad input — what happens?
- Hit the edge cases — does it degrade gracefully?
- Simulate production load — where does it slow down?
- Make a bad design decision intentionally — what goes wrong?

**Artifact:** Completed `FAILURE_ANALYSIS.md`

---

## Stage 6: Evaluate

**What you do:** Answer "how do we know it works?" in `EVALUATION.md`.

**Evaluation axes:**
- **Correctness** — Does it produce right answers?
- **Reliability** — Does it work consistently?
- **Speed** — Is it fast enough?
- **Cost** — Is it affordable at scale?
- **Failure behavior** — Does it fail gracefully?

**Artifact:** Completed `EVALUATION.md`

---

## Stage 7: Record Decisions

**What you do:** Document every non-obvious decision in `DECISIONS.md`.

**What counts as a decision:**
- Build vs. buy choices
- Architecture tradeoffs
- Library selections
- Prompt design choices
- Parameter choices (chunk size, temperature, etc.)

**Artifact:** Completed `DECISIONS.md`

---

## Stage 8: Reflect

**What you do:** Write your retrospective in `PROJECT_JOURNAL.md` and `STARCALLOS_REFLECTION.md`.

**Reflection questions:**
- What surprised you?
- What would you do differently?
- What patterns emerged that you've seen before?
- What would you build next based on this?
- How does this apply to StarcallOS?

**Artifact:** Final entries in `PROJECT_JOURNAL.md` and `STARCALLOS_REFLECTION.md`

---

## Stage 9: Next Project

You're ready for the next project when:
- [ ] `UNDERSTANDING.md` — complete
- [ ] `UNDERSTANDING_FEEDBACK.md` — reviewed
- [ ] `IMPLEMENTATION.md` — complete
- [ ] `FAILURE_ANALYSIS.md` — complete
- [ ] `EVALUATION.md` — complete
- [ ] `DECISIONS.md` — complete
- [ ] `PROJECT_JOURNAL.md` — complete
- [ ] `STARCALLOS_REFLECTION.md` — complete
- [ ] Code is committed and runs cleanly
