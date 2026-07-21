# Live Review — F017 Scope Fences

## Status
**T001 BUILT** — FenceSpec + pure path checker + exhaustive tests.
**T002 BUILT + REPAIRED** — Applicator enforcement, atomicity, change-set
                  preflight, violation Evidence, postmortem classification.
                  Repairs: config enforcement, fail-closed builtins, role dedup.
**T003 BUILT + REPAIRED** — Job model fences field, config keys, CLI display.
                  Repairs: centralized resolver, closed JobFences, provenance.

Module: `packages/orchestration/scope_fences.py`
Model:  `packages/core/models.py` — JobFences (closed, extra="forbid", model_validator)
Config: `packages/orchestration/config.py` — scope.allow, scope.deny
CLI:    `apps/cli/commands/job.py` — remedy job fences
Tests:  `tests/orchestration/test_fences.py` — 78 passed
        `tests/orchestration/test_applicator_fences.py` — 43 passed
        `tests/orchestration/test_fence_e2e.py` — 104 passed

## Package discrepancy (a0aa69f) — RESOLVED
Previous ZIP (`remedy-review-20260720-233422`) built at `0846a18`
(10 commits). Superseded by repair block. New package covers all
commits including repair scopes 1-5.

## External review findings — ALL CLOSED
1. ~~Duplicate TOML authority~~ → removed `_read_scope_table`, central config only (35f3e67)
2. ~~Malformed config fails open~~ → `FenceConfigError` raised, fail-closed (35f3e67)
3. ~~JobFences not closed~~ → `extra="forbid"` on model (35f3e67)
4. ~~Five applicators diverge~~ → all 5 use `enforce_change_set` (a2e6c0c)
5. ~~No production callers~~ → 5 applicators call `enforce_change_set` (a2e6c0c)
6. ~~Artifact writer uses write_text~~ → `write_file_atomically` + O_NOFOLLOW + uuid (f1ce7a4)
7. ~~Exception leaks abs paths~~ → `_redact_path` in FenceViolationError (f1ce7a4)
8. ~~repo_applicator no job_fences~~ → `check_and_apply_to_repo` propagates (a2e6c0c)
9. ~~patch_apply no Evidence~~ → writes via `enforce_change_set` (a2e6c0c)
10. ~~do_continue uses APPLY_FAILED~~ → `FENCE_VIOLATION` stop reason (a2e6c0c)

## Final closure findings — ALL CLOSED
1. Non-canonical review package → canonical Evidence via `create_manual_completion_bundle`
2. repo_applicator job-scoped Evidence → `check_and_apply_to_repo` passes job_id + evidence_dir
3. Diagnostic path leaks → `_sanitize_diagnostic` regex-based redaction (POSIX/Win/UNC/file URI)
4. Allow-list violation provenance → `_match_violation_rule` returns rule_source + applicable_rules
5. Strict JobFences validation → Pydantic model_validator (trim, reject empty/non-string/nested)
6. Real production E2E → sanitizer, allow-list provenance, JobFences validation, job-scoped Evidence tests
7. Canonical ZIP → via `create_manual_completion_bundle` + `make_review_zip.sh`

## Next
Pending external acceptance. F017 stays `[~]`.
