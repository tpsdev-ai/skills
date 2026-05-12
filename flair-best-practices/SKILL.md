---
name: flair-best-practices
description: Best practices for using Flair as durable agent memory — writing and reading memory, Soul records for identity, federation pairs, memory bridges, MCP integration, and Ed25519 identity. Triggers when an agent needs to persist decisions, recall context, share memory across hosts, or integrate with the broader agent ecosystem.
license: Apache-2.0
metadata:
  author: tpsdev-ai
  version: '0.1.0'
---

# Flair Best Practices

Guidelines for using [Flair](https://github.com/tpsdev-ai/flair) as the long-term memory layer for AI agents. Flair is a Harper-backed memory store with cryptographic identity, federation, and cross-orchestrator portability.

## When to Use

Reference these guidelines when:

- Persisting an agent decision, lesson, or piece of context you want to recall later
- Searching for prior agent knowledge before acting
- Setting up identity for a new agent (Ed25519 keypair, public-key registration)
- Federating memory between hosts (hub-spoke pair)
- Importing memory from other systems (mem0, ChatGPT export, Claude project export)
- Integrating Flair with MCP-aware agents

## Rule Categories

| Priority | Category | Prefix |
| -------- | -------- | ------ |
| 1 | Memory Operations | `memory-` |
| 2 | Soul Records | `soul-` |
| 3 | Identity & Auth | `identity-` |
| 4 | Federation | `federation-` |
| 5 | Bridges & Integrations | `integration-` |

## Quick Reference

### Memory Operations

- `memory-writing-memory` — `writeMemory()`, durability levels (permanent/persistent/standard/ephemeral), tags, subjects
- `memory-reading-memory` — semantic search, tag-based listing, subject groupings, fetch-by-id

### Soul Records

- `soul-when-to-use` — Soul (identity-card-shaped, agent-owned) vs Memory (knowledge-shaped, content-addressable)

### Identity & Auth

- `identity-ed25519-keys` — keypair generation, public-key registration with Flair Agent table, signing requests, key rotation

### Federation

- `federation-pair` — hub-spoke topology, pairing tokens, syncing memories across instances

### Bridges & Integrations

- `integration-mcp` — using `@tpsdev-ai/flair-mcp` for MCP-aware agents (Claude Desktop, Cursor, Continue, etc.)
- `integration-bridges` — `flair bridge import` for mem0, ChatGPT, Claude-project exports

## How to Use

Read individual rule files for detailed explanations and examples:

```
rules/memory-writing-memory.md
rules/memory-reading-memory.md
rules/identity-ed25519-keys.md
rules/integration-mcp.md
```

## Companion Skill

See [`tps-best-practices`](../tps-best-practices/SKILL.md) for agent infrastructure patterns. TPS handles agents; Flair handles their memory. They compose.
