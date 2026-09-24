# Handback — F019 Live node materialization · Round 2 (book round 1 + T002's pure half)

## Session

SESSION 1 of feature F019 · round 2 · rounds so far 2

This round books round 1's PASS, records DECISION F019 D2, and lands T002's
pure half: `buildBrainLayout` in `buildForceBrainModel.ts` with its shapes
in `forceBrainTypes.ts`, the birth schedule in the new `brainMotion.ts`,
the two birth-motion tokens in `apps/ui/src/styles/tokens.css` and their
guard `tests/ui_contracts/test_brain_motion_tokens.py`, with vitest tests
and red proofs. I had ample context remaining throughout this round; no
session-limit pressure at any point.

## Range

Review of b6cc2690a..HEAD

## Commits

### a0a3dc267 F019 R2 C1a: copy round 2 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r2-block.md | +173/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r2-plan.md | +36/-0 | copy of the plan.md payload |

209 insertions by `git show --numstat` (block's 173 lines + 36); matches
the block's expectation exactly; under the 500-insertion cap.

### 32547eeb0 F019 R2 C1b: copy round 2 records and product diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r2-product.diff | +325/-0 | copy of the product.diff payload |
| .agent/authored/f019-r2-records.diff | +64/-0 | copy of the records.diff payload |

389 insertions by `git show --numstat`; matches the block's expectation exactly.

### f4483d6da F019 R2 C1c: copy round 2 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r2-tests.diff | +367/-0 | copy of the tests.diff payload |

367 insertions by `git show --numstat`; matches the block's expectation exactly.

### 42f64dd68 F019 R2 C1d: copy round 2 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r2-mutations.py | +346/-0 | copy of the mutations.py payload |

346 insertions by `git show --numstat`; matches the block's expectation exactly.

### c8e43121f F019 R2 C2: book round 1's PASS, record DECISION F019 D2
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +46/-0 | DECISION F019 D2 appended |
| .agent/live_review.md | +2/-0 | `Gate: F019 R1 —` entry appended |
| .agent/plan.md | +9/-9 | rewritten to the plan.md payload (round 2 scope) |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0.
Insertions by `git show --numstat`: 46 decisions.md, 2 live_review.md,
9 plan.md — matches the block's expectation exactly on every file.

### 0b4712829 F019 R2 C3: lay out the reducer's model and schedule its births
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainMotion.ts | +60/-0 | new file, the birth schedule |
| apps/ui/src/components/graph/buildForceBrainModel.ts | +171/-1 | `buildBrainLayout` and its layout constants added |
| apps/ui/src/components/graph/forceBrainTypes.ts | +46/-0 | `BrainLayoutNode`/`BrainLayoutLink`/`BrainLayoutData` added |
| apps/ui/src/styles/tokens.css | +5/-0 | `--remedy-dur-birth` and `--remedy-ease-soft` added |

60/171/46/5 insertions by `git show --numstat`; matches the block's
expectation exactly. `brainMotion.ts` was `git add`ed before commit (no
untracked product file at commit time).

### 500357997 F019 R2 C4: pin the layout, the birth schedule and the motion tokens
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainMotion.test.ts | +83/-0 | new file, vitest tests for `scheduleBrainBirths` |
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | +195/-1 | vitest tests for `buildBrainLayout` added |
| tests/ui_contracts/test_brain_motion_tokens.py | +62/-0 | new file, the token/constant contract guard |

83/195/62 insertions by `git show --numstat`; matches the block's
expectation exactly. Both new files were `git add`ed before commit.

### (this commit) F019 R2 C5: rewrite handoff for round 2
This file, rewritten, its own commit — self-reference exception per the
handback template (a handback cannot table the commit that writes it).

## External actions

- `git worktree add --detach .remedy-wt/f019-r2-mut 500357997` (G5) — real
  outcome: `Preparing worktree (detached HEAD 500357997)`, `HEAD is now at
  500357997`.
- `git worktree remove --force .remedy-wt/f019-r2-mut` (G5, after the
  mutation sweep) — real outcome: exit 0, no output.
- `git worktree prune` (G5) — real outcome: exit 0, no output.
- `git push -u origin feature/f019-live-node-materialization` runs after
  this handback is committed; its real outcome is reported in the reply
  only, per G6.
- No `gh pr` command of any kind this round. No checkout of `main`, no
  branch deletion, no force-push, no `git stash`.

## Verification

G1 TRANSPORT — all 5 payloads measured against the block's PAYLOADS table,
all matched (line count, byte count, sha256):
```
records.diff    lines=64  bytes=9957  sha256=54c531862bf89959ec01655f127d3d6ce748779b8ffcceb0e93ce91c4fad1d1a
plan.md         lines=36  bytes=1434  sha256=27b6456594fcfd7fc82af88d34c30f6da8c631ed1e85fd767910719d7b37d165
product.diff    lines=325 bytes=14833 sha256=84ddd740553e117a298e7a3cc8a57399d0176aa91873e6fed5829c4bf15a8327
tests.diff      lines=367 bytes=18134 sha256=4155efec6af89ab73ffb372b402c688d2f8e07d85d53a6afcb868ae4dfdb7db0
mutations.py    lines=346 bytes=13825 sha256=5076fbef3eefdf16820ccc642a3d6c67c7346c21337826277b1ad2d36eef8c2e
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r2-*` copy, read back with `git show
<commit>:<path>` from the commit that added it, matched its source byte
for byte (6 comparisons: the block copy against
`.remedy-wt/f019-r2/block.md`, plus the 5 payload copies) — `ALL MATCH`.

G2 THE BOOKING — at C2 (`c8e43121f`), `.agent/live_review.md` read 309572
bytes, sha256 `cf732f8ecb9c05e5ba1fd5a0af8cad22f658e3de198944c2db410058d0cd3553`
(MATCH); `.agent/decisions.md` read 2000583 bytes, sha256
`c7749033d278e777e12c9dfc5e6dcf6b5a5b463aff3832d8fe290f619c8513e6` (MATCH);
`.agent/plan.md` at C2 equals the plan.md payload byte for byte (MATCH).
The count of lines C2 adds to the ledger beginning `Gate: F019 R1 — ` is 1
(measured: 2 lines total added to live_review.md, 1 of them starting that
prefix). `open_finding_ids` (`scripts/rotate_live_review.py`) over
`.agent/live_review.md`: at `b6cc2690` → `['R-0499', 'R-0950', 'R-1008',
'R-1046']`; at C2 (`c8e43121f`) → the same four — matches the reviewer's
reading exactly at both.

G3 THE PRODUCT AND TESTS — at C4 (`500357997`), the byte count and sha256
of all 7 named files, read with `git show 500357997:<path>`, matched the
reviewer's simulated reading exactly:
```
forceBrainTypes.ts               2571 bytes  MATCH
buildForceBrainModel.ts         13454 bytes  MATCH
brainMotion.ts                   2766 bytes  MATCH
tokens.css                       3911 bytes  MATCH
buildForceBrainModel.test.ts    11980 bytes  MATCH
brainMotion.test.ts              3895 bytes  MATCH
test_brain_motion_tokens.py      2770 bytes  MATCH
```

G4 THE TESTS — real transcript, primary checkout, at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md deleted deliberately
1398 passed, 5 skipped in 72.32s (0:01:12)
REAL_EXIT=0
```
All 5 SKIPPED lines are pre-existing D3/D12 quarantine skips, unrelated to
the toolchain. The four toolchain nodes the block named (the two eslint
checks in `test_ui_lint.py`, the `tsc --noEmit` node in
`test_dashboard_contract.py`, the vitest node in `test_test_runner.py`)
do not appear in the skip list — each ran and PASSED, as the block
requires for the primary checkout. (The reviewer's sim-tree run, without
the golden path and without a built toolchain, read `1351 passed, 10
skipped`; the primary-checkout difference — 47 more passed, 5 fewer
skipped — is exactly the golden-path suite plus those four toolchain
nodes running here instead of skipping.)
```
$ python3 -m ruff check tests/ui_contracts/test_brain_motion_tokens.py
All checks passed!
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — worktree `.remedy-wt/f019-r2-mut` added detached at
C4 (`500357997`), then `python3 -B .remedy-wt/f019-r2-payloads/mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f019-r2-mut`:
```
VITEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=64
PYTEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=5
L1  builder skips clusterBrainModel: exit=1 failed=2 restored byte-identical: True
L2  task ring radius 150 -> 151: exit=1 failed=1 restored byte-identical: True
L3  golden angle replaced by a different constant: exit=1 failed=2 restored byte-identical: True
L4  child distance measured from the core instead of the task: exit=1 failed=1 restored byte-identical: True
L5  child fan not centred: exit=1 failed=1 restored byte-identical: True
L6  core not pinned (fx/fy removed): exit=1 failed=1 restored byte-identical: True
L7  a task label falls back to "" instead of the id: exit=1 failed=1 restored byte-identical: True
L8  active ignores a task whose child is in_progress: exit=1 failed=1 restored byte-identical: True
L9  link widths swapped: exit=1 failed=1 restored byte-identical: True
B1  first paint schedules births (previous === null guard removed): exit=1 failed=1 restored byte-identical: True
B2  no concurrency cap (delay = i * stagger): exit=1 failed=1 restored byte-identical: True
B3  reduced-motion duration left at 420: exit=1 failed=1 restored byte-identical: True
B4  an existing (surviving) node re-born: exit=1 failed=4 restored byte-identical: True
P1  the app token --remedy-dur-birth changed to 400ms: exit=1 failed=2 restored byte-identical: True
P2  BRAIN_BIRTH_MS changed to 400: exit=1 failed=1 restored byte-identical: True
VITEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=64
PYTEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=5
vitest control #1 green: True
vitest control #2 green: True
pytest control #1 green: True
pytest control #2 green: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every one of the 15 mutation counts matches the reviewer's sim-tree reading
exactly (L1=2, L2=1, L3=2, L4=1, L5=1, L6=1, L7=1, L8=1, L9=1, B1=1, B2=1,
B3=1, B4=4, P1=2, P2=1), both vitest controls read `64 passed` at exit 0,
both pytest controls read `5 passed` at exit 0, every restore read
byte-identical True, and the final line reads `ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: True`. `git worktree remove --force
.remedy-wt/f019-r2-mut` and `git worktree prune` both exit 0; `git
worktree list` afterward shows no `f019-r2-mut` entry, only the primary
checkout, the pre-existing `f015-r*` worktrees, `f019-r1-proto`,
`f019-r1-sim`, `f019-r2-proto`, `f019-r2-sim` and the four `job-*`
worktrees — all named by the block's constraint 6, nothing else.

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f019-r2-*` (the block copy
plus the 5 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from the commit that added it with `git show
<commit>:<path>` and compared byte for byte against its source: all 6
`MATCH` (G1 above). `records.diff` was applied with `git apply` after
`git apply --check` passed (exit 0 both), never retyped or edited; its
resulting file contents (`.agent/live_review.md`, `.agent/decisions.md`)
were verified by byte count and sha256 against the reviewer's own readings
at C2 (G2 above) — both `MATCH`; `.agent/plan.md` was separately rewritten
whole via `shutil.copyfile` from its payload and also confirmed `MATCH`.
`product.diff` and `tests.diff` were applied the same way (`git apply
--check` then `git apply`, both exit 0), never retyped or edited; the
seven resulting product/test files' C4 contents were confirmed `MATCH`
against the reviewer's simulated reading in G3 above. `mutations.py` was
copied into `.agent/authored/` (G1, matched) and run unedited from its
payload location in G5; it was never applied to a tracked file, per the
block's instruction that it is a TOOL only.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1a, C1b, C1c,
C1d, C2, C3, C4, then this handback as C5), all gates G1–G5 ran before
C5 as ordered, and no payload was edited, retyped or repaired. The
round's tracked path set matches constraint 3 exactly: `git diff
--name-only b6cc2690 HEAD` (measured just before writing this handback,
i.e. through C4) names the six `.agent/authored/f019-r2-*` copies,
`.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, and the
seven files the two product/test diffs name — this handoff's own path is
added by C5 itself. No full-suite run was made (amend0917 rule 1; F019's
belongs to its closure). No `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `README.md`, `docs/roadmap/STATUS.md` or
`docs/roadmap/features/T5_F019.md` was touched, matching this round's
scope (round 1 already carried the STATUS/context edits at the claim).

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 209 insertions, matches (173 block + 36 plan.md) |
| C1b | done | 389 insertions, matches |
| C1c | done | 367 insertions, matches |
| C1d | done | 346 insertions, matches |
| C2 | done | git apply --check and apply both exit 0; 46/2/9 insertions, matches every file |
| C3 | done | 60/171/46/5 insertions, matches; brainMotion.ts tracked before commit |
| C4 | done | 83/195/62 insertions, matches; both new files tracked before commit |
| C5 | done | this handback, rewritten per docs/agents/handback_template.md |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | live_review.md and decisions.md byte counts/sha256 matched; plan.md MATCH; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | all 7 product/test file digests matched at C4 |
| G4 | done | 1398 passed, 5 skipped (all pre-existing quarantine, none toolchain), exit 0; ruff clean; integrity check all 6 pass, fail_count 0 |
| G5 | done | all 15 mutations caught, both vitest and pytest controls green, all restores byte-identical, final line True; worktree removed and pruned |
| G6 | pending | reported in the reply, measured after this handback and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 2.
Then T002's painted half as DECISION F019 D2 (1) names it: the renderer
that paints the layout on the canvas, its mount in `BrainGraphStage.tsx`
fed by the reducer's model seeded from the dashboard, the replacement of
the dashboard builder it supersedes, and the demo recording. Open
findings: 4. Operator questions open: 2.
