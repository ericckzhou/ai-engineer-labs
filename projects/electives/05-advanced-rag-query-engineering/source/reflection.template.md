# UNDERSTANDING.md — Template (Elective 05: Advanced RAG / Query Engineering)

> Copy into the project root as `UNDERSTANDING.md` and complete **before writing code**.

## 1. The two failure modes
*Name the two ways naive retrieve-then-read fails. Why are both QUERY problems, not index problems?*

## 2. Rewriting — predict
*Why is the user's question often not the best retrieval query? What could go wrong with a rewrite?*

## 3. HyDE — predict
*What does HyDE embed, and why does embedding a (possibly wrong) hypothetical answer help? When might it HURT?*

## 4. Fusion — predict
*You split a multi-hop question and retrieve per sub-question. Why is concatenating all the chunks a bad idea? What should you do instead?*

## 5. The referee — predict
*You add HyDE and retrieval-hit goes up but faithfulness goes down. Did the transform help? What's the real metric?*

---

## Prediction log (fill before, check after)
| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The transform that helps paraphrase queries is… | | |
| The transform that HURTS factual queries is… | | |
| Fusion-by-concatenation will lower faithfulness because… | | |

## Questions before starting
