# Context — F017 Scope Fences

## Branch
`feature/f017-scope-fences` (from main after F012 merge)
Base commit: `fe9898a`

## Current state
T001–T003 built (11 commits). External review returned 10 findings.
Repair block in progress: Scopes 1–5 (reconciliation → centralized
resolver → shared enforcement → secure Evidence → E2E + package).

Previous ZIP (`remedy-review-20260720-233422`) built at `0846a18`
(10 commits). Commit `a0aa69f` added after packaging (agent state only).
That ZIP is stale — new package will cover all commits.

## External review findings (under repair)
1. `_read_scope_table` duplicates central config — env vars never enforced
2. Malformed config fails open (parse error → default allow-all)
3. `JobFences` not closed — accepts unknown fields
4. Five applicators diverge — different subsets of resolve/check/write/raise
5. `enforce_change_set()` has no production callers
6. Artifact writer uses `write_text` — no symlink protection, no atomic write
7. Exception message leaks absolute paths
8. `repo_applicator` doesn't pass `job_fences`
9. `patch_apply` writes no Evidence artifact
10. `do_continue` uses `APPLY_FAILED` instead of `FENCE_VIOLATION`

## Key decisions (carried forward)
- Module: `packages/orchestration/scope_fences.py`
- `.git/` component matching anywhere in path
- `extra_builtin_denies` on FenceSpec for dynamic entries
- `resolve_effective_builtins` fails closed (RuntimeError)
- `check_change_set` dedup key: `(path, operation, role)`
- Collision-safe artifact naming
- `..` structurally denied (never resolved)
- Empty allow list = allow-all with logged warning
- `JobFences` on Job model (optional, default None)
- `scope.allow` / `scope.deny` registered config keys

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push, create PR, merge, or modify main
- F017 stays `[~]`, F018 stays `[ ]`
