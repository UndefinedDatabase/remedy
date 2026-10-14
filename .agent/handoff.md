# Handback — F308 round 4 — the closure's consolidation pass, self-use item and one full suite

## Session

SESSION 1 of feature F308 · round 4 · rounds so far 4

Context self-assessment: C1 to C4 landed clean on the first attempt, with no repair and nothing
re-run; both long runs (the self-use job and the full suite) came back exactly as their gates
require, and context held comfortably throughout.

Fortschritt: ~85 % (T001 to T003 landed; the consolidation pass, the self-use run and the one full
suite done · the evidence, the package and the closing round remain) — Schätzung

## Range

Review of `8b8d08206`..`2dff08d0d`

## Commits

| Commit | Path | +/- |
|---|---|---|
| `c58085d86` F308 R4 C1 | `.agent/authored/f308-r4-selfuse.py` | +122/-0 |
| `c58085d86` F308 R4 C1 | `.agent/authored/f308-r4.md` | +164/-0 |
| `c58085d86` F308 R4 C1 | `.agent/live_review.md` | +2/-0 |
| `c58085d86` F308 R4 C1 | `.agent/plan.md` | +6/-5 |
| `68bdcff95` F308 R4 C2 | `docs/agents/planner_reviewer_prompt.md` | +6/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/SU-063.md` | +17/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/changed_paths.txt` | +2/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/entry_and_job_file.txt` | +5/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/execution_config.txt` | +43/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/full_transcript.txt` | +14/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/job_diff.txt` | +27/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/result_state.txt` | +12/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/run_defects.txt` | +1/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/staleness_after.txt` | +2/-0 |
| `0b87b714b` F308 R4 C3 | `.agent/selfuse_f308/timing.txt` | +3/-0 |
| `0b87b714b` F308 R4 C3 | `scripts/self_use_queue.json` | +8/-0 |
| `2dff08d0d` F308 R4 C4 | `.agent/authored/f308-closure-suite.txt` | +28/-0 |
| (this commit) F308 R4 C5 | `.agent/handoff.md` | this commit |

## External actions

- No worktree added or removed beyond the pre-existing `.remedy-wt/f308-r4-worker/` scratch
  directory the block told the worker to use for throwaway proof/copy scripts and the two long
  runs' logs; nothing under it is tracked or committed. The self-use runner's own job workspace at
  `.remedy-wt/job-200387721a384487` and the job's own branch `remedy/job-200387721a384487` are the
  runner's, not this worker's, and are left as the run produced them.
- No `gh pr merge`, `gh pr edit`, `gh pr create` this round (the block orders none; no pull
  request is open for this branch).
- No branch created beyond the one already checked out.
- Push (`git push origin feature/f308-run-manifest-task-split`) runs after this commit; its
  outcome is reported in the session's final reply only, per the write-once rule — it did not
  exist when this file was written.

## Verification

Preconditions confirmed before C1: `git rev-parse HEAD` and `git rev-parse
origin/feature/f308-run-manifest-task-split` both read `8b8d0820687653551e4fe128257e86b3f7042522`;
`git status --porcelain` was empty; `.agent/STOP` was absent; `git branch --show-current` read
`feature/f308-run-manifest-task-split`. `block.md` was verified first: 164 lines, sha256
`67ba64d36aee7e1ceb0b5d997e9c2dcb62f15c9dc926c1e622d11b0dbd518206` — matches the digest given in
the prompt. `dry-live_review.md`, `dry-plan.md`, `dry-planner_reviewer_prompt.md`, `launch.py`,
`selfuse.py`, `verify.py` and `wait.py` were each checked by `sha256sum` against the digests given
in the prompt before any use; all seven matched. `git branch --show-current` was re-run
immediately before every commit and read `feature/f308-run-manifest-task-split` each time.

C1: the four files were copied by a disposable script and the copy proven by a second,
read-only script printing bytes-equality: `True` for all four, plus the block's own line count
(164) and sha256 (matching above). `git status --porcelain` then showed exactly the four named
paths; committed.

C2: `docs/agents/planner_reviewer_prompt.md` was copied over wholesale; `git diff --stat` read `1
file changed, 6 insertions(+)`; `git status --porcelain` showed only that path; committed.
`git show --numstat` of the resulting commit (`68bdcff95`) read `6\t0\tdocs/agents/planner_reviewer_prompt.md` — the `6 0` the block requires.

C3: `python3 .../launch.py selfuse ...` started the detached run; `python3 .../wait.py selfuse ...
50` was run once and returned on its first call with `exit 0 wall 179.8`. The run generated
`SU-063` (tier 4, the excused handler at `apps/cli/commands/status_cmd.py:81`), planned and ran it
through `self_use`'s configured provider to the approval gate, and never applied it.
`git status --porcelain` afterward showed exactly `M scripts/self_use_queue.json` and `??
.agent/selfuse_f308/`; `git diff scripts/self_use_queue.json` showed exactly one appended entry,
id `SU-063`, `"consumed_by": ""`. All ten files under `.agent/selfuse_f308/` existed and were
non-empty (sizes in gate 2 below); committed.

C4: reflog before (`0b87b714b ... F308 R4 C3: ...`) was read, then `python3 .../launch.py suite
...` started the suite and `python3 .../wait.py suite ... 50` returned on its first call with
`23032 passed, 22 skipped, 1 warning in 344.69s (0:05:44)` and `exit 0 wall 345.4`. Reflog after
matched reflog before byte-for-byte — the branch did not move during the run. `grep -c '^FAILED'`
on the suite log read `0`; no "process(es) behind" or ended-process line was present. The cost
script then ran once: exit 0, `Test load: 1170.14 CPU seconds, 344.70 wall seconds, 23054 tests
collected, exit status 0, recorded 2026-10-14T11:50:17Z`, `11.4 percent less than F306's 1321.14,
within the 14.1 percent limit`. The transcript `.agent/authored/f308-closure-suite.txt` was
written in the F306 shape (minus the two repair-only "bad set" lines the block excludes) and
committed alone; `git status --porcelain` showed only that one new path before the commit.

Gate 1: `git status --porcelain` — empty. `python3 .../verify.py /home/decodeux/Repos/remedy` —
19 lines, every one `True`, last line `ALL True`.

Gate 2: the ten files under `.agent/selfuse_f308/`, sizes in bytes: `SU-063.md` 1037,
`entry_and_job_file.txt` 399, `execution_config.txt` 1367, `result_state.txt` 810, `timing.txt`
105, `changed_paths.txt` 61, `full_transcript.txt` 1578, `staleness_after.txt` 59, `job_diff.txt`
1234, `run_defects.txt` 5 — all non-empty.

Gate 3: exit code `0`; summary line `23032 passed, 22 skipped, 1 warning in 344.69s (0:05:44)`;
bad node ids `NONE` — as the transcript records them.

Gate 4: `python3 -m apps.cli.main integrity check --json` — `"check_count": 6`, every check
`"status": "pass"`, `"fail_count": 0`, `"ok": true`, `"passed": true`.
`python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(...))"` — list
`['R-1246', 'R-1252', 'R-1276', 'R-1277', ..., 'R-1315']` — R-1246, R-1252, then R-1276 to R-1315
in order, length 42.

Gate 5 (after push): reported in the session's final reply only, per the write-once rule.

## Authored-text proofs

- `.agent/authored/f308-r4.md` against `block.md`: byte-equal, 164 lines, sha256
  `67ba64d36aee7e1ceb0b5d997e9c2dcb62f15c9dc926c1e622d11b0dbd518206`.
- `.agent/authored/f308-r4-selfuse.py` against `selfuse.py`: byte-equal.
- `.agent/live_review.md` (C1) against `dry-live_review.md`: byte-equal.
- `.agent/plan.md` (C1) against `dry-plan.md`: byte-equal.
- `docs/agents/planner_reviewer_prompt.md` (C2) against `dry-planner_reviewer_prompt.md`:
  byte-equal.
- C3 and C4 wrote no prepared reviewer-authored text — C3 ran the reviewer-authored, never-edited
  `selfuse.py` and C4 ran the launcher/waiter pair plus `closure_suite_cost.py` verbatim, and both
  commits' content is the real output those runs produced, not an authored paste.

## Self-use run

Entry `SU-063` — "Narrow the excused handler at apps/cli/commands/status_cmd.py:81" — job id
`200387721a384487`. Builder: `claude-cli`, model `claude-sonnet-4-6`. Reviewer: `claude-cli`,
model `claude-sonnet-4-6`. Job state `completed`, stop reason (empty). Task `T001`: status
`applied_to_job_workspace`, reviewer verdict `pass`, final status `staged_review_passed`,
repair_rounds_used `1`, run_id `c20c49d39abc42f7`. Wall seconds: `175.7`. Changed paths:
`apps/cli/commands/status_cmd.py`, `tests/test_ble001_ratchet.py`.

Job diff, verbatim:
```
$ git diff HEAD...remedy/job-200387721a384487  (exit 0)
diff --git a/apps/cli/commands/status_cmd.py b/apps/cli/commands/status_cmd.py
index f535e879d..3dcabc126 100644
--- a/apps/cli/commands/status_cmd.py
+++ b/apps/cli/commands/status_cmd.py
@@ -78,7 +78,7 @@ def _cmd_status(
             events = load_run_events(resolve_data_root(), j.job_id)
             decs = list_decisions(j, events)
             decisions_open += sum(1 for d in decs if d.status == "open")
-        except Exception:  # noqa: BLE001 — decision-count failure must not break the status overview
+        except (OSError, ValueError, ImportError):
             pass
 
     # F276 T002: the same three states this block used to spell for itself, now read
diff --git a/tests/test_ble001_ratchet.py b/tests/test_ble001_ratchet.py
index ff1f68ae3..cb21e641a 100644
--- a/tests/test_ble001_ratchet.py
+++ b/tests/test_ble001_ratchet.py
@@ -18,7 +18,7 @@ REASONED = re.compile(r"^ — \S")
 
 #: The number of excused blind handlers when BLE001 was turned on. Only ever falls: the
 #: commit that removes a mark lowers this number in the same commit, and it is never raised.
-MAX_EXCUSED = 285
+MAX_EXCUSED = 284
 
 
 def _marks() -> list[tuple[str, int, str]]:
```

`run_defects.txt`, verbatim:
```
NONE
```

No finding is registered by this worker for the self-use run; the reviewer mints ids from the
verbatim quote above (which is empty).

## Closure suite

`.agent/authored/f308-closure-suite.txt`, whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 345.4s (the launcher's reading); pytest's own reported wall time: 344.69s (0:05:44)
summary line: 23032 passed, 22 skipped, 1 warning in 344.69s (0:05:44)
bad node ids (failed + errors):
  NONE
leftover processes: NONE
tree it ran on: 0b87b714b (F308 R4 C3: the closure's self-use item run to its approval gate, never applied)
tree note: C3 changed only .agent/ files and the self-use queue
reflog before: 0b87b714b HEAD@{2026-10-14 13:44:24 +0200}: commit: F308 R4 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 0b87b714b HEAD@{2026-10-14 13:44:24 +0200}: commit: F308 R4 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F308 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1170.14 CPU seconds, 344.70 wall seconds, 23054 tests collected, exit status 0, recorded 2026-10-14T11:50:17Z
This closure's suite used 1170.14 CPU seconds, 11.4 percent less than F306's 1321.14, within the 14.1 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 14.1 percent.
The test modules whose CPU time rose most since F306's closure run:
  +3.36 s  tests/orchestration/test_self_use_generator.py (3.84 -> 7.20)
  +1.02 s  tests/orchestration/test_run_manifest_call_task_binding.py (2.21 -> 3.23)
  +0.52 s  tests/orchestration/test_persisted_run_call_schema.py (1.77 -> 2.29)
  +0.44 s  tests/cli/test_job_show.py (1.24 -> 1.68)
  +0.40 s  tests/orchestration/test_review_final_verifier_reproducible.py (1.06 -> 1.46)
  +0.39 s  tests/orchestration/test_structured_log.py (0.08 -> 0.47)
  +0.38 s  tests/cli/test_plan_cli.py (5.03 -> 5.41)
  +0.37 s  tests/orchestration/test_job_evidence.py (9.01 -> 9.38)
  +0.36 s  tests/cli/test_job_rerun_manifest.py (1.72 -> 2.08)
  +0.33 s  tests/cli/test_do_flags.py (4.44 -> 4.77)
```

## Deviations & assumptions

None. C1 to C4 landed in the block's ordered sequence with no repair, no re-run, and no commit
amended; both long runs came back on their first `wait.py` call.

## Next

1. Phase 1 rule 1: `.agent/STOP` — absent at this handoff.
2. Rule 2, the Open PR Gate: no pull request is open for this branch yet.
3. The reviewer reviews round 4, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The evidence bundle and the review package (the suite is green).
5. The closing round: the Built State, the resolutions, the rotation, the STATUS line and the pull
   request.

Operator questions open: 0.
Open findings: 42 (R-1252, R-1314 and R-1315 owned by F308, the rest by F307).

## For the operator, in plain sentences

The paid run was asked to narrow one overly broad error handler in the status command's code so
it only catches the specific errors that can actually happen there, and it finished with the
model's own review approving the change on its own separate branch, without touching the main
line of work. Its record of what ran was written this time, in full — every file the run exists
to produce was created and has content. The whole test collection passed completely: 23,032 tests
passed, 22 were intentionally skipped, and none failed. The run took a little under six minutes.
The cost script said this feature's computer time was about 11 percent lower than the previous
feature's, comfortably inside the allowed range. Nothing new waits for you.

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | `git show --numstat` read `6 0` as required |
| C3 | done | `SU-063` run to approval gate, exit 0, never applied |
| C4 | done | suite green, exit 0, cost script exit 0 |
| Gate 1 | done | all lines `True`, `ALL True` |
| Gate 2 | done | all ten files non-empty |
| Gate 3 | done | exit 0, `23032 passed, 22 skipped, 1 warning`, no bad node ids |
| Gate 4 | done | six checks `pass`, `fail_count` 0; open set length 42 in order |
| Gate 5 | pending | runs after push; reported in the session's final reply only |
| Push | pending | runs after this commit; outcome reported in the session's final reply only |
