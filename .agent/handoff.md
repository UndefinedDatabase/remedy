# Handback — F019 Live node materialization · Round 1 (claim + T001: the brain graph's pure reducer)

## Session

SESSION 1 of feature F019 · round 1 · rounds so far 1

This round claims F019, re-heads `.agent/live_review.md` at the F019 claim,
books F015's round 10 gate entry and resolves R-1047's `Done:` line,
records DECISION F019 D1 and operator question Q2, and lands T001: the
pure reducer from the stream's event frames to the brain graph's nodes and
links — `brainOntology.ts` and `brainReducer.ts` under
`apps/ui/src/components/graph/`, idempotent per seq, with the snapshot
rebuild, the derived core state and the cluster view — plus its fixtures
and vitest tests. I had ample context remaining throughout this round; no
session-limit pressure at any point.

## Range

Review of 92b7f5f18..HEAD

## Commits

### d9f7aa494 F019 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r1-block.md | +236/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r1-context.md | +40/-0 | copy of the context.md payload |
| .agent/authored/f019-r1-plan.md | +36/-0 | copy of the plan.md payload |

Total 312 insertions by `git show --numstat` (block's 236 lines + 76);
matches the block's expectation exactly; under the 500-insertion cap.

### ddbe0ed1f F019 R1 C1b: copy round 1 claim diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r1-claim.diff | +195/-0 | copy of the claim.diff payload |

195 insertions by `git show --numstat`; matches the block's expectation exactly.

### 5b1f6ee25 F019 R1 C1c: copy round 1 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r1-mutations.py | +364/-0 | copy of the mutations.py payload |

364 insertions by `git show --numstat`; matches the block's expectation exactly.

### 11ee0a855 F019 R1 C1d: copy round 1 product modules into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r1-brainOntology.ts | +109/-0 | copy of the brainOntology.ts payload |
| .agent/authored/f019-r1-brainReducer.ts | +363/-0 | copy of the brainReducer.ts payload |

472 insertions by `git show --numstat`; matches the block's expectation exactly.

### aa94c5c16 F019 R1 C1e: copy round 1 test payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r1-brainReducer.fixtures.ts | +227/-0 | copy of the brainReducer.fixtures.ts payload |
| .agent/authored/f019-r1-brainReducer.test.ts | +246/-0 | copy of the brainReducer.test.ts payload |

473 insertions by `git show --numstat`; matches the block's expectation exactly.

### 48e721ae5 F019 R1 C2: claim F019, re-head the live review record, book F015 R10, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +23/-23 | rewritten to the context.md payload (F019 scope) |
| .agent/decisions.md | +62/-0 | DECISION F019 D1 appended |
| .agent/live_review.md | +32/-31 | re-headed at the F019 claim; F015 R10 gate entry and R-1047's `Done:` line appended |
| .agent/operator_questions.md | +26/-0 | entry Q2 appended |
| .agent/plan.md | +23/-20 | rewritten to the plan.md payload (F019 scope) |
| docs/roadmap/STATUS.md | +1/-1 | F019's line `[ ]` to `[~]` |

`git apply --check` on claim.diff: exit 0. `git apply`: exit 0. Insertions
by `git show --numstat`: 23 context.md, 62 decisions.md, 32 live_review.md,
26 operator_questions.md, 23 plan.md, 1 STATUS.md — matches the block's
expectation exactly on every file.

### 32c02b055 F019 R1 C3: reduce stream frames into the brain graph's nodes and links
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainOntology.ts | +109/-0 | new file, copy of the brainOntology.ts payload |
| apps/ui/src/components/graph/brainReducer.ts | +363/-0 | new file, copy of the brainReducer.ts payload |

109 and 363 insertions by `git show --numstat`; matches the block's
expectation exactly. Both files were `git add`ed before commit (no
untracked product file at commit time).

### 4481f8445 F019 R1 C4: pin the reducer with goldens, replays, gaps and the cluster view
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainReducer.fixtures.ts | +227/-0 | new file, copy of the brainReducer.fixtures.ts payload |
| apps/ui/src/components/graph/brainReducer.test.ts | +246/-0 | new file, copy of the brainReducer.test.ts payload |

227 and 246 insertions by `git show --numstat`; matches the block's
expectation exactly. Both files were `git add`ed before commit.

### (this commit) F019 R1 C5: rewrite handoff for round 1
This file, rewritten, its own commit — self-reference exception per the
handback template (a handback cannot table the commit that writes it).

## External actions

- `git checkout -b feature/f019-live-node-materialization` (preflight) —
  real outcome: `Switched to a new branch 'feature/f019-live-node-materialization'`.
- `git worktree add --detach .remedy-wt/f019-r1-mut 4481f8445` (G5) — real
  outcome: `Preparing worktree (detached HEAD 4481f8445)`, `HEAD is now at
  4481f8445`.
- `git worktree remove --force .remedy-wt/f019-r1-mut` (G5, after the
  mutation sweep) — real outcome: exit 0, no output.
- `git worktree prune` (G5) — real outcome: exit 0, no output.
- `git push -u origin feature/f019-live-node-materialization` runs after
  this handback is committed; its real outcome is reported in the reply
  only, per G6.
- No `gh pr` command of any kind this round except the final G6 read (empty
  open-PR check). No checkout of `main`, no branch deletion, no
  force-push, no `git stash`.

## Verification

G1 TRANSPORT — all 8 payloads measured against the block's PAYLOADS table,
all matched (line count, byte count, sha256):
```
claim.diff                lines=195 bytes=23811  sha256=04a5e0c6ee5dd785bfa950c27ff8f61fa6e99c37ca9cc2aa4cefd706d4cb7aa5
plan.md                   lines=36  bytes=1532   sha256=eb06fb3096482ca29d35127900f1662692f79afb361c201b57b14ff53406e17c
context.md                lines=40  bytes=1825   sha256=4abc1dc732f7c3fd1f7b36cdab232f3755988f4c48c121009c5ed91fc109e1a0
mutations.py               lines=364 bytes=15075  sha256=325446c5c4cb51eb0db915c48108488f606a7e874cd451275c0b2fe040c64bbd
brainOntology.ts           lines=109 bytes=4317   sha256=fb1997c381f6095b55f2e079a730ab7faf61a38204c92d9eadf8b8e5ba70fb4f
brainReducer.ts            lines=363 bytes=16360  sha256=f2a3baa40c33c7c0ca4fe76b490334aaa28c070a5ca949c52596af5a7e6c8ad1
brainReducer.fixtures.ts   lines=227 bytes=12383  sha256=b1afe24bc6ac29029f3bb0f7178f7020f1f35c04492174f42d93bbe0ef13fd3c
brainReducer.test.ts       lines=246 bytes=11137  sha256=276f3d385b689586e526cb4d09dc70ae9e8b6359306870e72b3ef6a3e8e0cc2e
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r1-*` copy, read back with `git show
<commit>:<path>` from the commit that added it, matched its source byte
for byte (9 comparisons: the block copy against
`.remedy-wt/f019-r1/block.md`, plus the 8 payload copies) — `ALL MATCH`.

G2 THE CLAIM — at C2 (`48e721ae5`), the sha256 of all six named files,
read with `git show 48e721ae5:<path>`, matched the reviewer's reading
exactly (live_review.md, STATUS.md, decisions.md, operator_questions.md,
plan.md, context.md — all `MATCH`). `open_finding_ids`
(`scripts/rotate_live_review.py`) over `.agent/live_review.md`:
at `92b7f5f18` → `['R-0499', 'R-0950', 'R-1008', 'R-1046', 'R-1047']` (5);
at C2 (`48e721ae5`) → `['R-0499', 'R-0950', 'R-1008', 'R-1046']` (4, less
R-1047) — matches exactly. `docs/roadmap/STATUS.md`'s F019 line at C2
reads `- [~] F019 — Live node materialization`, verbatim as ordered.
`git diff --name-only aa94c5c16 48e721ae5` lists exactly the six paths of
G2's table: `.agent/context.md`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/operator_questions.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md`.

G3 THE PRODUCT — at C4 (`4481f8445`), the sha256 of all four `.ts` files
under `apps/ui/src/components/graph/`, read with `git show
4481f8445:<path>`, matched their payload sha256 exactly — all 4 `MATCH`.
`git diff --name-only 48e721ae5 32c02b055` lists exactly
`apps/ui/src/components/graph/brainOntology.ts` and `brainReducer.ts`;
`git diff --name-only 32c02b055 4481f8445` lists exactly
`brainReducer.fixtures.ts` and `brainReducer.test.ts`.

G4 THE TESTS — real transcript, primary checkout, at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md deleted deliberately
1393 passed, 5 skipped in 73.32s (0:01:13)
REAL_EXIT=0
```
All 5 SKIPPED lines are pre-existing D3/D12 quarantine skips, unrelated to
the toolchain. None of the four toolchain nodes the block named (the two
eslint checks in `test_ui_lint.py`, the `tsc --noEmit` node in
`test_dashboard_contract.py`, the vitest node in `test_test_runner.py`)
appear in the skip list — each ran and PASSED, as the block requires for
the primary checkout.
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — worktree `.remedy-wt/f019-r1-mut` added detached at
C4 (`4481f8445`), then `python3 -B .remedy-wt/f019-r1-payloads/mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f019-r1-mut`:
```
CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=36
m1  idempotence guard removed: exit=1 failed=9  restored byte-identical: True
m2  task_run_started no longer closes previous open run: exit=1 failed=1  restored byte-identical: True
m3  needs_repair mapped to pass: exit=1 failed=6  restored byte-identical: True
m4  rebuildBrainModel does not sort rows: exit=1 failed=2  restored byte-identical: True
m5  rebuildBrainModel keeps last of a repeated seq instead of first: exit=1 failed=1  restored byte-identical: True
m6  core state stored, not derived (always 'planned'): exit=1 failed=17 restored byte-identical: True
m7  cluster keeps an extra run (threshold off by one): exit=1 failed=1  restored byte-identical: True
m8  unknown kinds not counted in ignored: exit=1 failed=3  restored byte-identical: True
m9  builder_started counted in ignored: exit=1 failed=3  restored byte-identical: True
m10 unseeded task not born: exit=1 failed=4  restored byte-identical: True
m11 job_stopped leaves runs in_progress: exit=1 failed=1  restored byte-identical: True
m12 applied_to_job_workspace mapped to planned: exit=1 failed=1  restored byte-identical: True
m13 run id from a per-task counter, not birth seq: exit=1 failed=6  restored byte-identical: True
CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=36
control #1 green: True
control #2 green: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every one of the 13 mutation counts and exit codes matches the reviewer's
sim-tree reading exactly (m1=9, m2=1, m3=6, m4=2, m5=1, m6=17, m7=1, m8=3,
m9=3, m10=4, m11=1, m12=1, m13=6), both control runs read `36 passed` at
exit 0, every restore read byte-identical True, and the final line reads
`ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. `git worktree remove
--force .remedy-wt/f019-r1-mut` and `git worktree prune` both exit 0;
`git worktree list` afterward shows no `f019-r1-mut` entry, only the
primary checkout, the pre-existing `f015-r*` worktrees, `f019-r1-proto`,
`f019-r1-sim` and the four `job-*` worktrees — all named by the block's
constraint 6, nothing else.

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 9 authored copies under `.agent/authored/f019-r1-*` (the block copy
plus the 8 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from the commit that added it with `git show
<commit>:<path>` and compared byte for byte (sha256 and byte count) against
its source: all 9 `MATCH` (G1 above). `claim.diff` was applied with `git
apply` after `git apply --check` passed (exit 0 both), never retyped or
edited; its resulting file contents (live_review.md, STATUS.md,
decisions.md, operator_questions.md) were verified by sha256 against the
reviewer's own readings at C2 (G2 above) — all 6 files `MATCH`, including
`plan.md` and `context.md`, which were separately rewritten whole via
`shutil.copyfile` from their payloads and also confirmed `MATCH`. The four
`.ts` product/test files were copied whole via `shutil.copyfile` into
`apps/ui/src/components/graph/`, never retyped or edited, and their C4
contents were confirmed `MATCH` against payload sha256 in G3 above.
`mutations.py` was copied into `.agent/authored/` (G1, matched) and run
unedited from its payload location in G5; it was never applied to a
tracked file, per the block's instruction that it is a TOOL only.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1a, C1b, C1c,
C1d, C1e, C2, C3, C4, then this handback as C5), all gates G1–G5 ran
before C5 as ordered, and no payload was edited, retyped or repaired. The
round's tracked path set matches constraint 3 exactly: `git diff
--name-only 92b7f5f18 HEAD` (measured just before writing this handback,
i.e. through C4) names the nine `.agent/authored/f019-r1-*` copies,
`.agent/live_review.md`, `docs/roadmap/STATUS.md`, `.agent/decisions.md`,
`.agent/operator_questions.md`, `.agent/plan.md`, `.agent/context.md`, and
the four `.ts` files under `apps/ui/src/components/graph/` — this
handoff's own path is added by C5 itself. No full-suite run was made
(amend0917 rule 1; F019's belongs to its closure). No `.agent/prose_slips.md`,
`.agent/candidates.md`, `README.md` or
`docs/roadmap/features/T5_F019.md` was touched.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 312 insertions, matches (236 block + 40 context.md + 36 plan.md) |
| C1b | done | 195 insertions, matches |
| C1c | done | 364 insertions, matches |
| C1d | done | 472 insertions, matches |
| C1e | done | 473 insertions, matches |
| C2 | done | git apply --check and apply both exit 0; 23/62/32/26/23/1 insertions, matches every file |
| C3 | done | 109/363 insertions, matches; both files tracked before commit |
| C4 | done | 227/246 insertions, matches; both files tracked before commit |
| C5 | done | this handback, rewritten per docs/agents/handback_template.md |
| G1 | done | all 8 payload digests and 9 authored-copy comparisons matched |
| G2 | done | all 6 file digests matched; open_finding_ids correct at both commits; STATUS line verbatim; name-only diff exact |
| G3 | done | all 4 product/test file digests matched at C4; name-only diffs exact for C2→C3 and C3→C4 |
| G4 | done | 1393 passed, 5 skipped (all pre-existing quarantine, none toolchain), exit 0; integrity check all 6 pass, fail_count 0 |
| G5 | done | all 13 mutations caught, both controls green, all restores byte-identical, final line True; worktree removed and pruned |
| G6 | pending | reported in the reply, measured after this handback and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1.
Then T002 — rendering the reducer's model on react-force-graph-2d by
extending `buildForceBrainModel.ts`, the layout, the glyph slots, the
motion tokens and the demo recording. Open findings: 4. Operator questions
open: 2.
