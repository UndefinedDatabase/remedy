# Handback — F025 Pause/resume (global & per node) · Round 4

## Session

SESSION 1 of feature F025 · round 4 · rounds so far 4

Roughly a third of the context budget remained at the point this handback was written; the round
booked round 3's PASS and resolutions, then landed T002 whole — the catalog, the CLI, the shared
effects, the door and its audit, the docs, a 39-test CLI file, a 6-test live-door file and an
8-mutation red-proof tool. One real conflict surfaced and was resolved: the catalog id `job.pause`
collided with a word `tests/test_command_catalog.py`'s `TestDeletedCommands.DELETED` pinned as
never-to-return from an unrelated F261 cleanup; removed with a docstring recording why (Deviations
#2). One environment hazard was found and closed before it could run npm from inside this session:
G5's fresh worktree makes `apps/ui/src/*` look newer than the primary checkout's already-built
`dist/`, which the write door's own auto-build check reads as "stale" and tries to rebuild — the
mutation tool now copies (not symlinks) a fresh `dist/` and sets `REMEDY_UI_NO_AUTO_BUILD=1` so
that never fires (Deviations #6).

## Range

Review of 62e43ee88..HEAD

## Commits

### bb522981e F025 R4 C1a: copy round 4 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r4-block.md | +208/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r4-d2.md | +49/-0 | copy of the d2.md payload (DECISION F025 D2) |
| .agent/authored/f025-r4-ledger.md | +6/-0 | copy of the ledger.md payload |
| .agent/authored/f025-r4-plan.md | +33/-0 | copy of the plan.md payload |
| .agent/authored/f025-r4-q4.md | +25/-0 | copy of the q4.md payload (operator question Q4) |

321 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 208, plus 113: 49+6+33+25 = 113) — matches exactly.

### c99a9a5bc F025 R4 C1b: book round 3, resolve R-1049 and R-1050, record D2 and operator question Q4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +49/-0 | d2.md appended (bytes to bytes) |
| .agent/live_review.md | +6/-0 | ledger.md appended (bytes to bytes) |
| .agent/operator_questions.md | +25/-0 | q4.md appended (bytes to bytes) |
| .agent/plan.md | +11/-13 | rewritten whole to the plan.md payload |

49/0, 6/0, 25/0, 11/13 — matches the block's stated expectation exactly.

### 9c8aea963 F025 R4 C2: the shared pause/unpause effects and the task-pause event registries
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pause_control.py | +157/-0 | new S6 section (P2): `pause_job_command`/`unpause_job_command`, `_refuse_unknown_task`, `_write_task_paused_event`/`_write_task_resumed_event` (each an inline literal `RunLogWriter.log(...)` call, D2 clause 3), `_job_state_str`/`_job_task_ids` helpers, `_TERMINAL_STATES`/`_PARKED_STATE`; both new functions and `PauseControlError` etc. added to `__all__` |
| packages/orchestration/event_names.py | +2/-0 | `task_paused`/`task_resumed` join `EVENT_NAMES` (P5), same commit as their writer so no declared name is ever unused |
| apps/ui/src/api/humanizeCatalog.ts | +2/-0 | `task_paused`/`task_resumed` entries (P5), alphabetically placed |

161 insertions, under the cap. Ordered ahead of C3 (the catalog and CLI): job_pause_cmd.py imports
`pause_job_command`/`unpause_job_command` from this commit — see Deviations #1.

### 706f66aff F025 R4 C3: job.pause and job.unpause in the catalog and the CLI
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +42/-0 | two `CommandEntry` rows (P1): `job.pause` (job_id, --task, --reason, --source, --json) and `job.unpause` (job_id, --task, --source, --json), both `write_metadata`, exit_codes (0,1,2,3); both added to `UI_EXPOSED_COMMANDS` with a comment citing DECISION F025 D2 |
| apps/cli/commands/job_pause_cmd.py | +160/-0 | NEW FILE (P3), modelled on `job_stop_cmd.py`: `_resolve_job_id` (validate + prefix lookup, mirrors job_stop's inline logic), `_cmd_job_pause`/`_cmd_job_unpause` calling the C2 effects, `COMMAND_HANDLERS` for both ids |
| apps/cli/commands/__init__.py | +2/-1 | `job_pause_cmd` imported and folded into `collect_all_handlers`'s module tuple |
| tests/test_command_catalog.py | +6/-1 | `TestDeletedCommands.DELETED` drops `"job.pause"`, with a docstring paragraph recording why (Deviations #2) |
| tests/cli/test_job_refusal_envelope.py | +3/-1 | `_LOOKUP_CALLERS` gains `"job_pause_cmd.py": 1`, for its own `lookup_job_id` call site |
| tests/ui_server/test_command_channel.py | +4/-3 | `TestUiExposedCommands`'s exact-set assertion gains `job.pause`/`job.unpause` |

217 insertions, under the cap. Two tests stay red until their own commits land (see the commit
message, quoted in Verification): the exit-codes guide (C5) and the door's per-command dispatch
loop (C4).

### ce55bb347 F025 R4 C4: the door dispatches job.pause and job.unpause
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +100/-0 | a clause each for `job.pause`/`job.unpause` in `_handle_command_submission`, in D18's write order (effect, audit, publication); `_dispatch_job_pause`/`_dispatch_job_unpause` (P4); `JOB_PAUSE_COMMAND_ID`/`JOB_UNPAUSE_COMMAND_ID`/`COMMAND_PAUSE_STATE_MESSAGE` constants; a `refused` outcome takes 409/`rejected_state`, a raised effect keeps 500/`rejected_effect` |
| tests/ui_server/test_command_channel.py | +16/-0 | `DOOR_METHODS` gains the two dispatch methods, `ALLOWED_IMPORTS` gains the two `pause_control` names (each commented `# F025 D2`); the per-command dispatch-answer loop gains `job.pause`/`job.unpause` branches |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | `apps.cli.commands.job_pause_cmd`, reachable from the job path entry point since C3 registered it — see Deviations #5 |

117 insertions, under the cap.

### f85426246 F025 R4 C5: job pause/unpause in the exit-codes guide
| Path | +/- | Reason |
|---|---|---|
| docs/guides/exit-codes.md | +2/-0 | two rows in the per-command table (P6): `remedy job pause` and `remedy job unpause`, both exit codes 3 (above the floor), beside `remedy job stop` |

2 insertions, under the cap.

### 520643eb8 F025 R4 C6: test job.pause and job.unpause through the CLI (T1)
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_pause.py | +407/-0 | NEW FILE (T1), modelled on `test_job_stop.py`: every P2 outcome through the handlers with `--json`, idempotence, the task-pause/task-release events written exactly once (and not at all on a repeat), exit 2/3, exit 1 with the named state/task, the parked-job relaunch line, and catalog/handler/parser wiring |

407 insertions, under the cap. 39 tests collected (confirmed under G3).

### 1c38cb643 F025 R4 C7: test job.pause and job.unpause through the real door, live (T2)
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_pause_door_live.py | +499/-0 | NEW FILE (T2): `TestJobScopeLiveDoor` (L1) and `TestTaskScopeLiveDoor` (L2) run a fake-provider job in its own process (the `test_job_stop_integration.py` live-runner pattern) with an in-process UI server sharing `REMEDY_DATA_DIR`, driven through real HTTP; `TestRefusalsLiveDoor` (L3) and `TestWithdrawLiveDoor` (L4) need no live runner |

499 insertions — under the 500 cap by one line; the module docstring was rewrapped tighter to fit
after an initial draft measured 501 (caught before committing, not a deviation). 6 tests collected
(confirmed under G3).

### 882154601 F025 R4 C8: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r4-mutations.py | +307/-0 | the G5 tool: m1 (ui_server.py), m2–m6 (pause_control.py), m7 (ui_server.py), m8 (job_pause_cmd.py), each a single-occurrence FROM/TO pair verified before this commit; symlinks `apps/ui/node_modules` and COPIES (not symlinks) a freshly-mtimed `apps/ui/dist` into the worktree, and sets `REMEDY_UI_NO_AUTO_BUILD=1` for every test run, so the live-runner tests' `start_ui_server` never has a reason to attempt an npm build (Deviations #6) |

307 insertions, under the cap.

### (this commit) F025 R4 C9: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f025-r4-mut-dryrun HEAD` (at C7's HEAD `1c38cb643`, before
  the mutation tool was committed) — succeeded; a pre-commit dry run of the DRAFT tool
  (`.remedy-wt/f025-r4-worker/mutations_draft.py`, never committed under that name) to prove it
  before C8. Its FIRST dry run built a real `apps/ui/dist` via npm inside the worktree — the
  environment hazard Deviations #6 describes — caught here, before any committed artifact existed.
- `git worktree remove --force .remedy-wt/f025-r4-mut-dryrun` — succeeded, after that first dry run.
- `git worktree add --detach .remedy-wt/f025-r4-mut-dryrun HEAD` — succeeded, a second dry run
  after the fix (symlinked node_modules, copied+bumped dist, `REMEDY_UI_NO_AUTO_BUILD=1`): clean,
  no npm invoked, all mutations caught.
- `git worktree remove --force .remedy-wt/f025-r4-mut-dryrun` — succeeded.
- `git worktree add --detach .remedy-wt/f025-r4-mut 882154601` (C8's HEAD) — succeeded, for G5's
  one official run against the committed tool.
- `git worktree remove --force .remedy-wt/f025-r4-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees named in constraint 5 — nothing new left behind.
- `git push origin feature/f025-pause-resume` — runs immediately after this commit (C9); its real
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
62e43ee88 F025 R3 C7: rewrite handoff for round 3
```

```
$ (line count and sha256 of .remedy-wt/f025-r4/block.md, measured)
line_count: 208
sha256: 6040a772849c474245d517ffdb821f602a855fccb94fb939c4d8b0052c5fff07
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list   (as found, before this round touched anything)
```
Listed the primary checkout at `feature/f025-pause-resume`/`62e43ee88`, every `f015-*`/`f020-*`/
`f023-*`/`f024-*`/`f025-*`/`f284-*` round worktree already on disk (including `f025-r1-dry`,
`f025-r2-sim`, `f025-r3-sim`, `f025-r4-sim`), and four `job-*` worktrees — all left untouched all
round.

### PAYLOADS table
```
$ (python: newline count, byte count, sha256 of each payload)
d2.md     lines=49 bytes=4324 sha256=2a4cb7e224ede77e05fef88b9b4b990974724dc08ff1d3f38813c48c6758eca3
ledger.md lines=6  bytes=4199 sha256=b906f739fdf6eb9ea9c96bfa4ee2f3e18848551d28ce606063a777eb2518879a
plan.md   lines=33 bytes=1155 sha256=7f428ae0fb39c8e2c58850c33eabc559c653a91cf1f3321892c51de2f77d4061
q4.md     lines=25 bytes=1845 sha256=ce9bf59e31b6ee4333d67336949806fd8a98793c44f080079c72ff948b090275
```
All 4 match the PAYLOADS table exactly (G1).

### G1 — transport
```
$ (python: each committed .agent/authored/f025-r4-* copy, read via `git show bb522981e:<path>`,
   compared byte for byte against its source)
.agent/authored/f025-r4-block.md  == .remedy-wt/f025-r4/block.md  : True
.agent/authored/f025-r4-d2.md     == .remedy-wt/f025-r4/d2.md     : True
.agent/authored/f025-r4-ledger.md == .remedy-wt/f025-r4/ledger.md : True
.agent/authored/f025-r4-plan.md   == .remedy-wt/f025-r4/plan.md   : True
.agent/authored/f025-r4-q4.md     == .remedy-wt/f025-r4/q4.md     : True
```
```
$ (bytes comparison: C1b's .agent/decisions.md vs 62e43ee8's bytes + d2.md)
decisions match:  True
$ (bytes comparison: C1b's .agent/live_review.md vs 62e43ee8's bytes + ledger.md)
live_review match:  True
$ (bytes comparison: C1b's .agent/operator_questions.md vs 62e43ee8's bytes + q4.md)
operator_questions match:  True
$ (bytes comparison: C1b's .agent/plan.md vs plan.md payload)
plan match:  True
```
```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over C1b's .agent/live_review.md
['R-1008']
```
Matches the block's stated reading exactly.

### G2 — the code
```
$ python3 -m ruff check .agent/authored/f025-r4-mutations.py apps/cli/command_catalog.py \
  apps/cli/commands/__init__.py apps/cli/commands/job_pause_cmd.py \
  packages/orchestration/event_names.py packages/orchestration/pause_control.py \
  packages/orchestration/ui_server.py tests/cli/test_job_pause.py \
  tests/cli/test_job_refusal_envelope.py tests/test_command_catalog.py \
  tests/ui_server/test_command_channel.py tests/ui_server/test_pause_door_live.py
All checks passed!
```
```
$ git diff --stat 62e43ee8 882154601 -- packages/orchestration/safe_points.py \
  packages/orchestration/pingpong_job.py packages/orchestration/pingpong_loop.py \
  packages/orchestration/long_run_executor.py packages/common/secure_fs.py
(empty)
```
Confirmed empty — none of the five forbidden files touched.
```
$ git diff 62e43ee8 882154601 -- packages apps scripts | grep "^+" | grep -c "noqa: BLE001"
0
```
```
$ git diff --name-only c99a9a5bc 882154601
.agent/authored/f025-r4-mutations.py
apps/cli/command_catalog.py
apps/cli/commands/__init__.py
apps/cli/commands/job_pause_cmd.py
apps/ui/src/api/humanizeCatalog.ts
docs/guides/exit-codes.md
packages/orchestration/event_names.py
packages/orchestration/pause_control.py
packages/orchestration/ui_server.py
tests/cli/test_job_pause.py
tests/cli/test_job_refusal_envelope.py
tests/orchestration/import_reachability_allowlist.txt
tests/test_command_catalog.py
tests/ui_server/test_command_channel.py
tests/ui_server/test_pause_door_live.py
```
Every path is inside constraint 3's set — the four widened existing files
(`tests/test_command_catalog.py`, `tests/cli/test_job_refusal_envelope.py`,
`tests/ui_server/test_command_channel.py`, `tests/orchestration/import_reachability_allowlist.txt`)
are each named above with what they widened.

### G3 — the new tests, serially
```
$ python3 -m pytest -q -p no:cacheprovider tests/cli/test_job_pause.py \
  tests/ui_server/test_pause_door_live.py tests/ui_server/test_command_channel.py \
  tests/ui_server/test_command_dispatch.py
........................................................................ [ 38%]
........................................................................ [ 77%]
..........................................                               [100%]
186 passed in 17.26s
REAL_EXIT=0
```
```
$ python3 -m pytest --collect-only -q tests/cli/test_job_pause.py
39 tests collected
$ python3 -m pytest --collect-only -q tests/ui_server/test_pause_door_live.py
6 tests collected
```

### G4 — the neighbours
```
$ python3 .remedy-wt/f025-r4/run_sel.py /home/decodeux/Repos/remedy 8
files 144 exit 0 wall 188 s
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in ...
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257: UI source not found
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
8766 passed, 9 skipped in 187.97s (0:03:07)
```
Exit 0, 0 failed. The block's own baseline named 6 `tests/cli/test_study_cmd.py` nodes as flaky
under this specific combined-worker ordering at `62e43ee8`/`49624d5c8`; THIS run shows zero
failures — an ordering-luck outcome of xdist's own work distribution, not a regression either way.
Since nothing failed, the "re-run every failing node's FILE alone, serially" step has nothing to
do: no bad node exists to re-run.
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
$ git worktree add --detach .remedy-wt/f025-r4-mut 882154601
$ python3 -B .agent/authored/f025-r4-mutations.py .../f025-r4-mut
/.../apps/ui/node_modules: symlinked from the primary checkout
/.../apps/ui/dist: copied from the primary checkout, mtimes bumped +60s
control (before): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
m1: the door's pause ignores args.task and always pauses the job -- exit=1 failed=2 failing_node_ids=[tests/ui_server/test_pause_door_live.py::TestTaskScopeLiveDoor::test_pause_withholds_one_task_and_unpause_releases_it, tests/ui_server/test_pause_door_live.py::TestRefusalsLiveDoor::test_an_unknown_task_is_409_and_audited_rejected_state]
m1: restored byte-identical: True (packages/orchestration/ui_server.py)
m2: the terminal-state refusal is removed from pause_job_command -- exit=1 failed=3 failing_node_ids=[tests/cli/test_job_pause.py::TestJobScopePause::test_a_completed_job_is_refused_with_its_state_named, tests/cli/test_job_pause.py::TestJobScopePause::test_a_completed_job_says_so_in_json_too, tests/ui_server/test_pause_door_live.py::TestRefusalsLiveDoor::test_a_completed_job_is_409_and_audited_rejected_state]
m2: restored byte-identical: True (packages/orchestration/pause_control.py)
m3: a task id the plan does not hold is accepted -- exit=1 failed=4 failing_node_ids=[tests/cli/test_job_pause.py::TestTaskScopePause::test_an_unknown_task_is_refused_with_the_task_named, tests/cli/test_job_pause.py::TestTaskScopePause::test_an_unknown_task_is_refused_without_json_too, tests/cli/test_job_pause.py::TestTaskScopeUnpause::test_an_unknown_task_is_refused_with_the_task_named, tests/ui_server/test_pause_door_live.py::TestRefusalsLiveDoor::test_an_unknown_task_is_409_and_audited_rejected_state]
m3: restored byte-identical: True (packages/orchestration/pause_control.py)
m4: unpause_job_command on a parked job answers not_paused -- exit=1 failed=2 failing_node_ids=[tests/cli/test_job_pause.py::TestJobScopeUnpause::test_a_parked_job_answers_parked_with_the_relaunch_command, tests/ui_server/test_pause_door_live.py::TestJobScopeLiveDoor::test_pause_parks_the_job_and_unpause_names_the_relaunch]
m4: restored byte-identical: True (packages/orchestration/pause_control.py)
m5: task_paused is written on every call, not only when the entry is created -- exit=1 failed=1 failing_node_ids=[tests/cli/test_job_pause.py::TestTaskScopePause::test_pausing_the_same_task_twice_writes_the_event_exactly_once]
m5: restored byte-identical: True (packages/orchestration/pause_control.py)
m6: task_resumed is never written -- exit=1 failed=3 failing_node_ids=[tests/cli/test_job_pause.py::TestTaskScopeUnpause::test_releasing_a_paused_task_writes_one_task_resumed_event, tests/cli/test_job_pause.py::TestTaskScopeUnpause::test_releasing_twice_writes_the_event_exactly_once, tests/ui_server/test_pause_door_live.py::TestTaskScopeLiveDoor::test_pause_withholds_one_task_and_unpause_releases_it]
m6: restored byte-identical: True (packages/orchestration/pause_control.py)
m7: the door answers a refused outcome 500 rejected_effect instead of 409 rejected_state -- exit=1 failed=2 failing_node_ids=[tests/ui_server/test_pause_door_live.py::TestRefusalsLiveDoor::test_an_unknown_task_is_409_and_audited_rejected_state, tests/ui_server/test_pause_door_live.py::TestRefusalsLiveDoor::test_a_completed_job_is_409_and_audited_rejected_state]
m7: restored byte-identical: True (packages/orchestration/ui_server.py)
m8: the CLI exits 0 on a refused outcome -- exit=1 failed=4 failing_node_ids=[tests/cli/test_job_pause.py::TestJobScopePause::test_a_completed_job_is_refused_with_its_state_named, tests/cli/test_job_pause.py::TestJobScopePause::test_a_completed_job_says_so_in_json_too, tests/cli/test_job_pause.py::TestTaskScopePause::test_an_unknown_task_is_refused_with_the_task_named, tests/cli/test_job_pause.py::TestTaskScopePause::test_an_unknown_task_is_refused_without_json_too]
m8: restored byte-identical: True (apps/cli/commands/job_pause_cmd.py)
control (after): unmutated control run -- exit=0 failed=0 failing_node_ids=[(none)]
packages/orchestration/pause_control.py: restored byte-identical: True
packages/orchestration/ui_server.py: restored byte-identical: True
apps/cli/commands/job_pause_cmd.py: restored byte-identical: True
/.../apps/ui/node_modules: removed
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f025-r4-mut
$ git worktree prune
$ git worktree list
(primary + the pre-existing set only; f025-r4-mut gone)
```
Every one of the 8 mutations is red with at least one failing node id; every restore is
byte-identical for all three target files; no npm process ever ran (Deviations #6); the tool's own
final line reads `True`.

### G6 — tree and push (readings go in the final reply, after C9)

## Authored-text proofs

`.agent/authored/f025-r4-block.md`, `f025-r4-d2.md`, `f025-r4-ledger.md`, `f025-r4-plan.md` and
`f025-r4-q4.md` were built with `shutil.copyfile` from the reviewer's payload files — never
retyped, never edited — and G1 compared every one byte for byte, read back with `git show
bb522981e:<path>`, against its source: all five BYTE-IDENTICAL. `.agent/decisions.md`,
`.agent/live_review.md` and `.agent/operator_questions.md` were appended with raw bytes read from
`d2.md`/`ledger.md`/`q4.md` (`Path.write_bytes(before + payload)`), never retyped;
`.agent/plan.md` was rewritten whole from `plan.md`'s bytes. G1's byte-comparisons confirm all four
match the payloads exactly. `packages/orchestration/pause_control.py`,
`packages/orchestration/ui_server.py`, `apps/cli/command_catalog.py`,
`apps/cli/commands/job_pause_cmd.py`, `apps/cli/commands/__init__.py`,
`packages/orchestration/event_names.py`, `apps/ui/src/api/humanizeCatalog.ts`,
`docs/guides/exit-codes.md`, `tests/cli/test_job_pause.py`,
`tests/ui_server/test_pause_door_live.py`, `.agent/authored/f025-r4-mutations.py` and the four
widened existing test/generated-list files are WORKER-authored production code, tests, docs and the
G5 tool per the block's P1–P7/T1–T2 specification — not reviewer payloads — so no authored-text
proof applies to them.

## Deviations & assumptions

1. **C2/C3 reordered from the block's own labels.** The block names "C2 THE CATALOG AND THE CLI
   (P1, P3)" before "C3 THE EFFECTS AND THE REGISTRIES (P2, P5)" but explicitly says "Order C2 and
   C3 as your imports require" — `job_pause_cmd.py` (P3) imports `pause_job_command`/
   `unpause_job_command` (P2), so committing the catalog/CLI content before the effects existed
   would leave that commit's own imports unresolved. This handback keeps the block's C2/C3 LABELS
   attached to their CONTENT (catalog/CLI is still called C2 in the block's own vocabulary) but
   commits the effects content FIRST in the actual sequence — the commit table and the item-status
   table both name what each commit really contains, so nothing here is hidden, only the two
   labels' relative position, which the block itself authorized swapping.
2. **`tests/test_command_catalog.py`'s `DELETED` tuple loses `"job.pause"`.** F261 deleted a
   command by that id for reasons unrelated to F025; DECISION F025 D2 explicitly re-mints the exact
   word `job.pause` for this feature's job-scope/task-scope pause. Searched the repository
   (`grep -rn '"job\.pause"'`) before removing it: no other file still expects the old meaning. A
   docstring paragraph was added to `TestDeletedCommands` recording why the word is deliberately
   absent rather than merely omitted, and citing this decision as the record a later reader can
   check the removal against — the same rigor constraint 3 asks of an ADDITION to a pinned set,
   applied to a removal from one.
3. **Three more existing tests widened, each narrowly, named per constraint 3:**
   `tests/cli/test_job_refusal_envelope.py`'s `_LOOKUP_CALLERS` gains `"job_pause_cmd.py": 1`;
   `tests/ui_server/test_command_channel.py` widened TWICE — in C3 (`TestUiExposedCommands`'s
   exact-set list) and again in C4 (`DOOR_METHODS`, `ALLOWED_IMPORTS`, and the per-command
   dispatch-answer loop, which also needed a docstring note: `job.pause` and `job.unpause` share
   ONE test job and ONE loop iteration order, so the pause requested by the `job.pause` iteration is
   still pending by the time `job.unpause`'s turn comes, and that iteration answers `withdrawn`
   rather than `not_paused` — caught by running the test rather than assumed).
4. **`tests/orchestration/import_reachability_allowlist.txt` widened, folded into C4 rather than
   C3.** `apps.cli.commands.job_pause_cmd` became reachable from the job-path entry point the
   moment C3 registered it in `collect_all_handlers`, but the fuller sweep that catches this
   (`tests/orchestration/test_import_reachability.py`) only ran once, ahead of C4's own broader test
   pass — so the fix travels with C4's commit rather than amending C3. Named here per the "an extra
   [or relocated] finding-fix is a deviation even when correct" rule.
5. **The accepted body's `outcome` field is not the literal `"accepted"` D18's other clauses
   share.** DECISION F009 D18's FIRST clause states the general shape `{"command": <id>, "outcome":
   "accepted", ...}`; DECISION F025 D2 clause 2 rules a CLOSED, more specific outcome vocabulary
   for `job.pause`/`job.unpause` themselves — `requested`, `paused`, `released`, `withdrawn`,
   `parked`, `not_paused` — and P4 does not say to wrap that in a second, generic `"accepted"`
   token. The dispatch methods return `{"command": payload["command"], **result}`, so the wire
   `outcome` is whichever of D2's own tokens the effect produced; a client reading the body sees
   what actually happened rather than the word "accepted" beside a `next` field or a `task_id` it
   would then have to interpret anyway. `_handle_command_submission`'s own audit line still writes
   the literal `accepted`/`rejected_state` tokens D6 requires, unchanged from every other clause.
6. **G5's mutation tool copies `apps/ui/dist` and disables UI auto-build — an environment fix, not
   a product one.** `start_ui_server` (`_load_frontend`) pre-renders the React shell at STARTUP and
   auto-builds it via npm when `apps/ui/dist/` is missing or STALE relative to `apps/ui/src/`. A
   fresh `git worktree add` checkout gives every `apps/ui/src/*` file a "now" mtime, always newer
   than the primary checkout's already-built `dist/index.html`, so the staleness check fires even
   though nothing in `apps/ui/src` actually changed — discovered when the FIRST dry run of the
   draft tool (before C8 was committed, see External actions) genuinely built a fresh `dist/` via
   npm inside a throwaway worktree. Symlinking `apps/ui/node_modules` alone (G5's own literal
   instruction) does not prevent this, because the staleness check never gets far enough to need
   `node_modules` — it decides to rebuild before `npm install` ever runs. The tool now ALSO copies
   (not symlinks — a symlink's `stat()` would report the PRIMARY's older build time) `apps/ui/dist`
   into the worktree and bumps its files' mtimes 60 seconds into the future, and sets
   `REMEDY_UI_NO_AUTO_BUILD=1` for every pytest invocation as a third, independent guard. Re-run
   confirmed clean: no npm process started, all 8 mutations caught. This is scoped to the mutation
   tool alone; neither live-door test file needed any change, since the primary checkout (where G3
   and G4 run) already carries a fresh, non-stale `dist/`.
7. **`--task`'s resolution is exact match, not the planned-id-or-prefix `_TASK_OPT` promises
   elsewhere.** `job.context`'s `--task` (and its catalog shorthand `_TASK_OPT`) resolves a planned
   id (`T001`) or a task-id prefix via `resolve_task_for_context`. D2 does not ask for that, and the
   door cannot perform it without importing a CLI-only resolver its guard forbids — parity between
   the CLI and the door (both call the SAME `pause_control` functions) would break if only the CLI
   resolved prefixes. `pause_job_command`/`unpause_job_command` instead match `task_id` EXACTLY
   against `job.tasks[i].task_id` — the same internal id `remedy job plan-show` prints and T2's live
   tests pass straight through (`job.tasks[2].task_id`) — and the catalog's own `--task` help text
   for these two commands says so ("by its id as `remedy job plan-show` prints it") rather than
   reusing `_TASK_OPT`'s "planned id (T001) or task-id prefix" wording, which would promise
   resolution this feature does not perform.
8. **G4 found 0 failed, not the block's own named 6.** The block's baseline reading at `62e43ee8`/
   `49624d5c8` names 6 `tests/cli/test_study_cmd.py` nodes as flaky under this specific
   xdist-worker ordering. This round's run shows `8766 passed, 9 skipped`, zero failed — an
   ordering-luck artifact of how 8 workers happened to distribute 144 files' worth of tests this
   time, not a fix and not a regression. Since nothing failed, no serial per-file re-run was
   needed or performed.
9. **No full-suite run.** Per constraint 6 (amend0917-throughput), only G4's targeted selection
   ran; the one full-suite run per feature belongs to F025's closure, not this round.

No payload was edited or retyped. No production file outside `packages/orchestration/pause_control.py`,
`packages/orchestration/ui_server.py`, `packages/orchestration/event_names.py`,
`apps/cli/command_catalog.py`, `apps/cli/commands/job_pause_cmd.py`, `apps/cli/commands/__init__.py`,
`apps/ui/src/api/humanizeCatalog.ts` and `docs/guides/exit-codes.md` was touched;
`safe_points.py`, `pingpong_job.py`, `pingpong_loop.py`, `long_run_executor.py` and `secure_fs.py`
are confirmed untouched by G2's `git diff --stat`. The worktrees this round created
(`.remedy-wt/f025-r4-mut-dryrun` twice, `.remedy-wt/f025-r4-mut` once) were each removed the same
round, per constraint 5; every pre-existing worktree and stash was left alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 321 insertions, matches the block's expectation (208+113) exactly |
| C1b | done | 49/0, 6/0, 25/0, 11/13 insertions, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008']` |
| C2 | done | 161 insertions; P2's shared effects and P5's event registries landed together; committed ahead of C3 per Deviations #1 |
| C3 | done | 217 insertions; P1's catalog rows and P3's new CLI file landed, plus three narrow existing-test widenings (Deviations #2, #3) |
| C4 | done | 117 insertions; P4's door clauses and dispatch methods landed, plus the import-guard/allowlist widenings (Deviations #3, #4) |
| C5 | done | 2 insertions; P6's two guide rows landed |
| C6 | done | 407 insertions; T1's 39-test CLI file landed |
| C7 | done | 499 insertions; T2's 6-test live-door file landed |
| C8 | done | 307 insertions; the G5 tool landed, with the npm-avoidance guards Deviations #6 describes |
| C9 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical; open-finding set matched |
| G2 | done | ruff clean over every changed .py file; forbidden files untouched; noqa:BLE001 added = 0; name-only diff exactly inside constraint 3 |
| G3 | done | 186 passed (39+6+…), exit 0; collect-only counts 39 and 6 for the two new files |
| G4 | done | 8766 passed, 9 skipped, exit 0, 0 failed (see Deviations #8); integrity check 6/6 pass |
| G5 | done | all 8 mutations caught, all restores byte-identical, `True`; two pre-commit dry runs closed an environment hazard first (Deviations #6) |
| G6 | done | reported in the final reply, after C9 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 4. Then T003 — the paused
states, the banner, the NowCard line, the browser's pause and resume, and the end-to-end against an
unpaused control run. Open findings: 1 (`R-1008`, owned by F285) — the count `open_finding_ids`
reads at C1b. Operator questions open: 4.
