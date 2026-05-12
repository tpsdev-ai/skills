---
name: memory-reading-memory
description: How to find and load memory from Flair — semantic search, tag-based listing, subject groupings, and bootstrap-time recall.
---

# Reading Memory from Flair

## How

### Semantic search (vector)

```ts
const results = await flair.search("postgres deadlock fix", { agentId: "myagent", limit: 5 });
```

Returns ranked matches against memory content. Best when you have a phrase that describes what you want but not exact tags.

### Tag-based listing

```ts
const incidents = await flair.listMemories({
  agentId: "myagent",
  tags: ["kind:incident", "topic:database"],
  limit: 20,
});
```

Best when you know the category. Pair tags with `kind:` to filter sharply.

### Subject grouping

```ts
const allAboutThisIssue = await flair.listMemories({
  subject: "postgres-deadlock-on-uniqueness-checks",
});
```

Returns every memory ever written about one issue. Useful for postmortem context.

### Fetch by ID

```ts
const memory = await flair.getMemory("myagent-<uuid>");
```

Direct lookup. Useful when you have an ID from a prior search or a referenced memory.

### MCP equivalent

In an MCP-aware agent, `flair.memory.search` / `flair.memory.list` / `flair.memory.get` are available as tools. Same parameters; the model picks the right one for the question.

## Bootstrap-time recall

When an agent starts a new session or new task, the recommended pattern is:

1. Search for `tags:kind:identity` to load the agent's own behavioral rules
2. Search for the task topic to surface prior relevant memories
3. Inject the top N (5–20) into context as a system message

The `@tpsdev-ai/openclaw-flair` plugin does this automatically for OpenClaw agents. Claude Code agents typically rely on a local `MEMORY.md` shortlist that points at Flair entries by ID for deeper context.

## Anti-Patterns

- **Searching for exact phrases without using tags.** Semantic search is fuzzy by design. If you need exact matches, use tag filters or subject groupings.
- **Loading every memory at session start.** Flair will happily return thousands of memories; your context window won't fit them. Score, limit, summarize.
- **Treating search results as truth.** A 0.8-score match is a *candidate* — read it before acting. Confidence is fuzzy.
- **Forgetting that memories age.** A 6-month-old "always do X" rule may have been superseded. Check `createdAt` + `lastRetrieved` before relying on a memory blindly.

## See Also

- `memory-writing-memory` — write patterns
- `soul-when-to-use` — Soul records load differently (always-on by ID, not searched)
