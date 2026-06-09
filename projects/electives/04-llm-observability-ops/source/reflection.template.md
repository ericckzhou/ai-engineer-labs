# UNDERSTANDING.md — Template (Elective 04: LLM Observability & Ops)

> Copy into the project root as `UNDERSTANDING.md` and complete **before writing code**.

## 1. Observability vs. evaluation
*In your words, what does a trace tell you that a judge can't, and vice versa? Why do you need both?*

## 2. Standard names — predict
*Why use `gen_ai.usage.input_tokens` instead of your own `tokens_in`? What do you lose by inventing names?*

## 3. The global-mean trap — predict
*Your overall error rate is 3%. Why might that be a lie? What grouping fixes it?*

## 4. Drift — predict
*Define drift. Name one operational, one behavioral, and one distributional drift signal.*

## 5. The async judge — predict
*Why must a production quality-judge NOT run on every request synchronously? What does it do instead?*

---

## Prediction log (fill before, check after)
| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The route the monitor will flag is… | | |
| A threshold too tight will false-alarm on… | | |
| The metric that drifts most is… | | |

## Questions before starting
