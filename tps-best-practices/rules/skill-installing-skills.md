---
name: skill-installing-skills
description: How to register skills on an agent — single skills via tps skill register, npm-shipped packs via tps skill add-pack.
---

# Installing Skills on an Agent

Skills are knowledge packages — not executable code. They land as Soul records in Flair, scoped per-agent. There's an 8 KB cap per skill (skills are *patterns*, not documentation dumps) and a security scan that blocks high-risk content.

## Single-skill registration

```bash
tps skill register <source-file> \
  --name <skill-name> \
  --pack-version <hash-or-semver> \
  --agent <agent-id> \
  [--priority standard]
```

The scanner runs first (looks for shell commands, encoded payloads, zero-width chars, etc.). If `riskLevel` is `high` or `critical`, registration is refused. `medium` is allowed with a warning.

## Pack registration (npm-shipped skill packs)

For multi-skill packs published to npm (like `@harperfast/skills` or `@tpsdev-ai/skills`):

```bash
tps skill add-pack @harperfast/skills@1.4.2 --agent <agent-id>
# or with rules included:
tps skill add-pack @tpsdev-ai/skills --agent <agent-id> --include-rules memory-writing,memory-reading
```

Behavior:

1. `npm pack` the named package into a temp dir
2. Dynamic-import its `dist/index.js` to read `ruleNames`, `rules`, `skillSummary`
3. Scan + register the summary as one skill
4. If `--include-rules` is passed, also register each named rule

Idempotency: same pack + version on the same agent is a no-op. Different version errors with a request to revoke first.

## Listing + showing + revoking

```bash
tps skill list --agent <id>                       # what's registered
tps skill show <name> --agent <id>                # details
tps skill revoke <name> --agent <id>              # remove
```

## Loading order

Skills are loaded at agent bootstrap (via `openclaw-flair` plugin for OpenClaw agents, or via MEMORY.md references for Claude-Code-style agents). Priority order:

1. `critical` (rare — used for safety-critical behavioral rules)
2. `high` (organizational discipline)
3. `standard` (default — most skills land here)
4. `low` (informational nudges)

Higher-priority skills override lower-priority ones when content conflicts.

## Anti-Patterns

- **Trying to register a >8 KB skill.** Split it into multiple smaller skills or use a Memory entry instead. Skills are patterns, not docs.
- **Hardcoding shell commands in skill content.** The scanner will flag it as `shell_backtick` / `shell_command`. Either describe the pattern in words or use a code-fenced block with a non-shell language hint.
- **Re-registering the same skill on every session start.** It's already there. Use `tps skill list` to check before re-registering.

## See Also

- `agent-creating-an-agent` — needs to exist before skills can be registered
- `flair-best-practices/memory-writing-memory` — when a piece of knowledge is too big or too dynamic for a skill, use Memory
