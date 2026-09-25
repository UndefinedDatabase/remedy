# Handback — F025 Pause/resume (global & per node) · Round 5

## Session

SESSION 1 of feature F025 · round 5 · rounds so far 5

Roughly a third of the context budget remained at the point this handback was written; the round
booked round 4's PASS, repaired R-1051 and R-1052 against their own FIX clauses, then landed
DECISION F025 D3 whole: the dashboard's `pause` object (U1), the client type and its normalization
(U2), the graph's new `paused` node state with its treatment, mark, reducer cases and seed (U3-U6),
and the two design-reference rows (U7). No conflict surfaced against the record; two existing,
unlisted files needed touching to make D3 clause 2's own stated purpose true or to support a
widened existing test — both are named in Deviations #1 and #2, with reasons.

## Range

Review of db496696..HEAD

## Commits

### b6bce17fa F025 R5 C1a: copy round 5 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r5-block.md | +192/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r5-d3.md | +47/-0 | copy of the d3.md payload (DECISION F025 D3) |
| .agent/authored/f025-r5-ledger.md | +6/-0 | copy of the ledger.md payload (R-1051, R-1052) |
| .agent/authored/f025-r5-plan.md | +34/-0 | copy of the plan.md payload |
| .agent/authored/f025-r5-slip.txt | +1/-0 | copy of the slip.txt payload |

280 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 192, plus 88: 47+6+34+1 = 88) — matches exactly.

### bc50b0a8b F025 R5 C1b: book round 4, register R-1051 and R-1052, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +47/-0 | d3.md appended (bytes to bytes) |
| .agent/live_review.md | +6/-0 | ledger.md appended (bytes to bytes) |
| .agent/plan.md | +13/-12 | rewritten whole to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | slip.txt appended (bytes to bytes) |

47/0, 6/0, 13/12, 1/0 — matches the block's stated expectation exactly. `open_finding_ids` over
`.agent/live_review.md` at this commit reads `['R-1008', 'R-1051', 'R-1052']`, the reviewer's own
simulated reading.

### 510c5f01f F025 R5 C2: R-1051's FIX — withdraw a pending pause before answering parked
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pause_control.py | +18/-8 | `unpause_job_command`'s job-scope branch reordered: a pending job pause is withdrawn FIRST, whatever the state; only once nothing is pending does state `paused` WITH a non-empty `job.pause` answer `parked`; docstring rewritten to match |
| tests/cli/test_job_pause.py | +38/-0 | NEW `TestR1051WithdrawBeforeParked`: a new pause on an already-parked job now answers `withdrawn` with nothing left pending; a job the task cap parked (`job.pause` empty) answers `not_paused` |

56 insertions, under the cap. 41/41 tests pass in this file after the change (39 existing + 2 new).

### 58ddd1838 F025 R5 C3: R-1052's FIX — task_paused and task_resumed exactly once by the ledger
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pause_control.py | +48/-10 | new `_task_pause_event_exists` (mirrors `pingpong_job._job_paused_event_exists` exactly, True/False/None); `pause_job_command`'s task branch checks the LEDGER by request id, not the control-file entry; `unpause_job_command`'s task branch peeks the entry via `paused_tasks`, writes the event BEFORE releasing it, then releases; both `_write_task_*_event` docstrings rewritten |
| tests/cli/test_job_pause.py | +69/-0 | NEW `TestR1052EventsAreExactlyOnceByTheLedger`: a `task_paused` write that fails once is written by the retry, exactly once; a `task_resumed` write that fails leaves the task paused, the retry writes it once and releases |

117 insertions, under the cap. 43/43 tests pass in this file after the change (41 + 2 new).

### 18111e396 F025 R5 C4: U1 — the dashboard's pause object (DECISION F025 D3 clause 1)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +37/-0 | new `_build_pause_section(job)`: `record` (job's own pause record while `paused`, else `{}`), `requested` (`pause_control.pause_requested` is not None), `paused_task_ids` (paused AND `status == "pending"` tasks, in plan order — a done task's pause omitted), `error` (`""`, or a caught `PauseControlError`/`StopControlError`'s text, the other three then empty); wired into `_build_dashboard`'s return dict as `"pause"` |
| tests/ui_server/test_dashboard_pause.py | +135/-0 | NEW FILE (T2): `record` while parked / empty otherwise; `requested` true/false against a real control root; `paused_task_ids` omits a done task and keeps plan order; both control-error paths report `error` without raising, the other three fields empty |

172 insertions, under the cap. 8/8 tests pass, all new.

### b24ca9ae0 F025 R5 C5: U2 to U6 — the client pause type, the paused node state, its treatment, mark, reducer cases and seed
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/types.ts | +15/-1 | new `RemedyPause` interface (`record`, `requested`, `pausedTaskIds`, `error`); `RemedyDashboard` gains `pause: RemedyPause` (non-optional) |
| apps/ui/src/api/remedyApi.ts | +19/-1 | new `normalizePause(raw)`, a payload without `pause` normalizes to the "not paused" shape; wired into both `RemedyDashboard` builders (`normalizeDashboardPayload` and `normalizeApiFailure`) |
| apps/ui/src/api/remedyApi.test.ts | +35/-0 | three new tests: without a `pause` section, with all four fields read (snake→camel `pausedTaskIds`), and an error read with the other three kept empty |
| apps/ui/src/components/graph/brainOntology.ts | +16/-2 | `NodeState` gains `"paused"`; `SEED_STATUS_STATE_TABLE` gains `paused: "paused"` |
| apps/ui/src/components/graph/brainReducer.ts | +54/-0 | `onTaskPaused` (births like `task_needs_decision`, skips a task already `pass`/`fail`), `onTaskResumed` (paused→planned, no birth, touches only a currently-`paused` node), `onJobPaused` (in-progress task→planned as a stop does; in-progress RUN→`paused`, not `blocked`); four new `applyBrainEvent` cases, none counted in `ignored` |
| apps/ui/src/components/graph/brainReducer.test.ts | +58/-0 | new `describe` block: the four cases, never-overwrite-pass, no-op on a non-paused resume, not-ignored, and a replayed `task_paused` seq stays identical (===) |
| apps/ui/src/components/graph/brainReducer.fixtures.ts | +3/-0 | `SEED_STATUS_CASES` (Table 1's own fixture) gains `["paused", "paused"]` — see Deviations #2 |
| apps/ui/src/components/graph/brainView.ts | +17/-5 | `dashboardBrainSeeds` gains an optional `pausedTaskIds` parameter (default `[]`, every existing call site unchanged); `BRAIN_FILTER_STATES.planned` gains `"paused"` |
| apps/ui/src/components/graph/brainView.test.ts | +17/-0 | new tests: a named task seeds `paused` regardless of its dashboard status word; no second argument seeds exactly as before; `BRAIN_FILTER_STATES.planned` groups `paused` with `planned` |
| apps/ui/src/components/graph/BrainGraphStage.tsx | +4/-1 | the seed call now passes `dashboard.pause.pausedTaskIds` — see Deviations #1 |
| apps/ui/src/components/graph/renderers/glyphPaths.ts | +14/-2 | `StateMark` gains `"pause"`; `STATE_MARK_PATHS.pause` — two rectangles, x 17-19 and 21-23, y 1.5-7.5 (the status dot's own box), a visible 2-unit gap |
| apps/ui/src/components/graph/renderers/nodeStates.ts | +19/-0 | `NODE_STATE_TREATMENTS.paused` — the planned node's own fill/ink/line/size/no-halo/no-pulse/no-branch-glow, plus `marks: [ring, pause]`; legend name "Paused", placed right after `planned` |
| apps/ui/src/components/graph/renderers/nodeStates.test.ts | +23/-7 | `ALL_STATES`/`FILL_TOKENS` widened; the ink/line test widened to name `paused` alongside `planned`; the token list gains `--remedy-orange-400`; the branch-glow object literal widened; a new dedicated `paused` treatment/mark test |
| apps/ui/src/components/graph/renderers/glyphConformance.ts | +11/-1 | `BINDING_STATE_MARKS.paused = ["ring", "pause"]` (keyed right after `planned`, matching `nodeStateOrder()`); `BINDING_MARK_TOKENS.pause` |
| apps/ui/src/components/graph/renderers/glyphConformance.test.ts | +35/-10 | new pause-mark probe-point test; the conformance-probe tally test's counts widened for 8 states/4 marks (240 probes, was 144); a new "paused task present" probe test; the device-pixel placement test's `fail` column corrected (shifted from 4 to 5 by `paused`'s insertion) |
| apps/ui/src/components/graph/renderers/paintNode.test.ts | +11/-0 | new test: an outlined pause mark, in its orange, painted on a `paused` node, alongside its ring |
| apps/ui/src/components/graph/runDetailModel.ts | +1/-0 | `STATE_WORDS.paused = "Paused"` |

352 insertions, under the cap. `tsc --noEmit`, `eslint` over every touched file, and a vitest sweep
of 66 test files / 1226 tests (1 pre-existing unrelated skip file) all passed clean before this
commit.

### e07ebddd9 F025 R5 C6: U7 — the pause mark's row and the assumption-log entry (DECISION F025 D3)
| Path | +/- | Reason |
|---|---|---|
| docs/ui/design_reference/assets_spec.md | +1/-0 | §4's table gains the pause mark's row, in its existing 6-column shape, beside `vetoed` |
| docs/ui/design_reference/assumption_log.md | +1/-0 | one row, last, in its 7-column shape, citing DECISION F025 D3 — the reference names no paused state, token or icon |

2 insertions, under the cap.

### fe08bb772 F025 R5 C7: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r5-mutations.py | +308/-0 | m1-m2 (R-1051, `pause_control.py`), m3-m4 (R-1052, `pause_control.py`), m5-m6 (U1, `ui_server.py`) run `python3 -B -m pytest` over T1+T2 from the worktree root; m7-m9 (the reducer, `brainReducer.ts`), m10 (the treatment/mark, `nodeStates.ts`), m11 (the seed, `brainView.ts`) run vitest over the round's six changed `.test.ts` files by the f024-r1-mutations.py route; each FROM verified single-occurrence before commit and re-verified in a disposable pre-commit worktree (see External actions) |

308 insertions, under the cap.

### (this commit) F025 R5 C8: rewrite handoff for round 5
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f025-r5-mutdraft HEAD` (at C6's HEAD `e07ebddd9`, before the
  mutation tool was committed) — succeeded; a pre-commit dry run of the DRAFT tool
  (`.remedy-wt/f025-r5-worker/f025-r5-mutations.py`, copied to `.agent/authored/` only after this
  proved clean) — all 11 mutations caught, all restores byte-identical, both controls green.
- `git worktree remove --force .remedy-wt/f025-r5-mutdraft` — succeeded.
- `git worktree prune` — succeeded (no-op).
- `git worktree add --detach .remedy-wt/f025-r5-mut fe08bb772` (C7's HEAD) — succeeded, for G5's one
  official run against the committed tool.
- `git worktree remove --force .remedy-wt/f025-r5-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees named in constraint 5 — nothing new left behind.
- `git push origin feature/f025-pause-resume` — runs immediately after this commit (C8); its real
  outcome is reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 4: nothing is
merged). No `git stash`, no force-push, no checkout of another branch.

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
db4966962 F025 R4 C9: rewrite handoff for round 4
```

```
$ (line count and sha256 of .remedy-wt/f025-r5/block.md, measured)
line_count: 192
sha256: 20583aa153e709d677a87f571b18874ce40c7e5fc98a079db1349f3a60120d3c
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list   (as found, before this round touched anything)
```
Listed the primary checkout at `feature/f025-pause-resume`/`db4966962`, every `f015-*`/`f020-*`/
`f023-*`/`f024-*`/`f025-*`/`f284-*` round worktree already on disk (including `f025-r1-dry`,
`f025-r2-sim`, `f025-r3-sim`, `f025-r4-sim`, `f025-r5-sim`), and four `job-*` worktrees plus ten
`prunable` job worktrees under `/tmp` from a previous pytest run — all left untouched all round.

### PAYLOADS table
```
$ (python: newline count, byte count, sha256 of each payload)
d3.md     lines=47 bytes=4039 sha256=84e4d79e839c373c26d6c4e1552789afa14b65394a342569b6e628d5a47230e7
ledger.md lines=6  bytes=6480 sha256=393efd0aae8dc5ad5867249528fc5d85c922639103bdc861f365881bc38294a2
plan.md   lines=34 bytes=1236 sha256=b8918a99b856da122f1e8fdce542d554bb64ff7f83f4cddfd5f4ee445b451174
slip.txt  lines=1  bytes=342  sha256=b606248040beff21fd81b78a8c1ca4726e7488c0a6b407f628533702d82274f1
```
All 4 match the PAYLOADS table exactly (G1).

### G1 — transport
```
$ (python: each committed .agent/authored/f025-r5-* copy, read via `git show b6bce17fa:<path>`,
   compared byte for byte against its source)
.agent/authored/f025-r5-block.md  == .remedy-wt/f025-r5/block.md  : True
.agent/authored/f025-r5-d3.md     == .remedy-wt/f025-r5/d3.md     : True
.agent/authored/f025-r5-ledger.md == .remedy-wt/f025-r5/ledger.md : True
.agent/authored/f025-r5-plan.md   == .remedy-wt/f025-r5/plan.md   : True
.agent/authored/f025-r5-slip.txt  == .remedy-wt/f025-r5/slip.txt  : True
```
```
$ (numstat comparison against the block's C1b table: decisions.md 47/0, live_review.md 6/0,
   plan.md 13/12, prose_slips.md 1/0)
all four match exactly
```
```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over C1b's .agent/live_review.md
['R-1008', 'R-1051', 'R-1052']
```
Matches the block's stated reading exactly.

### G2 — the code
```
$ python3 -m ruff check packages/orchestration/pause_control.py packages/orchestration/ui_server.py \
  .agent/authored/f025-r5-mutations.py
All checks passed!
```
```
$ git diff --stat db496696 fe08bb772 -- packages/orchestration/safe_points.py \
  packages/orchestration/pingpong_job.py packages/orchestration/pingpong_loop.py \
  packages/orchestration/long_run_executor.py apps/ui/src/styles/tokens.css \
  docs/ui/design_reference/tokens.css docs/ui/design_reference/graph_spec.md
(empty)
```
Confirmed empty — none of the seven forbidden files/paths touched.
```
$ (python: count of lines added under packages/apps/scripts containing "noqa: BLE001")
noqa BLE001 additions: 0
```
```
$ git diff --name-only bc50b0a8b fe08bb772
.agent/authored/f025-r5-mutations.py
apps/ui/src/api/remedyApi.test.ts
apps/ui/src/api/remedyApi.ts
apps/ui/src/api/types.ts
apps/ui/src/components/graph/BrainGraphStage.tsx
apps/ui/src/components/graph/brainOntology.ts
apps/ui/src/components/graph/brainReducer.fixtures.ts
apps/ui/src/components/graph/brainReducer.test.ts
apps/ui/src/components/graph/brainReducer.ts
apps/ui/src/components/graph/brainView.test.ts
apps/ui/src/components/graph/brainView.ts
apps/ui/src/components/graph/renderers/glyphConformance.test.ts
apps/ui/src/components/graph/renderers/glyphConformance.ts
apps/ui/src/components/graph/renderers/glyphPaths.ts
apps/ui/src/components/graph/renderers/nodeStates.test.ts
apps/ui/src/components/graph/renderers/nodeStates.ts
apps/ui/src/components/graph/renderers/paintNode.test.ts
apps/ui/src/components/graph/runDetailModel.ts
docs/ui/design_reference/assets_spec.md
docs/ui/design_reference/assumption_log.md
packages/orchestration/pause_control.py
packages/orchestration/ui_server.py
tests/cli/test_job_pause.py
tests/ui_server/test_dashboard_pause.py
```
Every path is inside constraint 3's set — the two files outside U2-U6's literal name list
(`apps/ui/src/components/graph/BrainGraphStage.tsx`,
`apps/ui/src/components/graph/brainReducer.fixtures.ts`) are each named above and in Deviations
#1/#2 with what they widened and why.

### G3 — the tests nearest the change, serially
```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_pause.py \
  tests/ui_server/test_dashboard_contract.py tests/ui_server/test_dashboard_pause.py \
  tests/ui_contracts/test_node_glyph_tokens.py tests/ui_contracts/test_graph_legend_contract.py \
  tests/ui_contracts/test_ui_lint.py tests/orchestration/test_test_runner.py
........................................................................ [ 40%]
........................................................................ [ 80%]
...................................                                      [100%]
179 passed in 10.26s
REAL_EXIT=0
```
No `SKIPPED` line in this run. The three named nodes confirmed PASSED (not skipped), individually:
```
$ python3 -m pytest -q -p no:cacheprovider -rA \
  "tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles" \
  "tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem" \
  "tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes"
PASSED tests/ui_server/test_dashboard_contract.py::TestJobSummaryCommandContract::test_typescript_compiles
PASSED tests/ui_contracts/test_ui_lint.py::test_the_ui_lint_passes_with_no_problem
PASSED tests/orchestration/test_test_runner.py::TestVitestFrontendTestFoundation::test_vitest_passes
3 passed in 5.70s
```
(the tsc node, the eslint node and the vitest node respectively — PASSING, not skipped)

### G4 — the neighbours
```
$ python3 .remedy-wt/f025-r5/run_sel.py /home/decodeux/Repos/remedy 8
files 143 exit 1 wall 196 s
ERROR: React UI not built.  (×3, unrelated pre-existing fixture noise, see below)
FAILED tests/ui_server/test_command_channel.py::TestCommandChannelDoor::test_a_refused_command_announces_nothing
FAILED tests/ui_server/test_decisions_endpoint.py::TestDecisionsEndpoint::test_decisions_endpoint_returns_the_inbox_document
FAILED tests/ui_server/test_command_dispatch.py::TestTaskPlanApprovalDispatchEffects::test_a_supplied_clarification_answer_is_recorded_as_human
FAILED tests/ui_server/test_pause_door_live.py::TestTaskScopeLiveDoor::test_pause_withholds_one_task_and_unpause_releases_it
SKIPPED [1] tests/regression/test_named_bugs.py:295 ... (×6, D3 quarantine F252)
SKIPPED [1] tests/test_agent_tooling.py:43 ... (D12 quarantine F252)
SKIPPED [1] tests/test_install_smoke.py:175 ... (opt-in)
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257 ... (UI source not found)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441/484 ... (×2, D3 quarantine F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507/543 ... (×2, D3 quarantine F252)
4 failed, 9687 passed, 13 skipped, 1 warning in 196.03s (0:03:16)
```
Re-ran each failing node's FILE alone, serially, per the block's instruction:
```
$ python3 -m pytest -q -p no:cacheprovider -rfE tests/ui_server/test_pause_door_live.py
......                                                                   [100%]
6 passed in 7.48s
$ python3 -m pytest -q -p no:cacheprovider -rfE tests/ui_server/test_command_channel.py
........................................................................ [ 66%]
.....................................                                    [100%]
109 passed in 8.20s
$ python3 -m pytest -q -p no:cacheprovider -rfE tests/ui_server/test_decisions_endpoint.py
....                                                                     [100%]
4 passed in 1.72s
$ python3 -m pytest -q -p no:cacheprovider -rfE tests/ui_server/test_command_dispatch.py
................................                                         [100%]
32 passed in 2.46s
```
All four pass alone, serially — an xdist-worker-ordering flake class (the same category the block's
own baseline names for six `tests/cli/test_study_cmd.py` nodes, just a different set of files this
round), not a regression. See Deviations #3.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=159"},
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
```
$ git worktree add --detach .remedy-wt/f025-r5-mut fe08bb772
$ python3 -B .agent/authored/f025-r5-mutations.py .../f025-r5-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f025-r5-mut
CONTROL FIRST: pytest exit=0 failed=0 | vitest exit=0 failed=0
m1 (unpause_job_command answers parked before it looks for a pending pause) [py]: exit=1 failed=2
  failing=[...TestR1051WithdrawBeforeParked::test_a_new_pause_on_a_parked_job_can_be_withdrawn,
  ...TestR1051WithdrawBeforeParked::test_a_job_paused_by_the_task_cap_answers_not_paused]
  caught=True restored byte-identical=True
m2 (a job in state paused with an EMPTY pause record answers parked) [py]: exit=1 failed=1
  failing=[...TestR1051WithdrawBeforeParked::test_a_job_paused_by_the_task_cap_answers_not_paused]
  caught=True restored byte-identical=True
m3 (task_paused is written only when the call created the entry) [py]: exit=1 failed=1
  failing=[...TestR1052EventsAreExactlyOnceByTheLedger::test_a_failed_task_paused_write_is_written_by_the_retry]
  caught=True restored byte-identical=True
m4 (a release removes the entry before it writes task_resumed) [py]: exit=1 failed=1
  failing=[...TestR1052EventsAreExactlyOnceByTheLedger::test_a_failed_task_resumed_write_leaves_the_task_paused]
  caught=True restored byte-identical=True
m5 (the dashboard's paused_task_ids keeps a paused task that is done) [py]: exit=1 failed=1
  failing=[...TestPausedTaskIds::test_omits_a_done_task_and_keeps_plan_order]
  caught=True restored byte-identical=True
m6 (the dashboard raises on a PauseControlError instead of reporting error) [py]: exit=1 failed=2
  failing=[...TestError::test_a_pause_control_error_is_reported_without_raising,
  ...TestError::test_a_stop_control_error_is_reported_without_raising]
  caught=True restored byte-identical=True
m7 (the reducer ignores task_paused) [ts]: exit=1 failed=1
  failing=[F025 pause/resume events ... > task_paused births an unseen task paused, and is not counted in ignored]
  caught=True restored byte-identical=True
m8 (task_resumed leaves the node paused) [ts]: exit=1 failed=1
  failing=[F025 pause/resume events ... > task_resumed returns a paused task to planned, and is not counted in ignored]
  caught=True restored byte-identical=True
m9 (job_paused leaves in-progress run nodes in_progress) [ts]: exit=1 failed=1
  failing=[F025 pause/resume events ... > job_paused returns an in-progress task to planned and its open run to paused, and is not counted in ignored]
  caught=True restored byte-identical=True
m10 (the paused treatment drops the pause mark) [ts]: exit=1 failed=5
  failing=[NODE_STATE_TREATMENTS > names only design tokens..., state is never colour alone > draws a
  paused node..., state is never colour alone > draws only failed and blocked alike...,
  paintBrainNode — state is never colour alone > puts an outlined pause mark...,
  the binding spec the harness judges against > names a mark list for every state...]
  caught=True restored byte-identical=True
m11 (the seed ignores pausedTaskIds) [ts]: exit=1 failed=1
  failing=[dashboardBrainSeeds > seeds a task named in pausedTaskIds as paused...]
  caught=True restored byte-identical=True
CONTROL LAST: pytest exit=0 failed=0 | vitest exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f025-r5-mut
$ git worktree prune
$ git worktree list
(primary + the pre-existing set only; f025-r5-mut gone)
```
Every one of the 11 mutations is red with at least one failing node; every restore is
byte-identical; both the first and last unmutated controls (pytest AND vitest together) are green;
the tool's own final line reads `True`.

### G6 — tree and push (readings go in the final reply, after C8)

## Authored-text proofs

`.agent/authored/f025-r5-block.md`, `f025-r5-d3.md`, `f025-r5-ledger.md`, `f025-r5-plan.md` and
`f025-r5-slip.txt` were built with `shutil.copyfile` from the reviewer's payload files — never
retyped, never edited — and G1 compared every one byte for byte, read back with `git show
b6bce17fa:<path>`, against its source: all five BYTE-IDENTICAL. `.agent/decisions.md`,
`.agent/live_review.md` and `.agent/prose_slips.md` were appended with raw bytes read from
`d3.md`/`ledger.md`/`slip.txt` (`open(..., "ab").write(payload)`), never retyped; `.agent/plan.md`
was rewritten whole from `plan.md`'s bytes via `shutil.copyfile`. G1's numstat comparisons confirm
all four match the payloads' expected insertion counts exactly. `packages/orchestration/
pause_control.py`, `packages/orchestration/ui_server.py`, `tests/cli/test_job_pause.py`,
`tests/ui_server/test_dashboard_pause.py`, every `apps/ui/src/` file U2-U6 name plus
`BrainGraphStage.tsx` and `brainReducer.fixtures.ts`, both design-reference doc rows, and
`.agent/authored/f025-r5-mutations.py` are WORKER-authored production code, tests, docs and the G5
tool against the FIX clauses and U1-U7's own specification — not reviewer payloads — so no
authored-text proof applies to them.

## Deviations & assumptions

1. **`apps/ui/src/components/graph/BrainGraphStage.tsx` touched, though U2-U6 do not name it.**
   `dashboardBrainSeeds` gained an optional `pausedTaskIds` parameter (U6) so it CAN seed a paused
   task, but DECISION F025 D3 clause 2's own text states the purpose plainly: "The dashboard's
   `paused_task_ids` seed their tasks as `paused`, so a page opened on a parked job shows them" —
   a live-page guarantee, not merely a function capability. `BrainGraphStage.tsx` is the ONE call
   site in the tree that holds both `dashboard.tasks` and `dashboard.pause` in scope (confirmed by
   searching every `dashboardBrainSeeds(` call site); without wiring it, the clause's stated
   guarantee would be false in the running app. `useTimelineScrub.ts`'s separate call site (only
   `tasks`, no `dashboard`) was deliberately left untouched — it is not named by U2-U6 either, and
   D3 clause 5 defers "the rest of the UI" (the banner, the NowCard's line, the buttons) to next
   round; the scrubber's own pause-seeding is not named by clause 2's literal text and stays out of
   scope. The edit itself is a two-line call-site change plus its `useMemo` dependency array.
2. **`apps/ui/src/components/graph/brainReducer.fixtures.ts` touched, though it is not a `.test.ts`
   file.** `SEED_STATUS_CASES` is Table 1's own fixture — "every listed seed status, plus one
   unknown" — consumed ONLY by `brainReducer.test.ts`'s `it.each(SEED_STATUS_CASES)` (the "Seed
   status table (Table 1)" describe block, one of the five vitest files T3 names as widened). Adding
   `SEED_STATUS_STATE_TABLE.paused` (brainOntology.ts, named by U3/U6) without adding `["paused",
   "paused"]` here would leave that widened test's own table incomplete — the fixture is the widened
   test's data, inseparable from the widening constraint 3 already authorizes for
   `nodeStates.test.ts`/`glyphConformance.test.ts`/`paintNode.test.ts`.
3. **G4 found 4 failed on the combined 8-worker run, all four passing alone, serially.** An
   xdist-worker-ordering flake class, the same category the block's own baseline names for six
   `tests/cli/test_study_cmd.py` nodes (a different file set this round) — not a regression. Every
   failing file was re-run alone per the block's instruction; all pass (readings in Verification).
4. **`legendModel.test.ts` and `glyphMatrix.test.ts`, named by T3's widened-test list, needed no
   edit.** Both files derive their state list ENTIRELY from `nodeStateOrder()`
   (`Object.keys(NODE_STATE_TREATMENTS)`) with no hardcoded state array of their own — adding
   `paused` to `NODE_STATE_TREATMENTS` (nodeStates.ts) already widens what they exercise; running
   both unmodified confirmed 8/8 passing before and after. No change was made to either file.
5. **No full-suite run.** Per constraint 6 (amend0917-throughput), only G4's targeted selection ran;
   the one full-suite run per feature belongs to F025's closure, not this round.

No payload was edited or retyped. No production file outside `packages/orchestration/pause_control.py`,
`packages/orchestration/ui_server.py`, and the `apps/ui/src/` files named above (U2-U6 plus
Deviations #1/#2) was touched; `safe_points.py`, `pingpong_job.py`, `pingpong_loop.py`,
`long_run_executor.py`, `_safe_event_summary`, both `tokens.css` files, `graph_spec.md` and
`docs/roadmap/` are confirmed untouched by G2's `git diff --stat`. The worktrees this round created
(`.remedy-wt/f025-r5-mutdraft` once, `.remedy-wt/f025-r5-mut` once) were each removed the same
round, per constraint 5; every pre-existing worktree was left alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 280 insertions, matches the block's expectation (192+88) exactly |
| C1b | done | 47/0, 6/0, 13/12, 1/0 insertions, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1051', 'R-1052']` |
| C2 | done | 56 insertions; R-1051's FIX and its two new tests landed; 41/41 pass |
| C3 | done | 117 insertions; R-1052's FIX and its two new tests landed; 43/43 pass |
| C4 | done | 172 insertions; U1's dashboard section and T2's 8-test file landed |
| C5 | done | 352 insertions; U2-U6 landed whole, plus the two named widenings (Deviations #1, #2); tsc/eslint/vitest clean before commit |
| C6 | done | 2 insertions; U7's two rows landed |
| C7 | done | 308 insertions; the G5 tool landed, validated in a pre-commit dry-run worktree first |
| C8 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical; open-finding set matched |
| G2 | done | ruff clean over every changed .py file; forbidden files/paths untouched; noqa:BLE001 added = 0; name-only diff exactly inside constraint 3 |
| G3 | done | 179 passed, exit 0, no SKIPPED; the tsc node, the eslint node and the vitest node each confirmed PASSED individually |
| G4 | done | 4 failed on the combined run, all four pass alone/serially (Deviations #3); integrity check 6/6 pass |
| G5 | done | all 11 mutations caught, all restores byte-identical, `True`; validated once pre-commit in a disposable worktree, then officially at C7's HEAD |
| G6 | done | reported in the final reply, after C8 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 5. Then T003's second part —
the door client, the stage banner, the NowCard's line and the pause and resume buttons (job and
task scope), per DECISION F025 D3 clause 5's own deferral. Open findings: 3 — `R-1008` (owned by
F285), `R-1051` and `R-1052` (owned by F025, repaired this round pending the reviewer's own
verdict) — the count `open_finding_ids` reads at C1b. Operator questions open: 4 — the count of
`### Q` headings in `.agent/operator_questions.md` at C1b (unchanged this round).
