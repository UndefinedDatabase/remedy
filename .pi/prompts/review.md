---
description: Review current Remedy changes safely
---
Review the current Remedy task state and changed files.

Required:
- Read `AGENTS.md`, `.agent/plan.md`, `.agent/live_review.md`.
- Treat reviewer findings as stronger than worker self-report.
- Check scope drift, Proof Chain truth, safe outputs, wrapper test usage, and MCP/tooling security.
- Do not include raw diffs, artifacts, stdout/stderr, source content, command output, or secrets in the response.

Return PASS/BLOCKED with concrete blockers and targeted tests.
