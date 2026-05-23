---
name: feeds-github-releases
description: Use `<owner>/<repo>/releases.atom` for any open-source dependency or vendor SDK. Universal, anonymous-accessible, ETag-friendly. Pair with the REST API for release bodies when needed.
---

# feeds-github-releases — universal release feed pattern

Every public GitHub repo exposes `https://github.com/<owner>/<repo>/releases.atom`. This is the single most reliable intel source for any open-source dependency, since most projects ship via tagged GitHub Releases.

## Basic usage

```sh
curl -s "https://github.com/anthropics/anthropic-sdk-python/releases.atom" \
  | grep -oE '<title>[^<]+</title>' \
  | head -5
```

That's it for "what are the last 5 releases." No auth required, no rate limit hassle (atom feeds hit the static-content layer, not the API).

## When to add the GitHub API on top

The atom feed gives you titles + dates + tag URLs. For release **bodies** (what actually changed), use the REST API:

```sh
curl -s -H "Authorization: token $GH_TOKEN" \
  "https://api.github.com/repos/anthropics/anthropic-sdk-python/releases?per_page=5" \
  | jq '.[] | {name, published_at, body}'
```

This DOES count against the 5000/hr rate limit — see [`auth-github-pat`](auth-github-pat.md) for getting your ceiling raised.

## Atom feed quirks

- **Pre-releases** are included by default. To filter, check the title or use the REST API with `?prerelease=false`.
- **Tag-only "releases"** (no published Release object) don't appear in the feed. Watch tags via the API if a project ships that way.
- **Order is reverse-chronological** — first `<entry>` is the most recent.

## Cache + ETag

GitHub atom feeds support `ETag` / `If-None-Match`. Save the ETag from the last poll and send it back; you get a 304 (no body) if nothing changed:

```sh
ETAG=$(cat ~/.cache/intel/anthropic-sdk-python.etag 2>/dev/null || echo)
curl -s -D /tmp/h.$$ \
  ${ETAG:+-H "If-None-Match: $ETAG"} \
  "https://github.com/anthropics/anthropic-sdk-python/releases.atom" \
  -o ~/.cache/intel/anthropic-sdk-python.atom
grep -i ^etag /tmp/h.$$ | awk '{print $2}' | tr -d '\r' > ~/.cache/intel/anthropic-sdk-python.etag
```

Polite to upstream + cheap on agent context (no body to parse when nothing changed).

## See Also

- `auth-github-pat` — required for the REST API path
- `polling-cadence-and-caching` — how often + where to keep the cache
- `feeds-vendor-changelogs` — vendor-specific endpoints (some vendors publish RSS in addition to GitHub)
