---
name: quality-no-unverified-claims
description: Never claim a feature, integration, or roadmap state as current unless you've verified it. The risk is high for any prose touching public surfaces (blog, README, landing page, docs) — a single hallucinated claim damages credibility.
---

# Don't Claim What You Haven't Verified

## The rule

Before writing that Flair (or any of our products) does X, has X, or supports X — verify X. The acceptable forms of evidence:

1. **The code exists and ships.** A function, an endpoint, a CLI command, a config option. You can `grep` for it and find it.
2. **The integration tests pass.** Not just the unit tests — actual cross-process verification.
3. **A merged PR with the claim in the title or description.** Implied: it landed and isn't reverted.
4. **A specific public fact you can cite.** E.g. "Apache 2.0 license" is verifiable in `LICENSE`.

Anything weaker — "we're planning to", "we're working on", "soon we'll have", "is being extended to" — does NOT belong in prose for public surfaces unless explicitly framed as future/roadmap.

## Anti-pattern: the helpful-extrapolation hallucination

The most common form: you know about Feature A. You know about Vendor B. You write "we extend Feature A to Vendor B" without verifying that integration actually exists. Sometimes the bridge is real, sometimes you've inferred it from adjacent capabilities.

Concrete example from 2026-05-12: gemma-4-31b draft v2 of "What is Flair?" wrote:

> We are extending this federation to GCP and AWS, allowing you to distribute your agent's memory across clouds without sacrificing ownership.

That sentence is plausible. Federation is real, GCP/AWS deployments are a thing, "extending to" is a common phrasing. But the actual GCP work is a 30-minute spike (`task #54: GCP/ADK 30-min spike — plugin contract`), not a production roadmap commitment. The sentence implies we have a near-term GCP/AWS federation product. We don't.

The error class: the model knows the *shape* of a thing companies say at this stage, and helpfully generates that shape — without checking whether the specific claim maps to real work.

## How to apply

When you're drafting prose for any public-facing surface:

1. **Make a claim ledger.** Before writing the final draft, list every product claim the prose makes. Each one needs evidence.
2. **For each claim, ask: "is this verifiable today?"** If not, either remove the claim or reframe it ("planned", "in design", "spike in progress").
3. **Prefer specific to general.** "We dogfood across six agents" (verifiable) beats "we use it heavily" (vague, no evidence required).
4. **When unsure, ask.** "Do we actually do X?" sent to Flint or whoever owns the area is cheap. A hallucinated public claim is expensive.
5. **For roadmap claims, add a temporal qualifier and a status word.** "By Q3, we plan to ship the X integration (currently a spike)." Now the reader knows what they're reading.

## Red flags in your own drafts

- Compound claims joining a real thing to an aspirational thing: "we support A, B, and C [where C is not yet shipped]"
- Forward-looking verbs without a status qualifier: "extends", "now supports", "is being rolled out to" → ask: is the rollout actually in flight?
- Lists of integrations or capabilities — easy to add an extra item that sounds plausible. Cross-check every entry.
- Geographic / cloud / vendor coverage claims — these are commonly hallucinated because they sound natural to write.
- Counts and quantities that aren't sourced from a script or a doc — "11 integrations", "supports X languages", etc. Verify the count.

## When you make a mistake

If a claim ships and is later found to be wrong:

1. Correct it immediately — don't let the wrong claim stay public.
2. Note the hallucination class in a memory or skill rule (this one).
3. Do not blame "the model" generically. Identify the specific shape of the over-extrapolation so the next instance is easier to catch.

## Related disciplines

The same standard applies to claims about *external* tools and vendor behavior — verify with a repro before asserting. And when a fix is actually a workaround for someone else's bug, name it as a workaround in sentence one, not framed as the root-cause fix.
