# Handoff — F028, round 2

## Session

SESSION 1 of feature F028 · round 2 · rounds so far 2. Context remaining at
handback: comfortable — this round wrote roughly 1000 lines across
production and tests from a specification with no repair loop needed (every
gate matched on the first try, all 13 red-proof mutations caught on the
first run), leaving ample context had a further round been required this
session.

## Range

Review of `4b6ccd1d9`..`HEAD` (`HEAD` is this handback's own commit, `F028
R2 C7`, on `feature/f028-task-injection`).

## Commits

### 6f3e6e655 F028 R2 C1: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r2-block.md | 299/0 | copy of this round's block |
| .agent/authored/f028-r2-plan.md | 31/0 | copy of the plan payload |
| .agent/authored/f028-r2-records.diff | 89/0 | copy of the records diff payload |

Measured insertions: 419 (block's own line count 299 + 120), matching the
block's expectation exactly, under the 500-line cap.

### d5caa2372 F028 R2 C2: book round 1, register R-1076, record D2 and a prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 60/0 | DECISION F028 D2 appended |
| .agent/live_review.md | 4/0 | round 1's Gate entry and R-1076's registration appended |
| .agent/plan.md | 8/8 | rewrite from the plan payload |
| .agent/prose_slips.md | 1/0 | round 1's declared prose slip appended |

Matches the block's expected numstat (60/0, 4/0, 8/8, 1/0) exactly. Applied
via `git apply --check` (exit 0) then the real apply (exit 0) of
`records.diff`, followed by the `plan.md` rewrite via `shutil.copyfile`.

### 3e9b7afa5 F028 R2 C3: repair R-1076, confirm an injection, apply it to a job, and add the plan_add_task edit
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/plan_editing.py | 20/2 | S2: `_add_task`, `_EDITS` gains `plan_add_task` last, `PLAN_EDIT_COMMANDS` becomes the explicit six-command tuple |
| packages/orchestration/task_injection.py | 320/7 | S1: `read_injection_draft`'s expiry repair (R-1076); S3: `confirmed_injections`, `_publish_confirmed_injection`, `confirm_task_injection`; S4: `apply_injection_to_job` |

340 insertions total, under the 500-line cap — no split needed.

### 4249e9447 F028 R2 C4: fold confirmed injections into run_job at four points
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | 82/0 | S5: `_fold_task_injections` and its four call sites (a)-(d) in `run_job` |
| tests/orchestration/import_reachability_allowlist.txt | 1/0 | S6: `packages.orchestration.task_injection` added between `task_edit_runtime` and `task_veto` |
| tests/test_no_orphan_modules.py | 0/2 | S6: the module's `ALLOWED_UNWIRED` entry removed — it is wired now |

83 insertions total, under the 500-line cap.

### a49858dda F028 R2 C5a: test the confirmation, the apply and the edit kind (part 1 of 2)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_plan_editing.py | 38/0 | `TestAddTaskEditKind`: appends, a duplicate id refused, a missing task refused |
| tests/orchestration/test_task_injection.py | 396/0 | R-1076's four cases; `confirmed_injections` ordering and corruption; `confirm_task_injection`'s whole refusal ladder, the two `draft_stale` branches, `plan_full`, `already_confirmed`; `apply_injection_to_job`'s provenance, version bump, hash re-seal, DoD flag, edit log, `replay_edits`, and the missing-dependency refusal |

### 74e5538ab F028 R2 C5b: test the runner's fold of a confirmed injection (part 2 of 2)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_task_injection_runner.py | 330/0 (new file) | 6 tests: confirmed before the run, confirmed while the last task runs, confirmed exactly at point (d) (parks PAUSED, a second run completes it), folded once never twice across two runs, a corrupt confirmed-injection file blocks the job, an inert fold |

C5a + C5b together are the block's single C5 ("the tests"), split by
DECISION of this round under constraint 2: combined the three test files
are 396 + 38 + 330 = 764 insertion lines, over the 500-line cap — a split
constraint 2 itself names by example ("C5a and C5b"). Split by artifact: the
two files touching existing production modules in C5a, the new runner test
file in C5b. Each half independently green (114 passed / 6 passed).

### de08d9d48 F028 R2 C6: add the round 2 mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f028-r2-mutations.py | 227/0 | the G5 mutation (red-proof) tool, 13 mutations across the three touched production files |

### F028 R2 C7: rewrite handoff for round 2 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- No branch creation this round — the block continues on
  `feature/f028-task-injection`, already checked out from round 1.
- `git worktree add --detach .remedy-wt/f028-r2-smoke HEAD` (at C5b,
  `74e5538ab`) — an UNORDERED smoke test of the mutation tool before writing
  it into a scratch location distinct from the block's own worktree name,
  to catch a tool bug before the graded run; `git worktree remove --force
  .remedy-wt/f028-r2-smoke` immediately after — both succeeded. `git
  worktree list | wc -l` read 62 before the add and 62 after the remove.
  Declared under Deviations below.
- `git worktree add --detach .remedy-wt/f028-r2-mut de08d9d48` (at C6, G5's
  own ordered worktree) — succeeded; `git worktree remove --force
  .remedy-wt/f028-r2-mut` and `git worktree prune` afterwards — both
  succeeded. `git worktree list | wc -l` read 62 before the add and 62
  after the remove (step 4's own reading, unchanged).
- `git push` after C7 — reported under G6 in this round's reply (run after
  this file is committed).
- No `gh pr create` (the block does not order one this round), no `gh pr
  merge`, no checkout of `main`, no branch deletion, no force-push, no `git
  stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `records.diff`: 89 lines, 15410 bytes, sha256
  `eee1df8a3cef7ebbfda08fe8a7f0ba1c2825e2b3af76fbde7ff78309827a198a`.
- `plan.md`: 31 lines, 1161 bytes, sha256
  `b5dd27102ef67aa1efc7a465d85701cebba375a7f68a62b2d1c04dd465584386`.
- Block: 299 lines, sha256
  `58355c894fd6b8f4bbfd219b06f62d6aa986a7b839cd5a090e274c96fcbf03d3` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f028-r2-*` payload copy, read back with `git show
<commit>:<path>` from C1 (`6f3e6e655`), compared byte-for-byte (sha256)
against its source — all three MATCH:
```
.agent/authored/f028-r2-block.md byte-identical to source: True sha256: 58355c894fd6b8f4bbfd219b06f62d6aa986a7b839cd5a090e274c96fcbf03d3
.agent/authored/f028-r2-records.diff byte-identical to source: True sha256: eee1df8a3cef7ebbfda08fe8a7f0ba1c2825e2b3af76fbde7ff78309827a198a
.agent/authored/f028-r2-plan.md byte-identical to source: True sha256: b5dd27102ef67aa1efc7a465d85701cebba375a7f68a62b2d1c04dd465584386
```

### G2 — THE RECORDS
`git show <sha>:<path>`, bytes and sha256, each read from C2 (`d5caa2372`),
MATCHING the reviewer's table exactly:
```
.agent/live_review.md   bytes=313089  sha256=8cf8fc2a97363c1988bef8eabdf051347b5796605f48f7a9589d3a90b64768f6
.agent/decisions.md     bytes=2255784 sha256=e2c21f08ff91868b56048a033185ee244e37932b3926b800221b11cb85e580ff
.agent/prose_slips.md   bytes=372463  sha256=eaf83ba1b2cff40b2363f654d4f15e1867c44b209830a730ae401a64e0c17eb1
.agent/plan.md          bytes=1161   sha256=b5dd27102ef67aa1efc7a465d85701cebba375a7f68a62b2d1c04dd465584386
```
All four MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s text: at `4b6ccd1d9`
reads `[]`; at C2 (`d5caa2372`) reads `['R-1076']` — MATCH against the
reviewer's stated readings. `git diff --name-only 6f3e6e655 d5caa2372`
names exactly: `.agent/decisions.md`, `.agent/live_review.md`,
`.agent/plan.md`, `.agent/prose_slips.md` — the table's four paths, no
more, no fewer.

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check packages/orchestration/task_injection.py packages/orchestration/plan_editing.py packages/orchestration/pingpong_job.py tests/orchestration/test_task_injection.py tests/orchestration/test_plan_editing.py tests/orchestration/test_task_injection_runner.py tests/test_no_orphan_modules.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```

The whole of `_fold_task_injections`, quoted from the diff (C6 state,
`packages/orchestration/pingpong_job.py`):
```python
def _fold_task_injections(job: JobPlan, control_root_path: Path | None) -> bool:
    """Fold every confirmed injection ``job``'s own record does not yet hold (DECISION F028
    D2 (3)). Called by ``run_job`` at four points: directly after the veto fold before the
    task loop, directly after the veto fold at every pre-task safe point, as the last
    statement of the loop body, and once more after the loop, before the terminal readings.

    Returns True when the job was just blocked by an unreadable control area — a
    ``task_injection.TaskInjectionError`` reading the confirmed injections — and ``run_job``
    must return ``job`` right here, exactly as ``_fold_task_vetoes`` does for its own control
    area. A confirmed injection the record does not yet hold (its ``draft_id`` is not a key
    of ``job.metadata["task_injections"]``) is applied through
    ``task_injection.apply_injection_to_job``; an edit it refuses is recorded INERT with its
    detail rather than raised, so one bad confirmation blocks nothing else. Persists the
    record itself in every case that changes it or blocks the job.
    """
    from packages.orchestration import task_injection as _ti

    try:
        records = _ti.confirmed_injections(job.job_id, control_root_path=control_root_path)
    except _ti.TaskInjectionError as exc:
        job.state = JOB_BLOCKED
        job.error = f"task_injection_control_error: {exc}"
        _persist_job(job)
        return True

    task_injections = job.metadata.setdefault("task_injections", {})
    changed = False

    for record in records:
        draft_id = record["draft_id"]
        if draft_id in task_injections:
            continue                                          # already folded

        try:
            applied = _ti.apply_injection_to_job(job, record)
        except _ti.TaskInjectionRefused as exc:
            task_injections[draft_id] = {
                "inert": exc.detail,
                "folded_at": datetime.now(timezone.utc).isoformat(),
            }
            changed = True
            continue

        task_injections[draft_id] = applied
        changed = True

    if changed:
        _persist_job(job)
    return False
```

Its four call sites, three lines of context each:
```python
        # (a) — before the task loop
        if _fold_task_vetoes(job, job_handle, _control):
            return job

        # F028 D2 (3): the injection fold runs at the same point, right after the veto
        # fold — a confirmed injection waiting before this episode started joins task 1.
        if _fold_task_injections(job, _control):
            return job

        tasks_run = 0
```
```python
            # (b) — every pre-task safe point
            if _fold_task_vetoes(job, job_handle, _control):
                return job

            # F028 D2 (3): the injection fold runs again here too, right after the veto
            # fold — a confirmation recorded between two tasks joins the very next one.
            if _fold_task_injections(job, _control):
                return job

            if task.status == TASK_VETOED:
```
```python
                    job.error = f"budget_exhausted: {getattr(_stop, 'reason', 'budget')}"
                    _persist_job(job)
                    return job

            # (c) — the last statement of the loop body
            # F028 D2 (3): the injection fold's third point — the last statement of the
            # loop body — so a task confirmed while an earlier one ran is folded before the
            # NEXT iteration checks it (never later than one task late).
            if _fold_task_injections(job, _control):
                return job
```
```python
        # (d) — once after the loop, before the terminal
        # F028 D2 (3): the injection fold's fourth and last point, once the loop has ended.
        # A confirmation that arrives only now — after the last task already ran — appends a
        # task nothing in this run will dispatch, so the job parks PAUSED instead of racing
        # ahead to completion with new work pending.
        _tasks_before_injection_terminal_fold = len(job.tasks)
        if _fold_task_injections(job, _control):
            return job
        if len(job.tasks) > _tasks_before_injection_terminal_fold:
            job.state = JOB_PAUSED
```

`_add_task`, quoted whole (`packages/orchestration/plan_editing.py`):
```python
def _add_task(tasks: list[PlannedTask], args: dict[str, Any]) -> list[PlannedTask]:
    # A missing "task" key reads as `None`, which `model_validate` itself refuses with a
    # `ValidationError` (its "input should be a valid dictionary" reading) — the same path
    # a task shaped wrong takes, so both land on `_refuse_args` with the model's own reason.
    try:
        task = PlannedTask.model_validate(args.get("task"))
    except ValidationError as exc:
        raise _refuse_args(_reasons(exc)) from exc
    if any(t.id == task.id for t in tasks):
        raise _refuse_args(f"task id {task.id!r} is already used")
    return [*tasks, task]
```

The refusal ladder of `confirm_task_injection`, quoted whole
(`packages/orchestration/task_injection.py`):
```python
    refusal = injection_refusal(getattr(job, "state", ""), 0)
    if refusal is not None:
        return {"outcome": "refused", "code": refusal.code, "detail": refusal.detail}

    try:
        record = read_injection_draft(
            job.job_id, confirm_token, now=now, control_root_path=control_root_path)
    except TaskInjectionRefused as exc:
        return {"outcome": "refused", "code": exc.code, "detail": exc.detail}

    if record.get("job_id") != job.job_id:
        return {"outcome": "refused", "code": "draft_unknown",
                "detail": f"no injection draft {confirm_token!r} exists"}

    if record.get("status") != "confirmable":
        return {"outcome": "refused", "code": "draft_needs_decision",
                "detail": "this injection draft needs its shortfall decision answered first"}

    draft_id = record["draft_id"]
    task_injections = job.metadata.get("task_injections") or {}
    existing = confirmed_injections(job.job_id, control_root_path=control_root_path)
    if any(r["draft_id"] == draft_id for r in existing):
        return {"outcome": "refused", "code": "already_confirmed",
                "detail": f"injection draft {confirm_token!r} was already confirmed"}

    raw_plan = getattr(job, "task_plan", None)
    plan: TaskPlan | None = None
    if isinstance(raw_plan, dict):
        try:
            plan = TaskPlan.model_validate(
                {k: v for k, v in raw_plan.items() if not k.startswith("_")})
        except ValidationError:
            plan = None
    if plan is None:
        return {"outcome": "refused", "code": "no_task_plan",
                "detail": "this job has no readable task plan to confirm an injection into"}

    plan_ids = {t.id for t in plan.tasks}
    unfolded_ids = {
        r["task"]["id"] for r in existing if r["draft_id"] not in task_injections
    }
    known_ids = plan_ids | unfolded_ids

    task = record["task"]
    if task["id"] in known_ids:
        return {"outcome": "refused", "code": "draft_stale",
                "detail": f"task id {task['id']!r} is already used; draft again"}
    for dep in task.get("depends_on") or []:
        if dep not in known_ids:
            return {"outcome": "refused", "code": "draft_stale",
                    "detail": f"task {task['id']!r} depends on {dep!r}, which is no longer "
                              "in the plan; draft again"}

    if len(known_ids) >= MAX_PLAN_TASKS:
        return {"outcome": "refused", "code": "plan_full",
                "detail": f"the plan is already at its {MAX_PLAN_TASKS}-task cap"}
```

### G4 — THE TESTS
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_task_injection.py tests/orchestration/test_task_injection_runner.py tests/orchestration/test_plan_editing.py tests/orchestration/test_plan_edit_execution.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_task_veto.py tests/orchestration/test_task_veto_runner.py tests/orchestration/test_job_task_runner.py tests/orchestration/test_pause_resume.py tests/orchestration/test_pause_manifest.py tests/orchestration/test_job_stop_integration.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_worktree_resume_cli.py tests/orchestration/test_job_plan.py tests/orchestration/test_mint_call_sites.py tests/orchestration/test_human_change_one_path.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_unified_store_parity.py tests/orchestration/test_run_manifest_strict_boundaries.py tests/orchestration/test_budget_guard.py tests/orchestration/schemas/test_schemas.py tests/orchestration/test_structured_outputs.py tests/orchestration/test_import_reachability.py tests/test_imports.py tests/test_ble001_ratchet.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_subprocess_timeouts.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/test_no_orphan_modules.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1593 passed, 7 skipped in 207.05s (0:03:27)
REAL_EXIT=0
```
The reviewer's own baseline (same selection LESS `test_task_injection_runner.py`,
at `4b6ccd1d9` before any change) read `1560 passed, 7 skipped` at exit 0.
`--collect-only -q` node counts of the three edited/new test files:
```
                          4b6ccd1d9    C6 (de08d9d48)
test_task_injection.py        43            67
test_plan_editing.py          44            47
test_task_injection_runner.py  0             6   (did not exist at 4b6ccd1d9)
```
Delta: (67-43) + (47-44) + (6-0) = 24 + 3 + 6 = 33. 1560 + 33 = 1593, exactly
this run's total — no unexplained difference. The seven skips are the same
F252 quarantines (6 in `test_named_bugs.py`, 1 in `test_agent_tooling.py`),
unchanged.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=161"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0.

### G5 — THE RED PROOFS
`git worktree add --detach .remedy-wt/f028-r2-mut de08d9d48` (C6) then
`python3 -B .agent/authored/f028-r2-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f028-r2-mut`, whole output:
```
control (before): exit=0 failed=0 nodes=[]
m1_read_injection_draft_treats_a_missing_expiry_as_live (packages/orchestration/task_injection.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection.py::TestReadInjectionDraftUntrustedExpiry::test_missing_expires_at_raises', 'tests/orchestration/test_task_injection.py::TestReadInjectionDraftUntrustedExpiry::test_non_string_expires_at_raises']
m2_confirm_task_injection_skips_the_status_check (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestConfirmTaskInjection::test_a_shortfall_draft_answers_draft_needs_decision']
m3_confirm_task_injection_skips_the_task_id_half_of_the_stale_check (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestConfirmTaskInjection::test_two_drafts_of_one_plan_the_second_confirmed_after_is_stale']
m4_apply_injection_to_job_omits_origin (packages/orchestration/task_injection.py): exit=1 failed=3 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJob::test_appends_provenance_bumps_version_and_reseals_an_approved_hash', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedBeforeTheRun::test_the_injected_task_runs_in_the_same_run_and_the_job_completes', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedWhileTheLastTaskRuns::test_the_injected_task_runs_in_the_same_run_and_the_job_completes']
m5_apply_injection_to_job_never_reseals_the_approval_hash (packages/orchestration/task_injection.py): exit=1 failed=3 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJob::test_appends_provenance_bumps_version_and_reseals_an_approved_hash', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedExactlyAtPointD::test_the_job_parks_paused_and_a_second_run_completes_it', 'tests/orchestration/test_task_injection_runner.py::TestInjectionFoldedOnlyOnceAcrossRuns::test_a_second_run_never_refolds_the_same_confirmation']
m6_apply_injection_to_job_leaves_the_plan_version_unchanged (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJob::test_appends_provenance_bumps_version_and_reseals_an_approved_hash']
m7_apply_injection_to_job_writes_dod_resync_pending_false_always (packages/orchestration/task_injection.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection.py::TestApplyInjectionToJob::test_dod_resync_pending_true_with_a_dod_file_present']
m8_add_task_admits_a_duplicate_id (packages/orchestration/plan_editing.py): exit=1 failed=1 nodes=['tests/orchestration/test_plan_editing.py::TestAddTaskEditKind::test_a_duplicate_id_is_refused']
m9_fold_point_a_is_removed (packages/orchestration/pingpong_job.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection_runner.py::TestConfirmedExactlyAtPointD::test_the_job_parks_paused_and_a_second_run_completes_it']
m10_fold_point_c_is_removed (packages/orchestration/pingpong_job.py): exit=1 failed=2 nodes=['tests/orchestration/test_task_injection_runner.py::TestConfirmedWhileTheLastTaskRuns::test_the_injected_task_runs_in_the_same_run_and_the_job_completes', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedExactlyAtPointD::test_the_job_parks_paused_and_a_second_run_completes_it']
m11_fold_point_d_no_longer_sets_job_paused (packages/orchestration/pingpong_job.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection_runner.py::TestConfirmedExactlyAtPointD::test_the_job_parks_paused_and_a_second_run_completes_it']
m12_the_fold_ignores_task_injections_and_folds_every_record (packages/orchestration/pingpong_job.py): exit=1 failed=3 nodes=['tests/orchestration/test_task_injection_runner.py::TestConfirmedBeforeTheRun::test_the_injected_task_runs_in_the_same_run_and_the_job_completes', 'tests/orchestration/test_task_injection_runner.py::TestConfirmedWhileTheLastTaskRuns::test_the_injected_task_runs_in_the_same_run_and_the_job_completes', 'tests/orchestration/test_task_injection_runner.py::TestInjectionFoldedOnlyOnceAcrossRuns::test_a_second_run_never_refolds_the_same_confirmation']
m13_the_folds_taskinjectionerror_branch_answers_false_without_blocking (packages/orchestration/pingpong_job.py): exit=1 failed=1 nodes=['tests/orchestration/test_task_injection_runner.py::TestCorruptConfirmedInjectionFile::test_blocks_with_task_injection_control_error_and_dispatches_nothing']
restored byte-identical: True (packages/orchestration/task_injection.py)
restored byte-identical: True (packages/orchestration/plan_editing.py)
restored byte-identical: True (packages/orchestration/pingpong_job.py)
control (after): exit=0 failed=0 nodes=[]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 13 mutations red with at least one failing node each; no mutation
stayed green, so no fix-up test was needed. `git worktree remove --force
.remedy-wt/f028-r2-mut` then `git worktree prune`, both exit 0; `git
worktree list | wc -l` read 62 afterwards, matching step 4's own reading.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f028-r2-block.md`, at `6f3e6e655`) vs
  `.remedy-wt/f028-r2/block.md`: byte-identical, sha256
  `58355c894fd6b8f4bbfd219b06f62d6aa986a7b839cd5a090e274c96fcbf03d3` both
  sides.
- `plan.md` copy (`.agent/authored/f028-r2-plan.md`, at `6f3e6e655`) vs
  `.remedy-wt/f028-r2-payloads/plan.md`: byte-identical, sha256
  `b5dd27102ef67aa1efc7a465d85701cebba375a7f68a62b2d1c04dd465584386` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.
- `records.diff` copy (`.agent/authored/f028-r2-records.diff`, at
  `6f3e6e655`) vs `.remedy-wt/f028-r2-payloads/records.diff`:
  byte-identical, sha256
  `eee1df8a3cef7ebbfda08fe8a7f0ba1c2825e2b3af76fbde7ff78309827a198a` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.

The production code (`task_injection.py`, `plan_editing.py`,
`pingpong_job.py`), its tests (three files) and the mutation tool
(`f028-r2-mutations.py`) are the WORKER's own authored code against the
block's specification S1–S6, not reviewer-authored text, so no fidelity
comparison applies to them.

## Deviations & assumptions

1. C5 was split into C5a/C5b, departing from the block's literal
   single-commit-per-letter sequence. Justification: constraint 2's own
   500-insertion cap — the three test files together are 396 + 38 + 330 =
   764 insertion lines, over the cap combined — and constraint 2 explicitly
   names this exact split ("C5a and C5b") as the required response. Split
   by artifact: the two files touching existing modules in C5a (434
   insertions), the new runner test file alone in C5b (330 insertions).
   Each half leaves its own tests green independently (114 passed / 6
   passed) and together they leave the full selection at 1593 passed.
2. An UNORDERED smoke-test worktree (`.remedy-wt/f028-r2-smoke`) was added
   and removed before writing the tool into its final, graded state, to
   catch a mutation-tool bug cheaply before the one worktree G5 orders.
   Cleaned up immediately; `git worktree list | wc -l` read 62 before and
   after, matching step 4's reading both times, so nothing outlasted it.
3. `confirm_task_injection`'s S4 terminal check reuses round 1's
   `injection_refusal(job_state, 0)` rather than a fresh terminal-only
   helper — the block names it explicitly as "S4 of round 1's terminal
   check (`job_terminal`)", and calling it with a plan-task count of 0
   never independently triggers `plan_full` (the real cap `MAX_PLAN_TASKS`
   is 25), so only the terminal branch is ever live at this call site.
4. `confirm_task_injection` and `apply_injection_to_job` both re-derive the
   `TaskPlan` from `job.task_plan` independently (each doing its own
   `{k: v for k, v in raw_plan.items() if not k.startswith("_")}` plus
   `TaskPlan.model_validate`), rather than one shared helper — because they
   are never called back-to-back against the SAME in-memory `job` (the
   confirm door and the runner's fold run in different processes/calls in
   the real system, only sharing state through the control files and the
   persisted record), so no single call site would benefit from sharing
   the parse, and the duplication mirrors `draft_task_injection`'s own
   inline pattern already established in round 1.
5. `_publish_confirmed_injection` returns a bare `bool` rather than raising
   on a lost race (unlike round 1's `_publish_injection_draft`, which
   raises because a draft-id collision "should never happen"): the block's
   S3 explicitly wants "a lost publication race answering
   `already_confirmed`", and a confirmation racing another confirmation of
   the SAME draft is a normal double-click, not a request-id collision.

No test went red unexpectedly, no reviewer payload was edited or retyped,
no gate was skipped, and every G5 mutation was caught on the first run — no
fix-up test was required.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5a | deviated | block named one commit "C5"; split into C5a/C5b under constraint 2's 500-line cap (see Deviations §1) |
| C5b | deviated | see C5a |
| C6 | done | |
| C7 | done | |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | all 13 mutations caught, both controls clean, all three files restored byte-identical |
| G6 | deviated | its readings (git log, git status, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |
| R-1076 | done | repaired at C3 (`3e9b7afa5`); its four cases pinned in `TestReadInjectionDraftUntrustedExpiry` at C5a; the repair awaits review before it can be marked `Done:` in the ledger |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 2,
then the second half of T002 — the shortfall seed's three answers, its
labels as a mapping, and the run-log event with its readers. Open findings
(by `open_finding_ids` at this round's head): 1 (R-1076, its repair
awaiting review). Operator questions open: 0.
