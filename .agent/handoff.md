# Handback — F019 Live node materialization · Round 4 (book round 3 + finish T002)

## Session

SESSION 2 of feature F019 · round 4 · rounds so far 4

This round books round 3's PASS, records DECISION F019 D4, removes the old
decorative `buildForceBrainModel()` builder with its six source-pin types
(`ForceBrainNode`, `ForceBrainLink`, `ForceBrainGraphData`, `BrainSourceKind`,
`BrainNodeKind`, `BrainNodeState`), and adds the demo recording
`brainDemoRecording.ts` (a captured fake-provider job) with its hand-derived
golden test `brainDemoRecording.test.ts`, plus red proofs. I had ample
context remaining throughout this round; no session-limit pressure at any
point.

## Range

Review of 4b513511..HEAD

## Commits

### 2975cf430 F019 R4 C1a: copy round 4 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r4-block.md | +185/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r4-plan.md | +34/-0 | copy of the plan.md payload |

219 insertions by `git show --numstat` (block's 185 lines + 34); matches
the block's expectation exactly; under the 500-insertion cap.

### 859c44261 F019 R4 C1b: copy round 4 records and product diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r4-product.diff | +319/-0 | copy of the product.diff payload |
| .agent/authored/f019-r4-records.diff | +63/-0 | copy of the records.diff payload |

382 insertions by `git show --numstat`; matches the block's expectation
(382) exactly.

### 6c974124e F019 R4 C1c: copy round 4 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r4-tests.diff | +254/-0 | copy of the tests.diff payload |

254 insertions by `git show --numstat`; matches the block's expectation
exactly.

### c2dcb8900 F019 R4 C1d: copy round 4 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r4-mutations.py | +307/-0 | copy of the mutations.py payload |

307 insertions by `git show --numstat`; matches the block's expectation
exactly.

### 1fecf4293 F019 R4 C2: book round 3's PASS, record DECISION F019 D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +45/-0 | DECISION F019 D4 appended |
| .agent/live_review.md | +2/-0 | `Gate: F019 R3 —` entry appended |
| .agent/plan.md | +8/-11 | rewritten to the plan.md payload (round 4 scope) |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0.
Insertions/deletions by `git show --numstat`: 45/0 decisions.md, 2/0
live_review.md, 8/11 plan.md — matches the block's expectation exactly on
every file.

### d9872e697 F019 R4 C3: remove the decorative dashboard builder, add the demo recording
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/buildForceBrainModel.ts | +8/-143 | decorative `buildForceBrainModel()` removed |
| apps/ui/src/components/graph/forceBrainTypes.ts | +9/-51 | the six decorative source-pin types removed |
| apps/ui/src/components/graph/brainDemoRecording.ts | +72/-0 | new file, the captured fake-provider demo recording |

8/143, 9/51, 72/0 insertions/deletions by `git show --numstat`; matches
the block's expectation exactly on every file. `git apply --check` then
`git apply` on product.diff: exit 0 both. `brainDemoRecording.ts` was
`git add`ed before commit (no untracked product file at commit time).

### e96fc8e87 F019 R4 C4: pin the recording's golden and the graph's truth contract
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/components/graph/brainDemoRecording.test.ts | +116/-0 | new file, hand-derived golden for the recording |
| apps/ui/src/components/graph/buildForceBrainModel.test.ts | +1/-45 | trimmed to match the removed builder |
| tests/ui_server/test_dashboard_contract.py | +10/-31 | truth-contract updated for the removed types |
| tests/ui_contracts/test_graph_architecture.py | +1/-1 | source-pin assertion re-pointed at `buildBrainLayout` |

116/0, 1/45, 10/31, 1/1 insertions/deletions by `git show --numstat`;
matches the block's expectation exactly on every file. `git apply --check`
then `git apply` on tests.diff: exit 0 both. `brainDemoRecording.test.ts`
was `git add`ed before commit.

### (this commit) F019 R4 C5: rewrite handoff for round 4
This file, rewritten, its own commit — self-reference exception per the
handback template (a handback cannot table the commit that writes it).

## External actions

- `git worktree add --detach .remedy-wt/f019-r4-mut e96fc8e87` (G5) — real
  outcome: `Preparing worktree (detached HEAD e96fc8e87)`, `HEAD is now at
  e96fc8e87`.
- `git worktree remove --force .remedy-wt/f019-r4-mut` (G5, after the
  mutation sweep) — real outcome: exit 0, no output.
- `git worktree prune` (G5) — real outcome: exit 0, no output.
- `git push origin feature/f019-live-node-materialization` runs after
  this handback is committed; its real outcome is reported in the reply
  only, per G6.
- No `gh pr` command of any kind this round. No checkout of `main`, no
  branch deletion, no force-push, no `git stash`.

## Verification

G1 TRANSPORT — all 5 payloads measured against the block's PAYLOADS table,
all matched (line count, byte count, sha256):
```
records.diff    lines=63  bytes=10710 sha256=0a309187242068ace3d01a9498dfc6d44b2e186cca600b705335c818d05f30ce
plan.md         lines=34  bytes=1319  sha256=00a4280d10c26e8b39bb1e3749af15c345b2499798f9f99174c07fbf96648132
product.diff    lines=319 bytes=14553 sha256=a8eb07d3e66f84add33e3a8519e9a382bc0b6ae503b2a9f377e17aefcbea7fed
tests.diff      lines=254 bytes=12612 sha256=1d45048824625bed1d2baa9cd64560dbeb619e4d329e53c706547da964456a60
mutations.py    lines=307 bytes=12712 sha256=d3a2bbff5a7628f3baa5dd47dcdd05cc991f338346c9acb6eb85b1c9eedc6be6
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r4-*` copy, read back with `git show
<commit>:<path>` from the commit that added it, matched its source byte
for byte (6 comparisons: the block copy against
`.remedy-wt/f019-r4/block.md`, plus the 5 payload copies) — `ALL_TRANSPORT_OK: True`.

G2 THE BOOKING — at C2 (`1fecf4293`), `.agent/decisions.md` read 2008978
bytes, sha256 `5b3ef727c084fdde10ea377df14d38ee8cf8b43ea16b94af4dc6147ebcf00b22`
(MATCH); `.agent/live_review.md` read 313478 bytes, sha256
`7cd05b719fd2f803a3f8b4faf40803892c11b8194c855af3ccafe266c1ada853` (MATCH);
`.agent/plan.md` at C2 read 1319 bytes, sha256
`00a4280d10c26e8b39bb1e3749af15c345b2499798f9f99174c07fbf96648132` (MATCH,
equal to the plan.md payload). The count of lines C2 adds to the ledger
beginning `Gate: F019 R3 — ` is 1 (measured: `grep -c` over C2's
`.agent/live_review.md`). `open_finding_ids` (`scripts/rotate_live_review.py`)
over `.agent/live_review.md`: at `4b513511` → `['R-0499', 'R-0950',
'R-1008', 'R-1046']`; at C2 (`1fecf4293`) → the same four — matches the
reviewer's reading exactly at both.

G3 THE PRODUCT AND TESTS — at C4 (`e96fc8e87`), the byte count and sha256
of all 7 named files, read with `git show e96fc8e87:<path>`, matched the
reviewer's simulated reading exactly:
```
buildForceBrainModel.ts          8068 bytes  MATCH
forceBrainTypes.ts                1469 bytes  MATCH
brainDemoRecording.ts             4021 bytes  MATCH
buildForceBrainModel.test.ts      9929 bytes  MATCH
brainDemoRecording.test.ts        5938 bytes  MATCH
test_dashboard_contract.py       28533 bytes  MATCH
test_graph_architecture.py       36438 bytes  MATCH
```

G4 THE TESTS AND THE REMOVAL — real transcript, primary checkout, at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md deleted deliberately
1414 passed, 5 skipped in 71.77s (0:01:11)
REAL_EXIT=0
```
All 5 SKIPPED lines are pre-existing D3/D12 quarantine skips, unrelated to
the toolchain. The two eslint nodes of `test_ui_lint.py`, the tsc node of
`test_dashboard_contract.py`, and the vitest node of `test_test_runner.py`
do not appear in the skip list — each ran and PASSED, as the block
requires for the primary checkout. (The reviewer's sim-tree run, without
the golden path, read `1367 passed, 10 skipped`; the primary-checkout
difference — 47 more passed, 5 fewer skipped — is the golden-path suite
plus those toolchain nodes running here instead of skipping.)
```
$ python3 -m ruff check tests/ui_server/test_dashboard_contract.py tests/ui_contracts/test_graph_architecture.py
All checks passed!
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.
```
$ git grep -n -E "buildForceBrainModel\(|ForceBrainNode|ForceBrainLink|ForceBrainGraphData|BrainSourceKind|BrainNodeKind|BrainNodeState" -- apps packages tests scripts docs
GREP_EXIT=1
```
No matches — the six decorative types and the decorative call are fully
removed, as required.

G5 THE RED PROOFS — worktree `.remedy-wt/f019-r4-mut` added detached at
C4 (`e96fc8e87`), then `python3 -B .remedy-wt/f019-r4-payloads/mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f019-r4-mut`:
```
VITEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=89
PYTEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=11
D1  REVIEW_OUTCOME_STATE_TABLE maps needs_repair to pass: exit=1 failed=8 restored byte-identical: True
D2  one frame (seq 5) dropped from BRAIN_DEMO_FRAMES: exit=1 failed=2 restored byte-identical: True
D3  task A's nodeId set to empty string: exit=1 failed=1 restored byte-identical: True
D4  brainDemoRows hand-builds rows and drops outcome instead of using feedRowOf: exit=1 failed=2 restored byte-identical: True
P1  re-add sourceKind? to interface BrainLayoutNode: exit=1 failed=1 restored byte-identical: True
P2  a comment naming "layout_only" added to buildForceBrainModel.ts: exit=1 failed=1 restored byte-identical: True
P3  buildBrainLayout renamed to buildBrainLayoutX in its declaration line only: exit=1 failed=1 restored byte-identical: True
VITEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=89
PYTEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=11
vitest control #1 green: True
vitest control #2 green: True
pytest control #1 green: True
pytest control #2 green: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every one of the 7 mutation failed-counts matches the reviewer's
prototype-tree reading exactly (D1=8, D2=2, D3=1, D4=2, P1=1, P2=1, P3=1),
both vitest controls read `89 passed` at exit 0, both pytest controls read
`11 passed` at exit 0, every restore read byte-identical True, and the
final line reads `ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True`. `git
worktree remove --force .remedy-wt/f019-r4-mut` and `git worktree prune`
both exit 0; `git worktree list` afterward shows no `f019-r4-mut` entry,
only the primary checkout, the pre-existing `f015-r*` worktrees,
`f019-r2-sim`, `f019-r3-proto`, `f019-r3-sim`, `f019-r4-proto`,
`f019-r4-sim` and the four `job-*` worktrees — all named by the block's
constraint 6, nothing else.

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f019-r4-*` (the block copy
plus the 5 payload copies) were built by reading each source's bytes with
`shutil.copyfile` and writing them unedited — never retyped, never
edited. Each was read back from the commit that added it with `git show
<commit>:<path>` and compared byte for byte against its source: all 6
`BYTE-IDENTICAL` (G1 above). `records.diff` was applied with `git apply`
after `git apply --check` passed (exit 0 both), never retyped or edited;
its resulting file contents (`.agent/decisions.md`, `.agent/live_review.md`)
were verified by byte count and sha256 against the reviewer's own
readings at C2 (G2 above) — both `MATCH`; `.agent/plan.md` was separately
rewritten whole via `shutil.copyfile` from its payload and also confirmed
`MATCH`. `product.diff` was applied the same way (`git apply --check`
then `git apply`, both exit 0), never retyped or edited; `tests.diff`
likewise. The seven resulting product/test files' C4 contents were
confirmed `MATCH` against the reviewer's simulated reading in G3 above.
`mutations.py` was copied into `.agent/authored/` (G1, matched) and run
unedited from its payload location in G5; it was never applied to a
tracked file, per the block's instruction that it is a TOOL only.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1a, C1b, C1c,
C1d, C2, C3, C4, then this handback as C5), all gates G1–G5 ran before C5
as ordered, and no payload was edited, retyped or repaired. The round's
tracked path set matches constraint 3: `git diff --name-only 4b513511 HEAD`
(measured just before writing this handback, i.e. through C4) names the
six `.agent/authored/f019-r4-*` copies, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/plan.md`, and the seven files the
product/test diffs name — this handoff's own path is added by C5 itself.
No full-suite run was made (amend0917 rule 1; F019's belongs to its
closure). No `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
`docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F019.md` was
touched, matching this round's scope.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 219 insertions, matches (185 block + 34 plan.md) |
| C1b | done | 382 insertions, matches |
| C1c | done | 254 insertions, matches |
| C1d | done | 307 insertions, matches |
| C2 | done | git apply --check and apply both exit 0; 45/2/8-11 insertions/deletions, matches every file |
| C3 | done | 8/143, 9/51, 72/0 insertions/deletions, matches; diff applied clean; brainDemoRecording.ts tracked before commit |
| C4 | done | 116/0, 1/45, 10/31, 1/1 insertions/deletions, matches; tests.diff applied clean; brainDemoRecording.test.ts tracked before commit |
| C5 | done | this handback, rewritten per docs/agents/handback_template.md |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | decisions.md/live_review.md/plan.md byte counts and sha256 matched; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | all 7 product/test file digests matched at C4 |
| G4 | done | 1414 passed, 5 skipped (all pre-existing quarantine, none toolchain), exit 0; ruff clean; integrity check all 6 pass, fail_count 0; removal grep GREP_EXIT=1, no matches |
| G5 | done | all 7 mutations caught, both vitest and pytest controls green, all restores byte-identical, final line True; worktree removed and pruned |
| G6 | pending | reported in the reply, measured after this handback and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 4.
Then T003: the live wiring from the stream hook through the reducer to
the renderer, gap and snapshot recovery by paging `events-since`, the
performance fixture, and the end-to-end run on a live fake job compared
against the demo recording. Open findings: 4. Operator questions open: 3.
