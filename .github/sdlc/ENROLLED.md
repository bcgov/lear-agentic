# SDLC pipeline enrolled

Enrolled at: 2026-09-15T23:36:01Z
profile: delivery
gh-aw: false

Next:
1. Edit sdlc.config.json (project name; paths.impl for your layout).
2. Push; Actions → workflow permissions Read and write; run **SDLC / Preflight**.
3. Delivery: fill constitution.md placeholders (architecture review PR); write spec/spec.md + features (checkpoint 1); spec/plan.md (checkpoint 2).
4. Delivery: set secret COPILOT_ASSIGN_TOKEN; label issues ready-for-agent — or implement with a local agent (see pack LOCAL.md).
5. Every PR runs **SDLC / Gate**; a human merges (checkpoint 3). Weekly **SDLC / Measure** opens one review issue.
6. Day-to-day: .github/sdlc/OPERATE.md
