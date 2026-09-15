# AGENTS.md — {{SERVICE_NAME}}

Instructions for coding agents working in this repository.

## Mission

Implement only what is specified under `spec/`, consistent with `.specify/memory/constitution.md` (or `constitution.md` at repo root if that is where the bundle was placed).

## Before writing UI

1. Call the **BC Design System MCP** (`get_component`, `get_guidelines`, `get_setup`).
2. Prefer Design System components and tokens; never hard-code BC blue/gold hex values.
3. If Figma MCP is connected, re-read the live canvas; do not trust stale screenshots.

## Before claiming "done"

1. Map work to a `spec/features/*.feature` scenario or an explicit tasks.md item.
2. Attach or update `docs/pr-evidence.md` (see PR evidence pack).
3. Do not merge your own PR. Do not weaken checkpoint-gate checks.

## Repo conventions

- TypeScript/React unless `spec/plan.md` says otherwise.
- OpenShift manifests under `deploy/` or `.pipeline/` as the plan defines.
- No secrets in git; use cluster secrets / sealed secrets per PaaS practice.

## When blocked

Open a draft PR or issue describing the ambiguity. Do not invent product rules that contradict the constitution or spec.

## Optional local implement guard

During **implementation** sessions, teams may install Cursor hooks from `.github/sdlc/hooks/` that block agent edits to `spec/features/**`, `.github/workflows/**`, `.github/sdlc/**`, `constitution.md`, and `sdlc.config.json`. For spec/plan work, start the agent with `SDLC_ALLOW_SPEC_EDIT=1`. See pack `LOCAL.md` and `hooks/README.md`.

## SDLC pipeline — spec-driven delivery

This repository is enrolled in the BC Gov agentic SDLC pipeline (`sdlc.config.json`).

### Before implementing

1. Confirm the work is in `spec/tasks.md` and traced to `spec/features/*.feature` (scenarios carry `@R-xx.y` IDs).
2. Query **bc-design-system** MCP before UI (`get_component`, `get_guidelines`).
3. Query **bcgov-sdlc** MCP for constitution / Gherkin / OpenShift checks when relevant.
4. Do not invent scope outside the signed `spec/spec.md`.

### Checkpoints (humans)

1. Spec sign-off  2. Plan approval  3. Review & ship — **no agent self-merge**.

### Evidence

Append to `docs/pr-evidence.md` on implementation PRs (never overwrite prior slices):

```bash
node .github/sdlc/evidence.mjs --root . --finding ID --title "…" --append
```

Fill the **Review receipt** (Checked / Could not check / Residual risk). Implementation PRs that only change evidence fail the gate.

### Labels

- `ready-for-agent` — **SDLC / Intake** assigns the Copilot coding agent (needs `COPILOT_ASSIGN_TOKEN`).
