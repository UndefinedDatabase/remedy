# Handoff — F029, round 2

## Session

SESSION 1 of feature F029 · round 2 · rounds so far 2. Context remaining at
handback: comfortable — this round's context went mostly to reading the
source files and tests the block named (`subtree_rerun.py`, `pingpong_job.py`
sections, `worktrees.py`, `plan_editing.py`, `task_edit_runtime.py`,
`task_veto.py`, the `test_job_worktree_integration.py` harness) and drafting
`fold_subtree_rerun`/`prepare_subtree_rerun` against S1–S7; one repair loop
was needed (G4's BLE001 ratchet caught C5a's bare `except Exception`, fixed
in C5c with all gates re-run afterward), leaving ample context had a further
round been required this session.

## Range

Review of `0ae9f427`..`HEAD` (`HEAD` is this handback's own commit, `F029 R2
C6b`, on `feature/f029-subtree-rerun`).

## Commits

### 89ff794a0 F029 R2 C1: copy round 2 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r2-block.md | 282/0 | copy of this round's block |
| .agent/authored/f029-r2-booking.diff | 86/0 | copy of the booking diff payload |
| .agent/authored/f029-r2-plan.md | 34/0 | copy of the plan payload |

Measured insertions: 402 (block's own line count 282 + 120), matching the
block's expectation exactly, under the 500-line cap.

### 329dfb78a F029 R2 C2: book round 1's PASS, register R-1080, record D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 66/0 | DECISION F029 D2 appended |
| .agent/live_review.md | 4/0 | round 1's Gate entry and R-1080's registration appended |
| .agent/plan.md | 10/9 | rewrite from the plan payload |

Matches the block's expected numstat (66/0, 4/0, 10/9) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `booking.diff`,
followed by the `plan.md` rewrite via `shutil.copyfile`.

### cafea7db1 F029 R2 C3: R-1080 — refuse a rerun whose worktree head cannot be read
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 1/1 | S1: step d of `plan_subtree_reset` refuses `worktree_drift` whenever the live head is `""`, whatever `job.worktree_head` holds |
| tests/orchestration/test_subtree_rerun.py | 17/0 | one test: an empty `worktree_head` planned against a missing path still refuses `worktree_drift`, detail naming `unknown` |

### a0cc7d52c F029 R2 C4: carry attempts, a model override and reruns on the job record
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | 30/1 | S2: `TaskEntry.attempt`/`attempts`/`model_override` and `JobPlan.reruns`, each wired through `_export_job`/`_import_job` beside `spec_version`/`run_refs`; S3: the `run_pingpong(` call's `builder_model=(task.model_override or builder_model)` |

### b0add7836 F029 R2 C5a: prepare a subtree rerun on a job that is not running
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 269/5 | S4 (`fold_subtree_rerun`), S5 (`prepare_subtree_rerun`), the module docstring's T002 paragraph, and the new imports/constants (`HUMAN_OVERRIDE_REASON`, `RERUN_ADMITTED_STATES`, `_MODEL_OVERRIDE_RE`) both need |

### 6e4f506d4 F029 R2 C5b: test the subtree rerun preparation
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_subtree_rerun_prepare.py | 481/0 | new test file: S2 roundtrip (2 tests), S4 fold over synthetic entries (6 tests), S5 end to end through `run_job` with fake providers (1 test) and its refusals (7 tests) |

C5 was split into C5a/C5b under constraint 2: 269 (production) + 481
(tests) = 750 combined, over the 500-insertion cap; each part alone is well
under it. Split by artifact, mirroring round 1's C4a/C4b precedent.

### 9c903c202 F029 R2 C6a: add the mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r2-mutations.py | 179/0 | the G5 mutation (red-proof) tool, covering m1–m12 across `subtree_rerun.py` and `pingpong_job.py` |

### 1f7b1ae55 F029 R2 C5c: narrow the recovery handler to the exceptions apply_subtree_reset raises
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 4/1 | G4's serial run caught `tests/test_ble001_ratchet.py`'s frozen ratchet at 291 excused handlers, over 290; C5a's bare `except Exception as exc:  # noqa: BLE001` for the "kept for recovery" path is narrowed to `except (SubtreeRerunError, W.WorktreeError) as exc:`, the only two exceptions `apply_subtree_reset` can raise past `SubtreeRerunRefused` (handled separately) |

An EXTRA commit beyond the block's named C1–C6 sequence, landing after C6a
in linear history though it repairs C5a's code — see Deviations §2.

### F029 R2 C6b: rewrite handoff for round 2 (this commit — a handback cannot table the commit that writes it, R-0149 pattern)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | new | this handback |

## External actions

- `git apply --check .remedy-wt/f029-r2-payloads/booking.diff` (exit 0),
  then the real `git apply` (exit 0), at C2.
- `git worktree add --detach .remedy-wt/f029-r2-mut 1f7b1ae55` (this
  round's final tip, after C5c — see Deviations §2) for G5 — succeeded.
  `git worktree remove --force .remedy-wt/f029-r2-mut` then `git worktree
  prune` afterwards — both succeeded; `git worktree list | wc -l` read 61
  before the add and 61 after the remove, matching step 4's own reading of
  61 both times.
- `git push -u origin feature/f029-subtree-rerun` after C6b — reported
  under G6 in this round's reply (run after this file is committed).
- No `gh pr create` (a pull request already exists for this branch since
  round 1; this round adds no new PR), no `gh pr merge`, no checkout of
  `main`, no branch deletion, no force-push, no `git stash`.

## Verification

### G1 — TRANSPORT
Payload readings (measured before use, against the PAYLOADS table — all
MATCH):
- `booking.diff`: 86 lines, 14419 bytes, sha256
  `bc5d5bb90d471892243191c339e60935a3b669a7973df0bd8c055e742bf5ef5c`.
- `plan.md`: 34 lines, 1224 bytes, sha256
  `ffa31d57260b51ece7f6f9c81a91a3fed0071a76f8167481481a60590cd2964d`.
- Block: 282 lines, sha256
  `494daa73124cbf881efe7c61bfc9cb17b6222ecb4f8e57483ef9e83fa92532e7` — MATCH
  against both readings the delegation message stated.

Each `.agent/authored/f029-r2-*` payload copy, read back with `git show
89ff794a0:<path>`, compared byte-for-byte (sha256) against its source —
all three MATCH (identical bytes and sha256 to the source):
```
f029-r2-block.md      lines=282 bytes=23136 sha256=494daa73124cbf881efe7c61bfc9cb17b6222ecb4f8e57483ef9e83fa92532e7 EQUALS_SOURCE=True
f029-r2-booking.diff   lines=86  bytes=14419 sha256=bc5d5bb90d471892243191c339e60935a3b669a7973df0bd8c055e742bf5ef5c EQUALS_SOURCE=True
f029-r2-plan.md        lines=34  bytes=1224  sha256=ffa31d57260b51ece7f6f9c81a91a3fed0071a76f8167481481a60590cd2964d EQUALS_SOURCE=True
```

### G2 — THE BOOKING
`git show 329dfb78a:<path>`, bytes and sha256, each MATCHING the reviewer's
table exactly:
```
.agent/decisions.md    bytes=2287154  a0109b36884fa89227762c9af219e2a9d1975f673ef2e2147c4582a79e91416d
.agent/live_review.md  bytes=311765   a0b8341219b70e3a38debefeeea59c8a98bbf4ca259dde9b4e076e8c1e1d30a7
.agent/plan.md         bytes=1224     ffa31d57260b51ece7f6f9c81a91a3fed0071a76f8167481481a60590cd2964d
```
All three MATCH. `open_finding_ids` from `scripts/rotate_live_review.py`,
called directly against `.agent/live_review.md`'s TEXT at `0ae9f427` and at
`329dfb78a` (C2): `[]` and `['R-1080']` respectively — matching the
reviewer's reading exactly (empty before, `['R-1080']` after).

### G3 — THE CODE
```
$ bash -c 'python3 -m ruff check packages/orchestration/subtree_rerun.py packages/orchestration/pingpong_job.py tests/orchestration/test_subtree_rerun.py tests/orchestration/test_subtree_rerun_prepare.py; echo "REAL_EXIT=$?"'
All checks passed!
REAL_EXIT=0
```
(Re-run at the final tip `1f7b1ae55`, after C5c's narrowing — also passed
at the pre-C5c tip, `9c903c202`, before the ratchet fix.)

`prepare_subtree_rerun`, quoted whole from `git show
1f7b1ae55:packages/orchestration/subtree_rerun.py` (the commit that landed
its final form, after C5c's fix):

```python
def prepare_subtree_rerun(
    job_id: str,
    root_task_id: str,
    *,
    model_override: str = "",
    actor: str = "operator",
    now: datetime | None = None,
) -> dict[str, Any]:
    """DECISION F029 D2 — prepare a subtree rerun on a job that is NOT running.

    Re-acquires the job's worktree under its lock (re-adding it from the kept branch
    when the job had completed), resets the subtree with ``apply_subtree_reset``, and
    returns the subtree's tasks to pending with the finished attempt archived on each
    (S4's fold, ``fold_subtree_rerun``). Runs no provider and starts no task itself:
    ``remedy job run`` (round 3's command) is what re-executes the pending subtree.

    Raises ``SubtreeRerunRefused`` from the first unsafe condition, admission checks
    before anything worktree-related is touched, then ``apply_subtree_reset``'s own
    ladder once the worktree is claimed. A refusal removes a worktree this call
    created, or releases the lock on one that already existed, and leaves ``job.json``
    unchanged.
    """
    bounded_actor = task_veto._bounded_actor(actor)
    at = now or datetime.now(timezone.utc)

    with plan_editing.plan_edit_lock(job_id):
        job = load_job_plan(job_id)
        if job is None:
            raise SubtreeRerunRefused("job_not_found", f"there is no job {job_id!r}")

        if model_override and not _MODEL_OVERRIDE_RE.match(model_override):
            raise SubtreeRerunRefused(
                "model_invalid",
                f"{model_override!r} is not a valid model override; it must match "
                f"{_MODEL_OVERRIDE_RE.pattern}",
            )

        state = str(job.state)
        if state == "running":
            raise SubtreeRerunRefused(
                "job_running", "the job is running; pause or stop it, then rerun")
        if state not in RERUN_ADMITTED_STATES:
            raise SubtreeRerunRefused(
                "job_not_rerunnable",
                f"the job is {state!r}; a rerun needs a job that has completed, "
                f"blocked, paused or stopped",
            )

        subtree_ids = rerun_subtree_ids(job.tasks, root_task_id)   # unknown_task
        tasks_by_id = {t.task_id: t for t in job.tasks}
        root_task = tasks_by_id[root_task_id]

        if job.isolation_mode != "worktree":
            raise SubtreeRerunRefused(
                "not_worktree_mode",
                "the job ran in a copy of the repository, not on a job branch, "
                "so no task has a commit to go back to",
            )
        if not root_task.worktree_commit:
            raise SubtreeRerunRefused(
                "task_not_committed",
                f"task {root_task_id} has no commit on the job branch yet, "
                f"so there is nothing to rerun",
            )
        if not W._branch_exists(job.repo_path, job.worktree_branch):
            raise SubtreeRerunRefused(
                "job_branch_missing",
                f"job branch {job.worktree_branch!r} no longer exists",
            )
        if not job.job_initial_tree or not W.object_exists(job.repo_path, job.job_initial_tree):
            raise SubtreeRerunRefused(
                "checkpoint_object_missing",
                f"the job's initial tree {job.job_initial_tree!r} is gone",
            )

        try:
            handle = W.create(job_worktree_id(job_id), job.repo_path)
        except W.WorktreeLockError:
            raise SubtreeRerunRefused(
                "job_running", "the job is running; pause or stop it, then rerun") from None
        except W.WorktreeConflictError as exc:
            raise SubtreeRerunRefused("worktree_conflict", str(exc)) from exc

        try:
            reset = apply_subtree_reset(job, root_task_id, handle.path)
        except SubtreeRerunRefused:
            if handle.created:
                W.remove(handle, keep_branch=True)
            else:
                W.release_lock(handle)
            raise
        except (SubtreeRerunError, W.WorktreeError) as exc:
            # Every OTHER exception `apply_subtree_reset` can raise: a failed hash
            # proof or a git operation on the worktree itself. Kept for recovery,
            # never removed — an unproven or half-made reset must stay inspectable.
            W.retain_for_recovery(handle, f"{type(exc).__name__}: {exc}")
            raise

        moved_streams: dict[str, str] = {}
        evidence_root = job_evidence_dir(job_id)
        for task_id in subtree_ids:
            task = tasks_by_id[task_id]
            if not _task_ran(task):
                continue
            stream_dir = _task_stream_dir(job_id, task_id)
            if not stream_dir.exists():
                continue
            dest_rel = f"rerun_attempts/{task_id}/attempt-{task.attempt}"
            dest = evidence_root / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            os.replace(stream_dir, dest)
            moved_streams[task_id] = dest_rel

        rerun_id = f"rerun-{len(job.reruns) + 1}"
        record = fold_subtree_rerun(
            job, reset, rerun_id=rerun_id, model_override=model_override,
            actor=bounded_actor, now=at, moved_streams=moved_streams,
        )

        ref = job.job_initial_tree_ref
        if W.resolve_checkpoint_ref(job.repo_path, ref) != job.job_initial_tree:
            W.set_checkpoint_ref(job.repo_path, ref, job.job_initial_tree)

        save_job_plan(job)
        W.release_lock(handle)

        return {**record, "job_id": job_id, "worktree_rematerialized": handle.created}
```

The `run_pingpong(` call's `builder_model=` line, from `git show
a0cc7d52c:packages/orchestration/pingpong_job.py` (C4, unchanged since):
```python
                    builder_model=(task.model_override or builder_model),
```

### G4 — THE TESTS
Final run, at the round's completed tip `1f7b1ae55` (after C5c's fix):
```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_subtree_rerun.py tests/orchestration/test_subtree_rerun_prepare.py tests/orchestration/test_worktrees.py tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_plan.py tests/orchestration/test_job_plan_state_reads.py tests/orchestration/test_job_run_refs.py tests/orchestration/test_pingpong_job_dod_gate.py tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_job_evidence.py tests/orchestration/test_dag_schedule.py tests/orchestration/test_checkpoints.py tests/orchestration/test_task_veto.py tests/cli/test_job_commands.py tests/cli/test_job_run_invocation_truth.py tests/cli/test_job_pause.py tests/test_subprocess_timeouts.py tests/test_ble001_ratchet.py tests/test_no_orphan_modules.py tests/test_imports.py tests/orchestration/test_import_reachability.py tests/orchestration/test_durable_write_guard.py tests/test_data_paths.py tests/test_no_interactive_guard.py tests/test_path_utils.py tests/regression/test_named_bugs.py tests/orchestration/test_development_artifact_boundary.py tests/regression/test_resource_safety.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -12; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1250 passed, 7 skipped in 162.21s (0:02:42)
REAL_EXIT=0
```
The reviewer's own baseline (same selection, at `0ae9f427`) read `1233
passed, 7 skipped` at exit 0. `--collect-only -q` over the two touched test
files reads `tests/orchestration/test_subtree_rerun.py: 21` and
`tests/orchestration/test_subtree_rerun_prepare.py: 16` at this tip, 37
total; the same collection at `0ae9f427` reads 20 for
`test_subtree_rerun.py` (`git show 0ae9f427:tests/orchestration/
test_subtree_rerun.py | grep -c "    def test_"` → 20) and the second file
did not exist (0). The round therefore added 37 − 20 = 17 nodes;
1233 + 17 = 1250, exactly this run's total — no unexplained difference.
The seven skips are the same F252 quarantines, unchanged.

An earlier run at the pre-repair tip `9c903c202` (C5a's code, before
C5c) failed at exit 1: `1 failed, 1249 passed, 7 skipped` —
`tests/test_ble001_ratchet.py::test_the_count_of_excused_handlers_never_rises`
read `291 excused blind handlers, above the frozen 290` — see Deviations §2.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=164"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks read `pass`, `fail_count` 0; `high_blockers_open` reads
`pass` because R-1080 is Low, as expected.

### G5 — THE RED PROOFS
Run at the round's final tip `1f7b1ae55` (after C5c — see Deviations §2,
the mutation tool itself needed no change since m8's target text is
untouched by C5c's fix). `git worktree add --detach .remedy-wt/f029-r2-mut
1f7b1ae55` then `python3 -B .agent/authored/f029-r2-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r2-mut`, whole output:
```
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f029-r2-mut
control (before): exit=0 failed=0 failing=[]
m1 step d compares the live head with job.worktree_head again, as before S1: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun.py::TestRefusalsAreSideEffectFree::test_r1080_empty_worktree_head_with_missing_path_still_refuses_worktree_drift'] caught=True
m2 S4 does not raise attempt: exit=1 failed=2 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestFoldSubtreeRerun::test_attempt_record_and_every_cleared_field', 'tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m3 S4 appends no attempt record: exit=1 failed=2 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestFoldSubtreeRerun::test_attempt_record_and_every_cleared_field', 'tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m4 S4 keeps worktree_commit: exit=1 failed=2 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestFoldSubtreeRerun::test_attempt_record_and_every_cleared_field', 'tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m5 S4 leaves a skipped task outside the subtree as it is: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestFoldSubtreeRerun::test_skipped_outside_task_restored_applied_one_is_not'] caught=True
m6 S4 leaves a completed job completed: exit=1 failed=2 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestFoldSubtreeRerun::test_completed_job_becomes_paused', 'tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m7 the run_pingpong( call passes builder_model alone: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m8 S5 releases the lock on a refusal instead of removing a worktree it created: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunRefusals::test_worktree_drift_after_re_add_removes_the_worktree_again'] caught=True
m9 S5 does not set the job_initial_tree_ref again: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m10 S5 moves no stream directory: exit=1 failed=1 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m11 the export drops the attempts key: exit=1 failed=3 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestS2Fields::test_every_new_field_set_survives_save_and_load', 'tests/orchestration/test_subtree_rerun_prepare.py::TestS2Fields::test_a_record_without_the_four_keys_loads_defaults', 'tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
m12 S4 leaves worktree_cleanup_status as it was: exit=1 failed=2 failing=['tests/orchestration/test_subtree_rerun_prepare.py::TestFoldSubtreeRerun::test_completed_job_becomes_paused', 'tests/orchestration/test_subtree_rerun_prepare.py::TestPrepareSubtreeRerunEndToEnd::test_prepare_then_rerun_with_model_override'] caught=True
control (after): exit=0 failed=0 failing=[]
restored byte-identical (packages/orchestration/subtree_rerun.py): True
restored byte-identical (packages/orchestration/pingpong_job.py): True
restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
All 12 mutations red with at least one failing node each, on the first
run — no repair loop needed for G5 itself. `git worktree remove --force
.remedy-wt/f029-r2-mut` then `git worktree prune` — both exit 0; `git
worktree list | wc -l` read 61 afterwards, matching step 4's own reading.

Independently re-verified byte-identical restoration by sha256, before and
after the tool ran: `subtree_rerun.py`
`4f1bc37f3925cfac8c9f9fa6cff135bdb697ba77b22ba10ee5fbd119bd0bd332` and
`pingpong_job.py`
`605b881e7749bdbe52f4ed6c979eaa7d65232cb0b6c51036c8d2d6df3bcdab79`, both
sides equal.

(G6 — TREE AND PUSH runs after this commit; its readings are in the round
reply, not here, since this commit cannot contain them.)

## Authored-text proofs

- Block copy (`.agent/authored/f029-r2-block.md`, at `89ff794a0`) vs
  `.remedy-wt/f029-r2/block.md`: byte-identical, sha256
  `494daa73124cbf881efe7c61bfc9cb17b6222ecb4f8e57483ef9e83fa92532e7` both
  sides.
- `booking.diff` copy (`.agent/authored/f029-r2-booking.diff`, at
  `89ff794a0`) vs `.remedy-wt/f029-r2-payloads/booking.diff`:
  byte-identical, sha256
  `bc5d5bb90d471892243191c339e60935a3b669a7973df0bd8c055e742bf5ef5c` both
  sides; applied via `git apply --check` (exit 0) then the real apply
  (exit 0) at C2; never edited or retyped.
- `plan.md` copy (`.agent/authored/f029-r2-plan.md`, at `89ff794a0`) vs
  `.remedy-wt/f029-r2-payloads/plan.md`: byte-identical, sha256
  `ffa31d57260b51ece7f6f9c81a91a3fed0071a76f8167481481a60590cd2964d` both
  sides; used to rewrite `.agent/plan.md` via `shutil.copyfile` at C2.

The production code (`subtree_rerun.py`'s S1/S4/S5, `pingpong_job.py`'s
S2/S3), its tests (`test_subtree_rerun.py`'s new test,
`test_subtree_rerun_prepare.py`) and the mutation tool
(`f029-r2-mutations.py`) are the WORKER's own authored code against the
block's specification S1–S7, not reviewer-authored text, so no fidelity
comparison applies to them.

## Deviations & assumptions

1. C5 was split into C5a/C5b, departing from the block's literal
   single-commit "C5" naming. Justification: constraint 2's own
   500-insertion cap — the production code (269) plus the new test file
   (481) together are 750, over the cap combined — and constraint 2
   explicitly names this exact split ("C5a, C5b, ...") as the required
   response. Split by artifact: production in C5a, tests in C5b, mirroring
   round 1's C4a/C4b precedent.
2. A commit beyond the block's named C1–C6 sequence, `C5c`, was added
   after `C6a`. G4's serial run at `9c903c202` (the tip right after C6a)
   failed: `tests/test_ble001_ratchet.py::test_the_count_of_excused_
   handlers_never_rises` read 291 excused blind handlers against the
   frozen ceiling of 290, because C5a's `except Exception as exc:  #
   noqa: BLE001` in `prepare_subtree_rerun`'s "kept for recovery" path
   added a new excused mark. AGENTS.md's Commit Discipline forbids
   raising that ceiling to make the check green, and its git safety
   protocol prefers a new commit over amending one already made (C5a was
   not amended). C5c narrows the handler to `(SubtreeRerunError,
   W.WorktreeError)` — the only two exceptions `apply_subtree_reset` can
   raise past `SubtreeRerunRefused`, which is handled in the branch above
   it — removing the need for a `# noqa: BLE001` mark entirely, so the
   excused-handler count returns to 290. Because C5c necessarily lands
   after C6a in linear history, G3's `prepare_subtree_rerun` quote, the
   full G4 test run and G5's mutation-tool worktree were all taken at the
   round's FINAL tip (`1f7b1ae55`, after C5c) rather than literally at the
   commit named `C6a` — running them against the pre-fix code would have
   validated a version of the module this round no longer ships. This is
   the one substitution of "at C6a" the block's own G4/G5 wording implies;
   G1 and G2, which do not depend on the exception-handling fix, are
   unaffected and were read at their own named commits (C1, C2) as
   ordered.
3. S6's `ALLOWED_UNWIRED` entry for `subtree_rerun.py` was left unchanged:
   its reason ("F029 T001's subtree reset; T002's rerun command wires it
   (DECISION F029 D1)") remains true after this round — `prepare_
   subtree_rerun` is T002's preparation half, still uncalled from any
   command; round 3's `remedy job rerun-subtree` is what wires the module,
   exactly as the entry already says.
4. The block gives exact, quotable wording for most of the ordered
   refusals but leaves `job_branch_missing` and `checkpoint_object_missing`
   to name their subject rather than a literal string. Assumption:
   composed prose naming the missing branch or tree respectively, in the
   same terse style as the existing refusals in `plan_subtree_reset`.
5. `retain_for_recovery`'s error argument ("<the error>", not literally
   specified) is composed as `f"{type(exc).__name__}: {exc}"`, matching
   the existing convention elsewhere in this codebase (e.g.
   `worktrees.remove`'s own cleanup-error formatting,
   `pingpong_job._absorb_at_safe_point`).
6. "S2 of round 1's `unknown_task`" is read as: call `rerun_subtree_ids`
   (which itself raises `SubtreeRerunRefused("unknown_task", ...)`) at
   that position in `prepare_subtree_rerun`'s admission ladder — the same
   mechanism `plan_subtree_reset`'s own step `a` already uses, reused
   rather than reimplemented.

No test went red unexpectedly beyond the one repair loop above (§2), no
reviewer payload was edited or retyped, and no gate was skipped.

Landed: R-1080 — step d of `plan_subtree_reset` now refuses `worktree_drift`
whenever the live head is `""`, whatever `job.worktree_head` holds, pinned by
a new test with an empty recorded head and a missing worktree path, both
verified by G4's full run and G5's mutation m1.

## Item-status table

| Item | Status | Reason |
|------|--------|--------|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5a | deviated | block named one commit "C5"; split into C5a/C5b under constraint 2's 500-line cap (see Deviations §1) |
| C5b | deviated | see C5a |
| C5c | deviated | additional commit beyond the block's named sequence, repairing C5a's BLE001 ratchet regression G4 caught after C6a (see Deviations §2) |
| C6a | done | |
| C6b | done | this commit |
| S1 | done | R-1080 repaired: step d refuses `worktree_drift` whenever the live head is `""` |
| S2 | done | `TaskEntry.attempt`/`attempts`/`model_override` and `JobPlan.reruns`, exported/imported with defaults for a pre-F029 record |
| S3 | done | `run_pingpong(`'s `builder_model=(task.model_override or builder_model)` |
| S4 | done | `fold_subtree_rerun` — attempts archived, fields cleared, outside-skipped tasks restored, job state/cleanup updated, `reruns` record appended |
| S5 | done | `prepare_subtree_rerun` — admission ladder, worktree re-acquisition, stream-evidence move, fold, checkpoint-ref refresh, single save |
| S6 | done | `ALLOWED_UNWIRED` entry left unchanged; its reason is still true (see Deviations §3) |
| S7 | done | no command, no event, no edit to `apps/`, `worktrees.py`, `checkpoints.py`, `dag_schedule.py`, `task_edit_runtime.py` or `plan_editing.py` |
| G1 | done | |
| G2 | done | |
| G3 | done | re-run at the final tip after C5c; passed both before and after |
| G4 | deviated | run twice: at `9c903c202` (pre-C5c) 1 failed/1249 passed — the BLE001 ratchet; at `1f7b1ae55` (post-C5c) 1250 passed, 7 skipped, exit 0, integrity clean |
| G5 | done | run once at the final tip `1f7b1ae55`; all 12 mutations caught, restored byte-identical |
| G6 | deviated | its readings (git status, git log, worktree count, push outcome, `gh pr list`) are necessarily taken after this commit and the subsequent push; they appear in the round reply, per the block's own note that this commit cannot contain them |

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 2,
then the second half of T002 — `remedy job rerun-subtree` with the
subtree's cost estimate, the cost preview's confirmation, and the run-log
event with its readers. Open findings (by `open_finding_ids` at this
round's head): 1 (R-1080, landed and awaiting review). Operator questions
open: 0.
