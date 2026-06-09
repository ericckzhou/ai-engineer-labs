# UNDERSTANDING.md — Template (Elective 02: Guardrails & Safety Layer)

> Copy this into the project root as `UNDERSTANDING.md` and complete it **before writing code**.
> Explain in your own words. Predict before you build. The mentor reviews this before you start.

---

## 1. The problem, in my words

Your Project 08 agent works. Why is "it works" not the same as "it's safe to put behind a public
text box"? Name the three things that change when the user is a stranger, not you.

## 2. The data/instruction boundary

A SQL database knows the difference between a command and data. An LLM does not. Explain why, and
why that makes prompt injection **structural** (not a bug you can patch). What does this imply
about putting "don't obey injected instructions" in the system prompt?

## 3. Direct vs. indirect injection

Define both. For indirect injection, say **where the hostile text lives** and why a scanner that
only reads the user's prompt is blind to it. (Hint: Project 04.)

## 4. Fail closed — predict

A guard hits an unexpected error mid-check. What should it do, and why is the *other* choice worse
than having no guard at all? Write the rule as one sentence.

## 5. Redaction — predict

You need to remove PII from the output. Sketch the **two stages** (before reading Presidio's
design in detail). What could go wrong if you mask text inside a JSON payload?

## 6. The tradeoff — predict

A guard can miss attacks or block legitimate users. Which one does "block everything" optimize, and
why is that guard useless? Name the **two** numbers your evaluation must report.

## 7. The honest claim

After you build this, will your agent be "safe"? Write the most accurate one-sentence claim you can
make about what guardrails actually buy you. (Re-read after building — did your claim hold?)

---

## Prediction log (fill before building, check after)

| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The benign input my scanner will wrongly block is… | | |
| The injection my scanner will miss is… | | |
| Redaction will break when… | | |

---

## Questions I have before starting
