# Handback — F024 Phase timeline with scrubber · Round 1

## Session

SESSION 1 of feature F024 · round 1 · rounds so far 1

Ample context remained throughout this round; no session-limit pressure at any point (roughly
half the budget remained at the point this handback was written).

## Range

Review of 1bb3a35dc..HEAD

## Commits

### cf6406f01 F024 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r1-block.md | +245/-0 | copy of this round's block, verbatim |
| .agent/authored/f024-r1-context.md | +37/-0 | copy of the context.md payload |
| .agent/authored/f024-r1-plan.md | +36/-0 | copy of the plan.md payload |

318 insertions by `git show --numstat` (block's line count 245 + 73) — matches the block's
expectation exactly; well under the 500-insertion STOP threshold.

### d5cfbbe39 F024 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r1-claim.diff | +147/-0 | copy of the claim.diff payload |

147 insertions by `git show --numstat` — matches the block's expected 147 exactly.

### 630df5966 F024 R1 C1c: copy round 1 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r1-mutations.py | +170/-0 | copy of the mutations.py payload |

170 insertions by `git show --numstat` — matches the block's expected 170 exactly.

### 65a64a850 F024 R1 C1d: copy round 1 product module into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r1-phaseMapping.ts | +213/-0 | copy of the phaseMapping.ts payload |

213 insertions by `git show --numstat` — matches the block's expected 213 exactly.

### 11a1b9a47 F024 R1 C1e: copy round 1 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f024-r1-phaseMapping.test.ts | +325/-0 | copy of the phaseMapping.test.ts payload |
| .agent/authored/f024-r1-test_phase_mapping.py | +70/-0 | copy of the test_phase_mapping.py payload |

395 insertions by `git show --numstat` — matches the block's expected 395 (325+70) exactly.

### 0788f61a1 F024 R1 C2: claim F024, re-head the live review record, book F023 R10, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +13/-15 | rewritten to the context.md payload |
| .agent/decisions.md | +59/-0 | DECISION F024 D1 appended, via claim.diff |
| .agent/live_review.md | +25/-26 | re-head above `## Findings`, F023 R10 gate entry appended, via claim.diff |
| .agent/plan.md | +23/-15 | rewritten to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F024's line `[ ]` → `[~]`, via claim.diff |

`git apply --check` on claim.diff: exit 0. `git apply`: exit 0. Insertions/deletions by `git show
--numstat`: 13/15 context.md, 59/0 decisions.md, 25/26 live_review.md, 23/15 plan.md, 1/1
STATUS.md — matches the block's expectation exactly.

### c9f83db51 F024 R1 C3: add the phase mapping, its boundaries and the sub-glyph extraction
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/timeline/phaseMapping.ts | +213/-0 | new module: phase mapping table, phase boundaries, sub-glyph extraction |

213 insertions by `git show --numstat` — matches the block's expected 213 exactly.

### cc4fd4e73 F024 R1 C4: golden the phase boundaries and sub-glyphs, and guard the table
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/timeline/phaseMapping.test.ts | +325/-0 | vitest goldens on fixture ledgers and the demo recording |
| tests/ui_contracts/test_phase_mapping.py | +70/-0 | Python contract guard over the mapping tables |

325 and 70 insertions by `git show --numstat` — matches the block's expected 325 and 70 exactly.

### (this commit) F024 R1 C5: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | (self-reference) | this handback, rewritten for round 1 |

Per the handback template's self-reference exception: a handback cannot table the commit that
writes it. Insertions reported in the final reply, as measured by `git show --numstat` after the
commit.

## External actions

`git checkout -b feature/f024-phase-timeline-scrubber` at round start (from `main` at `1bb3a35dc`):
success. `git worktree add --detach .remedy-wt/f024-r1-mut cc4fd4e73` for G5: success (exit 0).
`git worktree remove --force .remedy-wt/f024-r1-mut`: success (exit 0). `git worktree prune`:
success (exit 0). The push after this commit and its real outcome are reported in the final reply,
per the block's ordering (G1–G5 run before this handback is written; this commit and the push
follow). No `gh pr create` this round — the block orders none; the branch opens a pull request at
F024's closure.

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
main
$ git log --oneline -1
1bb3a35dc Merge pull request #278 from UndefinedDatabase/feature/f023-semantic-zoom-l0-l3
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ git checkout -b feature/f024-phase-timeline-scrubber
Switched to a new branch 'feature/f024-phase-timeline-scrubber'
```

```
$ (line count and sha256 of .remedy-wt/f024-r1/block.md, measured with python3)
byte_count: 16542
line_count: 245
sha256: e3a55df5c3375a4630019038678aa86b8fd40fc47992a3e5118920f8a5d5d1e3
```
Matches both readings given in the delegation message exactly (245 lines,
e3a55df5c3375a4630019038678aa86b8fd40fc47992a3e5118920f8a5d5d1e3) — R-0954.

```
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 20 f023-*-dry/sim r1-r9, f023-r10-dry, f023-r10-sim, f024-r1-dry, f024-r1-sim,
 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
```

```
$ (lines/bytes/sha256 of each payload under .remedy-wt/f024-r1-payloads/)
claim.diff             lines=147 bytes=16701 sha256=ad11fd63156c57b0d46392fbf27431e94bcff84b0451f57c8104542650a0d154
context.md             lines=37  bytes=1625  sha256=d6eba45432667408969eefe383de52fe9f53c7bee13a3025e0bffd3cc26ce491
mutations.py           lines=170 bytes=8314  sha256=91cec40171bd9ae07e2d3242e8a69c83c58e0c708e0b10605804b93554583c46
phaseMapping.test.ts   lines=325 bytes=12392 sha256=2cd5f7b9a0931112f5389b12dcd958f8a352080bb857bd3be37798bb3ea41b3c
phaseMapping.ts        lines=213 bytes=8581  sha256=ae226e2e5386c29a163a2a7b3ea66108a97cba80a36c7df9e0359d0bafa7a27e
plan.md                lines=36  bytes=1448  sha256=32b86e0315f74236cd404c7b039d52fee983191377c4c558101df1b2cb7186cf
test_phase_mapping.py  lines=70  bytes=3525  sha256=ce219529777be40b23e506b221debcefbf427b149b658ae3ff885e81a8f97de7
```
All 7 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f024-r1-* blob against its source, via `git show <commit>:<path>`)
f024-r1-block.md              @ cf6406f01: IDENTICAL (sha e3a55df5...)
f024-r1-plan.md                @ cf6406f01: IDENTICAL (sha 32b86e03...)
f024-r1-context.md             @ cf6406f01: IDENTICAL (sha d6eba454...)
f024-r1-claim.diff             @ d5cfbbe39: IDENTICAL (sha ad11fd63...)
f024-r1-mutations.py           @ 630df5966: IDENTICAL (sha 91cec401...)
f024-r1-phaseMapping.ts        @ 65a64a850: IDENTICAL (sha ae226e2e...)
f024-r1-phaseMapping.test.ts   @ 11a1b9a47: IDENTICAL (sha 2cd5f7b9...)
f024-r1-test_phase_mapping.py  @ 11a1b9a47: IDENTICAL (sha ce219529...)
```
All 8 BYTE-IDENTICAL against their sources (G1).

```
$ git apply --check .remedy-wt/f024-r1-payloads/claim.diff; echo $?
0
$ git apply .remedy-wt/f024-r1-payloads/claim.diff; echo $?
0
```

```
$ (bytes/sha256 of the files named in the block's G2 table, read at 0788f61a1)
.agent/live_review.md   bytes=297529   sha256=1b4e6e5c04f9e091f70f5040af1a665341e6926da9e3d7cbafaf70020fef892c match=True
docs/roadmap/STATUS.md  bytes=51749    sha256=11008e7e63e83fff26f4328cff82b3a7a672677ba6ca08b0b20579bb73f107ee match=True
.agent/decisions.md     bytes=2076619  sha256=908506bfeeada0f41cd8dc9a0584906ce095762513b9fa734817d774052823d0 match=True
.agent/plan.md          bytes=1448     sha256=32b86e0315f74236cd404c7b039d52fee983191377c4c558101df1b2cb7186cf match=True
.agent/context.md       bytes=1625     sha256=d6eba45432667408969eefe383de52fe9f53c7bee13a3025e0bffd3cc26ce491 match=True
```
All 5 match the block's G2 table exactly.

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
  at 1bb3a35d and at 0788f61a1 (C2)
1bb3a35d open ids: ['R-1008']
0788f61a1 (C2) open ids: ['R-1008']
```
Reads R-1008 alone at both, matching the block's stated reading exactly (G2).

```
$ (structure checks on .agent/live_review.md at C2)
## Findings occurrences: 1
## Steps occurrences: 1
last line begins: "Gate: F023 R10 — "
```
All three match the block's requirement exactly (G2).

```
$ (docs/roadmap/STATUS.md F024 line at C2)
- [~] F024 — Phase timeline with scrubber
```
Matches the block's required reading exactly (G2).

```
$ git diff --name-only 11a1b9a47 0788f61a1
.agent/context.md
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
docs/roadmap/STATUS.md
```
Matches the G2 path table exactly.

```
$ (sha256 of the product and test files at their commits)
C3 apps/ui/src/components/timeline/phaseMapping.ts       bytes=8581  sha256=ae226e2e5386c29a163a2a7b3ea66108a97cba80a36c7df9e0359d0bafa7a27e match=True
C4 apps/ui/src/components/timeline/phaseMapping.test.ts  bytes=12392 sha256=2cd5f7b9a0931112f5389b12dcd958f8a352080bb857bd3be37798bb3ea41b3c match=True
C4 tests/ui_contracts/test_phase_mapping.py               bytes=3525  sha256=ce219529777be40b23e506b221debcefbf427b149b658ae3ff885e81a8f97de7 match=True
```
All 3 match the block's G3 table exactly.

```
$ git diff --name-only 0788f61a1 c9f83db51
apps/ui/src/components/timeline/phaseMapping.ts
$ git diff --name-only c9f83db51 cc4fd4e73
apps/ui/src/components/timeline/phaseMapping.test.ts
tests/ui_contracts/test_phase_mapping.py
```
Both match the block's G3 path lists exactly.

```
$ python3 -m ruff check tests/ui_contracts/test_phase_mapping.py
All checks passed!
REAL_EXIT=0
```

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py
  tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py
  tests/orchestration/test_block_lint.py tests/orchestration/test_event_names.py
  tests/test_agent_tooling.py tests/regression/test_resource_safety.py tests/docs
  tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1546 passed, 5 skipped in 89.03s (0:01:29)
REAL_EXIT=0
```
The reviewer's sim run WITHOUT the golden path read `1499 passed, 10 skipped` at exit 0; this
worker's run, WITH the golden path file and inside the primary checkout (where the four toolchain
nodes run instead of skip), reads `1546 passed, 5 skipped` at exit 0. None of the five SKIPPED
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
$ git worktree add --detach .remedy-wt/f024-r1-mut cc4fd4e73
Preparing worktree (detached HEAD cc4fd4e73)
REAL_EXIT=0

$ python3 -B .remedy-wt/f024-r1-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f024-r1-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f024-r1-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=24 | guard exit=0 failed=0 passed=4
m1 (planning_started marks Build): vitest exit=1 failed=2 passed=22 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m2 (a round with no reviewer marks Review): vitest exit=1 failed=1 passed=23 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m3 (a skipped phase gets no start): vitest exit=1 failed=7 passed=17 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m4 (Finalized is sticky): vitest exit=1 failed=1 passed=23 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m5 (the seed keeps today's statuses): vitest exit=1 failed=2 passed=22 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m6 (Finalized ignores a later marker): vitest exit=1 failed=1 passed=23 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m7 (a pass heals another task's failure): vitest exit=1 failed=1 passed=23 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m8 (one failure heals twice): vitest exit=1 failed=1 passed=23 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m9 (a repeated seq keeps the last row): vitest exit=1 failed=2 passed=22 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m10 (a prototype-named kind resolves as a marker): vitest exit=1 failed=1 passed=23 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m11 (the hover shows the raw kind): vitest exit=1 failed=3 passed=21 | guard exit=0 failed=0 passed=4 | caught=True restored byte-identical=True
m12 (the table names a kind nothing writes): vitest exit=1 failed=1 passed=23 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
m13 (a kind marks Job): vitest exit=1 failed=1 passed=23 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
m14 (the mapping reaches for the wall clock): vitest exit=0 failed=0 passed=24 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
m15 (the bar's phase order drifts from the mapping): vitest exit=0 failed=0 passed=24 | guard exit=1 failed=1 passed=3 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=24 | guard exit=0 failed=0 passed=4
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every count matches the reviewer's stated sim-tree reading exactly (control first v24/g4 exit 0;
m1 v2g0 .. m15 v0g1 as tabulated in the block's G5 section; control last equal to control first;
every `restored byte-identical` True; final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`).

```
$ git worktree remove --force .remedy-wt/f024-r1-mut; echo $?
0
$ git worktree prune; echo $?
0
$ git worktree list
(primary + 15 f015-*-dry/sim r1-r6, 5 f015-*-sim r7-r9, 16 f020-*-dry/sim r1-r8,
 20 f023-*-dry/sim r1-r9, f023-r10-dry, f023-r10-sim, f024-r1-dry, f024-r1-sim,
 8 f284-*-dry/sim r1-r4, 4 job-* worktrees)
```
`f024-r1-mut` is gone; every worktree constraint 6 names remains.

## Evidence and package summary

Not applicable this round: T001 lands product code and its guard/goldens under an open feature;
no closure, no evidence job, no review package is produced at a T-slice round. This section is
carried forward as N/A per the block's own scope (claim + T001, not closure).

## Authored-text proofs

All 8 authored copies under `.agent/authored/f024-r1-*` (the block copy, plan.md, context.md,
claim.diff, mutations.py, phaseMapping.ts, phaseMapping.test.ts, test_phase_mapping.py) were built
by `shutil.copyfile` from source to destination — never retyped, never edited. Each was read back
with `git show <commit>:<path>` and compared byte for byte against its source: all 8
BYTE-IDENTICAL (G1 above). `claim.diff` was applied with `git apply` after `git apply --check`
passed (exit 0, both). `.agent/plan.md` and `.agent/context.md` were rewritten whole via
`shutil.copyfile` from the payload sources — never retyped — and confirmed MATCH against both the
PAYLOADS table and the G2 table. `phaseMapping.ts` was copied whole via `shutil.copyfile` into
`apps/ui/src/components/timeline/phaseMapping.ts` and confirmed MATCH against the G3 table.
`phaseMapping.test.ts` and `test_phase_mapping.py` were likewise copied whole via
`shutil.copyfile` into their destinations and confirmed MATCH against the G3 table.

## Deviations & assumptions

None. All nine commits landed in the block's stated order: C1a, C1b, C1c, C1d, C1e, C2, C3, C4,
C5, exactly as ordered. No payload was edited, retyped or repaired. G1 through G5 ran before this
handback was written, per the block's instruction ("G1 to G5 run before C5 is written"). The
`.remedy-wt/f024-r1-mut` worktree G5 required was added and removed within this round, as its last
action, and `git worktree prune` was run after. No other worktree was added or removed this round;
every worktree named in constraint 6 (`f015-r*`, `f020-r*`, `f023-r*`, `f284-r*`, `job-*`, and the
reviewer's own `f024-r1-sim`/`f024-r1-dry`) was left untouched. No `git stash` was used, nothing
was merged, no pull request was created, no force-push occurred.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 318 insertions, matches block's expectation exactly (245+73); well under the 500-insertion STOP threshold |
| C1b | done | 147 insertions, matches block's expected 147 exactly |
| C1c | done | 170 insertions, matches block's expected 170 exactly |
| C1d | done | 213 insertions, matches block's expected 213 exactly |
| C1e | done | 395 insertions (325+70), matches block's expected 395 exactly |
| C2 | done | claim.diff apply --check and apply both exit 0; 13/15, 59/0, 25/26, 23/15, 1/1 insertions/deletions match exactly |
| C3 | done | 213 insertions, matches block's expected 213 exactly |
| C4 | done | 325 and 70 insertions, matches block's expected 325 and 70 exactly |
| G1 | done | all 7 payload digests and 8 authored-copy comparisons matched |
| G2 | done | all 5 named file digests matched; structure checks (1x `## Findings`, 1x `## Steps`, last line, STATUS line, path set) all matched |
| G3 | done | all 3 product/test digests matched; both path-name-only diffs matched; ruff clean |
| G4 | done | 1546 passed, 5 skipped, exit 0; all four toolchain nodes ran and passed (none skipped); integrity check 6/6 pass |
| G5 | done | control first/last and all 15 mutations matched the reviewer's stated readings exactly; all restored byte-identical; final line True |
| C5 | done | this handback |
| PUSH | pending | `git push -u origin feature/f024-phase-timeline-scrubber` after this commit; reported in the final reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1. Then T002 — snapshot
memoization every 200 seq with its memory cap and lazy rebuild, and the property test that the
state at any fuzzed position equals a fresh reduction of that prefix. Open findings: 1. Operator
questions open: 3.
