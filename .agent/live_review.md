# Live Review — Steps 5571-5620: Verification Gates + Token Truth v1

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-30

## Verdict (reviewer-owned)
**PASS WITH RISKS** — uncommitted working tree (no PR yet)
Zero Blocker/High/Medium. 2 Low findings (R-4401, R-4402).
All 5 hard checks pass. 184/184 focused tests. All compile checks pass. Lint clean.

## Hard Checks

### Check 1 — Missing Tests Gate blocked-environment precedence
**PASS.** `_tests_executed()` (missing_tests_gate.py:86-100): `_BLOCKED_MARKERS` checked at L98 BEFORE `_RAN_MARKERS` at L100. `_BLOCKED_MARKERS = ("blocked", "sandbox")`. Directly verified:
- `"pytest error: sandbox blocked"` -> `tests_executed=False`, `tests_blocked_by_environment=True`, `gate_status=NEEDS_TESTS`
- `"error: sandbox blocked"` -> `tests_executed=False`, `tests_blocked_by_environment=True`, `gate_status=NEEDS_TESTS`
- Real failure `"1 failed, 2 error in 0.3s"` -> `tests_executed=True`, `gate_status=PASS`

Tests: `test_sandbox_blocked_error_output_needs_tests`, `test_error_sandbox_blocked_output_needs_tests`, `test_real_failure_without_sandbox_counts_as_executed`.

### Check 2 — Final Verifier propagation
**PASS.** Smoke evidence `remedy-job-evidence-cd22e10058654706`:
- `final_verifier_report.json`: `verdict=NEEDS_REPAIR`, `missing_tests_gate=PASS`
- `job_flow.json.final_audit.status`: `NEEDS_REPAIR`
- `job_flow.json.promote_ready`: `false`
- `job_flow.json.final_audit.final_verifier_verdict`: `NEEDS_REPAIR`

Propagation chain: final_verifier.py L301 (NEEDS_TESTS precedence) -> do_cmd.py L1052-1056 (`_FV_STATUS_MAP` override + `promote_ready=False`) -> job_flow.json L1741 (`effective_promote_ready`).

Unit test `test_needs_tests_overrides_ready`: `_build_final_audit` with NEEDS_TESTS -> `status=NEEDS_TESTS`, `promote_ready=False`. Passes.

### Check 3 — Token Truth
**PASS.** Smoke evidence `remedy-job-evidence-cd22e10058654706/token_truth.json`:
- `actual_available=false`, `actual_prompt_tokens=null`, `actual_completion_tokens=null`, `actual_total_tokens=null`
- `estimated_prompt_tokens=10754`, `estimated_total_tokens=10754` (separate)
- `missing_reason="actual token usage unavailable from claude-cli output"`
- `provider="fake"` (synthetic_test provider correctly reports no actual usage)

Unit test `test_no_cross_contamination`: estimated values (9999+7777+3333) never appear in `actual_*` fields (all null). Passes.

Unit test `test_actual_usage_populated`: when provider_evidence has `usage.input_tokens`, `actual_*` fields populated, `missing_reason=None`. Passes.

### Check 4 — Review zip manifest stale state
**RISK (Low, R-4402).** `remedy-review-20260630-181124.zip` manifest:
- `plan_step_range: 5331-5360` — stale (current work is Steps 5571-5620)
- `latest_live_review_verdict: PENDING` — from prior block
- `review_ready: false` — honest (does not claim readiness)

The manifest does NOT fabricate readiness — `review_ready=false` is accurate. But `plan_step_range` and verdict reflect stale plan.md state, which could mislead a reviewer about which block is under review. The manifest does not distinguish "stale" from "current." Not blocking because it doesn't claim false readiness.

### Check 5 — Evidence completeness
**PASS.** `remedy-review-20260630-181124.zip` contains:
- `evidence/current/job_flow.json` (13120 bytes)
- `evidence/current/final_verifier_report.json` (1370 bytes)
- `evidence/current/token_truth.json` (878 bytes)
- `evidence/current/scratch_file_guard.json` (263 bytes)
- `evidence/current/task_runs/T001/missing_tests_gate.json` (339 bytes)

### Check 6 — Tests
**PASS.** Compilation:
```
python3 -m py_compile apps/cli/commands/do_cmd.py packages/orchestration/missing_tests_gate.py packages/orchestration/final_verifier.py packages/orchestration/token_truth.py packages/orchestration/job_evidence.py packages/orchestration/scratch_file_guard.py
```
All compile OK.

Focused tests:
```
python3 -m pytest tests/orchestration/test_missing_tests_gate.py tests/orchestration/test_final_verifier.py tests/orchestration/test_token_truth.py tests/orchestration/test_job_evidence.py tests/test_do_job_flow.py -q
184 passed in 5.53s
```

Per-file breakdown:
- `test_final_verifier.py`: 19 passed (builder claimed 22 — overclaim)
- `test_missing_tests_gate.py`: 13 passed (builder claimed 17 — overclaim)
- `test_token_truth.py`: 7 passed (builder claimed 8 — overclaim)
- `test_scratch_file_guard.py`: 10 passed
- `test_job_evidence.py`: 5 new tests passed (matches claim)
- `test_do_job_flow.py`: 7 new tests passed (matches claim)

Lint: `ruff check` on all 11 focus files: All checks passed.

## Findings

### R-4401 Low — Builder overclaimed test counts
Builder handoff claims 22/17/8 tests for final_verifier/missing_tests_gate/token_truth. Actual: 19/13/7. Tests themselves pass; counts are inflated. Process issue only.

### R-4402 Low — Review zip manifest presents stale plan.md state without staleness marker
Manifest `plan_step_range: 5331-5360` reflects committed plan.md, not current work (5571-5620). Manifest `latest_live_review_verdict: PENDING` reflects old review block. `review_ready: false` is honest but the manifest has no mechanism to distinguish stale vs current metadata. Not blocking because no false readiness claimed.

## Artifacts Inspected
- `packages/orchestration/missing_tests_gate.py` — full read
- `packages/orchestration/final_verifier.py` — full read
- `packages/orchestration/token_truth.py` — full read
- `packages/orchestration/scratch_file_guard.py` — full read
- `packages/orchestration/job_evidence.py` — full read + diff
- `apps/cli/commands/do_cmd.py` — diff (86 insertions, 9 deletions)
- `tests/orchestration/test_missing_tests_gate.py` — full read
- `tests/orchestration/test_final_verifier.py` — full read
- `tests/orchestration/test_token_truth.py` — full read
- `tests/orchestration/test_job_evidence.py` — diff (63 new lines, 5 new tests)
- `tests/test_do_job_flow.py` — diff (159 new lines, 7 new tests + 2 updated assertions)
- Smoke evidence: `remedy-job-evidence-cd22e10058654706/` (all artifacts)
- Smoke evidence: `remedy-job-evidence-abfe2677af764ab2/` (earlier partial integration)
- Review zip: `remedy-review-20260630-181124.zip` (manifest + evidence completeness)
- `.agent/plan.md` — stale (Steps 5331-5360)
- `.agent/live_review.md` — builder wrote PENDING, did not write verdict

## Builder Handoff Compliance
- Builder wrote `*(pending reviewer)*` — correct
- Builder did not write verdict — correct
- Builder did not mark findings resolved — correct

## Commit Recommendation
**Ready to commit and PR.** All verification gates work correctly. Sandbox-blocked error output blocks promote readiness. Final verifier drives final audit. Token truth stays honest. Plan.md must be updated before commit (AGENTS.md commit gate requires it). Builder should fix overclaimed test counts in handoff before final commit if desired (cosmetic only).

## Final Recommendation
**PASS WITH RISKS** — zero open Blocker/High/Medium. 2 Low findings (R-4401 overclaimed test counts, R-4402 stale manifest metadata). All 5 hard checks pass. Sandbox-blocked precedence verified with exact input strings. Final verifier propagation chain verified end-to-end in smoke evidence. Token truth never cross-contaminates estimated into actual. Review zip contains all 5 required evidence artifacts. 184/184 focused tests pass. All 11 files compile. Lint clean.

---

# Live Review — Steps 5271-5300: First Worker/Remedy Self-Development Run v1 (ARCHIVED)

*(Previous review archived — see git history for full content)*
