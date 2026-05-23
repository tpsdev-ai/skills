#!/usr/bin/env node
// validate-skills.mjs — sanity-check the generated dist + per-skill structure.
import { readFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
let errors = 0;

const SKILL_BYTE_CAP = 8192;

const skills = ["tps-best-practices", "flair-best-practices", "intel-gathering"];

for (const skill of skills) {
  const skillMd = join(root, skill, "SKILL.md");
  if (!existsSync(skillMd)) { console.error(`✗ missing ${skill}/SKILL.md`); errors++; continue; }
  const skillContent = readFileSync(skillMd, "utf8");
  if (Buffer.byteLength(skillContent, "utf8") > SKILL_BYTE_CAP) {
    console.error(`✗ ${skill}/SKILL.md exceeds 8KB cap (${Buffer.byteLength(skillContent, "utf8")} bytes)`);
    errors++;
  }
  if (!/^---$/m.test(skillContent.split("\n").slice(0, 10).join("\n"))) {
    console.error(`✗ ${skill}/SKILL.md missing YAML frontmatter`);
    errors++;
  }

  const rulesDir = join(root, skill, "rules");
  if (!existsSync(rulesDir)) { console.error(`✗ missing ${skill}/rules/`); errors++; continue; }
  for (const f of readdirSync(rulesDir).filter((x) => x.endsWith(".md"))) {
    const rulePath = join(rulesDir, f);
    const content = readFileSync(rulePath, "utf8");
    if (Buffer.byteLength(content, "utf8") > SKILL_BYTE_CAP) {
      console.error(`✗ ${skill}/rules/${f} exceeds 8KB cap (${Buffer.byteLength(content, "utf8")} bytes)`);
      errors++;
    }
    if (!/^---$/m.test(content.split("\n").slice(0, 10).join("\n"))) {
      console.error(`✗ ${skill}/rules/${f} missing YAML frontmatter`);
      errors++;
    }
  }
}

// Validate dist/ exists and exports match
const distIndex = join(root, "dist", "index.js");
if (!existsSync(distIndex)) {
  console.error(`✗ dist/index.js missing — run "npm run build" first`);
  errors++;
} else {
  const { ruleNames, rules, skillSummary, skillSummaries } = await import(distIndex);
  if (!Array.isArray(ruleNames) || ruleNames.length === 0) { console.error("✗ ruleNames empty"); errors++; }
  if (!rules || typeof rules !== "object") { console.error("✗ rules not an object"); errors++; }
  if (!skillSummary || typeof skillSummary !== "string") { console.error("✗ skillSummary missing"); errors++; }
  if (!skillSummaries || typeof skillSummaries !== "object") { console.error("✗ skillSummaries missing"); errors++; }
}

if (errors) {
  console.error(`\n${errors} validation error(s).`);
  process.exit(1);
}
console.log(`✓ validation passed (${skills.length} skills)`);
