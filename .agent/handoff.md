# Handback — F019 Live node materialization · Round 3 (book round 2 + mount the live renderer)

## Session

SESSION 2 of feature F019 · round 3 · rounds so far 3

This round books round 2's PASS, records DECISION F019 D3 and operator note
Q3, and lands the first part of T002's painted half: the new pure module
`brainView.ts`, the rewritten `ForceBrainGraph.tsx` that paints
`buildBrainLayout`'s output, and `BrainGraphStage.tsx` mounting it by
default while `BrainGraphCanvas.tsx` stays the simple view, with vitest
tests, a source guard and red proofs. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of fd976586..HEAD

## Commits

### 834fa715c F019 R3 C1a: copy round 3 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r3-block.md | +187/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r3-plan.md | +37/-0 | copy of the plan.md payload |

224 insertions by `git show --numstat` (block's 187 lines + 37); matches
the block's expectation exactly; under the 500-insertion cap.

### de1b2df1c F019 R3 C1b: copy round 3 records and product diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r3-product.diff | +252/-0 | copy of the product.diff payload |
| .agent/authored/f019-r3-records.diff | +106/-0 | copy of the records.diff payload |

358 insertions by `git show --numstat`; matches the block's expectation
(358) exactly.

### 449613bdd F019 R3 C1c: copy round 3 renderer diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r3-renderer.diff | +467/-0 | copy of the renderer.diff payload |

467 insertions by `git show --numstat`; matches the block's expectation
exactly.

### ecddca9c5 F019 R3 C1d: copy round 3 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r3-tests.diff | +350/-0 | copy of the tests.diff payload |

350 insertions by `git show --numstat`; matches the block's expectation
exactly.

### 746adf306 F019 R3 C1e: copy round 3 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r3-mutations.py | +331/-0 | copy of the mutations.py payload |

331 insertions by `git show --numstat`; matches the block's expectation
exactly.

### 78a869440 F019 R3 C2: book round 2's PASS, record DECISION F019 D3 and operator note Q3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +55/-0 | DECISION F019 D3 appended |
| .agent/live_review.md | +2/-0 | `Gate: F019 R2 —` entry appended |
| .agent/operator_questions.md | +25/-0 | operator note Q3 appended |
| .agent/plan.md | +10/-9 | rewritten to the plan.md payload (round 3 scope) |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0.
Insertions by `git show --numstat`: 55 decisions.md, 2 live_review.md, 25
operator_questions.md, 10 plan.md — matches the block's expectation
exactly on every file.

### 62cd77d48 F019 R3 C3: paint the reducer's model on the stage, keep the SVG picture as simple view
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/ForceBrainGraph.tsx | +261/-134 | rewritten to paint `buildBrainLayout`'s model |
| apps/ui/src/components/graph/brainView.ts | +132/-0 | new file, the pure stage-glue module |
| apps/ui/src/components/graph/BrainGraphStage.tsx | +40/-2 | mounts the painted renderer by default |
| apps/ui/src/components/graph/BrainGraphStage.module.css | +16/-0 | stage styling for the mounted renderer |
| apps/ui/src/components/graph/buildForceBrainModel.ts | +1/-1 | `seededRng` exported |
| apps/ui/src/types/react-force-graph-2d.d.ts | +4/-0 | `autoPauseRedraw` prop typed |

261/132/40/16/1/4 insertions by `git show --numstat`; matches the block's
expectation exactly on every file. `git apply --check` then `git apply`
on renderer.diff: exit 0 both. `git apply --check` then `git apply` on
product.diff: exit 0 both. `brainView.ts` was `git add`ed before commit
(no untracked product file at commit time).

### febaac8e5 F019 R3 C4: pin the stage glue, the mount and the selection mapping
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainView.test.ts | +223/-0 | new file, vitest tests for `brainView.ts` |
| tests/ui_contracts/test_brain_stage_mount.py | +115/-0 | new file, the mount/source guard |

223/115 insertions by `git show --numstat`; matches the block's
expectation exactly. `git apply --check` then `git apply` on tests.diff:
exit 0 both. Both new files were `git add`ed before commit.

### (this commit) F019 R3 C5: rewrite handoff for round 3
This file, rewritten, its own commit — self-reference exception per the
handback template (a handback cannot table the commit that writes it).

## External actions

- `git worktree add --detach .remedy-wt/f019-r3-mut febaac8e5` (G5) — real
  outcome: `Preparing worktree (detached HEAD febaac8e5)`, `HEAD is now at
  febaac8e5`.
- `git worktree remove --force .remedy-wt/f019-r3-mut` (G5, after the
  mutation sweep) — real outcome: exit 0, no output.
- `git worktree prune` (G5) — real outcome: exit 0, no output.
- `git push origin feature/f019-live-node-materialization` runs after
  this handback is committed; its real outcome is reported in the reply
  only, per G6.
- No `gh pr` command of any kind this round. No checkout of `main`, no
  branch deletion, no force-push, no `git stash`.

## Verification

G1 TRANSPORT — all 6 payloads measured against the block's PAYLOADS table,
all matched (line count, byte count, sha256):
```
records.diff    lines=106 bytes=12760 sha256=268e5cdb6eca78f2e580ad53e6e101bbde81ba0d73abed4bf07a725150a3005a
plan.md         lines=37  bytes=1495  sha256=80ac140ae3a98e9ed83530f313ea10639f9224906ce28d4106a7da9ad48facf7
renderer.diff   lines=467 bytes=20766 sha256=2f63160e5083507d5233bab7ecbc274a9b2bbeddd1e45a659305cfc05fc0a207
product.diff    lines=252 bytes=12490 sha256=ae15a39f9445ef74b31f5dbee0f57333010b114b89335ebbfac610c65441a98f
tests.diff      lines=350 bytes=13864 sha256=706881818b66022c0347298113a374c5e5d79f4ee9c42914b05b7006031333fe
mutations.py    lines=331 bytes=13896 sha256=cbc4242f3b7f83315efe2cc18dcee311b69f3402af78be6027ce5bd815dd76ad
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r3-*` copy, read back with `git show
<commit>:<path>` from the commit that added it, matched its source byte
for byte (7 comparisons: the block copy against
`.remedy-wt/f019-r3/block.md`, plus the 6 payload copies) — `ALL MATCH`.

G2 THE BOOKING — at C2 (`78a869440`), `.agent/decisions.md` read 2005325
bytes, sha256 `a3b512551ff10e96413676aa3782f9a6f6db72d2ad7cda18cb028c8a3e4e9ffc`
(MATCH); `.agent/live_review.md` read 311422 bytes, sha256
`447a154146f1ce0fe2071d27b1e4eb26764f72aa0bfe72f7a5037d685b85838b` (MATCH);
`.agent/operator_questions.md` read 5681 bytes, sha256
`3c7f2c772af005e7bc961e6b086e73abf028da3e7603b817aaf0d119076b0aee` (MATCH);
`.agent/plan.md` at C2 read 1495 bytes, sha256
`80ac140ae3a98e9ed83530f313ea10639f9224906ce28d4106a7da9ad48facf7` (MATCH,
equal to the plan.md payload). The count of lines C2 adds to the ledger
beginning `Gate: F019 R2 — ` is 1 (measured: `grep -c` over C2's
`.agent/live_review.md`). `open_finding_ids` (`scripts/rotate_live_review.py`)
over `.agent/live_review.md`: at `fd976586` → `['R-0499', 'R-0950',
'R-1008', 'R-1046']`; at C2 (`78a869440`) → the same four — matches the
reviewer's reading exactly at both.

G3 THE PRODUCT AND TESTS — at C4 (`febaac8e5`), the byte count and sha256
of all 8 named files, read with `git show febaac8e5:<path>`, matched the
reviewer's simulated reading exactly:
```
ForceBrainGraph.tsx              14829 bytes  MATCH
brainView.ts                      6725 bytes  MATCH
BrainGraphStage.tsx               2647 bytes  MATCH
BrainGraphStage.module.css        1087 bytes  MATCH
buildForceBrainModel.ts          13461 bytes  MATCH
react-force-graph-2d.d.ts         2767 bytes  MATCH
brainView.test.ts                 8721 bytes  MATCH
test_brain_stage_mount.py         4327 bytes  MATCH
```

G4 THE TESTS — real transcript, primary checkout, at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md deleted deliberately
1417 passed, 5 skipped in 71.51s (0:01:11)
REAL_EXIT=0
```
All 5 SKIPPED lines are pre-existing D3/D12 quarantine skips, unrelated to
the toolchain. The four toolchain nodes the block named (the two eslint
checks in `test_ui_lint.py`, the `tsc --noEmit` node in
`test_dashboard_contract.py`, the vitest node in `test_test_runner.py`)
do not appear in the skip list — each ran and PASSED, as the block
requires for the primary checkout. (The reviewer's sim-tree run, without
the golden path, read `1370 passed, 10 skipped`; the primary-checkout
difference — 47 more passed, 5 fewer skipped — is exactly the golden-path
suite plus those four toolchain nodes running here instead of skipping.)
```
$ python3 -m ruff check tests/ui_contracts/test_brain_stage_mount.py
All checks passed!
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — worktree `.remedy-wt/f019-r3-mut` added detached at
C4 (`febaac8e5`), then `python3 -B .remedy-wt/f019-r3-payloads/mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f019-r3-mut`:
```
VITEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=89
PYTEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=19
V1  the table maps done to running: exit=1 failed=1 restored byte-identical: True
V2  rank is not the index (index + 1): exit=1 failed=1 restored byte-identical: True
V3  filterBrainLayout keeps planned tasks under open: exit=1 failed=1 restored byte-identical: True
V4  a depth-2 node kept regardless of its parent: exit=1 failed=1 restored byte-identical: True
V5  a link kept when only its source is kept: exit=1 failed=1 restored byte-identical: True
V6  "all" returns a copy instead of the same object: exit=1 failed=1 restored byte-identical: True
V7  selectedBrainNodeId ignores nodeId: exit=1 failed=1 restored byte-identical: True
V8  selectionTaskIdOf returns the run's own id for a run: exit=1 failed=2 restored byte-identical: True
V9  carryBrainPositions copies fx/fy from previous: exit=1 failed=1 restored byte-identical: True
V10 carryBrainPositions ignores previous x/y: exit=1 failed=1 restored byte-identical: True
V11 shellSelectionIdOf returns the bare task id: exit=1 failed=1 restored byte-identical: True
S1  the stage mounts BrainGraphCanvas only (ForceBrainGraph element deleted): exit=1 failed=2 restored byte-identical: True
S2  the particle expression drops reducedMotion: exit=1 failed=1 restored byte-identical: True
S3  the stage stops calling shellSelectionIdOf (mapped callback replaced by the raw onSelectNode): exit=1 failed=1 restored byte-identical: True
VITEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=89
PYTEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=19
vitest control #1 green: True
vitest control #2 green: True
pytest control #1 green: True
pytest control #2 green: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every one of the 14 mutation counts matches the reviewer's sim-tree reading
exactly (V1=1, V2=1, V3=1, V4=1, V5=1, V6=1, V7=1, V8=2, V9=1, V10=1,
V11=1, S1=2, S2=1, S3=1), both vitest controls read `89 passed` at exit 0,
both pytest controls read `19 passed` at exit 0, every restore read
byte-identical True, and the final line reads `ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: True`. `git worktree remove --force
.remedy-wt/f019-r3-mut` and `git worktree prune` both exit 0; `git
worktree list` afterward shows no `f019-r3-mut` entry, only the primary
checkout, the pre-existing `f015-r*` worktrees, `f019-r2-sim`,
`f019-r3-proto`, `f019-r3-sim` and the four `job-*` worktrees — all named
by the block's constraint 6, nothing else.

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 7 authored copies under `.agent/authored/f019-r3-*` (the block copy
plus the 6 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from the commit that added it with `git show
<commit>:<path>` and compared byte for byte against its source: all 7
`MATCH` (G1 above). `records.diff` was applied with `git apply` after
`git apply --check` passed (exit 0 both), never retyped or edited; its
resulting file contents (`.agent/decisions.md`, `.agent/live_review.md`,
`.agent/operator_questions.md`) were verified by byte count and sha256
against the reviewer's own readings at C2 (G2 above) — all `MATCH`;
`.agent/plan.md` was separately rewritten whole via `shutil.copyfile`
from its payload and also confirmed `MATCH`. `renderer.diff` and
`product.diff` were applied the same way (`git apply --check` then `git
apply`, both exit 0 for each), never retyped or edited; `tests.diff`
likewise. The eight resulting product/test files' C4 contents were
confirmed `MATCH` against the reviewer's simulated reading in G3 above.
`mutations.py` was copied into `.agent/authored/` (G1, matched) and run
unedited from its payload location in G5; it was never applied to a
tracked file, per the block's instruction that it is a TOOL only.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1a, C1b, C1c,
C1d, C1e, C2, C3, C4, then this handback as C5), all gates G1–G5 ran
before C5 as ordered, and no payload was edited, retyped or repaired.
The round's tracked path set matches constraint 3 exactly: `git diff
--name-only fd976586 HEAD` (measured just before writing this handback,
i.e. through C4) names the seven `.agent/authored/f019-r3-*` copies,
`.agent/live_review.md`, `.agent/decisions.md`,
`.agent/operator_questions.md`, `.agent/plan.md`, and the eight files the
renderer/product/test diffs name — this handoff's own path is added by
C5 itself. No full-suite run was made (amend0917 rule 1; F019's belongs
to its closure). No `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `README.md`, `docs/roadmap/STATUS.md` or
`docs/roadmap/features/T5_F019.md` was touched, matching this round's
scope.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 224 insertions, matches (187 block + 37 plan.md) |
| C1b | done | 358 insertions, matches |
| C1c | done | 467 insertions, matches |
| C1d | done | 350 insertions, matches |
| C1e | done | 331 insertions, matches |
| C2 | done | git apply --check and apply both exit 0; 55/2/25/10 insertions, matches every file |
| C3 | done | 261/132/40/16/1/4 insertions, matches; both diffs applied clean; brainView.ts tracked before commit |
| C4 | done | 223/115 insertions, matches; tests.diff applied clean; both new files tracked before commit |
| C5 | done | this handback, rewritten per docs/agents/handback_template.md |
| G1 | done | all 6 payload digests and 7 authored-copy comparisons matched |
| G2 | done | decisions.md/live_review.md/operator_questions.md/plan.md byte counts and sha256 matched; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | all 8 product/test file digests matched at C4 |
| G4 | done | 1417 passed, 5 skipped (all pre-existing quarantine, none toolchain), exit 0; ruff clean; integrity check all 6 pass, fail_count 0 |
| G5 | done | all 14 mutations caught, both vitest and pytest controls green, all restores byte-identical, final line True; worktree removed and pruned |
| G6 | pending | reported in the reply, measured after this handback and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 3.
Then the rest of T002 as DECISION F019 D3 (7) names it: the old
decorative dashboard builder replaced with its source pins, and the demo
recording. Open findings: 4. Operator questions open: 3.
