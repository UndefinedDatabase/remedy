# Context — F017 Scope Fences

## Branch
`feature/f017-scope-fences` (from main after F012 merge)
Base commit: `fe9898a`

## Current state
T001–T003 built + repaired. All 10 external review findings closed.
Repair block complete (6 commits: aec3d12..Scope 6).
354 fence-related tests passing. Pending external acceptance.

## External review findings — ALL CLOSED
See `.agent/live_review.md` for per-finding commit references.

## Key decisions (carried forward)
- Module: `packages/orchestration/scope_fences.py`
- `.git/` component matching anywhere in path
- `extra_builtin_denies` on FenceSpec for dynamic entries
- `resolve_effective_builtins` fails closed (RuntimeError)
- `check_change_set` dedup key: `(path, operation, role)`
- Collision-safe artifact naming with uuid-based event_id
- `..` structurally denied (never resolved)
- Empty allow list = allow-all with logged warning
- `JobFences` on Job model (optional, default None, extra="forbid")
- `scope.allow` / `scope.deny` registered config keys
- `FenceConfigError` on malformed config (fail-closed, never defaults)
- `EffectiveFenceResult` typed provenance carrier
- All 5 applicators use `enforce_change_set` (no divergence)
- `write_file_atomically` for Evidence artifacts (O_NOFOLLOW, create_only)
- `_redact_path` in exception messages and artifacts

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push, create PR, merge, or modify main
- F017 stays `[~]`, F018 stays `[ ]`
