# Handback — F020 Node lifecycle & glyph language · Round 1

## Session

SESSION 1 of feature F020 · round 1 · rounds so far 1

This round cut `feature/f020-node-lifecycle-glyph-language` from `main` at `955a6240` (the F284
merge), claimed F020, re-headed `.agent/live_review.md` with F284's round 4 PASS, recorded
DECISION F020 D1, flipped F020's STATUS line to `[~]`, and landed T001: `glyphPaths.ts` (every
node kind's glyph as SVG path strings) and `nodeStates.ts` (every state's treatment naming design
tokens only) under the new directory `apps/ui/src/components/graph/renderers/`, their vitest
tests, the two new design tokens (`--remedy-state-vetoed`, `--remedy-graph-node-ring`), and the
token guard `tests/ui_contracts/test_node_glyph_tokens.py`, with 16 red proofs all caught and
restored cleanly. I had ample context remaining throughout this round; no session-limit pressure
at any point.

## Range

Review of 955a6240d..HEAD

## Commits

### 572c8aecb F020 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r1-block.md | +263/-0 | copy of this round's block, verbatim |
| .agent/authored/f020-r1-context.md | +38/-0 | copy of the context.md payload |
| .agent/authored/f020-r1-plan.md | +33/-0 | copy of the plan.md payload |

334 insertions by `git show --numstat` (block's 263 lines + 71); matches the block's expectation
exactly; under the 500-insertion cap.

### b569b45ac F020 R1 C1b: copy round 1 claim and token diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r1-claim.diff | +127/-0 | copy of the claim.diff payload |
| .agent/authored/f020-r1-tokens.diff | +41/-0 | copy of the tokens.diff payload |

168 insertions by `git show --numstat`; matches the block's expectation of 168 exactly.

### 06bc60417 F020 R1 C1c: copy round 1 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r1-mutations.py | +182/-0 | copy of the mutations.py payload (G5 tool) |

182 insertions by `git show --numstat`; matches the block's expectation of 182 exactly.

### 7222cfb3e F020 R1 C1d: copy round 1 product modules into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r1-glyphPaths.ts | +181/-0 | copy of the glyphPaths.ts payload |
| .agent/authored/f020-r1-nodeStates.ts | +156/-0 | copy of the nodeStates.ts payload |

337 insertions by `git show --numstat`; matches the block's expectation of 337 exactly.

### 07247b313 F020 R1 C1e: copy round 1 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f020-r1-glyphPaths.test.ts | +225/-0 | copy of the glyphPaths.test.ts payload |
| .agent/authored/f020-r1-nodeStates.test.ts | +129/-0 | copy of the nodeStates.test.ts payload |
| .agent/authored/f020-r1-test_node_glyph_tokens.py | +110/-0 | copy of the test_node_glyph_tokens.py payload |

464 insertions by `git show --numstat`; matches the block's expectation of 464 exactly.

### e1a069478 F020 R1 C2: claim F020, re-head the live review record, book F284 R4, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +13/-11 | rewritten to the context.md payload |
| .agent/decisions.md | +56/-0 | DECISION F020 D1 appended (claim.diff) |
| .agent/live_review.md | +28/-9 | re-head plus F284 R4 Gate entry appended (claim.diff) |
| .agent/plan.md | +20/-16 | rewritten to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F020's line `[ ]` → `[~]` (claim.diff) |

`git apply --check` on claim.diff: exit 0. `git apply`: exit 0. Insertions/deletions by
`git show --numstat`: 13/11 context.md, 56/0 decisions.md, 28/9 live_review.md, 20/16 plan.md, 1/1
STATUS.md — matches the block's expectation exactly.

### d9f585b23 F020 R1 C3: draw every node kind from one glyph source and every state from tokens
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/renderers/glyphPaths.ts | +181/-0 | new file: every node kind's glyph as SVG path strings |
| apps/ui/src/components/graph/renderers/nodeStates.ts | +156/-0 | new file: every state's treatment naming design tokens only |
| apps/ui/src/styles/tokens.css | +5/-0 | tokens.diff: `--remedy-state-vetoed`, `--remedy-graph-node-ring` |
| docs/ui/design_reference/tokens.css | +1/-0 | tokens.diff: `--remedy-state-vetoed` mirrored into the reference sheet |
| docs/ui/design_reference/tokens_rules.md | +2/-0 | tokens.diff: the two new tokens' rule lines |

`git apply --check` on tokens.diff: exit 0. `git apply`: exit 0. Insertions by `git show
--numstat`: 181 glyphPaths.ts, 156 nodeStates.ts, 5 tokens.css, 1 docs tokens.css, 2
tokens_rules.md — matches the block's expectation exactly.

### bef276a78 F020 R1 C4: pin the glyph goldens, the state language and the token guard
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/renderers/glyphPaths.test.ts | +225/-0 | vitest goldens for glyphPaths.ts |
| apps/ui/src/components/graph/renderers/nodeStates.test.ts | +129/-0 | vitest goldens for nodeStates.ts |
| tests/ui_contracts/test_node_glyph_tokens.py | +110/-0 | token guard: state module names tokens only |

Insertions by `git show --numstat`: 225 glyphPaths.test.ts, 129 nodeStates.test.ts, 110
test_node_glyph_tokens.py — matches the block's expectation exactly.

### (this commit) F020 R1 C5: rewrite handoff for round 1
Self-reference exception per the handback template (a handback cannot table the commit that
writes it).
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f020-r1-mut bef276a78` — outcome: success, detached HEAD
  at `bef276a78`.
- `git worktree remove --force .remedy-wt/f020-r1-mut` — outcome: success.
- `git worktree prune` — outcome: success, no output.
- `git push -u origin feature/f020-node-lifecycle-glyph-language` — runs AFTER this commit lands;
  its real outcome is reported in the reply, since this handback cannot contain an outcome that
  happens after it. No `gh pr create` this round: the block orders the branch to open its PR at
  F020's closure, not here.

## Verification

```
$ ls .agent/STOP
ls: cannot access '.agent/STOP': No such file or directory (absent, as required)

$ pwd
/home/decodeux/Repos/remedy
$ git status --porcelain
(empty)
$ git branch --show-current
main
$ git log --oneline -1
955a6240d Merge pull request #276 from UndefinedDatabase/feature/f284-findings-paydown-v3
```
All BEFORE ANYTHING ELSE checks passed at round start, before the branch was cut.

```
$ git checkout -b feature/f020-node-lifecycle-glyph-language
Switched to a new branch 'feature/f020-node-lifecycle-glyph-language'
```

```
$ wc -l / sha256sum .remedy-wt/f020-r1/block.md
263 lines, sha256=530439682c480004ac7e2062c24a75af42e229bb541b7199b0eee9f372179e19
```
Matches both readings given in the delegation message exactly (R-0954).

```
$ wc -lc / sha256sum over .remedy-wt/f020-r1-payloads/*
claim.diff                 lines=127 bytes=15248 sha256=9597baf5746e1586792d9c69a2f72c7d8b9e8ad3ec7845af805dd416faf7fd46
context.md                 lines=38  bytes=1676  sha256=cb92943f462e868eb1dbc33943d594536b30a16bf48248ae5a396c0f3e7c7b4a
glyphPaths.test.ts         lines=225 bytes=8816  sha256=b60ecd4aecba5d2a840bf07ed368d99b2d8fa7e35e739ccb4056aa9250968699
glyphPaths.ts               lines=181 bytes=6541  sha256=4c440b9217718edff780fddac75e8a413fd86bdf52104ad4c2e74dc8a348c8e2
mutations.py                lines=182 bytes=9233  sha256=ddb9db2dc73e2165913b7d861e2696a3bd30fd836629c75ca127b2094456e5a4
nodeStates.test.ts          lines=129 bytes=5165  sha256=34063c8af201ff4f7832d81a439abab0ebf1364bc2edbdfb3688a8b34ab3c885
nodeStates.ts                lines=156 bytes=5831  sha256=74b81d8f8d4cec4be3e6e375d96fb2fa4bb12813a04e48942eab82a9c5e21316
plan.md                      lines=33  bytes=1317  sha256=5e20ffbf9c71497548e91949ee7a739ae15db35a153cbc25a7897a712debc386
test_node_glyph_tokens.py    lines=110 bytes=4719  sha256=e7daf334a6d45461a6646f1cf62a65794362a8bc60a24f071b1c83e9f215e5db
tokens.diff                  lines=41  bytes=2186  sha256=13160072813b7ca734b3eb98f7c3426749b45cd792d3eb123b3d2e46239d8f1e
```
All 10 match the PAYLOADS table exactly (G1).

```
$ (compare each committed .agent/authored/f020-r1-* blob, read with `git show <commit>:<path>`,
   against its source)
f020-r1-block.md                  @ 572c8aecb: match=True
f020-r1-plan.md                   @ 572c8aecb: match=True
f020-r1-context.md                @ 572c8aecb: match=True
f020-r1-claim.diff                @ b569b45ac: match=True
f020-r1-tokens.diff               @ b569b45ac: match=True
f020-r1-mutations.py              @ 06bc60417: match=True
f020-r1-glyphPaths.ts             @ 7222cfb3e: match=True
f020-r1-nodeStates.ts             @ 7222cfb3e: match=True
f020-r1-glyphPaths.test.ts        @ 07247b313: match=True
f020-r1-nodeStates.test.ts        @ 07247b313: match=True
f020-r1-test_node_glyph_tokens.py @ 07247b313: match=True
```
All 11 BYTE-IDENTICAL against their sources (G1).

```
$ (sha256/bytes of C2's five files, read with `git show e1a069478:<path>`, against the block's G2 table)
.agent/live_review.md:  bytes=288899  sha256=2a3e1c928766677821aff55f37cefaf6128dccda1672a51b0be86c4743b9cecb match=True
docs/roadmap/STATUS.md: bytes=51033   sha256=def827f05e4cf8a0d569a793db20324df78e293ce539b890677777cd1d541e6c match=True
.agent/decisions.md:    bytes=2029556 sha256=774b744d0a0007770aedc48fcef3f0856440f9a7879a565245aa0d08161a5e12 match=True
.agent/plan.md:         bytes=1317    sha256=5e20ffbf9c71497548e91949ee7a739ae15db35a153cbc25a7897a712debc386 match=True
.agent/context.md:      bytes=1676    sha256=cb92943f462e868eb1dbc33943d594536b30a16bf48248ae5a396c0f3e7c7b4a match=True
```
All 5 match the block's G2 table exactly.

```
$ open_finding_ids(text) from scripts/rotate_live_review.py, over .agent/live_review.md's TEXT
955a6240d open ids: ['R-1008']
e1a069478 (C2) open ids: ['R-1008']
```
Both read R-1008 alone, matching the reviewer's stated reading exactly (G2).

```
$ git show e1a069478:docs/roadmap/STATUS.md | grep F020
- [~] F020 — Node lifecycle & glyph language
```
Matches the required reading exactly (G2).

```
$ git diff --name-only 07247b313 e1a069478
.agent/context.md
.agent/decisions.md
.agent/live_review.md
.agent/plan.md
docs/roadmap/STATUS.md
```
Exactly the five paths the block's G2 table names (G2).

```
$ (sha256/bytes of C3/C4 files, read with `git show <commit>:<path>`, against the block's G3 table)
C3 apps/ui/src/styles/tokens.css:                                bytes=4224 sha256=58c22798a2a1f12ba65d08986349d96b0e43f330479e5749ff138490d4e7bbf9 match=True
C3 docs/ui/design_reference/tokens.css:                          bytes=7109 sha256=912c39cb4d7e8a11e9bc2819a0f0dac09294ae89741d2c6417de5b37302d52a5 match=True
C3 docs/ui/design_reference/tokens_rules.md:                     bytes=3158 sha256=d0ef701deb923f1c74ef7e4cf9daa5a3b8f9a9b1b676e8fda7d14c0ef00962b5 match=True
C3 apps/ui/src/components/graph/renderers/glyphPaths.ts:         bytes=6541 sha256=4c440b9217718edff780fddac75e8a413fd86bdf52104ad4c2e74dc8a348c8e2 match=True
C3 apps/ui/src/components/graph/renderers/nodeStates.ts:         bytes=5831 sha256=74b81d8f8d4cec4be3e6e375d96fb2fa4bb12813a04e48942eab82a9c5e21316 match=True
C4 apps/ui/src/components/graph/renderers/glyphPaths.test.ts:    bytes=8816 sha256=b60ecd4aecba5d2a840bf07ed368d99b2d8fa7e35e739ccb4056aa9250968699 match=True
C4 apps/ui/src/components/graph/renderers/nodeStates.test.ts:    bytes=5165 sha256=34063c8af201ff4f7832d81a439abab0ebf1364bc2edbdfb3688a8b34ab3c885 match=True
C4 tests/ui_contracts/test_node_glyph_tokens.py:                 bytes=4719 sha256=e7daf334a6d45461a6646f1cf62a65794362a8bc60a24f071b1c83e9f215e5db match=True
```
All 8 match the block's G3 table exactly.

```
$ git diff --name-only e1a069478 d9f585b23
apps/ui/src/components/graph/renderers/glyphPaths.ts
apps/ui/src/components/graph/renderers/nodeStates.ts
apps/ui/src/styles/tokens.css
docs/ui/design_reference/tokens.css
docs/ui/design_reference/tokens_rules.md
$ git diff --name-only d9f585b23 bef276a78
apps/ui/src/components/graph/renderers/glyphPaths.test.ts
apps/ui/src/components/graph/renderers/nodeStates.test.ts
tests/ui_contracts/test_node_glyph_tokens.py
```
Both name exactly the paths C3 and C4 list (G3).

```
$ python3 -m ruff check tests/ui_contracts/test_node_glyph_tokens.py
All checks passed!
REAL_EXIT=0
```

```
$ bash -c 'python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py
  tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py
  tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py
  tests/orchestration/test_block_lint.py tests/test_agent_tooling.py tests/regression/test_resource_safety.py
  tests/docs tests/cli/test_golden_path.py 2>&1 | tail -15; echo "REAL_EXIT=${PIPESTATUS[0]}"'
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252) ...
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252) ...
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252) ...
1482 passed, 5 skipped in 83.19s (0:01:23)
REAL_EXIT=0
```
None of the 5 SKIPPED lines are the four toolchain nodes the block names (the two
`tests/ui_contracts/test_ui_lint.py` eslint checks, the tsc node in
`tests/ui_server/test_dashboard_contract.py`, the vitest node in
`tests/orchestration/test_test_runner.py`) — all four ran and PASSED in the primary checkout, not
skipped, as required. The 5 remaining skips are pre-existing D3/D12 quarantines unrelated to this
round's paths (G4).

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
$ git worktree add --detach .remedy-wt/f020-r1-mut bef276a78
Preparing worktree (detached HEAD bef276a78)
REAL_EXIT=0

$ python3 -B .remedy-wt/f020-r1-payloads/mutations.py /home/decodeux/Repos/remedy/.remedy-wt/f020-r1-mut
worktree: /home/decodeux/Repos/remedy/.remedy-wt/f020-r1-mut
CONTROL FIRST: vitest exit=0 failed=0 passed=31 | guard exit=0 failed=0 passed=6
m1 (the builder glyph's geometry drifts): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m2 (the flask's declared bounds stop short of its base): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m3 (glyphPath2D rebuilds its paths on every call): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m4 (the canvas stroke is built from the fill string): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m5 (run glyphs show from a lower zoom than L1): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m6 (glyphTransform scales the box to the radius, not the diameter): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m7 (a failed node loses its status dot): v exit=1 failed=3 | g exit=0 failed=0 | caught=True restored=True
m8 (a veto no longer dims what hangs below it): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m9 (a planned node is drawn full size): v exit=1 failed=2 | g exit=0 failed=0 | caught=True restored=True
m10 (reduced motion still pulses): v exit=1 failed=1 | g exit=0 failed=0 | caught=True restored=True
m11 (the in-progress state is painted with the open token): v exit=1 failed=1 | g exit=1 failed=1 | caught=True restored=True
m12 (the vetoed state names a token the sheet never declares): v exit=1 failed=2 | g exit=1 failed=1 | caught=True restored=True
m13 (the pulse constant drifts from --remedy-dur-pulse): v exit=1 failed=1 | g exit=1 failed=1 | caught=True restored=True
m14 (a raw colour literal enters the state module): v exit=0 failed=0 | g exit=1 failed=1 | caught=True restored=True
m15 (the app sheet's vetoed grey drifts from the reference): v exit=0 failed=0 | g exit=1 failed=1 | caught=True restored=True
m16 (the glyph module's header misquotes the precedence rule): v exit=0 failed=0 | g exit=1 failed=1 | caught=True restored=True
CONTROL LAST: vitest exit=0 failed=0 passed=31 | guard exit=0 failed=0 passed=6
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every (v, g) pair matches the block's stated reading exactly: control 31v/6g both exit 0; m1-m10
v1g0; m7 v3g0; m9 v2g0; m11-m13 v1g1; m12 v2g1; m14-m16 v0g1; control last equals control first;
every `restored` True; final line `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True` (G5).

```
$ git worktree remove --force .remedy-wt/f020-r1-mut
REAL_EXIT=0
$ git worktree prune
REAL_EXIT=0
```

## Authored-text proofs

All 11 authored copies under `.agent/authored/f020-r1-*` (the block copy plus the ten payload
copies) were built by `shutil.copyfile` from source to destination — never retyped, never edited.
Each was read back with `git show <commit>:<path>` and compared byte for byte against its source:
all 11 BYTE-IDENTICAL (G1 above). `claim.diff` and `tokens.diff` were each applied with `git apply`
after `git apply --check` passed (exit 0 both, every time), never retyped or edited; the resulting
files were verified by byte count and sha256 against the block's G2/G3 tables — all MATCH.
`.agent/plan.md` and `.agent/context.md` were rewritten whole via `shutil.copyfile` from the
payload sources — never retyped — and confirmed MATCH against the PAYLOADS table and the G2 table.
`glyphPaths.ts`, `nodeStates.ts`, `glyphPaths.test.ts`, `nodeStates.test.ts` and
`test_node_glyph_tokens.py` were each copied whole via `shutil.copyfile` into their product/test
locations and confirmed MATCH against the block's G3 table. `mutations.py` was run unmodified from
its payload path against the fresh `.remedy-wt/f020-r1-mut` worktree; its printed output was
reported verbatim and matches the block's stated G5 reading exactly.

## Deviations & assumptions

None. Every commit landed in the block's stated order C1a, C1b, C1c, C1d, C1e, C2, C3, C4, C5,
exactly as ordered. G1 through G5 ran before this handback was written, as the block orders. No
payload was edited, retyped or repaired. The round's tracked path set matches constraint 3 (full
list reported in the reply via `git diff --name-only 955a6240 HEAD` after this commit, since that
reading is taken after C5 lands). Nothing was merged this round: no `gh pr merge`, no `gh pr
create`, no checkout of `main` after the branch was cut, no branch deletion, no force-push, no
`git stash` — per constraint 5. The reviewer's worktrees, the `f015-r*`/`f284-r*` worktrees and the
`job-*` worktrees/branches were left untouched — per constraint 6.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 334 insertions, matches block's expectation exactly; under the 500-insertion cap |
| C1b | done | 168 insertions, matches block's expectation exactly |
| C1c | done | 182 insertions, matches block's expectation exactly |
| C1d | done | 337 insertions, matches block's expectation exactly |
| C1e | done | 464 insertions, matches block's expectation exactly |
| C2 | done | claim.diff apply --check and apply both exit 0; 13/11, 56/0, 28/9, 20/16, 1/1 insertions/deletions, matches; D1 recorded |
| C3 | done | tokens.diff apply --check and apply both exit 0; 181/156/5/1/2 insertions, matches |
| C4 | done | 225/129/110 insertions, matches |
| C5 | done | committing now with this handback |
| G1 | done | all 10 payload digests and 11 authored-copy comparisons matched |
| G2 | done | all 5 named file digests matched; STATUS line text exact; open set R-1008 at both points; C1e..C2 path set exact |
| G3 | done | all 8 named file digests matched; C2..C3 and C3..C4 path sets exact; ruff clean |
| G4 | done | 1482 passed, 5 skipped at exit 0; all 4 named toolchain nodes ran and passed (not skipped); integrity check 6/6 pass |
| G5 | done | 16 mutations + 2 controls all matched the block's stated (v,g) readings exactly; ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True |
| G6 | pending | runs after this commit (tree/log check, worktree list, push, `gh pr list`); reported in the reply |
| PUSH | pending | `git push -u origin feature/f020-node-lifecycle-glyph-language`, reported in the reply |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1. Then T002 — the canvas
painter reading both modules in place of F019's glyph slots through the palette bridge
`renderers/palette.ts`, the legend generated from the same source, and the kind-by-state matrix
fixture. Open findings: 1. Operator questions open: 3.
