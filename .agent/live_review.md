# Live Review — Steps 850-864

Reviewer: active agent + parallel findings
Scope: File provenance hotfix and local agent tooling modernization
Timestamp: 2026-06-08

## Incoming Blockers Resolved
1. File provenance appended every global `test_run_completed` event as a proof step.
2. Doctor secret scan initially overmatched ordinary policy words in committed docs/skills.

## Resolution
- `file_provenance.py` appends `test_run` only when `_link_test_to_change()` returns linked evidence.
- Unlinked/global tests are omitted from file causal/proof chain steps.
- `build_proof_chain(..., path=...)` counts total applied changes before path filtering, so path filtering cannot convert multi-change generic tests into sole-change proof.
- Doctor secret detection now looks for token-like values or assignments, not ordinary words like "token" or "secret".
- `.pi` was actually absent before this block and was added; `.claude` existed and was improved in place while preserving ignored `settings.local.json`.
- `.mcp.json` and `.vscode/mcp.json` are present with empty server maps; no MCP is active.

## Validation
- Doctor script runs successfully.
- Targeted wrapper suite passed for tooling, proof chain, change set, change proof CLI, and command catalog tests.

## Current Status
PASS for implemented scope; full pytest not run.
