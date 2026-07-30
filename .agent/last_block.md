OUTCOME: executed
── STEP R2/R0154 + R1/F050 — verdict · merge · claim · T001 · T002 ──
Goal:        Persist the R0154 R1 PASS verdict, merge PR #162 via the
             Open PR Gate, then build ALL of F050 — DAG scheduling
             (T001 pure module + T002 executor integration).
Bundle:      Slice 0 verdict + gate · Slice 1 claim + state ·
             Slice 2 T001 · Slice 3 T002. STOP at the FIRST red
             verification (AGENTS.md If-Blocked); hand back raw
             output with completed slices intact.
Change:      .agent/ state; docs/roadmap/STATUS.md (ONE line);
             packages/orchestration/dag_schedule.py (new);
             packages/orchestration/long_run_executor.py (batch
             selection + blocked tracking only);
             tests/orchestration/test_dag_schedule.py (new);
             executor tests as needed. Nothing else.
Constraints: AGENTS.md; feature file docs/roadmap/features/T1_F050.md
             is the spec — read it COMPLETELY first. Do-not-touch:
             plan-time validation, parallel workers, decision UX.
             NO THREADING — any diff adding threading is a defect.
             Commits < 500 lines each; split slices into several
             commits where needed. Authored texts verbatim:
             sha256-verify BEFORE apply; mismatch = STOP + refusal
             record. Worker never writes ## Verdicts for F050.
             NO closure work: no [x], no evidence job, no zip —
             closure is its own later round.
Done when:   Every slice gate green (commands below), pushed, PR
             open for feature/f050-dag-scheduling.
Handback:    Completion report + rewrite .agent/handoff.md:
             changed-files table PER COMMIT, raw gate transcripts
             (command, exit code, tail), sha256 + cmp proofs, STATUS
             grep proofs, PR number.

GROUND FACTS (reviewer-verified; do not re-derive, DO spot-check)
- Dependency edges: task.inputs["flight"]["depends_on"] (list of
  planned ids); own planned id in task.inputs["flight"]["planned_id"].
  Producer: map_flight_plan_to_tasks, flight_plan.py:417. Plan-time
  DAG validation exists — cycles cannot reach the executor.
- Legacy tasks (no inputs["flight"]) → implicit linear chain: each
  task depends on its predecessor. One rule, docstring, tested.
- Sole selection point: ready_tasks(job, batch_size),
  long_run_executor.py:572 — replace its linear logic; keep the
  signature the executor loop uses (or adapt the loop minimally).
- RunState: PENDING/PLANNED/RUNNING/PAUSED/COMPLETED/FAILED/
  CANCELLED. Task failure ROLLS BACK to PENDING (task_runner.py
  states table) — there is NO persistent task-level FAILED in the
  loop. Blocked tracking is therefore IN-RUN: a task whose attempt
  executed-but-failed in this run is blocked; its transitive
  downstream is skipped-blocked. Treat FAILED/CANCELLED task states
  as blocking too if encountered.
- Empty ready set + unfinished tasks → the existing TERMINAL_BLOCKED
  path (long_run_executor.py ~800) — reuse, do not invent a status.
- Cycle evidence: CycleRecord — extend to name skipped-blocked task
  ids so reports say WHY nothing happened on a branch.

PROCEDURE

Slice 0 — verdict + Open PR Gate
1. On feature/r0154-closure-ordering. .agent/last_block.md guard:
   line 1 "OUTCOME: pending", THIS block verbatim; flip to
   "OUTCOME: executed" at round end.
2. Save authored text r0154-r2-1 below VERBATIM to
   .agent/authored/r0154-r2-1.md; sha256sum must equal its BEGIN
   marker. FULL REPLACE .agent/live_review.md with it; cmp → 0.
   Commit: "chore(r0154): persist the R1 PASS verdict". Push.
3. Open PR Gate (AGENTS.md):
   gh pr list --state open --json number,headRefName,baseRefName,isDraft
   Expected exactly one: #162, head feature/r0154-closure-ordering,
   base main, not draft. Then:
   gh pr merge 162 --merge --delete-branch
   git checkout main && git pull --ff-only
   Any other gate state → STOP, hand back raw output.

Slice 1 — F050 claim + state reset
4. git checkout -b feature/f050-dag-scheduling
5. Save f050-r1-1 and f050-r1-2 below VERBATIM to .agent/authored/;
   sha256-verify. Apply by copy: f050-r1-1 FULL REPLACE
   .agent/live_review.md; f050-r1-2 FULL REPLACE .agent/plan.md;
   cmp both → 0.
6. docs/roadmap/STATUS.md: replace the exact line
   "- [ ] F050 — DAG scheduling"
   with
   "- [~] F050 — DAG scheduling"
   Touch no other line. Proof: grep -cF new = 1, old = 0.
7. Gate: python3 -m pytest tests/docs/ -q (docs/roadmap changed;
   F252 baseline 292 passed) AND canary
   python3 -m pytest tests/cli/test_golden_path.py -q (baseline 42).
   Both exit 0 ELSE STOP. Commit:
   "chore(f050): claim F050 — state reset". Push.

Slice 2 — T001 pure module + table tests
8. New packages/orchestration/dag_schedule.py, PURE (no I/O, no
   timestamps, no randomness, no threading):
   - ready_set(tasks) -> ordered list of task ids: PENDING tasks
     whose dependencies are ALL COMPLETED, in plan order (stable,
     deterministic).
   - blocked_downstream(tasks, blocked_ids) -> set: transitive
     dependents of the blocked tasks.
   - Dependency resolution per GROUND FACTS: flight metadata ids
     mapped to task order; legacy/missing metadata → predecessor
     chain; state the rule in the module docstring.
   - Unknown/dangling dep ids: treat the dep as never-completed and
     say so in the docstring (plan-time validation makes this a
     legacy-only corner).
9. New tests/orchestration/test_dag_schedule.py — table tests:
   diamond, chain, independent islands, legacy-linear rule, mixed
   (flight + legacy tasks in one plan), single-task plan,
   skipped-blocked transitivity, deterministic ordering (two calls,
   identical result).
10. Slice gate: python3 -m pytest tests/orchestration/test_dag_schedule.py -q
    exit 0 ELSE STOP here and hand back. Commit:
    "feat(f050): dag_schedule pure module + table tests (T001)".
    Push.

Slice 3 — T002 executor integration
11. long_run_executor.py: at each batch boundary compute
    ready_set minus blocked downstreams (recompute after EVERY task
    end); a task whose attempt executed-but-failed this run joins
    blocked_ids and its downstream is marked skipped-blocked in the
    cycle evidence (CycleRecord extension); empty ready set with
    unfinished tasks → existing TERMINAL_BLOCKED. Batch-size cap
    semantics unchanged. Legacy plans behave exactly as before.
12. Tests (extend tests/orchestration/test_long_run_executor.py or
    the T001 file where it fits):
    - Diamond fixture: forced failure on one branch → independent
      branch COMPLETES, failed branch's downstream skipped-blocked,
      final blocked status lists exactly the right tasks, evidence
      names them.
    - Recomputation after every task end via a counting stub.
    - Determinism: two runs of the same fixture → identical
      schedules.
    - Linear regression: existing linear fixtures produce unchanged
      behavior (existing executor tests stay green untouched).
13. Slice gate:
    python3 -m pytest tests/orchestration/test_dag_schedule.py tests/orchestration/test_long_run_executor.py tests/orchestration/test_queue_executor_binding.py tests/orchestration/test_overnight_executor.py -q
    exit 0 ELSE STOP. Then canary:
    python3 -m pytest tests/cli/test_golden_path.py -q  exit 0.
    Commit(s): "feat(f050): DAG ready-set executor integration +
    diamond fixture (T002)". Push.
14. PR per AGENTS.md: title "F050 — DAG scheduling (T001+T002)";
    body: what/why, ground facts used, changed-files table, gate
    results per slice, verdict: pending R1 review. Do NOT merge.
15. Handback per the Handback line above.

TRANSPORT NOTE (worker, R2/R1): the step-13 slice-gate command arrived
hard-wrapped, split after `test_queue_executor_binding.py`. Recorded
above rejoined into the single four-path pytest invocation that was
actually run — same recoverable wrap class as r0154-r1-1 last round.
No sha256-stamped text was affected.

--- BEGIN r0154-r2-1 sha256=800c9f15bf69fd222cfc6e13b1b51423580e000dcabf15e5516862104f7ebffb ---
# Live Review — R0154 micro-round (closure-ordering codification)

> Docs-only micro-round ordered by the operator before F050: persist
> the R-0154 ordering lesson from the F252 closure into
> docs/roadmap/STATUS_closure_protocol.md. Reviewer: Window 1.

## Steps
- R1: replace docs/roadmap/STATUS_closure_protocol.md with the
  authored v4 text (step 5 now pins the R-0154 ordering: README
  capability sync in the SAME commit as the STATUS `[x]` edit; the
  closure commit touches exactly STATUS.md, README.md and the final
  .agent/ state). Gate: tests/docs + canary. Done.

## Findings
(none — IDs continue monotonically from R-0154; next free: R-0155)

## Verdicts
- R1: PASS (reviewer, 2026-07-29). Range 757e06f..ffad73a, 2
  commits. All three authored texts disk-to-disk cmp 0 against the
  reviewer's originals; applied targets cmp 0; protocol diff =
  exactly the two authored hunks; docs gate 292 passed + canary 42
  passed, re-run by the reviewer; tree clean; the transport-wrap
  recovery on r0154-r1-1 is proven by hash identity (d2b67cb5…).
  Deviation accepted: round-end state in a second mechanical commit
  (ffad73a — handoff + OUTCOME flip only, verified via --stat).
  LAST_REVIEWED_SHA = ffad73a.
--- END r0154-r2-1 ---

--- BEGIN f050-r1-1 sha256=373c67edd96338b630eaedc7ab3c60a573712e9b24facc8c2809a20a4c5d1569 ---
# Live Review — F050 DAG scheduling (Tier 1)

Branch: feature/f050-dag-scheduling
Scope: topological ready set + blocked-downstream skip in the
multi-cycle executor (docs/roadmap/features/T1_F050.md).

## Steps
- R1: claim + state reset + T001 pure module + T002 executor
  integration (large bundle, per-slice gates, stop at the first red
  verification). In progress.

## Findings
(none yet — next free ID: R-0155)

## Verdicts
(pending R1)
--- END f050-r1-1 ---

--- BEGIN f050-r1-2 sha256=d019d7b347cb92468562c12acb5342cc585d627293aa8d1f5addd741bef744c7 ---
# Plan — F050 DAG scheduling

## Goal
The executor draws its next tasks from a topological READY SET
computed from the Flight Plan dependency edges
(task.inputs["flight"]["depends_on"]); a blocked branch (failed or
awaiting a decision) locks only its own downstream. DONE when the
diamond fixture executes the independent branch while the blocked
branch's downstream is skipped-blocked, the ready set recomputes
after every task end, and linear plans behave exactly as before
(docs/roadmap/features/T1_F050.md).

## Next Steps
- T001: pure module packages/orchestration/dag_schedule.py
  (ready_set, blocked_downstream, legacy-linear rule) + table tests
  in tests/orchestration/test_dag_schedule.py.
- T002: executor integration at the ready_tasks batch boundary in
  packages/orchestration/long_run_executor.py + diamond fixture +
  linear-regression proof.
- Then: integration gate round, closure per
  docs/roadmap/STATUS_closure_protocol.md (v4) — own rounds, never
  bundled.
--- END f050-r1-2 ---
