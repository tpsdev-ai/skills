---
name: runtime-providers
description: How to plug agent runtime providers (Claude Code, Codex, Gemini CLI, OpenClaw, pi) into TPS via OAuth-based credential bridging — no API keys held by the agent.
---

# Runtime Providers

TPS abstracts the LLM runtime so each agent can run on its preferred backend without holding API keys directly. Supported today:

| Runtime | Source | Auth Pattern |
|---|---|---|
| Claude Code (CLI) | `claude` binary, Anthropic | OAuth via `claude auth login`; TPS reads the local token |
| Codex (CLI) | OpenAI Codex CLI | OAuth via `codex auth`; same pattern |
| Gemini CLI | Google's Gemini CLI | OAuth via `gcloud auth` |
| OpenClaw | `openclaw` gateway, multi-provider | Per-agent `auth-profiles.json` |
| pi | Lightweight harness | Direct API key in env (per-process scope) |

## How TPS plugs them in

Each agent's `~/.tps/agents/<id>/agent.yaml` declares the runtime:

```yaml
agentId: alice
runtime: claude-code     # or: openclaw, codex, gemini, pi
llm:
  provider: anthropic     # informational
  model: claude-opus-4-7  # informational; runtime decides what it can use
```

When `tps agent start --id alice` runs, the chosen runtime is invoked with credentials sourced from:

- For CLI runtimes (claude/codex/gemini): the runtime picks up its OAuth token from a standard local credential file (e.g., `~/.claude/.credentials.json` for Claude Code) — each agent's wrapper should point at an *agent-specific* credential file (not a shared one — see "OAuth chain isolation" below)
- For openclaw: the agent's `auth-profiles.json` (per-agent, per-provider)
- For pi: API key from env var (`OLLAMA_API_KEY`, etc.), supplied by the wrapper script

## OAuth chain isolation

For CLI runtimes (Claude Code, Codex), each agent should get an *independent* OAuth chain. Sharing one Keychain entry across agents means all agents can be impersonated if one is compromised.

Pattern: each agent has its own `claude` (or equivalent) credential file at `~/.tps/agents/<id>/credentials/`. The runtime wrapper sets `XDG_CONFIG_HOME` or similar to point the CLI at the per-agent dir.

## Anti-Patterns

- **Sharing one OAuth chain across multiple agents.** Defeats per-agent audit + multiplies leak blast radius.
- **Storing the API key in `agent.yaml`.** Config files are commit candidates. Secrets go in `~/.tps/secrets/<scope>` with `chmod 600`.
- **Running multiple runtimes concurrently in one agent process.** Pick one per agent; switch by reconfiguring + restarting.

## See Also

- `agent-creating-an-agent` — runtime is chosen at create-time
- `branch-office-isolation` — runtimes execute inside branch offices
