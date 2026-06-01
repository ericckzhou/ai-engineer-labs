# Skill: Architecture Review

**Type:** Method  
**Used by:** Architect

## Purpose

Evaluate the design of a system — whether a project implementation, the repo structure, or a proposed StarcallOS component.

## Review Checklist

**Separation of Concerns**
- [ ] Does each component do one thing?
- [ ] Are interfaces between components explicit?
- [ ] Can one component change without breaking others?

**Complexity Budget**
- [ ] Is every layer necessary?
- [ ] What breaks if you remove each component?
- [ ] Is there a simpler solution that achieves the same goal?

**Failure Design**
- [ ] How does this fail?
- [ ] Does it fail gracefully or catastrophically?
- [ ] Is there a circuit breaker or fallback?

**Production Readiness**
- [ ] Can this be monitored?
- [ ] What would you alert on?
- [ ] At what scale does this break?

**Build vs. Buy**
- [ ] Is this commodity or differentiated?
- [ ] What is the engineering cost vs. the buy cost?
- [ ] What is the maintenance cost over 12 months?

## Output Format

Architecture review report:
1. Summary (one paragraph)
2. Strengths
3. Concerns (each with: issue, why it matters, proposed fix)
4. Questions for the builder
5. Verdict: ready / needs revision / significant rework
