# Plan — F017 Scope Fences — Completion Block

## Goal
Complete F017: repair T002 external-review findings, implement T003
(job field + config keys + CLI), create fresh canonical Evidence,
produce one READY_FOR_REVIEW ZIP. Manual operator only.

## Scope 1 — T002 enforcement/config repairs
- Shared effective-spec resolver: all 5 applicators call
  `load_fence_spec(worktree_root=..., config_path=<repo>/remedy.toml)`.
  Extract `resolve_fence_spec(worktree_root)` to do this in one place.
- Fix `resolve_effective_builtins` fail-open: typed BuiltinResolutionResult
  replaces bare-except-returns-empty. Failure = fail closed.
- Fix `check_change_set` dedup: key `(path, operation)` → `(path, operation, role)`.

## Scope 2 — Durable violation Evidence + real E2E tests
- Shared `enforce_change_set(worktree_root, spec, touched, evidence_ctx)`.
- Job-scoped, collision-safe Evidence location (not global data root).
- Closed versioned artifact schema with redacted absolute paths.
- Persistence failure still blocks repo mutation.
- All 5 paths expose typed `fence_violation` classification.
- Real production E2E tests: invoke actual entry points
  (source_apply, patch_apply, job_fulfillment, do_continue, repo_applicator).
- Artifact safety tests (abs path redaction, collision safety, symlink safety).

## Scope 3 — Complete T003 (job/config/CLI)
- Job model: optional `fences` field on Job (backward-compatible,
  closed type, no str() coercion, malformed fails closed).
- Config: extend ConfigKeySpec with `list` value_type for list-of-strings.
  Register `scope.allow` and `scope.deny` keys.
- CLI: `remedy job fences <id>` showing effective allow/deny/builtin rules,
  source of each, warnings, JSON output.

## Scope 4 — Fresh canonical F017 Evidence + package
- Fresh F017-specific manual Evidence (new job ID, not reusing F012/R40).
- Update T0_F017.md built state with T003 section.
- Update .agent/live_review.md, .agent/context.md.
- One READY_FOR_REVIEW ZIP.

## Commits
1. fix(f017): repair T002 config enforcement + dedup + fail-closed builtins
2. feat(f017): shared enforce_change_set adapter + job-scoped Evidence
3. test(f017): real production E2E tests for all 5 applicators
4. feat(f017): T003 job model fences field + config key extension + CLI
5. docs(f017): T003 built state + updated context/live_review
6. evidence(f017): fresh canonical F017 Evidence + READY_FOR_REVIEW ZIP

## Current Step
Scope 1 — fixing config enforcement, dedup, fail-closed builtins.

## Constraints
- No Fable/subagents/providers/network/Docker. Manual only.
- Do not amend/squash existing F017 commits.
- Do not push, create PR, merge, modify main, or start F018.
- Do not weaken, delete, skip, or xfail tests.
- F017 stays `[~]`, F018 stays `[ ]`.
