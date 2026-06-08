---
name: remedy-review
description: Use before final handoff or PR creation to review Remedy changes for safety, scope, tests, and reviewer blockers.
---

# Remedy Review

## Required inputs
- `AGENTS.md`
- `.agent/plan.md`
- `.agent/context.md`
- `.agent/live_review.md`
- Targeted changed files

## Review rules
- Reviewer findings beat worker self-report.
- Do not claim PASS while `.agent/live_review.md` has unresolved blockers.
- Confirm tests use Remedy wrappers.
- Confirm no unrelated scope drift.
- Confirm no raw artifacts, stdout/stderr, source content, raw diffs, command output, or secrets are exposed.
- For tooling work, confirm `.pi`, `.claude`, `.mcp.json`, and `.vscode/mcp.json` were inspected on disk.

## Output
Return PASS/BLOCKED, concrete blockers, tests run, full pytest status, and merge readiness.
