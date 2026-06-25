# Live Review — Steps 4887-4895: Job Target Guard Pre-Apply Closure v6

Reviewer: parallel reviewer (independent; owns verdict).
Builder must NOT write reviewer verdicts. Builder must NOT self-merge.
Builder must NOT mark findings as resolved.
Timestamp: 2026-06-25

## Verdict (reviewer-owned)
(pending)

## Commit reviewed
(pending — awaiting push)

## PR reviewed
(pending)

## Protocol compliance
(pending)

## Worker 5-minute quiet-window assessment
(pending)

## Reviewer 10-minute quiet-window assessment
(pending)

## Findings

### R-3201 Blocker — Workspace apply happens before job-level target guard
(pending — awaiting reviewer)

### R-3202 Blocker — Target mutation block leaves applied manifest
(pending — awaiting reviewer)

### R-3203 High — Workspace receives staged files after target mutation
(pending — awaiting reviewer)

### R-3204 Medium — Report implies blocked task was applied
(pending — awaiting reviewer)

### R-3205 Medium — Post-apply guard missing
(pending — awaiting reviewer)

### R-3206 Medium — Existing safety regresses
(pending — awaiting reviewer)

## Step assessments
(pending — awaiting reviewer)

## Architecture guard
(pending)

## Full suite result
(pending)

## Final recommendation
(pending)

---

## Builder Handoff — Steps 4887-4895

**Builder**: Claude (agent)
**Handoff timestamp**: 2026-06-25
**Branch**: feature/steps-3276-3355-job-fulfillment-spine-v0

### What changed

**Production code** (1 file, 1 function):

- `packages/orchestration/pingpong_job.py` — `run_job()`:
  - L931-938: Added pre-apply target repo guard (Step 4887). Runs `_check_target_repo_guard()` after completion gate passes but BEFORE `_strict_apply_to_workspace()`. If target mutated, task blocked with `target_repo_mutated:` error, no workspace apply, no proof summary.
  - L952-958: Converted existing post-workspace-apply target guard to defense-in-depth (Step 4889). Error string changed from `target_repo_mutated` to `target_repo_mutated_after_apply` to distinguish from pre-apply detection.

**Correct order now**:
1. Completion gate (L922-927)
2. Pre-apply target guard (L931-938) — NEW
3. Workspace apply (L940-948)
4. Post-apply target guard (L952-958) — defense-in-depth
5. Proof summary (L961-974)

**Tests** (1 file, +18 tests):

- `tests/orchestration/test_job_task_runner.py` — 181 tests (was 163):
  - `TestPreApplyTargetGuard` (6 tests): mutation blocks job, no workspace apply, no applied manifest, task 2 skipped, no proof summary, error says "target_repo_mutated" not "after_apply"
  - `TestPreApplyTargetGuardReport` (4 tests): JSON report shows blocked, no applied manifest, text report shows blocked, no proof summary in report
  - `TestPostApplyTargetGuard` (2 tests): post-apply mutation caught with "after_apply" error, changed files reported
  - `TestTargetMutatedResultGatePreserved` (4 tests): result.target_mutated=True still blocks at completion gate, no manifest, no proof summary, task 2 skipped
  - `TestCommandPathPreApplySmoke` (2 tests): handler-level mutation blocks, clean run unaffected

### Edited files and line ranges

| File | Lines changed | What |
|------|--------------|------|
| `packages/orchestration/pingpong_job.py` | L931-938 (new), L952-958 (modified) | Pre-apply guard + post-apply defense-in-depth |
| `tests/orchestration/test_job_task_runner.py` | L1-8 (docstring), L2433-2712 (new) | 18 new tests in 5 classes |
| `.agent/plan.md` | full rewrite | Updated for Steps 4887-4895 |
| `.agent/context.md` | full rewrite | Updated for Steps 4887-4895 |

### Test results

| Suite | Result |
|-------|--------|
| Compile | Clean |
| Job task runner | 181 passed (18 new) |
| Job fulfillment | 109 passed (2x) |
| Fast lane | 571 passed |
| Runtime lane | 4/4 suites passed |
| Lint (ruff + mypy) | Clean |
| Full suite | 7923 passed, 0 failed, 8 skipped |

### Step results

| Step | Description | Result |
|------|-------------|--------|
| 4887 | Move job-level target guard before workspace apply | Done. Pre-apply guard at L931-938. |
| 4888 | Explicit pre-apply guard block manifest/evidence | Done. `apply_manifest` remains `None` when pre-apply guard blocks. No proof summary created. |
| 4889 | Post-apply target guard sanity check | Done. Defense-in-depth at L952-958. Error string `target_repo_mutated_after_apply`. |
| 4890 | Regression test: target mutation before apply blocks | Done. `TestPreApplyTargetGuard` (6 tests). |
| 4891 | Regression test: report does not claim apply | Done. `TestPreApplyTargetGuardReport` (4 tests). |
| 4892 | Preserve result.target_mutated=True gate behavior | Done. `TestTargetMutatedResultGatePreserved` (4 tests). |
| 4893 | Preserve continuation config, reviewer evidence, token policy | Done. All v13-v15 tests pass (181 total). |
| 4894 | Preserve successful job flow and existing safety | Done. Full suite 7923 pass. |
| 4895 | Architecture guard and handoff | Done. All guards clean. |

### Architecture guard results

- No workspace apply before target guard: CLEAN (pre-apply guard at L931-938)
- No task applied after target mutation: VERIFIED
- No apply_manifest.status="applied" after target mutation: VERIFIED
- No proof summary after target mutation block: VERIFIED
- No task applied with reviewer_output=None: VERIFIED
- No task applied without reviewer verdict: VERIFIED
- No task applied when reviewer verdict is not pass: VERIFIED
- No task applied when reviewer pass includes findings: VERIFIED
- No task applied when test_passed=False: VERIFIED
- No task applied when target_mutated=True: VERIFIED
- Completion gate does NOT rely only on final_status: VERIFIED (8 conditions)
- No paused continuation losing config: VERIFIED
- No explicit --builder fake ignored: VERIFIED
- No unbounded context: VERIFIED
- No full repo in prompt: VERIFIED
- No automatic real repo promotion: CLEAN
- No shell=True: CLEAN
- No git commit/push/reset/checkout: CLEAN
- No env/API key leakage: CLEAN
- No .agent product dependency: CLEAN

### What this proves

- Target repo mutation is caught BEFORE workspace apply
- No staged files enter job workspace after target mutation
- Report does not claim workspace apply after target mutation block
- Proof summary is not created after target mutation block
- Post-apply defense-in-depth catches mutations during workspace apply
- result.target_mutated=True still blocks at completion gate (before target guard)
- Existing reviewer evidence gate, continuation config, and token policy intact
- Existing safety invariants preserved across full suite

### What this does not prove

- Real Claude provider behavior (tests use FakeProvider)
- Network resilience or timeout behavior
- Real git operations (product code has no git)
- Multi-process concurrency safety
- Performance under load

### Job Runner readiness for real 2-task Claude dogfood

Pre-apply target guard was the last known safety-ordering bug. All safety gates now fire in correct order:
1. Completion gate (8 independent conditions)
2. Pre-apply target guard (real target repo check)
3. Strict workspace apply (artifact validation)
4. Post-apply target guard (defense-in-depth)
5. Proof summary (only after all guards pass)

Remaining prerequisites for real dogfood:
- Real Claude provider integration (not FakeProvider)
- Real test command execution
- Real file staging from Claude output
- Human confirmation of first dogfood run parameters

### 5-minute quiet-window check

**Check timestamp**: 2026-06-25
**Activity seen**: No reviewer findings appeared during implementation.
**Findings addressed**: N/A (no findings yet)
**Findings still open**: All 6 finding slots in review template awaiting reviewer.
