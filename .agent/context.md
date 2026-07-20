# Context — F017 Scope Fences

## Branch
`feature/f017-scope-fences` (from main after F012 merge)

## Scope
T001 + T002 + T002 repairs + T003 built. Evidence + ZIP pending.

## Key decisions
- Module placed at `packages/orchestration/scope_fences.py` (not `fences.py`)
- `.git/` uses component matching: denied anywhere in path
- `extra_builtin_denies` on FenceSpec for dynamic entries (e.g. REMEDY_DATA_DIR)
- `resolve_effective_builtins` fails closed (RuntimeError, not empty tuple)
- `BuiltinResolutionResult` typed result for error detail
- `resolve_fence_spec(worktree_root)` shared resolver — always passes config_path
- `enforce_change_set` shared adapter — job-scoped Evidence
- `check_change_set` dedup key: `(path, operation, role)` — preserves roles
- Collision-safe artifact naming: `fence_violations_{jobid}_{applicator}.json`
- Absolute path redaction in violation artifacts
- `..` is structurally denied (never resolved, even if non-escaping)
- Symlink resolution uses `Path.resolve()` (read-only filesystem access)
- Case sensitivity: no folding, documented as filesystem-dependent
- Empty allow list = allow-all with logged warning (not a brick)
- Config scope table read from `[remedy.scope]` in remedy.toml
- `JobFences` closed Pydantic type on Job model (optional, default None)
- `ConfigKeySpec.value_type` extended with `list` for list-of-strings
- `scope.allow` / `scope.deny` registered config keys
- `remedy job fences <id>` CLI command with JSON support

## Enforcement sites (T002 + repairs)
- All use shared `resolve_fence_spec(worktree_root)` with config_path
- All pass per-job fences via `job.fences` when available
- `source_apply.apply_structured_patch` — preflight before snapshot
- `patch_apply.apply_patch_intent` — defensive single-intent check
- `job_fulfillment.run_job_fulfill` — batch preflight before intent loop
- `do_continue` — single-intent preflight before apply
- `repo_applicator.apply_task_output_to_repo` — preflight before write

## Evidence + postmortem
- Collision-safe `fence_violations_{id}_{applicator}.json` with `fence_violations/v1` schema
- `FENCE_VIOLATION` in FailureClass, classified via typed exception
