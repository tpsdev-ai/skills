---
name: auth-github-pat
description: Source a GitHub PAT into GH_TOKEN from a 0600 secret file inside the agent launcher. Lifts the rate-limit ceiling from ~60/hr (anonymous) to 5000/hr (authenticated) without putting the token in env-dump output or process listings.
---

# auth-github-pat — GitHub PAT for intel agents

Anonymous GitHub API calls are limited to ~60 requests per hour per IP. Authenticated calls get 5000/hr. For an intel-gathering agent that polls `<repo>/releases.atom` for a handful of projects, anonymous is fine. The moment you add the GitHub REST API (release bodies, commit metadata, comparison endpoints) or watch more than a few repos, the floor disappears fast.

## The pattern

1. Store the PAT in a per-agent file:

   ```
   ~/.tps/secrets/<agent>-github-pat   (mode 0600)
   ```

   One PAT per agent — not a shared "intel-bot" PAT. This way a leak rotates one identity, not the whole org.

2. Source it from the agent launcher at startup:

   ```sh
   GH_PAT_FILE="$HOME/.tps/secrets/<agent>-github-pat"
   if [ -r "$GH_PAT_FILE" ]; then
     GH_TOKEN=$(cat "$GH_PAT_FILE")
     export GH_TOKEN
   fi
   ```

3. The agent process then uses `GH_TOKEN` automatically via `gh` CLI, or explicitly via `curl -H "Authorization: token $GH_TOKEN" ...`.

`bob init` (Bob office shell) generates this block in `bin/<name>` automatically — when the secret file is absent the launcher still runs, you just fall back to the anonymous rate limit.

## PAT scope

For intel gathering, the PAT only needs:

- `public_repo` (read public repo contents, releases, atom feeds)

Don't grant `repo` or `workflow` unless the agent actually needs them. The whole point of per-agent PATs is bounding blast radius.

## Verification

```sh
curl -s -H "Authorization: token $GH_TOKEN" https://api.github.com/rate_limit | jq .resources.core
```

Expect `limit: 5000`, `remaining` decrementing per call. If you see `limit: 60` the token isn't getting picked up — check the launcher sourced the file before `exec`.

## Anti-patterns

- **PAT inline in `bob.yaml` or any other commit-able config.** Secrets in files that look like config drift into git history.
- **One shared PAT across multiple agents.** Defeats per-agent auditability and multiplies the leak blast radius.
- **`echo $GH_TOKEN` to verify it's set.** That writes to shell history and (in agent contexts) to the transcript. Use `wc -c <<< "$GH_TOKEN"` if you must confirm presence.
- **PAT in process command line.** `gh --token X ...` puts X in `ps`. Use the env var.

## See Also

- `feeds-github-releases` — what to do with the ceiling once you've got it
- `polling-cadence-and-caching` — how to make the 5000/hr budget last
