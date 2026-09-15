/**
 * Assign GitHub Copilot coding agent when an issue is labeled ready-for-agent.
 *
 * COPILOT_ASSIGN_TOKEN must be a user PAT / OAuth token; an Actions
 * GITHUB_TOKEN cannot assign Copilot because billing is tied to a user.
 */
import { appendFileSync } from "node:fs";
import { execFileSync } from "node:child_process";
import { loadConfig, repoRoot } from "../lib/config.mjs";

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? undefined : process.argv[i + 1];
}

function ghJson(args, token, input) {
  return execFileSync("gh", args, {
    encoding: "utf8",
    input,
    env: { ...process.env, GH_TOKEN: token, GITHUB_TOKEN: token },
  });
}

export async function runAssign(issueNumber) {
  const cfg = loadConfig(repoRoot());
  const ca = cfg.intake.coding_agent;
  if (ca.auto_assign === false) {
    console.log("intake.coding_agent.auto_assign disabled — skip");
    return;
  }

  const issue = String(issueNumber);
  const repo =
    arg("repo") ||
    process.env.GITHUB_REPOSITORY ||
    (() => {
      try {
        return execFileSync(
          "gh",
          ["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"],
          { encoding: "utf8" },
        ).trim();
      } catch {
        return null;
      }
    })();

  if (!repo || !repo.includes("/")) {
    throw new Error("GITHUB_REPOSITORY or --repo owner/name required");
  }

  const userToken = process.env.COPILOT_ASSIGN_TOKEN || process.env.COPILOT_GITHUB_TOKEN || "";
  const commentToken = process.env.GITHUB_TOKEN || process.env.GH_TOKEN || userToken;

  function postComment(body) {
    if (!commentToken) return;
    try {
      ghJson(
        [
          "api",
          "--method",
          "POST",
          "-H",
          "Accept: application/vnd.github+json",
          `repos/${repo}/issues/${issue}/comments`,
          "--input",
          "-",
        ],
        commentToken,
        JSON.stringify({ body }),
      );
    } catch (error) {
      console.warn("Could not comment:", error.message);
    }
  }

  if (!userToken) {
    const msg = [
      "### SDLC intake — coding agent not assigned",
      "",
      "Label `ready-for-agent` was applied, but secret **`COPILOT_ASSIGN_TOKEN`** is not set.",
      "",
      "Copilot assignment requires a **user** PAT (Actions `GITHUB_TOKEN` cannot assign Copilot):",
      "",
      "- Fine-grained: Issues (RW), Contents (RW), Pull requests (RW), Metadata (R)",
      "- Classic: `repo` scope",
      "- Copilot coding agent must be enabled for this repository and the token owner",
      "",
      "After adding the secret, remove and re-apply `ready-for-agent`.",
    ].join("\n");
    console.error(msg);
    postComment(msg);
    process.exitCode = 1;
    return;
  }

  const assignLabel = ca.label || "ready-for-agent";
  const baseBranch = ca.base_branch || "main";
  const assignee = "copilot-swe-agent[bot]";
  const customInstructions =
    (ca.custom_instructions && String(ca.custom_instructions).trim()) ||
    [
      "Follow AGENTS.md and the repository constitution (constitution.md / .specify/memory/constitution.md).",
      "Implement only what the issue acceptance criteria and linked spec/features require.",
      "Open a draft pull request. Do not merge.",
      "Update docs/pr-evidence.md when touching implementation paths.",
      "Prefer B.C. Design System components for UI; meet WCAG 2.1 AA.",
    ].join(" ");

  const issueMeta = JSON.parse(
    ghJson(
      ["api", `repos/${repo}/issues/${issue}`, "-H", "Accept: application/vnd.github+json"],
      userToken,
    ),
  );

  const labels = (issueMeta.labels || []).map((label) => label.name);
  if (!labels.includes(assignLabel)) {
    console.log(`Issue #${issue} lacks label ${assignLabel} — skip`);
    return;
  }

  const already = (issueMeta.assignees || []).some((candidate) =>
    ["copilot-swe-agent[bot]", "copilot-swe-agent", "Copilot"].includes(candidate.login),
  );
  if (already) {
    console.log(`Issue #${issue} already assigned to Copilot — skip`);
    return;
  }

  const assignBody = {
    assignees: [assignee],
    agent_assignment: {
      target_repo: repo,
      base_branch: baseBranch,
      custom_instructions: customInstructions,
    },
  };

  console.log(`Assigning ${assignee} to ${repo}#${issue} (base=${baseBranch})…`);
  let response;
  try {
    response = ghJson(
      [
        "api",
        "--method",
        "POST",
        "-H",
        "Accept: application/vnd.github+json",
        "-H",
        "X-GitHub-Api-Version: 2022-11-28",
        `repos/${repo}/issues/${issue}/assignees`,
        "--input",
        "-",
      ],
      userToken,
      JSON.stringify(assignBody),
    );
  } catch (error) {
    const detail = error.stderr?.toString?.() || error.message;
    console.error("Assign failed:", detail);
    if (/\b(?:HTTP\s*)?(?:402|403)\b|quota|insufficient/i.test(detail)) {
      postComment("**Copilot assign failed (quota/permission)** — implement locally or top up credits.");
    } else {
      postComment(
        [
          "### SDLC intake — coding agent assign failed",
          "",
          `Could not assign \`${assignee}\` automatically.`,
          "",
          "Common causes:",
          "- Token is not a **user** PAT / OAuth token",
          "- Copilot coding agent is not enabled for this repo + token owner",
          "- PAT missing Issues / Contents / Pull requests write",
          "",
          `Error (truncated): \`${String(detail).slice(0, 400).replace(/`/g, "'")}\``,
        ].join("\n"),
      );
    }
    process.exitCode = 1;
    return;
  }

  const assigned = JSON.parse(response);
  const logins = (assigned.assignees || []).map((candidate) => candidate.login).join(", ");
  console.log(`Assigned. Assignees now: ${logins || "(none returned)"}`);

  const comment = [
    "### SDLC intake — coding agent assigned",
    "",
    `Assigned **${assignee}** because of label \`${assignLabel}\`.`,
    "",
    `- Base branch: \`${baseBranch}\``,
    "- Expect a **draft PR** from Copilot; humans own merge (checkpoint 3).",
    "- Checkpoint gate + spec review will run on that PR.",
  ].join("\n");
  postComment(comment);

  if (process.env.GITHUB_STEP_SUMMARY) {
    appendFileSync(process.env.GITHUB_STEP_SUMMARY, comment + "\n");
  }
}
