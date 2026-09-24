# Handback — F020 Node lifecycle & glyph language · Round 2

## Session

SESSION 1 of feature F020 · round 2 · rounds so far 2

This round booked round 1's PASS into the live review record, recorded DECISION F020 D2, and
landed T002's first half: `renderers/palette.ts` (resolves every token the painter reads once
per mount), `renderers/paintNode.ts` (paints every non-core node from its kind's glyph and its
state's treatment, holding no colour/shape/state rule of its own), the state table's glyph ink
and body-line colours in `renderers/nodeStates.ts`, and `ForceBrainGraph.tsx` painting every
non-core kind through the painter in place of F019's placeholder sphere, with the token guard
pinning the wiring. All nine commits landed in the block's ordered sequence; all five gates
passed with exact matches to the reviewer's stated readings. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 06d185c64..HEAD

## Commits

### 0342dc16d F020 R2 C1a: copy round 2 block and plan payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r2-block.md | +249/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r2-plan.md | +34/-0 | copy of the plan.md payload |

283 insertions by `git show --numstat` (block's 249 lines + 34); matches the block's expectation
exactly; under the 500-insertion cap.

### 20864b9ea F020 R2 C1b: copy round 2 diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r2-book.diff | +61/-0 | copy of the book.diff payload |
| .agent/authored/f020-r2-product.diff | +268/-0 | copy of the product.diff payload |
| .agent/authored/f020-r2-tests.diff | +88/-0 | copy of the tests.diff payload |

417 insertions by `git show --numstat`; matches the block's expectation of 417 exactly.

### 3cbc555e3 F020 R2 C1c: copy round 2 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r2-mutations.py | +181/-0 | copy of the mutations.py payload (G5 tool) |

181 insertions by `git show --numstat`; matches the block's expectation of 181 exactly.

### 43ad8359d F020 R2 C1d: copy round 2 product modules into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r2-palette.ts | +45/-0 | copy of the palette.ts payload |
| .agent/authored/f020-r2-paintNode.ts | +132/-0 | copy of the paintNode.ts payload |

177 insertions by `git show --numstat`; matches the block's expectation of 177 exactly.

### 6264e9feb F020 R2 C1e: copy round 2 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r2-palette.test.ts | +26/-0 | copy of the palette.test.ts payload |
| .agent/authored/f020-r2-paintNode.test.ts | +206/-0 | copy of the paintNode.test.ts payload |

232 insertions by `git show --numstat`; matches the block's expectation of 232 exactly.

### fa259367c F020 R2 C2: book round 1's PASS, record D2, advance the plan
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +43/-0 | DECISION F020 D2 appended (book.diff) |
| .agent/live_review.md | +2/-0 | F020 R1 Gate entry appended (book.diff) |
| .agent/plan.md | +8/-7 | rewritten to the plan.md payload |

`git apply --check` on book.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 43 decisions.md, 2 live_review.md, 8 plan.md — matches the block's expectation
exactly; aggregate 53 insertions(+)/7 deletions(-), all attributable to plan.md's rewrite diff.

### 063081143 F020 R2 C3: paint every non-core node from the glyph and state modules in a resolved palette
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/ForceBrainGraph.tsx | +40/-64 | paints every non-core kind through paintNode in place of F019's placeholder sphere (product.diff) |
| apps/ui/src/components/graph/renderers/nodeStates.ts | +23/-2 | glyph ink and body-line colours added to the state table (product.diff) |
| apps/ui/src/components/graph/renderers/palette.ts | +45/-0 | new file: resolves every token the painter reads once per mount |
| apps/ui/src/components/graph/renderers/paintNode.ts | +132/-0 | new file: paints every non-core node from its kind's glyph and state's treatment |

`git apply --check` on product.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 40 ForceBrainGraph.tsx, 23 nodeStates.ts, 132 paintNode.ts, 45 palette.ts — matches
the block's expectation exactly.

### 632034b14 F020 R2 C4: pin the painter, the palette bridge, the glyph ink and the canvas wiring
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/renderers/nodeStates.test.ts | +17/-0 | vitest additions for the new glyph ink / body-line colours |
| apps/ui/src/components/graph/renderers/paintNode.test.ts | +206/-0 | new file: vitest goldens for paintNode.ts |
| apps/ui/src/components/graph/renderers/palette.test.ts | +26/-0 | new file: vitest goldens for palette.ts |
| tests/ui_contracts/test_node_glyph_tokens.py | +28/-3 | token guard additions pinning the canvas wiring |

`git apply --check` on tests.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 17 nodeStates.test.ts, 206 paintNode.test.ts, 26 palette.test.ts, 28
test_node_glyph_tokens.py — matches the block's expectation exactly.

### (this commit) F020 R2 C5: rewrite handoff for round 2
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f020-r2-mut 632034b14` — outcome: success, detached HEAD
  at `632034b14`.
- `git worktree remove --force .remedy-wt/f020-r2-mut` — outcome: success.
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
06d185c64 F020 R1 C5: rewrite handoff for round 1
```
All BEFORE ANYTHING ELSE checks passed at round start.

```
$ wc -l / sha256sum .remedy-wt/f020-r2/block.md
249 lines, sha256=68b3eb845088cc55bc536be1dcc3c2dfcb99c3e40db4a2e0dbd9739b1967e062
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ wc -lc / sha256sum over .remedy-wt/f020-r2-payloads/*
book.diff           lines=61  bytes=9624  sha256=756f6e8b8a856a36c9bc8d99d8887f42f2d7409fc05f28819f5e07aec97cd763
mutations.py         lines=181 bytes=9454  sha256=9d77bca61444f306536bf571c1675c448c86293bc13d15c4ed062a764a9ce6c5
paintNode.test.ts    lines=206 bytes=9071  sha256=8fdbfc95754e45c1535582de5b22ad9d45e07f99cbefc48215eaa2f76c282add
paintNode.ts         lines=132 bytes=5450  sha256=5fe0bf691ba79df127b4fa3c444c4b4fb94317468d15a956274f3e86c14313bc
palette.test.ts      lines=26  bytes=1207  sha256=2f019b3a80a234d30d887636d46e1a857fe1fda6938aaefbaffe43e68c89e604
palette.ts           lines=45  bytes=2048  sha256=0059fca296472cb660a26b809933054d365d0cf9aebfd78ab1de9babe0e8be7e
plan.md              lines=34  bytes=1325  sha256=60d57a350b0e0f8c93b4115df553e07d6bb0b6e81a8d048dffde0bb23cf2d88e
product.diff         lines=268 bytes=13052 sha256=5ab9a90a27d3faa1ee13b50002adbea53febd8e70016dde78e67ac62c4b889c6
tests.diff           lines=88  bytes=4781  sha256=66c15fe332b73ca51264c37f6b684404f2d42aac1a6dbbd5387d7fe080140040
```
All 9 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r2-* blob, read with `git show <commit>:<path>`,
   against its source)
f020-r2-block.md          @ 0342dc16d: match=True
f020-r2-plan.md           @ 0342dc16d: match=True
f020-r2-book.diff         @ 20864b9ea: match=True
f020-r2-product.diff      @ 20864b9ea: match=True
f020-r2-tests.diff        @ 20864b9ea: match=True
f020-r2-mutations.py      @ 3cbc555e3: match=True
f020-r2-palette.ts        @ 43ad8359d: match=True
f020-r2-paintNode.ts      @ 43ad8359d: match=True
f020-r2-palette.test.ts   @ 6264e9feb: match=True
f020-r2-paintNode.test.ts @ 6264e9feb: match=True
```
All 10 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's three files, read with `git show fa259367c:<path>`, against the block's G2 table)
.agent/live_review.md: bytes=290916  sha256=f7b088ac3f7677c3f33edc88aa56f5b35cd44a5601e051c7945e95bf23bdc65e match=True
.agent/decisions.md:   bytes=2033260 sha256=d4910bc8630f45ebfb3817b4b6cdd3685e200658fd4a1e26a25dbc9c226d3f79 match=True
.agent/plan.md:        bytes=1325    sha256=60d57a350b0e0f8c93b4115df553e07d6bb0b6e81a8d048dffde0bb23cf2d88e match=True
```
All 3 match the block's G2 table exactly.

```
$ git diff fa259367c^ fa259367c -- .agent/live_review.md, counting added lines starting
  "Gate: F020 R1 — "
count = 1
```
Matches the reviewer's stated reading of 1 exactly (G2).

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT at C2
fa259367c (C2) open ids: ['R-1008']
```
Reads R-1008 alone, matching the reviewer's stated reading exactly (G2).

```
$ git diff --name-only 6264e9feb fa259367c
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
```
Exactly the three paths the block's G2 table names (G2).

```
$ (sha256/bytes of C3/C4 files, read with `git show <commit>:<path>`, against the block's G3 table)
C3 apps/ui/src/components/graph/ForceBrainGraph.tsx:               bytes=13868 sha256=4fa15823837f45dd142f7d06b0bbd4c88bd73e3915178338b563c7975572aeff match=True
C3 apps/ui/src/components/graph/renderers/nodeStates.ts:           bytes=6770  sha256=de1a08c87eb9dfcf1b3004fd78da1d97a483153c5edab9d67a8996b6f5ad7b58 match=True
C3 apps/ui/src/components/graph/renderers/palette.ts:               bytes=2048  sha256=0059fca296472cb660a26b809933054d365d0cf9aebfd78ab1de9babe0e8be7e match=True
C3 apps/ui/src/components/graph/renderers/paintNode.ts:             bytes=5450  sha256=5fe0bf691ba79df127b4fa3c444c4b4fb94317468d15a956274f3e86c14313bc match=True
C4 apps/ui/src/components/graph/renderers/nodeStates.test.ts:       bytes=5947  sha256=e7102241a14d818001d2318c4b3b254dd8160d613278086e31776c7a6faae1c5 match=True
C4 tests/ui_contracts/test_node_glyph_tokens.py:                    bytes=6134  sha256=f96925c2e51f7267b891f7ec3636597298bb94c0670dec7649e6b4c5df05b442 match=True
C4 apps/ui/src/components/graph/renderers/palette.test.ts:          bytes=1207  sha256=2f019b3a80a234d30d887636d46e1a857fe1fda6938aaefbaffe43e68c89e604 match=True
C4 apps/ui/src/components/graph/renderers/paintNode.test.ts:        bytes=9071  sha256=8fdbfc95754e45c1535582de5b22ad9d45e07f99cbefc48215eaa2f76c282add match=True
```
All 8 match the block's G3 table exactly.

```
$ git diff --name-only fa259367c 063081143
apps/ui/src/components/graph/ForceBrainGraph.tsx
apps/ui/src/components/graph/renderers/nodeStates.ts
apps/ui/src/components/graph/renderers/paintNode.ts
apps/ui/src/components/graph/renderers/palette.ts
$ git diff --name-only 063081143 632034b14
apps/ui/src/components/graph/renderers/nodeStates.test.ts
apps/ui/src/components/graph/renderers/paintNode.test.ts
apps/ui/src/components/graph/renderers/palette.test.ts
tests/ui_contracts/test_node_glyph_tokens.py
```
Both name exactly the paths C3 and C4 list (G3).

```
$ python3 -m ruff check tests/ui_contracts/test_node_glyph_tokens.py
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
1165 passed, 11 skipped in 72.02s (0:01:12)
REAL_EXIT=0
```
None of the 11 SKIPPED lines are the four toolchain nodes the block names (the two
`tests/ui_contracts/test_ui_lint.py` eslint checks, the tsc node in
`tests/ui_server/test_dashboard_contract.py`, the vitest node in
`tests/orchestration/test_test_runner.py`) — all four ran and PASSED in the primary checkout, not
skipped, as required. The 11 remaining skips are pre-existing D3/D12 quarantines unrelated to this
round's paths. The reviewer's sim-tree run (without golden path) read `1118 passed, 16 skipped`;
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
$ git worktree add --detach .remedy-wt/f020-r2-mut 632034b14
Preparing worktree (detached HEAD 632034b14)
REAL_EXIT=0

$ python3 -B .remedy-wt/f020-r2-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f020-r2-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f020-r2-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=50 | guard exit=0 failed=0 passed=8
m1 (the halo is drawn at full alpha): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
m2 (the painter ignores the state's size factor): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
m3 (a run's glyph is drawn at every zoom): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
m4 (the state marks are never drawn): vitest exit=1 failed=3 | guard exit=0 failed=0 | caught=True restored=True
m5 (a mark's outline is never drawn): vitest exit=1 failed=2 | guard exit=0 failed=0 | caught=True restored=True
m6 (the artifact is drawn as a sphere): vitest exit=1 failed=3 | guard exit=0 failed=0 | caught=True restored=True
m7 (the sphere's gloss starts from the fill, not the highlight): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
m8 (a token that resolves to nothing is not named): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
m9 (a resolved value keeps the stylesheet's whitespace): vitest exit=1 failed=2 | guard exit=0 failed=0 | caught=True restored=True
m10 (the canvas paints builder runs with the core's painter): vitest exit=0 failed=0 | guard exit=1 failed=1 | caught=True restored=True
m11 (the palette is resolved again on every layout): vitest exit=0 failed=0 | guard exit=1 failed=1 | caught=True restored=True
m12 (the canvas passes a fixed zoom to the painter): vitest exit=0 failed=0 | guard exit=1 failed=1 | caught=True restored=True
m13 (a raw colour literal enters the painter): vitest exit=0 failed=0 | guard exit=1 failed=1 | caught=True restored=True
m14 (the canvas paints a state colour of its own again): vitest exit=0 failed=0 | guard exit=1 failed=1 | caught=True restored=True
m15 (a planned glyph is inked in the planned white): vitest exit=1 failed=3 | guard exit=0 failed=0 | caught=True restored=True
m16 (the sphere glyph is stroked in the highlight, not the state's ink): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
m17 (a shape kind is lined in its fill colour): vitest exit=1 failed=1 | guard exit=0 failed=0 | caught=True restored=True
CONTROL LAST: vitest exit=0 failed=0 passed=50 | guard exit=0 failed=0 passed=8
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every (v, g) pair matches the block's stated reading exactly: control 50v/8g both exit 0;
m1-m3 v1g0; m4 v3g0; m5 v2g0; m6 v3g0; m7 v1g0; m8 v1g0; m9 v2g0; m10-m14 v0g1; m15 v3g0;
m16-m17 v1g0; control last equals control first; every `restored` True; final line
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` (G5).

```
$ git worktree remove --force .remedy-wt/f020-r2-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```

## Authored-text proofs

All 10 authored copies under `.agent/authored/f020-r2-*` (the block copy plus the nine payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 10 BYTE-IDENTICAL (G1 above). `book.diff`, `product.diff` and `tests.diff` were each applied
with `git apply` after `git apply --check` passed (exit 0 both, every time), never retyped or
edited; the resulting files were verified by byte count and sha256 against the block's G2/G3
tables — all MATCH. `.agent/plan.md` was rewritten whole via `shutil.copyfile` from the payload
source — never retyped — and confirmed MATCH against the PAYLOADS table and the G2 table.
`palette.ts`, `paintNode.ts`, `palette.test.ts` and `paintNode.test.ts` were each copied whole via
`shutil.copyfile` into their product/test locations and confirmed MATCH against the block's G3
table. `mutations.py` was run unmodified from its payload path against the fresh
`.remedy-wt/f020-r2-mut` worktree; its printed output was reported verbatim and matches the
block's stated G5 reading exactly.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1a, C1b, C1c, C1d, C1e, C2, C3, C4, C5,
exactly as ordered. G1 through G5 ran before this handback was written, as the block orders. No
payload was edited, retyped or repaired. The round's tracked path set matches constraint 3 (full
list reported in the reply via `git diff --name-only 06d185c6 HEAD` after this commit, since that
reading is taken after C5 lands). Nothing was merged this round: no `gh pr merge`, no `gh pr
create`, no checkout of `main` after the branch was cut, no branch deletion, no force-push, no
`git stash` — per constraint 5. The reviewer's worktrees, the `f015-r*`/`f284-r*` worktrees and the
`job-*` worktrees/branches were left untouched — per constraint 6.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 283 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C1b | done | 417 insertions, matches block's expectation exactly |
| C1c | done | 181 insertions, matches block's expectation exactly |
| C1d | done | 177 insertions, matches block's expectation exactly |
| C1e | done | 232 insertions, matches block's expectation exactly |
| C2 | done | book.diff apply --check and apply both exit 0; 43/2/8 insertions, matches; D2 recorded |
| C3 | done | product.diff apply --check and apply both exit 0; 40/23/132/45 insertions, matches |
| C4 | done | tests.diff apply --check and apply both exit 0; 17/206/26/28 insertions, matches |
| C5 | done | committing now with this handback |
| G1 | done | all 9 payload digests and 10 authored-copy comparisons matched |
| G2 | done | all 3 named file digests matched; gate-line count 1; open set R-1008 alone; C1e..C2 path set exact |
| G3 | done | all 8 named file digests matched; C2..C3 and C3..C4 path sets exact; ruff clean |
| G4 | done | 1165 passed, 11 skipped at exit 0; all 4 named toolchain nodes ran and passed (not skipped); integrity check 6/6 pass |
| G5 | done | 17 mutations + 2 controls all matched the block's stated (v,g) readings exactly; ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True |
| G6 | pending | runs after this commit (tree/log check, worktree list, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2. Then T002's second
half — the legend popover from the graph's chrome, enumerated from the glyph and state modules,
the cluster's count, and the kind-by-state matrix fixture. Open findings: 1. Operator questions
open: 3.
