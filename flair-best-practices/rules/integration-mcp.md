---
name: integration-mcp
description: How to wire Flair into MCP-aware agents (Claude Desktop, Cursor, Continue, Windsurf, Zed) so memory operations are native tools the agent can call.
---

# Flair via MCP

If your agent harness speaks [Model Context Protocol](https://modelcontextprotocol.io), `@tpsdev-ai/flair-mcp` exposes Flair's memory/soul/agent operations as MCP tools. No language SDK, no CLI in the loop — the agent calls tools by name.

## Install

```bash
npm install -g @tpsdev-ai/flair-mcp
```

## Configure

Add to your MCP server config (varies per host):

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "flair": {
      "command": "npx",
      "args": ["-y", "@tpsdev-ai/flair-mcp"],
      "env": {
        "FLAIR_URL": "http://127.0.0.1:9926",
        "FLAIR_AGENT_ID": "myagent",
        "FLAIR_KEY_PATH": "/Users/you/.tps/identity/myagent.key"
      }
    }
  }
}
```

**Cursor, Continue, Windsurf, Zed** all use a similar pattern; consult your host's MCP docs for the exact path.

## Tools Available

Once connected, the agent has these tools to call:

- `flair.memory.write` — persist a memory
- `flair.memory.search` — semantic search
- `flair.memory.list` — tag/subject filter
- `flair.memory.get` — fetch by ID
- `flair.soul.get` — load an agent's soul card
- `flair.soul.set` — update a soul entry
- `flair.agent.list` — discover other agents
- `flair.bootstrap` — fetch the agent's startup context

The MCP server handles the Ed25519 signing internally — the agent never sees the key.

## Multi-Agent Setup

If multiple agents on the same host share an MCP-aware harness, configure separate MCP server entries — one per agent identity:

```json
"flair-flint": { ..., "env": { "FLAIR_AGENT_ID": "flint" } },
"flair-kern":  { ..., "env": { "FLAIR_AGENT_ID": "kern"  } }
```

Each instance signs with its own key. The agent picks which "flair-*" tool to use.

## Anti-Patterns

- **Sharing one identity across agents.** Defeats the audit trail. One identity per agent.
- **Embedding the keypair in the MCP config.** Use `FLAIR_KEY_PATH` to a file with `chmod 600`. Config files are often synced to cloud (Mac Settings sync, dotfiles repos).
- **Hardcoding a remote `FLAIR_URL` without TLS.** Plain HTTP only on `127.0.0.1` / `localhost`. For Fabric or other remote instances, always `https://`.

## See Also

- `identity-ed25519-keys` — key generation and rotation
- `memory-writing-memory` — what to write once tools are available
