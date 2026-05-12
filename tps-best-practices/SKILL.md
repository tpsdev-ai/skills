---
name: tps-best-practices
description: Best practices for working with TPS (Team Provisioning System) — agent provisioning, inter-agent mail, skill governance, branch-office isolation, and runtime providers. Triggers on tasks involving multi-agent coordination, agent identity setup, mail routing, sandboxing, or skill management.
license: Apache-2.0
metadata:
  author: tpsdev-ai
  version: '0.1.0'
---

# TPS Best Practices

Guidelines for building and operating multi-agent systems with [TPS](https://github.com/tpsdev-ai/cli). TPS provides the primitives for agents to exist (identity), discover each other (roster), communicate (mail), run in sandboxes (branch offices), and load knowledge (skills).

## When to Use

Reference these guidelines when:

- Provisioning a new agent (identity, soul, config)
- Setting up mail-based coordination between agents
- Registering or governing skills for agents
- Configuring branch-office sandboxing with nono
- Plugging an external runtime (Claude Code, Codex, OpenClaw, etc.)

## Rule Categories

| Priority | Category | Prefix |
| -------- | -------- | ------ |
| 1 | Agent Lifecycle | `agent-` |
| 2 | Inter-Agent Communication | `mail-` |
| 3 | Skill Governance | `skill-` |
| 4 | Isolation & Sandboxing | `branch-` |
| 5 | Runtime Integration | `runtime-` |

## Quick Reference

### Agent Lifecycle

- `agent-creating-an-agent` — `tps agent create`, identity, soul, config defaults

### Inter-Agent Communication

- `mail-sending-mail` — Maildir shape (new/cur/tmp/dlq/outbox), `tps mail send`, ack semantics

### Skill Governance

- `skill-installing-skills` — `tps skill register` for single skills, `tps skill add-pack` for npm-shipped skill packs, 8KB cap, security scan

### Isolation & Sandboxing

- `branch-office-isolation` — Four-layer sandboxing model (Docker → Linux users → nono Landlock → BoundaryManager)

### Runtime Integration

- `runtime-providers` — Plugging Claude Code, Codex, OpenClaw, or custom runtimes via OAuth-based credential bridging

## How to Use

Read individual rule files for detailed explanations and examples:

```
rules/agent-creating-an-agent.md
rules/mail-sending-mail.md
rules/skill-installing-skills.md
```

## Companion Skill

See [`flair-best-practices`](../flair-best-practices/SKILL.md) for memory + identity-aware persistence patterns. TPS handles agent infrastructure; Flair handles agent memory. They compose.
