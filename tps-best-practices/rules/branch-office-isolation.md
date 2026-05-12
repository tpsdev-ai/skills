---
name: branch-office-isolation
description: Four-layer sandboxing model for agents running in TPS branch offices — Docker containers, Linux users, nono Landlock, and BoundaryManager.
---

# Branch-Office Isolation

TPS provides multiple isolation layers for agents that need stronger boundaries than process-level. Use when:

- Agent runs code from third-party sources (PR diffs, untrusted skills)
- Agent has access to credentials or network paths you don't want compromised
- Multi-tenant: multiple agents share a host but should not see each other

## The four layers

| Layer | Mechanism | What it bounds |
|---|---|---|
| 1. **Docker container** | `docker-compose.yml` per agent | Filesystem root, process namespace, kernel features |
| 2. **Linux user** | Distinct uid per agent inside container | UID-based filesystem ACLs, process visibility |
| 3. **nono Landlock** | `tps-agent-run.toml` (nono profile) | Per-process read/write/exec allowlist (Linux kernel Landlock) |
| 4. **BoundaryManager** | TPS runtime guard | Wraps tools the agent calls, enforces tps-mail-only inter-agent comm |

The default profile (`packages/cli/nono-profiles/tps-agent-run.toml`) is conservative: filesystem read-only except `~/.tps/` + `~/ops/`; localhost-only network; exec allowlist of git/bun/node.

## Branch office init

```bash
# On a host that will run a remote agent
tps branch init --port 9090 --transport ws
tps branch start
```

This spawns a long-running daemon that:
- Listens for inbound mail from other TPS hosts (via WS or TCP)
- Drains the outbox to the connected hub
- Manages per-agent maildirs

Branch offices are network endpoints. The agent itself runs *inside* the branch office via the chosen runtime (Claude Code, OpenClaw, etc.).

## When to use which layer

- **Local development, trusted single-user host**: skip Docker; rely on nono profile only
- **Multi-agent shared host**: layer 1 (Docker) + layer 3 (nono) — Docker for namespace isolation, nono for fs/network constraints
- **High-security agent (touches secrets, untrusted input)**: all four — full Docker, distinct uid, nono profile, BoundaryManager

## Anti-Patterns

- **Running an agent on host as root.** Defeats every layer.
- **Mounting `~/.tps/secrets/` into a branch office.** Agents should never see other agents' secrets. Each agent gets only its own subdir.
- **Allowing arbitrary network in nono profile.** Default deny; allow specific hosts (localhost, your LLM proxy, your GitHub mirror).

## See Also

- `agent-creating-an-agent` — create the agent first
- `runtime-providers` — pluggable runtimes that live inside branch offices
