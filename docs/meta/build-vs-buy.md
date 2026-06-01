# Build vs. Buy Decision Framework

Every engineering decision in this lab should be examined through the build vs. buy lens.

## The Core Question

> "Could we solve this with a library, an API, or a managed service — and should we?"

Building is often wrong. Buying is often wrong. **Judgment is always right.**

## The Decision Matrix

| Dimension | Build | Buy |
|-----------|-------|-----|
| Control | Full | Partial |
| Time to value | Slow | Fast |
| Maintenance cost | High | Low (vendor handles it) |
| Learning value | High | Low |
| Customization | Unlimited | Limited |
| Risk | High (you own bugs) | Medium (vendor bugs) |
| Cost at scale | Often lower | Often higher |

## Resource Lens

For every decision, analyze:

- **Engineering Cost** — How long to build? How long to maintain?
- **Maintenance Cost** — What breaks over time? Who fixes it?
- **Infrastructure Cost** — Hosting, compute, storage, bandwidth
- **Opportunity Cost** — What can't you build while building this?
- **Complexity Cost** — How much harder does this make the system to understand?
- **Time To Value** — When does the user benefit?

## When to Build

- The capability is core to your product's differentiation
- No good off-the-shelf solution exists
- You need full control for compliance/privacy reasons
- The learning value justifies the cost (this lab)
- The cost at scale is prohibitive with managed solutions

## When to Buy

- The capability is commodity (auth, storage, queues)
- A managed service exists and is cheap
- Your team lacks the expertise to build it reliably
- Speed to market matters more than control
- Vendor handles compliance burden

## Lab Application

In this lab, we often **build what we could buy** — not because buying is wrong, but because **building teaches you why the bought solution works**.

After building, we always ask:
- "Now that I've built this, when would I reach for the library version?"
- "What does the library do that I didn't implement?"
- "What are the edge cases I missed?"

## Common Mistakes

**Over-building:** Implementing a vector database from scratch when Chroma or Qdrant exist.

**Over-buying:** Using LangChain for a simple chain of 3 LLM calls that 40 lines of Python would handle.

**Not asking the question at all:** Just defaulting to whatever tutorial you read.

## Decision Log

Every non-trivial build-vs-buy decision belongs in `DECISIONS.md` for that project.

Format:
```
## Decision: [Name]
Date: YYYY-MM-DD
Options considered: build / library X / managed service Y
Decision: [what you chose]
Reason: [why]
Tradeoff accepted: [what you gave up]
Revisit if: [conditions that would change this decision]
```
