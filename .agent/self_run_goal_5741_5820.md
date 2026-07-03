# Steps 5741-5820: Sticky Builder/Reviewer Repair Loop v1 + Final Job Review v1 + Token-Cost Policy Evidence

## Product goal

Implement honest evidence taxonomy, sticky per-task builder/reviewer repair loops,
final job-level review loop, token-cost policy evidence, and tighten configured vs
actual evidence separation. This is core Remedy workflow infrastructure.

## Hard constraints

- Do NOT fake provider token usage.
- Do NOT fake provider/model data.
- Do NOT invent prompt/provider evidence for manual repair tasks.
- Do NOT reuse old evidence as proof.
- Do NOT auto-push or auto-merge.
- Do NOT use variable names or strings containing `secret`, `password`, `token`, `key`, `credential`, `api_key`, `SECRET`, `SYSTEM PROMPT`, `API_KEY` in test fixtures.
- Do NOT label estimated tokens as exact/actual.
- Do NOT copy estimated values into `actual_*` fields.
- Do NOT copy configured values into actual values unless they are truly the same source.
- If prompt_trace has zero prompts and provider_call_count is zero, do not label the task as provider-backed.
- If work was operator-built, label it `operator_built_no_provider` or `manual_operator_repair`.

---

## Task 1: Evidence execution mode taxonomy

### Files allowed

- `packages/orchestration/evidence_mode.py` (new)
- `tests/orchestration/test_evidence_mode.py` (new)

### Summary

Create an evidence execution mode taxonomy module. Each task's evidence must declare
its execution mode: `provider_backed`, `fake_provider_test`, `manual_operator_repair`,
`operator_built_no_provider`, or `unknown`.

Provide a function `classify_execution_mode(prompt_count, provider_call_count,
builder_provider, reviewer_provider)` that returns the correct mode based on actual
evidence signals. Also provide `build_task_execution_evidence(task_id, mode,
builder_provider, reviewer_provider, builder_identity, reviewer_identity, ...)` that
returns a structured dict with all required evidence fields.

### Acceptance

- `ExecutionMode` enum with 5 values: provider_backed, fake_provider_test, manual_operator_repair, operator_built_no_provider, unknown
- `classify_execution_mode()` returns correct mode based on prompt/provider signals
- `build_task_execution_evidence()` returns dict with: execution_mode, builder_provider, reviewer_provider, builder_identity, reviewer_identity, prompt_trace_available, provider_call_count, actual_provider_available, actual_model_available, actual_token_usage_available
- Zero prompts + zero provider calls + non-fake provider → operator_built_no_provider
- Fake provider → fake_provider_test
- Non-zero prompts + non-zero calls → provider_backed
- At least 10 tests covering: all 5 modes, mode classification logic, evidence dict completeness, field validation

---

## Task 2: Sticky per-task actor binding

### Files allowed

- `packages/orchestration/task_actor_binding.py` (new)
- `tests/orchestration/test_task_actor_binding.py` (new)

### Summary

Create task actor binding module. For each task, persist a `task_actor_binding` artifact
recording builder/reviewer identity, provider, model, session/instance IDs, round counts,
repair rounds, findings per round, and whether the same actor was used across rounds.

Provide `build_task_actor_binding(task_id, builder_provider, builder_model, reviewer_provider,
reviewer_model, rounds, repair_rounds, findings_by_round, repaired_by_round, unresolved,
same_builder_repairs, same_reviewer_re_review)`.

### Acceptance

- Returns dict with: task_id, builder_role, builder_provider, builder_model_configured, builder_identity, reviewer_role, reviewer_provider, reviewer_model_configured, reviewer_identity, sticky_across_rounds, rounds, repair_rounds, reviewer_findings_by_round, repaired_findings_by_round, unresolved_findings, same_builder_used_for_repairs, same_reviewer_used_for_re_review
- sticky_across_rounds = True only when same_builder_repairs and same_reviewer_re_review are both True
- At least 10 tests: basic binding, sticky true when same actors, sticky false when different actors, round tracking, finding tracking, unresolved tracking, identity recording, empty rounds, multiple repair rounds

---

## Task 3: Final job-level review

### Files allowed

- `packages/orchestration/final_job_review.py` (new)
- `tests/orchestration/test_final_job_review.py` (new)

### Summary

Create final job review module. After all task reviewers pass, run a final job-level
review that checks the original goal, task plan, all task summaries/diffs/verdicts,
test evidence, and proof gates. Persist final_job_review.json and final_job_review_findings.json.

Provide `build_final_job_review(job_goal, task_plan, task_summaries, task_diffs,
task_verdicts, test_evidence, gate_verdicts)` and `build_final_job_repair_loop(findings,
repair_tasks, re_review_verdict)`.

### Acceptance

- `build_final_job_review()` returns dict with: schema_version, job_id, job_goal, verdict, findings, task_count, tasks_reviewed, scope_check, acceptance_criteria_check, changed_files_match
- Verdict is PASS when no findings, NEEDS_REPAIR when findings exist but repairable, BLOCKED when critical issues
- `build_final_job_repair_loop()` tracks repair attempts with: findings_count, repair_tasks_created, repair_tasks_completed, re_review_verdict, rounds, budget_remaining
- At least 10 tests: pass case, findings case, repair loop, scope check, acceptance criteria check, blocker detection, repair budget exhaustion, re-review after repair, finding-to-task routing, empty task list

---

## Task 4: Token-cost policy evidence

### Files allowed

- `packages/orchestration/token_cost_policy.py` (new)
- `tests/orchestration/test_token_cost_policy.py` (new)

### Summary

Create token cost policy evidence module. Build a `token_cost_policy.json` artifact
that records per-role model policy, context budget, max rounds, repair budget,
actual/estimated token usage by role, provider call counts, cost risk findings,
and recommendations.

Provide `build_token_cost_policy(job_id, step_range, role_configs, token_truth,
prompt_trace_summary, max_rounds, repair_budget)`.

### Acceptance

- Returns dict with: schema_version, job_id, step_range, per_role_model_policy, context_budget_policy, max_prompt_chars_per_role, max_rounds, repair_budget, actual_available_by_role, estimated_tokens_by_role, provider_call_count_by_role, cost_risk_findings, recommendations
- cost_risk_findings includes warnings for: full repo context used unnecessarily, prompt traces exceed budget, actual token usage unavailable but reported as actual, estimated token usage missing
- At least 8 tests: basic policy, per-role breakdown, cost risk detection, budget tracking, missing actual warning, estimate recording, provider call counts, recommendations

---

## Task 5: Execution config evidence honesty

### Files allowed

- `packages/orchestration/execution_config_evidence.py` (modify)
- `tests/orchestration/test_execution_config_evidence.py` (modify)

### Summary

Tighten execution config evidence to clearly separate configured from actual.
Rename `actual_invocation_args` to `configured_invocation_args` when args are
planned/configured but not observed from provider output. Add `actual_invocation_args`
only when provider exposes them. Final verifier must not treat configured args as
proof of actual calls.

### Acceptance

- `configured_invocation_args` field for planned/configured args
- `actual_invocation_args` field only when provider output confirms them (null otherwise)
- `configured_model` vs `actual_model` separation maintained
- Evidence dict includes `actual_invocation_observed: bool` field
- At least 6 tests: configured only (actual null), actual when observed, separation maintained, no cross-contamination, field validation

---

## Task 6: Final verifier integration

### Files allowed

- `packages/orchestration/final_verifier.py` (modify)
- `tests/orchestration/test_final_verifier.py` (modify)

### Summary

Update final verifier to read and validate: execution mode per task, task actor
binding (sticky proof), token cost policy, final job review, and configured vs
actual invocation args. Warn or block on inconsistencies.

### Acceptance

- Final verifier reads execution_mode per task and validates consistency with prompt trace
- Final verifier reads task_actor_binding and warns if sticky proof missing
- Final verifier reads token_cost_policy and reports cost risk findings
- Final verifier reads final_job_review and blocks if final review has unresolved findings
- Final verifier warns if configured_invocation_args treated as actual
- At least 8 tests: execution mode consistency check, sticky actor warning, cost policy integration, final review integration, configured vs actual warning, mixed mode handling, all-pass case, multi-issue reporting

---

## Task 7: Review bundle and evidence consistency

### Files allowed

- `packages/orchestration/job_evidence.py` (modify)
- `scripts/build_review_manifest.py` (modify)
- `tests/orchestration/test_job_evidence.py` (modify)

### Summary

Ensure review bundle integrity: package_status=READY_FOR_REVIEW must not be emitted
with contradictory integrity fields. If current_content_hash_checked=false, either
package_status is not READY or the field accurately explains the status.

Write execution_mode, task_actor_binding, token_cost_policy, and final_job_review
artifacts into the evidence bundle.

### Acceptance

- package_status=READY_FOR_REVIEW requires current_content_hash_checked=true or field absent
- If hash check not run, package_status is READY_FOR_REVIEW_UNVERIFIED or similar honest status
- Evidence bundle includes execution_mode per task
- Evidence bundle includes task_actor_binding per task
- Evidence bundle includes token_cost_policy.json
- Evidence bundle includes final_job_review.json
- At least 6 tests: ready requires hash check, unverified status when unchecked, evidence artifacts present, bundle completeness

---

## Task 8: Pingpong loop and job integration

### Files allowed

- `packages/orchestration/pingpong_loop.py` (modify)
- `packages/orchestration/pingpong_job.py` (modify)
- `apps/cli/commands/do_cmd.py` (modify)
- `tests/orchestration/test_pingpong_integration.py` (new)

### Summary

Wire execution mode classification, task actor binding recording, and final job
review into the existing pingpong loop and job flow. After all tasks complete
in run_job, invoke final job review. Record execution mode and actor binding
per task during pingpong rounds.

### Acceptance

- run_pingpong records execution_mode based on actual prompt/provider activity
- run_pingpong records task_actor_binding per task
- run_job invokes final job review after all task reviewers pass
- run_job persists final_job_review.json and final_job_repair_loop.json if findings
- do_cmd wires final review results into evidence export
- At least 8 tests: execution mode recording, actor binding recording, final review invocation, repair loop trigger, evidence persistence, end-to-end flow
