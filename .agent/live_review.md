# Parallel Review — Steps 655-669 (Independent Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 655-669 (Backend basis final closure — budget enforcement, events, worker CLI E2E)
Commit: 1296f66
Status: VERIFIED

## Test Results (independently run)
- All targeted suites: **164/164 passed** (4.14s)
  - `test_proposed_tasks.py`: 47 tests
  - `test_task_execution.py`: 33 tests (was 28 → +3 budget, +2 guard refine)
  - `test_worker_execution.py`: 23 tests (was 15 → +2 budget, +2 result v2, +2 blocked fixture, +2 events)
  - `test_propose_cli_runtime.py`: 11 tests (hardened assertions, bounded event read)
  - `test_worker_cli_runtime.py`: 5 tests (NEW — subprocess worker E2E via grouped entrypoint)
- 0 warnings (timeout mark removed)
- Worker claims 4427 full baseline (not independently verified — targeted suites confirm no regressions)

## Prior Findings Resolution

| Finding | Severity | Status |
|---------|----------|--------|
| R-640-001 (BudgetGate not used by worker) | medium | **RESOLVED** — BudgetGate imported and enforced in _run_via_task_execution. Tests: max_steps=0 blocks, max_steps=1 allows |
| R-640-002 (no token/time budget tests) | low | **RESOLVED** — test_tokens_exhausted, test_runtime_exhausted, test_record_step_tracks_all added |
| R-640-003 (list_jobs_safe unused by readiness) | low | **OPEN** — acknowledged at 90% in context. Readiness uses load_job_safe per-job. |
| R-640-004 (no execution_health section) | low | **OPEN** — finalize_readiness covers task state, no separate section. |
| R-640-005 (no blocked event test) | low | **RESOLVED** — test_blocked_event_written verifies task_execution_started + task_execution_blocked |
| R-640-006 (timeout mark not effective) | low | **RESOLVED** — @pytest.mark.timeout removed, bounded event read added instead |
| R-640-007 (broad Exception catch) | low | **RESOLVED** — separate JobNotFoundError + JobStoreError catches |
| R-610-002 (dashboard no reconcile) | low | **OPEN** — ui_server.py unchanged |
| R-595-003 (no lock timeout test) | low | **OPEN** — still no concurrent/timeout test |
| R-595-005 (double-load in lock) | low | **OPEN** — same pattern remains |

## Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 655 | Component status table in context. Stale risks removed. Current risks listed. 100% definition honest (Ollama/rollback/overnight/UI all 0% or paused) | PASS |
| 656 | 11 propose CLI tests pass. Timeout mark removed. Bounded event read [:5]. Better assertion messages. No shell=True. No lock leftovers | PASS |
| 657 | 5 worker CLI subprocess tests via `python -m apps.cli.grouped worker run`. Fixture complete, second-run, none, events, full loop. All timeout=10. No Ollama | PASS |
| 658 | WorkerResult v2: last_task_id, provider, work_performed, task_status, artifact_ids, blocked_reason, budget_status. export_worker_result_json includes all. redaction="safe_metadata_only". Tests verify | PASS |
| 659 | BudgetGate imported in _run_via_task_execution. can_execute() before execute_task(). record_step() after. max_steps/tokens/runtime flow from run_worker_once params. Tests: zero blocks, one allows | PASS |
| 660 | task_execution_started before executor call. task_execution_completed/blocked after. Both tested via function + subprocess. Payload: proposed_task_id, provider. Budget-block = no execution, no event (correct: policy, not task) | PASS |
| 661 | JobNotFoundError → "job_not_found". JobStoreError → "job_store_degraded". No broad `except Exception`. blocked_reason set on result | PASS |
| 662 | blocked_fixture → RunState.FAILED + blocked_reason persisted. Event: started + blocked. Finalize: False with blocked task. All 3 tests pass | PASS |
| 663 | Tested in 640-654: test_two_tasks_one_per_run (one per run, re-queue, completed after final). Queue entry transitions correct | PASS |
| 664 | test_blocked_task_finalize_false. test_finalize_after_task_completed. test_finalize_false_with_pending_task. Failed task blocks finalize | PASS |
| 665 | list_jobs_safe exists, list_jobs delegates. Readiness uses load_job_safe per-job. Corrupt individual job detected. Context says 90% — honest | PASS (with note) |
| 666 | test_propose_to_worker_completion via subprocess: propose→eval→approve→mat→enqueue→worker→completed. Events verified: evaluated+approved+materialized+started+completed. timeout=10. No shell=True | PASS |
| 667 | 10 guard tests: no ollama import (3), no source_apply (2), storage through helpers (1), no circular deps (2), autorun isolated (1), fixture path pure (1) | PASS |
| 668 | Component table: Ollama 0%, rollback 0%, overnight 0%, UI paused, list_jobs 90%. All "100%" backed by tests. No overclaim | PASS |
| 669 | 164 independently verified via wrapper. No background pytest. CLI no hang. Worker CLI E2E passes. 0 warnings | PASS |

## Scope Blockers

| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS |
| shell=True | PASS — not in any new code |
| External CDN | PASS |
| Ollama API | PASS — legacy autorun only |
| WebSocket | PASS |
| POST/PUT/DELETE | PASS — 405 enforced |
| Outbound HTTP | PASS |
| Raw content leaks | PASS — safe_summary[:200], blocked_reason[:200], description[:80] |
| UI redesign | PASS — backend only |
| Overnight autonomy execution | PASS — overnight_readiness still returns False |
| Docker/MemPalace | PASS |
| Provider-specific imports in core | PASS — 10 guard tests enforce |
| Claude/OpenAI provider | PASS |
| Git commit gate | PASS |

## Findings

### R-655-001
Status: Open
Severity: low
Area: readiness
Summary: list_jobs_safe still not consumed by readiness
Details: list_jobs_safe returns (jobs, degraded, skipped_files) but backend_readiness uses load_job_safe for the specific job. Multi-job listing corruption is invisible to readiness. Context honestly says 90%. Acceptable for single-job readiness context.
Evidence: `grep -rn "list_jobs_safe" packages/ tests/` — only storage.py internal
Expected fix: Add list_jobs_safe to a CLI command or readiness section for all-jobs health.

### R-655-002
Status: Open
Severity: low
Area: readiness
Summary: No execution_health section in backend_readiness
Details: Readiness has storage_health, proposal_health, build_readiness, finalize_readiness, overnight_readiness. No execution_health reflecting last execution time, provider used, or execution outcomes. finalize_readiness tracks pending/completed/blocked counts which is functionally sufficient.
Evidence: `grep -n "execution_health" packages/orchestration/proposed_tasks.py` returns empty
Expected fix: Optional — add execution_health section or note that finalize_readiness covers task state.

## Architecture Assessment

**Strengths:**
- ALL R-640-xxx findings resolved (5 of 7 fully resolved, 2 acknowledged with honest percentages)
- BudgetGate fully integrated: imported, checked before execution, recorded after, params flow through
- Worker CLI E2E via subprocess — not just function tests
- Started + completed + blocked events all exist and tested
- Separate exception handling: JobNotFoundError vs JobStoreError
- WorkerResult v2: caller knows which task ran, what happened, budget status
- Blocked fixture path fully tested: persistence, events, finalize blocks
- 10 modularity guard tests: comprehensive boundary enforcement
- Component status table is maximally honest: 0% where 0%, 90% where 90%
- Event reads bounded ([:5], [:10]) — no broad glob scans
- grouped.py CLI arg fixes enable subprocess tests

**Remaining Risks (all low):**
1. list_jobs_safe not in readiness (R-655-001)
2. No execution_health section (R-655-002)
3. Dashboard doesn't detect materialization mismatch (carry-forward R-610-002)
4. Lock timeout/concurrent test missing (carry-forward R-595-003)
5. Double-load in lock (carry-forward R-595-005)

## Final Verdict

**PASS**

- Propose runtime CLI status: **PASS** — 11 tests, no hang, bounded event reads, no timeout mark warning
- Worker CLI runtime status: **PASS** — 5 subprocess tests via grouped entrypoint, full loop proven
- WorkerResult contract status: **PASS** — task_id, provider, work_performed, task_status, artifact_ids, blocked_reason, budget_status. JSON export safe
- BudgetGate worker usage status: **PASS** — imported, enforced, tested (zero blocks, one allows). R-640-001 fully resolved
- Execution events status: **PASS** — started + completed/blocked events. Both tested via function + subprocess. Blocked path verified
- Exception handling status: **PASS** — separate JobNotFoundError/JobStoreError. No broad catch. R-640-007 resolved
- Blocked task persistence status: **PASS** — RunState.FAILED + blocked_reason. Finalize blocks. Event written
- Multi-task queue status: **PASS** — one per run, re-queue, completed after final (640-654 tests)
- Readiness/finalize status: **PASS** — pending/completed/blocked reflected. Corrupt blocks. No fake ready. list_jobs gap acknowledged at 90%
- Storage corruption status: **PASS** — list_jobs_safe exists. load_job_safe per-job in readiness. Honest 90% in context
- Runtime backend E2E status: **PASS** — propose→eval→approve→mat→enqueue→worker→completed via subprocess. Events chain: evaluated+approved+materialized+started+completed
- Baukasten/modularity status: **PASS** — 10 guard tests. No provider imports in core. Autorun isolated. No circular deps
- 100% component list accuracy: **PASS** — Ollama 0%, rollback 0%, overnight 0%, UI paused, list_jobs 90%. All "100%" backed by tests
- Raw leak status: **PASS** — safe_summary[:200], blocked_reason[:200], description[:80], redaction="safe_metadata_only"
- Tests run: 164 independently verified via scripts/remedy_pytest.sh (47 proposed + 33 task_exec + 23 worker_exec + 11 propose_cli + 5 worker_cli)
- Full pytest: Worker reports 4427 passed (not independently verified — targeted suites confirm no regressions)
- Top remaining backend risks:
  1. list_jobs_safe not consumed by readiness (R-655-001 — low)
  2. No execution_health section in readiness (R-655-002 — low)
  3. Dashboard doesn't detect materialization mismatch (R-610-002 — low, carry-forward)
  4. Lock timeout/concurrent test missing (R-595-003 — low, carry-forward)
  5. Double-load in lock (R-595-005 — low, carry-forward)
- Merge readiness: **YES** — all prior medium findings resolved. 2 new low findings. Backend basis loop is proven end-to-end through both function tests and subprocess CLI. Budget enforced. Events complete (started+completed+blocked). Modularity guarded. 100% claims honest.

---

# Parallel Review — Steps 640-654 (Independent Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 640-654 (Backend basis completion — worker executes real Job.tasks)
Commit: 383bf23
Status: VERIFIED

## Test Results (independently run)
- `tests/orchestration/test_worker_execution.py` + `test_task_execution.py` + `test_proposed_tasks.py` + `test_propose_cli_runtime.py`: **143/143 passed** (2.26s)
- New test file: `test_worker_execution.py` — 15 tests covering worker execution, persistence, events, queue gate, finalize gate, readiness, full E2E loop
- 1 warning: `PytestUnknownMarkWarning` for `@pytest.mark.timeout(30)` — pytest-timeout not installed
- Worker claims 4406 full baseline (not independently verified — targeted suites confirm no regressions)

## Prior Findings Resolution

| Finding | Severity | Status |
|---------|----------|--------|
| R-625-001 (can_retry_task t/task var) | low | **RESOLVED** — `t` → `task` on line 213 |
| R-625-002 (BudgetGate only checks steps) | low | **RESOLVED** (class-level) — can_execute() now checks max_tokens + max_runtime. **BUT**: worker does not use BudgetGate (see R-640-001) |
| R-625-003 (execution port not wired) | info | **RESOLVED** — _run_via_task_execution in worker_queue.py uses execute_task() |
| R-610-001 (queue gate no materialization) | medium | **RESOLVED** — _has_unresolved_proposals now checks approved_not_materialized |
| R-610-002 (dashboard no reconcile) | low | **OPEN** — ui_server.py unchanged |
| R-595-003 (no lock timeout test) | low | **OPEN** — still no concurrent/timeout test |
| R-595-005 (double-load in lock) | low | **OPEN** — same pattern remains |

## Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 640 | "Basis complete" defined concretely (9 items). Stale risks removed. Current risks listed (6). context/plan/live_review updated | PASS |
| 641 | 11 subprocess tests pass. subprocess timeout=10 on all. No shell=True. No shared state. No lock held. `@pytest.mark.timeout(30)` added but plugin not installed (R-640-006) | PASS (with note) |
| 642 | can_retry_task fixed (t→task). BudgetGate can_execute checks tokens/runtime. BUT: no tests for max_tokens_exhausted or max_runtime_exhausted | **PARTIAL** (see R-640-002) |
| 643 | list_jobs_safe() returns (jobs, degraded, skipped). Not silently skipped. No traceback. BUT: readiness does not use list_jobs_safe | **PARTIAL** (see R-640-003) |
| 644 | _run_via_task_execution: imports task_execution (provider-neutral), finds pending task, creates TaskExecutionRequest, calls execute_task(), saves Job. No provider-specific imports. No source_apply | PASS |
| 645 | Executes first pending task, breaks. Remaining>0 → re-queue. Remaining==0 → completed. test_two_tasks_one_per_run proves one per run. Provider none → no_work | PASS |
| 646 | Task.status=COMPLETED + execution_summary[:200] + artifact_ids + provider persist. Reload tests verify. No raw output stored. No duplication on second run | PASS |
| 647 | task_execution_completed event via RunLogWriter. proposed_task_id + provider + artifact_count + token_count in metadata. BUT: no blocked execution event test through worker | **PARTIAL** (see R-640-005) |
| 648 | approved_not_materialized blocks queue (tested). Materialized allows (tested). Corrupt blocks (existing). Rejected/deferred safe | PASS |
| 649 | can_finalize blocks pending. After worker completion: finalize=True. backend_readiness computes pending from Job.tasks → passes to can_finalize. Blocked/failed blocks. Corrupt blocks | PASS |
| 650 | storage/build/finalize/overnight separated (from 627). Pending/completed/blocked reflected in finalize_readiness. No fake ready. BUT: no explicit execution_health section | **PARTIAL** (see R-640-004) |
| 651 | BudgetGate class enforces tokens/runtime. BUT: worker_queue.py has ZERO references to BudgetGate. Worker does not check budget before executing. max_steps=0 does not prevent execution | **FAIL** (see R-640-001) |
| 652 | test_propose_to_completion: propose→evaluate→approve→materialize→enqueue→worker fixture→completed→finalize→events. Full backend loop proven. No Ollama. No shell=True | PASS |
| 653 | Worker imports task_execution, not providers. Legacy autorun isolated in _run_via_legacy_autorun. No source_apply. Adding provider: add to _EXECUTORS dict only | PASS |
| 654 | Worker claims 4406 passed. 143 independently verified. Tests via wrapper. No background pytest. live_review has step log. But "basis complete" while budget gate unused by worker | **PARTIAL** |

## Scope Blockers

| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS |
| shell=True | PASS — not in any new code |
| External CDN | PASS |
| Ollama API | PASS — ollama routed to legacy autorun, not task_execution |
| WebSocket | PASS |
| POST/PUT/DELETE | PASS — 405 enforced |
| Outbound HTTP | PASS |
| Raw content leaks | PASS — safe_summary[:200], blocked_reason[:200], description[:80] |
| UI redesign | PASS — backend only |
| Overnight autonomy execution | PASS — overnight_readiness still returns False |
| Docker/MemPalace | PASS |
| Provider-specific imports in core | PASS — _run_via_task_execution imports only task_execution + storage + models |
| Claude/OpenAI provider | PASS |
| Git commit gate | PASS |

## Findings

### R-640-001
Status: Open
Severity: medium
Area: budget
Summary: BudgetGate not used by worker — execution has no budget check
Details: worker_queue._run_via_task_execution() calls execute_task() directly without importing or checking BudgetGate. BudgetGate(max_steps=0) does not prevent execution. BudgetGate(max_steps=1) does not limit worker. The class was updated (R-625-002 fix) to check tokens/runtime, but the worker ignores it entirely. `grep -c "BudgetGate" packages/orchestration/worker_queue.py` returns 0.
Evidence: worker_queue.py has zero references to BudgetGate. _run_via_task_execution calls execute_task without any budget check.
Expected fix: Import BudgetGate in _run_via_task_execution. Create gate from request params. Call can_execute() before execute_task(). Call record_step() after.

### R-640-002
Status: Open
Severity: low
Area: budget
Summary: No tests for BudgetGate max_tokens or max_runtime enforcement
Details: BudgetGate.can_execute() was updated to check max_tokens and max_runtime_seconds. But TestBudgetGate only has 4 tests — all for max_steps (no_budget, allows, exhausted, has_budget). No test exercises `max_tokens_exhausted` or `max_runtime_exhausted` return values.
Evidence: `grep -n "max_tokens\|max_runtime\|elapsed" tests/orchestration/test_task_execution.py` returns empty
Expected fix: Add test_tokens_exhausted and test_runtime_exhausted to TestBudgetGate.

### R-640-003
Status: Open
Severity: low
Area: readiness
Summary: list_jobs_safe not used by readiness or any consumer
Details: list_jobs_safe() was added to storage.py (Step 643) and list_jobs() delegates to it. But no readiness function, dashboard, or CLI command calls list_jobs_safe directly. The degraded/skipped information is only available if a caller explicitly uses list_jobs_safe instead of list_jobs. backend_readiness uses load_job_safe (single job), not list_jobs_safe.
Evidence: `grep -rn "list_jobs_safe" packages/ tests/` shows only storage.py internal usage
Expected fix: Either expose job store degradation in backend_readiness via list_jobs_safe, or add a CLI command that uses it.

### R-640-004
Status: Open
Severity: low
Area: readiness
Summary: No execution_health section in readiness
Details: backend_readiness has 5 sections: storage_health, proposal_health, build_readiness, finalize_readiness, overnight_readiness. No execution_health section reflecting worker execution state (last execution time, provider, pending/completed task counts with execution metadata). finalize_readiness reflects pending/completed/blocked counts but without execution context.
Evidence: `grep -n "execution_health" packages/orchestration/proposed_tasks.py` returns empty
Expected fix: Add execution_health section or fold execution state into finalize_readiness with more detail.

### R-640-005
Status: Open
Severity: low
Area: events
Summary: No test for blocked execution event through worker
Details: test_fixture_writes_event verifies task_execution_completed event. No test for task_execution_blocked event when execution is blocked (e.g., unavailable provider through task_execution port). The event code exists in _run_via_task_execution (event_name = f"task_execution_{exec_result.status}") but the blocked path is untested through the worker.
Evidence: `grep -rn "blocked.*event\|event.*blocked\|task_execution_blocked" tests/orchestration/test_worker_execution.py` returns empty
Expected fix: Add test that forces blocked execution through _run_via_task_execution and verifies event file.

### R-640-006
Status: Open
Severity: low
Area: runtime-cli
Summary: pytest.mark.timeout(30) not effective — plugin not installed
Details: `@pytest.mark.timeout(30)` added to TestSubprocessFullFlow.test_end_to_end but pytest-timeout plugin is not installed, producing `PytestUnknownMarkWarning`. The mark is ignored at runtime. Actual protection is subprocess timeout=10 on each _run() call, which is effective.
Evidence: Warning in test output: "PytestUnknownMarkWarning: Unknown pytest.mark.timeout"
Expected fix: Either install pytest-timeout or remove the decorator to eliminate the warning.

### R-640-007
Status: Open
Severity: low
Area: worker
Summary: Overly broad exception catch on job load in _run_via_task_execution
Details: Line 429 catches `(JobNotFoundError, Exception)` which is equivalent to catching all exceptions. Any error during job load (permission denied, disk full, JSON decode error) becomes "job_not_found" instead of surfacing the real cause. Should distinguish missing from corrupt/unreadable.
Evidence: worker_queue.py:429 — `except (JobNotFoundError, Exception)`
Expected fix: Catch JobNotFoundError separately, then catch specific exceptions (ValueError, OSError) with appropriate blocked_reasons.

## Architecture Assessment

**Strengths:**
- R-625-001, R-625-002 (class-level), R-625-003, R-610-001 all RESOLVED
- Full backend loop proven: propose→evaluate→approve→materialize→enqueue→worker→completed→finalize→events
- Worker correctly finds pending Job task, executes through port, saves result, emits event
- One task per run: clean re-queue pattern for remaining tasks
- Legacy autorun isolated in separate function — fixture uses modular path
- No provider-specific imports in core execution path
- 15 new tests covering all critical worker execution paths
- Persistence verified: status, summary, artifacts survive reload
- Queue gate now blocks approved_not_materialized (R-610-001 finally resolved)

**Remaining Risks:**
1. BudgetGate not used by worker (R-640-001) — mandate violation
2. Dashboard doesn't detect materialization mismatches (carry-forward R-610-002)
3. No token/time budget tests (R-640-002)
4. list_jobs_safe unused by readiness (R-640-003)
5. Lock timeout/busy path untested (carry-forward R-595-003)

## Final Verdict

**PASS WITH RISKS**

- Runtime CLI stability: **PASS** — 11 tests, unique UUIDs, subprocess timeout=10. Timeout mark cosmetic only (R-640-006)
- Storage corruption handling: **PASS** — list_jobs_safe added (not consumed by readiness — R-640-003)
- Task execution correctness: **PASS** — execute_task() through modular port, result mapped to RunState
- Worker execution status: **PASS** — _run_via_task_execution finds pending task, calls execute_task, saves Job. Fixture provider proven
- Persistence status: **PASS** — Task.status, execution_summary, artifact_ids, provider all survive reload
- Execution events status: **PASS** — task_execution_completed event with metadata (blocked path untested — R-640-005)
- Queue/finalize gate status: **PASS** — queue blocks approved_not_materialized (R-610-001 resolved). Finalize blocks pending tasks. Both tested
- Readiness status: **PARTIAL** — finalize_readiness reflects task state. No execution_health section (R-640-004). list_jobs_safe not integrated (R-640-003)
- Budget status: **FAIL** — BudgetGate class works (enforces steps/tokens/time). Worker does not use it (R-640-001). No token/time tests (R-640-002)
- E2E status: **PASS** — test_propose_to_completion covers full backend loop. Events verified. Job.tasks.status == COMPLETED
- Modularity status: **PASS** — task_execution imports only. Legacy autorun isolated. Guard tests pass. No provider coupling
- Raw leak status: **PASS** — safe_summary[:200], blocked_reason[:200], description[:80]. No raw output stored
- Tests run: 143 (97 proposed_tasks + 20 task_execution + 15 worker_execution + 11 subprocess) — all guarded via scripts/remedy_pytest.sh
- Full pytest: Worker reports 4406 passed (not independently verified — targeted suites confirm no regressions)
- Which backend parts are now 100%:
  - Proposed task lifecycle (propose→evaluate→approve/reject/defer→materialize)
  - True materialization into Job.tasks
  - Worker execution through modular port (fixture provider)
  - Task state persistence (status, summary, artifacts)
  - Execution events via RunLogWriter
  - Queue gate (unresolved + approved_not_materialized + corrupt)
  - Finalize gate (pending/blocked/approved_not_materialized/corrupt)
  - Runtime CLI subprocess tests
  - Atomic writes + file locking on proposal store
  - Storage data-root resolution (REMEDY_DATA_DIR)
- Which backend parts are NOT 100%:
  - Budget gate enforcement in worker (class exists, worker ignores — R-640-001)
  - Readiness execution_health section (R-640-004)
  - Dashboard mismatch detection (R-610-002)
  - Token/time budget tests (R-640-002)
  - Lock timeout/concurrent tests (R-595-003)
  - Blocked execution event verification (R-640-005)
  - Overnight readiness (correctly gated as not-ready)
- Top 5 remaining backend risks:
  1. BudgetGate not used by worker — execution unbounded (R-640-001)
  2. Dashboard doesn't detect materialization mismatches (R-610-002)
  3. No token/time budget tests (R-640-002)
  4. Lock timeout/busy path untested (R-595-003)
  5. Broad exception catch masks real job load errors (R-640-007)
- Answer: **Backend basis loop complete? YES for fixture provider.** propose→evaluate→approve→materialize→enqueue→worker→completed→finalize→events fully proven. Worker executes real Job.tasks through modular port. Persistence verified. BUT budget gate unused by worker — execution is unbounded.
- Answer: **Close to overnight autonomous builder? NO.** overnight_readiness correctly returns False. BudgetGate not consumed. Missing: rollback, real provider execution, budget enforcement.
- Merge readiness: **YES** — 4 prior findings resolved, 7 new findings (1 medium, 6 low/info), no scope blockers. Core backend loop is real and tested. Budget gap is significant but non-blocking for merge since overnight gate prevents autonomous execution.

---

# Parallel Review — Steps 625-639 (Independent Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 625-639 (Modular task execution port, fixture executor, readiness v2)
Commit: af2e021
Status: VERIFIED

## Test Results (independently run)
- `tests/orchestration/test_proposed_tasks.py` + `tests/orchestration/test_task_execution.py` + `tests/cli/test_propose_cli_runtime.py`: **128/128 passed** (2.03s)
- New test file: `test_task_execution.py` — 28 tests covering execution port, fixture/none executors, provider selection, budget gate, retry boundary, modularity guards
- Refactored: `test_propose_cli_runtime.py` — unique UUID per test via `env` fixture, no shared state
- New: `test_materialized_pending_task` in readiness tests — verifies build_ready=True with pending tasks
- Worker claims full baseline (not independently verified — targeted suites confirm no regressions)

## Prior Findings Resolution

| Finding | Severity | Status |
|---------|----------|--------|
| R-610-001 (queue gate no materialization check) | medium | **OPEN** — worker_queue.py unchanged |
| R-610-002 (dashboard no reconcile) | low | **OPEN** — ui_server.py unchanged |
| R-610-003 (origin_task_id missing from Task inputs) | low | **RESOLVED** — conditionally added in materialize_approved_task (proposed_tasks.py:609-612) |
| R-610-004 (Job load outside file_lock) | low | **RESOLVED** — load_job moved inside _file_lock in do_materialize (proposed_tasks.py:644) |
| R-595-003 (no lock timeout test) | low | **OPEN** — still no concurrent/timeout test |
| R-595-005 (double-load in lock) | low | **OPEN** — same pattern remains |

## Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 625 | context/plan current, readiness terms defined, 6 risks carried, live_review appended | PASS |
| 626 | Runtime CLI tests: `env` fixture creates unique UUID+Job per test, `_run()` helper with subprocess+REMEDY_DATA_DIR, no shared JOB_UUID. 11 pass reliably | PASS |
| 627 | backend_readiness v2: structured dict with storage_health, proposal_health, build_readiness, finalize_readiness, overnight_readiness. `_task_status_val` helper. `no_pending_work` blocker. 5 tests including new `test_materialized_pending_task` | PASS |
| 628 | TaskExecutionRequest: job_id, task_id, description, inputs, provider, mode, max_steps, max_runtime_seconds, max_tokens. TaskExecutionResult: status, outcome, artifact_ids, safe_summary, timestamps. TaskExecutor Protocol. execute_task() dispatches via get_executor() | PASS |
| 629 | FixtureTaskExecutor: deterministic completion with artifact_id (uuid hex[:12]), blocked path for `blocked_fixture` task_type, safe_summary bounded. No external calls. Tests verify both paths | PASS |
| 630 | Merged into 628-629. execute_task() dispatches to provider executor. Worker not wired yet — port defined, integration pending | PASS (see R-625-003) |
| 631 | Provider adapter: _EXECUTORS dict, get_executor() returns class instance. ALLOWED_PROVIDERS frozenset includes "ollama" but returns None (unavailable). NoneExecutor for explicit "none". Unknown → None → blocked result | PASS |
| 632 | Merged into 628. TaskExecutionResult has status field: no_work, completed, blocked. Lifecycle states in result, not in separate model | PASS |
| 633 | Merged into 628. safe_summary, started_at, completed_at in result. No separate event emission yet — result carries metadata | PASS |
| 634 | Merged into tests. Subprocess E2E already verifies Job.tasks persistence. Execution persistence not yet applicable (port not wired) | PASS |
| 635 | can_retry_task(): read-only, checks job/task existence, status (completed/pending/failed), reconciliation. Returns {ready, blockers, reason, required_human_action}. 3 tests | PASS (see R-625-001) |
| 636 | BudgetGate: max_steps, record_step, has_budget property, can_execute() → (bool, reason). Tests: no_budget, allows, exhausted, has_budget | PASS (see R-625-002) |
| 637 | overnight_readiness v2: extends blockers from storage_health + build_readiness sections, adds pending_tasks + blocked_tasks from finalize. Still always returns ready=False | PASS |
| 638 | 5 modularity guard tests: no ollama import in worker_queue/task_execution/proposed_tasks, no raw open in proposed_tasks, no source_apply in task_execution | PASS |
| 639 | Committed af2e021. 128 independently verified (targeted suites). No test_steps files. 2 new files, 3 modified Python files | PASS |

## Scope Blockers

| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS |
| shell=True | PASS — not in any new code |
| External CDN | PASS |
| Ollama API | PASS — in ALLOWED_PROVIDERS but get_executor returns None (unavailable) |
| WebSocket | PASS |
| POST/PUT/DELETE | PASS — 405 enforced |
| Outbound HTTP | PASS |
| Raw content leaks | PASS — safe_summary bounded, title[:80], reason[:200] |
| UI redesign | PASS — backend only |
| Overnight autonomy execution | PASS — read-only gate only, always False |
| Docker/MemPalace | PASS |
| Provider-specific imports in core | PASS — guard tests enforce no ollama/source_apply in core modules |

## Findings

### R-625-001
Status: Open
Severity: low
Area: retry-boundary
Summary: can_retry_task uses loop variable `t` instead of found `task` at line 210
Details: After `for t in job.tasks: if str(t.id) == task_id: task = t; break`, line 210 reads `status = t.status.value ...` using `t` (loop var) instead of `task` (found var). Correct due to break — when task is found, t == task. But fragile: if loop is refactored to not use break (e.g., generator), `t` would point to last task.
Evidence: task_execution.py:202-210
Expected fix: Change line 210 to `status = task.status.value if hasattr(task.status, "value") else str(task.status)`

### R-625-002
Status: Open
Severity: low
Area: budget-gate
Summary: BudgetGate.can_execute() only checks max_steps — ignores max_tokens and max_runtime_seconds
Details: BudgetGate has fields max_tokens and max_runtime_seconds, but can_execute() only checks max_steps. Token and time budgets are tracked (tokens_used incremented by record_step) but never enforced. Partial enforcement — steps gate works, token/time gates are structural placeholders.
Evidence: task_execution.py:172-177 — only max_steps checked
Expected fix: Add token/time checks to can_execute() or remove unused fields to avoid false confidence.

### R-625-003
Status: Open
Severity: info
Area: integration
Summary: Execution port defined but not wired into worker
Details: task_execution.py defines TaskExecutionRequest/Result, FixtureTaskExecutor, execute_task(), BudgetGate, can_retry_task(). But worker_queue.py has zero changes — the port exists as a standalone module. No worker state changes tied to Job.tasks execution. This is expected for this block (port definition before integration) but means "worker runs real tasks" is not yet proven end-to-end.
Evidence: `git diff 7cb6b7c..af2e021 -- packages/orchestration/worker_queue.py` returns empty
Expected: Worker integration in next block (640+).

## Architecture Assessment

**Strengths:**
- R-610-003 RESOLVED: origin_task_id + origin_recommendation_id conditionally in Task inputs
- R-610-004 RESOLVED: load_job inside _file_lock — concurrent materialization race eliminated
- TaskExecutor Protocol + get_executor() is clean provider abstraction — no core imports of providers
- FixtureTaskExecutor is truly deterministic: uuid-based artifact IDs, bounded summaries, no external calls
- BudgetGate is simple and testable: can_execute() before each step, record_step() after
- can_retry_task() is read-only — checks reconciliation before allowing retry
- Modularity guard tests enforce architecture boundaries at test time
- backend_readiness v2 structured sections give targeted diagnostics (not just flat blockers list)
- Runtime CLI tests refactored cleanly — each test isolated with unique UUID

**Remaining Risks:**
1. Queue gate doesn't enforce materialization (carry-forward R-610-001)
2. Dashboard doesn't detect materialization mismatches (carry-forward R-610-002)
3. Execution port not wired into worker (R-625-003)
4. BudgetGate token/time enforcement missing (R-625-002)
5. Lock timeout/busy path untested (carry-forward R-595-003)

## Final Verdict

**PASS WITH RISKS**

- Task execution port status: **PASS** — Request/Result models, Protocol interface, dispatch function
- Fixture executor status: **PASS** — deterministic, bounded, no external calls
- Provider adapter status: **PASS** — get_executor(), ALLOWED_PROVIDERS, ollama unavailable, NoneExecutor
- Budget gate status: **PASS** — max_steps enforcement works; token/time structural only (R-625-002)
- Retry boundary status: **PASS** — read-only, reconciliation-aware (minor t/task var issue R-625-001)
- Backend readiness v2 status: **PASS** — 5 structured sections, pending_tasks awareness
- Overnight readiness v2 status: **PASS** — always false, pending/blocked counted from structured readiness
- Modularity guards status: **PASS** — 5 guard tests enforce no provider imports in core
- Prior fix R-610-003 status: **RESOLVED** — origin_task_id in Task inputs
- Prior fix R-610-004 status: **RESOLVED** — Job load inside lock
- Worker integration status: **NOT YET** — port defined, worker not wired (R-625-003)
- Runtime CLI tests status: **PASS** — refactored with unique UUID per test, 11 pass
- Raw leak status: **PASS** — safe_summary bounded, task_description[:60] in fixture
- Tests run: 128 (97 proposed_tasks + 20 task_execution + 11 subprocess) — all guarded via scripts/remedy_pytest.sh
- Top 5 remaining risks:
  1. Execution port not wired into worker (R-625-003)
  2. Queue gate doesn't enforce materialization (R-610-001)
  3. BudgetGate only checks max_steps (R-625-002)
  4. Dashboard doesn't detect materialization mismatch (R-610-002)
  5. Lock timeout/busy path untested (R-595-003)
- Answer: **Close to worker executing real tasks? PARTIALLY.** Execution port is defined, fixture executor proves the interface, budget gate exists. But worker_queue.py is unchanged — no Job.tasks item is executed through the port yet. Need worker integration next.
- Answer: **Close to overnight autonomous builder? NO.** `overnight_readiness()` still correctly returns `ready: False`. Missing: worker execution wiring, rollback, execution proof. Budget gate exists but is not consumed by worker.
- Merge readiness: **YES** — 2 prior findings resolved, 3 new findings (2 low, 1 info), no blockers, execution port is architecturally sound

---

# Parallel Review — Steps 610-624 (Independent Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 610-624 (True Job.tasks materialization, runtime CLI, backend readiness)
Commit: 7cb6b7c
Status: VERIFIED

## Test Results (independently run)
- `tests/orchestration/test_proposed_tasks.py` + `tests/cli/test_propose_cli.py`: **120/120 passed** (0.27s)
- `tests/cli/test_propose_cli_runtime.py`: **11/11 passed** (1.87s) — SUBPROCESS via `python -m apps.cli.grouped`
- `tests/ui_contracts/` + `tests/ui_server/`: **584 passed** (7.65s)
- `tests/test_storage.py` + `tests/test_context_coverage.py`: **97 passed** (0.77s)
- `tests/orchestration/test_approval_queue.py` + reviewer-related: **98 passed, 1 skipped** (2.11s)
- Total independently verified: **910 tests**, zero failures
- Worker claims 4365 full baseline (not independently verified — targeted suites confirm no regressions)

## Prior Findings Resolution

| Finding | Severity | Status |
|---------|----------|--------|
| R-595-001 (CLI tests handler-only) | medium | **RESOLVED** — 11 subprocess tests in test_propose_cli_runtime.py, E2E flow verified |
| R-595-002 (queue/finalize ignores materialization) | medium | **PARTIALLY RESOLVED** — can_finalize() now blocks approved-not-materialized; queue gate unchanged |
| R-595-003 (no lock timeout test) | low | **OPEN** — still no concurrent/timeout test |
| R-595-004 (do_materialize orphans Task dict) | low | **RESOLVED** — do_materialize now creates real Task, appends to Job.tasks, saves Job |
| R-595-005 (double-load in lock) | low | **OPEN** — same pattern remains |

## Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 610 | context/plan current, stale risks removed, true risks carried, live_review appended | PASS |
| 611 | storage.py: `_DATA_DIR=None`, `_resolve_jobs_dir(root)`, `_atomic_write_job`, `JobStoreError`, `load_job_safe`, root= on all funcs | PASS |
| 612 | `_require_job` gate on evaluate/approve/reject/defer/materialize; list/show read-only, no gate; missing Job → error + exit | PASS |
| 613 | `do_materialize` loads real Job, creates `Task.model_validate(task_dict)`, appends to Job.tasks, saves Job, then marks ProposedTask. Test verifies Job.tasks has real task | PASS |
| 614 | `reconcile_materialized` checks both directions: missing_job_task + missing_proposal_marker. Corrupt store safe. 3 tests | PASS |
| 615 | `can_finalize()` now blocks approved_not_materialized. But worker_queue._has_unresolved_proposals unchanged — queue gate does NOT block | **PARTIAL** (see R-610-001) |
| 616 | 11 subprocess tests: list, evaluate, approve/reject/defer, materialize, errors, E2E flow. Via `python -m apps.cli.grouped`. No shell=True. Temp REMEDY_DATA_DIR | PASS |
| 617 | `emit_proposed_task_event` includes materialized_task_id in metadata. Event written after real Job task saved. E2E subprocess test verifies event file | PASS |
| 618 | Dashboard already has v2 (from 604) with approved_not_materialized/materialized/summaries. Does NOT call reconcile_materialized | **PARTIAL** (see R-610-002) |
| 619 | `can_finalize()` blocks approved_not_materialized + unresolved + degraded. Test verifies. Finalize passes only when all materialized | PASS |
| 620 | Same materialize path for all proposal sources. But `origin_task_id` not in materialized Task inputs | **PARTIAL** (see R-610-003) |
| 621 | `_atomic_write_job` (tempfile+fsync+rename), `JobStoreError` on corrupt, `load_job_safe` returns (None, True) on corrupt. storage test updated | PASS |
| 622 | `backend_readiness()` checks job store, proposal store, unresolved, approved_not_materialized, materialization consistency. 4 tests | PASS |
| 623 | `overnight_readiness()` always returns `ready: False`, `max_safe_autonomy_level: 0`. Hard-coded blockers: no_overnight_mode, no_rollback, no_budget. NO execution code | PASS |
| 624 | Worker claims 4365 passed. 910 independently verified. Subprocess tests included. No test_steps files | PASS |

## Scope Blockers

| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS |
| shell=True | PASS — not in any new code |
| External CDN | PASS |
| Ollama API | PASS |
| WebSocket | PASS |
| POST/PUT/DELETE | PASS — 405 enforced |
| Outbound HTTP | PASS |
| Raw content leaks | PASS — bounded fields everywhere |
| UI redesign | PASS — backend only |
| Overnight autonomy execution | PASS — read-only gate only |
| Docker/MemPalace | PASS |

## Findings

### R-610-001
Status: Open
Severity: medium
Area: queue-gate
Summary: Worker queue gate does not block on approved-not-materialized
Details: `can_finalize()` now blocks approved-not-materialized (Step 619 done). But `worker_queue._has_unresolved_proposals()` still only checks PROPOSED+EVALUATED via `count_unresolved_safe`. APPROVED_FOR_BUILD is terminal, not unresolved — the queue can schedule new work while approved proposals have not been materialized into Job.tasks. The finalize gate catches this, so jobs can't complete in this state, but the queue doesn't enforce the materialization step.
Evidence: `grep -n "materialized\|approved_not" packages/orchestration/worker_queue.py` returns empty. No changes to worker_queue.py in this commit.
Expected fix: Either add `list_approved_not_materialized` check to `_has_unresolved_proposals`, or document that queue intentionally allows work while awaiting materialization.

### R-610-002
Status: Open
Severity: low
Area: dashboard-contract
Summary: Dashboard does not detect materialization mismatch
Details: `_build_proposed_tasks_section` shows approved_not_materialized and materialized counts. But it does NOT call `reconcile_materialized()` to detect mismatches (ProposedTask marked materialized but Job.tasks missing the task). The `backend_readiness()` function does call reconcile, so the mismatch is detectable — just not from the dashboard view.
Evidence: `grep -n "reconcile" packages/orchestration/ui_server.py` returns empty
Expected fix: Add `reconcile_materialized()` call to dashboard section, or add a `/readiness` CLI command that exposes backend_readiness.

### R-610-003
Status: Open
Severity: low
Area: reviewer-rework
Summary: Materialized Task inputs missing origin_task_id
Details: `materialize_approved_task()` includes proposed_task_id, task_type, reason, source, risk, priority in Task inputs. But `origin_task_id` (which links rework proposals to original Tasks) is not included. Trace chain: Task.inputs.proposed_task_id → ProposedTask.origin_task_id → original Task. Direct link is missing, requiring two lookups.
Evidence: materialize_approved_task at proposed_tasks.py:603 — inputs dict does not include origin_task_id
Expected fix: Add `"origin_task_id": proposed.origin_task_id` to Task inputs dict.

### R-610-004
Status: Open
Severity: low
Area: materialization
Summary: Job loaded outside file_lock in do_materialize — concurrent materialization could lose Job tasks
Details: `do_materialize()` calls `job = load_job(job_uuid, root)` at line 638, BEFORE `with _file_lock(job_id, root):` at line 640. Two concurrent materializations of different proposals for the same job would both load the same Job state. The second materialization's `save_job(job, root)` would overwrite the first's added Task. The `_file_lock` only protects proposal store, not Job store.
Evidence: proposed_tasks.py:638 (`job = load_job(...)`) vs line 640 (`with _file_lock(...)`)
Expected fix: Move `job = load_job(job_uuid, root)` inside the `_file_lock` block. Or add a separate job-level lock.

## Architecture Assessment

**Strengths:**
- R-595-001 FULLY resolved: 11 subprocess tests through real CLI entrypoint, E2E verified
- R-595-004 FULLY resolved: `do_materialize` creates real Task, appends to Job.tasks, saves Job
- storage.py now mirrors proposed_tasks pattern: `_DATA_DIR=None`, `_resolve_jobs_dir(root)`, atomic writes, error types
- `_require_job` gate prevents mutations on non-existent Jobs
- Reconciliation detects mismatches in both directions (missing Job task, missing proposal marker)
- `backend_readiness` is comprehensive: job store, proposal store, unresolved, materialization consistency
- `overnight_readiness` is maximally honest: always false, explicit blockers, no execution code
- Subprocess E2E test proves full flow: propose → evaluate → approve → materialize → Job.tasks verified → events verified
- `can_finalize` now blocks approved-not-materialized — R-595-002 partially resolved

**Remaining Risks:**
1. Queue gate doesn't enforce materialization (R-610-001)
2. Dashboard doesn't detect materialization mismatches (R-610-002)
3. Materialized Task missing origin_task_id trace (R-610-003)
4. Job load outside file_lock — concurrent race possible (R-610-004)
5. Lock timeout/busy path untested (carry-forward R-595-003)

## Final Verdict

**PASS WITH RISKS**

- Job storage status: **PASS** — root= param, atomic writes, JobStoreError, load_job_safe
- Real Job.tasks materialization status: **PASS** — do_materialize creates real Task, appends to Job.tasks, saves Job, verifiable via tests
- Runtime CLI subprocess status: **PASS** — 11 subprocess tests, E2E flow, no shell=True
- Audit event status: **PASS** — events include materialized_task_id, verified in subprocess E2E
- Queue/finalize status: **PARTIAL** — finalize blocks approved-not-materialized; queue gate unchanged (R-610-001)
- Dashboard backend contract status: **PARTIAL** — materialization counts shown; mismatch detection not wired (R-610-002)
- Reviewer/rework status: **PARTIAL** — same materialization path, but origin_task_id not in Task inputs (R-610-003)
- Backend readiness status: **PASS** — comprehensive checks including reconciliation
- Overnight readiness gate status: **PASS** — always false, no execution, explicit blockers
- Raw leak status: **PASS** — bounded fields, title[:80], reason[:200], safe summaries
- Tests run: 120 handler + 11 subprocess + 584 UI + 97 storage/context + 98 reviewer = 910 (all guarded via scripts/remedy_pytest.sh)
- Full pytest: Worker reports 4365 passed (not independently verified — targeted suites confirm no regressions)
- Top 5 remaining backend risks:
  1. Queue gate doesn't enforce materialization (R-610-001)
  2. Job load outside file_lock — race possible (R-610-004)
  3. Dashboard doesn't detect materialization mismatch (R-610-002)
  4. origin_task_id missing from materialized Task (R-610-003)
  5. Lock timeout/busy path untested (R-595-003)
- Answer: **Close to overnight autonomous builder? NO.** `overnight_readiness()` correctly returns `ready: False`. Missing: rollback snapshots, token/time budgets, execution proof, overnight mode implementation. Backend stores and gates are production-grade, but autonomous execution is correctly gated as not-ready.
- Merge readiness: **YES** — 2 prior findings resolved, 4 new findings (1 medium, 3 low), no blockers, materialization is real

---

# Parallel Review — Steps 595-609 (Independent Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 595-609 (Backend reliability closure — audit trail, locking, materialization, centralized gates)
Commit: 3cb3f20
Status: VERIFIED

## Test Results (independently run)
- `tests/orchestration/test_proposed_tasks.py` + `tests/cli/test_propose_cli.py`: **110/110 passed** (0.25s)
- `tests/orchestration/test_approval_queue.py` + reviewer-related: **98 passed, 1 skipped** (2.36s)
- `tests/ui_contracts/`: **397 passed** (2.51s)
- `tests/ui_server/`: **187 passed** (5.23s)
- No regressions detected across any targeted suite
- Worker claims 4344 full baseline (not independently verified — targeted suites confirm no regressions)

## Prior Findings Resolution

| Finding | Severity | Status |
|---------|----------|--------|
| R-580-001 (CLI audit events dormant) | medium | **RESOLVED** — `_make_writer(job_id)` creates real RunLogWriter. `test_no_dormant_none_writer_in_cli` enforces. |
| R-580-002 (dashboard finalized duplication) | low | **RESOLVED** — `ui_server.py` now calls `can_finalize()`. Timeline guard test updated. |

## Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 595 | context/plan current, old blockers removed, true risks carried forward, live_review appended | PASS |
| 596 | "merged into 608" — no subprocess CLI tests exist; all tests call COMMAND_HANDLERS directly | **PARTIAL** (see R-595-001) |
| 597 | `_make_writer` creates RunLogWriter from UUID; all 5 transition handlers use real writer; `test_evaluate_writes_event` verifies event file; `test_no_dormant_none_writer_in_cli` guards regression | PASS |
| 598 | `fcntl.flock` with LOCK_EX\|LOCK_NB + 5s bounded retry; all read-modify-write ops locked; lock released on exception; 4 locking tests | PASS |
| 599 | `_STORE_DIR = None` default; `_resolve_store_dir` calls `proposed_tasks_dir()` at call time; tests verify REMEDY_DATA_DIR and root= override | PASS |
| 600 | Dashboard calls `can_finalize()` directly; `is_finalized = job_says_done and finalize_ok`; timeline guard test updated to check `can_finalize` | PASS |
| 601 | `materialized_task_id`, `materialized_at`, `is_materialized` property on ProposedTask; `do_materialize` sets both under lock; tests cover happy/guard/double-materialize | PASS |
| 602 | `propose.materialize` in catalog + handler; `--task-id` and `--all` modes; emits audit event; 4 CLI tests | PASS |
| 603 | "merged into 601/602" — queue gate (worker_queue.py) UNCHANGED; `can_finalize` doesn't check materialization; approved-not-materialized doesn't block | **PARTIAL** (see R-595-002) |
| 604 | `approved_not_materialized`, `materialized`, `summaries` in dashboard; per-task materialization status; bounded fields; no raw leaks | PASS |
| 605 | "merged into 597" — reviewer already uses root= param from 580-594; no direct Task bypass; no changes in this commit | PASS (pre-existing) |
| 606 | "merged into tests" — CLI/queue/finalize/dashboard all handle corruption via ProposedTaskStoreError; existing tests cover all surfaces | PASS |
| 607 | "merged into tests" — 4 locking tests (sequential adds, update+add, approve+materialize, lock creation); no concurrent/timeout test | **PARTIAL** (see R-595-003) |
| 608 | "merged into CLI tests" — handler-level integration tests with real store; audit event file verified; but no subprocess entrypoint | **PARTIAL** (see R-595-001) |
| 609 | Worker claims 4344 passed; targeted suites independently verified (110+98+397+187=792); plan says all done; live_review incomplete | PASS |

## Scope Blockers

| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS |
| shell=True | PASS — not in any new Python code |
| External CDN | PASS |
| Ollama API | PASS |
| WebSocket | PASS |
| POST/PUT/DELETE | PASS — 405 enforced |
| Outbound HTTP | PASS |
| Raw content leaks | PASS — _safe_text, title[:80], bounded summaries |
| UI redesign | PASS — backend only |
| Docker/MemPalace | PASS |

## Findings

### R-595-001
Status: Open
Severity: medium
Area: cli-runtime
Summary: CLI tests call COMMAND_HANDLERS directly, not through subprocess entrypoint
Details: All CLI tests (including new materialize + audit tests) invoke handlers from `collect_all_handlers()` dict. No test runs `python -m apps.cli.grouped propose ...` via subprocess. Steps 596 and 608 were "merged" but the subprocess coverage gap remains. Handler-level tests ARE integration-level (hitting real store operations, emitting real events), but argument parsing and grouped entrypoint wiring are untested at runtime.
Evidence: `grep -rn "subprocess\|python -m\|grouped" tests/cli/test_propose_cli.py` returns empty
Expected fix: Add 1-2 subprocess tests that invoke `python -m apps.cli.grouped propose list --job-id <id> --json` with temp REMEDY_DATA_DIR.

### R-595-002
Status: Open
Severity: medium
Area: queue-semantics
Summary: Queue gate ignores materialization state; can_finalize doesn't check approved-not-materialized
Details: `worker_queue._has_unresolved_proposals` only checks PROPOSED+EVALUATED (unresolved). APPROVED_FOR_BUILD is terminal — doesn't block queue or finalization. `can_finalize()` also doesn't check materialization. Dashboard shows `approved_not_materialized` count but no enforcement. Step 603 was "merged into 601/602" but worker_queue.py had zero changes. Design choice may be intentional (approved = decided, materialization is implementation detail), but the gap between dashboard visibility and gate enforcement is notable.
Evidence: `grep -n "materialized\|approved_not\|approved_for_build" packages/orchestration/worker_queue.py` returns empty
Expected fix: Either add `approved_not_materialized > 0` check to can_finalize/queue gate, or document that materialization is optional for finalization.

### R-595-003
Status: Open
Severity: low
Area: race-tests
Summary: No concurrent/timeout test for file locking
Details: TestFileLocking has 4 sequential tests (adds, update+add, approve+materialize, lock creation). No test exercises the lock timeout path (5s deadline), concurrent access from multiple threads/processes, or what happens when the lock is busy. The lock mechanism works for sequential access but error paths are untested.
Evidence: `grep -rn "LOCK_TIMEOUT\|concurrent\|threading\|multiprocessing" tests/orchestration/test_proposed_tasks.py` returns empty
Expected fix: Add 1 test that holds a lock and verifies ProposedTaskStoreError on timeout. Optional: thread-based concurrent add test.

### R-595-004
Status: Open
Severity: low
Area: storage-locking
Summary: do_materialize generates Task dict but only keeps UUID — standalone materialize_approved_task() is redundant
Details: `do_materialize()` calls `materialize_approved_task(task)` internally, gets back a full Task dict (id, description, inputs, status), but only stores `task_dict["id"]` on the ProposedTask. The full dict is discarded. `materialize_approved_task()` as a standalone function is now misleading — its only caller discards most of its return. Docstring says "Caller still needs to append the Task to Job and save it" but the caller never sees the dict.
Evidence: `do_materialize` at proposed_tasks.py:618 — `task_dict = materialize_approved_task(task); task.materialized_task_id = task_dict["id"]`
Expected fix: Either have `do_materialize` return `(ProposedTask, task_dict)` tuple, or simplify to `task.materialized_task_id = str(uuid4())` and remove `materialize_approved_task`.

### R-595-005
Status: Open
Severity: low
Area: storage-locking
Summary: approve/reject/defer double-load within lock
Details: `approve_proposed_task`, `reject_proposed_task`, `defer_proposed_task` each call `get_proposed_task` (loads all tasks + finds one) then `load_proposed_tasks` again for the save loop. Two reads per operation within the same lock. Functionally correct but wasteful.
Evidence: `approve_proposed_task` at proposed_tasks.py:505 — `task = get_proposed_task(...)` then `tasks = load_proposed_tasks(...)`
Expected fix: Load once, find task in list, transition, save list. Low priority — no functional impact.

## Architecture Assessment

**Strengths:**
- R-580-001 fully resolved: `_make_writer` creates real RunLogWriter, `test_no_dormant_none_writer_in_cli` prevents regression
- R-580-002 fully resolved: dashboard delegates to `can_finalize()`, timeline guard test enforces
- File locking with `fcntl.flock` + bounded retry is production-appropriate for single-host
- `_STORE_DIR = None` default eliminates import-time side effects
- Materialization state on ProposedTask gives `approved_for_build` concrete meaning
- Dashboard v2 exposes materialization status with bounded safe summaries
- 16 new tests (110 total for proposed tasks + CLI)

**Remaining Risks:**
1. No subprocess CLI runtime tests — handler dispatch verified but not entrypoint
2. Queue gate doesn't enforce materialization — visibility without enforcement
3. Lock timeout/busy path untested
4. `do_materialize` orphans the generated Task dict
5. Lock files (.{job_id}.lock) never cleaned up (accumulate, tiny)

## Final Verdict

**PASS WITH RISKS**

- Audit event status: **PASS** — R-580-001 resolved. Real RunLogWriter from UUID. Regression test enforced.
- Store locking status: **PASS** — fcntl.flock with bounded retry on all mutations. Sequential tests green.
- Data-root status: **PASS** — call-time resolution via proposed_tasks_dir(). REMEDY_DATA_DIR tested.
- Finalized gate status: **PASS** — R-580-002 resolved. Dashboard delegates to can_finalize().
- Materialization status: **PASS** — ProposedTask tracks materialized state. do_materialize under lock.
- Queue semantics status: **PARTIAL** — queue gate unchanged, doesn't check materialization (R-595-002)
- Dashboard contract status: **PASS** — v2 with materialization counts, bounded summaries, no raw leaks
- Reviewer/rework status: **PASS** — pre-existing, no changes needed
- Corrupt-store status: **PASS** — all surfaces handle ProposedTaskStoreError consistently
- Runtime CLI E2E status: **PARTIAL** — handler-level integration yes, subprocess entrypoint no (R-595-001)
- Raw leak status: **PASS** — _safe_text, title[:80], bounded summaries, scope blockers clean
- Tests run: 110 proposed+CLI + 98 reviewer + 397 UI contracts + 187 UI server (all guarded via scripts/remedy_pytest.sh)
- Full pytest: Worker reports 4344 passed (not independently verified — targeted suites confirm no regressions)
- Top 5 remaining backend risks:
  1. No subprocess CLI entrypoint tests (R-595-001)
  2. Queue gate ignores materialization state (R-595-002)
  3. Lock timeout/busy path untested (R-595-003)
  4. do_materialize orphans Task dict (R-595-004)
  5. Lock files never cleaned up
- Merge readiness: **YES** — all 2 prior findings resolved, new findings are medium/low severity

---

# Parallel Review — Steps 580-594 (Independent Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 580-594 (Proposed task backend closure — CLI handlers, storage stability, honest gates)
Commit: 4f8e6dd
Status: VERIFIED

## Test Results (independently run)
- `tests/orchestration/test_proposed_tasks.py` + `tests/cli/test_propose_cli.py`: **94/94 passed** (0.20s)
- `tests/orchestration/test_approval_queue.py` + reviewer-related: **98 passed, 1 skipped** (2.39s)
- `tests/ui_contracts/`: **397 passed** (2.44s)
- `tests/ui_server/`: **187 passed** (5.36s)
- No regressions detected across any targeted suite
- Worker claims 4328 full baseline (not independently verified — targeted suites confirm no regressions)

## Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 580 | context/plan current, UI paused, backend blockers listed, live_review used | PASS |
| 581 | propose_cmd.py with 6 handlers, collect_all_handlers includes it, all catalog commands run | PASS |
| 582 | 23 CLI contract tests: catalog coverage, list/show/evaluate/approve/reject/defer, corrupt, no-traceback | PASS |
| 583 | All functions accept root= param. _STORE_DIR kept for legacy but not relied on. Test isolation verified | PASS |
| 584 | _atomic_write: tempfile.mkstemp + os.fsync + os.replace. Cleanup on exception | PASS |
| 585 | ProposedTaskStoreError raised on corrupt. load_proposed_tasks_safe returns ([], True). CLI/queue/dashboard handle | PASS |
| 586 | Terminal states block further transitions. Timestamps set. Reasons bounded to 200 chars | PASS |
| 587 | CLI calls emit_proposed_task_event — but writer=None → all no-ops | **PARTIAL** (see R-580-001) |
| 588 | _has_unresolved_proposals takes data_dir. Corrupt → blocks. get_next_job passes data_dir | PASS |
| 589 | materialize_approved_task returns Task-compatible dict. list_approved_not_materialized filters | PASS |
| 590 | can_finalize() centralized, degraded blocks. Dashboard uses inline (functionally equivalent) | PASS (see R-580-002) |
| 591 | accept_recommendation creates ProposedTask, NOT direct Task. Tests updated across 3 files | PASS |
| 592 | Dashboard: degraded, blocking_finalized, blocking_build fields. Uses load_proposed_tasks_safe | PASS |
| 593 | E2E tests: full lifecycle, reject flow, defer flow, queue gate, corrupt gate | PASS |
| 594 | Worker claims 4328 passed. Targeted suites confirmed green. Single commit | PASS |

## Scope Blockers (delegated to agent)

| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS |
| shell=True | PASS |
| External CDN | PASS |
| Ollama API | PASS |
| WebSocket | PASS |
| POST/PUT/DELETE | PASS — 405 enforced |
| Outbound HTTP | PASS |
| Raw content leaks | PASS — _safe_text truncation everywhere |

## Findings

### R-580-001
Status: Open
Severity: medium
Area: audit-events
Summary: CLI audit events are functionally dormant — writer always None
Details: All 4 CLI handlers (evaluate, approve, reject, defer) call `emit_proposed_task_event(None, ...)`. Since the function does `if writer is None: return`, no events are recorded from CLI. The calls are structurally present but produce no audit trail. Worker checklist marks this as PASS.
Evidence: `grep -n "emit_proposed_task_event(None" apps/cli/commands/propose_cmd.py` → lines 153, 158, 217, 267, 317
Expected fix: Either create a RunLogWriter from job_id in CLI context, or document that CLI transitions are intentionally unaudited (acceptable if orchestrator loop audits them independently).

### R-580-002
Status: Open
Severity: low
Area: finalized-gate
Summary: Dashboard `is_finalized` duplicates can_finalize() logic inline
Details: ui_server.py:406 has inline `is_finalized = (job_says_done and pending_task_count == 0 and ...)`. The new `can_finalize()` in proposed_tasks.py covers the same checks (minus `job_says_done`, which is a different concern). Currently equivalent, but drift risk if one is updated without the other.
Evidence: `grep -n "can_finalize\|is_finalized" packages/orchestration/ui_server.py` — only inline, no import of can_finalize
Expected fix: Dashboard could call `can_finalize()` for the proposal/task portion and combine with `job_says_done`. Low priority — no functional gap today.

## Architecture Assessment

**Strengths:**
- Atomic write pattern (tempfile + fsync + rename) is production-grade
- Corrupt store → error instead of silent empty fixes a real safety gap
- `_safe` variants return degraded flag — callers can distinguish empty from broken
- Reviewer integration change removes direct task bypass (was a real risk)
- Materialization gives approved_for_build concrete meaning
- Test coverage is thorough (94 targeted tests covering all paths)

**Risks:**
1. CLI audit trail is dormant (R-580-001)
2. No file locking — concurrent CLI commands could race on store writes (atomic rename helps but doesn't prevent read-modify-write races)
3. can_finalize() exists but isn't actually called by ui_server.py

## Final Verdict

**PASS WITH RISKS**

- CLI handler status: **PASS** — all 6 handlers functional, tested
- CLI contract status: **PASS** — 23 tests, catalog coverage verified
- Data-dir storage status: **PASS** — root= param throughout, test isolation verified
- Atomic write/lock status: **PASS** — atomic write yes, file lock no (acceptable for single-user)
- Corrupt store status: **PASS** — ProposedTaskStoreError, degraded propagated to queue/finalize/dashboard
- Transition status: **PASS** — terminal blocks, timestamps, bounded notes
- Audit event status: **PARTIAL** — calls present but writer=None → no-ops from CLI
- Queue gate status: **PASS** — data_dir correct, corrupt blocks
- Approved task meaning status: **PASS** — materialize_approved_task() gives real meaning
- Finalized gate status: **PASS** — degraded blocks, centralized helper exists (dashboard uses inline equivalent)
- Reviewer/rework status: **PASS** — accept_recommendation creates ProposedTask, not direct Task
- Dashboard contract status: **PASS** — degraded/blocking fields present, safe output
- E2E status: **PASS** — full lifecycle, queue gate, finalize gate tested
- Raw leak status: **PASS** — _safe_text truncation, scope blocker audit clean
- Tests run: 94 proposed + 98 reviewer + 397 UI contracts + 187 UI server (all guarded via scripts/remedy_pytest.sh)
- Full pytest: Worker reports 4328 passed (not independently verified as full run — targeted suites confirm no regressions)
- Top 3 remaining backend risks:
  1. CLI audit trail is dormant (no writer in CLI context)
  2. No file locking on proposed task store (concurrent write races possible)
  3. Dashboard finalized logic duplicates can_finalize() — drift risk
- Merge readiness: **YES** — functional and safe, findings are medium/low severity

---

# Addendum Review — Timeline + Button Shape (post-565-579)

Reviewer: parallel watcher (independent)
Scope: Timeline visual correctness + button shape audit (current state, after Steps 545-564 + 565-579)
Status: COMPLETE

## Checklist

| # | Check | File | Verdict |
|---|-------|------|---------|
| 1 | PhaseGlyph always in header (not TaskDoneGlyph) | PhaseTimeline.tsx:90 | PASS |
| 2 | Event rail always visible (no conditional wrapper) | PhaseTimeline.tsx:111 | PASS |
| 3 | Legend always visible (no conditional wrapper) | PhaseTimeline.tsx:133 | PASS |
| 4 | Button shapes pill-like | various CSS | MIXED (see below) |
| 5 | PhaseGlyph icons correct (6 phases, strokeWidth=1.45) | RemedyGlyphs.tsx:166-180 | PASS |
| 6 | No fake events (fallbackEventsFromTasks removed) | PhaseTimeline.tsx, remedyApi.ts | PASS |
| 7 | No overflow:hidden on timeline | PhaseTimeline.module.css:17 | PASS — overflow:visible |

## Button Shape Detail

| Button | File:Line | border-radius | Pill? |
|--------|-----------|---------------|-------|
| GraphFilterChips | GraphFilterChips.module.css:2 | 999px | YES |
| TopMetricsBar badge | TopMetricsBar.module.css:71 | 999px | YES |
| LayerSwitcher | LayerSwitcher.module.css:2 | 50% (circular) | OK |
| CommandBar send | CommandBar.module.css:37 | 50% (circular) | OK |
| askBar button | RightLivePanel.module.css:74 | 8px | NO — could be pill |
| projectCommandButton | Pipeline.module.css:186 | 6px | NO — monospace command, OK |
| DetailPopover close | DetailPopover.module.css:2 | 9px | NO — small close X, OK |

## Findings

- R-ADD-001 (low): `askBar button` in RightLivePanel uses `border-radius: 8px` — should be pill (999px) for consistency with design language. Non-blocking, small 34px square button.

## Summary

Timeline visual correctness: **PASS** — PhaseGlyph in headers, event rail always visible, legend always visible, no fake events, overflow:visible. PhaseGlyph icons correct for all 6 phases.

Button shapes: **MOSTLY PASS** — primary interactive buttons (filter chips, metrics) use pill (999px). One minor inconsistency in askBar send button (8px instead of pill). Circular buttons (layer switcher, command send) are OK. Monospace command buttons (6px) are intentionally different.

---

# Parallel Review — Steps 565-579 (Reviewer)

Reviewer: parallel watcher (independent)
Scope: Steps 565-579 (Orchestrator task evaluation flow — proposed tasks, evaluator, build gate, CLI)
Status: VERIFIED

## Reviewer Verification

### Test Results
- `tests/orchestration/test_proposed_tasks.py`: **35/35 passed** (0.09s)
- 7 test classes: Model (8), Transitions (6), Store (6), ReviewBridge (3), Evaluator (6), ApproveRejectDefer (4), EventAudit (2)

### Per-Step Checklist

| Step | Check | Verdict |
|------|-------|---------|
| 565 | context.md, plan.md, live_review.md updated | PASS |
| 566 | ProposedTask Pydantic model, source/status enums, `_VALID_TRANSITIONS` map | PASS |
| 567 | JSON store: save/load/add/get/update/count/list_by_status, `_STORE_DIR` monkeypatchable | PASS |
| 568 | `propose_task_from_review_finding` sets source=REVIEWER, `propose_from_recommendation` bridges dict | PASS |
| 569 | Deterministic evaluator: duplicate→reject, high-risk→evaluate, low+no-approval→auto-approve | PASS |
| 570 | `evaluate_with_llm` stub falls back to deterministic when llm_fn=None | PASS |
| 571 | approve/reject/defer with `InvalidTransitionError` guard, terminal states block further transitions | PASS |
| 572 | `worker_queue._has_unresolved_proposals` + `get_next_job` skips unresolved | PASS |
| 573 | `propose_rework` sets source=ORCHESTRATOR, task_type="rework", priority="high" | PASS |
| 574 | Finalized gate: `unresolved_proposals == 0` added at ui_server.py:410 | PASS |
| 575 | CLI "propose" group with 6 commands in catalog (list/show/evaluate/approve/reject/defer) | PASS |
| 576 | `emit_proposed_task_event` via RunLogWriter, noop on None writer | PASS |
| 577 | `_build_proposed_tasks_section` returns counts by status, wired at response line 498 | PASS |
| 578 | Tests pass (verified 35/35 proposed_tasks) | PASS |
| 579 | Handoff report written | PASS |

### Scope Blockers
| Blocker | Verdict |
|---------|---------|
| 0.0.0.0 bind | PASS — not in changed files |
| shell=True | PASS — not in changed files (pre-existing in test_runner.py etc.) |
| External CDN | PASS — none found |
| Ollama API calls | PASS — none in changed files |
| WebSocket | PASS — none found |
| POST/PUT/DELETE | PASS — ui_server returns 405 on all |
| Outbound HTTP | PASS — no requests/urllib in changed files |

### Findings
- R-565-001: No findings. Implementation clean and well-structured.

### Architecture Notes
- ProposedTask uses Pydantic BaseModel (not dataclass) — consistent with domain model pattern
- Store uses `_STORE_DIR` module-level var — monkeypatchable in tests, good isolation
- Evaluator rules are deterministic, no LLM calls by default — safe for autonomy
- Import guard (`try/except ImportError`) on worker_queue and ui_server — graceful degradation

---

# Worker Review — Steps 565-579

## Summary

PASS — Orchestrator task evaluation flow implemented. ProposedTask domain model with Pydantic BaseModel. JSON file store per job. Deterministic evaluator with duplicate/risk/auto-approve rules. State transitions: proposed → evaluated → approved_for_build | rejected | deferred. Build queue skips jobs with unresolved proposals. Finalized gate blocks on unresolved proposals. CLI group "propose" with list/show/evaluate/approve/reject/defer. Event audit trail via RunLogWriter. Dashboard backend counts. 4259 pytest + 35 Vitest + tsc clean.

## Files Changed
- `packages/orchestration/proposed_tasks.py` — NEW: domain model, store, evaluator, transitions, bridges, events
- `packages/orchestration/data_paths.py` — added `proposed_tasks_dir()`
- `packages/orchestration/worker_queue.py` — build queue gate (`_has_unresolved_proposals`)
- `packages/orchestration/ui_server.py` — finalized gate + `_build_proposed_tasks_section`
- `apps/cli/command_catalog.py` — "propose" group + 6 commands
- `tests/orchestration/test_proposed_tasks.py` — NEW: 35 tests
- `tests/ui_server/test_dashboard_contract.py` — fixed brittle step-range assertion
- `tests/orchestration/test_test_runner.py` — fixed brittle step-range assertion
- `.agent/context.md`, `.agent/plan.md`, `.agent/live_review.md` — updated

## Step Log
- Step 565: Handoff — context.md, plan.md, live_review.md updated
- Step 566: ProposedTask Pydantic model with source/status enums, transitions map
- Step 567: JSON store per job with save/load/add/get/update/count/list_by_status
- Step 568: propose_task_from_review_finding + propose_from_recommendation bridge
- Step 569: Deterministic evaluator: duplicate→reject, high-risk→evaluate, low+no-approval→auto-approve, default→evaluate
- Step 570: evaluate_with_llm stub (falls back to deterministic when llm_fn=None)
- Step 571: approve/reject/defer functions with InvalidTransitionError guard
- Step 572: worker_queue.get_next_job skips jobs with unresolved proposals
- Step 573: propose_rework for orchestrator-created rework proposals
- Step 574: ui_server finalized gate now checks unresolved_proposals == 0
- Step 575: CLI "propose" group: list, show, evaluate, approve, reject, defer
- Step 576: emit_proposed_task_event for RunLogWriter audit trail
- Step 577: _build_proposed_tasks_section in dashboard response
- Step 578: 4259 passed, 0 failed, 35 Vitest, tsc clean
- Step 579: Handoff report (this file)

---

# Live Review — Steps 580-594

Reviewer: self (backend closure block)
Scope: Proposed task backend — CLI handlers, storage stability, gates, tests
Status: IN PROGRESS

## Step Log
- Step 580: Backend handoff — context.md, plan.md, live_review.md updated. UI paused. Known blockers documented.
- Step 581: Created `apps/cli/commands/propose_cmd.py` — 6 handlers (list/show/evaluate/approve/reject/defer). Wired into `__init__.py collect_all_handlers()`.
- Step 582: Created `tests/cli/test_propose_cli.py` — 23 tests. Catalog coverage, JSON output, error handling, corrupt store, no traceback.
- Step 583: Refactored proposed_tasks.py — all store functions accept `root: Path | None` param. `_STORE_DIR` kept for legacy compat but not relied on.
- Step 584: Atomic writes via `_atomic_write()` — tempfile + fsync + os.replace. Partial writes cannot corrupt store.
- Step 585: `ProposedTaskStoreError` exception. `load_proposed_tasks` raises on corrupt JSON. `load_proposed_tasks_safe` returns ([], True). Queue/finalized treat degraded as blocking.
- Step 586: Transition hardening — bounded reasons (200 chars), evaluated_at/resolved_at timestamps, terminal states raise InvalidTransitionError. Tests cover approve-rejected, defer-approved, reject-approved.
- Step 587: CLI handlers call `emit_proposed_task_event` on approve/reject/defer/evaluate transitions. Event payload bounded (title ≤80, notes ≤200).
- Step 588: `_has_unresolved_proposals(job_id, data_dir)` — passes data_dir to store. Corrupt store returns True (blocks). `get_next_job` passes its `data_dir`.
- Step 589: `materialize_approved_task()` — converts approved ProposedTask to Task-compatible dict. `list_approved_not_materialized()` finds un-materialized approvals.
- Step 590: `can_finalize()` centralized helper — checks pending/blocked tasks, approvals, unresolved proposals, degraded store. Used concept, ui_server uses inline check (same logic).
- Step 591: `accept_recommendation()` now creates ProposedTask instead of direct Task. Test updated. `review.accept` CLI shows "proposed task created — evaluate before build".
- Step 592: Dashboard `_build_proposed_tasks_section` includes: degraded, blocking_finalized, blocking_build fields. Uses `load_proposed_tasks_safe`.
- Step 593: End-to-end tests in test_proposed_tasks.py: TestEndToEndFlow (3 tests), TestWorkerQueueGate (3 tests), TestCanFinalize (9 tests), TestMaterialization (3 tests).
- Step 594: Full pytest: 4328 passed, 0 failed, 8 skipped. Safety checks: no shell=True, no 0.0.0.0, no test_steps_*.py.

## Checklist
| # | Check | Verdict |
|---|-------|---------|
| 1 | All 6 propose commands have handlers | PASS |
| 2 | CLI handlers execute without error | PASS (23 CLI tests) |
| 3 | Data-dir correct (root= param) | PASS |
| 4 | Atomic writes | PASS (tempfile + os.replace) |
| 5 | Corrupt store raises ProposedTaskStoreError | PASS |
| 6 | Corrupt store does NOT return empty list | PASS |
| 7 | Worker queue blocks on corrupt store | PASS |
| 8 | Finalized gate blocks on corrupt store | PASS |
| 9 | Transition hardening (terminal blocks) | PASS |
| 10 | Bounded reasons (200 chars) | PASS |
| 11 | Audit events emitted from CLI | PASS |
| 12 | accept_recommendation creates ProposedTask | PASS |
| 13 | accept_recommendation does NOT create Task | PASS |
| 14 | can_finalize() centralized helper | PASS |
| 15 | materialize_approved_task() | PASS |
| 16 | Dashboard proposed_tasks: degraded/blocking fields | PASS |
| 17 | No shell=True in production code | PASS |
| 18 | No 0.0.0.0 in changed source | PASS |
| 19 | No test_steps_*.py | PASS |

## Summary
PASS — Steps 580-594 complete. Proposed task backend is reliable.

---

# Live Review — Steps 595-609

Reviewer: self (backend reliability closure)
Scope: Audit trail, store locking, materialization truth, centralized gates
Status: IN PROGRESS

## Step Log
- Step 595: Backend handoff — context.md, plan.md, live_review.md updated. Carried forward 7 risks from reviewer findings.
- Step 597: Real audit events — `_make_writer(job_id)` creates RunLogWriter from UUID. All CLI transitions (evaluate/approve/reject/defer/materialize) use real writer. No `emit_proposed_task_event(None` remains.
- Step 598: File locking — `fcntl.flock` with 5s bounded retry. Protects add/update/evaluate/approve/reject/defer/materialize.
- Step 599: `_STORE_DIR` now defaults to `None`. `_resolve_store_dir()` calls `proposed_tasks_dir()` at call time, not import time. Test proves `REMEDY_DATA_DIR` env var works.
- Step 600: `ui_server.py` finalized gate now calls `can_finalize()` instead of inline logic. Single truth source.
- Step 601: `ProposedTask` gains `materialized_task_id: str` and `materialized_at: datetime | None`. `is_materialized` property. `do_materialize()` sets both atomically under lock.
- Step 602: `propose.materialize` command — catalog entry + CLI handler. Supports `--task-id` and `--all`. Emits `proposed_task_materialized` event.
- Step 604: Dashboard v2 — `approved_not_materialized`, `materialized`, `summaries` with per-task materialization status.

---

# Live Review — Steps 610-624

Reviewer: self (materialization + backend readiness)
Scope: True Job.tasks materialization, subprocess CLI, readiness gates
Status: IN PROGRESS

## Step Log
- Step 610: Backend handoff — context.md, plan.md, live_review.md updated. 7 real risks documented.
- Step 611: Job storage — root= param, _DATA_DIR=None default, atomic writes, JobStoreError, load_job_safe.
- Step 612: _require_job() gate on all mutating CLI handlers. Invalid/missing job → safe error, no mutation.
- Step 613: do_materialize() now loads real Job, creates Task, appends to job.tasks, saves Job, then marks ProposedTask.
- Step 614: reconcile_materialized() — detects missing Job tasks and missing proposal markers.
- Step 615: can_finalize() blocks on approved_not_materialized.
- Step 616: test_propose_cli_runtime.py — 11 subprocess tests via `python -m apps.cli.grouped`.
- Step 617: Audit events include materialized_task_id. Full flow test verifies events on disk.
- Step 619: Finalize gate v2 — approved_not_materialized blocks.
- Step 622: backend_readiness() — compact health report: job, proposal store, materialization consistency.
- Step 623: overnight_readiness() — always not ready, specific blockers listed.

---

# Live Review — Steps 625-639

Reviewer: self (modular task execution + worker runs real tasks)
Scope: Task execution port, fixture executor, worker runs Job.tasks, budget, readiness v2
Status: IN PROGRESS

## Step Log
- Step 625: Clean handoff — readiness terms defined, agent files updated, 6 risks carried.
- Step 626: Runtime CLI tests stabilized — unique UUID per test via fixture, no shared module-level state, 11 pass reliably.
- Step 627: backend_readiness v2 — structured: storage_health, proposal_health, build_readiness, finalize_readiness, overnight.
- Step 628: TaskExecutionRequest/Result models, TaskExecutor protocol, execute_task() dispatch.
- Step 629: FixtureTaskExecutor — deterministic completion, blocked_fixture type, artifact IDs, safe summaries.
- Step 631: Provider adapter — get_executor(), NoneExecutor, ALLOWED_PROVIDERS, ollama returns None (unavailable).
- Step 635: can_retry_task() — read-only, checks completed/pending/failed states, materialization consistency.
- Step 636: BudgetGate — max_steps, record_step, has_budget, can_execute with exhaustion check.
- Step 637: overnight_readiness v2 — adds pending_tasks + blocked_tasks as blockers from finalize section.
- Step 638: Modular guard tests — no ollama import in core, no source_apply in executor, storage through helpers.
- Fix R-610-003: origin_task_id + origin_recommendation_id in materialize_approved_task inputs.
- Fix R-610-004: load_job moved inside _file_lock in do_materialize (prevents concurrent job task loss).

---

# Live Review — Steps 640-654

Reviewer: self (backend basis completion)
Scope: Worker executes real Job.tasks, events, readiness, budget, E2E
Status: IN PROGRESS

## Step Log
- Step 640: Handoff — "basis complete" defined, 6 risks carried.
- Step 641: Runtime CLI test file: pytest.mark.timeout(30) on E2E, unique UUIDs already from 626.
- Step 642: can_retry_task uses `task` not `t`. BudgetGate enforces max_tokens + max_runtime_seconds.
- Step 643: list_jobs_safe() returns (jobs, degraded, skipped_files).
- Step 644: _run_via_task_execution() — loads Job, finds pending task, calls execute_task(), saves Job.
- Step 645: One task per --once. Remaining > 0 → release lease + re-queue. Remaining == 0 → completed.
- Step 646: Task.status=COMPLETED, execution_summary, execution_artifact_ids, execution_provider persisted.
- Step 647: RunLogWriter emits task_execution_completed with proposed_task_id, provider, artifact_count.
- Step 648: _has_unresolved_proposals blocks approved_not_materialized + unresolved + corrupt.
- Step 649: can_finalize blocks pending_task_count (tests prove before/after worker run).
- Step 652: TestFullBackendLoop.test_propose_to_completion — full loop proven end-to-end.
- Step 653: Legacy autorun isolated in _run_via_legacy_autorun. Fixture path uses task_execution only.

---

# Live Review — Steps 655-669

Reviewer: self (backend basis final closure)
Scope: Runtime stability, budget, start/end events, worker CLI E2E, Baukasten guards
Status: IN PROGRESS

## Step Log
- Step 655: Handoff — component status table, 6 risks carried, plan updated.
- Step 656: Runtime CLI hardened — bounded event file read ([:5]), assertion messages with r.stderr.
- Step 657: Worker CLI runtime tests — 5 subprocess tests: fixture run, second run, none provider, events, full loop.
- Step 658: WorkerResult v2 — last_task_id, provider, work_performed, task_status, artifact_ids, blocked_reason, budget_status.
- Step 659: BudgetGate consumed by _run_via_task_execution — max_steps/tokens/runtime checked before execute_task().
- Step 660: task_execution_started event emitted before executor call. task_execution_completed/blocked after.
- Step 661: Narrow exceptions — JobNotFoundError → job_not_found, JobStoreError → job_store_degraded. No broad Exception.
- Step 662: Blocked fixture → FAILED + blocked_reason persisted + task_execution_blocked event.
- Step 666: Full backend loop via subprocess: propose→evaluate→approve→materialize→enqueue→worker→completed→events.
- Step 667: Baukasten v2 — 10 guard tests (no provider imports, no source_apply, autorun isolated).
- Step 668: Component status table in context.md.
- Also: Fixed grouped CLI --once/--max-jobs/--max-seconds parsing. Fixed worker handler args.job mapping.

---

# Live Review — Steps 670-684

Reviewer: self (backend basis hardening final)
Scope: Runtime no-hang, budget CLI, execution_health, lock tests, clean handoff
Status: IN PROGRESS

## Step Log
- Step 670: Handoff — 6 risks carried, plan updated.
- Step 671: Shared subprocess helper (runtime_helpers.py) — run_grouped_cli, run_json, read_events, create_test_env.
- Step 672: Propose runtime uses helper — cleaner assertions, bounded reads.
- Step 673: Worker runtime uses helper + budget max_steps=0 test.
- Step 675: Worker CLI budget args — --max-steps, --max-tokens, --max-runtime-seconds wired through catalog/grouped/handler.
- Step 676: execution_health section in backend_readiness — pending/completed/blocked/total.
- Step 677: list_jobs_safe consumed by backend_readiness — skipped_files count, storage degraded.
- Step 678: Lock timeout test — test_lock_timeout_on_busy, test_lock_released_on_exception.
- Step 679: Double-load cleanup — approve/reject/defer rewritten to single load-modify-write.
- Step 680: Worker lease released on budget block.
- Step 682: Backend basis smoke script (scripts/remedy_backend_basis_smoke.sh).
- Step 683: Completion table with freeze rules in context.md.
- Fixes: lock fd double-close in _file_lock timeout path, defer_proposed_task bug (used task.id before assignment).
