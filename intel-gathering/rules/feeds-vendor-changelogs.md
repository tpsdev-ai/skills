---
name: feeds-vendor-changelogs
description: Verified-working atom/RSS endpoints for the AI vendors most agents care about. Documents known 404s + HTML-scrape fallbacks so future agents don't burn cycles probing for non-existent feeds.
---

# feeds-vendor-changelogs — known-good vendor sources

For an EA-style agent that needs to know "what did Anthropic / Google / OpenAI ship overnight," prefer atom/RSS over scraping. Atom is stable, parseable, and tells you exactly what changed. Scraping breaks every time the vendor's blog template gets a refresh.

This rule lists endpoints we've verified working, plus the dead-end ones to skip. Re-verify before relying on any of these — vendors change feed URLs without notice.

## Anthropic

| What | URL | Status |
|---|---|---|
| API changelog | `https://docs.anthropic.com/en/release-notes/api.atom` | Atom; verified 200 |
| Python SDK releases | `https://github.com/anthropics/anthropic-sdk-python/releases.atom` | Atom; verified 200 |
| TypeScript SDK releases | `https://github.com/anthropics/anthropic-sdk-typescript/releases.atom` | Atom; verified 200 |
| News / announcements | `https://www.anthropic.com/news` | **No RSS** — `/news/feed.xml`, `/news/all/feed.xml`, `/feed` all 404. HTML scrape only. |

**Recommendation:** Pull API changelog + SDK releases.atom for model/API changes; HTML-scrape the news page only when an agent needs marketing/announcement context.

## Google Gemini

| What | URL | Status |
|---|---|---|
| Gemini blog | `https://blog.google/products-and-platforms/products/gemini/rss/` | RSS; verified 200 |
| DeepMind blog | `https://deepmind.google/blog/rss` | **404** — no published feed |

## OpenAI

| What | URL | Status |
|---|---|---|
| OpenAI blog | `https://openai.com/blog/rss/` | RSS; intermittent (verify per use) |

## Generic pattern for missing feeds

When a vendor doesn't publish RSS, the GitHub releases.atom for their SDK repo is usually the next-best signal — model/API changes have to surface there to ship the client. See [`feeds-github-releases`](feeds-github-releases.md) for the universal pattern.

## Verification before reliance

```sh
curl -sI "https://docs.anthropic.com/en/release-notes/api.atom" | head -1
# Want: HTTP/2 200
```

If an agent's daily brief misses something, first thing to check is whether the upstream feed is still 200ing — vendors retire URLs without redirects.

## See Also

- `feeds-github-releases` — universal pattern for any open-source dependency
- `polling-cadence-and-caching` — how often to hit these without being a bad citizen
