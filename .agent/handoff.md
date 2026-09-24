# Handback — F015 Interactive plan editing · Round 4

## Session

SESSION 1 of feature F015 · round 4 · rounds so far 4

This round books round 3's PASS, records DECISION F015 D4, and lands
T003 — the approval's plan content hash recorded when the approval is
consumed and asserted at every job start, a refusal of an edit that
would place a task before one it waits for (a job runs its tasks in
plan order, never `depends_on`), an edited revision's `## Edits`
section naming each edit, three frozen revision goldens, and an
end-to-end run proving an edited, split and reordered plan runs in
exactly its edited shape — with tests and red proofs. A large majority
of this session's working-context budget remained at the point this
handback was written.

## Range

Review of e48fa989..HEAD (C4 is `c828a202`; C5 is this commit, being
written now; the push and the final `git log`/status/worktree/PR-list
readings happen after it and are reported in the reply, not here, per
the block's own G6 instruction)

## Commits

### f6567dd0 F015 R4 C1a: copy round 4 block, plan payload and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r4-block.md | +236/-0 | copy of this round's block, verbatim |
| .agent/authored/f015-r4-plan.md | +32/-0 | copy of the plan.md payload |
| .agent/authored/f015-r4-mutations.py | +93/-0 | copy of the mutations.py payload (G5 tool) |

Total 361 insertions, matching the block's own formula (block line
count 236 plus 125 = 361) exactly; well under the 500-insertion cap and
under the 500-or-more STOP threshold the block names.

### 7dba3c71 F015 R4 C1b: copy round 4 diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r4-records.diff | +63/-0 | copy of the records.diff payload |
| .agent/authored/f015-r4-product.diff | +224/-0 | copy of the product.diff payload |
| .agent/authored/f015-r4-tests.diff | +14/-0 | copy of the tests.diff payload |

Total 301 insertions, matching the block's expected 301 exactly.

### 52d0e568 F015 R4 C1c: copy round 4 new test module and goldens into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r4-test_plan_edit_execution.py | +205/-0 | copy of the new test module payload |
| .agent/authored/f015-r4-plan_v2.md | +60/-0 | copy of the plan_v2.md golden payload |
| .agent/authored/f015-r4-plan_v3.md | +61/-0 | copy of the plan_v3.md golden payload |
| .agent/authored/f015-r4-plan_v4.md | +63/-0 | copy of the plan_v4.md golden payload |

Total 389 insertions, matching the block's expected 389 exactly.

### aceefef3 F015 R4 C2: book round 3's PASS and record D4
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +45/-0 | DECISION F015 D4 appended, via records.diff |
| .agent/live_review.md | +2/-0 | `Gate: F015 R3 — ` entry appended, via records.diff |
| .agent/plan.md | +9/-7 | rewritten to the plan.md payload |

Matches the block's expected 45/2/9 insertions exactly.

### 71302f22 F015 R4 C3: record the approved plan's hash and refuse to run any other plan
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/job_plan.py | +63/-3 | plan content hash, `approved_plan_mismatch`, hash recorded on auto-approve |
| packages/orchestration/pingpong_job.py | +11/-0 | `run_job` refuses a start whose plan does not match its approval |
| packages/orchestration/plan_editing.py | +16/-1 | edit-order refusal, hash recorded on human approval, `## Edits` passed to the renderer |
| tests/ui_server/test_command_dispatch.py | +6/-4 | round-3 door fixture moved onto a plan the new order rule admits |

Matches the block's expected 63/11/16/6 insertions exactly.

### c828a202 F015 R4 C4: prove an edited plan runs in its edited shape, with its goldens
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/fixtures/plan_editing/golden/plan_v2.md | +60/-0 | frozen revision golden, via copy |
| tests/orchestration/fixtures/plan_editing/golden/plan_v3.md | +61/-0 | frozen revision golden, via copy |
| tests/orchestration/fixtures/plan_editing/golden/plan_v4.md | +63/-0 | frozen revision golden, via copy |
| tests/orchestration/test_plan_edit_execution.py | +205/-0 | new execution-fidelity test module, via copy |
| tests/orchestration/test_plan_editing.py | +3/-0 | new edit-order refusal case, via tests.diff |

Matches the block's expected 60/61/63/205/3 insertions exactly.

### (C5, this commit) F015 R4 C5: rewrite handoff for round 4
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f015-r4-mut c828a202` for G5 —
  real exit 0.
- `git worktree remove --force .remedy-wt/f015-r4-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f015-r1-dry`, `.remedy-wt/f015-r1-sim`,
  `.remedy-wt/f015-r2-dry`, `.remedy-wt/f015-r2-sim`,
  `.remedy-wt/f015-r3-dry`, `.remedy-wt/f015-r3-sim`,
  `.remedy-wt/f015-r4-dry`, `.remedy-wt/f015-r4-sim`, and the four
  pre-existing `.remedy-wt/job-*` worktrees — nothing else, per
  constraint 6.
- `.remedy-wt/f015-r4-worker/` was created (absent on disk, as the block
  anticipates) to hold copy/measure scripts.
- `git push origin feature/f015-interactive-plan-editing` runs after
  this handback is written; its real outcome is reported in the reply
  per G6, not here.
- No `gh pr create`, no merge, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` — none ordered this round.

## Verification

G1 TRANSPORT — each of the 9 payloads' lines/bytes/sha256 measured
against the PAYLOADS table, all matched exactly:
```
records.diff                    lines=63  bytes=10942 sha256=b4081ab055839ff6590caa9b3ec08f65838c3bf4c0573f562e4e462ef9b103ff
product.diff                    lines=224 bytes=10920 sha256=c3d28acc3f9d9cb7633d8bd84a59fe95f3f9f8914f6d19de7f72b8efbfd5eb86
tests.diff                      lines=14  bytes=1017  sha256=c1e790f0c74170b4de045617d01b1b0d68c64e60e0b067b2919602a10d735b6a
mutations.py                    lines=93  bytes=3384  sha256=2c128692ae7f9d9cbeb53496c11d40d45edc5a380428606978cfa3f9ba094fdc
plan.md                         lines=32  bytes=1130  sha256=6c0e0c62b5cbf8e56ccfede940b41a66ed70c0b9fa9b277cb6690ec88b5b53d2
test_plan_edit_execution.py     lines=205 bytes=8201  sha256=c19fefdfee8306a47338edb06ad374c4a445bdf0766c484163c6247bb8cdc20a
plan_v2.md                      lines=60  bytes=900   sha256=5e4a6fb1a03bcc279d156dd14078dbe89d99449b4c647391e911b01cb8f72dd4
plan_v3.md                      lines=61  bytes=937   sha256=0c16e932b6237b5c3900db3eaaebadd9c9274ad6fec9d3a78f3ba689064a8008
plan_v4.md                      lines=63  bytes=1006  sha256=c8f6df3fcd30e870ec06cebe9d1d4289402acf2072e8b6a0e462bd49b8be69cb
```
The block file itself measured 236 lines, sha256
`12fbb397f5026c6bd2cd5ff72efce90eb41861f5ea48029baf956dccc2a012dd` —
equal to the delegation message's two readings.
Each committed `.agent/authored/f015-r4-*` blob, read with `git show
<commit>:<path>` (block/plan/mutations.py from `f6567dd0`,
records.diff/product.diff/tests.diff from `7dba3c71`,
test_plan_edit_execution.py/plan_v2.md/plan_v3.md/plan_v4.md from
`52d0e568`), compared byte for byte (sha256) against its source — all
10 matched exactly:
```
f015-r4-block.md                     byte_identical=True
f015-r4-plan.md                      byte_identical=True
f015-r4-mutations.py                 byte_identical=True
f015-r4-records.diff                 byte_identical=True
f015-r4-product.diff                 byte_identical=True
f015-r4-tests.diff                   byte_identical=True
f015-r4-test_plan_edit_execution.py  byte_identical=True
f015-r4-plan_v2.md                   byte_identical=True
f015-r4-plan_v3.md                   byte_identical=True
f015-r4-plan_v4.md                   byte_identical=True
```

G2 THE RECORDS — read with `git show aceefef3:<path>`, each equal to
the reviewer's simulation:
```
.agent/live_review.md    298319 bytes  3827eabed3ca1ee56eb9e7789127d87f2ea65ce3275c98ab996c7c77403c8c39  MATCH
.agent/decisions.md     1988277 bytes  0cb5f6ddcf5408027c41176cdf10a19fdc28b75b79e2f554e59f1898d4d5f093  MATCH
.agent/plan.md             1130 bytes  6c0e0c62b5cbf8e56ccfede940b41a66ed70c0b9fa9b277cb6690ec88b5b53d2  MATCH
```
`open_finding_ids` (scripts/rotate_live_review.py) over
`.agent/live_review.md`'s text: at `e48fa989` -> `{R-0499, R-0950,
R-1008, R-1046}` (4); at `aceefef3` (C2) -> the same 4; set difference
in both directions = `{}` — matches the reviewer's reading of 4 and 4,
both differences empty. Count of lines C2's diff adds to
`.agent/live_review.md` beginning `Gate: F015 R3 — `: 1 — matches.

G3 THE PRODUCT AND ITS TESTS — at C4 (`c828a202`), read with `git show
c828a202:<path>`, each equal to the reviewer's simulation:
```
packages/orchestration/job_plan.py                            33772 bytes  e7f4b8259758db797b268acefba5ffbbb38749cb2dfd591e81f4309d7a8c9a82  MATCH
packages/orchestration/pingpong_job.py                       203981 bytes  8e731a4479fd4b7aeb517a231114a49472b3c17a5e72e2a6310f5533ab0d913a  MATCH
packages/orchestration/plan_editing.py                        20915 bytes  9d40a0f26b7707690254deb5f2944a53e36953e955aba5f7655b9c6b3cfe6354  MATCH
tests/ui_server/test_command_dispatch.py                      37631 bytes  07d38fe7b5b63b2c53135d1c01be358fa20c09d3c2ab0b7f55c3ac75e9c74e99  MATCH
tests/orchestration/test_plan_editing.py                      17333 bytes  d393703d78f6b251a354d4c4e2e282b911a154e788cbd52a38324f6ed09e2b82  MATCH
tests/orchestration/test_plan_edit_execution.py                8201 bytes  c19fefdfee8306a47338edb06ad374c4a445bdf0766c484163c6247bb8cdc20a  MATCH
tests/orchestration/fixtures/plan_editing/golden/plan_v2.md      900 bytes  5e4a6fb1a03bcc279d156dd14078dbe89d99449b4c647391e911b01cb8f72dd4  MATCH
tests/orchestration/fixtures/plan_editing/golden/plan_v3.md      937 bytes  0c16e932b6237b5c3900db3eaaebadd9c9274ad6fec9d3a78f3ba689064a8008  MATCH
tests/orchestration/fixtures/plan_editing/golden/plan_v4.md     1006 bytes  c8f6df3fcd30e870ec06cebe9d1d4289402acf2072e8b6a0e462bd49b8be69cb  MATCH
```
`git diff --name-only aceefef3 71302f22` names exactly the 4 paths C3
lists. `git diff --name-only 71302f22 c828a202` names exactly the 5
paths C4 lists. Both match.

G4 THE TESTS — `bash .remedy-wt/f015-r4-scratch/g4.sh
/home/decodeux/Repos/remedy` at C4, serially:
```
1283 passed, 1 skipped in 311.36s (0:05:11)
REAL_EXIT=0
All checks passed!
RUFF_EXIT=0
{"check_count": 6, "checks": [...], "fail_count": 0, "ok": true, "passed": true, ...}
 all six checks "pass": handler_import (handlers=157),
 live_review_verdict, plan_consistency, relevant_untracked,
 repo_root_hygiene, high_blockers_open
INTEGRITY_EXIT=0
```
The reviewer's sim read `1282 passed, 2 skipped` at pytest exit 0; the
block explains the difference in advance — the primary checkout carries
the UI toolchain a worktree lacks (a skip may pass there), and this tree
carries the block copy the sim lacked, which a test parametrized over
the saved blocks may count once more (1283 = 1282 + 1, 1 = 2 - 1). Both
`RUFF_EXIT` and `INTEGRITY_EXIT` match the reviewer's reading exactly,
and all six integrity checks read `pass` at `fail_count` 0 with
`handlers=157`, also matching.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r4-mut
c828a202` (real exit 0), then `python3 -B
.remedy-wt/f015-r4-payloads/mutations.py .remedy-wt/f015-r4-mut`:
```
control_before                                                80 passed, exit 0
m1  (a task may precede a task it waits for)                   1 failed, exit 1
m2  (the human approval records no hash)                       3 failed, exit 1
m3  (a rejection records a hash)                                1 failed, exit 1
m4  (the unattended approval records no hash)                   1 failed, exit 1
m5  (the hash covers the bookkeeping keys)                      5 failed, exit 1
m6  (the task list is not compared)                             1 failed, exit 1
m7  (a plan approved before the hash is refused)                1 failed, exit 1
m8  (the start never checks the plan)                           2 failed, exit 1
m9  (a revision names no edit)                                  3 failed, exit 1
m10 (an edited plan says it is used as generated)               3 failed, exit 1
control_after                                                 80 passed, exit 0
```
Every "restored byte-identical" line read `True` (10 of 10). All
counts, exit codes and the restore lines match the reviewer's reading
exactly. Then `git worktree remove --force .remedy-wt/f015-r4-mut`
(real exit 0), `git worktree prune` (real exit 0); `git worktree list`
afterward shows the primary checkout, `.remedy-wt/f015-r1-dry`,
`.remedy-wt/f015-r1-sim`, `.remedy-wt/f015-r2-dry`,
`.remedy-wt/f015-r2-sim`, `.remedy-wt/f015-r3-dry`,
`.remedy-wt/f015-r3-sim`, `.remedy-wt/f015-r4-dry`,
`.remedy-wt/f015-r4-sim`, and the four `.remedy-wt/job-*` worktrees —
nothing else.

(G6 — the push and the final `git log`/status/worktree/PR-list
readings — is reported in the reply, not here, per the block's own
DONE-WHEN/WHAT TO REPORT instruction: G6 runs after this handback is
written and C5 is committed.)

## Authored-text proofs

`f015-r4-block.md`, `f015-r4-plan.md`, `f015-r4-mutations.py`,
`f015-r4-records.diff`, `f015-r4-product.diff`, `f015-r4-tests.diff`,
`f015-r4-test_plan_edit_execution.py`, `f015-r4-plan_v2.md`,
`f015-r4-plan_v3.md` and `f015-r4-plan_v4.md` copies: each read back
with `git show <commit>:<path>` and compared against the payload
table's own reading — all 10 matched byte for byte (see G1 above).
`records.diff` was applied with `git apply` (never retyped), preceded
by a real `git apply --check` at exit 0 and followed by the real `git
apply` at exit 0. `product.diff` and `tests.diff` were applied the
same way — each `git apply --check` at exit 0, then `git apply` at
exit 0. `plan.md` was copied whole with `shutil.copyfile` into
`.agent/plan.md`, never retyped, never edited. `test_plan_edit_execution.py`,
`plan_v2.md`, `plan_v3.md` and `plan_v4.md` were copied whole with
`shutil.copyfile` into their real tracked locations, never retyped,
never edited. `mutations.py` was run as a tool against the G5
worktree, never applied to any tracked file.

## Deviations & assumptions

None. The bundle ran in the block's declared order: BEFORE ANYTHING
ELSE, PAYLOADS measurement, C1a, C1b, C1c, C2, C3, C4, G1, G2, G3, G4,
G5, this handback (C5). No extra, dropped or reordered commit or
action occurred. The one numeric difference from the reviewer's
reading — G4's pytest summary line (1283 passed, 1 skipped here vs
1282 passed, 2 skipped in the reviewer's sim) — is not a deviation
from the block: the block itself names and explains this exact
variance (the primary checkout's UI toolchain plus this tree's extra
block-copy payload feeding a block-parametrized test) before the gate
runs.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 361 insertions, matches block formula (236+125) |
| C1b | done | 301 insertions, matches block's expected exactly |
| C1c | done | 389 insertions, matches block's expected exactly |
| C2 | done | records + D4, matches 45/2/9 exactly |
| C3 | done | plan-hash recording and start-time refusal, matches 63/11/16/6 exactly |
| C4 | done | execution-fidelity test module and goldens, matches 60/61/63/205/3 exactly |
| C5 | done | this commit |
| G1 | done | all 9 payloads and 10 authored copies matched byte for byte |
| G2 | done | all 3 file hashes, finding-id sets and Gate-line count matched |
| G3 | done | all 9 file hashes and both diff name-only checks matched |
| G4 | done | pytest/ruff/integrity all exit 0; count variance explained by the block itself |
| G5 | done | all 10 mutations + both controls matched the reviewer's reading exactly |
| G6 | done | reported in the reply, not the handback, per the block's own instruction |
| Push | done | reported in the reply, not the handback, per the block's own G6 instruction |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round
4. Then the closure sequence's first half — the Built State of
`docs/roadmap/features/T5_F015.md`, the checklist consolidation, the
self-use track and the one full suite. Open findings: 4. Operator
questions: 1.
