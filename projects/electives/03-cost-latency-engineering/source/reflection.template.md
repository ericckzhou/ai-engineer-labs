# UNDERSTANDING.md — Template (Elective 03: Cost & Latency Engineering)

> Copy into the project root as `UNDERSTANDING.md` and complete **before writing code**.

## 1. The two axes
*Cost and quality are separate. Explain why you can't safely optimize cost without an eval, and what role Project 07's eval plays here.*

## 2. Prompt caching — predict
*A cache write costs MORE than a normal call. So when does caching actually save money? What happens if you cache a prefix that changes every request?*

## 3. Semantic cache — predict
*Sketch how a semantic cache decides a "hit". What is the "false hit", and which setting causes it?*

## 4. Cascade — predict
*A cascade sends easy queries to a cheap model and hard ones to a strong one. What's the hard part — and what goes wrong if you remove it (never escalate)?*

## 5. The honest result
*Your boss says "make it cheaper." Write the one-sentence result you'd report that an engineer would trust (hint: two numbers).*

---

## Prediction log (fill before, check after)
| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The cache threshold that causes a false hit is around… | | |
| The cascade will escalate on these queries… | | |
| Quality will drop by… and cost by… | | |

## Questions before starting
