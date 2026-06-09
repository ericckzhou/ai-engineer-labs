# UNDERSTANDING.md — Elective 02: Guardrails & Safety Layer

> Complete this **before writing code** (Workflow B). Explain in your own words; predict before you
> build. The mentor reviews this before you start. Prompts are from
> [source/reflection.template.md](source/reflection.template.md).

---

## 1. The problem, in my words
*Why is "it works" not the same as "it's safe to expose"? Name the three things that change when the user is a stranger.*



## 2. The data/instruction boundary
*Why can't an LLM reliably separate instructions from data, and why does that make prompt injection structural rather than a patchable bug?*



## 3. Direct vs. indirect injection
*Define both. For indirect injection, where does the hostile text live, and why is scanning only the user prompt blind to it?*



## 4. Fail closed — predict
*A guard hits an unexpected error mid-check. What should it do, and why is the other choice worse than no guard? One sentence.*



## 5. Redaction — predict
*Sketch the two stages of removing PII. What breaks if you mask inside a JSON payload?*



## 6. The tradeoff — predict
*Which error does "block everything" optimize, and why is that guard useless? Name the two numbers your evaluation must report.*



## 7. The honest claim
*After building this, will your agent be "safe"? Write the most accurate one-sentence claim you can make.*



---

## Prediction log (fill before building, check after)

| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The benign input my scanner will wrongly block is… | | |
| The injection my scanner will miss is… | | |
| Redaction will break when… | | |

## Questions I have before starting
