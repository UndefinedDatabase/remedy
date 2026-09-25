# Handback — F023 Semantic zoom L0–L3 · Round 4

## Session

SESSION 1 of feature F023 · round 4 · rounds so far 4

This round booked round 3's PASS, recorded DECISION F023 D4, and landed T002's second half, the
L2 run detail: `runDetailModel.ts`, pure words for a run's verdict, round, tokens, duration and
retries, each a real value or a plain sentence saying why it is missing; `RunDetailPopover.tsx`
and its stylesheet, reading the rounds door, placed beside the L2 camera's centred run, with Open
diff, Why and a disabled Rerun whose reason is visible; `BrainGraphStage.tsx` mounting it for the
focused run and handing it the server token and the diff panel's opener; `RemedyShell.tsx` handing
the stage both; and `ForceBrainGraph.tsx` no longer opening the task's popover on a run click. All
five red-proof-verified with vitest goldens and the guard `tests/ui_contracts/test_run_detail_wiring.py`.
Ample context remained throughout this round; no session-limit pressure at any point.

## Range

Review of 12275971..HEAD

## Commits

### 8c48da408 F023 R4 C1a: copy round 4 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f023-r4-block.md | +249/-0 | copy of this round's block, verbatim |
| .agent/authored/f023-r4-plan.md | +36/-0 | copy of the plan.md payload |

285 insertions by `git show --numstat` — matches the block's expectation exactly; well under the
500-insertion STOP threshold and the 500-line commit cap.

### 8f7b2ce76 F023 R4 C1b: copy round 4 ledger and canvas diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f023-r4-ledger.diff | +66/-0 | copy of the ledger.diff payload |
| .agent/authored/f023-r4-canvas.diff | +92/-0 | copy of the canvas.diff payload |

158 insertions — matches the block's expectation exactly.

### fd7ef1a6f F023 R4 C1c: copy round 4 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f023-r4-mutations.py | +178/-0 | copy of the mutations.py payload |

178 insertions — matches the block's expectation exactly.

### 062177e54 F023 R4 C1d: copy round 4 product modules into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f023-r4-runDetailModel.ts | +170/-0 | copy of the runDetailModel.ts payload |
| .agent/authored/f023-r4-RunDetailPopover.tsx | +89/-0 | copy of the RunDetailPopover.tsx payload |
| .agent/authored/f023-r4-RunDetailPopover.module.css | +98/-0 | copy of the RunDetailPopover.module.css payload |

357 insertions — matches the block's expectation exactly.

### 28df59608 F023 R4 C1e: copy round 4 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f023-r4-runDetailModel.test.ts | +161/-0 | copy of the runDetailModel.test.ts payload |
| .agent/authored/f023-r4-test_run_detail_wiring.py | +68/-0 | copy of the test_run_detail_wiring.py payload |

229 insertions — matches the block's expectation exactly.

### 4c3845203 F023 R4 C2: book round 3's PASS, record D4, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +48/-0 | DECISION F023 D4 appended |
| .agent/live_review.md | +2/-0 | Gate: F023 R3 entry appended |
| .agent/plan.md | +13/-14 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 48/0 decisions.md, 2/0 live_review.md, 13/14 plan.md — matches the block's expectation
exactly.

### 1a5117b47 F023 R4 C3: show the L2 run detail beside the run the camera centred
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/BrainGraphStage.tsx | +20/-0 | mounts `RunDetailPopover` for the focused L2/L3 run, computed from the model, and takes `serverToken`/`onOpenDiff` props |
| apps/ui/src/components/graph/ForceBrainGraph.tsx | +3/-0 | a run click no longer also selects its task, via `isZoomRunKind` guard |
| apps/ui/src/components/graph/RunDetailPopover.module.css | +98/-0 | new file — the popover's stylesheet |
| apps/ui/src/components/graph/RunDetailPopover.tsx | +89/-0 | new file — the popover reading the rounds door, with Open diff, Why and disabled Rerun |
| apps/ui/src/components/graph/runDetailModel.ts | +170/-0 | new file — pure words for a run's verdict, round, tokens, duration and retries |
| apps/ui/src/components/shell/RemedyShell.tsx | +1/-1 | hands the stage `serverToken` and `setOpenDiffTaskId` as `onOpenDiff` |

`git apply --check` on canvas.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 20/0, 3/0, 98/0, 89/0, 170/0, 1/1 — matches the block's expectation exactly. All three
new files `git add`-ed (integrity's `relevant_untracked` check would otherwise fail).

### b7f54134a F023 R4 C4: golden the run detail's words and pin its wiring
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/runDetailModel.test.ts | +161/-0 | new file — vitest goldens over the words |
| tests/ui_contracts/test_run_detail_wiring.py | +68/-0 | new file — Python contract guard for the popover's wiring |

Insertions by `git show --numstat`: 161/0, 68/0 — matches the block's expectation exactly. Both
new files `git add`-ed.

### (this commit) F023 R4 C5: rewrite handoff for round 4
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this round-4 handback |

## External actions

- `git worktree add --detach .remedy-wt/f023-r4-mut b7f54134a` — succeeded, exit 0.
- `git worktree remove --force .remedy-wt/f023-r4-mut` — succeeded, exit 0 (after G5's mutation
  tool completed and restored every file byte-identical).
- `git worktree prune` — succeeded, exit 0.
- `git push origin feature/f023-semantic-zoom-l0-l3` — runs AFTER this commit lands; its real
  outcome is reported in the reply, since this handback cannot contain an outcome that happens
  after it.
- No pull request created — constraint 5/the block's C5 instruction forbids it this round; the
  branch opens one at F023's closure.
- No merge, no checkout of `main`, no branch deletion, no force-push, no `git stash` — none
  performed.

## Verification

```
$ ls .agent/STOP; echo $?
ls: cannot access '.agent/STOP': No such file or directory
2
(absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f023-semantic-zoom-l0-l3
$ git log --oneline -1
122759717 F023 R3 C5: rewrite handoff for round 3
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ (line count via newline-count, byte count, sha256 of .remedy-wt/f023-r4/block.md)
lines(newlines)=249 bytes=17064 sha256=34b526ac2c2cab2d766569614048726e9a335eeaae47c1d18b0997c54096c46b
```
Matches both readings given in the delegation message exactly (249 lines,
34b526ac2c2cab2d766569614048726e9a335eeaae47c1d18b0997c54096c46b) — R-0954.

```
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 f023-r1-dry, f023-r1-sim, f023-r2-dry, f023-r2-sim, f023-r3-dry, f023-r3-sim,
 f023-r4-dry, f023-r4-sim, 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
```

```
$ (line count, byte count, sha256 of each payload under .remedy-wt/f023-r4-payloads/)
RunDetailPopover.module.css   lines=98  bytes=2008  sha256=f74ec09058c7982e7ee511ca23a63419f3fe13ea384b9291fd008735f69bcf84
RunDetailPopover.tsx          lines=89  bytes=4111  sha256=a5519df21bcbe2660d0ab340fb5ea40d5f1b56bfffb799b79f51ef55d4df424a
canvas.diff                   lines=92  bytes=4934  sha256=f3fc5fdfacdf955ac4e6f9c2dbe7e876ef89aa2a11abfcdd3831b3eb947f7f17
ledger.diff                   lines=66  bytes=10297 sha256=c349bd0042f9ec35d524b6eefb6f8de51e17eb0159b70ec8da8cfbb91c9289e7
mutations.py                  lines=178 bytes=9141  sha256=4bc82dd21deeadcbef4474eca81670a6102cb880cd07a9f4e56c84a5266c6e9f
plan.md                       lines=36  bytes=1332  sha256=cc718e99296a0210193f4de7526ace6695b8c68c7dcc8522e3e0038c134f8da1
runDetailModel.test.ts        lines=161 bytes=7826  sha256=46a97e1e1279681bc3823aa42ca5d739627d58c60d15c4482897dafde7bebe3a
runDetailModel.ts             lines=170 bytes=8019  sha256=a0f3e15c091ca07bd03fe43e803224154b7c051456fbe093e2ede3c737ad127f
test_run_detail_wiring.py     lines=68  bytes=3505  sha256=6c48ca4ba0739e49f712f548fc49e426242476d0a3f342f8221329860f65d34a
```
All 9 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f023-r4-* blob, read with `git show <commit>:<path>`,
   against its source, plus the block copy)
f023-r4-block.md                       @ 8c48da408: IDENTICAL (sha 34b526ac...)
f023-r4-plan.md                        @ 8c48da408: IDENTICAL (sha cc718e99...)
f023-r4-ledger.diff                    @ 8f7b2ce76: IDENTICAL (sha c349bd00...)
f023-r4-canvas.diff                    @ 8f7b2ce76: IDENTICAL (sha f3fc5fdf...)
f023-r4-mutations.py                   @ fd7ef1a6f: IDENTICAL (sha 4bc82dd2...)
f023-r4-runDetailModel.ts              @ 062177e54: IDENTICAL (sha a0f3e15c...)
f023-r4-RunDetailPopover.tsx           @ 062177e54: IDENTICAL (sha a5519df2...)
f023-r4-RunDetailPopover.module.css    @ 062177e54: IDENTICAL (sha f74ec090...)
f023-r4-runDetailModel.test.ts         @ 28df59608: IDENTICAL (sha 46a97e1e...)
f023-r4-test_run_detail_wiring.py      @ 28df59608: IDENTICAL (sha 6c48ca4b...)
```
All 10 BYTE-IDENTICAL against their sources (G1).

```
$ git apply --check .remedy-wt/f023-r4-payloads/ledger.diff; echo $?
0
$ git apply .remedy-wt/f023-r4-payloads/ledger.diff; echo $?
0
```

```
$ (bytes/sha256 of the 3 ledger-touched files, read with `git show 4c3845203:<path>`)
.agent/live_review.md: bytes=301099  sha256=63485c3552ff84f3c79668d68aae45cdbdc1cd748011d92e26a69cd37c5c46d3 match=True
.agent/decisions.md:   bytes=2059971 sha256=6801f73ecbee7fbf09d10b12597f0f8a2f4ad9dbef7a21a282cd8f60e8c90d2c match=True
.agent/plan.md:        bytes=1332    sha256=cc718e99296a0210193f4de7526ace6695b8c68c7dcc8522e3e0038c134f8da1 match=True
```
All 3 match the block's G2 table exactly.

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 12275971 and at 4c3845203 (C2)
12275971 open ids: ['R-1008']
4c3845203 (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ last non-empty line of .agent/live_review.md at C2:
"Gate: F023 R3 — the F023 round 3 entry: the booking of round 2, DECISION F023 D3, and the named
prerequisite of the L2 run detail, the read route serving each round of a task's latest run with
its client door. VERDICT PASS, NO DEVIATION DECLARED. ..."
```
Begins `Gate: F023 R3 — ` exactly, as required (G2).

```
$ git diff --name-only 28df59608 4c3845203
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Names exactly the paths of the G2 table — matches exactly (G2).

```
$ (bytes/sha256 of the product and test files, read with `git show <commit>:<path>`)
1a5117b47 apps/ui/src/components/graph/BrainGraphStage.tsx:               bytes=5503  match=True
1a5117b47 apps/ui/src/components/graph/ForceBrainGraph.tsx:               bytes=19621 match=True
1a5117b47 apps/ui/src/components/shell/RemedyShell.tsx:                   bytes=13170 match=True
1a5117b47 apps/ui/src/components/graph/runDetailModel.ts:                 bytes=8019  match=True
1a5117b47 apps/ui/src/components/graph/RunDetailPopover.tsx:              bytes=4111  match=True
1a5117b47 apps/ui/src/components/graph/RunDetailPopover.module.css:       bytes=2008  match=True
b7f54134a apps/ui/src/components/graph/runDetailModel.test.ts:            bytes=7826  match=True
b7f54134a tests/ui_contracts/test_run_detail_wiring.py:                   bytes=3505  match=True
```
All 8 match the block's G3 table exactly.

```
$ git diff --name-only 4c3845203 1a5117b47
apps/ui/src/components/graph/BrainGraphStage.tsx
apps/ui/src/components/graph/ForceBrainGraph.tsx
apps/ui/src/components/graph/RunDetailPopover.module.css
apps/ui/src/components/graph/RunDetailPopover.tsx
apps/ui/src/components/graph/runDetailModel.ts
apps/ui/src/components/shell/RemedyShell.tsx
$ git diff --name-only 1a5117b47 b7f54134a
apps/ui/src/components/graph/runDetailModel.test.ts
tests/ui_contracts/test_run_detail_wiring.py
```
Both name exactly the paths C3 and C4 list — matches exactly (G3).

```
$ python3 -m ruff check tests/ui_contracts/test_run_detail_wiring.py
All checks passed!
REAL_EXIT=0
```
Matches exactly (G3).

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts
  tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/orchestration/test_roadmap_index.py tests/orchestration/test_block_lint.py
  tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs
  tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252)
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252)
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252)
1513 passed, 5 skipped in 85.45s (0:01:25)
REAL_EXIT=0
```
Exit 0. All 5 skips are the pre-existing D3/D12 quarantine nodes; none of the four toolchain nodes
the block names (the two eslint nodes in `test_ui_lint.py`, the `tsc --noEmit` node in
`test_dashboard_contract.py`, the vitest node in `test_test_runner.py`) appear in the `-rs`
summary, confirming each PASSED rather than skipped, as the block requires (G4). The count differs
from the reviewer's sim reading (1466 passed, 10 skipped, golden path excluded) because this run,
in the primary checkout, includes the golden path and runs the four toolchain nodes for real
instead of skipping them, exactly as the block anticipates.

```
$ bash -c 'python3 -m apps.cli.main integrity check --json; echo "REAL_EXIT=$?"'
{"check_count": 6, "checks": [
  {"name": "handler_import", "status": "pass", "message": "handlers=157"},
  {"name": "live_review_verdict", "status": "pass", "message": "last Gate verdict PASS"},
  {"name": "plan_consistency", "status": "pass", "message": "unchecked=0, context_complete=False"},
  {"name": "relevant_untracked", "status": "pass", "message": "untracked=0, relevant=0"},
  {"name": "repo_root_hygiene", "status": "pass", "message": "no reviewer scratch, evidence dir or archive at the root"},
  {"name": "high_blockers_open", "status": "pass", "message": "no open blocker/high findings"}
], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0 — matches exactly (G4).

```
$ git worktree add --detach .remedy-wt/f023-r4-mut b7f54134a
Preparing worktree (detached HEAD b7f54134a)
REAL_EXIT=0
$ python3 -B .remedy-wt/f023-r4-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f023-r4-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=13 | guard exit=0 failed=0 passed=5
m1  (a round the ledger logged without a review is not counted): v3 g0 caught=True restored=True
m2  (an earlier run is taken for the latest): v2 g0 caught=True restored=True
m3  (the reviewer's tokens are filled from the builder's): v2 g0 caught=True restored=True
m4  (a running run is described from the report): v1 g0 caught=True restored=True
m5  (needs repair reads as failed): v1 g0 caught=True restored=True
m6  (a test run claims a timing): v1 g0 caught=True restored=True
m7  (Why opens a reviewer prompt of another round): v1 g0 caught=True restored=True
m8  (a long duration is written in seconds only): v2 g0 caught=True restored=True
m9  (a task with no run reads as an unreadable report): v1 g0 caught=True restored=True
m10 (the detail shows a report read for another task): v0 g1 caught=True restored=True
m11 (Rerun is enabled): v0 g1 caught=True restored=True
m12 (the detail becomes a dialog Escape skips): v0 g1 caught=True restored=True
m13 (the stage looks the run up in the filtered view): v0 g1 caught=True restored=True
m14 (a run click opens its task's popover too): v0 g1 caught=True restored=True
m15 (the shell hands the stage no token): v0 g1 caught=True restored=True
CONTROL LAST: vitest exit=0 failed=0 passed=13 | guard exit=0 failed=0 passed=5
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every mutation's vitest-failed / guard-failed count matches the block's stated reading exactly
(m1 v3g0 through m15 v0g1), both controls green as stated (control first/last), every `restored
byte-identical` reading True, and the final line reads exactly `ALL MUTATIONS CAUGHT AND RESTORED
CLEANLY: True` — matches the block's G5 table exactly.

```
$ git worktree remove --force .remedy-wt/f023-r4-mut; echo $?
0
$ git worktree prune; echo $?
0
$ git worktree list
(primary + the same 43 reviewer worktrees + 4 job-* worktrees as before; the mut worktree gone)
```

## Closure pins

None — this round does not close F023 (T002's second half only, of a multi-slice feature). No
package, no evidence job, no accepted head at this round.

## Authored-text proofs

All 10 authored copies under `.agent/authored/f023-r4-*` (the block copy plus the nine payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 10 BYTE-IDENTICAL (G1 above). `ledger.diff` was applied with `git apply` after `git apply
--check` passed (exit 0 both), never retyped or edited; the resulting 3 files were verified by
byte count and sha256 against the block's G2 table — MATCH. `.agent/plan.md` was rewritten whole
via `shutil.copyfile` from the payload source — never retyped — and confirmed MATCH against both
the PAYLOADS table and the G2 table. `canvas.diff` was applied with `git apply` after `git apply
--check` passed (exit 0 both), never retyped or edited; the resulting edited files
(`BrainGraphStage.tsx`, `ForceBrainGraph.tsx`, `RemedyShell.tsx`) plus `runDetailModel.ts`,
`RunDetailPopover.tsx`, `RunDetailPopover.module.css`, `runDetailModel.test.ts` and
`test_run_detail_wiring.py` (each copied whole via `shutil.copyfile`) were all confirmed MATCH
against the PAYLOADS table and the G3 table.

## Deviations & assumptions

None. Every commit landed in the block's stated order: C1a, C1b, C1c, C1d, C1e, C2, C3, C4, then
C5 (this handback), exactly as ordered. No payload was edited, retyped or repaired. G1 through G5
ran before C5 was written, as required. The round's tracked path set through C4 was exactly the
ten `.agent/authored/f023-r4-*` copies, `.agent/live_review.md`, `.agent/decisions.md`,
`.agent/plan.md`, the three paths `canvas.diff` edited (`BrainGraphStage.tsx`,
`ForceBrainGraph.tsx`, `RemedyShell.tsx`), and the five new files the payloads name
(`runDetailModel.ts`, `RunDetailPopover.tsx`, `RunDetailPopover.module.css`,
`runDetailModel.test.ts`, `test_run_detail_wiring.py`) — confirmed by `git diff --name-only
12275971 HEAD` before this commit; C5 adds exactly `.agent/handoff.md`. Nothing was merged this
round: no `gh pr merge`, no `gh pr create`, no checkout of `main`, no branch deletion, no
force-push, no `git stash` — per constraint 5. The worktree G5 added (`.remedy-wt/f023-r4-mut`)
was removed as G5's last action; every other reviewer worktree (`f015-r*`, `f020-r*`,
`f023-r1-sim`, `f023-r1-dry`, `f023-r2-sim`, `f023-r2-dry`, `f023-r3-sim`, `f023-r3-dry`,
`f023-r4-sim`, `f023-r4-dry`, `f284-r*`) and every `job-*` worktree/branch were left untouched —
per constraint 6. The full suite was not run — per constraint 7, this feature's one full-suite run
belongs to its closure.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 285 insertions, matches block's expectation exactly; well under the 500-insertion STOP threshold and the 500-line cap |
| C1b | done | 158 insertions, matches exactly |
| C1c | done | 178 insertions, matches exactly |
| C1d | done | 357 insertions, matches exactly |
| C1e | done | 229 insertions, matches exactly |
| C2 | done | ledger.diff apply --check and apply both exit 0; 48/0, 2/0, 13/14 insertions/deletions match exactly |
| C3 | done | canvas.diff apply --check and apply both exit 0; 20/0, 3/0, 98/0, 89/0, 170/0, 1/1 insertions match exactly; all three new files `git add`-ed |
| C4 | done | 161/0, 68/0 insertions match exactly; both new files `git add`-ed |
| G1 | done | all 9 payload digests and 10 authored-copy comparisons matched |
| G2 | done | all 3 named file digests matched; open set R-1008 alone at both; last-line prefix matched; diff --name-only matched |
| G3 | done | all 8 named file digests matched; both diff --name-only checks matched; ruff clean |
| G4 | done | 1513 passed, 5 skipped (all pre-existing quarantine, none of the 4 named toolchain nodes), exit 0; integrity check 6/6 pass, fail_count 0 |
| G5 | done | all 15 mutations caught with exact v/g-count matches to the block's table, both controls green, all restores byte-identical, final line matches exactly |
| G6 | pending | runs after this commit (git status, git log, worktree list, push, gh pr list); reported in the reply |
| PUSH | pending | `git push origin feature/f023-semantic-zoom-l0-l3`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 4. Then T003 — the L3
evidence panel with its lazy tabs, Open diff and Why moved onto its tabs, and the deep links. Open
findings: 1. Operator questions open: 3.
