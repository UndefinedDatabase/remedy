# Plan — F017 Scope Fences — Final Closure

## Goal
Close 7 findings from non-canonical package review: repo_applicator
job-scoped Evidence, persistence diagnostic redaction, allow-list
provenance, strict JobFences validation, real production E2E tests,
one canonical full Remedy READY_FOR_REVIEW package.

## Branch state
Base: `fe9898a`
HEAD: `ee156ab` (23 commits; 17 original + 1 roadmap + 5 acceptance repair)
Previous ZIP: non-canonical (6 members, missing root manifest/subject/
content proof/commit chain/patches/final verifier/token truth/gates).
Post-ZIP commit problem: ZIP declared HEAD 705ab36 but ee156ab followed.

## Scope 1 — remaining model/provenance/redaction contracts ✓
- ✓ repo_applicator: check_and_apply_to_repo passes job_id and evidence_dir
- ✓ _sanitize_diagnostic: regex redaction of POSIX/Win/UNC/file URI paths
- ✓ _match_violation_rule: 4-tuple with applicable_rules for allow-list violations
- ✓ write_fence_violations_artifact: unpacks 4-tuple, includes applicable_rules
- ✓ enforce_change_set: uses _sanitize_diagnostic for persistence errors
- ✓ JobFences Pydantic model_validator: trim, reject empty/non-string/nested

## Scope 2 — E2E tests ✓
- ✓ _sanitize_diagnostic mutation tests (POSIX/Win/UNC/file-uri/control/length/multi)
- ✓ Allow-list provenance: rule_source + applicable_rules in artifact
- ✓ JobFences strict validation: trim, empty, int, bool, nested, dict
- ✓ repo_applicator job-scoped Evidence via check_and_apply_to_repo
- ✓ Persistence failure via check_and_apply_to_repo
- ✓ All 289 fence tests passing (test_fences + test_applicator_fences + test_fence_e2e)

## Scope 3 — regression proof, STATUS/docs/state, final package
- ✓ Updated context.md, live_review.md, plan.md
- Commit #1 + #2 + #3
- Confirm clean tree
- Fresh canonical Evidence via create_manual_completion_bundle
- Build canonical ZIP via make_review_zip.sh
- Verify SHA-256
- No commit after packaging

## Commits
1. fix(f017): repo-applicator job Evidence + diagnostic sanitizer + provenance + model validation
2. test(f017): real production E2E for all five paths + CLI + regression
3. docs(f017): final state + canonical Evidence + READY_FOR_REVIEW package

## Current Step
Scope 3: committing and packaging.

## Constraints
- No Fable/subagents/providers/network/Docker. Manual only.
- Do not amend/squash existing F017 commits.
- Do not push, create PR, merge, modify main, or start F018.
- Do not weaken, delete, skip, or xfail tests.
- F017 stays `[~]`, F018 stays `[ ]`.
