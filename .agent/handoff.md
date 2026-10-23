# Handback — F315 "The loop runs through the adapter," round 4

## Session

SESSION 1 of feature F315 · round 4 · rounds so far 4. Context self-assessment: this session
continued directly from round 3's handback, booked round 3's verdict, landed the checklist's
consolidation paragraph, ran the closure's self-use item to its approval gate exactly once, and
ran the feature's one full suite exactly once, everything green, carrying forward only the
evidence bundle, the review package and the closing round.

**Fortschritt:** ~90 % (T001 to T003 and the docs landed; the consolidation pass, the self-use
run and the one full suite done · the evidence, the package and the closing round remain) —
Schätzung.

## Range

Review of `a1adcfa5b`..`a213fc32f`.

## Commits

### 6fb29cd85 F315 R4 C1: book round 3, the plan, the block and the self-use script
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-r4.md` | +156/-0 | NEW FILE; byte copy of this round's block, `block.md` |
| `.agent/authored/f315-r4-selfuse.py` | +133/-0 | NEW FILE; byte copy of the reviewer's self-use runner script for this round |
| `.agent/live_review.md` | +2/-0 | books round 3's VERDICT PASS (F315 R3, over `30cd588dc`..`a1adcfa5b`) |
| `.agent/plan.md` | +6/-6 | rewritten for round 4's current step (the closure's integration-gate round) and the next steps (repair-or-evidence, then the closing round) |

All four paths are byte copies of the reviewer's prepared `c1-*` files; gate 1's `verify.py`
confirms each equality (see Verification).

### c501fc4bd F315 R4 C2: the checklist's consolidation pass for F315
| Path | +/- | Reason |
|---|---|---|
| `docs/agents/planner_reviewer_prompt.md` | +7/-0 | F315's consolidation paragraph: nothing joins the checklist, no two items merge, the list stays at 34 items |

Byte copy of the reviewer's prepared `c2-*` file; gate 1's `verify.py` confirms the equality.

### 9e91d122a F315 R4 C3: the closure's self-use item run to its approval gate, never applied
| Path | +/- | Reason |
|---|---|---|
| `scripts/self_use_queue.json` | +8/-0 | the generator's one appended entry, `SU-079`, "Narrow the excused handler at apps/cli/grouped.py:619," `consumed_by` empty |
| 10 files under `.agent/selfuse_f315/` | NEW FILES | the self-use run's record: the job file, entry/job metadata, execution config, result state, timing, changed paths (`NONE`), full transcript, post-run staleness, the job's own diff and the run's defects, each read verbatim into the next handback section |

Written by running the reviewer-authored, never-edited script once via `launch.py`/`wait.py`
(exit 0, wall 270.6s); `git status --porcelain` showed only these paths changed, exactly as the
block requires.

### a213fc32f F315 R4 C4: the closure's one full suite and its CPU cost
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f315-closure-suite.txt` | +27/-0 | NEW FILE; the suite's one run this round (command, exit code, wall time, summary line, bad node ids, leftover processes, reflog before/after) and the CPU-cost script's full output |

## Item status

| Item | Status | Reason |
|---|---|---|
| C1 | done | `6fb29cd85`, four paths, byte-equal to prepared files |
| C2 | done | `c501fc4bd`, one path, byte-equal to prepared file, numstat `7 0` |
| C3 | done | `9e91d122a`, self-use script run once (exit 0), one queue entry appended, ten new files under `.agent/selfuse_f315/`, job ended `blocked` at its approval gate, never applied |
| C4 | done | `a213fc32f`, one new transcript file; suite `23762 passed, 11 skipped` exit 0; cost script exit 0, within budget |
| Gate 1 | done | `git status --porcelain` empty; `verify.py` every line `True`, `C5` read `absent` (as expected before this commit), `ALL True` |
| Gate 2 | done | all ten `.agent/selfuse_f315/` files non-empty (sizes in Verification) |
| Gate 3 | done | suite exit 0, summary line verbatim, bad node ids `NONE` |
| Gate 4 | done | `integrity check --json` `fail_count` 0; open finding ids the required eleven |
| C5 | done | this file |
| Push | done | see External actions |

## External actions

- `git push origin feature/f315-loop-through-adapter` — run after this handback's own commit,
  carrying `6fb29cd85`, `c501fc4bd`, `9e91d122a`, `a213fc32f` and the handback commit itself; see
  the reply for the push's own result.
- No pull request opened (the block orders none; the Open PR Gate found `[]` before this round
  started).
- No worktree created or removed by this session. The self-use script's own run read the job's
  result directly from its still-present workspace (`staleness_after.txt`: "Read from: the job
  workspace"), so it took no `git worktree add`/`remove` branch of its own logic this time.
- One scratch directory was used, `.remedy-wt/f315-r4-worker/`, holding only python helper
  scripts (digest checks, byte copies, gate readings) and the two command logs/exit files
  `launch.py` wrote; `.remedy-wt/f315-r4/` (the reviewer's prepared tree) was only read, never
  written.

## Verification

Gate order per the block: run once each, after C4 and before C5.

1. `git status --porcelain` → empty.
   `python3 .remedy-wt/f315-r4/prep/verify.py .` → exit 0. Every line `True`: each commit's
   single-parent check, its new-subject check, its insertions-under-500 check (297, 7, 110, 27),
   the branch check, each commit's exact-path-set check and every per-path byte-equality check
   against the prepared `c1-*`/`c2-*` files, the C3 queue-append check (`SU-079`) and its
   no-machine-path check on every `.agent/selfuse_f315/` file, the C4 path-alone and
   no-machine-path checks, `C5` → `absent` (as the block states, before this commit exists), "the
   saved block equals block.md" `True`, final line `ALL True`.
2. The ten files under `.agent/selfuse_f315/`, each non-empty: `SU-079.md` 962 bytes,
   `entry_and_job_file.txt` 345 bytes, `execution_config.txt` 1367 bytes, `result_state.txt`
   937 bytes, `timing.txt` 105 bytes, `changed_paths.txt` 5 bytes, `full_transcript.txt`
   1639 bytes, `staleness_after.txt` 222 bytes, `job_diff.txt` 56 bytes, `run_defects.txt`
   282 bytes.
3. The suite of C4: exit code `0`; summary line `23762 passed, 11 skipped, 1 warning in 341.00s
   (0:05:41)`; bad node ids (failed + errors) `NONE`; no `process(es) behind` line anywhere in the
   log.
4. `python3 -m apps.cli.main integrity check --json` → exit 0, `{"check_count": 6, "checks":
   [{"message": "handlers=201", "name": "handler_import", "status": "pass"}, {"message": "last
   Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0,
   context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message":
   "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no
   reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status":
   "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status":
   "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}`.
   `python3 -c "import scripts.rotate_live_review as r; print(r.open_finding_ids(open('.agent/live_review.md').read()))"`
   → exit 0, printed `['R-1246', 'R-1281', 'R-1326', 'R-1351', 'R-1353', 'R-1418', 'R-1421',
   'R-1425', 'R-1426', 'R-1427', 'R-1428']`, matching the block's required eleven ids exactly.

## Self-use run

Entry `SU-079`, "Narrow the excused handler at apps/cli/grouped.py:619" (generated, tier 4).
Job ID `511bda34db8c4be4`. Builder: `claude-cli`, model `claude-sonnet-4-6`. Reviewer: `claude-cli`,
model `claude-sonnet-4-6` (both from `execution_config.txt`). Job state `blocked`, stop reason
empty, stop source empty. Task `T001`: status `blocked`, reviewer verdict `blocked`, final status
`staged_blocked`, repair rounds used `1` (from `result_state.txt`). Wall seconds `266.9` (from
`timing.txt`). Paths in `changed_paths.txt`: `NONE`.

`job_diff.txt` VERBATIM:
```
$ git diff HEAD...remedy/job-511bda34db8c4be4  (exit 0)

```

`run_defects.txt` VERBATIM:
```
From describe_self_use_run_defects():

1. job 511bda34db8c4be4 (blocked): task_T001_gate_failed: final_status=staged_blocked; no_file_changed; reviewer_verdict=blocked
2. T001 (blocked): completion_gate_failed: final_status=staged_blocked; no_file_changed; reviewer_verdict=blocked
```

No finding is registered by this worker for the above; the block reserves that for the next
round's reviewer.

## Closure suite

`.agent/authored/f315-closure-suite.txt`, quoted whole and verbatim:
```
command: python3 -m pytest -n auto -q
real exit code: 0
wall time: 341.8s (the launcher's reading); pytest's own reported wall time: 341.00s (0:05:41)
summary line: 23762 passed, 11 skipped, 1 warning in 341.00s (0:05:41)
bad node ids (failed + errors): NONE
leftover processes: NONE
tree it ran on: 9e91d122a (F315 R4 C3: the closure's self-use item run to its approval gate, never applied)
tree note: C1 to C3 changed only .agent/ files, the checklist page and the self-use queue
reflog before: 9e91d122a HEAD@{2026-10-23 22:23:45 +0200}: commit: F315 R4 C3: the closure's self-use item run to its approval gate, never applied
reflog after: 9e91d122a HEAD@{2026-10-23 22:23:45 +0200}: commit: F315 R4 C3: the closure's self-use item run to its approval gate, never applied
reflog unchanged during the run: yes
cost command: python3 scripts/closure_suite_cost.py --feature F315 --record ~/.remedy-loop/test_load.jsonl
cost exit code: 0
Test load: 1255.17 CPU seconds, 341.03 wall seconds, 23773 tests collected, exit status 0, recorded 2026-10-23T20:29:34Z
This closure's suite used 1255.17 CPU seconds, 3.5 percent less than F151's 1300.34, within the 10 percent limit.
The limit is the larger of 10 percent and the largest spread between full-suite runs of the record that collected the same tests, 0 percent.
The test modules whose CPU time rose most since F151's closure run:
  +3.75 s  tests/orchestration/test_self_use_generator.py (3.81 -> 7.56)
  +3.69 s  tests/test_grouped_cli.py (26.51 -> 30.20)
  +1.63 s  tests/orchestration/test_stream_export_e2e.py (3.14 -> 4.77)
  +1.24 s  tests/cli/test_plan_approval.py (6.99 -> 8.23)
  +0.76 s  tests/orchestration/test_job_task_runner.py (18.16 -> 18.92)
  +0.74 s  tests/orchestration/test_job_worktree_integrity.py (6.90 -> 7.64)
  +0.71 s  tests/orchestration/test_job_retry.py (2.36 -> 3.07)
  +0.71 s  tests/orchestration/test_worker_adapter_slot.py (0.00 -> 0.71)
  +0.70 s  tests/orchestration/test_dirty_baseline_secrets.py (2.61 -> 3.31)
  +0.65 s  tests/test_timeline.py (5.12 -> 5.77)
```

## Authored-text proofs

- `.agent/authored/f315-r4.md` (this round's committed copy of the block) against
  `.remedy-wt/f315-r4/prep/block.md`: both 156 lines; sha256
  `a93a13036cd24441303388674185779615af6de8e64e9526b86289787d5440b9` on both. Byte-identical.
- `.agent/authored/f315-r4-selfuse.py` against `.remedy-wt/f315-r4/prep/c1-.agent__authored__f315-r4-selfuse.py`:
  sha256 `7c892caab897fb9aef8768c99cb29b0180aac9fb2665d4bb9b30ff6bb1002514` on both. Byte-identical,
  confirmed by a direct Python byte comparison before commit.
- `.agent/live_review.md` against `.remedy-wt/f315-r4/prep/c1-.agent__live_review.md`: sha256
  `3e6971a5b62b8f77d1d7fa8c8c28836842e3e5d50295e204aac65451bb8149a0` on both. Byte-identical.
- `.agent/plan.md` against `.remedy-wt/f315-r4/prep/c1-.agent__plan.md`: sha256
  `6491877d788b9b682df32fd5a004182aad7f98ae70876d67ed87acbbe610f86a` on both. Byte-identical.
- `docs/agents/planner_reviewer_prompt.md` against
  `.remedy-wt/f315-r4/prep/c2-docs__agents__planner_reviewer_prompt.md`: sha256
  `fa49afab49cbdac89e519e696901336d8c868f512d74bcfad071aa3e3f70d989` on both. Byte-identical.

Before using any prepared file, `.remedy-wt/f315-r4/prep/digests.txt` was checked against its own
stated sha256 (`2ff9df1754444737924a43c18f53ed601f7b9fc0889b7eb4dfd065ade90e3ced`, matched), then
every one of its nine listed entries was recomputed and matched, before any prepared file was
copied, run or read for C1 through C4.

## Deviations & assumptions

- No deviation from the block's ordered commit sequence (C1, C2, C3, C4, gates 1–4, C5, push);
  nothing was added, dropped or reordered. Every `c1-*`/`c2-*` prepared byte was copied verbatim
  and proved equal by a direct comparison before being added to the index.
- `LAST_REVIEWED_SHA` in the Range line above is taken as `a1adcfa5b`, round 3's handback commit,
  the base this round's block names.
- The self-use job's terminal state (`blocked`, at its approval gate, no file changed) is read as
  the ordinary "run it to its approval gate, never apply it" outcome the block describes, not as
  a deviation; the script itself exited 0.

## Next

1. Phase 1 rule 1: if `.agent/STOP` exists, the next session finishes whatever commit is in hand,
   writes the handoff, pushes, and stops, before anything else.
2. Phase 1 rule 2: the next session runs the Open PR Gate before opening any new branch; no pull
   request is open for this branch yet.
3. The reviewer reviews round 4, books its verdict and registers every self-use run defect in the
   next round's first commit.
4. The suite was green, so next: the evidence bundle and the review package.
5. Then the closing round: the Built State, the rotation, the STATUS line, the README and the
   pull request.

Operator questions open: 0. Open findings (gate 4): 11.

## For the operator, in plain sentences

The paid run this round was asked to narrow one overly broad error handler in a single file and
tighten its matching test to match, and it ended blocked at its own review step before anything
was written, so nothing changed. The feature's whole test collection ran once on the code that
will ship, and all of it passed except eleven tests that stay skipped on purpose, in a little
under six minutes. The cost reading said this run used a few percent less computer time than the
previous feature's closure run, comfortably inside the normal range. The jobs Remedy runs now
take every command they send to the command-line model from that model's adapter, the piece that
will let other vendors' models plug in the same way, and the self-use run this round just went
through it.
