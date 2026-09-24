# Handback — F020 Node lifecycle & glyph language · Round 4

## Session

SESSION 1 of feature F020 · round 4 · rounds so far 4

This round booked round 3's PASS into the live review record, recorded DECISION F020 D4, and
landed T003's first half: `renderers/stateMotion.ts` (a 300 ms crossfade scheduled for every
state change and a completion ripple into `pass`, and the frame rule deciding whether the canvas
needs frames at all — never on a hidden page); the pulse multiplier `pulseScaleAt` moved into
`renderers/nodeStates.ts`; the motion-aware painter `paintBrainNodeInMotion` in
`renderers/paintNode.ts`; `usePageVisible.ts`; and `ForceBrainGraph.tsx` wired to all of them,
its edge particles stopping with the page. All nine commits landed in the block's ordered
sequence; all five gates passed with exact matches to the reviewer's stated readings, with one
arithmetic reconciliation on G4's skip count (explained below, not a deviation). I had ample
context remaining throughout this round; no session-limit pressure at any point.

## Range

Review of 6f43c63a..HEAD

## Commits

### 151bc29ca F020 R4 C1a: copy round 4 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r4-block.md | +258/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r4-plan.md | +30/-0 | copy of the plan.md payload |

288 insertions by `git show --numstat` (block's 258 lines + 30); matches the block's expectation
exactly; under the 500-insertion cap.

### c8dd2bb0e F020 R4 C1b: copy round 4 diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r4-book.diff | +64/-0 | copy of the book.diff payload |
| .agent/authored/f020-r4-product.diff | +233/-0 | copy of the product.diff payload |
| .agent/authored/f020-r4-tests.diff | +113/-0 | copy of the tests.diff payload |

410 insertions by `git show --numstat`; matches the block's expectation of 410 exactly.

### 5b7a13389 F020 R4 C1c: copy round 4 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r4-mutations.py | +187/-0 | copy of the mutations.py payload (G5 tool) |

187 insertions by `git show --numstat`; matches the block's expectation of 187 exactly.

### b330d3826 F020 R4 C1d: copy round 4 product files into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r4-stateMotion.ts | +101/-0 | copy of the stateMotion.ts payload |
| .agent/authored/f020-r4-usePageVisible.ts | +15/-0 | copy of the usePageVisible.ts payload |

116 insertions by `git show --numstat`; matches the block's expectation of 116 exactly.

### a3c53a8d1 F020 R4 C1e: copy round 4 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r4-stateMotion.test.ts | +151/-0 | copy of the stateMotion.test.ts payload |
| .agent/authored/f020-r4-test_brain_motion_wiring.py | +57/-0 | copy of the test_brain_motion_wiring.py payload |

208 insertions by `git show --numstat`; matches the block's expectation of 208 exactly.

### 08b93a19a F020 R4 C2: book round 3's PASS, record D4, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +46/-0 | DECISION F020 D4 appended (book.diff) |
| .agent/live_review.md | +2/-0 | F020 R3 Gate entry appended (book.diff) |
| .agent/plan.md | +6/-7 | rewritten to the plan.md payload |

`git apply --check` on book.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 46 decisions.md, 2 live_review.md, 6 plan.md — matches the block's expectation
exactly; aggregate 54 insertions(+)/7 deletions(-), all deletions attributable to plan.md's
rewrite diff.

### 3a182fb66 F020 R4 C3: crossfade state changes, ripple completions, pulse, and draw frames only on a visible page
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/ForceBrainGraph.tsx | +56/-9 | wires `usePageVisible`, the frame rule and the motion-aware painter; gates edge particles on visibility (product.diff) |
| apps/ui/src/components/graph/renderers/nodeStates.ts | +12/-7 | `pulseScaleAt` gains the reduced-motion guard (product.diff) |
| apps/ui/src/components/graph/renderers/paintNode.ts | +46/-0 | new export `paintBrainNodeInMotion` (product.diff) |
| apps/ui/src/components/graph/renderers/stateMotion.ts | +101/-0 | new file: crossfade scheduling, completion ripple, frame rule |
| apps/ui/src/components/graph/usePageVisible.ts | +15/-0 | new file: `visibilitychange`-driven visibility hook |

`git apply --check` on product.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 56 ForceBrainGraph.tsx, 12 nodeStates.ts, 46 paintNode.ts, 101 stateMotion.ts, 15
usePageVisible.ts — matches the block's expectation exactly.

### fcb71150a F020 R4 C4: pin the motion, the frame rule, the replayed recording and the canvas wiring
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/renderers/nodeStates.test.ts | +21/-1 | vitest additions for the reduced-motion pulse guard (tests.diff) |
| apps/ui/src/components/graph/renderers/paintNode.test.ts | +47/-1 | vitest additions for `paintBrainNodeInMotion` (tests.diff) |
| apps/ui/src/components/graph/renderers/stateMotion.test.ts | +151/-0 | new file: vitest goldens for stateMotion.ts |
| tests/ui_contracts/test_brain_motion_wiring.py | +57/-0 | new file: contract replaying F019's demo recording through the motion module |
| tests/ui_contracts/test_node_glyph_tokens.py | +1/-1 | token-guard adjustment for the motion tokens (tests.diff) |

`git apply --check` on tests.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 21 nodeStates.test.ts, 47 paintNode.test.ts, 151 stateMotion.test.ts, 57
test_brain_motion_wiring.py, 1 test_node_glyph_tokens.py — matches the block's expectation
exactly.

### (this commit) F020 R4 C5: rewrite handoff for round 4
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f020-r4-mut fcb71150a` — outcome: success, detached HEAD
  at `fcb71150a`.
- `git worktree remove --force .remedy-wt/f020-r4-mut` — outcome: success.
- `git worktree prune` — outcome: success, no output.
- `git push origin feature/f020-node-lifecycle-glyph-language` — runs AFTER this commit lands;
  its real outcome is reported in the reply, since this handback cannot contain an outcome that
  happens after it. No `gh pr create` this round: the block forbids it (constraint 5).

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory (absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
feature/f020-node-lifecycle-glyph-language
$ git log --oneline -1
6f43c63a4 F020 R3 C5: rewrite handoff for round 3
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r4/block.md
258 lines, sha256=e2db2736ab3d27d78544a4124368d990305cf2e453c3313a247c73b98601edd1
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ wc -lc / sha256sum over .remedy-wt/f020-r4-payloads/*
book.diff                     lines=64  bytes=11647 sha256=c0f4f0750ccda20105cd82615e49063f4f6c729705bd83081e14ce9d2d10fd5b
mutations.py                  lines=187 bytes=10093 sha256=7533d95038ea65645b979ff4482a37520574482f99c8582577920d0771020b81
plan.md                       lines=30  bytes=1116  sha256=7c10e770db7b24c290866d2c3c3280feeb20a14aba54803ed8530c332cb0d72d
product.diff                  lines=233 bytes=12343 sha256=86945bd38e5d7e39388c4e17ec2a1e1e5d7c224fafcf7201b2a08412019c11d1
stateMotion.test.ts           lines=151 bytes=7514  sha256=f33a61a8ae450d327ed7f2a59b5ae35824157eb01080a06bfc1dd2fc50748d01
stateMotion.ts                lines=101 bytes=4173  sha256=3228d4d97bb77aaba636e783626d5745ae339c70c6b546d99cde3d89821c685a
test_brain_motion_wiring.py   lines=57  bytes=3085  sha256=5c85828096ceeceeed2dff223a42b19bf692957ea617a7429c1afc52cf22e2d5
tests.diff                    lines=113 bytes=5759  sha256=d4970a9e7c61ce6e5c3838779d76328205a02edaa5227d9cb805f3c4a1dfc8ea
usePageVisible.ts             lines=15  bytes=768   sha256=4e034c48d00949c5171e50eda04efb4748c477e52785df2cc37339b873312ff4
```
All 9 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r4-* blob, read with `git show <commit>:<path>`,
   against its source)
f020-r4-block.md                    @ 151bc29ca: match=True
f020-r4-plan.md                     @ 151bc29ca: match=True
f020-r4-book.diff                   @ c8dd2bb0e: match=True
f020-r4-product.diff                @ c8dd2bb0e: match=True
f020-r4-tests.diff                  @ c8dd2bb0e: match=True
f020-r4-mutations.py                @ 5b7a13389: match=True
f020-r4-stateMotion.ts              @ b330d3826: match=True
f020-r4-usePageVisible.ts           @ b330d3826: match=True
f020-r4-stateMotion.test.ts         @ a3c53a8d1: match=True
f020-r4-test_brain_motion_wiring.py @ a3c53a8d1: match=True
```
All 10 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's three files, read with `git show 08b93a19a:<path>`, against the block's G2 table)
.agent/live_review.md: bytes=295964  sha256=a5f11b1f31bf69f8979c82d3488bd927d87ce9b563f0d999c5376647a87f0c44 match=True
.agent/decisions.md:   bytes=2040394 sha256=b8589c84a33ecd767c9323bcfb9955c37efaa36bc550c4da2501a1b815536e81 match=True
.agent/plan.md:        bytes=1116    sha256=7c10e770db7b24c290866d2c3c3280feeb20a14aba54803ed8530c332cb0d72d match=True
```
All 3 match the block's G2 table exactly.

```
$ git diff <C1e> 08b93a19a -- .agent/live_review.md, counting added lines starting
  "Gate: F020 R3 — "
count = 1
```
Matches the reviewer's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT at C2
08b93a19a (C2) open ids: ['R-1008']
```
Reads R-1008 alone, matching the reviewer's stated reading exactly (G2).

```
$ git diff --name-only a3c53a8d1 08b93a19a
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Exactly the three paths the block's G2 table names (G2).

```
$ (sha256/bytes of C3/C4 files, read with `git show <commit>:<path>`, against the block's G3 table)
C3 apps/ui/src/components/graph/ForceBrainGraph.tsx:                       bytes=16279 sha256=1b426ee1e69ddd674016fa97ece8a4e6a41282334204f6c5b6e09be1fc8c3e9c match=True
C3 apps/ui/src/components/graph/renderers/nodeStates.ts:                  bytes=7016  sha256=6bb616d191f910664f484de5761a55268e724cd576024c293cd3b33899bea4be match=True
C3 apps/ui/src/components/graph/renderers/paintNode.ts:                   bytes=8098  sha256=df2cf6105056588dc1ae5e73bc07fc4e6923eca7594547f989d9091be62d238a match=True
C3 apps/ui/src/components/graph/renderers/stateMotion.ts:                 bytes=4173  sha256=3228d4d97bb77aaba636e783626d5745ae339c70c6b546d99cde3d89821c685a match=True
C3 apps/ui/src/components/graph/usePageVisible.ts:                        bytes=768   sha256=4e034c48d00949c5171e50eda04efb4748c477e52785df2cc37339b873312ff4 match=True
C4 apps/ui/src/components/graph/renderers/nodeStates.test.ts:             bytes=6774  sha256=0e6ad9051ddec719a9fe4c82965756fb18f7cdb1ce5b04f746a62b8e036bb34a match=True
C4 apps/ui/src/components/graph/renderers/paintNode.test.ts:              bytes=12429 sha256=7375c307d99ec579ebc32a62a510124ced596d6458d521cd0edb3c9b9b963763 match=True
C4 tests/ui_contracts/test_node_glyph_tokens.py:                          bytes=6142  sha256=c3f1710c162944e773945ec18b097bbbb2d7fc0b1076249908f69c717528a584 match=True
C4 apps/ui/src/components/graph/renderers/stateMotion.test.ts:            bytes=7514  sha256=f33a61a8ae450d327ed7f2a59b5ae35824157eb01080a06bfc1dd2fc50748d01 match=True
C4 tests/ui_contracts/test_brain_motion_wiring.py:                        bytes=3085  sha256=5c85828096ceeceeed2dff223a42b19bf692957ea617a7429c1afc52cf22e2d5 match=True
```
All 10 match the block's G3 table exactly.

```
$ git diff --name-only 08b93a19a 3a182fb66
apps/ui/src/components/graph/ForceBrainGraph.tsx
apps/ui/src/components/graph/renderers/nodeStates.ts
apps/ui/src/components/graph/renderers/paintNode.ts
apps/ui/src/components/graph/renderers/stateMotion.ts
apps/ui/src/components/graph/usePageVisible.ts
$ git diff --name-only 3a182fb66 fcb71150a
apps/ui/src/components/graph/renderers/nodeStates.test.ts
apps/ui/src/components/graph/renderers/paintNode.test.ts
apps/ui/src/components/graph/renderers/stateMotion.test.ts
tests/ui_contracts/test_brain_motion_wiring.py
tests/ui_contracts/test_node_glyph_tokens.py
```
Both name exactly the paths C3 and C4 list (G3).

```
$ python3 -m ruff check tests/ui_contracts/test_brain_motion_wiring.py tests/ui_contracts/test_node_glyph_tokens.py
All checks passed!
REAL_EXIT=0
```

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts
  tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
  tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py
  tests/orchestration/test_block_lint.py tests/regression/test_named_bugs.py
  tests/test_agent_tooling.py tests/cli/test_golden_path.py 2>&1 | tail -20; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:295: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:312: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:321: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:383: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:392: D3 quarantine (F252) ...
SKIPPED [1] tests/regression/test_named_bugs.py:399: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1174 passed, 11 skipped in 76.47s (0:01:16)
REAL_EXIT=0
```
None of the 11 SKIPPED lines are the four toolchain nodes the block names (the two
`tests/ui_contracts/test_ui_lint.py` eslint checks, the tsc node in
`tests/ui_server/test_dashboard_contract.py`, the vitest node in
`tests/orchestration/test_test_runner.py`) — all four ran and PASSED in the primary checkout, not
skipped, as required. The 11 remaining skips are pre-existing D3/D12 quarantines unrelated to this
round's paths. The reviewer's sim-tree run (without golden path) read `1127 passed, 16 skipped`;
reconciled: `tests/ui_contracts/test_responsive.py` — collected as part of the bare
`tests/ui_contracts` directory argument, not named individually in the block — carries one more
conditional skip ("dist/assets/ not built") that fires in a fresh sim tree but not in the primary
checkout, where `apps/ui/dist` is already built from earlier rounds; together with the four named
toolchain nodes that is 5 skip-to-pass conversions (16 − 5 = 11 skipped here), and this run
additionally includes `tests/cli/test_golden_path.py` (42 collected tests, confirmed by
`--collect-only`), giving 1127 + 5 + 42 = 1174 passed exactly. Not a deviation: every reading the
block gates on (the four named nodes passing, not skipping) is met; this is the arithmetic that
explains the remainder.

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
$ git worktree add --detach .remedy-wt/f020-r4-mut fcb71150a
Preparing worktree (detached HEAD fcb71150a)
REAL_EXIT=0

$ python3 -B .remedy-wt/f020-r4-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f020-r4-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f020-r4-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=56 | guard exit=0 failed=0 passed=12
m1 (reduced motion still schedules state changes): vitest exit=1 failed=2 passed=54 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m2 (the job core's state change is scheduled): vitest exit=1 failed=2 passed=54 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m3 (every state change ripples): vitest exit=1 failed=3 passed=53 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m4 (a node just born is scheduled as a change): vitest exit=1 failed=2 passed=54 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m5 (the crossfade runs backwards): vitest exit=1 failed=2 passed=54 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m6 (the ripple travels linearly): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m7 (a hidden page still asks for frames): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m8 (the pulse draws frames under reduced motion): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m9 (the core counts as a pulsing node): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m10 (the pulse multiplier ignores reduced motion): vitest exit=1 failed=2 passed=54 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m11 (the old state is painted at full alpha during a change): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m12 (the ripple is never painted): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m13 (the painter ignores the pulse multiplier): vitest exit=1 failed=1 passed=55 | guard exit=0 failed=0 passed=12 | caught=True restored byte-identical=True
m14 (the canvas redraws only for births again): vitest exit=0 failed=0 passed=56 | guard exit=1 failed=1 passed=11 | caught=True restored byte-identical=True
m15 (particles flow on a hidden page): vitest exit=0 failed=0 passed=56 | guard exit=1 failed=1 passed=11 | caught=True restored byte-identical=True
m16 (the frame rule is told the page is always visible): vitest exit=0 failed=0 passed=56 | guard exit=1 failed=1 passed=11 | caught=True restored byte-identical=True
m17 (the canvas paints every node without its motion): vitest exit=0 failed=0 passed=56 | guard exit=1 failed=1 passed=11 | caught=True restored byte-identical=True
m18 (the visibility hook never listens): vitest exit=0 failed=0 passed=56 | guard exit=1 failed=1 passed=11 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=56 | guard exit=0 failed=0 passed=12
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every (v, g) pair matches the block's stated reading exactly: control 56v/12g both exit 0;
m1-m2 v2g0; m3 v3g0; m4-m5 v2g0; m6-m9 v1g0; m10 v2g0; m11-m13 v1g0; m14-m18 v0g1; control last
equals control first; every `restored byte-identical` True; final line
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` (G5).

```
$ git worktree remove --force .remedy-wt/f020-r4-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```

## Authored-text proofs

All 10 authored copies under `.agent/authored/f020-r4-*` (the block copy plus the nine payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 10 BYTE-IDENTICAL (G1 above). `book.diff`, `product.diff` and `tests.diff` were each applied
with `git apply` after `git apply --check` passed (exit 0 both, every time), never retyped or
edited; the resulting files were verified by byte count and sha256 against the block's G2/G3
tables — all MATCH. `.agent/plan.md` was rewritten whole via `shutil.copyfile` from the payload
source — never retyped — and confirmed MATCH against the PAYLOADS table and the G2 table.
`stateMotion.ts`, `usePageVisible.ts`, `stateMotion.test.ts` and `test_brain_motion_wiring.py`
were each copied whole via `shutil.copyfile` into their product/test locations and confirmed
MATCH against the block's G3 table. `mutations.py` was run unmodified from its payload path
against the fresh `.remedy-wt/f020-r4-mut` worktree; its printed output was reported verbatim and
matches the block's stated G5 reading exactly.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1a, C1b, C1c, C1d, C1e, C2, C3, C4, C5,
exactly as ordered. G1 through G5 ran before this handback was written, as the block orders. No
payload was edited, retyped or repaired. The round's tracked path set matches constraint 3 (full
list reported in the reply via `git diff --name-only 6f43c63a HEAD` after this commit, since that
reading is taken after C5 lands). Nothing was merged this round: no `gh pr merge`, no `gh pr
create`, no checkout of `main` after the branch was cut, no branch deletion, no force-push, no
`git stash` — per constraint 5. The reviewer's worktrees, the `f015-r*`/`f284-r*` worktrees and the
`job-*` worktrees/branches were left untouched — per constraint 6. G4's skip-count arithmetic
(1127→1174 passed, 16→11 skipped) is explained in the Verification section above; it is a
reconciliation of an environment difference (dist already built, node_modules present, golden
path included), not a departure from the block, and every explicitly gated reading (the four
named toolchain nodes passing, not skipping) was met exactly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 288 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C1b | done | 410 insertions, matches block's expectation exactly |
| C1c | done | 187 insertions, matches block's expectation exactly |
| C1d | done | 116 insertions, matches block's expectation exactly |
| C1e | done | 208 insertions, matches block's expectation exactly |
| C2 | done | book.diff apply --check and apply both exit 0; 46/2/6 insertions, matches; D4 recorded |
| C3 | done | product.diff apply --check and apply both exit 0; 56/12/46/101/15 insertions, matches |
| C4 | done | tests.diff apply --check and apply both exit 0; 21/47/151/57/1 insertions, matches |
| C5 | done | committing now with this handback |
| G1 | done | all 9 payload digests and 10 authored-copy comparisons matched |
| G2 | done | all 3 named file digests matched; gate-line count 1; open set R-1008 alone; C1e..C2 path set exact |
| G3 | done | all 10 named file digests matched; C2..C3 and C3..C4 path sets exact; ruff clean |
| G4 | done | 1174 passed, 11 skipped at exit 0; all 4 named toolchain nodes ran and passed (not skipped); integrity check 6/6 pass |
| G5 | done | 18 mutations + 2 controls all matched the block's stated (v,g) readings exactly; ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True |
| G6 | pending | runs after this commit (tree/log check, worktree list, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 4. Then T003's second
half — the conformance assertions over the matrix fixture's pixels, with the headless harness
that reads them. Open findings: 1. Operator questions open: 3.
