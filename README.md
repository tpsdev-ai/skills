# TPS Skills

Skill packs for [TPS](https://github.com/tpsdev-ai/cli) and [Flair](https://github.com/tpsdev-ai/flair) — best practices for any agent harness (Claude Code, OpenClaw, Cursor, n8n, MCP-aware agents, etc.).

## Install

### Via `tps skill add-pack` (TPS-hosted agents)

```bash
tps skill add-pack @tpsdev-ai/skills --agent <agent-id>
```

Registers the orientation skill on the specified agent. Use `--include-rules` to register specific rule files alongside the summary.

### Via `npx skills add` (Claude Code, Cursor, Windsurf, Continue, Junie)

```bash
npx skills add tpsdev-ai/skills/tps-best-practices
npx skills add tpsdev-ai/skills/flair-best-practices
```

### Programmatic (Node/TS)

```ts
import { ruleNames, rules, skillSummary } from "@tpsdev-ai/skills";
```

## Available skills

### [tps-best-practices](tps-best-practices/SKILL.md)

How to use TPS as a product — agent provisioning, inter-agent mail, skill governance, branch-office isolation, runtime providers.

### [flair-best-practices](flair-best-practices/SKILL.md)

How to use Flair as a product — writing/reading memory, Soul records, Ed25519 identity, federation, MCP integration.

### [ascii-boxes](ascii-boxes/SKILL.md)

Generate and validate ASCII box diagrams with Unicode box-drawing characters (pre-existing skill).

## Layered usage

`@tpsdev-ai/skills` is product-level — applicable to anyone running TPS/Flair. Teams typically layer a private skill pack on top of this for team-specific operating discipline (review process, on-call patterns, etc.).

## License

Apache 2.0. See [LICENSE](LICENSE).
