/**
 * @tpsdev-ai/skills — programmatic access to the skill content.
 *
 * Two skills shipped:
 *   - tps-best-practices  → SKILL.md + rules/*.md
 *   - flair-best-practices → SKILL.md + rules/*.md
 *
 * Consumed by `tps skill add-pack @tpsdev-ai/skills` (cli#278) and by
 * any npm-aware agent harness that wants programmatic access to the
 * skill summary + per-rule content.
 *
 * The build script (scripts/build.mjs) generates the actual content
 * maps; this file declares the export shape.
 */

export declare const ruleNames: readonly string[];
export type RuleName = (typeof ruleNames)[number];
export declare const rules: Record<RuleName, string>;
export declare const skillSummary: string;
