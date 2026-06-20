# Live Review — Steps 3276-3355: Job Fulfillment Spine v0 — First Completed Fixture Job

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Timestamp: 2026-06-20

## Verdict (reviewer-owned)
**FAIL** @ cdc6950

9 files changed, +1447/-2. PR #100 open (builder did NOT self-merge).
Builder did NOT write reviewer verdict. Working tree clean.

## Reason for FAIL

5 Medium findings remain open. Per verdict rules: PASS requires zero Medium.
These findings are explicitly tracked for closure in the next block (Steps 3356-3435).

## Findings

### R-0189 Medium — Direct repo write bypass
Lines 621-625 of `job_fulfillment.py` write secondary artifacts directly to repo with
`sec_path.write_text(wo["content"])` instead of routing through `apply_patch_intent`.
All repo writes must go through existing patch apply gate.

### R-0190 Low — Catalog classification
`job.fulfill` cataloged as `write_metadata` but actually mutates repo through patch apply
+ direct writes. Should be `write_data` or `repo_write` classification.

### R-0191 Medium — Contract not used
`JobFulfillmentContract.check()` is defined but never called in `run_job_fulfill`.
The final_pass check at line 699-705 is a hand-written shortcut that duplicates
(and deviates from) the contract model. `completed_verified` should come from contract.

### R-0192 Medium — Blocked tests accepted as pass
Line 657: `test_res.status in ('passed', 'blocked')` accepts `blocked` as test pass.
Blocked means test runner had no scripts — not that tests passed.

### R-0193 Medium — Test exception swallowed
Lines 659-662: Exception in test runner sets `test_passed = True`. Any test runner
failure should NOT count as pass.

### R-0194 Medium — Incomplete proof accepted
Line 704: `record.proof_status in ("verified", "accepted", "incomplete")` allows
`incomplete` proof for final pass. Incomplete proof should block completion.

### R-0195 Low — Proposed task command syntax
Line 718: `remedy propose list --job-id {job_id}` — the `--job-id` flag syntax
may not match actual CLI argument parsing. Needs verification.

## Required checks (10 from review prompt)
1. Protocol compliance — **PASS**. Builder did not self-merge. Did not write verdict. Working tree clean.
2. Fulfillment status truth — **FAIL**. Contract not used (R-0191). Blocked tests accepted (R-0192). Exceptions swallowed (R-0193). Incomplete proof accepted (R-0194).
3. Task loop — **PASS**. 2 tasks (docs_update + evidence_summary). Repair task from finding visible.
4. Worker and review loop — **PASS**. Deterministic fixture worker/reviewer. One-finding mode works.
5. Approval/apply/test/proof — **FAIL**. Direct repo write bypass (R-0189). Blocked tests as pass (R-0192).
6. Report/status truth — **PASS**. Status shows completed, report shows code_applied=true after fulfillment.
7. Proposed next tasks — **PASS** (with R-0195 Low risk). 3 suggestions generated.
8. CLI and docs — **PASS**. `job fulfill` exists, requires `--fixture-demo`. Demo guide exists.
9. Command catalog and run contract — **PASS** (with R-0190 Low risk). Cataloged but classification debatable.
10. Safety — **FAIL**. Direct repo write outside patch apply (R-0189).

## Test evidence (reviewer-run)
- Compileall: 193 files clean
- Fulfillment tests: 34 passed, 0.18s
- Product spine: 72 passed, 0.12s
- Command catalog: 23 passed, 0.42s
- Run contract: 88 passed, 0.13s
- Boundary guard: 18 passed, 0.19s
- Review bundle: 90 passed, 1.69s
- Fast lane: 571 passed, 0.93s
- Runtime lane: 4/4 suites passed
- Lint: ruff clean, mypy clean (193 files)
- Full suite: 7097 passed, 0 failed, 8 skipped, 1 deselected, 200.18s

## Changed Line Map spot-check
- packages/orchestration/job_fulfillment.py (+731, NEW): Full fulfillment engine, model, contract, fixture components, storage, export. Verified.
- tests/orchestration/test_job_fulfillment.py (+495, NEW): 34 tests across model, planner, reviewer, contract, integration, CLI, docs, boundary. Verified.
- apps/cli/commands/job.py (+90): `_cmd_job_fulfill`, `_extract_job_truth` enriched with `code_applied`. Verified.
- apps/cli/command_catalog.py (+15): `job.fulfill` entry. Verified.
- docs/first-fulfilled-job-demo-v0.md (+94, NEW): Demo guide. Verified.
- docs updates: spine, quickstart, perfect demo doc. Verified.

## Top risks
5 Medium findings (R-0189, R-0191, R-0192, R-0193, R-0194) prevent PASS.
2 Low findings (R-0190, R-0195) are non-blocking.
All findings tracked in Steps 3356-3435 closure prompt.

## Merge readiness
NOT ready to merge. 5 Medium findings open.
Closure block (Steps 3356-3435) is expected to address these.
Do NOT merge PR #100 until closure block resolves findings.

NO PR unless user asks.

## Reviewer audit log
- Builder committed @ cdc6950. PR #100 opened. 9 files changed, +1447/-2.
- Diff reading: job_fulfillment.py (731 lines), test_job_fulfillment.py (495), job.py (+90), catalog (+15), demo doc (+94).
- All tests pass (7097 passed, 0 failed).
- Code review found 5 Medium + 2 Low findings.
- Verdict: **FAIL** @ cdc6950 — 5 open Medium findings.
