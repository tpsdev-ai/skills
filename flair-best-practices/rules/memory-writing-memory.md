---
name: memory-writing-memory
description: How to write durable memory to Flair, with the right durability level, tags, and subject.
---

# Writing Memory to Flair

Flair memory is the durable, federated record of agent decisions and lessons. Write a memory when:

- You resolved an incident and want future-you to know the cause + fix
- You found a non-obvious gotcha or pattern that should propagate to other agents
- You made a decision worth defending later
- A user (or another agent) corrected you on something

## How

### Via the JS/TS client

```ts
import { createFlairClient } from "@tpsdev-ai/flair-client";

const flair = createFlairClient({
  agentId: "myagent",
  baseUrl: "http://127.0.0.1:9926",
  keyPath: "~/.tps/identity/myagent.key",
});

await flair.writeMemory(`myagent-${crypto.randomUUID()}`, content, {
  type: "reference",
  durability: "persistent",
  tags: ["source:incident-2026-05-12", "kind:operational", "topic:database"],
  subject: "postgres-deadlock-on-uniqueness-checks",
});
```

### Via the CLI

```sh
tps memory write "<content>" \
  --type reference \
  --durability persistent \
  --tags source:incident-2026-05-12,kind:operational \
  --subject postgres-deadlock-on-uniqueness-checks
```

### Via MCP (Claude Desktop, Cursor, etc.)

If `@tpsdev-ai/flair-mcp` is installed in your MCP server config, you have a `flair.memory.write` tool available. Same shape; the agent calls it directly mid-turn.

### Via raw HTTP

```sh
curl -X PUT "http://127.0.0.1:9926/Memory/$(uuidgen)" \
  -H "Content-Type: application/json" \
  -H "Authorization: TPS-Ed25519 <agentId>:<timestamp>:<nonce>:<sig>" \
  -d '{"content": "...", "type": "reference", "durability": "persistent", "tags": ["..."]}'
```

## Durability Levels

| Level | Lifetime | Use For |
|---|---|---|
| `permanent` | Never auto-archived | Identity-level constants, business invariants |
| `persistent` | Default — kept until explicitly archived | Operational rules, incident lessons, design decisions |
| `standard` | Auto-archive after 30 days | Working notes, transient observations |
| `ephemeral` | Auto-archive after 7 days | Debug breadcrumbs, scratch work |

Default to `persistent` for any memory worth writing. Use `permanent` sparingly — every entry there is a long-term commitment.

## Tags Convention

Tags are the primary search-and-filter surface. Conventions that compose well:

- `source:<context>` — e.g., `source:incident-2026-05-12`, `source:onboarding`, `source:user-feedback`
- `kind:<category>` — e.g., `kind:operational`, `kind:design`, `kind:incident`, `kind:correction`
- `topic:<domain>` — e.g., `topic:database`, `topic:auth`, `topic:deploy`
- `from:<entity>` — e.g., `from:user`, `from:reviewer`, `from:postmortem`

Tags are case-sensitive. Use kebab-case within values. Keep the count small (3–5 per memory).

## Subject

The `subject` field groups related memories. A query for `subject:postgres-deadlock-on-uniqueness-checks` returns every memory written about that one issue. Use a slug-shaped subject (lowercase, hyphens, no spaces). Reuse across related writes.

## Anti-Patterns

- **Writing the same memory to multiple agents.** Tag it instead. A memory written by `flint` with `topic:database` is searchable by `kern` if both share the Flair instance.
- **Putting secrets in memory content.** Flair memory is encrypted at rest, but treat it like a public-ish substrate — never write passwords, tokens, or PII.
- **Skipping `type`.** Defaulting `type` to `reference` is fine for most cases; only override if the surface (Soul, AgentSeed, etc.) calls for something else.
- **Forgetting to write.** Memory you didn't write doesn't exist. If a future-you would benefit from knowing this, write it now.

## See Also

- `memory-reading-memory` — search and retrieval patterns
- `soul-when-to-use` — Soul records vs Memory records
- `integration-mcp` — using Flair from MCP-aware agents
