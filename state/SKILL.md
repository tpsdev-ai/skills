---
name: state
description: Snapshot of in-flight tps work — open PRs (CI + reviews), agent session activity, flint inbox newest, disk pool. Use when the user asks "what's the state", "how's progress", "snapshot", "where are we", "status check", or any variant that wants a current picture of the system.
user-invocable: true
allowed-tools:
  - Bash
  - Read
---

# /state — TPS in-flight snapshot

Produce a tight status snapshot covering open PRs, active agents, recent inbox, disk pool. Aim for ≤200 words. Lead with anything red. End with one suggested next move if obvious, else "no immediate action."

## What to gather

Run these in parallel via Bash, then synthesize:

```bash
# Open PRs
gh-as flint pr list --repo tpsdev-ai/flair --state open --json number,headRefName,statusCheckRollup,reviews,title 2>&1 | jq -c '.'
gh-as flint pr list --repo tpsdev-ai/cli --state open --json number,headRefName,statusCheckRollup,reviews,title 2>&1 | jq -c '.'

# Agent sessions (latest jsonl mtime → "active in last X min" or "idle since Y")
ssh tps-anvil 'ls -lat /home/exedev/.openclaw/agents/anvil/sessions/*.jsonl 2>/dev/null | head -1'
ls -lat /Users/squeued/agents/ember/.pi-agent/sessions/--Users-squeued-agents-ember-work-flair--/*.jsonl 2>/dev/null | head -1
ls -lat /Users/squeued/.openclaw/agents/kern/sessions/*.jsonl 2>/dev/null | head -1
ls -lat /Users/squeued/.openclaw/agents/sherlock/sessions/*.jsonl 2>/dev/null | head -1

# Flint inbox newest 3
ls -lat ~/.tps/mail/flint/new/*.json 2>/dev/null | head -3
for f in $(ls -t ~/.tps/mail/flint/new/*.json 2>/dev/null | head -3); do
  jq -r '"\(.from): \(.body[0:100])"' "$f" 2>/dev/null
done

# Disk pool (pool cap is 25GB combined across all VMs per Nathan 2026-04-29)
ssh tps-anvil 'df -h / | tail -1'
ssh pulse.exe.xyz 'df -h / | tail -1'
```

## Output format

One short section per active surface, bold-leading any RED:

- **PRs:** `#NUM [branch] CI X/Y · K&S verdicts · headline`. Skip green-and-approved-and-mergeable; just say "#310 ready to merge" if all gates met.
- **Agents:** `Anvil/Ember/Kern/Sherlock` — active <5 min ago / idle for X min. If session.ended or context-overflow recently, say so.
- **Inbox:** newest 3, prefixed with sender and 1-line gist.
- **Disk:** combined as `X.X / 25 GB (NN%)`. Flag if >85%.

Then a one-line suggested next move ("ping Kern on #310; merge once approved"; "ops-got7 PR-A awaiting Sherlock re-review on f4fb5908"; etc).

## Why this skill exists

Flint manually composes this snapshot 5+ times per session. It's the "where are we" query Nathan asks frequently and it's the implicit context-load whenever a new question comes in. Compounding payoff: lower latency on every status check, fewer missed signals (saved by the don't-go-silent feedback memory).
