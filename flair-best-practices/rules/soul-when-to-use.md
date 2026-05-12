---
name: soul-when-to-use
description: When to use a Soul record (identity-shaped, key-addressable, agent-owned) vs a Memory record (knowledge-shaped, content-addressable, searchable).
---

# Soul vs Memory

Flair has two record types. Choosing the right one matters for findability and lifecycle.

## Soul

**Shape**: `(agentId, key, value)`. Keyed lookup, one value per `(agent, key)` pair. Mostly write-once-read-many. The agent's identity card.

**Use for**:

- `agent_id` + `key=identity` — the agent's persona, role, voice (e.g., the "you are X" system-prompt content)
- `agent_id` + `key=workspace-rules` — durable behavioral rules ("always commit before deactivating")
- `agent_id` + `key=user-context` — the user's preferences as the agent has come to understand them

**Loaded by**: bootstrap. The openclaw-flair plugin and the Flair MCP server inject Soul entries directly into the agent's context at session start, by key. Not searched.

```ts
await flair.setSoulEntry({ agentId: "myagent", key: "identity", value: "..." });
const identity = await flair.getSoul("myagent", "identity");
```

## Memory

**Shape**: `(id, agentId, content, type, durability, tags, subject, ...)`. Content-addressable + searchable. Many entries per agent, with semantic search and tag filters.

**Use for**:

- Incident write-ups, decisions made, gotchas discovered
- Per-task context the agent wants to recall later by topic
- Cross-agent shared knowledge (any agent can search the others' memories)

**Loaded by**: explicit query — `search()`, `listMemories()`, or `getMemory(id)`. Not auto-injected at boot (too many entries).

```ts
await flair.writeMemory("myagent-uuid", "...", { tags: ["..."], subject: "..." });
const results = await flair.search("query", { agentId: "myagent" });
```

## Quick decision tree

| Question | Answer | Use |
|---|---|---|
| Is this part of *who the agent is* (role, voice, rules)? | Yes | Soul |
| Is this *something the agent learned* (incident, gotcha, decision)? | Yes | Memory |
| Does it need to load on every session? | Yes | Soul |
| Will agents search for this later? | Yes | Memory |
| Is there *one canonical value* for a key? | Yes | Soul |
| Will there be many of these over time? | Yes | Memory |

## Anti-Patterns

- **Putting big knowledge dumps in Soul.** Soul should be small, loadable, identity-shaped. Knowledge goes in Memory.
- **Putting identity rules in Memory.** They won't auto-load; the agent may not search for them when needed.
- **Soul with versioning.** Soul is single-value-per-key by design. If you need version history, use Memory with `subject:agent-identity-v1` etc.
- **Writing the same Soul entry from multiple agents.** Each agent owns its own Soul space.

## See Also

- `memory-writing-memory` / `memory-reading-memory` — Memory operations
- `identity-ed25519-keys` — auth for both Soul and Memory writes
