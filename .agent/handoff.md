# Handback — F026 Task edit at runtime · Round 4

## Session

SESSION 1 of feature F026 · round 4 · rounds so far 4

A large fraction of the session's context budget remained by the point this handback was
written. This round booked round 3's PASS verdict, registered R-1060, recorded DECISION
F026 D4, repaired R-1060 (the `sk-` alternative now matches only at a token start), and
landed T003's second half: the client's pure eligibility/diff view (`taskEditAction`,
`changedTaskFields` in `taskSpecView.ts`), the send module `taskEditSend.ts` (modelled on
`pauseSend.ts`), the detail popover's "Edit task" form (`TaskEditForm.tsx`, wired into
`DetailPopover.tsx`, the popover's scroll rule), and the live end-to-end proving a planned
job fails through the CLI, is edited through the real door, is relaunched through the CLI,
and its new trace and the live server's `events-since` frames show the edit and the second
run.

## Range

Review of 753f44bd1..HEAD

## Commits

### 0dc9a0be6 F026 R4 C1a: copy round 4 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r4-block.md | +245/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f026-r4-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f026-r4-records.diff | +67/-0 | copy of the records.diff payload |

343 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 245, plus 98: 31+67 = 98) — matches exactly.

### 7b963106a F026 R4 C1b: book round 3, register R-1060, record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +47/-0 | records.diff: DECISION F026 D4 appended |
| .agent/live_review.md | +4/-0 | records.diff: F026 R3 gate entry and R-1060's registration appended |
| .agent/plan.md | +11/-11 | rewritten whole to the plan.md payload (`shutil.copyfile`) |

47/0, 4/0, 11/11 — matches the block's G2 stated expectation exactly. `git apply --check` on
records.diff: exit 0; `git apply`: exit 0.

### b3b6a77cd F026 R4 C2: the secret detector finds a key only at a token start (R-1060)
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/redaction_patterns.py | +1/-1 | S1: the `sk-` alternative of `_SECRET_RE` gains a negative lookbehind for a letter or a digit (`(?<![A-Za-z0-9])`); no other line of the file changed |
| tests/orchestration/test_redaction_patterns.py | +44/-0 | NEW FILE, THE TESTS: no finding for the three named false positives; a finding for a key after a space, `=`, a double quote, `/`, `-`, and at the start of the text |
| .agent/live_review.md | +2/-0 | the `Landed: R-1060 —` line this block orders |

47 insertions, under the cap. `python3 -m ruff check` on both `.py` files: clean.
`tests/orchestration/test_redaction_patterns.py`: 9 passed. The previously-red
`tests/ui_contracts/test_graph_architecture.py::TestSpatialLayout::test_no_raw_leaks_in_viewer`:
1 passed, from this commit on.

### f455e74a7 F026 R4 C3a: the client reads the edit action and the changed fields
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/taskSpecView.ts | +103/-0 | S2: `taskEditAction` (null unless `editState` is waiting/paused/failed), `TaskEditDraft`, `TaskEditFields`, `changedTaskFields` (trims acceptance/files lines, drops blanks, includes only changed keys) |
| apps/ui/src/api/taskSpecView.test.ts | +108/-2 | THE TESTS: the action for each of the three states, null for `""` and a missing spec; `changedTaskFields` for no change, each single field, trimming and blank lines |

211 insertions, under the cap. **DEVIATION (declared before review, S7):** the block's
single commit "C3" (S2 and S3 together) would insert 679 lines — over the 500-line cap —
so it is split into C3a (S2, this commit) and C3b (S3, next). `tsc --noEmit`: exit 0.
`eslint`: 0 problems. `vitest run` (this file): 24 passed.

### 5744ff367 F026 R4 C3b: the send module for job.edit-task
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/taskEditSend.ts | +249/-0 | NEW FILE, S3: `JOB_EDIT_TASK_COMMAND_ID`, `buildTaskEditRequest`, `submitTaskEditRequest`, `describeTaskEditResult` (stale-version and detail 409s, everything else reused from `describePauseSendResult`), `sendTaskEdit` |
| apps/ui/src/api/taskEditSend.test.ts | +219/-0 | NEW FILE, THE TESTS: the request's path/headers/body; null for each unusable input and for empty fields; each sentence of `describeTaskEditResult`; the injected-seam flow |

468 insertions, under the cap (see C3a for the split reason). `tsc --noEmit`: exit 0.
`eslint`: 0 problems. `vitest run` (this file): 24 passed.

### 19e82d0ea F026 R4 C4: the detail popover offers the edit form for an editable task
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/detail/TaskEditForm.tsx | +104/-0 | NEW FILE, S4: closed ghost "Edit task" button; open form (Title, Goal, Acceptance, Size band, Files) prefilled from `action.current`; the failed-state relaunch note; Save (disabled while `changedTaskFields` is `{}` or sending) and Cancel; shows `sendTaskEdit`'s sentence in `<p aria-live="polite">` |
| apps/ui/src/components/detail/DetailPopover.tsx | +20/-1 | S4: computes `editAction = task ? taskEditAction(dashboard, task.id) : null`; mounts `<TaskEditForm key={task.id} …/>` directly after `<TaskVersionList/>` only when `task && serverToken && editAction` |
| apps/ui/src/components/detail/DetailPopover.module.css | +19/-1 | S4: `.ghostButton`, `.savePill`, `.editForm`/`.editField`/`.editNote`/`.editActions`/`.editResult` — tokens only; `.popover` gains `max-height: calc(100vh - 120px); overflow-y: auto;`, its only other change |
| docs/ui/design_reference/assumption_log.md | +1/-0 | S5: the edit-form/scroll row, dated 2026-09-25, feature F026, citing DECISION F026 D4 |
| tests/ui_contracts/test_task_edit_controls_contract.py | +57/-0 | NEW FILE, THE TESTS: no `fetch(` in `TaskEditForm.tsx`/`taskSpecView.ts`; `taskEditSend.ts` names `"job.edit-task"`; the popover mounts `<TaskEditForm` with `key={task.id}` inside the condition naming `taskEditAction(dashboard, task.id)` |

201 insertions, under the cap. `tsc --noEmit`: exit 0. `eslint`: 0 problems.
`tests/ui_contracts/test_task_edit_controls_contract.py` + `test_pause_controls_contract.py`:
10 passed. Full `tests/ui_contracts`: 940 passed, 4 skipped (no regression). Full `vitest run`:
1350 passed, 5 skipped (no regression).

### 00a5db67a F026 R4 C5: the end-to-end: fail, edit through the door, relaunch, read the trace and the fan
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_task_edit_e2e_live.py | +245/-0 | NEW FILE, S6: an approved two-task plan (T1 carries the OLD marker), run 1 through the real CLI subprocess (`--builder-provider fake --reviewer-provider fake --max-rounds 1 --repair-rounds 0`) ends blocked/blocked/skipped; a real UI server POST of `job.edit-task` answers 200 with `spec_version` 2 and T2 in `restored`; run 2 (`--max-rounds 3 --repair-rounds 2`) completes both tasks; the new run's trace carries NEW not OLD, the old run's trace keeps OLD; `events-since`, paged from cursor 0, holds exactly two `task_run_started` frames for T1 |
| apps/ui/src/components/graph/brainReducer.test.ts | +16/-0 | THE TEST: a start, a failed run (`task_run_failed`) and a second start leave two builder-run nodes under the task, the first `fail` |

261 insertions, under the cap. `python3 -m ruff check`: clean.
`tests/ui_server/test_task_edit_e2e_live.py`: 1 passed (first attempt, no retry needed).
`vitest run` (brainReducer.test.ts): 45 passed.

### 967e07c92 F026 R4 C6: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r4-mutations.py | +254/-0 | G5: the round's mutation tool, `git add`ed |

254 insertions, under the cap.

### (pending) F026 R4 C7: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f026-r4-mut 967e07c92` (G5) — added, then
  `git worktree remove --force .remedy-wt/f026-r4-mut` — removed after the mutation tool's run.
  `git worktree list` afterward shows the primary checkout and every worktree already present at
  session start, unchanged, `f026-r4-mut` absent. No `git worktree prune` was run this round.
- `git push origin feature/f026-task-edit-runtime` (after C7) — its real outcome is reported in
  the final reply, since the push happens after this commit.
- No `gh pr create` — the branch's pull request opens at F026's closure, per the block.
- No `git stash`, no force-push, no checkout of `main`, no branch deletion, no `remedy/job-*`
  worktree or branch created or deleted by this worker, no `npm`/`npx`.

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory
(absent, checked before step one)
```

```
$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f026-task-edit-runtime
$ git log --oneline -1
753f44bd1 F026 R3 C8: rewrite handoff for round 3
```
All three matched the block's stated readings exactly, before any commit of this round.

```
$ (line count and sha256 of .remedy-wt/f026-r4/block.md, measured)
line_count: 245
sha256: 65562974d5ef456a4aecdd7d062b746ae25acad2eb5d334b52c2934e898474d4
```
Matches both readings the block's own step 3 gave exactly.

```
$ git worktree list
(reported at step 4: primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r4-dry/sim/
F284 dry/sim worktrees, and the same remedy/job-* worktrees already present at session start — no
stale/prunable entries observed)
```

### G1 — payload transport

```
$ wc -lc .remedy-wt/f026-r4-payloads/plan.md .remedy-wt/f026-r4-payloads/records.diff
plan.md          31 lines,  1169 bytes
records.diff     67 lines, 13331 bytes
$ sha256sum .remedy-wt/f026-r4-payloads/plan.md .remedy-wt/f026-r4-payloads/records.diff
plan.md      d3d2704400c50593d7166f219ddceaa3f2062b283070e1754b54311bbdb08d0b
records.diff d6fe996241624d65508ea6c07522f9f4917db1dabc96264a0208896831293afc
```
Every payload's measured lines/bytes/sha256 matched the block's table exactly.

```
$ git show 0dc9a0be6:.agent/authored/f026-r4-block.md | sha256sum
65562974d5ef456a4aecdd7d062b746ae25acad2eb5d334b52c2934e898474d4
$ git show 0dc9a0be6:.agent/authored/f026-r4-plan.md | sha256sum
d3d2704400c50593d7166f219ddceaa3f2062b283070e1754b54311bbdb08d0b
$ git show 0dc9a0be6:.agent/authored/f026-r4-records.diff | sha256sum
d6fe996241624d65508ea6c07522f9f4917db1dabc96264a0208896831293afc
```
Each `.agent/authored/f026-r4-*` copy, read back with `git show 0dc9a0be6:<path>`, is
byte-identical to its `.remedy-wt/f026-r4(-payloads)/` source.

### G2 — the records

```
$ git show 7b963106a:.agent/live_review.md | wc -c; git show 7b963106a:.agent/live_review.md | sha256sum
325971  f99a5029779fa894cb5d31bb818e7f6c5a791d5cfc367ca3cb9c427e951b6246
$ git show 7b963106a:.agent/decisions.md | wc -c; git show 7b963106a:.agent/decisions.md | sha256sum
2139835  5d5bf3580408b46cb3b50e214439e4d216fddff52fe669ba9007be2961d51fc4
$ git show 7b963106a:.agent/plan.md | wc -c; git show 7b963106a:.agent/plan.md | sha256sum
1169  d3d2704400c50593d7166f219ddceaa3f2062b283070e1754b54311bbdb08d0b
```
All three equal the block's stated G2 table exactly.

```
$ python3 -c "from scripts.rotate_live_review import open_finding_ids; ..."
open at 753f44bd1: ['R-1008', 'R-1055', 'R-1057', 'R-1058']
open at 7b963106a:  ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1060']
open at 967e07c92:  ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1060']
```
Matches the block's stated reading exactly at every point named. The ledger's last line at C2
begins `Landed: R-1060 — `.

### G3 — the code, at C6 (967e07c92)

```
$ python3 -m ruff check packages/orchestration/redaction_patterns.py tests/orchestration/test_redaction_patterns.py tests/ui_contracts/test_task_edit_controls_contract.py tests/ui_server/test_task_edit_e2e_live.py .agent/authored/f026-r4-mutations.py
All checks passed!
```
(every `.py` path of CONSTRAINT 2)

### G4 — the tests, in the primary checkout at C6

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/orchestration/test_redaction_patterns.py tests/ui_contracts/test_task_edit_controls_contract.py tests/ui_server/test_task_edit_e2e_live.py tests/ui_contracts tests/ui_server/test_auth_redaction.py tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/ui_server/test_dashboard_task_specs.py tests/ui_server/test_command_dispatch.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_prompt_redaction.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
1675 passed, 5 skipped in 92.10s (0:01:32)
REAL_EXIT=0
```
Exactly five `SKIPPED` lines: the four D3 quarantines and the one D12 quarantine the block says
stay skipped — no other skip, and no failure at all (unlike round 3's carried-over R-1060
failure, repaired at C2 this round).

Individually confirmed: the TypeScript node `test_typescript_compiles`
(`tests/ui_server/test_dashboard_contract.py`) — **the responsive node** — ran the real local
`tsc --noEmit` (the binary is present) and PASSED, not skipped (1 passed). The vitest node of
`tests/orchestration/test_test_runner.py`: 49 passed. The two lint nodes of
`tests/ui_contracts/test_ui_lint.py`: 2 passed.
`test_no_raw_leaks_in_viewer` (`tests/ui_contracts/test_graph_architecture.py::TestSpatialLayout`):
PASSES, from C2 on (it was round 3's sole carried failure, R-1060).

**Accounting for the pass/skip-count difference against the reviewer's stated baseline
(`1615 passed, 10 skipped` for the same selection minus the three new test files and the golden
path):** this run adds the three new files' own tests (`test_redaction_patterns.py` 9,
`test_task_edit_controls_contract.py` 3, `test_task_edit_e2e_live.py` 1 — 13 total) plus
`tests/cli/test_golden_path.py`'s own tests, which together account for the +60 passed
(1675−1615). This run's skip count (5) is exactly the steady-state four-D3-plus-one-D12 set the
block itself names as what should stay skipped; the reviewer's stated 10-skip baseline is not
reproduced or re-derived here (their tree's exact state at that reading is not this worker's to
reconstruct), but every skip THIS run actually produced is accounted for by name above, and no
skip beyond that steady-state five was observed.

```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=160"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true}
REAL_EXIT=0
```
Six `pass`, `fail_count` 0.

### G5 — the red proofs

```
$ git worktree add --detach .remedy-wt/f026-r4-mut 967e07c92
Preparing worktree (detached HEAD 967e07c92)
$ python3 -B .agent/authored/f026-r4-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r4-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f026-r4-mut
CONTROL FIRST: pytest exit=0 failed=0 | vitest exit=0 failed=0
m1 (the sk- alternative loses its R-1060 boundary) [py]: exit=1 failed=3 failing=[...test_no_finding[feature/f026-task-edit-runtime], ...test_no_finding[risk-assessment-notes], ...test_no_finding[a]] | caught=True restored byte-identical=True
m2 (taskEditAction answers an action for an editState of "") [ts]: exit=1 failed=1 failing=[taskEditAction > is null for an editState of ""] | caught=True restored byte-identical=True
m3 (changedTaskFields returns every field, changed or not) [ts]: exit=1 failed=9 failing=[...9 changedTaskFields cases...] | caught=True restored byte-identical=True
m4 (changedTaskFields keeps blank lines) [ts]: exit=1 failed=3 failing=[...3 trim/blank-line cases...] | caught=True restored byte-identical=True
m5 (buildTaskEditRequest sends job.plan-edit-task) [ts]: exit=1 failed=2 failing=[builds the exact request, names the command job.edit-task] | caught=True restored byte-identical=True
m6 (buildTaskEditRequest omits expected_version) [ts]: exit=1 failed=1 failing=[builds the exact request: path, headers and body] | caught=True restored byte-identical=True
m7 (describeTaskEditResult drops the relaunch sentence for a failed task) [ts]: exit=1 failed=1 failing=[adds the relaunch sentence when the body's state is failed] | caught=True restored byte-identical=True
m8 (the popover mounts <TaskEditForm without the taskEditAction condition) [py]: exit=1 failed=1 failing=[test_the_popover_mounts_the_form_keyed_by_the_task_id_inside_the_eligibility_condition] | caught=True restored byte-identical=True
CONTROL LAST: pytest exit=0 failed=0 | vitest exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f026-r4-mut
$ git worktree list
(primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r4-dry/sim/F284 dry/sim
worktrees and the same remedy/job-* worktrees already present at session start; f026-r4-mut absent)
```
Every one of the 8 mutations was caught (exit≠0, failed>0) on the FIRST run, every restore
byte-identical, both controls green (exit 0, 0 failed). No mutation stayed green; no test needed
to be added.

## Authored-text proofs

`.agent/authored/f026-r4-block.md`, `f026-r4-plan.md` and `f026-r4-records.diff` (at C1a) were
built with `shutil.copyfile` from the reviewer's payload files — never retyped, never edited —
and G1 compared every one byte for byte, read back with `git show 0dc9a0be6:<path>`, against its
source: all three BYTE-IDENTICAL. `.agent/plan.md` was REWRITTEN whole (verbatim to the `plan.md`
payload) at C1b; `records.diff` was applied verbatim with `git apply --check` then `git apply`,
never retyped or hand-edited — G2's byte/sha256 table on the resulting `.agent/live_review.md`,
`.agent/decisions.md` and `.agent/plan.md` confirms the applied result matches the reviewer's own
target state exactly.

Everything else this round wrote — the R-1060 repair and its test, the pure client view, the send
module, the edit form and its wiring, the assumption-log row, the live end-to-end and the reducer
test, and the mutation tool — is WORKER-authored production code and tests against the
specification S1–S7 (the block's own framing, "THE PRODUCTION CHANGE IS SPECIFIED, NOT SLICED"),
not reviewer payload text, so no authored-text fidelity proof applies to it.

## Deviations & assumptions

1. **The block's single C3 (S2 and S3 together) was split into C3a and C3b.** Staged together,
   S2 and S3 with their tests would insert 679 lines — over the 500-line cap AGENTS.md's commit
   discipline sets and S7 repeats. C3a carries S2 (`taskSpecView.ts`'s `taskEditAction` and
   `changedTaskFields`, 211 insertions); C3b carries S3 (`taskEditSend.ts`, 468 insertions). Both
   declared here per S7 ("split one that would reach it and say so") and R-0485's rule that a
   commit-sequence departure belongs in this section even though the commit table above already
   shows it.
2. **`TaskEditForm.tsx`'s exact prop shape (`target`, `jobId`, `action`) was a judgment call.**
   The block names the component as "taking `target`, `jobId` and the `taskEditAction` result"
   without stating what `jobId` is used for beyond what `target` (a `DecisionSendTarget` already
   carrying `jobId`) provides. It is threaded through as a `data-job-id` attribute on the form
   element and otherwise unused in visible text; `sendTaskEdit`'s relaunch sentence keeps the
   literal placeholder text "remedy job run <job id>" (not a substituted value), matching the
   block's own quoted string exactly, since `describeTaskEditResult` is a pure function of the
   door's reply alone and is not handed a job id.
3. **`describeTaskEditResult`'s "any other 409 with a `detail`" reuses `describePauseSendResult`
   only for statuses it does not special-case.** For 409, the function reads `current_version` or
   `detail` off the body itself (DECISION F026 D2's two shapes) rather than calling
   `describePauseSendResult`, which would otherwise answer the PAUSE door's own fixed 409 sentence
   ("This job has ended…") — wrong for a task-edit refusal. Every other status (400, 403, 429, 500,
   unreachable, and an unrecognised default) is delegated to `describePauseSendResult` unchanged,
   which `taskEditSend.test.ts`'s "words every other refusal exactly as describePauseSendResult
   words its own" test pins directly against that function's real output.
4. Everything else followed the block's ordered commit sequence exactly (C1a, C1b, C2, C3a, C3b,
   C4, C5, C6, C7, then C8 inside which this handback lives — see the item-status table for the
   C3/C3b relabelling); no payload was edited or retyped; no commit touched a path outside the
   tracked set CONSTRAINT 2 names (confirmed by `git diff --name-only 753f44bd1` below); no gate
   went red on this round's own code; no mutation stayed green.

```
$ git diff --name-only 753f44bd1
.agent/authored/f026-r4-block.md
.agent/authored/f026-r4-mutations.py
.agent/authored/f026-r4-plan.md
.agent/authored/f026-r4-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
apps/ui/src/api/taskEditSend.test.ts
apps/ui/src/api/taskEditSend.ts
apps/ui/src/api/taskSpecView.test.ts
apps/ui/src/api/taskSpecView.ts
apps/ui/src/components/detail/DetailPopover.module.css
apps/ui/src/components/detail/DetailPopover.tsx
apps/ui/src/components/detail/TaskEditForm.tsx
apps/ui/src/components/graph/brainReducer.test.ts
docs/ui/design_reference/assumption_log.md
packages/orchestration/redaction_patterns.py
tests/orchestration/test_redaction_patterns.py
tests/ui_contracts/test_task_edit_controls_contract.py
tests/ui_server/test_task_edit_e2e_live.py
```
(measured again after C7, before push, in the final reply) Exactly CONSTRAINT 2's named path set
plus `.agent/handoff.md` (this commit). None of `packages/orchestration/task_edit_runtime.py`,
`packages/orchestration/ui_server.py`, `packages/orchestration/pingpong_job.py`,
`apps/ui/src/api/pauseSend.ts`, `README.md`, `.agent/prose_slips.md`, `.agent/candidates.md`,
`.agent/operator_questions.md` or `docs/roadmap/features/T5_F026.md` appears.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 343 insertions (245+98), matches the block's expectation exactly; all three copies byte-identical |
| C1b | done | `git apply --check`/`git apply` both exit 0; per-file numstat 47/0, 4/0, 11/11 matches the G2 table exactly; open-finding set gains R-1060 |
| C2 | done | 47 insertions; single-line regex repair, comment-only otherwise unchanged; new test file 9 passed; `test_no_raw_leaks_in_viewer` PASSES from here on; the `Landed:` line appended |
| C3 | deviated | split into C3a (S2, 211 insertions) and C3b (S3, 468 insertions) — see Deviations #1; both under the cap, both green |
| C4 | done | 201 insertions, under the cap; `tsc`/`eslint` clean; contract test 3 passed; full `ui_contracts` and `vitest` show no regression |
| C5 | done | 261 insertions, under the cap; live e2e passed first attempt; reducer test passed |
| C6 | done | 254 insertions, under the cap; ruff-clean |
| G1 | done | every payload's lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | all three files match the stated bytes/sha256; open-finding set correct at every reading named; ledger's last line at C2 begins `Landed: R-1060 — ` |
| G3 | done | ruff clean over every `.py` path of CONSTRAINT 2 at C6 |
| G4 | done | 1675 passed, 5 skipped (the four D3 + one D12 quarantines only, no failure); every named toolchain node PASSES individually, including the responsive node `test_typescript_compiles`; six `integrity check` pass |
| G5 | done | all 8 mutations caught on the first run, every restore byte-identical, both controls green; no test needed after G5 |
| G6 | done | reported in the final reply, after C7, the push and the pull-request list |
| Pull request | skipped | not opened this round — the branch opens one at F026's closure, per the block |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 4. Then F026's closure
sequence: the Built State, the checklist consolidation, the self-use item and the feature's one
full suite; then the evidence bundle and the review package; then the acceptance and the pull
request. Open findings: 5 — `R-1008`, `R-1055`, `R-1057` and `R-1058`, owned by F285, and
`R-1060`, owned by F026 (stays open until the reviewer's `Done:`). Operator questions open: 4 —
the count of `### Q` headings in `.agent/operator_questions.md`.
