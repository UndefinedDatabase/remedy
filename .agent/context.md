# Context — F017 Scope Fences

## Branch
`feature/f017-scope-fences-clean` (reconstructed from mixed branch)
Base commit: `fe9898a`
Previous mixed branch: `feature/f017-scope-fences` (backed up at `backup/f017-scope-fences-mixed-17592a5`)
Unrelated roadmap commit: separated to `docs/roadmap-features-f221-f250`

## Current state
T001–T003 built + repaired. All 10 external review findings closed.
Final closure block: 7 findings closed. Branch cleanup: unrelated
roadmap commit 0b71df6 removed. General POSIX path redaction. Real
production E2E (20 tests). Docs consistency fixed. 27 commits, HEAD ca65478.
Pending external acceptance.

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
- `JobFences` Pydantic model_validator: trims whitespace, rejects empty/non-string
- `scope.allow` / `scope.deny` registered config keys
- `FenceConfigError` on malformed config (fail-closed, never defaults)
- `EffectiveFenceResult` typed provenance carrier
- All 5 applicators use `enforce_change_set` (no divergence)
- `write_file_atomically` for Evidence artifacts (O_NOFOLLOW, create_only)
- `_sanitize_diagnostic` replaces `_redact_path(raw)[:200]` in persistence errors
- `_match_violation_rule` returns 4-tuple with `applicable_rules`
- `check_and_apply_to_repo` passes `job_id` and `evidence_dir` through

## Constraints
- No providers, no network, no Docker, no subagents
- Do not amend/squash existing commits
- Do not push, create PR, merge, or modify main
- F017 stays `[~]`, F018 stays `[ ]`
