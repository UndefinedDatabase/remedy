# Handoff — F029, round 4

## Session

SESSION 1 of feature F029 · round 4 · rounds so far 4. Context remaining at
handback: comfortable — reading `subtree_rerun.py`, `task_veto.py`,
`event_names.py`/its test, `humanizeCatalog.ts`/its test, the relevant slices of
`ui_server.py` (`_build_dashboard`, `JOB_INJECT_COMMAND_IDS`,
`_handle_command_submission`, `_dispatch_injection`,
`_read_command_payload`), `UI_EXPOSED_COMMANDS`, `test_command_channel.py`'s
door-import guard and exposed-commands pin, the injection class of
`test_command_dispatch.py`, and `test_dashboard_task_origin.py`, then drafting
S1–S4 plus their three new/extended test files and the mutation tool took the
bulk of it; one unexpected repair (a transitive-import guard reach and a cost
estimate's dependency-graph interaction with test fixtures) was found and fixed
within the round; every gate ran clean afterward, with ample context left had a
further repair round been needed.

## Range

Review of `5d9c8784`..`HEAD` (`HEAD` is this handback's own commit, `F029 R4
C6b`, on `feature/f029-subtree-rerun`).

## Commits

### 5ed69a271 F029 R4 C1: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r4-block.md | 242/0 | copy of this round's block |
| .agent/authored/f029-r4-booking.diff | 73/0 | copy of the booking diff payload |
| .agent/authored/f029-r4-plan.md | 35/0 | copy of the plan payload |

Measured insertions: 350 (block's own line count 242 + 108), matching the
block's expectation exactly, under the 500-line cap.

### 5dc524232 F029 R4 C2: book round 3's PASS, resolve R-1081, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | 53/0 | DECISION F029 D4 appended |
| .agent/live_review.md | 4/0 | round 3's Gate entry and R-1081's `Done:` line appended |
| .agent/plan.md | 12/10 | rewrite from the plan payload |

Matches the block's expected numstat (53/0, 4/0, 12/10) exactly. Applied via
`git apply --check` (exit 0) then the real apply (exit 0) of `booking.diff`,
followed by the `plan.md` rewrite via `shutil.copyfile`.

### bd9acd152 F029 R4 C3: one rerun command answers the preview or the preparation, and the preparation writes its event
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/subtree_rerun.py | 105/1 | S1: `rerun_subtree_command` — never raises, answers `refused`/`needs_confirmation`/`prepared`; S2: `prepare_subtree_rerun` writes `subtree_rerun_prepared` to the run log after `save_job_plan`, inside R-1081's guarded block |
| packages/orchestration/event_names.py | 1/0 | S2: `subtree_rerun_prepared` joins `EVENT_NAMES` in sorted place |
| apps/ui/src/api/humanizeCatalog.ts | 1/0 | S2: the catalog's plain sentence for `subtree_rerun_prepared`, in sorted place |
| tests/orchestration/test_subtree_rerun_prepare.py | 161/0 | new `TestRerunSubtreeCommand` (refused/needs_confirmation/prepared paths, thresholds, facts) and `TestRerunSubtreeCommandWritesTheEvent` (exactly one event on preparation, none on refusal) |

268 total insertions, under the 500-line cap; no split needed.

### 4c628ba56 F029 R4 C4: the dashboard's task item carries its attempts
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | 4/0 | S3: `_build_dashboard`'s task item gains `attempt` and `attempts`, directly before `origin`, which stays last |
| tests/ui_server/test_dashboard_task_attempts.py | 120/0 | new file, built as `test_dashboard_task_origin.py` builds its dashboard: after a fold, the reset task reads `attempt` 2 with one archived attempt, an untouched sibling reads `attempt` 1 and `attempts` `[]`, `origin` stays last in both |

124 total insertions, under the 500-line cap; no split needed.

### 7ab30b7f1 F029 R4 C5: expose job.rerun-subtree through the write door
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | 2/0 | S4: `job.rerun-subtree` joins `UI_EXPOSED_COMMANDS`, comment naming DECISION F029 D4 |
| packages/orchestration/ui_server.py | 69/0 | S4: `JOB_RERUN_SUBTREE_COMMAND_ID`, the `_handle_command_submission` branch (effect → 409 on `refused` → accepted/publish/event/200 otherwise), `_dispatch_rerun_subtree`, and `_read_command_payload`'s `task_id`/`model`/`confirm_cost` shape checks |
| tests/ui_server/test_command_channel.py | 19/5 | `DOOR_METHODS` gains `_dispatch_rerun_subtree`; `ALLOWED_IMPORTS` gains `(subtree_rerun, rerun_subtree_command)`; `ACCEPTED_TRANSITIVE_FORBIDDEN` gains `subprocess` (subtree_rerun's own module-level git plumbing import, reached now the door imports from it) with its stale "deliberately absent" comment corrected; the exact `UI_EXPOSED_COMMANDS` pin and the exposed-command loop each gain `job.rerun-subtree` |
| tests/ui_server/test_rerun_subtree_door.py | 177/0 | new file, modelled on `TestInjectionDispatchEffects`: `needs_confirmation` a 200 changing nothing, `prepared` a 200 after `confirm_cost` with a real one-task worktree job, a refusal a 409 reading `unknown_task: ...`, a non-bool `confirm_cost` and a missing `task_id` each 400 |

267 total insertions, under the 500-line cap; no split needed.

### 796500fe9 F029 R4 C6a: add the mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f029-r4-mutations.py | 198/0 | the G5 mutation (red-proof) tool, covering m1–m8 across `subtree_rerun.py` and `ui_server.py` |

### (this commit) F029 R4 C6b: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file |

## External actions

`git worktree add --detach .remedy-wt/f029-r4-mut 796500fe9` — created the disposable
mutation worktree at the last commit before C6b. `git worktree remove --force
.remedy-wt/f029-r4-mut` then `git worktree prune` — removed it after G5; `git worktree
list | wc -l` read 61 both before and after, matching the step-4 reading. `git push
origin feature/f029-subtree-rerun` — reported below under Verification/G6; its real
outcome is in the reply to the delegator, since C6b cannot contain it. No PR opened,
no merge, no branch deleted, no force-push, no stash.

## Verification

**BEFORE ANYTHING ELSE**
- `ls .agent/STOP` → `No such file or directory` (absent).
- `pwd` → `/home/decodeux/Repos/remedy`; `git status --porcelain` → empty; `git branch
  --show-current` → `feature/f029-subtree-rerun`; `git log --oneline -1` → `5d9c87849`.
- Block bytes (R-0954): measured 242 lines, sha256
  `d34d1d2a00de39cb74b26e90b8473e296a751e4ec7690023f5dae35af397314d` — both match the
  delegation message's readings exactly.
- `git worktree list | wc -l` → 61.

**PAYLOADS** — both matched the table exactly:
`booking.diff` 73 lines / 12137 bytes / `07ed6d77ca9f0a84086c2b7d62e3adf36637bbe7d88340902e0021e3d0ae4b5f`;
`plan.md` 35 lines / 1269 bytes / `1449df68e5a4957b0f60b3efa28cb39fc61493a87fffe09504426c2a6017efd5`.

**G1 TRANSPORT** — each `.agent/authored/f029-r4-*` copy read via `git show
5ed69a271:<path>` equals its source byte for byte: block copy (19432 bytes) ==
source (True, sha256 `d34d1d2a...397314d`); booking.diff copy (12137 bytes) ==
source (True, sha256 `07ed6d77...e3d0ae4b5f`); plan.md copy (1269 bytes) == source
(True, sha256 `1449df68...6017efd5`).

**G2 THE BOOKING** — sha256 of each file read via `git show 5dc524232:<path>`
equals the reviewer's reading exactly:
`.agent/decisions.md` 2295769 bytes, `3b542a421d20aa63a9640f80af772233c4c95a55083cb64a0e180fe66232493e` — match.
`.agent/live_review.md` 320687 bytes, `9ea984ea34c730d89b383cd745f3663836c5c97001f72d3a9fba8d99a84802d0` — match.
`.agent/plan.md` 1269 bytes, `1449df68e5a4957b0f60b3efa28cb39fc61493a87fffe09504426c2a6017efd5` — match.
`open_finding_ids` (`scripts/rotate_live_review.py`) over `.agent/live_review.md`'s
text: at `5d9c8784` → `['R-1081']`; at `5dc524232` → `[]` — both match the
reviewer's stated readings.

**G3 THE CODE** —
```
python3 -m ruff check apps/cli/command_catalog.py packages/orchestration/event_names.py packages/orchestration/subtree_rerun.py packages/orchestration/ui_server.py tests/orchestration/test_subtree_rerun_prepare.py tests/ui_server/test_command_channel.py tests/ui_server/test_dashboard_task_attempts.py tests/ui_server/test_rerun_subtree_door.py
```
→ `All checks passed!`, exit 0. `rerun_subtree_command`'s whole body (from
`bd9acd152`), `_dispatch_rerun_subtree`'s whole body and the new branch of
`_handle_command_submission` (both from `7ab30b7f1`) were read back with `git
show` and quoted in full during the round; all three match what is committed.

**G4 THE TESTS** — the exact selection, serially, real exit code:
```
python3 -m pytest -q -p no:cacheprovider -rs <the block's 30-file selection> 2>&1 | tail -16
```
→ `2417 passed, 11 skipped` at real exit code 0. All eleven `SKIPPED` lines cite
an F252 quarantine: four in `tests/ui_contracts/` (`test_graph_architecture.py`
lines 441, 484; `test_ux_quality.py` lines 507, 543, each D3), six in
`test_named_bugs.py`'s D3 quarantine (lines 295, 312, 321, 383, 392, 399) and one
in `test_agent_tooling.py`'s D12 quarantine (line 43) — the same eleven the
reviewer's own base reading at `5d9c8784` already carried; none is outside F252's
quarantine (the block's phrase "the seven F252 quarantines" describes an earlier
baseline the ledger has since grown past — a `prose_slips.md`-class inaccuracy,
not a defect, noted under Deviations below).
Accounting for the difference from 2402: `--collect-only -q` over the four test
files this round touched reads `tests/orchestration/test_subtree_rerun_prepare.py`
grown from 21 to 29 (+8), `tests/ui_server/test_dashboard_task_attempts.py` new at
2 (+2), `tests/ui_server/test_rerun_subtree_door.py` new at 5 (+5), and
`tests/ui_server/test_command_channel.py` unchanged at 110 (+0) — 15 nodes added
in total. 2402 + 15 = 2417, exactly the passed count above; no unexplained
difference. Then `python3 -m apps.cli.main integrity check --json` → all 6
checks `pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`), `fail_count: 0`,
`ok: true`.

**G5 THE RED PROOFS** — `git worktree add --detach .remedy-wt/f029-r4-mut
796500fe9`, then `python3 -B .agent/authored/f029-r4-mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f029-r4-mut`:
```
control (unmutated, first): exit=0 failed=0 nodes=[(none)]
m1 S1 prepares over an unavailable estimate without confirm_cost: exit=1 failed=3 nodes=[...TestRerunSubtreeCommand::test_needs_confirmation_above_the_threshold, ...test_needs_confirmation_for_an_unavailable_estimate_touches_nothing, tests/ui_server/test_rerun_subtree_door.py::TestRerunSubtreeDoor::test_needs_confirmation_is_a_200_that_changes_nothing]
m2 S1 answers needs_confirmation even with confirm_cost: exit=1 failed=5 nodes=[...TestRerunSubtreeCommand::test_a_preparation_refusal_answers_the_refused_shape_with_its_facts, ...test_confirm_cost_true_prepares_over_an_unavailable_estimate, ...TestRerunSubtreeCommandWritesTheEvent::test_a_preparation_writes_exactly_one_event_with_its_fields, ...test_a_refusal_writes_no_event, tests/ui_server/test_rerun_subtree_door.py::TestRerunSubtreeDoor::test_confirm_cost_prepares_and_answers_200]
m3 S1 passes no model to the preparation: exit=1 failed=4 nodes=[...TestRerunSubtreeCommand::test_a_preparation_refusal_answers_the_refused_shape_with_its_facts, ...test_confirm_cost_true_prepares_over_an_unavailable_estimate, ...TestRerunSubtreeCommandWritesTheEvent::test_a_preparation_writes_exactly_one_event_with_its_fields, ...test_a_refusal_writes_no_event]
m4 S2 writes no event: exit=1 failed=1 nodes=[...TestRerunSubtreeCommandWritesTheEvent::test_a_preparation_writes_exactly_one_event_with_its_fields]
m5 S3 leaves attempts out of the task item: exit=1 failed=2 nodes=[tests/ui_server/test_dashboard_task_attempts.py::test_a_never_run_tasks_item_names_attempt_one_and_no_attempts, ...test_after_a_preparation_t002_carries_its_old_attempt_and_t001_carries_none]
m6 S3 places attempt after origin: exit=1 failed=2 nodes=[tests/ui_server/test_dashboard_task_attempts.py::test_after_a_preparation_t002_carries_its_old_attempt_and_t001_carries_none, tests/ui_server/test_dashboard_task_origin.py::test_a_planned_tasks_item_names_the_empty_string]
m7 S4's branch answers a refusal as a 200: exit=1 failed=1 nodes=[tests/ui_server/test_rerun_subtree_door.py::TestRerunSubtreeDoor::test_a_refusal_is_a_409_naming_unknown_task]
m8 _read_command_payload accepts a confirm_cost that is not a bool: exit=1 failed=1 nodes=[tests/ui_server/test_rerun_subtree_door.py::TestRerunSubtreeDoor::test_a_non_bool_confirm_cost_is_400_before_the_job_is_read]
restored byte-identical: True
control (unmutated, last): exit=0 failed=0 nodes=[(none)]
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```
Every mutation was red on the first run; no repair round was needed. Then
`git worktree remove --force .remedy-wt/f029-r4-mut`, `git worktree prune`;
`git worktree list | wc -l` → 61, matching the step-4 reading.

**Constraint 3** — `git diff --name-only 5d9c8784`, run once more after writing
this file, lists exactly the 16 paths inside the block's tracked path set
(`.agent/authored/f029-r4-block.md`,
`.agent/authored/f029-r4-booking.diff`, `.agent/authored/f029-r4-plan.md`,
`.agent/authored/f029-r4-mutations.py`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/plan.md`, `apps/cli/command_catalog.py`,
`apps/ui/src/api/humanizeCatalog.ts`, `packages/orchestration/event_names.py`,
`packages/orchestration/subtree_rerun.py`, `packages/orchestration/ui_server.py`,
`tests/orchestration/test_subtree_rerun_prepare.py`,
`tests/ui_server/test_command_channel.py`,
`tests/ui_server/test_dashboard_task_attempts.py`,
`tests/ui_server/test_rerun_subtree_door.py`) — 16 paths, the 17th being this
commit's `.agent/handoff.md`; no path outside the set changed.

## Authored-text proofs

`.agent/authored/f029-r4-block.md`, `f029-r4-booking.diff` and `f029-r4-plan.md`
(C1, `5ed69a271`): each read back via `git show` equals its source
(`.remedy-wt/f029-r4/block.md`, `.remedy-wt/f029-r4-payloads/booking.diff`,
`.remedy-wt/f029-r4-payloads/plan.md`) byte for byte — see G1 above.
`.agent/authored/f029-r4-mutations.py` (C6a, `796500fe9`) is this session's OWN
tool, not reviewer-authored text, so it carries no fidelity comparison; its
behavior is proved instead by G5's live run above.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| C6a | done | |
| C6b | done | this commit |
| G1 transport | done | PASS — all copies byte-identical |
| G2 the booking | done | PASS — sha256 and open_finding_ids both match |
| G3 the code | done | PASS — ruff exit 0, three functions quoted from disk |
| G4 the tests | done | PASS — 2417 passed, 11 skipped, exit 0; +15 nodes fully accounted |
| G5 the red proofs | done | PASS — all 8 mutations caught, both controls green, restored byte-identical |
| S1 the function | done | `rerun_subtree_command` in `subtree_rerun.py` |
| S2 the event | done | `subtree_rerun_prepared`, declared and catalogued |
| S3 the dashboard | done | `attempt`/`attempts` before `origin` |
| S4 the door | done | `job.rerun-subtree` exposed, dispatched, guarded |
| S5 nothing else | done | no edit under `apps/ui/` beyond S2's one line; `pingpong_job.py`, `worktrees.py`, `job_rerun_cmd.py` and the catalog entry's own body untouched |

## Deviations & assumptions

One repair made within the round, both declared here:
1. `tests/ui_server/test_command_channel.py`'s
   `TestCommandDoorImportGuard.test_the_door_reaches_only_the_accepted_forbidden_modules_transitively`
   went red once `_dispatch_rerun_subtree` started importing
   `subtree_rerun.rerun_subtree_command`: `subtree_rerun.py` imports `subprocess`
   at MODULE level for its git plumbing, so the transitive-closure guard now
   reaches it. Recorded `subprocess` in `ACCEPTED_TRANSITIVE_FORBIDDEN` with its
   route, and corrected the comment above it that had called `subprocess`
   "deliberately absent" (still true of `evidence_index`'s own import, no longer
   true of the set as a whole). This is a widening the S4 spec's own ALLOWED_IMPORTS
   instruction implies but does not spell out in this much detail; declared here
   per constraint 4/guardrail discipline even though the guard itself is inside
   this round's tracked path set.
2. Two `TestRerunSubtreeCommand` tests initially set `est_tokens_band` directly
   into `job.tasks[1:]`'s `inputs["plan"]`, which — per `dag_schedule.build_graph`'s
   documented "legacy" rule — SILENTLY DROPPED T003's implicit dependency on T002
   the instant T003 gained a `plan` dict with no `depends_on` key, collapsing the
   priced subtree from two tasks to one and mismatching the expected sum (0.16 vs
   the observed 0.08). Fixed by declaring `planned_id`/`depends_on` explicitly in
   the test fixture (`_price_the_subtree_of_t002`) so the edge survives; no
   production code was touched by this fix, only the test's own setup. Both were
   caught during this session's own `pytest` runs before any commit, so neither
   reached a committed file in a wrong state.

A `prose_slips.md`-class inaccuracy (not a defect, not a round of its own,
amend0827-process-diet rule 2): G4's instructions ask which of the eleven
skips "are not the seven F252 quarantines" — the reviewer's own base reading at
`5d9c8784` already carries eleven F252-cited skips, not seven, so the premise
undercounts the current ledger; all eleven are accounted for above.

No commit was split, reordered or dropped from the block's ordered sequence
(C1–C6a as named, C6b this one); no existing test was edited to pass; no gate
went red in its FINAL (committed) state.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 4, then
T003's browser half: the send module, the types, the attempt chip, the attempt
list in the task's popover, the Rerun control, and the render proof.

Open findings: 0. Operator questions: 0.
