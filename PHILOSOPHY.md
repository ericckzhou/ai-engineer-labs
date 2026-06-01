# Philosophy

This document states what we believe. It does not prescribe what Claude must do — that is OPERATING_RULES.md.

---

## About the Learner

The goal is not to become an AI researcher.

The goal is to become an **AI Systems Engineer** — someone who can build AI products, start AI companies, design AI architectures, and ship things that work.

Researchers discover new truth. Engineers use existing truth to build things. Both matter. This lab is for engineers.

## About Learning

Understanding precedes implementation. Implementation precedes judgment. Judgment precedes architecture.

You do not understand a concept until you can:
1. Explain it simply to someone who knows nothing
2. Build something with it
3. Break it and explain why it broke
4. Evaluate whether it worked

Terminology is not understanding. Being able to define "cosine similarity" is not the same as knowing when to use it and when to use something else.

## About Sources

Truth lives in primary sources.

A concept is only as reliable as its source. Model memory is not a source. A blog post recapitulating another blog post is not a source. The original paper, the official documentation, the engineering team's own account — those are sources.

We prefer:
1. Official documentation
2. Foundational papers
3. Engineering blogs from the teams who built it
4. Educational resources grounded in the above

We do not prefer:
- Model-generated explanations without citation
- Tutorial sites that don't cite originals
- "Common wisdom" without evidence

## About Evaluation

You cannot improve what you cannot measure.

Every project in this lab requires evaluation — quantitative, honest, uncomfortable when necessary. The evaluation criteria are defined before implementation, not after.

A demo that works is not evidence. A benchmark that passes specific cases is evidence. The difference matters.

## About Complexity

The right amount of complexity is the minimum that solves the problem.

Adding a framework because it exists is wrong. Adding an agent because agents are exciting is wrong. Adding abstraction because you might need it someday is wrong.

Every layer of complexity has a cost: debugging time, onboarding time, cognitive load, failure surface. Those costs are real even when they're invisible.

Ask before adding anything:
- What breaks if I don't add this?
- Is there a simpler solution?
- Am I solving a real problem or an imagined one?

## About Memory

Memory is personal. Sources are universal.

The learner's reflections, misconceptions, and growth are stored in memory. They inform how instruction is personalized. They do not override what is true in sources.

A learner who believed something wrong, learned the right thing, and documented the transition — that's valuable memory. That record doesn't change what the source says. It changes how we teach it next time.

## About StarcallOS

StarcallOS is the north star, not the immediate destination.

Every project in this lab is independent. Every project teaches something real. But every project also asks: "How does this change how I think about StarcallOS?"

The goal is to discover patterns through building, not to prototype StarcallOS components directly. The most valuable discoveries are the ones you couldn't have planned in advance.

## The Core Rule

```
Sources establish truth.
Docs teach truth.
Projects apply truth.
Memory records what changed in the learner.
```

No layer below overrides a layer above.
Memory can personalize instruction. Memory cannot establish truth.
