# Context

## Active Branch
feature/steps-880-894-context-truth

## Scope
Steps 880-894: Context Inspector Truth Closure — "No Fake Visibility"

## Prior Step Status
Steps 810-824: PASS — Proof Chain v1 shipped.
Steps 825-839: PASS — False verified fix, structured NextSafeAction, redaction hardening.
Steps 840-849: PASS — After-apply timing enforcement, change_set safe association.
Steps 850-864: PASS WITH RISKS — File provenance linked-test filtering, Pi/Claude/MCP tooling config (MCP inactive).
Steps 865-879: PASS — Context Inspector v1 shipped. 70 targeted + 3011 fast lane passed.

## Proof Chain / File Provenance
Accepted for current evidence model. No false verified, linked test evidence only.

## Agent Tooling
Configured and documented. `.pi`, `.claude`, `.mcp.json`, `.vscode/mcp.json` present. MCP inactive by default.

## Current Work
Context Inspector Truth Closure: fix 6 identified issues from independent review.
1. `.env.*` generic protection gap — only specific names, not pattern-based
2. Path traversal false positives — `".." in path_str` matches filenames
3. Task existence not validated — UUID format checked but not presence in job
4. Events parameter unused — no event target paths extracted
5. Budget wording mismatch — says "enforced" but only reports
6. No deterministic budget trimming or stable sorting

## Resource Safety
Use `scripts/remedy_pytest.sh`; no direct pytest, no background pytest, no `shell=True`.
No secrets, `.env`, `.data`, raw artifacts/stdout/diffs/source content in output.

## Existing Context Infrastructure
- `source_context.py` — file selection with deny lists, budget, categories
- `context_pack.py` — token-budget-aware section packing
- `context_optimizer.py` — explain/optimize context
- `context_coverage.py` — signal-based coverage snapshot
- `project_constitution.py` — protected_paths, risky_paths, conventions
- `token_policy.py` — routing constraints, zero-token steps
- CLI: context.pack, context.explain, context.optimize, context.inspect
