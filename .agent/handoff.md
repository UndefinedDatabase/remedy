# Handback — F020 Node lifecycle & glyph language · Round 3

## Session

SESSION 1 of feature F020 · round 3 · rounds so far 3

This round booked round 2's PASS into the live review record, recorded DECISION F020 D3, and
landed T002's second half: `renderers/legendModel.ts` (the legend's rows enumerated from the
glyph and state modules), `GraphLegend.tsx` and its stylesheet (a "Legend" dialog opened from the
graph's chrome, rendering only those rows, writing no name/path/colour of its own), mounted by
`BrainGraphStage.tsx`; a cluster's `+n` count from the layout's label, written by the painter in a
font the palette bridge resolves; and `renderers/glyphMatrix.ts` (every non-core kind in every
state painted by the live painter). All nine commits landed in the block's ordered sequence; all
five gates passed with exact matches to the reviewer's stated readings. I had ample context
remaining throughout this round; no session-limit pressure at any point.

## Range

Review of 1d954ef5e..HEAD

## Commits

### 8776503fe F020 R3 C1a: copy round 3 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r3-block.md | +269/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r3-plan.md | +31/-0 | copy of the plan.md payload |

300 insertions by `git show --numstat` (block's 269 lines + 31); matches the block's expectation
exactly; under the 500-insertion cap.

### 3ead9e61a F020 R3 C1b: copy round 3 diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r3-book.diff | +58/-0 | copy of the book.diff payload |
| .agent/authored/f020-r3-product.diff | +187/-0 | copy of the product.diff payload |
| .agent/authored/f020-r3-tests.diff | +126/-0 | copy of the tests.diff payload |

371 insertions by `git show --numstat`; matches the block's expectation of 371 exactly.

### 57cba67b9 F020 R3 C1c: copy round 3 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r3-mutations.py | +195/-0 | copy of the mutations.py payload (G5 tool) |

195 insertions by `git show --numstat`; matches the block's expectation of 195 exactly.

### d3062ef96 F020 R3 C1d: copy round 3 product files into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r3-GraphLegend.module.css | +60/-0 | copy of the GraphLegend.module.css payload |
| .agent/authored/f020-r3-GraphLegend.tsx | +83/-0 | copy of the GraphLegend.tsx payload |
| .agent/authored/f020-r3-glyphMatrix.ts | +76/-0 | copy of the glyphMatrix.ts payload |
| .agent/authored/f020-r3-legendModel.ts | +72/-0 | copy of the legendModel.ts payload |

291 insertions by `git show --numstat`; matches the block's expectation of 291 exactly.

### 3fd4ed871 F020 R3 C1e: copy round 3 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r3-glyphMatrix.test.ts | +69/-0 | copy of the glyphMatrix.test.ts payload |
| .agent/authored/f020-r3-legendModel.test.ts | +63/-0 | copy of the legendModel.test.ts payload |
| .agent/authored/f020-r3-test_graph_legend_contract.py | +68/-0 | copy of the test_graph_legend_contract.py payload |

200 insertions by `git show --numstat`; matches the block's expectation of 200 exactly.

### 6d42d954d F020 R3 C2: book round 2's PASS, record D3, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +40/-0 | DECISION F020 D3 appended (book.diff) |
| .agent/live_review.md | +2/-0 | F020 R2 Gate entry appended (book.diff) |
| .agent/plan.md | +8/-11 | rewritten to the plan.md payload |

`git apply --check` on book.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 40 decisions.md, 2 live_review.md, 8 plan.md — matches the block's expectation
exactly; aggregate 50 insertions(+)/11 deletions(-), all deletions attributable to plan.md's
rewrite diff.

### 062abc7da F020 R3 C3: generate the graph legend from the glyph and state modules, count clusters, paint the matrix
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/BrainGraphStage.module.css | +1/-1 | legend-dialog styling hook (product.diff) |
| apps/ui/src/components/graph/BrainGraphStage.tsx | +2/-0 | mounts the "Legend" dialog from the graph's chrome (product.diff) |
| apps/ui/src/components/graph/GraphLegend.module.css | +60/-0 | new file: legend dialog stylesheet |
| apps/ui/src/components/graph/GraphLegend.tsx | +83/-0 | new file: legend dialog rendering rows from legendModel.ts only |
| apps/ui/src/components/graph/buildForceBrainModel.ts | +10/-3 | writes each cluster's `+n` label (product.diff) |
| apps/ui/src/components/graph/renderers/glyphMatrix.ts | +76/-0 | new file: every non-core kind in every state painted by the live painter |
| apps/ui/src/components/graph/renderers/legendModel.ts | +72/-0 | new file: legend rows enumerated from the glyph and state modules |
| apps/ui/src/components/graph/renderers/paintNode.ts | +23/-10 | paints the cluster count in a palette-resolved font (product.diff) |
| apps/ui/src/components/graph/renderers/palette.ts | +6/-1 | resolves the count font token (product.diff) |

`git apply --check` on product.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 1 BrainGraphStage.module.css, 2 BrainGraphStage.tsx, 60 GraphLegend.module.css, 83
GraphLegend.tsx, 10 buildForceBrainModel.ts, 76 glyphMatrix.ts, 72 legendModel.ts, 23
paintNode.ts, 6 palette.ts — matches the block's expectation exactly.

### 358f30bdd F020 R3 C4: pin the legend's rows, its wiring, the cluster count and the matrix
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | +8/-0 | vitest additions for the cluster `+n` label (tests.diff) |
| apps/ui/src/components/graph/renderers/glyphMatrix.test.ts | +69/-0 | new file: vitest goldens for glyphMatrix.ts |
| apps/ui/src/components/graph/renderers/legendModel.test.ts | +63/-0 | new file: vitest goldens for legendModel.ts |
| apps/ui/src/components/graph/renderers/paintNode.test.ts | +30/-4 | vitest additions for the count's font/palette wiring (tests.diff) |
| apps/ui/src/components/graph/renderers/palette.test.ts | +4/-2 | vitest additions for the count font token (tests.diff) |
| tests/ui_contracts/test_graph_legend_contract.py | +68/-0 | new file: contract pinning the legend's rows, wiring, cluster count and matrix |

`git apply --check` on tests.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 8 buildForceBrainModel.test.ts, 69 glyphMatrix.test.ts, 63 legendModel.test.ts, 30
paintNode.test.ts, 4 palette.test.ts, 68 test_graph_legend_contract.py — matches the block's
expectation exactly.

### (this commit) F020 R3 C5: rewrite handoff for round 3
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f020-r3-mut 358f30bdd` — outcome: success, detached HEAD
  at `358f30bdd`.
- `git worktree remove --force .remedy-wt/f020-r3-mut` — outcome: success.
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
1d954ef5e F020 R2 C5: rewrite handoff for round 2
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r3/block.md
269 lines, sha256=7c2bf6b9d365120286c3947c1f9bf7754fa49ed71dff6a72aa5f24da474b988b
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ wc -lc / sha256sum over .remedy-wt/f020-r3-payloads/*
GraphLegend.module.css        lines=60  bytes=1508  sha256=0f14ff256eba21b459a7dd35c0e30e951b24871db87ea5f1900e2435830bdbee
GraphLegend.tsx                lines=83  bytes=3143  sha256=ad0c565b5e3f973aa3128fa76a1b2951edeb6a268638a2cf1986fe0fbca739de
book.diff                      lines=58  bytes=10093 sha256=4b4a1f748c5a109eb763e757fd8f842e62f441c9f255bdae0469e319ab4ef147
glyphMatrix.test.ts            lines=69  bytes=3253  sha256=69726b35ede404be10bbc327143591c9ceb63e10a3ddd3b71d299eb45a399d33
glyphMatrix.ts                 lines=76  bytes=3139  sha256=a386296e9408fac82eff5fa5e1b0aca3b7471b95eaf65987217089ed31a78e84
legendModel.test.ts            lines=63  bytes=2649  sha256=8649a311c069b5adb1a6dfa3785409d2361f52b8900c5a6439f79143ef738d38
legendModel.ts                 lines=72  bytes=2609  sha256=133d45264c4858edd3432ac65af4d6590bf7c6bdbe7a945ff7147e1df7b74e16
mutations.py                   lines=195 bytes=10532 sha256=b17af969d6349d43152df6b7c2591bba585268ac4a25ce61ccc48f89e7649623
plan.md                        lines=31  bytes=1155  sha256=c79de02923262d0d6dd2329e284175816375650aad7edb80abdc46103bc4bc4f
product.diff                   lines=187 bytes=9353  sha256=58175cd16fd3e55bd83037bab733bc2ada099677e00950e6904975aec367a909
test_graph_legend_contract.py  lines=68  bytes=3056  sha256=1ad5d9063894f72aa59bae789077d96f72ac068a9c21c57e0c1174b0643b4e03
tests.diff                     lines=126 bytes=6631  sha256=03c25f5d259c95a837b844ca12b3221a9b89fb5630b320d24e052cb306701dc8
```
All 12 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r3-* blob, read with `git show <commit>:<path>`,
   against its source)
f020-r3-block.md                      @ 8776503fe: match=True
f020-r3-plan.md                       @ 8776503fe: match=True
f020-r3-book.diff                     @ 3ead9e61a: match=True
f020-r3-product.diff                  @ 3ead9e61a: match=True
f020-r3-tests.diff                    @ 3ead9e61a: match=True
f020-r3-mutations.py                  @ 57cba67b9: match=True
f020-r3-legendModel.ts                @ d3062ef96: match=True
f020-r3-glyphMatrix.ts                @ d3062ef96: match=True
f020-r3-GraphLegend.tsx               @ d3062ef96: match=True
f020-r3-GraphLegend.module.css        @ d3062ef96: match=True
f020-r3-legendModel.test.ts           @ 3fd4ed871: match=True
f020-r3-glyphMatrix.test.ts           @ 3fd4ed871: match=True
f020-r3-test_graph_legend_contract.py @ 3fd4ed871: match=True
```
All 13 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's three files, read with `git show 6d42d954d:<path>`, against the block's G2 table)
.agent/live_review.md: bytes=293386  sha256=8565fe941e7222e08f633ffdcf0e3a6c08b386f2e73c7c060c938134dedeef94 match=True
.agent/decisions.md:   bytes=2036559 sha256=b30351b7139ca97ee81b05e19a158bc2b2192c96208c590fe2ec0fa143834b4f match=True
.agent/plan.md:        bytes=1155    sha256=c79de02923262d0d6dd2329e284175816375650aad7edb80abdc46103bc4bc4f match=True
```
All 3 match the block's G2 table exactly.

```
$ git diff <parent> 6d42d954d -- .agent/live_review.md, counting added lines starting
  "Gate: F020 R2 — "
count = 1
```
Matches the reviewer's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT at C2
6d42d954d (C2) open ids: ['R-1008']
```
Reads R-1008 alone, matching the reviewer's stated reading exactly (G2).

```
$ git diff --name-only 3fd4ed871 6d42d954d
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Exactly the three paths the block's G2 table names (G2).

```
$ (sha256/bytes of C3/C4 files, read with `git show <commit>:<path>`, against the block's G3 table)
C3 apps/ui/src/components/graph/BrainGraphStage.tsx:                       bytes=3438  sha256=996eb59cfdd062dbdacfa004c006a22149789040d70f7974ea34f67ff30b76ee match=True
C3 apps/ui/src/components/graph/BrainGraphStage.module.css:                bytes=1112  sha256=8d15d5450a2811b5cef68a6934d18064397d26709f6d5755578d9e9b65ba6944 match=True
C3 apps/ui/src/components/graph/buildForceBrainModel.ts:                   bytes=8422  sha256=4c93b0dc7287a91ebc6a5fe52efe3183a482858a5a62bc392c2d742a39b8a274 match=True
C3 apps/ui/src/components/graph/renderers/paintNode.ts:                    bytes=6057  sha256=6828b4a51eff6f2d19e5b7e3c5dd058e4340a70b82bde482c9c610c2e8beb47f match=True
C3 apps/ui/src/components/graph/renderers/palette.ts:                      bytes=2348  sha256=4926d3d0b2dcd90803dba48a6d2b743e2f896adf7d5f5ac2654fee2bdb1d8b31 match=True
C3 apps/ui/src/components/graph/renderers/legendModel.ts:                  bytes=2609  sha256=133d45264c4858edd3432ac65af4d6590bf7c6bdbe7a945ff7147e1df7b74e16 match=True
C3 apps/ui/src/components/graph/renderers/glyphMatrix.ts:                  bytes=3139  sha256=a386296e9408fac82eff5fa5e1b0aca3b7471b95eaf65987217089ed31a78e84 match=True
C3 apps/ui/src/components/graph/GraphLegend.tsx:                           bytes=3143  sha256=ad0c565b5e3f973aa3128fa76a1b2951edeb6a268638a2cf1986fe0fbca739de match=True
C3 apps/ui/src/components/graph/GraphLegend.module.css:                   bytes=1508  sha256=0f14ff256eba21b459a7dd35c0e30e951b24871db87ea5f1900e2435830bdbee match=True
C4 apps/ui/src/components/graph/buildForceBrainModel.test.ts:             bytes=10378 sha256=ad72e789e7c6e8d84bac13cde2645412b73730154c3e1cdf431b14d863dfc294 match=True
C4 apps/ui/src/components/graph/renderers/paintNode.test.ts:               bytes=10285 sha256=dd49b85750b5c2b417c11cb78ef7e8f30d99d9114695078da7132490793b526c match=True
C4 apps/ui/src/components/graph/renderers/palette.test.ts:                 bytes=1367  sha256=b5d43d7e1695c4d73b5b5b94de8526049ca36f72b7cda9805d550ae2815c66bb match=True
C4 apps/ui/src/components/graph/renderers/legendModel.test.ts:             bytes=2649  sha256=8649a311c069b5adb1a6dfa3785409d2361f52b8900c5a6439f79143ef738d38 match=True
C4 apps/ui/src/components/graph/renderers/glyphMatrix.test.ts:             bytes=3253  sha256=69726b35ede404be10bbc327143591c9ceb63e10a3ddd3b71d299eb45a399d33 match=True
C4 tests/ui_contracts/test_graph_legend_contract.py:                       bytes=3056  sha256=1ad5d9063894f72aa59bae789077d96f72ac068a9c21c57e0c1174b0643b4e03 match=True
```
All 15 match the block's G3 table exactly.

```
$ git diff --name-only 6d42d954d 062abc7da
apps/ui/src/components/graph/BrainGraphStage.module.css
apps/ui/src/components/graph/BrainGraphStage.tsx
apps/ui/src/components/graph/GraphLegend.module.css
apps/ui/src/components/graph/GraphLegend.tsx
apps/ui/src/components/graph/buildForceBrainModel.ts
apps/ui/src/components/graph/renderers/glyphMatrix.ts
apps/ui/src/components/graph/renderers/legendModel.ts
apps/ui/src/components/graph/renderers/paintNode.ts
apps/ui/src/components/graph/renderers/palette.ts
$ git diff --name-only 062abc7da 358f30bdd
apps/ui/src/components/graph/buildForceBrainModel.test.ts
apps/ui/src/components/graph/renderers/glyphMatrix.test.ts
apps/ui/src/components/graph/renderers/legendModel.test.ts
apps/ui/src/components/graph/renderers/paintNode.test.ts
apps/ui/src/components/graph/renderers/palette.test.ts
tests/ui_contracts/test_graph_legend_contract.py
```
Both name exactly the paths C3 and C4 list (G3).

```
$ python3 -m ruff check tests/ui_contracts/test_graph_legend_contract.py
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
1170 passed, 11 skipped in 71.79s (0:01:11)
REAL_EXIT=0
```
None of the 11 SKIPPED lines are the four toolchain nodes the block names (the two
`tests/ui_contracts/test_ui_lint.py` eslint checks, the tsc node in
`tests/ui_server/test_dashboard_contract.py`, the vitest node in
`tests/orchestration/test_test_runner.py`) — all four ran and PASSED in the primary checkout, not
skipped, as required. The 11 remaining skips are pre-existing D3/D12 quarantines unrelated to this
round's paths. The reviewer's sim-tree run (without golden path) read `1123 passed, 16 skipped`;
this run additionally includes `tests/cli/test_golden_path.py` and the four toolchain nodes the
primary checkout can run that the worktree cannot, accounting for the difference (G4).

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
$ git worktree add --detach .remedy-wt/f020-r3-mut 358f30bdd
Preparing worktree (detached HEAD 358f30bdd)
REAL_EXIT=0

$ python3 -B .remedy-wt/f020-r3-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f020-r3-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f020-r3-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=51 | guard exit=0 failed=0 passed=13
m1 (the kind rows ignore the module they are given): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m2 (a kind row carries its fill path as its stroke): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m3 (a state row's mark takes another mark's path): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m4 (tokenVar writes the bare token): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m5 (the matrix columns run in reverse state order): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m6 (the matrix grows a core row): vitest exit=1 failed=3 passed=48 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m7 (the matrix paints at a zoom that hides run glyphs): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m8 (a cluster cell carries no count): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m9 (the painter writes any kind's label): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m10 (the count is written in the fill colour): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m11 (the count's font names no resolved family): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m12 (the count's font leaves the palette): vitest exit=1 failed=2 passed=49 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m13 (the layout gives a cluster no label): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m14 (the cluster label drops its plus sign): vitest exit=1 failed=1 passed=50 | guard exit=0 failed=0 passed=13 | caught=True restored byte-identical=True
m15 (the legend draws a path literal of its own): vitest exit=0 failed=0 passed=51 | guard exit=1 failed=1 passed=12 | caught=True restored byte-identical=True
m16 (the legend paints a colour that is not a token): vitest exit=0 failed=0 passed=51 | guard exit=1 failed=1 passed=12 | caught=True restored byte-identical=True
m17 (the legend writes a kind's name by hand): vitest exit=0 failed=0 passed=51 | guard exit=1 failed=1 passed=12 | caught=True restored byte-identical=True
m18 (the legend no longer closes on Escape): vitest exit=0 failed=0 passed=51 | guard exit=1 failed=1 passed=12 | caught=True restored byte-identical=True
m19 (the stage no longer mounts the legend): vitest exit=0 failed=0 passed=51 | guard exit=1 failed=1 passed=12 | caught=True restored byte-identical=True
CONTROL LAST: vitest exit=0 failed=0 passed=51 | guard exit=0 failed=0 passed=13
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every (v, g) pair matches the block's stated reading exactly: control 51v/13g both exit 0;
m1-m5 v1g0; m6 v3g0; m7-m11 v1g0; m12 v2g0; m13-m14 v1g0; m15-m19 v0g1; control last equals
control first; every `restored byte-identical` True; final line
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` (G5).

```
$ git worktree remove --force .remedy-wt/f020-r3-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```

## Authored-text proofs

All 13 authored copies under `.agent/authored/f020-r3-*` (the block copy plus the twelve payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 13 BYTE-IDENTICAL (G1 above). `book.diff`, `product.diff` and `tests.diff` were each applied
with `git apply` after `git apply --check` passed (exit 0 both, every time), never retyped or
edited; the resulting files were verified by byte count and sha256 against the block's G2/G3
tables — all MATCH. `.agent/plan.md` was rewritten whole via `shutil.copyfile` from the payload
source — never retyped — and confirmed MATCH against the PAYLOADS table and the G2 table.
`legendModel.ts`, `glyphMatrix.ts`, `GraphLegend.tsx`, `GraphLegend.module.css`,
`legendModel.test.ts`, `glyphMatrix.test.ts` and `test_graph_legend_contract.py` were each copied
whole via `shutil.copyfile` into their product/test locations and confirmed MATCH against the
block's G3 table. `mutations.py` was run unmodified from its payload path against the fresh
`.remedy-wt/f020-r3-mut` worktree; its printed output was reported verbatim and matches the
block's stated G5 reading exactly.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1a, C1b, C1c, C1d, C1e, C2, C3, C4, C5,
exactly as ordered. G1 through G5 ran before this handback was written, as the block orders. No
payload was edited, retyped or repaired. The round's tracked path set matches constraint 3 (full
list reported in the reply via `git diff --name-only 1d954ef5 HEAD` after this commit, since that
reading is taken after C5 lands). Nothing was merged this round: no `gh pr merge`, no `gh pr
create`, no checkout of `main` after the branch was cut, no branch deletion, no force-push, no
`git stash` — per constraint 5. The reviewer's worktrees, the `f015-r*`/`f284-r*` worktrees and the
`job-*` worktrees/branches were left untouched — per constraint 6.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 300 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C1b | done | 371 insertions, matches block's expectation exactly |
| C1c | done | 195 insertions, matches block's expectation exactly |
| C1d | done | 291 insertions, matches block's expectation exactly |
| C1e | done | 200 insertions, matches block's expectation exactly |
| C2 | done | book.diff apply --check and apply both exit 0; 40/2/8 insertions, matches; D3 recorded |
| C3 | done | product.diff apply --check and apply both exit 0; 1/2/60/83/10/76/72/23/6 insertions, matches |
| C4 | done | tests.diff apply --check and apply both exit 0; 8/69/63/30/4/68 insertions, matches |
| C5 | done | committing now with this handback |
| G1 | done | all 12 payload digests and 13 authored-copy comparisons matched |
| G2 | done | all 3 named file digests matched; gate-line count 1; open set R-1008 alone; C1e..C2 path set exact |
| G3 | done | all 15 named file digests matched; C2..C3 and C3..C4 path sets exact; ruff clean |
| G4 | done | 1170 passed, 11 skipped at exit 0; all 4 named toolchain nodes ran and passed (not skipped); integrity check 6/6 pass |
| G5 | done | 19 mutations + 2 controls all matched the block's stated (v,g) readings exactly; ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True |
| G6 | pending | runs after this commit (tree/log check, worktree list, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 3. Then T003 —
transition and pulse motion with visibility pausing, the conformance assertions over the matrix
fixture's pixels, and the live fixture pass on a streamed fake job. Open findings: 1. Operator
questions open: 3.
