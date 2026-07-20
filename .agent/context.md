# Context — F017 Scope Fences

## Branch
`feature/f017-scope-fences` (from main after F012 merge)

## Scope
T001 + T002 built. T003 (job field + config keys + CLI) is future.

## Key decisions
- Module placed at `packages/orchestration/scope_fences.py` (not `fences.py`)
- `.git/` uses component matching: denied anywhere in path (T002 change from T001's root-prefix)
- `extra_builtin_denies` on FenceSpec for dynamic entries (e.g. REMEDY_DATA_DIR)
- `resolve_effective_builtins(worktree_root)` resolves effective data dir
- `..` is structurally denied (never resolved, even if non-escaping)
- Symlink resolution uses `Path.resolve()` (read-only filesystem access)
- Case sensitivity: no folding, documented as filesystem-dependent
- Empty allow list = allow-all with logged warning (not a brick)
- Config scope table read from `[remedy.scope]` in remedy.toml

## Enforcement sites (T002)
- `source_apply.apply_structured_patch` — preflight before snapshot
- `patch_apply.apply_patch_intent` — defensive single-intent check
- `job_fulfillment.run_job_fulfill` — batch preflight before intent loop
- `do_continue` — single-intent preflight before apply
- `repo_applicator.apply_task_output_to_repo` — preflight before write

## Evidence + postmortem (T002)
- `fence_violations.json` — `fence_violations/v1` schema
- `FENCE_VIOLATION` in FailureClass, classified via typed exception
