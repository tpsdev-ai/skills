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
Authorization: TPS-Ed25519 <agentId>:<unixMillisecondsTimestamp>:<nonce>:<base64SignatureNoPad>
```

The signature payload is:

```
<agentId>:<timestamp>:<nonce>:<METHOD>:<path-with-query>
```

The server replays the signature with the registered public key. Mismatch → 401 `invalid_signature`. Timestamp drift outside the window → 401 `timestamp_out_of_window`.

The timestamp is **unix milliseconds** (the value of `Date.now()`), not unix seconds. Off-by-1000x produces immediate `timestamp_out_of_window` rejection.

If you use `@tpsdev-ai/flair-client`, signing is automatic — just provide `keyPath`. If you use `@tpsdev-ai/flair-mcp`, it's automatic. For raw HTTP, implement the signing shape above.

## Key rotation (manual procedure)

TPS CLI does not yet ship a one-shot `agent rotate-key` command. The current-state procedure is:

1. Generate a new keypair into a staging path so the old key keeps working until cutover:
   ```bash
   # Using Node's crypto to mint an Ed25519 seed:
   node -e "
     const c = require('node:crypto');
     const { publicKey, privateKey } = c.generateKeyPairSync('ed25519');
     const seed = privateKey.export({ format: 'der', type: 'pkcs8' }).slice(-32);
     const pub = publicKey.export({ format: 'der', type: 'spki' }).slice(-32);
     require('node:fs').writeFileSync('~/.tps/identity/myagent.key.new'.replace('~', process.env.HOME), seed);
     require('node:fs').writeFileSync('~/.tps/identity/myagent.pub.new'.replace('~', process.env.HOME), pub);
     console.log('pub:', pub.toString('base64').replace(/\\+/g, '-').replace(/\\//g, '_').replace(/=+$/, ''));
   "
   chmod 600 ~/.tps/identity/myagent.key.new
   ```

2. PATCH the `Agent` record in Flair to use the new public key (signed with the OLD key — last legitimate use):
   ```bash
   curl -X PUT "$FLAIR_URL/Agent/myagent" \
     -H "Authorization: TPS-Ed25519 ..." \
     -H "Content-Type: application/json" \
     -d '{"publicKey": "<new-pub-base64url-no-pad>", ...}'
   ```

3. Move the new key into place + archive the old:
   ```bash
   mv ~/.tps/identity/myagent.key ~/.tps/identity/myagent.key.bak-$(date +%Y%m%dT%H%M%S)
   mv ~/.tps/identity/myagent.key.new ~/.tps/identity/myagent.key
   mv ~/.tps/identity/myagent.pub ~/.tps/identity/myagent.pub.bak-$(date +%Y%m%dT%H%M%S)
   mv ~/.tps/identity/myagent.pub.new ~/.tps/identity/myagent.pub
   ```

4. Verify with a `GET /Memory/?agentId=myagent` probe under the new key.

A `tps agent rotate-key` command that wraps this is a planned addition to the TPS CLI but not shipped today.

## When public key in Flair diverges from local

Symptom: requests fail with `401 invalid_signature` even though `*.key` and `*.pub` exist locally. Likely cause: the local public key doesn't match what's in `Agent.publicKey`. Diagnose:

```bash
# Local
base64 -i ~/.tps/identity/myagent.pub | tr '+/' '-_' | tr -d '='

# Remote (via admin auth or any other authorized agent)
curl -s "$FLAIR_URL/Agent/myagent" -u "admin:..." | jq -r '.publicKey'
```

If they differ, the agent was likely re-provisioned without re-registering, OR the local key file is stale, OR the canonical key lives on a different host. Reconciliation: either re-mint the agent record in Flair to match the local key (admin-auth `PUT /Agent/<id>`), or fetch the canonical key from the host that holds it.

## Anti-Patterns

- **Sharing a keypair between agents.** Defeats the audit trail and lets any leak compromise multiple agents. One key per agent.
- **Committing `*.key` files to git.** Even private repos. `~/.tps/identity/` should be in `.gitignore` everywhere.
- **Storing the key in env vars.** Process env is visible to other processes via `ps eww`. Stick with the file + `chmod 600`.
- **Using admin auth for agent operations.** Admin auth is for the human operator + bootstrap flows. Agents should sign as themselves.

## See Also

- `memory-writing-memory` — what to write once you have a key
- `integration-mcp` — MCP-aware harness uses the key transparently
