#!/usr/bin/env node
/**
 * SDLC / Gate — one PR check: checkpoints + structural + provenance + review (+ optional risk triage).
 * One comment (upserted by marker), one step summary, one exit code.
 *
 *   node gate.mjs --root . --changed-paths src/a.ts,docs/b.md --pr 12 --pr-title "…" --pr-body "…"
 *   node gate.mjs --root . --changed-paths src/a.ts --no-comment        # local dry run
 */
import path from "node:path";
import { execFileSync } from "node:child_process";
import { loadConfig } from "./lib/config.mjs";
import { Results } from "./lib/report.mjs";
import { gh } from "./lib/gh.mjs";
import { resolveAgentMode } from "./lib/agent-mode.mjs";
import { runCheckpoints } from "./gate/checkpoints.mjs";
import { runStructural } from "./gate/structural.mjs";
import { runProvenance } from "./gate/provenance.mjs";
import { runReview, redactionHits } from "./gate/review.mjs";
import { triageChange } from "./gate/risk-triage.mjs";

const MARKER = "<!-- sdlc-gate -->";

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`);
  if (i === -1) return fallback;
  return process.argv[i + 1] ?? fallback;
}
const has = (name) => process.argv.includes(`--${name}`);

const root = path.resolve(arg("root", process.env.GITHUB_WORKSPACE || "."));
const cfg = loadConfig(root);
const pr = arg("pr", process.env.PR_NUMBER);
const prTitle = arg("pr-title", process.env.PR_TITLE || "");
const prBody = arg("pr-body", process.env.PR_BODY || "");
const noComment = has("no-comment");
const asJson = has("json");

function changedPathsFromArgsOrGit() {
  const raw = arg("changed-paths", process.env.CHANGED_PATHS || "");
  if (raw) return raw.split(",").map((s) => s.trim()).filter(Boolean);
  const base = process.env.BASE_SHA || arg("base-ref", "");
  if (!base) return [];
  try {
    return execFileSync("git", ["diff", "--name-only", `${base}...HEAD`], {
      cwd: root,
      encoding: "utf8",
    })
      .split("\n")
      .map((s) => s.trim())
      .filter(Boolean);
  } catch {
    return [];
  }
}

if (cfg.gate.enabled === false) {
  console.log(`SDLC gate disabled (profile: ${cfg.profile}) — nothing to check.`);
  process.exit(0);
}

const changedPaths = changedPathsFromArgsOrGit();
let triageMode = "pipeline";
let triageReasons = [];
if (cfg.gate.risk_triage.enabled) {
  const triage = triageChange({
    root,
    cfg,
    paths: changedPaths,
    baseRef: process.env.BASE_SHA || "",
  });
  triageMode = triage.mode;
  triageReasons = triage.reasons || [];
}

const ctx = {
  root,
  cfg,
  changedPaths,
  triageMode,
  prTitle,
  prBody,
  files: changedPaths,
};
const all = new Results();
all.merge(runCheckpoints(ctx));
all.merge(runStructural(ctx));
all.merge(runProvenance(ctx));
const { results: reviewResults, narrative } = await runReview(ctx);
all.merge(reviewResults);

const title = `SDLC gate${triageMode === "direct" ? " · direct mode" : ""}`;
const sections = [MARKER, all.toMarkdown(title)];
if (triageReasons.length) {
  sections.push(`_Risk triage → **${triageMode}**: ${triageReasons.join("; ")}_\n`);
}
if (narrative) sections.push(`## Agent notes\n\n${narrative}\n`);
sections.push("_Human still owns checkpoint 3 (merge)._");
let comment = sections.join("\n");

const hits = redactionHits(comment, cfg);
if (hits.length) {
  console.error("Redaction guard: comment withheld — matched", hits);
  comment = `${MARKER}\n### SDLC gate · \`${all.status()}\`\n\nPublic comment withheld by redaction guard (${hits.length} match). See workflow step summary.\n`;
}

if (asJson) {
  console.log(JSON.stringify({ status: all.status(), triageMode, items: all.items }, null, 2));
} else {
  all.toConsole(title);
}
all.writeStepSummary(title);

if (!noComment && pr && (process.env.GITHUB_TOKEN || process.env.GH_TOKEN)) {
  if (resolveAgentMode(cfg) === "gh-aw" && cfg.gate.review.enabled) {
    console.log(
      "llm.mode is gh-aw — compiled sdlc-review.lock.yml owns the narrative; posting checks only.",
    );
  }
  try {
    const existing = JSON.parse(
      gh(["api", `repos/{owner}/{repo}/issues/${pr}/comments`, "--paginate"], {
        ignoreError: true,
      }) || "[]",
    ).find((candidate) => typeof candidate.body === "string" && candidate.body.startsWith(MARKER));
    if (existing) {
      gh([
        "api",
        "--method",
        "PATCH",
        `repos/{owner}/{repo}/issues/comments/${existing.id}`,
        "-f",
        `body=${comment}`,
      ]);
    } else {
      gh(["pr", "comment", String(pr), "--body", comment]);
    }
    console.log(existing ? "Updated gate comment" : "Posted gate comment");
  } catch (error) {
    console.warn("Could not comment:", error.message);
  }
}

process.exit(all.exitCode());
