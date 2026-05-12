---
name: federation-pair
description: Setting up a Flair hub-spoke federation pair so memory written on one instance propagates to others. Useful for multi-host teams or laptop-to-cloud sync.
---

# Federation Pair

A federation pair is a one-directional sync from a Flair *spoke* (your local instance) to a *hub* (typically Fabric or another shared host). Memory written on the spoke flows to the hub automatically; agents on either side can read either's data.

## Topology

```
[local spoke] ──sync──> [hub on Fabric]
                              ▲
                              │
[another spoke] ──sync────────┘
```

Each spoke writes to its own instance. The hub aggregates. Reads can come from either side — agents typically search their local spoke first (fast), then federate to hub for cross-host context.

## Pair setup

On the **hub**, generate a pairing token:

```bash
flair federation token --label "<spoke-name>" --ttl 1h
# Returns: a single-use token, valid for 1 hour
```

On the **spoke**:

```bash
FLAIR_ADMIN_PASS=$(cat ~/.flair/admin-pass) \
  flair federation pair https://flair.example.com --token <token>
```

This:
1. Authenticates to the hub with the token
2. Receives the hub's identity (Ed25519 pubkey)
3. Inserts a Peer record in the spoke's local DB
4. Starts the background sync watcher

## Verify

```bash
flair federation list   # Shows peers + last sync time
flair federation sync   # One-shot sync trigger (otherwise periodic)
```

## What syncs

By default: all Memory records with `durability >= persistent`. Soul records (per-agent identity cards) sync only if the agent's `syncSoul` flag is set in their Agent record.

## Anti-Patterns

- **Pairing a spoke to multiple hubs.** Conflicts on cross-hub writes. Pick one hub per spoke; if you need multi-hub, design an explicit per-tag routing layer.
- **Long-lived pairing tokens.** Tokens are one-use by design. If you need to re-pair, mint a fresh token.
- **Skipping the hub's Peer write permission check.** The hub must allow the spoke to create Peer + Memory records. See `identity-ed25519-keys` for the auth shape.

## See Also

- `memory-writing-memory` — writes go to the local spoke; sync handles propagation
- `identity-ed25519-keys` — both sides authenticate via their own keys
