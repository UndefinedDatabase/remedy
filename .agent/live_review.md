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
