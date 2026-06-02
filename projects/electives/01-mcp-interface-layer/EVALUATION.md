# Evaluation

> How do we know it works? Measure everything.
> For this elective, the central evidence is the TWO-CONSUMER demonstration.

## The Two-Consumer Demonstration (Definition of Done)

> Prove one server, many hosts. Record what each consumer saw.

| Consumer | How you connected it | Tools/resources/prompt it saw | Result |
|----------|----------------------|-------------------------------|--------|
| #1 stdio client (`client_smoke_test.py`) | | | |
| #2 host (Claude Desktop / MCP Inspector) | | | |

**Cross-consumer round-trip:** save a note via one, read it as a resource via the other.
**What happened:**

---

## Evaluation Criteria

> Before measuring, define what "good" looks like.

| Criterion | Why It Matters | How to Measure | Target |
|-----------|---------------|----------------|--------|
| Surface correctness | | | |
| Schema quality (tool selection) | | | |
| Trust boundary | | | |
| Reusability (consumers) | | | |

---

## Correctness Evaluation

### Guiding Tests
**`python -m pytest` result:** X / Y passing

### Manual Tool/Resource/Prompt Checks

| Call | Input | Expected | Actual | Pass/Fail |
|------|-------|----------|--------|-----------|
| memory_search | | | | |
| memory_save | | | | |
| read_resource | | | | |
| reflect_on | | | | |

### Failure Patterns
<!-- What inputs cause failures (and should they)? -->

---

## Trust-Boundary Evaluation

| Hostile input | Guard that should stop it | Stopped? |
|---------------|---------------------------|----------|
| `k = 10_000_000` | clamp in `validate_search_args` | |
| 5 MB `text` | cap in `validate_save_args` | |
| `memory://entries/../secret` | `validate_resource_uri` | |
| `file:///etc/passwd` | `validate_resource_uri` | |
| `kind = "rumor"` | whitelist | |

---

## Overall Assessment

**Does it work well enough to ship?** Yes / No / With caveats

**What would need to improve before production?**
1. 
2. 

**What would you measure in production?**
