# Handback — F024 Phase timeline with scrubber · Round 2

## Session

SESSION 1 of feature F024 · round 2 · rounds so far 2

Ample context remained throughout this round; no session-limit pressure at any point (roughly
two-thirds of the budget remained at the point this handback was written).

## Range

Review of 78d60af2d..HEAD

## Commits

### aa32c88a1 F024 R2 C1a: copy round 2 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r2-block.md | +237/-0 | copy of this round's block, verbatim |
| .agent/authored/f024-r2-plan.md | +34/-0 | copy of the plan.md payload |

271 insertions by `git show --numstat` (block's line count 237 + 34) — matches the block's
expectation exactly; well under the 500-insertion STOP threshold.

### e29f50e1e F024 R2 C1b: copy round 2 ledger diff and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r2-ledger.diff | +64/-0 | copy of the ledger.diff payload |
| .agent/authored/f024-r2-mutations.py | +167/-0 | copy of the mutations.py payload |

231 insertions by `git show --numstat` — matches the block's expected 231 exactly.

### 9f25e6301 F024 R2 C1c: copy round 2 product module into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r2-scrubSnapshots.ts | +147/-0 | copy of the scrubSnapshots.ts payload |

147 insertions by `git show --numstat` — matches the block's expected 147 exactly.

### 60c0bfc48 F024 R2 C1d: copy round 2 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r2-scrubSnapshots.test.ts | +236/-0 | copy of the scrubSnapshots.test.ts payload |
| .agent/authored/f024-r2-test_scrub_snapshots.py | +57/-0 | copy of the test_scrub_snapshots.py payload |

293 insertions by `git show --numstat` — matches the block's expected 293 (236+57) exactly.

### c677183b9 F024 R2 C2: book round 1's PASS, record D2, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +46/-0 | DECISION F024 D2 appended, via ledger.diff |
| .agent/live_review.md | +2/-0 | round 1's Gate entry appended, via ledger.diff |
| .agent/plan.md | +10/-12 | rewritten to the plan.md payload |

`git apply --check` on ledger.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 46/0 decisions.md, 2/0 live_review.md, 10/12 plan.md — matches the block's expectation
exactly.

### 91578e97f F024 R2 C3: add the scrubber's snapshot memo
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/timeline/scrubSnapshots.ts | +147/-0 | new module: the snapshot memo (every 200 seq, cap 64, lazy rebuild, farthest-first eviction, refetch reset) |

147 insertions by `git show --numstat` — matches the block's expected 147 exactly.

### fcaede0b3 F024 R2 C4: hold the memo to a fresh fold at fuzzed positions, and guard its spacing
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/timeline/scrubSnapshots.test.ts | +236/-0 | vitest property test: memo state at fuzzed positions equals a fresh reduction of the prefix |
| tests/ui_contracts/test_scrub_snapshots.py | +57/-0 | Python contract guard over the memo's spacing/cap |

236 and 57 insertions by `git show --numstat` — matches the block's expected 236 and 57 exactly.

### (this commit) F024 R2 C5: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-reference) | this handback, rewritten for round 2 |

Per the handback template's self-reference exception: a handback cannot table the commit that
writes it. Insertions reported in the final reply, as measured by `git show --numstat` after the
commit.

## External actions

`git worktree add --detach .remedy-wt/f024-r2-mut fcaede0b3` for G5: success (exit 0).
`git worktree remove --force .remedy-wt/f024-r2-mut`: success (exit 0). `git worktree prune`:
success (exit 0). The push after this commit and its real outcome are reported in the final reply,
per the block's ordering (G1–G5 run before this handback is written; this commit and the push
follow). No `gh pr create` this round — the block orders none; the branch already carries PR #278
opened at F023's closure and reused for F024 per the round 1 record; no PR action this round in
any case.

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
feature/f024-phase-timeline-scrubber
$ git log --oneline -1
78d60af2d F024 R1 C5: rewrite handoff for round 1
```
All BEFORE ANYTHING ELSE step 2 checks passed at round start.

```
$ (line count and sha256 of .remedy-wt/f024-r2/block.md, measured)
line_count: 237
sha256: 8da5d69b1e0c1d1c7cc8b83e903c4557a30ecfae826b70a1100f73f05aeaeaca
```
Matches both readings given in the delegation message exactly (237 lines,
8da5d69b1e0c1d1c7cc8b83e903c4557a30ecfae826b70a1100f73f05aeaeaca) — R-0954.

```
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 20 f023-*-dry/sim r1-r9, f023-r10-dry, f023-r10-sim, f024-r1-dry, f024-r1-sim,
 f024-r2-dry, f024-r2-sim, 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
```

```
$ (lines/bytes/sha256 of each payload under .remedy-wt/f024-r2-payloads/)
ledger.diff              lines=64  bytes=9590  sha256=a7af36b247fc24acc1958dfbe6384d80e1b464994e131d89084c38480a1f0f82
mutations.py             lines=167 bytes=8177  sha256=10448dcdcbf62cf1b1db09a5b369ef2eb67177d80a76388187c8510671f76295
plan.md                  lines=34  bytes=1321  sha256=6d461d078ff4f572e5bf010d67ed205159f776f38c7a6d914ca73f39393d606b
scrubSnapshots.test.ts   lines=236 bytes=10046 sha256=8a3f62dd6940956564f45402365396abe0dd03390f908dcf1b54e408844511ae
scrubSnapshots.ts        lines=147 bytes=5533  sha256=c898fd7562f7a0c4fd40ee2184ca117d0c24bb0254818b0ad422dfa6f41266d2
test_scrub_snapshots.py  lines=57  bytes=2884  sha256=0a6fab2256c80ca618e244ef598c8b0235c5d765ff1b2ae854fd9d8b3f1bb6ff
```
All 6 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f024-r2-* blob against its source, via `git show <commit>:<path>`)
f024-r2-block.md                @ aa32c88a1: IDENTICAL (sha 8da5d69b...)
f024-r2-plan.md                 @ aa32c88a1: IDENTICAL (sha 6d461d07...)
f024-r2-ledger.diff             @ e29f50e1e: IDENTICAL (sha a7af36b2...)
f024-r2-mutations.py            @ e29f50e1e: IDENTICAL (sha 10448dcd...)
f024-r2-scrubSnapshots.ts       @ 9f25e6301: IDENTICAL (sha c898fd75...)
f024-r2-scrubSnapshots.test.ts  @ 60c0bfc48: IDENTICAL (sha 8a3f62dd...)
f024-r2-test_scrub_snapshots.py @ 60c0bfc48: IDENTICAL (sha 0a6fab22...)
```
All 7 BYTE-IDENTICAL against their sources (G1).

```
$ git apply --check .remedy-wt/f024-r2-payloads/ledger.diff; echo $?
0
$ git apply .remedy-wt/f024-r2-payloads/ledger.diff; echo $?
0
```

```
$ (bytes/sha256 of the files named in the block's G2 table, read at c677183b9)
.agent/live_review.md   bytes=299296   sha256=a4ac18dee4af1177cd028bef5665e702c280e92482ee6d0cad9c390e464d69f9 match=True
.agent/decisions.md     bytes=2080562  sha256=64fa6f4fb7a71774eed6e6e9598025be9536e5300d439616ac4ebba2f84a2aa1 match=True
.agent/plan.md          bytes=1321     sha256=6d461d078ff4f572e5bf010d67ed205159f776f38c7a6d914ca73f39393d606b match=True
```
All 3 match the block's G2 table exactly.

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 78d60af2d and at c677183b9 (C2)
78d60af2d open ids: ['R-1008']
c677183b9 (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ (lines C2's own diff adds to .agent/live_review.md, via `git show C2 -- .agent/live_review.md`)
+
+Gate: F024 R1 — the F024 round 1 entry ... (full gate-entry line)
```
2 lines added, exactly one beginning "Gate: F024 R1 — ", matching the block's stated reading
exactly (G2).

```
$ (ledger's last line at C2)
Gate: F024 R1 — the F024 round 1 entry ...
```
Begins "Gate: F024 R1 — ", matching the block's requirement exactly (G2).

```
$ git diff --name-only 60c0bfc48 c677183b9
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Matches the G2 path table exactly.

```
$ (sha256 of the product and test files at their commits)
C3 apps/ui/src/components/timeline/scrubSnapshots.ts       bytes=5533  sha256=c898fd7562f7a0c4fd40ee2184ca117d0c24bb0254818b0ad422dfa6f41266d2 match=True
C4 apps/ui/src/components/timeline/scrubSnapshots.test.ts  bytes=10046 sha256=8a3f62dd6940956564f45402365396abe0dd03390f908dcf1b54e408844511ae match=True
C4 tests/ui_contracts/test_scrub_snapshots.py               bytes=2884  sha256=0a6fab2256c80ca618e244ef598c8b0235c5d765ff1b2ae854fd9d8b3f1bb6ff match=True
```
All 3 match the block's G3 table exactly.

```
$ git diff --name-only c677183b9 91578e97f
apps/ui/src/components/timeline/scrubSnapshots.ts
$ git diff --name-only 91578e97f fcaede0b3
apps/ui/src/components/timeline/scrubSnapshots.test.ts
tests/ui_contracts/test_scrub_snapshots.py
```
Both match the block's G3 path lists exactly.

```
$ python3 -m ruff check tests/ui_contracts/test_scrub_snapshots.py
All checks passed!
REAL_EXIT=0
```

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py
  tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/orchestration/test_block_lint.py
  tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs
  tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1503 passed, 5 skipped in 84.46s (0:01:24)
REAL_EXIT=0
```
The reviewer's sim run WITHOUT the golden path read `1456 passed, 10 skipped` at exit 0; this
worker's run, WITH the golden path file and inside the primary checkout (where the four toolchain
nodes run instead of skip), reads `1503 passed, 5 skipped` at exit 0. None of the five SKIPPED
lines are any of the four toolchain nodes the block names (`tests/ui_contracts/test_ui_lint.py`'s
two eslint nodes, the `tsc --noEmit` node in `test_dashboard_contract.py`, or the vitest node in
`test_test_runner.py`) — all four ran and PASSED, as required.

```
$ python3 -m apps.cli.main integrity check --json
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
All six checks `pass`, `fail_count` 0 (G4).

```
$ git worktree add --detach .remedy-wt/f024-r2-mut fcaede0b3
Preparing worktree (detached HEAD fcaede0b3)
REAL_EXIT=0

$ python3 -B .remedy-wt/f024-r2-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f024-r2-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f024-r2-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=14 | guard exit=0 failed=0 passed=4
m1 (the boundary rounds down one seq early): vitest exit=1 failed=3 passed=11 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m2 (a snapshot also holds the row at its boundary): vitest exit=1 failed=7 passed=7 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m3 (the ledger is kept in arrival order): vitest exit=1 failed=4 passed=10 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m4 (a gap-filling row leaves the snapshots above it): vitest exit=1 failed=2 passed=12 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m5 (a row at the head drops every snapshot): vitest exit=1 failed=3 passed=11 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m6 (a reset keeps the old snapshots): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m7 (the cap drops the nearest snapshot): vitest exit=1 failed=2 passed=12 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m8 (a tie drops the higher snapshot): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m9 (the cap is never enforced): vitest exit=1 failed=3 passed=11 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m10 (a missing snapshot is always rebuilt from the seed): vitest exit=1 failed=1 passed=13 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m11 (the memo seeds with today's statuses): vitest exit=1 failed=8 passed=6 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
m12 (the spacing drifts from the spec): vitest exit=1 failed=2 passed=12 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
m13 (the memo reaches for the wall clock): vitest exit=0 failed=0 passed=14 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
m14 (every position folds from the seed): vitest exit=1 failed=6 passed=8 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m15 (a position also folds the row after it): vitest exit=1 failed=7 passed=7 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=14 | guard exit=0 failed=0 passed=4
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every count matches the reviewer's stated sim-tree reading exactly (control first v14/g4 exit 0;
m1 v3g0 .. m15 v7g0 as tabulated in the block's G5 section; control last equal to control first;
every `restored byte-identical` True; final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`).

```
$ git worktree remove --force .remedy-wt/f024-r2-mut; echo $?
0
$ git worktree prune; echo $?
0
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 20 f023-*-dry/sim r1-r9, f023-r10-dry, f023-r10-sim, f024-r1-dry, f024-r1-sim,
 f024-r2-dry, f024-r2-sim, 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
```
`f024-r2-mut` is gone; every worktree constraint 6 names remains.

## Evidence and package summary

Not applicable this round: T002 lands product code and its guard/property test under an open
feature; no closure, no evidence job, no review package is produced at a T-slice round. This
section is carried forward as N/A per the block's own scope (book round 1's PASS + D2 + T002, not
closure).

## Authored-text proofs

All 7 authored copies under `.agent/authored/f024-r2-*` (the block copy, plan.md, ledger.diff,
mutations.py, scrubSnapshots.ts, scrubSnapshots.test.ts, test_scrub_snapshots.py) were built by
`shutil.copyfile` from source to destination — never retyped, never edited. Each was read back
with `git show <commit>:<path>` and compared byte for byte against its source: all 7
BYTE-IDENTICAL (G1 above). `ledger.diff` was applied with `git apply` after `git apply --check`
passed (exit 0, both). `.agent/plan.md` was rewritten whole via `shutil.copyfile` from the payload
source — never retyped — and confirmed MATCH against both the PAYLOADS table and the G2 table.
`scrubSnapshots.ts` was copied whole via `shutil.copyfile` into
`apps/ui/src/components/timeline/scrubSnapshots.ts` and confirmed MATCH against the G3 table.
`scrubSnapshots.test.ts` and `test_scrub_snapshots.py` were likewise copied whole via
`shutil.copyfile` into their destinations and confirmed MATCH against the G3 table.

## Deviations & assumptions

None. All eight commits landed in the block's stated order: C1a, C1b, C1c, C1d, C2, C3, C4, C5,
exactly as ordered. No payload was edited, retyped or repaired. G1 through G5 ran before this
handback was written, per the block's instruction ("G1 to G5 run before C5 is written"). The
`.remedy-wt/f024-r2-mut` worktree G5 required was added and removed within this round, as its last
action, and `git worktree prune` was run after. No other worktree was added or removed this round;
every worktree named in constraint 6 (`f015-r*`, `f020-r*`, `f023-r*`, `f284-r*`, `job-*`, and the
reviewer's own `f024-r2-sim`/`f024-r2-dry`, plus the round 1 `f024-r1-sim`/`f024-r1-dry`) was left
untouched. No `git stash` was used, nothing was merged, no pull request was created, no
force-push occurred.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 271 insertions, matches block's expectation exactly (237+34); well under the 500-insertion STOP threshold |
| C1b | done | 231 insertions, matches block's expected 231 exactly |
| C1c | done | 147 insertions, matches block's expected 147 exactly |
| C1d | done | 293 insertions (236+57), matches block's expected 293 exactly |
| C2 | done | ledger.diff apply --check and apply both exit 0; 46/0, 2/0, 10/12 insertions/deletions match exactly |
| C3 | done | 147 insertions, matches block's expected 147 exactly |
| C4 | done | 236 and 57 insertions, matches block's expected 236 and 57 exactly |
| G1 | done | all 6 payload digests and 7 authored-copy comparisons matched |
| G2 | done | all 3 named file digests matched; open-id set, added-lines count/content, ledger last line, and path set all matched |
| G3 | done | all 3 product/test digests matched; both path-name-only diffs matched; ruff clean |
| G4 | done | 1503 passed, 5 skipped, exit 0; all four toolchain nodes ran and passed (none skipped); integrity check 6/6 pass |
| G5 | done | control first/last and all 15 mutations matched the reviewer's stated readings exactly; all restored byte-identical; final line True |
| C5 | done | this handback |
| PUSH | pending | `git push origin feature/f024-phase-timeline-scrubber` after this commit; reported in the final reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2. Then T003 — the bar
reading the phase mapping and the memo, the scrubber with its keyboard, the LIVE toggle with the
SCRUBBED banner and the capped catch-up, and the end-to-end on a live fake job and the demo
recording. Open findings: 1. Operator questions open: 3.
