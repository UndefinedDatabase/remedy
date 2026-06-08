# Context

## Active Branch
feature/steps-865-879-context-inspector

## Scope
Steps 865-879: Context Inspector v1 — "What will the worker see?"

## Prior Step Status
Steps 810-824: PASS — Proof Chain v1 shipped.
Steps 825-839: PASS — False verified fix, structured NextSafeAction, redaction hardening.
Steps 840-849: PASS — After-apply timing enforcement, change_set safe association.
Steps 850-864: PASS WITH RISKS — File provenance linked-test filtering, Pi/Claude/MCP tooling config (MCP inactive).

## Proof Chain / File Provenance
Accepted for current evidence model. No false verified, linked test evidence only.

## Agent Tooling
Configured and documented. `.pi`, `.claude`, `.mcp.json`, `.vscode/mcp.json` present. MCP inactive by default.

## Current Work
Context Inspector v1: `remedy context inspect <job_id> [task_id] --json`
Shows file-level included/excluded paths, reasons, token estimates, policy gates, tooling awareness.
No raw source content, file bodies, secrets, prompts, MCP config content.

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
- CLI: context.pack, context.explain, context.optimize
