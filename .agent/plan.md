# Plan — F017 Scope Fences — T002

## Goal
Implement T002: applicator enforcement, atomicity, violation Evidence,
and postmortem classification. Preserve T001 behavior. Do not implement T003.

## Scope 1 — T001 builtin-boundary repairs
- `.git` denied as path COMPONENT anywhere (not just root prefix)
- Effective Remedy data dir resolved dynamically via `resolve_data_root()`
- Protected when inside worktree; `.data/` remains static fallback
- `extra_builtin_denies` field on FenceSpec (backward compatible)
- `resolve_effective_builtins(worktree_root)` function
- Fix `test_non_root_git_dir_allowed` → now denied
- Add regression tests for nested `.git` and overridden data dir

## Scope 2 — shared change-set preflight
- `TouchedPath` (path, operation, role) frozen dataclass
- `FenceViolation` (path, normalized, operation, role, reason, matched_rule, rule_source)
- `ChangeSetFenceResult` (allowed, violations, warnings, touched_count)
- `FenceViolationError` typed exception carrying stable violation set
- `check_change_set(worktree_root, spec, touched_paths)` pure preflight
- Deterministic ordering, dedup, all violations collected
- Uses `check_path` as single semantic authority

## Scope 3 — applicator enforcement + atomicity
- `source_apply.apply_structured_patch`: derive touched-path set, preflight
  before snapshot/mutation. Violation → no mutation, no snapshot.
- `patch_apply.apply_patch_intent`: defensive single-intent preflight.
- `job_fulfillment.run_job_fulfill`: preflight ALL intent targets before
  first `_approve_and_apply_intent` call. One violation → nothing applied.
- `do_continue.py`: single-intent preflight before apply.
- `repo_applicator`: preflight before `_write_to_repo`.
- All enforcement uses shared `check_change_set` from scope_fences.

## Scope 4 — violation Evidence + postmortem classification
- `fence_violations.json` artifact with closed schema
- Written to Evidence root before error escapes
- No absolute paths; Evidence-safe relative paths only
- `FENCE_VIOLATION` added to `FailureClass` enum
- `FenceViolationError` classified as `fence_violation` via typed exception
- `fence_violation` added to `TERMINAL_STATUS_CLASSES`

## Commits
1. T001 builtin repairs + shared change-set preflight
2. Applicator and batch-boundary enforcement
3. Violation Evidence + postmortem classification
4. T002 tests + truthful documentation/state

## Constraints
- Do not push, create PR, merge, modify main, or start T003/F018
- Do not amend/squash T001 commits
- Do not weaken or xfail tests
- Zero provider calls
