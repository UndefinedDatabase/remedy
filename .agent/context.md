# Context

## Active Branch
feature/steps-880-894-context-truth

## Scope
Steps 895-904: Parallel Review Protocol Repair + Context Inspector Verification

## Prior Step Status
Steps 810-824: PASS — Proof Chain v1 shipped.
Steps 825-839: PASS — False verified fix, structured NextSafeAction, redaction hardening.
Steps 840-849: PASS — After-apply timing enforcement, change_set safe association.
Steps 850-864: PASS WITH RISKS — File provenance linked-test filtering, Pi/Claude/MCP tooling config (MCP inactive).
Steps 865-879: PASS — Context Inspector v1 shipped.
Steps 880-894: PASS — Context Inspector Truth Closure (6 fixes verified).

## Builder/Reviewer Handoff Rules

- Before final handoff, builder MUST read `.agent/live_review.md`.
- If latest verdict is PENDING or FAIL, builder must NOT claim merge-ready PASS.
- Every open finding must have `Done: R-XXXX` marker or be listed as remaining risk.
- See `.agent/review_protocol.md` for full finding format and resolution rules.

## Known Risks

### Pre-existing test failure
`tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order`
fails on `main` with chain order mismatch (missing `test_run` step).
Unrelated to context inspector. Deselected in fast lane runs.
Must be fixed in a future block — not this scope.

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
