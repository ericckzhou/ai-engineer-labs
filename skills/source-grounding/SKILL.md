# Skill: Source Grounding

**Type:** Method  
**Used by:** Teacher, Reviewer, Researcher

## Purpose

Verify that a claim is backed by a primary source before stating it.

## Procedure

1. Identify the claim being made
2. Check `catalogs/concept-map.md` — is there a listed source?
3. If yes: navigate to `sources/` and verify the source supports the claim
4. If no: check `sources/` directly by topic
5. If still not found: state "I cannot find a primary source for this claim"
6. Never cite a source that doesn't exist in `sources/` without flagging that it needs to be added

## Failure Modes

- Fabricating a citation (critical violation — never do this)
- Citing a secondary source as primary (e.g., a tutorial that cites a paper — use the paper)
- Citing an outdated source without noting the date

## Output Format

When a claim is grounded: cite the source inline.  
When a claim cannot be grounded: "This claim needs a primary source — adding to `sources/` is recommended."
