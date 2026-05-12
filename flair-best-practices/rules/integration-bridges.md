---
name: integration-bridges
description: Importing memory from other systems (mem0, ChatGPT export, Claude project export, etc.) into Flair via the `flair bridge import` command. Plugin-based extensible.
---

# Memory Bridges

Flair's bridge system imports memory from other agent-memory systems so you can migrate without losing context. Bridges are plugins; each handles one source format.

## Supported sources

| Source | Plugin | Input |
|---|---|---|
| mem0 | `mem0` | mem0 JSON export OR live API URL + key |
| ChatGPT export | `chatgpt-project` | the `.zip` from a ChatGPT data export |
| Claude project | `claude-project` | a Claude project export `.zip` |
| Manual MD batch | `markdown` | a folder of `.md` files, one per memory |

## Import

```bash
flair bridge import <source> --input <path-or-url> --agent <agent-id> [--dry-run]
```

Examples:

```bash
flair bridge import mem0 --input mem0-export.json --agent alice
flair bridge import chatgpt-project --input ~/Downloads/chatgpt-export.zip --agent alice
flair bridge import claude-project --input ~/Downloads/claude-project-foo.zip --agent alice
```

`--dry-run` previews what would be imported without writing. Always start there.

## What gets written

For each source memory, the bridge writes a Flair Memory record with:
- `content` = the source memory content
- `type` = `imported`
- `durability` = `persistent` (importable history is worth keeping)
- `tags` = `source:<bridge-name>`, plus any tags from the source
- `subject` = the source's group/conversation/note name if available
- `metadata` = bridge-specific provenance (original ID, original timestamps)

## Plugin authoring

Bridges live in `packages/flair-bridges/<source>/`. The contract:

```ts
export interface Bridge {
  name: string;
  acceptsInput(path: string): boolean;
  importToFlair(input: string, agentId: string, opts): AsyncIterable<MemoryWrite>;
}
```

Bridges run client-side; they call `flair.writeMemory()` for each entry.

## Anti-Patterns

- **Importing without `--dry-run` first.** Always preview. Imports are bulk-writes; a malformed source can fill an agent's memory with garbage.
- **Importing into an agent's "production" identity if the source had different conventions.** Use a sandbox agent id (e.g., `alice-import`) first, review, then re-tag + migrate.
- **Trusting the bridge's content normalizer.** Cross-system content has different conventions. Audit the first 50 imports manually.

## See Also

- `memory-writing-memory` — bridges call this for each imported entry
- The flair repo's `packages/flair-bridges/` for source plugins
