# Live Review — Steps 905-924

Reviewer: parallel reviewer
Scope: remedy do v1 Cohesive Flow
Timestamp: 2026-06-08

## Verdict
PENDING — all findings addressed by builder, awaiting reviewer re-check

## Prior Block Status
- Steps 880-894 (Context Inspector Truth Closure): PASS
- Steps 895-904 (Review Protocol Repair): PASS — PR #47 merged

## Finding Ledger

### R-0001: Context phase exception overclaims "completed"
- **Status**: Done: R-0001
- **Severity**: Medium
- **Area**: do_run.py:351
- **Details**: `_run_context_phase` broad `except Exception` returns status="completed" with "skipped" in summary.
- **Evidence**: Fixed — `do_run.py:351` now `status="skipped"`.

### R-0002: No grouped CLI subprocess test for `remedy do`
- **Status**: Done: R-0002
- **Severity**: High
- **Area**: tests/cli/test_do_runtime.py
- **Details**: Needed subprocess test for `remedy do --json`.
- **Evidence**: Fixed — `test_do_runtime.py` has 10 subprocess tests: exit code, JSON parse, required keys, stop reason, next_safe_action, phases, no traceback, no raw content, no absolute paths, text mode. No shell=True. Timeout=30s.

### R-0003: Plan file stale — shows step 905 current
- **Status**: Done: R-0003
- **Severity**: Low
- **Area**: .agent/plan.md
- **Details**: Plan showed step 905 as current.
- **Evidence**: Fixed — plan.md updated to step 924 current, all steps marked complete.

### R-0004: `next_safe_action` commands must exist in catalog
- **Status**: Done: R-0004
- **Severity**: Medium
- **Area**: do_run.py + test_do_run.py
- **Details**: `next_safe_action.command` hardcoded strings. Test validates group prefix resolves to catalog entry.
- **Evidence**: `TestNextSafeActionCatalog::test_next_action_command_is_real` checks all commands (`context.inspect`, `patch.approve`, `job.show`, `do.run`) exist in catalog. Full subcommand matching deferred to v2 (catalog lookup API not yet available).

### R-0005: `DoRunContract` duplicates `RunContract`
- **Status**: Accepted risk
- **Severity**: Low
- **Area**: do_run.py:96-103
- **Details**: v1 uses simplified contract. Consolidation deferred to v2 when apply path is wired.
