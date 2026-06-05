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
