# Failure Analysis

> You don't understand a system until you know how it fails.
> This file documents intentional breakage and unexpected failures.

## Intentional Breakage Experiments

> For each experiment: describe what you broke, what you expected, what actually happened, and what you learned.

### Experiment 1: [What You Broke]
**How I broke it:**
**What I expected to happen:**
**What actually happened:**
**Why it happened:**
**What this teaches about the system:**

### Experiment 2: [What You Broke]
**How I broke it:**
**What I expected to happen:**
**What actually happened:**
**Why it happened:**
**What this teaches about the system:**

### Experiment 3: [What You Broke]
**How I broke it:**
**What I expected to happen:**
**What actually happened:**
**Why it happened:**
**What this teaches about the system:**

<!-- Add more experiments — the more the better -->

---

## Unexpected Failures

> Things that broke without you trying to break them.

### Failure 1: [Description]
**What happened:**
**Root cause:**
**How I fixed it:**
**How to prevent this in production:**

---

## Edge Cases Discovered

> Inputs or conditions that caused unexpected behavior.

| Input / Condition | Expected | Actual | Notes |
|-------------------|----------|--------|-------|
| | | | |
| | | | |

---

## Production Risk Assessment

> Based on your failure experiments, how would this system perform in production?

**Biggest risk:**
**Most common failure mode:**
**Graceful degradation:** Does it fail gracefully? How?
**Monitoring needed:** What would you alert on?
