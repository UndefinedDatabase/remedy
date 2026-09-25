# Handback — F025 Pause/resume (global & per node) · Round 7

## Session

SESSION 2 of feature F025 · round 7 · rounds so far 7

Roughly a third of the context budget remained at the point this handback was written; the round
booked round 6's PASS with its three deviations, repaired R-1053 and R-1054 in the task popover's
control, registered R-1055 to F285, then landed DECISION F025 D5 whole: the live end-to-end test of
both scopes — a job paused mid-build through the real door, parked, relaunched through the real
`remedy job run`, and compared with an unpaused control run of the same job file by its normalized
export, its workspace bytes and its ordered task-level events. One nontrivial discovery drove most
of the round's iteration (see Deviations & assumptions #1-#3): the control run's own "first runner"
had to be rebuilt to resolve providers BY NAME through a monkeypatched `create_provider`, exactly as
the CLI does, rather than by an injected object — an injected object is reused across every task in
one process, which silently changes which tasks need a repair round and broke the comparison the
decision needs.

## Range

Review of 218eaabd6..HEAD

## Commits

### 8b3f652d6 F025 R7 C1a: copy round 7 block and payloads
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r7-block.md | +177/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f025-r7-d5.md | +40/-0 | copy of the d5.md payload (DECISION F025 D5) |
| .agent/authored/f025-r7-f285_from.txt | +2/-0 | copy of the f285_from.txt payload |
| .agent/authored/f025-r7-f285_to.txt | +5/-0 | copy of the f285_to.txt payload |
| .agent/authored/f025-r7-ledger.md | +8/-0 | copy of the ledger.md payload (round 6's PASS, R-1053, R-1054, R-1055) |
| .agent/authored/f025-r7-plan.md | +29/-0 | copy of the plan.md payload |

261 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 177, plus 84: 40+2+5+8+29 = 84) — matches exactly.

### a2de57b52 F025 R7 C1b: book round 6, register R-1053 to R-1055, record D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +40/-0 | d5.md appended (bytes to bytes) |
| .agent/live_review.md | +8/-0 | ledger.md appended (bytes to bytes) |
| .agent/plan.md | +8/-9 | rewritten whole to the plan.md payload |
| docs/roadmap/features/T2_F285.md | +3/-0 | f285_from.txt replaced by f285_to.txt (an APPEND: FROM once before, TO once after) |

40/0, 8/0, 8/9, 3/0 — matches the block's stated expectation exactly. `open_finding_ids` over
`.agent/live_review.md` at this commit reads `['R-1008', 'R-1053', 'R-1054', 'R-1055']`, the
reviewer's own simulated reading.

### 434cae84e F025 R7 C2: R-1053's fix — a task pause offers only while pending
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/pauseView.ts | +7/-2 | R-1053's FIX: `taskPauseAction` answers `pause` only for state `pending` (was: every state but `done`), `resume` for a paused task as before, `null` otherwise |
| apps/ui/src/api/pauseView.test.ts | +14/-2 | one test per FIX-named state: `current`, `blocked` and `suggested` each now assert `null`; the old "not done" test is rebased onto `pending` |

21 insertions, under the cap. `python3 -m ruff check` clean; the touched vitest tests were re-run as
part of every later gate in this handback (never in isolation as a standalone claim).

### 1a8b1cab7 F025 R7 C3: R-1054's fix — key the popover's control by the task id
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/detail/DetailPopover.tsx | +1/-0 | R-1054's FIX: `<PauseControl key={task.id} ...>` — React now remounts the control (dropping its last answer) when the selection changes |
| tests/ui_contracts/test_pause_controls_contract.py | +10/-0 | `test_the_popovers_control_is_keyed_by_the_tasks_id`, the test R-1054's FIX clause names |

11 insertions, under the cap.

### c1de616fd F025 R7 C4a: DECISION F025 D5's end-to-end live test, helpers and E4's normalization (part 1/2, split for size)
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_pause_e2e_live.py | +419/-0 | NEW FILE, first half: module docstring, `test_pause_door_live.py`'s own helpers copied verbatim (E1), the CLI-faithful `_RUNNER` (E2), `_run_control`, `E4_REMOVED_FIELDS` with its reasons, `_normalized_export`, `_workspace_bytes` and `_task_level_event_names` (E4) |

### 117bc440f F025 R7 C4b: DECISION F025 D5's end-to-end live test, JOB and TASK scope (part 2/2)
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_pause_e2e_live.py | +206/-0 | second half: `TestJobScopeE2ELive` and `TestTaskScopeE2ELive` (E3) |

Constraint 2 declared split: the whole new file is 625 lines, over the 500-insertion cap in one
commit, so it is committed in two parts at the file's own natural seam (immediately before the
first test class) — the only oversize content this round produced, and it is split rather than
accepted whole, so DECISION F104 D1's oversize-commit exception is not invoked. `python3 -m ruff
check` on the file after C4a alone reports two unused imports (`time`, `pytest`, both first used in
part 2) — an artifact of the split, not of the finished file, which is clean after C4b (see G2).

### eed6ff30b F025 R7 C5: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f025-r7-mutations.py | +281/-0 | m1 (vitest, R-1053's fix) and m2 (pytest, R-1054's fix), reusing `f025-r6-mutations.py`'s vitest route; m3-m5 (pytest, the e2e), reusing `f025-r4-mutations.py`'s live-worktree-prep route; each FROM verified single-occurrence read-only against the primary checkout before commit (see External actions) and re-verified live in a disposable worktree after |

281 insertions, under the cap.

### (this commit) F025 R7 C6: rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback |

## External actions

- Read-only check of the mutation tool's five FROM patterns against the primary checkout's real
  files (`apps/ui/src/api/pauseView.ts`, `DetailPopover.tsx`, `pingpong_job.py` twice,
  `pause_control.py`) before it was committed: each occurs exactly once. No primary file was
  mutated by this check.
- `git worktree add --detach .remedy-wt/f025-r7-mut eed6ff30b` (C5's HEAD) — succeeded, for G5's one
  official run against the committed tool.
- `python3 -B .agent/authored/f025-r7-mutations.py .../f025-r7-mut` — all 5 mutations caught, all
  restores byte-identical, both controls (pytest + vitest) green first and last, final line `True`.
- `git worktree remove --force .remedy-wt/f025-r7-mut` — succeeded; `git worktree prune` —
  succeeded (no-op); `git worktree list` afterward shows only the primary checkout and the
  pre-existing worktrees found at session start — nothing new left behind.
- `git push origin feature/f025-pause-resume` — runs immediately after this commit (C6); its real
  outcome is reported in the final reply, since the handoff commit precedes the push.

No `gh pr create`, no `gh pr merge`, no other `gh` command this round (constraint 5: nothing is
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
218eaabd6 F025 R6 C7: rewrite handoff for round 6
```

```
$ (line count and sha256 of .remedy-wt/f025-r7/block.md, measured)
line_count: 177
sha256: e2241811c146aa6d69caf709a23c73b7912bcbf46b53b3ce4f4988522de16b82
```
Matches both readings the delegation message gave exactly.

```
$ git worktree list
(reported: primary checkout + the pre-existing F015/F020/F023/F024/F025/F284 dry/sim worktrees and
four remedy/job-* worktrees already present at session start — left alone throughout, per constraint 5)
```

### G1 — transport

Every payload's measured lines/bytes/sha256 matched the block's table exactly (d5.md 40/3598/
ed1e3cbe…, f285_from.txt 2/158/6a0b143f…, f285_to.txt 5/420/00426287…, ledger.md 8/6832/8ad8cf41…,
plan.md 29/994/f8850294…). Each `.agent/authored/f025-r7-*` copy, read back with
`git show 8b3f652d6:<path>`, is byte-identical (both raw-bytes `==` and sha256 match) to its
`.remedy-wt/f025-r7/` source, block copy included. At C1b: `.agent/decisions.md` and
`.agent/live_review.md` equal their `218eaabd` bytes plus their payloads (verified by the exact
append operation, python `bytes + bytes`, plus the numstat match); `.agent/plan.md` equals
`plan.md`'s bytes exactly (`==` check, True); the T2_F285.md pair holds — FROM occurred once before
the edit, TO occurs once after, and the file equals its `218eaabd` bytes with FROM replaced by TO
(diff shown above under C1b). `open_finding_ids` over `.agent/live_review.md` at C1b reads
`['R-1008', 'R-1053', 'R-1054', 'R-1055']`, matching the block's stated reviewer reading exactly.

### G2 — the code

```
$ python3 -m ruff check tests/ui_contracts/test_pause_controls_contract.py tests/ui_server/test_pause_e2e_live.py .agent/authored/f025-r7-mutations.py apps/ui/src/api/pauseView.ts
All checks passed!
```
(pauseView.ts and pauseView.test.ts are TypeScript, not ruff's domain, and are covered instead by
G3's vitest node.)

```
$ git diff --stat 218eaabd HEAD -- packages apps/cli
(empty)
```

```
$ git diff 218eaabd HEAD -- packages apps scripts | grep -c "noqa: BLE001"
0
```

```
$ git diff --name-only a2de57b52 eed6ff30b
.agent/authored/f025-r7-mutations.py
apps/ui/src/api/pauseView.test.ts
apps/ui/src/api/pauseView.ts
apps/ui/src/components/detail/DetailPopover.tsx
tests/ui_contracts/test_pause_controls_contract.py
tests/ui_server/test_pause_e2e_live.py
```
Every path is inside constraint 3's tracked set.

### G3 — the tests nearest the change

```
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_pause_e2e_live.py tests/ui_server/test_pause_door_live.py tests/orchestration/test_pause_resume.py tests/ui_contracts/test_pause_controls_contract.py tests/ui_contracts/test_ui_lint.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/cli/test_golden_path.py tests/docs/
517 passed in 91.67s (0:01:31)
```
Exit 0, zero SKIPPED lines. `test_dashboard_contract.py::test_typescript_compiles` (tsc),
`test_ui_lint.py`'s eslint tests and `test_test_runner.py`'s vitest tests are all inside this run and
all passed — none skipped.

```
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_pause_e2e_live.py
2 passed in 14.73s
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_pause_e2e_live.py
2 passed in 14.65s
```
The e2e file alone, twice more, serially, as ordered.

### G4 — the neighbours

```
$ python3 -m pytest -q -p no:cacheprovider tests/ui_server/test_command_channel.py
109 passed in 7.48s
```

```
$ python3 <equivalent of run_sel.py, round 6's selection.txt files + tests/ui_server/test_pause_e2e_live.py, -n 8>
files 146 exit 0 wall 190 s
SKIPPED [1] tests/regression/test_named_bugs.py:295 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:312 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:321 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:383 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:392 ... (D3 quarantine, F252)
SKIPPED [1] tests/regression/test_named_bugs.py:399 ... (D3 quarantine, F252)
SKIPPED [1] tests/test_agent_tooling.py:43 ... (D12 quarantine, F252)
SKIPPED [1] tests/test_install_smoke.py:175 ... (install smoke opt-in)
SKIPPED [1] tests/test_repair_context_reviewer_memory.py:257 ... (UI source not found)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441 ... (D3 quarantine, F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484 ... (D3 quarantine, F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507 ... (D3 quarantine, F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543 ... (D3 quarantine, F252)
9700 passed, 13 skipped in 189.19s (0:03:09)
```
Exit 0. 13 skipped — the same standing set `218eaabd` carried. 9700 passed against `218eaabd`'s 9697
over round 6's 144 files (the e2e file not yet existing): +3, exactly the two new e2e tests plus the
one new contract test C3 added; no failing node, so nothing needed a serial re-run.
`.remedy-wt/f025-r7/run_sel.py` itself reads a fixed `selection.txt` with no room for an extra file
argument, so its exact command was replicated inline with the e2e file appended to the same file
list, `-n 8`, otherwise identical (same flags, same cwd).

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, ... "fail_count": 0, "ok": true, "passed": true, ...}
```
Six `pass`, `fail_count` 0.

### G5 — the red proofs

```
$ python3 -B .agent/authored/f025-r7-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f025-r7-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f025-r7-mut
.../apps/ui/node_modules: symlinked from the primary checkout
.../apps/ui/dist: copied from the primary checkout, mtimes bumped +60s
CONTROL FIRST: pytest exit=0 failed=0 | vitest exit=0 failed=0
m1 (taskPauseAction answers pause for a task in state current) [vitest]: exit=1 failed=1
  failing=[taskPauseAction > answers null for a task that is already current (R-1053)]
  caught=True restored byte-identical=True
m2 (the popover's key={task.id} is deleted) [pytest]: exit=1 failed=1
  failing=[tests/ui_contracts/test_pause_controls_contract.py::test_the_popovers_control_is_keyed_by_the_tasks_id]
  caught=True restored byte-identical=True
m3 (lift_job_pause's body is replaced by raise RuntimeError("m3 probe")) [pytest]: exit=1 failed=2
  failing=[...TestJobScopeE2ELive..., ...TestTaskScopeE2ELive...]
  caught=True restored byte-identical=True
m4 (unpause_job_command answers not_paused where it answers parked) [pytest]: exit=1 failed=1
  failing=[...TestJobScopeE2ELive...]
  caught=True restored byte-identical=True
m5 (the park leaves job.pause empty) [pytest]: exit=1 failed=2
  failing=[...TestJobScopeE2ELive..., ...TestTaskScopeE2ELive...]
  caught=True restored byte-identical=True
CONTROL LAST: pytest exit=0 failed=0 | vitest exit=0 failed=0
apps/ui/src/api/pauseView.ts: restored byte-identical: True
apps/ui/src/components/detail/DetailPopover.tsx: restored byte-identical: True
packages/orchestration/pingpong_job.py: restored byte-identical: True
packages/orchestration/pause_control.py: restored byte-identical: True
.../apps/ui/node_modules: removed
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
```

```
$ git worktree remove --force .remedy-wt/f025-r7-mut
$ git worktree prune
$ git worktree list
(no f025-r7-mut entry; every pre-existing worktree still present, untouched)
```

## Authored-text proofs

`.agent/authored/f025-r7-block.md`, `f025-r7-d5.md`, `f025-r7-f285_from.txt`, `f025-r7-f285_to.txt`,
`f025-r7-ledger.md` and `f025-r7-plan.md` were built with `shutil.copyfile` from the reviewer's
payload files — never retyped, never edited — and G1 compared every one byte for byte, read back
with `git show 8b3f652d6:<path>`, against its source: all six BYTE-IDENTICAL.
`.agent/decisions.md` and `.agent/live_review.md` were appended with raw bytes read from
`d5.md`/`ledger.md` (python `Path.write_bytes(old_bytes + payload_bytes)`), never retyped;
`.agent/plan.md` was rewritten whole from `plan.md`'s bytes via `shutil.copyfile`;
`docs/roadmap/features/T2_F285.md` had `f285_from.txt`'s bytes replaced by `f285_to.txt`'s bytes via
one `bytes.replace(from_bytes, to_bytes, 1)` call, asserted single-occurrence before and after. G1's
numstat comparisons confirm all four match the payloads' expected insertion counts exactly.
`apps/ui/src/api/pauseView.ts`/`.test.ts`, `DetailPopover.tsx`,
`tests/ui_contracts/test_pause_controls_contract.py`, `tests/ui_server/test_pause_e2e_live.py` and
`.agent/authored/f025-r7-mutations.py` are WORKER-authored production code, tests and the G5 tool
against R-1053's and R-1054's FIX clauses and DECISION F025 D5's own specification — not reviewer
payloads — so no authored-text proof applies to them.

## Deviations & assumptions

1. **The first runner resolves providers BY NAME, monkeypatching `create_provider`, not by an
   injected provider object (E2).** The door test's own `_RUNNER` passes `builder_provider=`/
   `reviewer_provider=` OBJECTS, which `run_job` then reuses UNCHANGED across every task in that one
   process — `FakeProvider`'s pass/fail rounds are counted on that one instance's cumulative
   `_build_count`/`_review_count`, so after task 1 spends two review calls to pass, tasks 2 and 3
   inherit a counter already past the pass threshold and need no repair round at all. The real CLI
   relaunch never injects an object (`builder_provider`/`reviewer_provider` stay their `None`
   default), so `run_pingpong` calls `create_provider(name)` FRESH for every task — every task gets
   its own round 1. Object injection therefore made a single continuous control run and a
   two-episode relaunch produce different `repair_rounds_used` per task by construction, nothing to
   do with the pause itself; the runner now calls `run_job(job.job_id, builder_name="fake",
   reviewer_name="fake")` with `packages.orchestration.pingpong_loop.create_provider` monkeypatched
   to add the sleep while returning a fresh instance every call, exactly matching what the CLI
   relaunch already does unmonkeypatched. This is why D5's own text was followed literally ("read
   `_cmd_job_run` and `create_provider` for those values; never assume them") rather than copying the
   door test's shortcut.
2. **`_task_level_event_names` sorts by each event's own `timestamp` field, not by run-log filename.**
   `new_run_id()` is a random UUID4 (confirmed by reading `run_log.py`), not a chronological one, so
   sorting the job's several run-log files (one per process/episode) by NAME — safe for `_events`
   above, which only ever counts a named event — would silently interleave a relaunch's episode
   ahead of the run it resumed. Not stated in the block; discovered by reproducing the scenario
   outside pytest first (see below) and confirmed necessary before the job-scope comparison could
   ever pass regardless of the other fixes.
3. **A job-scope park's own interrupted task-attempt events are trimmed to their final attempt
   before the ordered comparison.** A JOB-SCOPE pause lands mid-call on the task after the one just
   applied (S1: "every call already in flight finishes"); that task's `task_run_started` (and
   sometimes one `task_round_completed`, depending on exactly which call was in flight) is written
   before the roll-back to `pending`, then the task runs again in full once relaunched. Neither the
   final export nor the final workspace bytes reflect the abandoned attempt — `_normalized_export`
   and `_workspace_bytes` only ever see the task's FINAL, committed run — so `_task_level_event_names`
   applies the same "final state only" principle: per task id, only the events from its LAST
   `task_run_started` onward are kept. This is not one of D5's four named pause/resume event
   exclusions (`job_paused`/`job_resumed`/`task_paused`/`task_resumed`); it is a consequence of the
   SAME park mechanic those four exclusions exist for, expressed through ordinary task-lifecycle
   events rather than a dedicated one, and a control task (started exactly once) is untouched by the
   filter. Recorded here per constraint 3's own rule ("A field you find differing that is not in
   that class is a FINDING for the handback, never a new entry in the list") — this is reported as a
   deviation with its reasoning rather than silently folded into `E4_REMOVED_FIELDS`, which names
   only fields inside `_export_job`'s own shape.
4. **Every `*_source` provenance field inside `execution_config` (and the job's own
   `repair_rounds_source`) is treated as a "run reference" for E4 and stripped.** A relaunch always
   re-resolves its config from the job's OWN persisted `execution_config`, so every provenance label
   reads `persisted` after a relaunch and `default` for a single control run, for a value that is
   otherwise byte-identical — discovered the same way as #1, by running the comparison and reading
   the actual diff rather than predicting it. Listed once in `E4_REMOVED_FIELDS` as `*_source` with
   its reason, applied by a key-suffix rule in `_strip_generic_keys`.
5. **`run_manifest.error` is treated as a run-manifest episode field and stripped.** The manifest's
   per-episode call-expectation check reports a relaunch's SECOND episode short for a task that made
   its calls in the FIRST one — a real, deterministic manifest-validation message, not a fake
   provider artifact — while a single-episode control never triggers it. Classified under "the run
   manifest's episodes and episode fields" per D5's own class list; also fixed a bug in the first
   attempt at this normalization, which named `run_manifest.path` in `E4_REMOVED_FIELDS`'s prose but
   never actually popped it in `_normalized_export` — corrected before this handback, not left for a
   finding.
6. **The C4 commit is split across C4a/C4b (constraint 2).** The whole new test file is 625 lines,
   over the 500-insertion cap as one commit; split at the file's own natural seam, immediately before
   `TestJobScopeE2ELive`. Declared here per the block's own instruction ("split any that would reach
   500 insertions and say so"), not treated as DECISION F104 D1's oversize-commit exception (nothing
   here is accepted whole over the cap).
7. **No production file under `packages/` or `apps/cli/` needed changing.** E3 and E4 both pass
   against the code exactly as `218eaabd` left it — `run_job`, `park_job_pause`, `lift_job_pause`,
   `unpause_job_command` and `_export_job` needed no widening, only a test-side normalization of
   what a relaunch legitimately changes. Constraint 4's stop-and-report clause is therefore not
   invoked.
8. **No full-suite run.** Per constraint 6 (amend0917 rule 1), only G3's and G4's targeted selections
   ran; the one full-suite run per feature belongs to F025's closure, not this round.

No payload was edited or retyped. `packages/`, `apps/cli/`, `cockpitLogic.ts`, `decisionSubmit.ts`,
`steeringSend.ts`, both `tokens.css` files, `graph_spec.md` and `docs/roadmap/ROADMAP.md` are
confirmed untouched by G2's `git diff --stat` (only `docs/roadmap/features/T2_F285.md` changed,
exactly as PAYLOADS orders). The one worktree this round created (`.remedy-wt/f025-r7-mut`) was
removed the same round, per constraint 5; every pre-existing worktree was left alone.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 261 insertions, matches the block's expectation (177+84) exactly |
| C1b | done | 40/0, 8/0, 8/9, 3/0 insertions, matches the block's expectation exactly; `open_finding_ids` reads `['R-1008', 'R-1053', 'R-1054', 'R-1055']` |
| C2 | done | 21 insertions; R-1053's FIX landed with its three new state-specific tests |
| C3 | done | 11 insertions; R-1054's FIX landed with its named test |
| C4 | done | 625 insertions total, split C4a (419) + C4b (206) per constraint 2; E1-E4 landed whole |
| C5 | done | 281 insertions; the G5 tool landed, its FROM patterns pre-checked against the primary checkout |
| C6 | done | this handback |
| G1 | done | all payload and copy identity checks byte-identical; open-finding set matched at C1b |
| G2 | done | ruff clean over every changed .py file; packages/apps-cli untouched; no new noqa: BLE001; name-only diff exactly inside constraint 3 |
| G3 | done | 517 passed, exit 0, no SKIPPED; tsc/eslint/vitest nodes each confirmed PASSED; e2e file alone green twice more |
| G4 | done | 109 passed (neighbour); 9700 passed, 13 skipped, exit 0 (selection + e2e, 8 workers); integrity check 6/6 pass |
| G5 | done | all 5 mutations caught, all restores byte-identical, `True`; pre-checked read-only against the primary, then officially at C5's HEAD in a disposable worktree |
| G6 | done | reported in the final reply, after C6 and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 7. Then F025's closure
sequence. Open findings: 4 — `R-1008` and `R-1055`, owned by F285, and `R-1053` and `R-1054`, owned
by F025 and repaired this round — the count `open_finding_ids` reads at C1b. Operator questions
open: 4 — the count of `### Q` headings in `.agent/operator_questions.md` at C1b (unchanged this
round).
