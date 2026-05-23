---
name: polling-cadence-and-caching
description: Default poll cadences, ETag/If-Modified-Since usage, and on-disk cache layout for intel-gathering agents. Keeps you off vendor rate-limit radar and inside GitHub's 5000/hr budget.
---

# polling-cadence-and-caching

The 5000/hr GitHub budget (see [`auth-github-pat`](auth-github-pat.md)) sounds generous until you watch 50 repos every 5 minutes — that's 36,000 requests/day. Treat the cadence as a real budget, and cache aggressively so most polls return 304 with no body.

## Default cadences

| Source type | Cadence | Reason |
|---|---|---|
| Vendor changelogs (Anthropic API, Gemini blog) | 1×/hour | Vendors publish on business hours; sub-hourly is noise |
| GitHub releases.atom (per repo) | 1×/hour | Same — most projects don't release more than daily |
| GitHub REST API (release bodies) | On-change only | Trigger from atom feed showing a new entry, not on a clock |
| Daily-brief composition | 1×/day at agent's morning hour | Aggregates from cached intel; doesn't hit upstream |

If an agent has cron-driven hourly polls, that's 24 atom hits per repo per day. Watching 30 repos = 720/day. Well under any sensible budget.

## Cache layout

Default to `~/.cache/intel/` (per-agent, per-source):

```
~/.cache/intel/
├── github/
│   ├── anthropics-anthropic-sdk-python.atom
│   ├── anthropics-anthropic-sdk-python.etag
│   ├── ...
├── anthropic/
│   ├── api-changelog.atom
│   ├── api-changelog.etag
├── gemini/
│   ├── blog.rss
│   └── blog.lastmod
└── state.json     # what the agent has already seen, per-source
```

The `.etag` / `.lastmod` files live next to the cached body so a re-fetch is a single `curl` with `-H "If-None-Match: $(cat .etag)"`.

The `state.json` tracks "highest entry ID I've reported on" per source, so the agent doesn't re-surface the same release tomorrow.

## ETag + If-Modified-Since

GitHub atom feeds support `ETag`; most vendor RSS supports `Last-Modified`. Send both, take whichever the server uses:

```sh
ETAG=$(cat .etag 2>/dev/null || echo)
LASTMOD=$(cat .lastmod 2>/dev/null || echo)
curl -sf -D headers.$$ \
  ${ETAG:+-H "If-None-Match: $ETAG"} \
  ${LASTMOD:+-H "If-Modified-Since: $LASTMOD"} \
  -o body.$$ \
  "$URL"
case $? in
  0) # 200 — new content
    cp body.$$ feed.atom
    grep -i ^etag headers.$$ | awk '{print $2}' | tr -d '\r' > .etag
    grep -i ^last-modified headers.$$ | sed 's/^[^:]*: //' | tr -d '\r' > .lastmod
    ;;
  22) # curl -f: 304 from server
    : # nothing to do, cache is fresh
    ;;
  *) # network error
    echo "intel fetch failed: $URL" >&2
    ;;
esac
```

## Anti-patterns

- **Polling every minute.** Burns budget, surfaces nothing — vendors don't ship that fast.
- **Re-fetching without ETag.** Wastes upstream bandwidth and your own budget.
- **Stuffing release bodies into context every run.** Cache and diff; only feed the agent's prompt the entries with IDs the agent hasn't seen.
- **One cache dir shared across agents.** Per-agent cache so a misbehaving agent doesn't corrupt another's state.

## When to break the cadence

Real-time matters for security advisories — a Socket Firewall alert that landed 10 minutes ago is worth a manual `bob run <agent> "check the supply-chain audit script against <package>"` immediately, regardless of cron. Cadences are for the unattended path.

## See Also

- `auth-github-pat` — authenticated baseline so cadence math doesn't fall over
- `feeds-github-releases` — ETag pattern in context
- `feeds-vendor-changelogs` — which vendors actually publish enough to be worth polling
