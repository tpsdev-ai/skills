---
name: identity-ed25519-keys
description: Ed25519 keypair generation, public-key registration with Flair, request signing, and key rotation. Every agent that writes to Flair signs with its own key — no shared credentials.
---

# Ed25519 Identity for Flair

Every Flair-writing agent has its own Ed25519 keypair. The private key signs requests; the public key lives in Flair's `Agent` table so the server can verify the signature. No shared admin tokens for agent operations.

## Generate

```bash
# TPS CLI generates + registers in one step:
tps agent create --id myagent --name "My Agent"
```

This writes:

- `~/.tps/identity/myagent.key` — Ed25519 private seed (32 bytes, `chmod 600`)
- `~/.tps/identity/myagent.pub` — public key (32 bytes, encoded base64url)
- `~/.tps/identity/myagent.meta.json` — metadata (creation time, x25519 pair for ECDH if needed)
- A new row in Flair's `Agent` table with `id`, `name`, `publicKey` (base64url, no padding)

## Sign a request

The Flair client constructs an `Authorization` header for every request:

```
Authorization: TPS-Ed25519 <agentId>:<unixSecondsTimestamp>:<nonce>:<base64SignatureNoPad>
```

The signature payload is:

```
<agentId>:<timestamp>:<nonce>:<METHOD>:<path-with-query>
```

The server replays the signature with the registered public key. Mismatch → 401 `invalid_signature`.

If you use `@tpsdev-ai/flair-client`, signing is automatic — just provide `keyPath`. If you use `@tpsdev-ai/flair-mcp`, it's automatic. For raw HTTP, implement the signing shape above.

## Rotate

```bash
tps agent rotate-key --id myagent
```

Behavior:

1. Generate a new keypair into a `~/.tps/identity/myagent.key.new` staging path
2. `PATCH /Agent/<id>` to update the registered publicKey (signed with the OLD key — last legitimate use)
3. Move `.new` → primary; archive old key with timestamp suffix
4. Verify with a `GET /Memory/?agentId=myagent` probe under the new key

If a rotation fails midway, the old key is still good — only the staging copy is dirty. Delete `.new` and retry.

## When public key in Flair diverges from local

Symptom: requests fail with `401 invalid_signature` even though `*.key` and `*.pub` exist locally. Likely cause: the local public key doesn't match what's in `Agent.publicKey`. Diagnose:

```bash
# Local
base64 -i ~/.tps/identity/myagent.pub | tr '+/' '-_' | tr -d '='

# Remote (via admin auth or any other authorized agent)
curl -s "http://127.0.0.1:9926/Agent/myagent" -u "admin:..." | jq -r '.publicKey'
```

If they differ, the agent was likely re-provisioned without re-registering, or the local key file is stale. Re-register via `tps agent re-register --id myagent`.

## Anti-Patterns

- **Sharing a keypair between agents.** Defeats the audit trail and lets any leak compromise multiple agents. One key per agent.
- **Committing `*.key` files to git.** Even private repos. `~/.tps/identity/` should be in `.gitignore` everywhere.
- **Storing the key in env vars.** Process env is visible to other processes via `ps eww`. Stick with the file + `chmod 600`.
- **Using admin auth for agent operations.** Admin auth is for the human operator + bootstrap flows. Agents should sign as themselves.

## See Also

- `memory-writing-memory` — what to write once you have a key
- `integration-mcp` — MCP-aware harness uses the key transparently
