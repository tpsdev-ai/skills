---
name: intel-gathering
description: Best practices for agents that periodically gather external intelligence — GitHub releases, vendor changelogs, RSS/atom feeds — for briefings, monitoring, or trend detection. Triggers when an agent's job involves pulling fresh state from third-party sources (e.g., an EA composing a morning brief, a research agent watching tooling announcements).
license: Apache-2.0
metadata:
  author: tpsdev-ai
  version: '0.1.0'
---

# Intel Gathering

Guidelines for agents that poll external sources — GitHub releases, vendor changelogs, blog feeds — and surface what changed. Most often this is a daily/hourly cron, but the patterns apply to any agent doing periodic external reads.

The goal: get reliable, authenticated reads with respectful poll cadences, without leaking tokens or burning rate limits.

## When to Use

Reference these guidelines when:

- Building an EA agent that composes a morning brief from external sources
- Wiring an agent to track new releases of dependencies your team uses
- Watching vendor release notes (Anthropic, Google, OpenAI, etc.) for changes that affect your stack
- Any periodic-poll workload where the agent reads from an HTTP source it doesn't control

## Rule Categories

| Priority | Category | Prefix |
| -------- | -------- | ------ |
| 1 | Authentication | `auth-` |
| 2 | Known-good Sources | `feeds-` |
| 3 | Polling Discipline | `polling-` |

## Quick Reference

### Authentication

- `auth-github-pat` — Read GH_TOKEN from a 0600 secret file in the agent launcher; 60/hr → 5000/hr rate-limit ceiling

### Known-good Sources

- `feeds-vendor-changelogs` — Verified-working atom/RSS endpoints for Anthropic, Google Gemini, GitHub releases; documented 404s and HTML-scrape fallbacks
- `feeds-github-releases` — `<owner>/<repo>/releases.atom` is the universal pattern; works for any public repo

### Polling Discipline

- `polling-cadence-and-caching` — Default cadences, ETag/If-Modified-Since usage, on-disk cache layout

## How to Use

Read individual rule files for detailed explanations and examples:

```
rules/auth-github-pat.md
rules/feeds-vendor-changelogs.md
rules/feeds-github-releases.md
rules/polling-cadence-and-caching.md
```

## Companion Skills

- [`tps-best-practices`](../tps-best-practices/SKILL.md) — agent infrastructure (provisioning, mail, sandboxing)
- [`flair-best-practices`](../flair-best-practices/SKILL.md) — persist findings to durable memory so the agent doesn't re-discover the same release tomorrow
