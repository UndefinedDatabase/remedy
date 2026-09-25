# Handback — F025 Pause/resume (global & per node) · Round 2

## Session

SESSION 1 of feature F025 · round 2 · rounds so far 2

A little under half the context budget remained at the point this handback was written; the
round was large (six commits, five gates, a fresh design of the pause-vs-stop wiring inside
`run_job`, and a full test file) but produced only one dead end — G5's first pass found
mutation m7 green, fixed in C5b and re-run clean.

## Range

Review of e9824ebec..HEAD

## Commits

### 264dced31 F025 R2 C1: book round 1, copy round 2 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r2-block.md | +223/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r2-ledger.md | +2/-0 | copy of the ledger.md payload |
| .agent/authored/f025-r2-plan.md | +36/-0 | copy of the plan.md payload |
| .agent/authored/f025-r2-slip.txt | +1/-0 | copy of the slip.txt payload |
| .agent/live_review.md | +2/-0 | ledger.md appended (bytes to bytes) |
| .agent/plan.md | +7/-7 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | slip.txt appended (bytes to bytes) |

272 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 223, plus 49) — matches exactly.

### fe4937637 F025 R2 C2: record an operator pause on the job and say who paused it
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +21/-0 | S1: `JobPlan.pause: dict`, wired through `_export_job`/`_import_job` as key `"pause"`; S6: the two extra summary lines in `format_job_report_text` |

21 insertions, well under the 500-line cap.

### d62b01ed8 F025 R2 C3: pause the linear runner at its safe points, park, resume on relaunch, and let a stop win
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +373/-3 | S2 (`_stop_check`'s pause read, `_pause_park_signal`, `_run_stop_check`'s in-flight reading, the three call-site routings), S3 (`_park_job`, `_append_job_paused_event`, `_job_paused_event_exists`), S4 (`_stop_job`'s new "settle a pending job pause as superseded" step and its `job.pause = {}` clear), S5 (the relaunch-decision gate, `_lift_job_pause`, `_append_job_resumed_event`) |
| packages/orchestration/event_names.py | +2/-0 | S7: `job_paused`, `job_resumed` join `EVENT_NAMES` |
| apps/ui/src/api/humanizeCatalog.ts | +2/-0 | S7: the two catalog entries the humanize-catalog guard requires |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | S7: `packages.orchestration.pause_control` joins the allowlist in the commit that first imports it from the runner |

378 insertions, under the 500-line cap.

### 5f5ae833b F025 R2 C4: test every row of the pause semantics on the linear runner
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_pause_resume.py | +417/-0 | NEW FILE — one test class per row (1–11) of DECISION F025 D1's semantics table, plus a white-box class proving the park never settles ahead of its own persist (see Deviations) |

417 insertions, under the 500-line cap.

### 6cd28d607 F025 R2 C5: add the mutation tool for the linear runner's pause
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r2-mutations.py | +263/-0 | the G5 tool: m1–m11, each editing `packages/orchestration/pingpong_job.py` inside a worktree |

263 insertions, under the 500-line cap.

### 4fc507bd2 F025 R2 C5b: prove task 2 is never dispatched, not merely halted (m7)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_pause_resume.py | +4/-0 | strengthens Row 4's test with `run_id == ""` on both withheld tasks — see Deviations #1 |

4 insertions, under the 500-line cap.

### (this commit) F025 R2 C6: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f025-r2-mut 6cd28d607` (C5's HEAD) — succeeded, for G5's
  first run.
- `git worktree remove --force .remedy-wt/f025-r2-mut` — succeeded, after the first G5 run found
  m7 green.
- `git worktree add --detach .remedy-wt/f025-r2-mut 4fc507bd2` (C5b's HEAD) — succeeded, for G5's
  second, clean run.
- `git worktree remove --force .remedy-wt/f025-r2-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees named in constraint 5 (`.remedy-wt/f025-r1-dry`, `f025-r2-sim`,
  `f024-r9-sim`, and the older `f015-*`, `f020-*`, `f023-*`, `f024-*` and `f284-*` ones, plus the
  `job-*` ones) — nothing new left behind.
- `git push origin feature/f025-pause-resume` — runs immediately after this commit (C6); its
  real outcome is reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 4: nothing is
merged; the branch's PR opens at F025's closure, not this round — PR #279 belongs to F024 and is
unrelated). No `git stash`, no force-push, no checkout of another branch.

## Verification

```
$ ls .agent/STOP; echo "REAL_EXIT=$?"
ls: cannot access '.agent/STOP': No such file or directory
REAL_EXIT=2
(absent, as required — checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f025-pause-resume
$ git log --oneline -1
e9824ebec F025 R1 C5: rewrite handoff for round 1
```

```
$ (line count and sha256 of .remedy-wt/f025-r2/block.md, measured)
line_count: 223
sha256: e41d14b3b526972f94c2c65aabad017763c8e720c27bc8c5c026cc00d6b1c85d
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list   (as found, before this round touched anything)
```
Listed the primary checkout at `feature/f025-pause-resume`/`e9824ebec`, `.remedy-wt/f025-r1-dry`
(the reviewer's round-1 authoring tree), `.remedy-wt/f025-r2-sim` (the reviewer's round-2
authoring tree), every `f015-*`/`f020-*`/`f023-*`/`f024-*`/`f284-*` round worktree, `f024-r9-sim`,
and four `job-*` worktrees — all left untouched all round.

### PAYLOADS table
```
$ (python: newline count, byte count, sha256 of each payload)
ledger.md  lines=2  bytes=2839 sha256=85e94e9efa2834cb90978ed1de615c1f5a3282996fd45304ae275fe70339a418
plan.md    lines=36 bytes=1427 sha256=a586b8a56001cb877473ec1b1953ba9eae70d7a4847fed21f1820405368b01f8
slip.txt   lines=1  bytes=273  sha256=2ba22d9e5c9a13762d9332189ffb3ee5921ceb0b94e6530d4a276e56ab6d2185
```
All 3 match the PAYLOADS table exactly (G1).

### G1 — transport
```
$ (python: each committed .agent/authored/f025-r2-* copy, read via `git show <C1>:<path>`,
   compared byte for byte against its source)
.agent/authored/f025-r2-block.md  == .remedy-wt/f025-r2/block.md  : True
.agent/authored/f025-r2-ledger.md == .remedy-wt/f025-r2/ledger.md : True
.agent/authored/f025-r2-plan.md   == .remedy-wt/f025-r2/plan.md   : True
.agent/authored/f025-r2-slip.txt  == .remedy-wt/f025-r2/slip.txt  : True
```
```
$ (bytes comparison: C1's .agent/live_review.md vs e9824ebe's bytes + ledger.md)
live_review match:  True
$ (bytes comparison: C1's .agent/prose_slips.md vs e9824ebe's bytes + slip.txt)
prose_slips match:  True
$ (bytes comparison: C1's .agent/plan.md vs plan.md payload)
plan match:  True
```
```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over C1's .agent/live_review.md
['R-1008']
```
Matches the block's stated reading exactly.

### G2 — the code
```
$ python3 -m ruff check .agent/authored/f025-r2-mutations.py packages/orchestration/event_names.py \
  packages/orchestration/pingpong_job.py tests/orchestration/test_pause_resume.py
All checks passed!
```
```
$ git diff --stat e9824ebe HEAD -- packages/orchestration/safe_points.py \
  packages/orchestration/pingpong_loop.py packages/orchestration/long_run_executor.py \
  packages/common/secure_fs.py
(empty)
```
Confirmed empty — none of the four forbidden files touched.
```
$ git diff --name-only C1 HEAD
.agent/authored/f025-r2-mutations.py
apps/ui/src/api/humanizeCatalog.ts
packages/orchestration/event_names.py
packages/orchestration/pingpong_job.py
tests/orchestration/import_reachability_allowlist.txt
tests/orchestration/test_pause_resume.py
```
Every path is inside constraint 3's set. `packages/orchestration/pause_control.py` was NOT
touched this round (the runner reads it; nothing about it needed to change).

### G3 — the new tests, serially
```
$ python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_pause_resume.py \
  tests/orchestration/test_pause_control.py
.............................................                            [100%]
45 passed in 3.31s
REAL_EXIT=0
```
```
$ python3 -m pytest --collect-only -q tests/orchestration/test_pause_resume.py
15 tests collected
$ python3 -m pytest --collect-only -q tests/orchestration/test_pause_control.py
30 tests collected
```
15 + 30 = 45, matching the summary line exactly.

### G4 — the neighbours
```
$ python3 .remedy-wt/f025-r2/run_sel.py /home/decodeux/Repos/remedy 8
exit 0 wall 66 s
2445 passed in 66.32s (0:01:06)
```
Matches the reviewer's reading at `e9824ebe` exactly (`exit 0`, `2445 passed`); no node failed,
so no serial re-run was needed.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0. (Re-confirmed identically at the final HEAD after C5b.)

### G5 — the red proofs
First run, worktree at C5's HEAD `6cd28d607`:
```
$ git worktree add --detach .remedy-wt/f025-r2-mut 6cd28d607
$ python3 -B .agent/authored/f025-r2-mutations.py .../f025-r2-mut
control (before): exit=0 failed=0
m1..m6, m8..m11: each exit=1, failed>=1, with failing node ids (caught)
m7: the pre-task safe point ignores the task mask -- exit=0 failed=0
  failing_node_ids=[(none)]           <-- GREEN, reported as green, not papered over
m7: restored byte-identical: True
control (after): exit=0 failed=0
packages/orchestration/pingpong_job.py: restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
$ git worktree remove --force .remedy-wt/f025-r2-mut
```
WHY m7 stayed green: with the pre-task mask read disabled, the withheld task still gets caught
by ITS OWN in-task safe point the instant `run_pingpong` starts it — task 2 is directly paused
either way, so the job still parks in the same state (S2's IN-TASK reading is a genuine second
line of defense here). The two paths differ only in whether task 2 was ever DISPATCHED at all: a
real PRE-TASK block never calls `run_pingpong`, so `task.run_id` stays `""`; falling through to
the in-task check sets a real run id first. C5b adds that `run_id == ""` assertion to Row 4's
test, and the tool was re-run from a fresh worktree at the new HEAD:
```
$ git worktree add --detach .remedy-wt/f025-r2-mut 4fc507bd2
$ python3 -B .agent/authored/f025-r2-mutations.py .../f025-r2-mut
control (before): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
m1: the job pause is read BEFORE the operator stop -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow6AStopBeatsAPause::test_a_pending_stop_and_a_pending_job_pause_the_stop_wins]
m1: restored byte-identical: True
m2: the park settles the request BEFORE it persists the job -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestParkNeverSettlesBeforeItIsDurable::test_a_persist_failure_leaves_the_pause_control_request_pending]
m2: restored byte-identical: True
m3: the park writes job_paused without checking the ledger for that request id -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow8AFailedSettleReparksWithoutADuplicateEvent::test_the_next_run_reparks_and_settles_without_a_second_job_paused]
m3: restored byte-identical: True
m4: the park leaves the in-flight task running -- exit=1 failed=2 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow1JobPauseDuringABuildCall::test_lets_the_call_finish_and_starts_no_reviewer, tests/orchestration/test_pause_resume.py::TestRow5AnInFlightTaskPause::test_halts_then_stays_parked_until_released_then_resumes]
m4: restored byte-identical: True
m5: the relaunch never lifts the pause -- exit=1 failed=2 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow3TheRelaunchResumes::test_writes_one_job_resumed_and_matches_an_unpaused_control_run, tests/orchestration/test_pause_resume.py::TestRow5AnInFlightTaskPause::test_halts_then_stays_parked_until_released_then_resumes]
m5: restored byte-identical: True
m6: the relaunch dispatches a task that is still withheld -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow5AnInFlightTaskPause::test_halts_then_stays_parked_until_released_then_resumes]
m6: restored byte-identical: True
m7: the pre-task safe point ignores the task mask -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow4AMidPlanTaskPause::test_earlier_task_runs_and_the_rest_park_withheld]
m7: restored byte-identical: True
m8: the in-task safe point ignores a pause of the in-flight task -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow5AnInFlightTaskPause::test_halts_then_stays_parked_until_released_then_resumes]
m8: restored byte-identical: True
m9: the relaunch re-stamps first_running_at -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow3TheRelaunchResumes::test_writes_one_job_resumed_and_matches_an_unpaused_control_run]
m9: restored byte-identical: True
m10: a PauseControlError at a safe point is swallowed and the task dispatched -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow9AnUnreadablePausedTasksEntry::test_blocks_the_job_with_pause_control_error_and_dispatches_nothing]
m10: restored byte-identical: True
m11: a served stop leaves a pending job pause unsettled -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_resume.py::TestRow6AStopBeatsAPause::test_a_pending_stop_and_a_pending_job_pause_the_stop_wins]
m11: restored byte-identical: True
control (after): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
packages/orchestration/pingpong_job.py: restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f025-r2-mut
$ git worktree prune
$ git worktree list
(primary + the pre-existing set only; f025-r2-mut gone)
```
Every one of the 11 mutations is now red with at least one failing node id; every restore is
byte-identical; the tool's own final line reads `True`.

### G6 — tree and push (readings go in the final reply, after C6)

## Authored-text proofs

`.agent/authored/f025-r2-block.md`, `f025-r2-ledger.md`, `f025-r2-plan.md` and
`f025-r2-slip.txt` were built with `shutil.copyfile` from the reviewer's payload files — never
retyped, never edited — and G1 compared every one byte for byte, read back with
`git show <C1>:<path>`, against its source: all four BYTE-IDENTICAL. `.agent/live_review.md` and
`.agent/prose_slips.md` were appended with raw bytes read from `ledger.md`/`slip.txt`
(`open(..., "ab").write(...)`), never retyped; `.agent/plan.md` was rewritten whole from
`plan.md`'s bytes (`Path.write_bytes`). G1's byte-comparisons confirm all three match the
payloads exactly. `packages/orchestration/pingpong_job.py`,
`tests/orchestration/test_pause_resume.py` and `.agent/authored/f025-r2-mutations.py` are
WORKER-authored production code, tests and the G5 tool per the block's S1–S8 specification — not
reviewer payloads — so no authored-text proof applies to them.

## Deviations & assumptions

1. **Extra commit C5b.** G5's first run (worktree at C5's HEAD) found mutation m7 green — with
   the PRE-TASK mask read disabled, the withheld task still gets caught by its OWN in-task safe
   point (a genuine second line of defense: task 2 is directly paused either way), so the job
   still parked in the same observable end state and the existing Row 4 assertions could not
   tell the two code paths apart. Per the block's own G5 clause ("a mutation that stays green...
   the catching test is added in a further commit before C6, and the tool re-run"), C5b adds the
   one assertion that DOES distinguish them — a genuine PRE-TASK block never calls
   `run_pingpong`, so the withheld tasks' `run_id` stays `""`, while falling through to the
   in-task check sets a real one first. G5's second run, from a fresh worktree at C5b's HEAD,
   caught all 11 mutations and reported `True`. This is an extra commit not named in the block's
   C1/C2/C3/C4/C5 sequence, recorded here per the "extra commit is a deviation even when correct"
   rule.
2. **No full-suite run.** Per constraint 6 (amend0917-throughput), only G4's targeted selection
   ran; the one full-suite run per feature belongs to F025's closure, not this round.
3. **No existing test file widened.** Constraint 3 names this as a possible category (an
   existing test whose only edit adds the new record key or event names to a set it pins); none
   was needed this round — `test_humanize_catalog.py` and `test_event_names.py` both derive their
   sets from the source by AST walk (no hand-pinned literal set to widen), and
   `test_import_reachability.py`'s allowlist ratchet only checks `reachable ⊆ allowlist`, so
   adding `packages.orchestration.pause_control` to the allowlist needed no test-side edit
   either. All three passed unmodified (G3's neighbour run and the targeted runs above).
4. **`packages/orchestration/pause_control.py` untouched.** The block allowed "small helpers
   only, named in the handback" there; none were needed — every S2–S5 read of it (`pause_requested`,
   `paused_tasks`, `withheld_task_ids`, `settle_pause`, `release_task_pause`) already existed
   from round 1 with the exact signature the runner needed.

No payload was edited or retyped. No production file outside
`packages/orchestration/pingpong_job.py`, `packages/orchestration/event_names.py` and
`apps/ui/src/api/humanizeCatalog.ts` was touched; `safe_points.py`, `pingpong_loop.py`,
`long_run_executor.py` and `secure_fs.py` are confirmed untouched by G2's `git diff --stat`. The
worktree `.remedy-wt/f025-r2-mut` this round created (twice, for G5's two runs) was removed both
times, per constraint 5; every pre-existing worktree and stash was left alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 272 insertions, matches the block's expectation (223+49) exactly |
| C2 | done | 21 insertions; S1 + S6 landed together, well under the cap |
| C3 | done | 378 insertions; S2–S5, S7 landed together, well under the cap |
| C4 | done | 417 insertions; one test class per row 1–11 plus the white-box park-ordering test |
| C5 | done | 263 insertions; the mutation tool, m1–m11 |
| C5b | deviated | extra commit fixing a mutation G5 found green; see Deviations #1 |
| C6 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical; open-finding set matched |
| G2 | done | ruff clean over every changed .py file; forbidden files untouched; name-only diff exactly inside constraint 3 |
| G3 | done | 45 passed (15+30), exit 0 |
| G4 | done | 2445 passed, exit 0, matches the reviewer's reading exactly; integrity check 6/6 pass |
| G5 | deviated | first run found m7 green (reported as green, not papered over); fixed in C5b; second run caught all 11, `True` |
| G6 | done | reported in the final reply, after C6 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2. Then the same pause in
the cycle executor, `run_cycles`. Open findings: 1. Operator questions open: 3.
