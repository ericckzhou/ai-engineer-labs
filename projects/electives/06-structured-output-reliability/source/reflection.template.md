# UNDERSTANDING.md — Template (Elective 06: Structured Output & Reliability)

> Copy into the project root as `UNDERSTANDING.md` and complete **before writing code**.

## 1. The three failure modes
*Name the three ways "just `json.loads` the output" fails. Which one is the most dangerous, and why?*

## 2. Extraction vs validation — predict
*Why are these different stages? Give one failure extraction fixes and one it can never fix.*

## 3. The bool/int trap — predict
*A model returns `"priority": true`. A naive `isinstance(priority, int)` check — does it catch it? Why?*

## 4. Repair — predict
*Why does feeding the specific validation errors back to the model beat a blind "try again"?*

## 5. Fail closed — predict
*The budget is exhausted and you still don't have a valid object. What should `coerce` do, and why is
returning the least-bad object dangerous?*

---

## Prediction log (fill before, check after)
| I predict… | Actual | Surprise? |
|------------|--------|-----------|
| The failure kind fixed with zero model calls is… | | |
| The failure kind that needs a repair round is… | | |
| Blind retry fails to converge because… | | |

## Questions before starting
