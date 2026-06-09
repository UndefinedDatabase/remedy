# Live Review — Steps 1030-1044

Reviewer: parallel reviewer
Scope: Integrity Gate + Review Zip Closure
Timestamp: 2026-06-09

## Verdict
PASS WITH RISKS — R-0017 Medium open (known risk)

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS (R-0013, R-0014 low/open; 10 files untracked)

## Finding Ledger

### R-0015: integrity_cmd not registered in collect_all_handlers

- **Status**: Resolved
- **Severity**: Blocker
- **Area**: imports
- **Details**: `apps/cli/commands/__init__.py` did not import `integrity_cmd`.
- **Evidence**: Verified fix: `__init__.py` line 27 now imports `integrity_cmd`, line 30 loop includes it.

### R-0016: --collect-only wired as string, always truthy

- **Status**: Resolved
- **Severity**: High
- **Area**: integrity-gate
- **Details**: `--collect-only` fell through to grouped.py else branch as string arg.
- **Evidence**: Verified fix: grouped.py lines 142-143 now have explicit `--collect-only` handler with `action="store_true"`.

### R-0017: ctx_says_complete heuristic too loose

- **Status**: Open
- **Severity**: Medium
- **Area**: integrity-gate
- **Details**: `_check_live_review_verdict` and `_check_plan_consistency` use `"complete" in ctx_text or "done" in ctx_text` full-text search. Matches "done" in prior step status descriptions, causing false positives.
- **Evidence**: `remedy integrity check --json` shows "Context says complete but verdict is PENDING" — triggered by "done" in prior block status text.
- **Expected fix**: Tighten heuristic — only check "## Current Step" line for "COMPLETE", not full-text search.

