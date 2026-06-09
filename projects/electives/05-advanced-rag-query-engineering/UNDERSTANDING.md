# UNDERSTANDING.md — Elective 05: Advanced RAG / Query Engineering

> Complete **before writing code**. Prompts from [source/reflection.template.md](source/reflection.template.md).

## 1. The two failure modes
*Name the two ways naive retrieve-then-read fails. Why are both QUERY problems, not index problems?*



## 2. Rewriting — predict
*Why is the user's question often not the best retrieval query? What could go wrong with a rewrite?*



## 3. HyDE — predict
*What does HyDE embed, and why does embedding a (possibly wrong) hypothetical answer help? When might it HURT?*



## 4. Fusion — predict
*You split a multi-hop question and retrieve per sub-question. Why is concatenating all the chunks bad? What should you do instead?*



## 5. The referee — predict
*HyDE raises retrieval-hit but lowers faithfulness. Did it help? What's the real metric?*



---

## Prediction log (fill before, check after)
| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The transform that helps paraphrase queries is… | | |
| The transform that HURTS factual queries is… | | |
| Concatenation fusion lowers faithfulness because… | | |

## Questions before starting
