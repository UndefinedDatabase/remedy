# Handback — F025 Pause/resume (global & per node) · Round 1

## Session

SESSION 1 of feature F025 · round 1 · rounds so far 1

A comfortable majority of the context budget remained at the point this handback was written;
the round was long (nine commits, five gates plus a targeted-suite run over 774 collected
tests) but produced only one dead end — G5's first pass found mutation m8 green, fixed in C4c
and re-run clean.

## Range

Review of 49624d5c8..HEAD

## Commits

### ebf906034 F025 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r1-block.md | +300/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r1-context.md | +35/-0 | copy of the context.md payload |
| .agent/authored/f025-r1-plan.md | +36/-0 | copy of the plan.md payload |

371 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 300, plus 71) — matches exactly.

### 1209db260 F025 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r1-claim.diff | +171/-0 | copy of the claim.diff payload |

171 insertions — matches the block's expected 171 exactly.

### c523a8b98 F025 R1 C2: claim F025, re-head the live review record, book F024 R9, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +15/-17 | rewritten whole to the context.md payload |
| .agent/decisions.md | +82/-0 | DECISION F025 D1 appended (claim.diff) |
| .agent/live_review.md | +29/-24 | re-headed for F025; F024 R9's gate entry and R-1048's `Done:` paragraph appended (claim.diff) |
| .agent/plan.md | +23/-20 | rewritten whole to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F025's line `[ ]` → `[~]` (claim.diff) |

15/17, 82/0, 29/24, 23/20, 1/1 by `git show --numstat` — matches the block's expected table
exactly, cell by cell. `git apply --check` on claim.diff exited 0 before the real `git apply`,
which also exited 0.

### 474011b9a F025 R1 C3a: add the pause control records and the job-scope pause files (S2, S3)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pause_control.py | +291/-0 | NEW FILE: module docstring naming DECISION F025 D1 (S1); `PauseControlError`, `PauseSignal`, `TaskPause` (S2); `_bounded`, `_open_named_dir`, `_parse_pause_signal` helpers; `request_pause`, `pause_requested`, `settle_pause`, `withdraw_pause` (S3) |

291 insertions.

### 5e03502af F025 R1 C3b: add the task-scope pause files and the mask arithmetic (S4, S5)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pause_control.py | +253/-0 | `_validate_task_id`, `_task_pause_filename`, `_parse_task_pause` helpers; `request_task_pause`, `release_task_pause`, `paused_tasks` (S4); `WithheldTasks`, `withheld_task_ids` (S5) |

253 insertions. The whole module is 544 lines (`wc -l`, matching 291+253); landing it as one
commit would have exceeded S6's 500-insertion cap, so it landed as C3a (S2, S3) and C3b (S4,
S5), exactly as S6 names.

### b32f74053 F025 R1 C4a: test the pause control files and the mask arithmetic
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_pause_control.py | +319/-0 | NEW FILE: `TestJobScopePause`, `TestReasonAndSourceAreBounded`, `TestTaskScopePause`, `TestTheMask` — 30 tests over a `tmp_path` control root, covering every row the block lists (idempotence and convergence both scopes, the cheap check's None, archive-before-remove with a forced archive failure, a settle that spares a newer pending request, the unknown-outcome refusal, `consumed_count` staying 0, release-of-unpaused writing nothing, `paused_tasks` ordering with a forced tie, a corrupt entry raising, a `/`/`..` id round-tripping, empty/over-long id refusal, a symlinked `paused_tasks/` refusal, reason truncation, the linear rows parametrized, and the graph rows built with `test_dag_schedule.flight_task`, imported, asserting `downstream` equals `dag_schedule.blocked_downstream`) |

319 insertions.

### 9c211876a F025 R1 C4b: add the mutation tool proving the pause control tests bite
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r1-mutations.py | +260/-0 | NEW FILE: the G5 mutation tool — m1 through m15, one FROM/TO pair each, plus the worktree-driving harness (purge `__pycache__`, run pytest, restore, report) |

260 insertions. Bundling the test file and the mutation tool into one C4 commit, as the block
names it, would have totaled 579 insertions (319+260) — over constraint 2's 500-insertion cap.
Split into C4a and C4b, mirroring the C3a/C3b mechanism S6 already authorizes for the module;
see Deviations.

### dbc7cafc3 F025 R1 C4c: fix the unpaused-task release test to reach the no-entry branch (m8)
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_pause_control.py | +5/-0 | G5's first run (at C4b's HEAD) found mutation m8 green: `test_releasing_an_unpaused_task_returns_none_and_writes_nothing` released a task from a job whose `paused_tasks/` directory never existed, so `release_task_pause` returned via the earlier `tasks_fd is None` branch and never reached the "no entry for this task" code m8 mutates. Pausing a *different* task first makes `paused_tasks/` exist, so the release of the still-unpaused id now reaches the right branch and the archive-fabrication mutation goes red |

5 insertions, 0 deletions — a pure addition, per G5's own instruction ("you then add the test
that catches it in C4 before C5 and re-run the tool"); see Deviations.

(C5, this handback, is its own commit and is not tabled here per the handback template's
self-reference exception.)

## External actions

- `git checkout -b feature/f025-pause-resume` — succeeded, from `main` at `49624d5c8`.
- `git worktree add --detach .remedy-wt/f025-r1-mut 9c211876a` (C4b's HEAD) — succeeded, for
  G5's first run.
- `git worktree remove --force .remedy-wt/f025-r1-mut` — succeeded, after the first G5 run found
  m8 green.
- `git worktree add --detach .remedy-wt/f025-r1-mut dbc7cafc3` (C4c's HEAD) — succeeded, for
  G5's second, clean run.
- `git worktree remove --force .remedy-wt/f025-r1-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees named in constraint 6 (`.remedy-wt/f025-r1-dry`, `f024-r9-sim`, and the
  older `f015-*`, `f020-*`, `f023-*`, `f024-*` and `f284-*` ones, plus the `job-*` ones) —
  nothing new left behind.
- `git push -u origin feature/f025-pause-resume` — runs immediately after this commit (C5);
  its real outcome is reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 5: nothing is
merged; the branch opens a pull request at F025's closure, not this round). No `git stash`, no
force-push, no checkout of `main` after the branch was cut.

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
main
$ git log --oneline -1
49624d5c8 Merge pull request #279 from UndefinedDatabase/feature/f024-phase-timeline-scrubber
```

```
$ (line count and sha256 of .remedy-wt/f025-r1/block.md, measured)
line_count: 300
sha256: f77cf2e3fa0397da20559766b02079a5ee5fa47b7db93aaccb18b9c867d80e72
```
Matches both readings the delegation message gave exactly — R-0954.

```
$ git checkout -b feature/f025-pause-resume
Switched to a new branch 'feature/f025-pause-resume'
```

```
$ git worktree list   (as found, before this round touched anything)
```
Listed the primary checkout at `main`/`49624d5c8`, `.remedy-wt/f025-r1-dry` (the reviewer's
authoring tree, `49624d5c8`, read-only), every `f015-*`/`f020-*`/`f023-*`/`f024-*`/`f284-*`
round worktree, `f024-r9-sim`, and four `job-*` worktrees — all left untouched all round.

### PAYLOADS table
```
claim.diff   lines=171 bytes=20176 sha256=506a8c85a23624a68ec2a9aba95866a0f782b605169f9ca2230179a2e3c83053
context.md   lines=35  bytes=1544  sha256=9f6e71a9ae0000d7ae04cabcf5f4bfbd31ef41b7d0262fc0a5a1065c70a6f414
plan.md      lines=36  bytes=1410  sha256=d4fedcab75d5384f8d043bee85fc135660671ffbae7b500bb61a465233c2b11e
```
All 3 match the PAYLOADS table exactly (G1).

### G1 — transport
```
$ (python: each committed .agent/authored/f025-r1-* copy, read via `git show <commit>:<path>`,
   compared byte for byte against its source)
.agent/authored/f025-r1-block.md   == .remedy-wt/f025-r1/block.md              : True
.agent/authored/f025-r1-plan.md    == .remedy-wt/f025-r1-payloads/plan.md      : True
.agent/authored/f025-r1-context.md == .remedy-wt/f025-r1-payloads/context.md   : True
.agent/authored/f025-r1-claim.diff == .remedy-wt/f025-r1-payloads/claim.diff   : True
```
One reading per copy, all byte-identical (G1).

### G2 — the claim
```
$ (bytes/sha256 of each row, read via `git show c523a8b98:<path>`)
.agent/live_review.md    bytes=298345  sha256=4657ecfc6446ccf3891e0850edfc1b11fe0bbfb794bc878d37b1b1cb1cd96110
docs/roadmap/STATUS.md   bytes=52107   sha256=b96ba6d2412d48aada739351d9e4a6a8db46f4c103e90320616b1793f24a7bd8
.agent/decisions.md      bytes=2100860 sha256=24b15c68325ccf9f333faf8f942556f70814c0ba056265e8f48beea6b025c7ab
.agent/plan.md           bytes=1410    sha256=d4fedcab75d5384f8d043bee85fc135660671ffbae7b500bb61a465233c2b11e
.agent/context.md        bytes=1544    sha256=9f6e71a9ae0000d7ae04cabcf5f4bfbd31ef41b7d0262fc0a5a1065c70a6f414
```
All 5 match the reviewer's reading exactly.
```
$ open_finding_ids(text) from scripts/rotate_live_review.py
at 49624d5c: ['R-1008', 'R-1048']
at C2:       ['R-1008']
```
Matches the block's stated readings exactly. At C2: exactly one `## Findings` line, exactly one
`## Steps` line; the last line begins `Done: R-1048 — ` (confirmed True). F025's STATUS line at
C2 reads back in full as `- [~] F025 — Pause/resume (global & per node)` (confirmed True).
`git diff --name-only 1209db260 c523a8b98` names exactly the 5 paths of the table above.

### G3 — the module
```
$ python3 -m ruff check packages/orchestration/pause_control.py tests/orchestration/test_pause_control.py
All checks passed!
```
```
$ git diff --name-only c523a8b98 HEAD
.agent/authored/f025-r1-mutations.py
packages/orchestration/pause_control.py
tests/orchestration/test_pause_control.py
```
Exactly the module, the test file and the mutation tool — matches.
```
$ (python ast: every Import/ImportFrom node in pause_control.py)
imported modules: ['__future__', 'collections.abc', 'dataclasses', 'hashlib', 'json', 'os',
  'packages.common', 'packages.orchestration', 'packages.orchestration.failure_postmortem',
  'pathlib', 're', 'typing']
banned hit (subprocess/threading/signal/time): set()
```
None of the four banned names appear.
```
$ git diff --stat 49624d5c HEAD -- packages/orchestration/safe_points.py packages/common/secure_fs.py
(empty)
```
Confirmed empty — neither file touched.

### G4 — the tests, serially, at final HEAD (dbc7cafc3)
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_pause_control.py \
  tests/orchestration/test_safe_points.py tests/orchestration/test_dag_schedule.py \
  tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py \
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py \
  tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py \
  tests/orchestration/test_import_reachability.py tests/test_agent_tooling.py \
  tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
760 passed, 1 skipped in 76.28s
REAL_EXIT=0
```
Only ONE `SKIPPED` line, the D12 quarantine (as the block says must stay skipped); the
typescript node in `test_dashboard_contract.py` and the vitest node in `test_test_runner.py`
both PASSED, not skipped. Reconciling against the reviewer's `686 passed, 3 skipped`: 686 + 2
(the two toolchain nodes converting from skip to pass in the primary checkout) + 30 (this
round's new test file, confirmed by `--collect-only -q`) + 42 (`test_golden_path.py`, which the
reviewer's selection excluded, confirmed by `--collect-only -q`) = 760 passed exactly; skips
3 − 2 = 1 exactly. No unaccounted difference.
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
All six checks `pass`, `fail_count` 0.

### G5 — the red proofs
First run, worktree at C4b's HEAD `9c211876a`:
```
$ git worktree add --detach .remedy-wt/f025-r1-mut 9c211876a
$ python3 -B .agent/authored/f025-r1-mutations.py .../f025-r1-mut
control (before): exit=0 failed=0
m1..m7, m9..m15: each exit=1, failed>=1, with failing node ids (caught)
m8: release_task_pause of an unpaused task writes an archive entry -- exit=0 failed=0
  failing_node_ids=[(none)]           <-- GREEN, reported as green, not papered over
m8: restored byte-identical: True
control (after): exit=0 failed=0
packages/orchestration/pause_control.py: restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: False
$ git worktree remove --force .remedy-wt/f025-r1-mut
```
Per the block's instruction, C4c then added the test that catches m8 (see Commits), and the
tool was re-run from a fresh worktree at the new HEAD:
```
$ git worktree add --detach .remedy-wt/f025-r1-mut dbc7cafc3
$ python3 -B .agent/authored/f025-r1-mutations.py .../f025-r1-mut
control (before): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
m1: request_pause overwrites a pending request with a new id -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestJobScopePause::test_idempotent_second_request_returns_the_first_signal]
m1: restored byte-identical: True
m2: pause_requested always returns None -- exit=1 failed=4 failing_node_ids=[tests/orchestration/test_pause_control.py::TestJobScopePause::test_a_failed_archive_publication_leaves_the_request_pending, tests/orchestration/test_pause_control.py::TestJobScopePause::test_settling_an_old_request_leaves_a_newer_pending_request_in_place, tests/orchestration/test_pause_control.py::TestJobScopePause::test_an_unknown_outcome_is_refused_and_nothing_changes, tests/orchestration/test_pause_control.py::TestJobScopePause::test_withdraw_settles_pending_as_withdrawn_else_none]
m2: restored byte-identical: True
m3: settle_pause removes the pending file BEFORE publishing the archive -- exit=1 failed=2 failing_node_ids=[tests/orchestration/test_pause_control.py::TestJobScopePause::test_a_failed_archive_publication_leaves_the_request_pending, tests/orchestration/test_pause_control.py::TestJobScopePause::test_settling_an_old_request_leaves_a_newer_pending_request_in_place]
m3: restored byte-identical: True
m4: settle_pause removes a pending file whose request id differs -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestJobScopePause::test_settling_an_old_request_leaves_a_newer_pending_request_in_place]
m4: restored byte-identical: True
m5: the pause archive is written under the stop's archive/ directory -- exit=1 failed=5 failing_node_ids=[tests/orchestration/test_pause_control.py::TestJobScopePause::test_settle_archives_before_removing_the_pending_file, tests/orchestration/test_pause_control.py::TestJobScopePause::test_a_failed_archive_publication_leaves_the_request_pending, tests/orchestration/test_pause_control.py::TestJobScopePause::test_a_second_settle_of_an_already_archived_request_writes_nothing_new, tests/orchestration/test_pause_control.py::TestJobScopePause::test_withdraw_settles_pending_as_withdrawn_else_none, tests/orchestration/test_pause_control.py::TestTaskScopePause::test_release_archives_under_pause_archive_tasks_and_removes_the_entry]
m5: restored byte-identical: True
m6: settle_pause accepts an unknown outcome -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestJobScopePause::test_an_unknown_outcome_is_refused_and_nothing_changes]
m6: restored byte-identical: True
m7: request_task_pause replaces an existing entry with a new request id -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTaskScopePause::test_idempotent_pause_of_an_already_paused_task_returns_the_existing_entry]
m7: restored byte-identical: True
m8: release_task_pause of an unpaused task writes an archive entry -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTaskScopePause::test_releasing_an_unpaused_task_returns_none_and_writes_nothing]
m8: restored byte-identical: True
m9: paused_tasks skips an entry it cannot parse -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTaskScopePause::test_a_corrupt_entry_raises_rather_than_being_dropped]
m9: restored byte-identical: True
m10: the task file is named by the raw task id instead of its digest -- exit=1 failed=2 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTaskScopePause::test_a_path_shaped_task_id_round_trips_and_names_no_path_shaped_file, tests/orchestration/test_pause_control.py::TestTaskScopePause::test_the_task_file_is_named_by_digest_not_by_the_raw_id]
m10: restored byte-identical: True
m11: the linear mask withholds only the paused task, not the tasks after it -- exit=1 failed=3 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTheMask::test_linear_paused_position_decides_what_is_spared[A-withheld0-downstream0], tests/orchestration/test_pause_control.py::TestTheMask::test_linear_paused_position_decides_what_is_spared[B-withheld1-downstream1], tests/orchestration/test_pause_control.py::TestTheMask::test_linear_two_paused_tasks]
m11: restored byte-identical: True
m12: the linear mask also withholds the pending tasks BEFORE the paused one -- exit=1 failed=3 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTheMask::test_linear_paused_position_decides_what_is_spared[B-withheld1-downstream1], tests/orchestration/test_pause_control.py::TestTheMask::test_linear_paused_position_decides_what_is_spared[C-withheld2-downstream2], tests/orchestration/test_pause_control.py::TestTheMask::test_linear_two_paused_tasks]
m12: restored byte-identical: True
m13: the graph mask withholds direct dependents only, not transitive ones -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTheMask::test_graph_transitive_dependents_beyond_the_immediate_child_are_withheld]
m13: restored byte-identical: True
m14: a paused task that is not pending still withholds its dependents -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestTheMask::test_graph_a_paused_task_that_is_not_pending_does_not_withhold_its_dependents]
m14: restored byte-identical: True
m15: the reason is stored unbounded -- exit=1 failed=1 failing_node_ids=[tests/orchestration/test_pause_control.py::TestReasonAndSourceAreBounded::test_an_over_long_reason_is_truncated_never_refused]
m15: restored byte-identical: True
control (after): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
packages/orchestration/pause_control.py: restored byte-identical: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f025-r1-mut
$ git worktree prune
$ git worktree list
(primary + the pre-existing set only; f025-r1-mut gone)
```
Every one of the 15 mutations is now red with at least one failing node id; every restore is
byte-identical; the tool's own final line reads `True`.

### G6 — tree and push (readings go in the final reply, after C5)

## Authored-text proofs

`.agent/authored/f025-r1-block.md`, `f025-r1-plan.md`, `f025-r1-context.md` and
`f025-r1-claim.diff` were built with `shutil.copyfile` from the reviewer's payload files —
never retyped, never edited — and G1 compared every one byte for byte, read back with
`git show <commit>:<path>`, against its source: all four BYTE-IDENTICAL. `.agent/plan.md` and
`.agent/context.md` were rewritten whole via `shutil.copyfile` from the same payload files
(never retyped) as part of C2; G2 confirmed both match the PAYLOADS table's digests exactly.
`claim.diff` was applied with `git apply` (never hand-edited) after `git apply --check` passed;
G2's per-file byte/sha256 table over `.agent/live_review.md`, `docs/roadmap/STATUS.md`,
`.agent/decisions.md` and the re-copied `plan.md`/`context.md` confirms the applied result.
`packages/orchestration/pause_control.py` and `tests/orchestration/test_pause_control.py` are
WORKER-authored production code and tests per the block's S1–S9 specification, not reviewer
payloads — no authored-text proof applies to them; `.agent/authored/f025-r1-mutations.py` is
likewise worker-authored (the G5 tool), saved as instructed rather than copied from a payload.

## Deviations & assumptions

1. **C3 split into C3a/C3b.** S6 explicitly authorizes this when the module alone would reach
   the 500-insertion cap; the whole module is 544 lines, so it landed as C3a (S2, S3, 291
   insertions) and C3b (S4, S5, 253 insertions), exactly as S6 names them. Not a deviation from
   the letter of the block, but noted per the "any departure from the ordered sequence" rule.
2. **C4 split into C4a/C4b.** The block's BUNDLE line names C4 as one commit ("THE TESTS AND
   THE MUTATION TOOL"), but bundling `tests/orchestration/test_pause_control.py` (319
   insertions) and `.agent/authored/f025-r1-mutations.py` (260 insertions) into one commit would
   total 579 insertions — over constraint 2's unconditional 500-insertion cap, which the block
   did not anticipate for this pairing the way it did for the module. Rather than compress
   either file in ways that could weaken test coverage or the tool's clarity, I split it the
   same way S6 authorizes for C3: C4a (tests) then C4b (mutation tool), same content, two
   commits. Justification: constraint 2 is unconditional and binds regardless of which item it
   applies to; S6 already establishes the repair mechanism (split, don't shrink) for exactly
   this situation.
3. **Extra commit C4c.** G5's first run (worktree at C4b's HEAD) found mutation m8 green — the
   test for "release of an unpaused task" was releasing a task from a job that had never paused
   *any* task, so it returned via `release_task_pause`'s earlier "`paused_tasks/` does not
   exist" branch rather than reaching the "no entry for this specific task" branch m8 mutates.
   Per the block's own G5 clause ("a mutation that stays green ... you then add the test that
   catches it in C4 before C5 and re-run the tool"), C4c adds five lines pausing a different
   task first, so the release now reaches the mutated code; G5's second run, from a fresh
   worktree at C4c's HEAD, caught all 15 mutations and reported `True`. This is an extra commit
   not named in the block's C1a/C1b/C2/C3a/C3b/C4a/C4b/C5 sequence, recorded here per the
   "extra commit is a deviation even when correct" rule.
4. **No full-suite run.** Per constraint 7 / amend0917-throughput, only G4's targeted selection
   ran; the one full-suite run per feature belongs to F025's closure, not this round.

No payload was edited or retyped. No production file outside
`packages/orchestration/pause_control.py` was touched; `safe_points.py` and `secure_fs.py` are
confirmed untouched by G3's `git diff --stat`. The worktree `.remedy-wt/f025-r1-mut` this round
created (twice, for G5's two runs) was removed both times, per constraint 6; every pre-existing
worktree and stash was left alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 371 insertions, matches block's expectation (300+71) exactly |
| C1b | done | 171 insertions, matches exactly |
| C2 | done | 15/17, 82/0, 29/24, 23/20, 1/1 by `git show --numstat`, matches the block's table exactly |
| C3a | deviated | S6-authorized split of the module spec (S2, S3); see Deviations #1 |
| C3b | deviated | S6-authorized split of the module spec (S4, S5); see Deviations #1 |
| C4a | deviated | split from the block's single C4 to respect the 500-insertion cap; see Deviations #2 |
| C4b | deviated | split from the block's single C4 to respect the 500-insertion cap; see Deviations #2 |
| C4c | deviated | extra commit fixing a mutation G5 found green; see Deviations #3 |
| C5 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical |
| G2 | done | all 5 file digests matched; open-finding sets, heading counts, last line, STATUS line and name-only diff all matched |
| G3 | done | ruff clean, diff-name-only exact, no banned imports, safe_points.py/secure_fs.py untouched |
| G4 | done | 760 passed, 1 skipped (D12 only), exit 0; reconciled exactly against the reviewer's count; integrity check 6/6 pass |
| G5 | deviated | first run found m8 green (reported as green, not papered over); fixed in C4c; second run caught all 15, `True` |
| G6 | done | reported in the final reply, after C5 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1. Then T001's second
half — the pause at the linear runner's and the cycle executor's safe points and ready sets,
parking, the relaunch, a stop beating a pause, and the deadline counting through a pause. Open
findings: 1. Operator questions open: 3.
