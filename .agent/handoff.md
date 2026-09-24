# Handback — F019 Live node materialization · Round 5 (book round 4 + T003 first half: the ledger)

## Session

SESSION 2 of feature F019 · round 5 · rounds so far 5

This round books round 4's PASS, records DECISION F019 D5, and lands
T003's first half: the new pure module `brainLedger.ts` (merges
`events-since` pages and the live ring into one ledger, one row per seq,
folds only the contiguous prefix from seq 0, fills a hole by paging from
its first missing seq), its thin hook `useBrainLedger.ts`, the exported
path builder `eventsSincePath` in `brainStreamDeps.ts`, the shell handing
the stage the live ring and a page reader, and the stage rebuilding its
model from the ledger's prefix via `rebuildBrainModel` — with vitest
tests, a source guard and red proofs. I had ample context remaining
throughout this round; no session-limit pressure at any point.

## Range

Review of 238f2aa5..HEAD

## Commits

### c191e2de1 F019 R5 C1a: copy round 5 block and plan into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r5-block.md | +184/-0 | copy of this round's block, verbatim |
| .agent/authored/f019-r5-plan.md | +34/-0 | copy of the plan.md payload |

218 insertions by `git show --numstat` (block's 184 lines + 34); matches
the block's expectation exactly; under the 500-insertion cap.

### 3f3ff9a6d F019 R5 C1b: copy round 5 records and product diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r5-product.diff | +375/-0 | copy of the product.diff payload |
| .agent/authored/f019-r5-records.diff | +57/-0 | copy of the records.diff payload |

432 insertions by `git show --numstat`; matches the block's expectation
(432) exactly.

### 06b25ea37 F019 R5 C1c: copy round 5 tests diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r5-tests.diff | +365/-0 | copy of the tests.diff payload |

365 insertions by `git show --numstat`; matches the block's expectation
exactly.

### d16b99358 F019 R5 C1d: copy round 5 mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f019-r5-mutations.py | +351/-0 | copy of the mutations.py payload |

351 insertions by `git show --numstat`; matches the block's expectation
exactly.

### 2f6d68081 F019 R5 C2: book round 4's PASS, record DECISION F019 D5
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +39/-0 | DECISION F019 D5 appended |
| .agent/live_review.md | +2/-0 | `Gate: F019 R4 —` entry appended |
| .agent/plan.md | +10/-10 | rewritten to the plan.md payload (round 5 scope) |

`git apply --check` on records.diff: exit 0. `git apply`: exit 0.
Insertions/deletions by `git show --numstat`: 39/0 decisions.md, 2/0
live_review.md, 10/10 plan.md — matches the block's expectation exactly
on every file.

### 50790f63f F019 R5 C3: fold the ledger's complete prefix into the live graph
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStreamDeps.ts | +9/-1 | exports `eventsSincePath`, reuses it in the stream's own `since` closure |
| apps/ui/src/components/graph/BrainGraphStage.tsx | +25/-4 | rebuilds from the ledger's prefix via `rebuildBrainModel` instead of seeding once |
| apps/ui/src/components/graph/brainLedger.ts | +165/-0 | new file, the merged ledger and prefix/hole logic |
| apps/ui/src/components/graph/useBrainLedger.ts | +72/-0 | new file, the thin hook holding ledger state and the in-flight guard |
| apps/ui/src/components/shell/RemedyShell.tsx | +12/-3 | hands the stage the live ring and a page reader built on `eventsSincePath` |

9/1, 25/4, 165/0, 72/0, 12/3 insertions/deletions by `git show --numstat`;
matches the block's expectation exactly on every file. `git apply --check`
then `git apply` on product.diff: exit 0 both. `brainLedger.ts` and
`useBrainLedger.ts` were `git add`ed before commit (no untracked product
file at commit time).

### f21e7a10c F019 R5 C4: pin the ledger, the gap fill and the live wiring
| Path | +/- | Reason |
|---|---|---|
| apps/ui/src/api/brainStreamDeps.test.ts | +7/-1 | pins `eventsSincePath` |
| apps/ui/src/components/graph/brainLedger.test.ts | +196/-0 | new file, pins the merge, prefix and hole-fill logic |
| tests/ui_contracts/test_brain_live_wiring.py | +114/-0 | new file, pins the stage/shell/hook wiring |
| tests/ui_contracts/test_brain_stage_mount.py | +5/-2 | re-pointed at `rebuildBrainModel(` |

7/1, 196/0, 114/0, 5/2 insertions/deletions by `git show --numstat`;
matches the block's expectation exactly on every file. `git apply --check`
then `git apply` on tests.diff: exit 0 both. `brainLedger.test.ts` and
`test_brain_live_wiring.py` were `git add`ed before commit.

### (this commit) F019 R5 C5: rewrite handoff for round 5
This file, rewritten, its own commit — self-reference exception per the
handback template (a handback cannot table the commit that writes it).

## External actions

- `git worktree add --detach .remedy-wt/f019-r5-mut f21e7a10c` (G5) — real
  outcome: `Preparing worktree (detached HEAD f21e7a10c)`, `HEAD is now at
  f21e7a10c`.
- `git worktree remove --force .remedy-wt/f019-r5-mut` (G5, after the
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
records.diff    lines=57  bytes=10140 sha256=1900ffc087f94bc6e789b8f380ce0eaf4c1141fa030f406e7de5bf2bc802ae09
plan.md         lines=34  bytes=1362  sha256=bc1babf1c5bca2ddf7bf73bf9c24906da2dafbf3d63148c3e41ecac179377e77
product.diff    lines=375 bytes=18748 sha256=27b555cfab0fb4b94efff4808d84e9ee7be214c61f5dfcfecfc61cea131aab8d
tests.diff      lines=365 bytes=15972 sha256=9da3e999e72390047363a72d0bcc074ecb44d35b1c5ecc4d02143ea92b675e43
mutations.py    lines=351 bytes=14009 sha256=923127841b30d778a59403d84c35bf3bc665ffbb843f2d7c4550902a4e512864
ALL PAYLOAD DIGESTS MATCH: True
```
Each `.agent/authored/f019-r5-*` copy, read back with `git show
<commit>:<path>` from the commit that added it, matched its source byte
for byte (6 comparisons: the block copy against
`.remedy-wt/f019-r5/block.md`, plus the 5 payload copies) — `ALL_TRANSPORT_OK: True`.

G2 THE BOOKING — at C2 (`2f6d68081`), `.agent/decisions.md` read 2012239
bytes, sha256 `d489e9b2c5f8f2478723cff983b3e4f13f2d764cf2483f34f9b33b5f6f1517e2`
(MATCH); `.agent/live_review.md` read 315698 bytes, sha256
`06b91d40088f7bee6702f8b62c8facac9791251a46d0cf53ca5a2eb0a3fe75be` (MATCH);
`.agent/plan.md` at C2 read 1362 bytes, sha256
`bc1babf1c5bca2ddf7bf73bf9c24906da2dafbf3d63148c3e41ecac179377e77` (MATCH,
equal to the plan.md payload). The count of lines C2 adds to the ledger
beginning `Gate: F019 R4 — ` is 1 (measured: `grep -c` over C2's
`.agent/live_review.md`). `open_finding_ids` (`scripts/rotate_live_review.py`)
over `.agent/live_review.md`: at `238f2aa5` → `['R-0499', 'R-0950',
'R-1008', 'R-1046']`; at C2 (`2f6d68081`) → the same four — matches the
reviewer's reading exactly at both.

G3 THE PRODUCT AND TESTS — at C4 (`f21e7a10c`), the byte count and sha256
of all 9 named files, read with `git show f21e7a10c:<path>`, matched the
reviewer's simulated reading exactly:
```
apps/ui/src/api/brainStreamDeps.ts                 7546 bytes  MATCH
apps/ui/src/components/graph/brainLedger.ts         7527 bytes  MATCH
apps/ui/src/components/graph/useBrainLedger.ts      2927 bytes  MATCH
apps/ui/src/components/graph/BrainGraphStage.tsx    3369 bytes  MATCH
apps/ui/src/components/shell/RemedyShell.tsx       13113 bytes  MATCH
apps/ui/src/api/brainStreamDeps.test.ts             7110 bytes  MATCH
apps/ui/src/components/graph/brainLedger.test.ts    8214 bytes  MATCH
tests/ui_contracts/test_brain_live_wiring.py        4805 bytes  MATCH
tests/ui_contracts/test_brain_stage_mount.py        4582 bytes  MATCH
```

G4 THE TESTS — real transcript, primary checkout, at C4:
```
$ python3 -m pytest -q -p no:cacheprovider -rs tests/ui_contracts tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py tests/orchestration/test_live_review_rotation.py tests/orchestration/test_integrity_gate.py tests/orchestration/test_roadmap_index.py tests/test_agent_tooling.py tests/docs tests/cli/test_golden_path.py
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:441: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_graph_architecture.py:484: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:507: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/ui_contracts/test_ux_quality.py:543: D3 quarantine (F252): pre-rebuild legacy sources not in tree
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md deleted deliberately
1427 passed, 5 skipped in 72.03s (0:01:12)
REAL_EXIT=0
```
All 5 SKIPPED lines are pre-existing D3/D12 quarantine skips, unrelated to
the toolchain. The two eslint nodes of `test_ui_lint.py`, the tsc node of
`test_dashboard_contract.py`, and the vitest node of `test_test_runner.py`
do not appear in the skip list — each ran and PASSED, as the block
requires for the primary checkout. (The reviewer's sim-tree run, without
the golden path, read `1380 passed, 10 skipped`; the primary-checkout
difference — 47 more passed, 5 fewer skipped — is the golden-path suite
plus those toolchain nodes running here instead of skipping.)
```
$ python3 -m ruff check tests/ui_contracts/test_brain_live_wiring.py tests/ui_contracts/test_brain_stage_mount.py
All checks passed!
REAL_EXIT=0
```
```
$ python3 -m apps.cli.main integrity check --json
{"check_count": 6, "checks": [{"message": "handlers=157", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
REAL_EXIT=0
```
All six checks `pass`, `fail_count` 0.

G5 THE RED PROOFS — worktree `.remedy-wt/f019-r5-mut` added detached at
C4 (`f21e7a10c`), then `python3 -B .remedy-wt/f019-r5-payloads/mutations.py
/home/decodeux/Repos/remedy/.remedy-wt/f019-r5-mut`:
```
VITEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=124
PYTEST CONTROL RUN #1 (unmutated, before any mutation): exit_code=0 failed=0 passed=32
L1  merge lets the incoming duplicate win instead of the already-held row: exit=1 failed=2 restored byte-identical: True
L2  prefix returns every held row, ignoring a hole: exit=1 failed=4 restored byte-identical: True
L3  next cursor returns null before any read instead of 0: exit=1 failed=2 restored byte-identical: True
L4  next cursor returns known instead of the first hole: exit=1 failed=7 restored byte-identical: True
L5  an unchanged read does not stall: exit=1 failed=1 restored byte-identical: True
L6  a live change does not clear the stall: exit=1 failed=1 restored byte-identical: True
L7  brainLedgerPage ignores the payload's cursor: exit=1 failed=1 restored byte-identical: True
L8  known is not raised by held rows past the declared length: exit=1 failed=5 restored byte-identical: True
W1  the stage builds from seedBrainModel again instead of rebuildBrainModel: exit=1 failed=3 restored byte-identical: True
W2  the shell's stage line loses recent=: exit=1 failed=1 restored byte-identical: True
W3  useBrainLedger.ts stops holding the in-flight cursor in a useRef: exit=1 failed=1 restored byte-identical: True
VITEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=124
PYTEST CONTROL RUN #2 (unmutated, after the full sweep): exit_code=0 failed=0 passed=32
vitest control #1 green: True
vitest control #2 green: True
pytest control #1 green: True
pytest control #2 green: True
ALL MUTATIONS CAUGHT AND RESTORED CLEANLY: True
REAL_EXIT=0
```
Every one of the 11 mutation failed-counts matches the reviewer's
prototype-tree reading exactly (L1=2, L2=4, L3=2, L4=7, L5=1, L6=1, L7=1,
L8=5, W1=3, W2=1, W3=1), both vitest controls read `124 passed` at exit 0,
both pytest controls read `32 passed` at exit 0, every restore read
byte-identical True, and the final line reads `ALL MUTATIONS CAUGHT AND
RESTORED CLEANLY: True`. `git worktree remove --force .remedy-wt/f019-r5-mut`
and `git worktree prune` both exit 0; `git worktree list` afterward shows
no `f019-r5-mut` entry, only the primary checkout, the pre-existing
`f015-r*` worktrees, `f019-r2-sim`, `f019-r3-proto`, `f019-r3-sim`,
`f019-r4-proto`, `f019-r4-sim`, `f019-r5-proto`, `f019-r5-sim` and the
four `job-*` worktrees — all named by the block's constraint 6, nothing
else.

G6 — reported in the reply per the block's own instruction (measured
after this handback is written, committed and pushed).

## Authored-text proofs

All 6 authored copies under `.agent/authored/f019-r5-*` (the block copy
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
likewise. The nine resulting product/test files' C4 contents were
confirmed `MATCH` against the reviewer's simulated reading in G3 above.
`mutations.py` was copied into `.agent/authored/` (G1, matched) and run
unedited from its payload location in G5; it was never applied to a
tracked file, per the block's instruction that it is a TOOL only.

## Deviations & assumptions

None. Every commit landed in the block's stated order (C1a, C1b, C1c,
C1d, C2, C3, C4, then this handback as C5), all gates G1–G5 ran before C5
as ordered, and no payload was edited, retyped or repaired. The round's
tracked path set matches constraint 3: `git diff --name-only 238f2aa5 HEAD`
(measured just before writing this handback, i.e. through C4) names the
six `.agent/authored/f019-r5-*` copies, `.agent/live_review.md`,
`.agent/decisions.md`, `.agent/plan.md`, and the nine files the
product/test diffs name — this handoff's own path is added by C5 itself.
No full-suite run was made (amend0917 rule 1; F019's belongs to its
closure). No `.agent/context.md`, `.agent/prose_slips.md`,
`.agent/candidates.md`, `.agent/operator_questions.md`, `README.md`,
`docs/roadmap/STATUS.md` or `docs/roadmap/features/T5_F019.md` was
touched, matching this round's scope.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 218 insertions, matches (184 block + 34 plan.md) |
| C1b | done | 432 insertions, matches |
| C1c | done | 365 insertions, matches |
| C1d | done | 351 insertions, matches |
| C2 | done | git apply --check and apply both exit 0; 39/2/10-10 insertions/deletions, matches every file |
| C3 | done | 9/1, 25/4, 165/0, 72/0, 12/3 insertions/deletions, matches; diff applied clean; brainLedger.ts and useBrainLedger.ts tracked before commit |
| C4 | done | 7/1, 196/0, 114/0, 5/2 insertions/deletions, matches; tests.diff applied clean; brainLedger.test.ts and test_brain_live_wiring.py tracked before commit |
| C5 | done | this handback, rewritten per docs/agents/handback_template.md |
| G1 | done | all 5 payload digests and 6 authored-copy comparisons matched |
| G2 | done | decisions.md/live_review.md/plan.md byte counts and sha256 matched; 1 new Gate line; open_finding_ids correct at both commits |
| G3 | done | all 9 product/test file digests matched at C4 |
| G4 | done | 1427 passed, 5 skipped (all pre-existing quarantine, none toolchain), exit 0; ruff clean; integrity check all 6 pass, fail_count 0 |
| G5 | done | all 11 mutations caught, both vitest and pytest controls green, all restores byte-identical, final line True; worktree removed and pruned |
| G6 | pending | reported in the reply, measured after this handback and the push |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 5.
Then the rest of T003 as DECISION F019 D5 (1) names it: the end-to-end run
of a live fake job compared against the demo recording, and the
performance fixture's measurement. Open findings: 4. Operator questions
open: 3.
