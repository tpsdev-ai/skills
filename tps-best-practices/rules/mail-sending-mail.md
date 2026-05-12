---
name: mail-sending-mail
description: Inter-agent communication via TPS mail — Maildir-shaped, async, persistent, with ack semantics.
---

# Sending Mail Between Agents

TPS mail is the canonical way agents talk to each other. Maildir-shaped on disk; async; persistent; ack'd.

## Anatomy

Each agent has a maildir at `~/.tps/mail/<agent>/`:

```
~/.tps/mail/<agent>/
├── new/         # Inbound messages, unread
├── cur/         # Inbound, opened/being processed
├── tmp/         # Inbound, mid-write (don't read)
├── inbox/       # Legacy inbox (deprecated)
├── outbox/      # Outbound, ready for delivery
└── dlq/         # Dead-letter — undeliverable or rejected
```

A message file is a JSON document:

```json
{
  "id": "uuid",
  "from": "alice",
  "to": "bob",
  "timestamp": "2026-05-12T17:00:00.000Z",
  "subject": null,
  "body": "...",
  "headers": { ... }
}
```

## How to send

```bash
TPS_AGENT_ID=alice tps mail send bob "Hey Bob, can you review PR #123?"
```

Behavior:

- Generates a fresh UUID id
- Writes a `tmp/<filename>.json` first, then atomic-renames to `new/<filename>.json` (avoids partial reads)
- If `bob` lives on a different host, the TPS dispatcher routes via the configured branch-office transport (TCP/WS) or the GAL (Global Address List) entry

## How to receive

Each agent's runtime needs a mail watcher that polls `new/` and emits processable messages:

- **OpenClaw agents** → `openclaw-tps-mail` plugin handles polling + dispatch in-process
- **Custom pi agents** → run `tps mail watch --agent <id>` as a long-lived process, or wire a `tps-mail-watcher.mjs` script in the agent's harness directory
- **One-shot scripts** → `tps mail check <agent>` returns unread, then `tps mail open <id>` moves it to `cur/` + prints body

## Ack semantics

A message is "delivered" once moved out of `new/`. The receiving agent's runtime moves it to `cur/` after processing. If the runtime crashes mid-process, the message is still in `cur/` — agents need to be idempotent on retry.

For dead-letter: if a message can't be processed (malformed, missing fields), move it to `dlq/` and don't retry. A human-or-other-agent sweep will triage.

## Subjects + grouping

`subject` is optional but useful for threading. Reply to a message by reusing its `id` in `headers.in_reply_to`. The receiving agent can group all messages with the same `subject` to recover a conversation.

## Anti-Patterns

- **Writing directly to another agent's `new/`.** Bypasses the dispatcher → no cross-host routing, no signing, no audit. Always use `tps mail send`.
- **Putting secrets in mail body.** Mail files are unencrypted on disk. Use Flair (encrypted memory) for any sensitive context.
- **Polling `cur/` for inbound.** That's the in-process bucket. Always read from `new/`.
- **Forgetting to move processed messages.** Mail piles up in `new/` and eventually trips the per-agent inbox cap. Each runtime's mail watcher should drain.

## See Also

- `agent-creating-an-agent` — creates the maildir tree
- `branch-office-isolation` — cross-host mail routing
