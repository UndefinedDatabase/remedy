# Live Review — Steps 1045-1064

Reviewer: parallel reviewer
Scope: Integrity Gate Truth Closure + Run Contract Enforcement v1
Timestamp: 2026-06-10

## Verdict
PENDING — 3 blockers open, 1 high open

## Prior Block Status
- Steps 940-974: PASS
- Steps 975-994: PASS
- Steps 995-1009: PASS
- Steps 1010-1029: PASS WITH RISKS (R-0013, R-0014 low/open; 10 files untracked)
- Steps 1030-1044: PASS WITH RISKS (R-0017 medium open)

## Finding Ledger

### R-0017: ctx_says_complete regex does not match multi-line scope declarations

- **Status**: Open
- **Severity**: Blocker
- **Area**: integrity-gate
- **Details**: R-0017 fix introduced `_SCOPE_COMPLETE_RE` and `_CURRENT_STEP_COMPLETE_RE` regex patterns, but they only match COMPLETE/DONE on the SAME line as the `## Scope` heading. In practice (and in the new tests), the keyword appears on the NEXT line after the heading. The regex `^##\s+Scope\b.*?\b(COMPLETE|DONE)\b` with `re.MULTILINE` treats `.` as non-newline, so it cannot cross to the next line.
- **Evidence**: 5 test failures in `tests/orchestration/test_integrity_gate.py`:
  - `test_explicit_scope_complete_triggers` — `_ctx_says_complete("## Scope\nSteps 1045-1064: ... — COMPLETE\n")` returns `False`
  - `test_explicit_scope_done_triggers` — same pattern
  - `test_current_step_complete_triggers` — same pattern
  - `test_pending_live_review_with_explicit_complete_fails` — integrity check does not FAIL as expected
  - `test_unchecked_with_scope_complete_fails` — plan check does not FAIL as expected
- **Expected fix**: Either (a) use `re.DOTALL` so `.` crosses newlines, or (b) change regex to match COMPLETE/DONE on the line FOLLOWING the `## Scope` heading (e.g., read lines, find heading, check next line). Option (b) is safer to avoid over-matching.

### R-0018: No evaluate_action helper — allowed/denied actions not enforced at runtime

- **Status**: Open
- **Severity**: Blocker
- **Area**: run-contract
- **Details**: `DoRunContract` declares `allowed_actions` and `denied_actions` tuples, but no code checks these before executing phases. There is no `evaluate_action()`, `is_action_allowed()`, or similar helper anywhere in the orchestration package. The actions are only exported to JSON — never enforced.
- **Evidence**: `grep -r "evaluate_action\|check_action\|is_action_allowed\|action_allowed" packages/orchestration/` returns no matches. `do_run.py` never references `contract.allowed_actions` or `contract.denied_actions` except in the export function at line 554-555.
- **Expected fix**: Add `evaluate_action(action: str, contract: DoRunContract) -> bool` that checks allowed/denied lists. Call it before each phase in `run_do()`. If action is in `denied_actions`, block. If `allowed_actions` is non-empty and action not in it, block.

### R-0019: repair_loop has no contract enforcement

- **Status**: Open
- **Severity**: Blocker
- **Area**: repair-loop
- **Details**: `start_repair_loop_v0()` does not create, receive, or check any RunContract or DoRunContract. No max_loops budget, no denied_actions check, no allowed_actions check. The repair loop is completely unguarded by the contract system.
- **Evidence**: `grep -r "contract\|max_loops\|max_test_runs" packages/orchestration/repair_loop.py` returns no matches. The function signature has no contract parameter.
- **Expected fix**: Either (a) accept a contract parameter and check it before creating fix tasks / patch intents, or (b) build a default repair contract internally and enforce it. At minimum, denied actions like `apply_patch` should be checked before `create_patch_intent`.

### R-0020: do_run does not check contract before phases

- **Status**: Open
- **Severity**: High
- **Area**: do-flow
- **Details**: `run_do()` creates a `DoRunContract` at line 200 but only uses it for `stop_before_apply` (line 333) and `autonomy_level` (line 283). The `allowed_actions` and `denied_actions` fields are never consulted before running plan/context/build/patch_intent phases. If someone sets `denied_actions=("plan",)`, the plan phase still runs.
- **Evidence**: No call to any action-checking function between contract creation (line 200) and phase execution (lines 238-370). Only `contract.stop_before_apply` and `contract.autonomy_level` are read.
- **Expected fix**: Before each phase, check `evaluate_action(phase_action, contract)`. Block if denied. This ties R-0018 + R-0020 together.

## Checks Passed

- **source_apply**: Not imported in `do_run.py` or `repair_loop.py`. Approval gate intact.
- **shell=True**: Not found in any production orchestration code. Multiple test contracts verify.
- **stop_before_apply**: Enforced at `do_run.py:333`. Default `True`. CLI enforces True.
- **Redaction**: `review_bundle.py` strips raw fields. `redaction_patterns.py` has FORBIDDEN_RAW_FIELD_NAMES. Memory layer has `_FORBIDDEN_KEYS`. No raw source/diff/stdout/stderr/secrets in output paths.
- **max_loops validation**: `do_run.py:179` rejects `< 1`. But v1 caps to single pass (`min(max_loops, 1)`).
- **RunContract model**: Exists, frozen dataclass, JSON-serializable, all fields present. Tests pass (18/18).
- **do_run tests**: 38/38 pass (contract, autonomy, approval, phases).
- **repair_loop_hardened tests**: 7/7 pass (deterministic cycles, approval gate, no raw leaks).

## Test Summary

107 passed, 5 failed (all integrity gate R-0017 regex).
