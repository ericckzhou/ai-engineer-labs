# STARCALLOS_REFLECTION.md — Elective 06: Structured Output & Reliability

> [learner] Patterns from this elective that could apply to StarcallOS. This lab builds the
> understanding, not StarcallOS itself. ≥1 concrete chain, with the mechanism.

## The pattern
*StarcallOS chains models: classify → pick a tool → fill arguments → act → judge. Each hop hands
structured data to the next. Name a concrete chain where ONE unreliable hop poisons the rest.*

## Where coerce sits
*At which boundary would you put the validate→repair→fail-closed layer, and what does it protect against
(e.g. a mis-parsed action running the wrong tool on real files)?*

## Fail-closed in a personal OS
*When an action can't be coerced to a valid, in-policy object, what should StarcallOS do instead of
guessing — ask the user? skip? log and halt? Why does "best guess" become dangerous when the system can
act on your data?*

## Cost angle (→ Elective 03)
*Every repair is a generation. Where in a personal OS would you prefer constrained decoding (cheap,
guaranteed shape) over a repair loop?*

## Implementation path
*One concrete way you'd build this into StarcallOS.*
