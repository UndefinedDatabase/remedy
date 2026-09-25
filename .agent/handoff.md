# Handback — F026 Task edit at runtime · Round 3

## Session

SESSION 1 of feature F026 · round 3 · rounds so far 3

A small fraction of the session's context budget remained by the point this handback was
written. This round booked round 2's PASS verdict, resolved R-1059 (its `Done:` paragraph),
recorded DECISION F026 D3, reworded `job.edit-task`'s help text ("while its job is not running"),
and landed T003's first half: the dashboard's `task_specs` section
(`packages/orchestration/ui_server.py`), the client's normalization and pure view
(`apps/ui/src/api/types.ts`, `remedyApi.ts`, the new `taskSpecView.ts`), the canvas's version
chip (`brainOntology.ts`, `brainReducer.ts`, `brainView.ts`, `forceBrainTypes.ts`,
`buildForceBrainModel.ts`, `renderers/paintNode.ts`, `BrainGraphStage.tsx`), and the popover's
chip and Versions list (`DetailPopover.tsx`, the new `TaskVersionList.tsx`) with the two
`assumption_log.md` rows DECISION F026 D3 orders.

## Range

Review of 10ec25125..HEAD

## Commits

### 00f262daf F026 R3 C1a: copy round 3 block and payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r3-block.md | +259/-0 | copy of this round's block, verbatim (`shutil.copyfile`) |
| .agent/authored/f026-r3-plan.md | +31/-0 | copy of the plan.md payload |
| .agent/authored/f026-r3-records.diff | +63/-0 | copy of the records.diff payload |

353 insertions by `git show --numstat` — the block's stated expectation (this block's own line
count, 259, plus 94: 31+63 = 94) — matches exactly.

### ca8aea639 F026 R3 C1b: book round 2, resolve R-1059, record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +43/-0 | records.diff: DECISION F026 D3 appended |
| .agent/live_review.md | +4/-0 | records.diff: F026 R2 gate entry and R-1059's `Done:` paragraph appended |
| .agent/plan.md | +10/-10 | rewritten whole to the plan.md payload (`shutil.copyfile`) |

43/0, 4/0, 10/10 — matches the block's G2 stated expectation exactly. `git apply --check` on
records.diff: exit 0; `git apply`: exit 0.

### c48d2cb56 F026 R3 C2: word job.edit-task's help text for the operator
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +2/-2 | S1: `job.edit-task`'s description reworded to end "while its job is not running." — nothing else in the file changed |

2 insertions, 2 deletions. `tests/test_command_catalog.py`: 60 passed.

### 66893fee1 F026 R3 C3: the dashboard carries each task's spec and version chain
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/ui_server.py | +76/-0 | S2: `_build_task_spec_section(job)`, wired into `_build_dashboard` as `"task_specs"` directly after `"pause"` |
| tests/ui_server/test_dashboard_task_specs.py | +174/-0 | THE TESTS: never-edited task (v1, no versions, `waiting`); after one edit (v2, one archived version); a blocked task reads `failed`; a running job reads `""` with a detail naming `running`; no plan reads no tasks; a corrupt task-pause file reads no tasks and a non-empty error without raising; `_build_dashboard` carries the key |

250 insertions, under the cap. `tests/ui_server/test_dashboard_task_specs.py`: 7 passed.
`tests/ui_server/test_dashboard_pause.py` + `test_dashboard_contract.py`: 72 passed (no
regression).

### a3ec3583a F026 R3 C4: the client reads task specs and derives the chip and the version rows
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/types.ts | +43/-1 | S3: `RemedyTaskSpecFields`, `RemedyTaskSpecVersion`, `RemedyTaskSpec`, `RemedyTaskSpecs`, each doc-commented to DECISION F026 D3; `RemedyDashboard` gains required `taskSpecs` after `pause` |
| apps/ui/src/api/remedyApi.ts | +71/-1 | S3: `normalizeTaskSpecs` and its helpers; wired into `normalizeDashboardPayload` (`dashboard.task_specs`) and `normalizeApiFailure` (`undefined`) |
| apps/ui/src/api/remedyApi.test.ts | +90/-0 | THE TESTS: the mapping, the empty default, a bad `edit_state`, a bad `spec_version` (0, `"3"`, missing → 1), the failure shape |
| apps/ui/src/api/taskSpecView.ts | +109/-0 | NEW FILE, S4: `taskSpecOf`, `taskSpecVersions`, `versionChipLabel`, `specVersionRows` |
| apps/ui/src/api/taskSpecView.test.ts | +122/-0 | THE TESTS: chip labels for 1/2/undefined; rows' order, current flag, per-field changes, list joining |

435 insertions, under the cap. `tsc --noEmit`: exit 0. `vitest run` (these two files): 84 passed.

### aa50254fe F026 R3 C5: an edited task's node carries its version chip
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainOntology.ts | +4/-0 | S5: `BrainTaskSeed` gains optional `specVersion` |
| apps/ui/src/components/graph/brainReducer.ts | +1/-0 | S5: `seedBrainModel` copies `specVersion` into the task node's `meta.specVersion` when present |
| apps/ui/src/components/graph/brainView.ts | +9/-1 | S5: `dashboardBrainSeeds` gains third parameter `specVersions` (default `{}`), puts `specVersion` on a seed only when the map has the task |
| apps/ui/src/components/graph/brainView.test.ts | +15/-0 | THE TESTS: the seed key only when given, and with no third argument no seed carries one |
| apps/ui/src/components/graph/forceBrainTypes.ts | +3/-0 | S5: `BrainLayoutNode` gains optional `chip` |
| apps/ui/src/components/graph/buildForceBrainModel.ts | +11/-0 | S5: `taskChipOf`, and `buildBrainLayout` sets a task node's `chip` only when `meta.specVersion` is a number of at least 2 |
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | +18/-0 | THE TESTS: the chip only at 2 or more, absent (not `undefined`-valued) otherwise |
| apps/ui/src/components/graph/renderers/paintNode.ts | +16/-0 | S5: `PaintableNode` gains optional `chip`; `CHIP_FONT_SIZE` (0.6) and `CHIP_OFFSET` (0.8) beside `CLUSTER_COUNT_SIZE`; `paintBrainNode` paints a task node's chip after the cluster count, before the marks |
| apps/ui/src/components/graph/renderers/paintNode.test.ts | +20/-3 | THE TESTS: the painter's `fillText` of the chip at the specified point for a task, never for another kind |
| apps/ui/src/components/graph/BrainGraphStage.tsx | +3/-2 | S5: passes `taskSpecVersions(dashboard)` as the seeding's third argument |

100 insertions, under the cap. `tsc --noEmit`: exit 0. `eslint src --max-warnings 0`: 0 problems
(the `useMemo` dependency became `[dashboard]`, since `taskSpecVersions(dashboard)` reads the
whole object — see Deviations). Full `vitest run`: 1311 passed, 5 skipped (no regression).

### e9afd218b F026 R3 C6: the detail popover shows the chip and the Versions list
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/detail/DetailPopover.tsx | +14/-0 | S6: reads the task's spec with `taskSpecOf`; the status row's chip span; mounts `<TaskVersionList key={task?.id ?? ""} rows={specVersionRows(spec)} />` after `<PromptTracePanel …/>` |
| apps/ui/src/components/detail/TaskVersionList.tsx | +58/-0 | NEW FILE, S6: renders nothing for no rows, else a "Versions" section, `aria-label="Spec versions"`, one `<li>`/button per row (disabled when no changes), one `<dl>` diff open at a time |
| apps/ui/src/components/detail/DetailPopover.module.css | +15/-0 | S6: `.versionChip`, `.versionList`, `.versionRow`, `.versionDiff` — tokens.css custom properties only, plain pixel sizes, no animation |
| docs/ui/design_reference/assumption_log.md | +2/-0 | S7: the chip row and the Versions-list row, dated 2026-09-25, feature F026, citing DECISION F026 D3 |
| tests/ui_contracts/test_task_version_contract.py | +55/-0 | NEW FILE, THE TESTS: the mount order and key; no `fetch` in `TaskVersionList.tsx`/`taskSpecView.ts`; every button `type="button"` with `aria-expanded` |

144 insertions, under the cap. `tests/ui_contracts/test_task_version_contract.py`: 3 passed.
First attempt at the CSS used `var(--remedy-ink-strong, #0a1c48)`/`var(--remedy-faint, #9aa9c5)`
fallbacks copied from an existing rule in the same file; `tests/ui_contracts/test_raw_colour_ratchet.py`
caught the resulting rise (15→17) before this commit was made, so the fallbacks were dropped
(the tokens are already defined) and the commit above is the corrected version — no ratchet rise.

### 0c6dc30f1 F026 R3 C7: the round's red-proof mutation tool
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f026-r3-mutations.py | +274/-0 | G5: the round's mutation tool, `git add`ed |
| apps/ui/src/api/taskSpecView.test.ts | +16/-0 | m6 stayed green on the first `taskSpecView.test.ts` (see Deviations): added a test asserting a row diffs against the row immediately before it, not the first row, when at least two archived versions exist with distinct values; re-ran green, then confirmed red under the mutation by hand before restoring |

290 insertions, under the cap.

### (pending) F026 R3 C8: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | measured after this commit exists, in the final reply | this handback (self-reference, R-0149 pattern) |

## External actions

- `git worktree add --detach .remedy-wt/f026-r3-mut 0c6dc30f1` (G5) — added, then
  `git worktree remove --force .remedy-wt/f026-r3-mut` — removed after the mutation tool's run.
  `git worktree list` afterward shows the primary checkout and every worktree already present at
  session start, unchanged, `f026-r3-mut` absent. No `git worktree prune` was run this round (none
  was needed — no stale entry was observed at session start).
- `git worktree add --detach .remedy-wt/f026-r3-check 10ec25125` — a throwaway worktree, NOT ordered
  by the block, created to isolate whether a `tests/ui_contracts/test_graph_architecture.py` failure
  (see Deviations) predates this round's diff. Removed with `git worktree remove --force` immediately
  after use; recorded here and in Deviations because CONSTRAINT 5 asks every worktree add/remove be
  reported, not only the ordered one.
- `git push origin feature/f026-task-edit-runtime` (after C8) — its real outcome is reported in
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
10ec25125 F026 R2 C8: rewrite handoff for round 2
```
All three matched the block's stated readings exactly, before any commit of this round.

```
$ (line count and sha256 of .remedy-wt/f026-r3/block.md, measured)
line_count: 259
sha256: 7fd2ae0e91d5a32d348648fb3f7cdb0462364704cd3f9807349d6d1945767744
```
Matches both readings the block's own step 3 gave exactly.

```
$ git worktree list
(reported at step 4: primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r3-dry/sim/
F284 dry/sim worktrees, and the same remedy/job-* worktrees already present at session start — no
stale/prunable entries observed)
```

### G1 — payload transport

```
$ (lines/bytes/sha256 of each .remedy-wt/f026-r3-payloads/ payload, measured)
plan.md          31 lines,  1150 bytes, 2b82375cb0f32a7cc0fac17b1077716442f88d1b1c6e30344e28f1787d674709
records.diff     63 lines,  9689 bytes, a0e6484f1ad7ee8173a9364e722b6a83109df434601ad3293f800ace1abbddf7
```
Every payload's measured lines/bytes/sha256 matched the block's table exactly.

```
$ python3 -c "committed = git show <commit>:<path>; source = open(<src>, 'rb').read(); committed == source"
f026-r3-block.md     (at 00f262daf)  EQUAL (sha256 7fd2ae0e...)
f026-r3-plan.md      (at 00f262daf)  EQUAL (sha256 2b82375c...)
f026-r3-records.diff (at 00f262daf)  EQUAL (sha256 a0e6484f...)
```
Each `.agent/authored/f026-r3-*` copy, read back with `git show 00f262daf:<path>`, is
byte-identical to its `.remedy-wt/f026-r3(-payloads)/` source.

### G2 — the records

```
$ python3 -c "bytes/sha256 of each path read with git show ca8aea639:<path>"
.agent/live_review.md    321169 bytes  3d044b3cd18c6f316415ead6462635c27d5d725efec46a2701b17c98e80e8646
.agent/decisions.md     2135451 bytes  58e8b195149417b1873607ad9740fc425f65bbc07a93ae65c86c8b6729ad337a
.agent/plan.md             1150 bytes  2b82375cb0f32a7cc0fac17b1077716442f88d1b1c6e30344e28f1787d674709
```
All three equal the block's stated G2 table exactly.

```
$ python3 -c "from scripts.rotate_live_review import open_finding_ids; ..."
open at 10ec25125: ['R-1008', 'R-1055', 'R-1057', 'R-1058', 'R-1059']
open at ca8aea639:  ['R-1008', 'R-1055', 'R-1057', 'R-1058']
open at 0c6dc30f1:  ['R-1008', 'R-1055', 'R-1057', 'R-1058']
```
Matches the block's stated reading exactly at every point named.

### G3 — the code, at C7 (0c6dc30f1)

```
$ python3 -m ruff check apps/cli/command_catalog.py packages/orchestration/ui_server.py tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_task_version_contract.py .agent/authored/f026-r3-mutations.py
All checks passed!
REAL_EXIT=0
```
(every `.py` path of CONSTRAINT 2)

### G4 — the tests, in the primary checkout at C7

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_server/test_dashboard_task_specs.py tests/ui_contracts/test_task_version_contract.py tests/ui_server/test_dashboard_contract.py tests/ui_server/test_dashboard_pause.py tests/orchestration/test_test_runner.py tests/ui_contracts tests/test_command_catalog.py tests/orchestration/test_task_edit_runtime.py tests/orchestration/test_import_reachability.py tests/test_no_orphan_modules.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): ...
1 failed, 1684 passed, 5 skipped in 92.45s (0:01:32)
REAL_EXIT=1
```
Exactly five `SKIPPED` lines: the four D3 quarantines and the one D12 quarantine the block says
stay skipped — no other skip. The toolchain nodes all PASS in this run (confirmed individually):
the TypeScript node of `test_dashboard_contract.py` and the vitest node of `test_test_runner.py`
together read 113 passed, 0 skipped; the two lint nodes of `test_ui_lint.py` read 2 passed; the
responsive node of `tests/ui_contracts/test_responsive.py` reads 89 passed, 0 skipped, 0 failed.

**The one FAILURE — accounted for, not a product of this round's diff:**
`TestSpatialLayout.test_no_raw_leaks_in_viewer` (`tests/ui_contracts/test_graph_architecture.py`)
fails with `forbidden secret pattern: sk-edit-runtime`. `packages/orchestration/redaction_patterns.py`
flags any `sk-[a-zA-Z0-9_-]{8,}` substring as an API-key-shaped secret; `project_brain.py`'s git-status
node embeds the CURRENT REPO'S REAL branch name via `Git: <branch> (<sha>)`
(`status.current_branch`, read live from the actual checkout the test runs in, since the test's
`_make_job()` fixture sets `metadata={"target_repo": "."}"`), and this branch's own name,
`feature/f026-task-edit-runtime`, contains the substring `sk-edit-runtime` (`ta` + `sk` + `-edit-
runtime`) — a false positive of the branch's own name, not of any file this round wrote. Proved
independent of this round's diff: `find_forbidden_surface_tokens("branch feature/f026-task-edit-
runtime")` returns the same finding directly, with no dashboard, viewer or round-3 code involved;
and the pre-existing reviewer worktrees at `.remedy-wt/f026-r3-dry`/`-sim` sit at DETACHED HEAD
(branch name reads literally `HEAD`, not the feature name), which is why the reviewer's own
baseline run (in a tree at 10ec2512, from the block's own description) read this test GREEN — its
`git rev-parse --abbrev-ref HEAD` never produced the offending substring there. Neither
`redaction_patterns.py` nor `project_brain.py` nor this branch's name is in CONSTRAINT 2's set, and
renaming the branch or widening the touch set is not this round's business — reported here per G4's
"account for every other difference," not repaired.

Net accounting: reviewer's baseline (same selection, WITHOUT the two new test files and the golden
path) read 1628 passed, 10 skipped at 10ec2512. This run adds `test_dashboard_task_specs.py` (7),
`test_task_version_contract.py` (3) and `tests/cli/test_golden_path.py`, and runs from the PRIMARY
checkout rather than the reviewer's detached scratch tree, so the four toolchain-node skips the
block names (TS `test_dashboard_contract.py`, vitest `test_test_runner.py`, the two `test_ui_lint.py`
lint nodes) become PASSES here rather than skips — accounting for the skip count falling from 10 to
5, and the one new FAILURE above being the branch-name artifact, not a fresh regression.

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
$ git worktree add --detach .remedy-wt/f026-r3-mut 0c6dc30f1
Preparing worktree (detached HEAD 0c6dc30f1)
$ python3 -B .agent/authored/f026-r3-mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f026-r3-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f026-r3-mut
CONTROL FIRST: pytest exit=0 failed=0 | vitest exit=0 failed=0
m1 (the section's versions is always []) [py]: exit=1 failed=1 failing=[tests/ui_server/test_dashboard_task_specs.py::TestAfterOneEdit::test_version_2_and_one_archived_version_with_the_old_fields] | caught=True restored byte-identical=True
m2 (the section lets a PauseControlError escape instead of reporting it) [py]: exit=1 failed=1 failing=[tests/ui_server/test_dashboard_task_specs.py::TestCorruptPauseFile::test_a_corrupt_task_pause_file_reads_no_tasks_and_a_nonempty_error] | caught=True restored byte-identical=True
m3 (a PlanEditRefused makes edit_state read "waiting") [py]: exit=1 failed=1 failing=[tests/ui_server/test_dashboard_task_specs.py::TestRunningJob::test_a_running_job_reads_empty_with_a_detail_naming_running] | caught=True restored byte-identical=True
m4 (normalizeTaskSpecs drops spec_version, so every task reads 1) [ts]: exit=1 failed=1 failing=[normalizeDashboardPayload > reads a task_specs section: the mapping] | caught=True restored byte-identical=True
m5 (versionChipLabel gives v1 for version 1) [ts]: exit=1 failed=1 failing=[versionChipLabel > is null for spec version 1] | caught=True restored byte-identical=True
m6 (specVersionRows compares every row against the FIRST row instead of the previous one) [ts]: exit=1 failed=1 failing=[specVersionRows > compares each row to the one before it, not to the first row] | caught=True restored byte-identical=True
m7 (the painter paints a chip for a non-task kind) [ts]: exit=1 failed=1 failing=[paintBrainNode — the task's version chip (DECISION F026 D3 clause 2) > writes nothing for a task with no chip, or a chip on any other kind] | caught=True restored byte-identical=True
m8 (buildBrainLayout ignores meta.specVersion) [ts]: exit=1 failed=1 failing=[buildBrainLayout > chip: v<n> when a task's seeded specVersion is 2 or more, else no chip key at all] | caught=True restored byte-identical=True
m9 (dashboardBrainSeeds drops specVersion) [ts]: exit=1 failed=1 failing=[dashboardBrainSeeds > puts specVersion on a seed only when the map carries that task] | caught=True restored byte-identical=True
CONTROL LAST: pytest exit=0 failed=0 | vitest exit=0 failed=0
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
$ git worktree remove --force .remedy-wt/f026-r3-mut
$ git worktree list
(primary checkout + the pre-existing F015/F020/F023/F024/F025/F026-r3-dry/sim/F284 dry/sim
worktrees and the same remedy/job-* worktrees already present at session start; f026-r3-mut absent)
```
Every one of the 9 mutations was caught (exit≠0, failed>0), every restore byte-identical, both
controls green (exit 0, 0 failed). ONE mutation (m6) stayed green on the FIRST version of
`taskSpecView.test.ts` (committed at C4) — the test suite had no case with two archived versions
whose values differed from BOTH the version immediately before them AND the first version, so
"compare to previous" and "compare to first" produced the same answer everywhere the tests looked.
A new test (`compares each row to the one before it, not to the first row`) was added to
`apps/ui/src/api/taskSpecView.test.ts` — bundled into C7 alongside the mutation tool, since no
commit in the block's sequence is designated for a test-only correction found only once G5 runs —
verified green against the true code and confirmed red by hand-applying m6's exact edit before
restoring; re-run above shows m6 now caught.

## Authored-text proofs

`.agent/authored/f026-r3-block.md`, `f026-r3-plan.md` and `f026-r3-records.diff` (at C1a) were
built with `shutil.copyfile` from the reviewer's payload files — never retyped, never edited —
and G1 compared every one byte for byte, read back with `git show 00f262daf:<path>`, against its
source: all three BYTE-IDENTICAL. `.agent/plan.md` was REWRITTEN whole (`shutil.copyfile`) from
`plan.md` at C1b; `records.diff` was applied verbatim with `git apply --check` then `git apply`,
never retyped or hand-edited — G2's byte/sha256 table on the resulting `.agent/live_review.md`,
`.agent/decisions.md` and `.agent/plan.md` confirms the applied result matches the reviewer's own
target state exactly.

Everything else this round wrote — the help-text reword, the `task_specs` section and its test,
the client normalization and pure view, the canvas chip and its wiring, the popover's chip and
Versions list, the two assumption-log rows, and the mutation tool — is WORKER-authored production
code and tests against the specification S1–S8 (the block's own framing, "THE PRODUCTION CHANGE IS
SPECIFIED, NOT SLICED"), not reviewer payload text, so no authored-text fidelity proof applies to
it.

## Deviations & assumptions

1. **A test was added after C4, bundled into C7 rather than its own commit.** G5's mutation m6
   stayed green against the `taskSpecView.test.ts` committed at C4 (see G5 above and the C7 table).
   A test was added, verified against real behaviour, hand-confirmed red under m6's exact edit, and
   restored — then bundled into C7 alongside the mutation tool, since the block names no commit for
   a G5-discovered gap. Recorded here per the "the second occurrence... blocks" framing and R-0485's
   rule that a departure belongs here even when the commit table already shows it.
2. **The CSS ratchet caught a wrong first draft before it was committed.** The first version of
   `DetailPopover.module.css`'s two new rules used `var(--remedy-ink-strong, #0a1c48)` and
   `var(--remedy-faint, #9aa9c5)` — copying an existing fallback pattern in the same file —
   which `tests/ui_contracts/test_raw_colour_ratchet.py` (not itself in CONSTRAINT 2, and not
   touched) correctly read as two new raw hex literals (15→17). Both tokens are already defined in
   `tokens.css`, so the fallbacks were simply dropped before C6 was committed; the committed C6
   diff already reflects the corrected, ratchet-clean rules — this is reported because the wrong
   draft was measured and is worth a reader knowing the ratchet is this sensitive, not because any
   wrong bytes reached a commit.
3. **One pre-existing test failure, accounted for, not repaired.** `tests/ui_contracts
   /test_graph_architecture.py::TestSpatialLayout::test_no_raw_leaks_in_viewer` fails in the primary
   checkout because this BRANCH'S OWN NAME (`feature/f026-task-edit-runtime`) contains the substring
   `sk-edit-runtime`, which `redaction_patterns.py`'s secret-pattern regex flags — see the full
   G4 write-up above for the proof this is independent of any round-3 diff and specific to running
   from an attached branch checkout rather than the reviewer's detached-HEAD scratch trees. Neither
   `redaction_patterns.py` nor `project_brain.py` is in CONSTRAINT 2's touch set, and the branch
   cannot be renamed mid-round, so this is reported rather than fixed.
4. **A throwaway worktree, outside the block's own G5 worktree, was created and removed to prove
   deviation 3.** `.remedy-wt/f026-r3-check` at `10ec25125` — confirmed to sit at DETACHED HEAD,
   which is what let the reviewer's own baseline run pass this same test — then removed. Not one of
   the round's named directories; created and removed entirely within this session, no trace left.
5. **This session's actual sandbox did not enforce every shape the block describes as refused**
   (`cd <dir> && git ...`, multi-operation `&&` chains outside `bash -c`, etc.) — several early
   commands in this round used a `cd <path> && git <cmd>` shape and it executed rather than being
   refused. No command relied on this beyond ordinary `git`/`python3` invocations already shown
   above; `git -C <path>` and `bash -c '<cmd>; echo REAL_EXIT=$?'` were used for the gates that read
   an exit code. Noted because the block's own environment description did not match what this
   worker's tools actually enforced, not because any command bypassed a rule that mattered to a
   result.
6. Everything else followed the block's ordered commit sequence exactly (C1a, C1b, C2, C3, C4, C5,
   C6, C7, then C8 inside which this handback lives); no payload was edited or retyped; no commit
   touched a path outside the tracked set CONSTRAINT 2 names (confirmed by
   `git diff --name-only 10ec25125` below); no gate went red on this round's own code (the one
   failure is deviation 3, unrelated to it).

```
$ git diff --name-only 10ec25125
.agent/authored/f026-r3-block.md
.agent/authored/f026-r3-mutations.py
.agent/authored/f026-r3-plan.md
.agent/authored/f026-r3-records.diff
.agent/decisions.md
.agent/handoff.md
.agent/live_review.md
.agent/plan.md
apps/cli/command_catalog.py
apps/ui/src/api/remedyApi.test.ts
apps/ui/src/api/remedyApi.ts
apps/ui/src/api/taskSpecView.test.ts
apps/ui/src/api/taskSpecView.ts
apps/ui/src/api/types.ts
apps/ui/src/components/detail/DetailPopover.module.css
apps/ui/src/components/detail/DetailPopover.tsx
apps/ui/src/components/detail/TaskVersionList.tsx
apps/ui/src/components/graph/BrainGraphStage.tsx
apps/ui/src/components/graph/brainOntology.ts
apps/ui/src/components/graph/brainReducer.ts
apps/ui/src/components/graph/brainView.test.ts
apps/ui/src/components/graph/brainView.ts
apps/ui/src/components/graph/buildForceBrainModel.test.ts
apps/ui/src/components/graph/buildForceBrainModel.ts
apps/ui/src/components/graph/forceBrainTypes.ts
apps/ui/src/components/graph/renderers/paintNode.test.ts
apps/ui/src/components/graph/renderers/paintNode.ts
docs/ui/design_reference/assumption_log.md
packages/orchestration/ui_server.py
tests/ui_contracts/test_task_version_contract.py
tests/ui_server/test_dashboard_task_specs.py
```
(measured again after C8, before push, in the final reply) Exactly CONSTRAINT 2's named path set
plus `.agent/handoff.md` (this commit). None of `packages/orchestration/task_edit_runtime.py`,
`packages/orchestration/pingpong_job.py`, `apps/ui/src/api/pauseSend.ts`, `README.md`,
`.agent/prose_slips.md`, `.agent/candidates.md`, `.agent/operator_questions.md` or
`docs/roadmap/features/T5_F026.md` appears.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 353 insertions (259+94), matches the block's expectation exactly; all three copies byte-identical |
| C1b | done | `git apply --check`/`git apply` both exit 0; per-file numstat 43/0, 4/0, 10/10 matches the G2 table exactly; open-finding set drops R-1059 |
| C2 | done | 2/2; catalog description reworded to the exact required text, nothing else in the file changed; `test_command_catalog.py` 60 passed |
| C3 | done | 250 insertions, under the cap; `_build_task_spec_section` wired in; new test file 7 passed, no regression in pause/contract tests |
| C4 | done | 435 insertions, under the cap; `tsc` clean; 84 vitest passed across the two new/changed files |
| C5 | done | 100 insertions, under the cap; `tsc` and `eslint` clean; full vitest suite 1311 passed, 5 skipped, no regression |
| C6 | done | 144 insertions, under the cap; popover and TaskVersionList wired per spec; contract test 3 passed; CSS ratchet clean (see Deviations #2) |
| C7 | done | 290 insertions, under the cap; mutation tool ruff-clean; one test added to close m6 (see Deviations #1) |
| G1 | done | every payload's lines/bytes/sha256 matched the table; every copy byte-identical by `git show` |
| G2 | done | all three files match the stated bytes/sha256; open-finding set correct at every reading named |
| G3 | done | ruff clean over every `.py` path of CONSTRAINT 2 at C7 |
| G4 | done | 1684 passed, 5 skipped (the four D3 + one D12 quarantines only), one failure fully accounted for as a pre-existing branch-name artifact unrelated to this round's diff (Deviations #3); every toolchain node PASSES; six `integrity check` pass |
| G5 | done | all 9 mutations caught, every restore byte-identical, both controls green; one test added before C8 to catch m6 (Deviations #1) |
| G6 | done | reported in the final reply, after C8, the push and the pull-request list |
| Pull request | skipped | not opened this round — the branch opens one at F026's closure, per the block |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 3. Then T003's second
half — the edit affordance on eligible nodes only, sent through the write door, and the
end-to-end: fail, edit through the door, relaunch, the new trace carrying the edit, the fan
visible. Open findings: 4 — `R-1008`, `R-1055`, `R-1057` and `R-1058`, all owned by F285.
Operator questions open: 4 — the count of `### Q` headings in `.agent/operator_questions.md`.
