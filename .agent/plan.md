# Plan — F017 Scope Fences — Final Acceptance Repair

## Goal
Close 7 acceptance findings: rule-level provenance, job-scoped durable
Evidence, typed persistence failures, strict glob contracts, CLI
provenance completion, real 5-path E2E verification, one clean
final-HEAD READY_FOR_REVIEW package.

## Branch state (Scope 1)
Base: `fe9898a`
HEAD: `0b71df6` (18 commits; 17 F017 + 1 operator roadmap detail)
Tree: clean
Commit `c69e05b` confirmed: docs/STATUS/agent-state only.
Commit `0b71df6` confirmed: roadmap feature details only (T14–T17).
Neither touches F017 code/tests.

## Scope 1 — package/HEAD reconciliation
- Inspect branch, record base/HEAD/count/tree state
- Confirm c69e05b and 0b71df6 contents — no F017 code change
- Final sequence: implement → test → docs → commit all → clean tree
  → Evidence for exact HEAD → ZIP for exact HEAD → no post-ZIP commit

## Scope 2 — typed provenance and durable job Evidence
- EffectiveFenceRule: pattern, kind (allow|deny|builtin), source
  (per_job|environment|project|default|builtin|dynamic_builtin), reason
- EffectiveFenceResult: spec, allow_rules, deny_rules, builtin_rules,
  warnings, diagnostics, case_sensitivity, source (compat)
- Strict glob contracts: trim whitespace, reject empty/whitespace-only,
  reject nested containers, reject boolean/numeric, no str() coercion
- Deterministic violation ordering: sort by (path, operation, role)
- Artifact schema v2: schema_version, rule info per violation
  (matched_rule, rule_kind, rule_source, path_kind, reason_code)
- Persistence failures: FenceViolationError with persistence_status,
  secondary_diagnostic; artifact_path may be None
- All 5 applicators preserve fence_violation on Evidence failure
- CLI: display per-rule provenance, missing repo → nonzero exit

## Scope 3 — production E2E closure
- source_apply: project/env/job deny, persistence failure
- patch_apply: project/env/job deny, job-scoped artifact
- job_fulfillment: multi-intent atomicity, nothing promoted on deny
- do_continue: fence_violation stop reason, job-scoped artifact
- repo_applicator: job ID reaches Evidence, job-scoped artifact
- CLI: per-rule provenance, JSON, missing repo, malformed config
- Deterministic ordering regression test
- Regression matrix (all 11 suites + compileall + docs + git diff)
- job_fulfillment baseline comparison

## Scope 4 — final clean Evidence and package
- Truthful docs/STATUS/agent state update
- Commit all source/test/docs/state files
- Confirm clean tree
- Fresh canonical Evidence (3 tasks: T001/T002/T003)
- Build READY_FOR_REVIEW ZIP for exact HEAD
- Verify SHA-256
- No commit after packaging

## Commits
1. fix(f017): rule-level provenance + strict glob contracts
2. fix(f017): job-scoped durable Evidence + typed persistence failures
3. fix(f017): CLI missing-context and provenance completion
4. test(f017): real five-path production E2E + fulfillment diagnosis
5. docs(f017): final implementation state + Evidence + READY_FOR_REVIEW ZIP

## Current Step
All scopes complete. Commits #1–#4 done. Building commit #5 (docs + Evidence + ZIP).

## Constraints
- No Fable/subagents/providers/network/Docker. Manual only.
- Do not amend/squash existing F017 commits.
- Do not push, create PR, merge, modify main, or start F018.
- Do not weaken, delete, skip, or xfail tests.
- F017 stays `[~]`, F018 stays `[ ]`.
