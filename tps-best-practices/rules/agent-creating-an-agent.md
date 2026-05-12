---
name: agent-creating-an-agent
description: Provisioning a new agent in TPS — generates Ed25519 identity, registers in Flair, writes the agent config.
---

# Creating an Agent

`tps agent create` is the one-shot command. It handles identity, Flair registration, and config.

## How

```bash
tps agent create --id <id> --name "<Display Name>" --model "<provider>/<model>"
```

Example:

```bash
tps agent create --id alice --name "Alice" --model "ollama-cloud/deepseek-v4-pro"
```

What this does:

1. Generates an Ed25519 keypair → `~/.tps/identity/alice.{key,pub,seed}`
2. Generates an x25519 pair for ECDH (used by some plugins) → `~/.tps/identity/alice.x25519.{key,pub}`
3. Registers `alice` in the Flair `Agent` table (id, name, publicKey, role, createdAt)
4. Writes config to `~/.tps/agents/alice/agent.yaml`
5. Creates the maildir tree at `~/.tps/mail/alice/{new,cur,tmp,inbox,dlq,outbox}`

After this, `alice` is ready to send/receive mail and write to Flair as herself.

## Provider/model

Common choices:

| Provider | Models | Notes |
|---|---|---|
| `anthropic` | `claude-opus-4-7`, `claude-sonnet-4-6`, `claude-haiku-4-5` | Cloud, paid |
| `google` | `gemini-3-flash-preview`, `gemini-2.5-flash` | Cloud, requires API key |
| `ollama-cloud` | `deepseek-v4-pro`, `kimi-k2.6:cloud` | Cloud, paid, ollama-shaped |
| `ollama` | any local model | Local, free, host-dependent |
| `omlx` | Apple-MLX models | Local, Mac-only |

The agent config keeps `provider` + `model` as the LLM target. The runtime (Claude Code, OpenClaw, pi, etc.) consumes this; switch runtime by editing config or by passing `--runtime` to `tps agent start`.

## What's NOT done automatically

- **Soul not written.** Use `tps soul set --agent alice --key identity --value "..."` to give the agent a persona.
- **Runtime not started.** Run `tps agent start --id alice` (long-running) or `tps agent run --id alice --message "..."` (one-shot) to invoke.
- **Mail watcher not enabled.** If the agent should respond to inbound mail asynchronously, set up a mail watcher via the appropriate runtime's mail plugin (`openclaw-tps-mail` for OpenClaw, custom watcher for pi).
- **Skills not registered.** Use `tps skill register` or `tps skill add-pack` to give the agent skill files.

## Anti-Patterns

- **Re-creating an existing agent.** `tps agent create` won't overwrite. To rotate identity, use `tps agent rotate-key`. To fully decommission + recreate, `tps agent decommission --id <id>` first.
- **Generating an identity offline + uploading separately.** The combined `tps agent create` flow keeps the local key + Flair Agent record in sync. Splitting them risks mismatch (the most common cause of `401 invalid_signature`).

## See Also

- `mail-sending-mail` — first thing the new agent will need to do
- `flair-best-practices/identity-ed25519-keys` — key format + rotation
- `flair-best-practices/soul-when-to-use` — what to write as Soul once the agent exists
