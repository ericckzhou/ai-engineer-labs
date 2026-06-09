# UNDERSTANDING.md — Elective 03: Cost & Latency Engineering

> Complete **before writing code**. Prompts from [source/reflection.template.md](source/reflection.template.md).

## 1. The two axes
*Why can't you safely optimize cost without an eval? What role does Project 07's eval play here?*



## 2. Prompt caching — predict
*A cache write costs MORE than a normal call. So when does caching save money? What if you cache a prefix that changes every request?*



## 3. Semantic cache — predict
*How does a semantic cache decide a "hit"? What is the false hit, and which setting causes it?*



## 4. Cascade — predict
*What's the hard part of a cascade, and what goes wrong if you never escalate?*



## 5. The honest result
*"Make it cheaper." Write the one-sentence result an engineer would trust (two numbers).*



---

## Prediction log (fill before, check after)
| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The cache threshold that causes a false hit is around… | | |
| The cascade will escalate on these queries… | | |
| Quality will drop by… and cost by… | | |

## Questions before starting
