# Handback — F015 Interactive plan editing · Round 3

## Session

SESSION 1 of feature F015 · round 3 · rounds so far 3

This round books round 2's PASS, records DECISION F015 D3, and lands
T002's second half: the write door exposes the six `job.plan-*` edit
commands (`job.plan-edit-task`, `job.plan-delete-task`,
`job.plan-reorder`, `job.plan-merge-tasks`, `job.plan-split-task` and
`job.plan-edit-acceptance`), each run through `plan_editing.edit_plan`
with a required `args.expected_version`, attributed to the request's
token fingerprint, and each refusal answered with the status and reason
D3 rules, with tests and red proofs. A large majority of this session's
working-context budget remained at the point this handback was written.

## Range

Review of 1a95e306..HEAD (C4 is `09eb2f0e`; C5 is this commit, being
written now; the push and the final `git log`/status/worktree/PR-list
readings happen after it and are reported in the reply, not here, per
the block's own G6 instruction)

## Commits

### 6ca8a5b8 F015 R3 C1a: copy round 3 block, plan payload and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r3-block.md | +214/-0 | copy of this round's block, verbatim |
| .agent/authored/f015-r3-plan.md | +30/-0 | copy of the plan.md payload |
| .agent/authored/f015-r3-mutations.py | +91/-0 | copy of the mutations.py payload (G5 tool) |

Total 335 insertions, matching the block's own formula (block line
count 214 plus 121 = 335) exactly; well under the 500-insertion cap and
under the 500-or-more STOP threshold the block names.

### eee76c36 F015 R3 C1b: copy round 3 diffs into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r3-records.diff | +55/-0 | copy of the records.diff payload |
| .agent/authored/f015-r3-product.diff | +195/-0 | copy of the product.diff payload |
| .agent/authored/f015-r3-tests.diff | +178/-0 | copy of the tests.diff payload |

Total 428 insertions, matching the block's expected 428 exactly.

### 6c8e549d F015 R3 C2: book round 2's PASS and record D3
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +37/-0 | DECISION F015 D3 appended, via records.diff |
| .agent/live_review.md | +2/-0 | `Gate: F015 R2 — ` entry appended, via records.diff |
| .agent/plan.md | +7/-10 | rewritten to the plan.md payload |

Matches the block's expected 37/2/7 insertions exactly.

### 154ca02c F015 R3 C3: expose the six job plan edits through the write door
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +7/-0 | six `job.plan-*` door ids registered |
| packages/orchestration/ui_server.py | +96/-0 | write door dispatches the six edits through `edit_plan` |
| tests/ui_server/test_command_channel.py | +9/-1 | channel test updated for the newly exposed ids |

Matches the block's expected 7/96/9 insertions exactly.

### 09eb2f0e F015 R3 C4: test each door edit, its refusals and its replay
| Path | +/- | Reason |
|---|---|---|
| tests/ui_server/test_command_dispatch.py | +170/-0 | door-edit, refusal and replay tests, via tests.diff |

Matches the block's expected 170 insertions exactly.

### (C5, this commit) F015 R3 C5: rewrite handoff for round 3
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f015-r3-mut 09eb2f0e` for G5 —
  real exit 0.
- `git worktree remove --force .remedy-wt/f015-r3-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f015-r1-dry`, `.remedy-wt/f015-r1-sim`,
  `.remedy-wt/f015-r2-dry`, `.remedy-wt/f015-r2-sim`,
  `.remedy-wt/f015-r3-dry`, `.remedy-wt/f015-r3-sim`, and the four
  pre-existing `.remedy-wt/job-*` worktrees — nothing else, per
  constraint 6.
- `.remedy-wt/f015-r3-worker/` was created (absent on disk, as the block
  anticipates) to hold copy/measure scripts.
- `git push origin feature/f015-interactive-plan-editing` runs after
  this handback is written; its real outcome is reported in the reply
  per G6, not here.
- No `gh pr create`, no merge, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` — none ordered this round.

## Verification

G1 TRANSPORT — each of the 5 payloads' lines/bytes/sha256 measured
against the PAYLOADS table, all matched exactly:
```
records.diff    lines=55  bytes=10308 sha256=34bf7105e76e56942c46005ebb8322c095bc90373e5362bfcd3b1189b705da1c
product.diff    lines=195 bytes=11252 sha256=873f43772a0236ab1a0a86767f7336c1f6fcc6c5e1c626b03e9f2f480a73df9f
tests.diff      lines=178 bytes=9299  sha256=78277c4557900c227ba38fae0d59fbe7acf58a9e88bd323c0981bd1768e38286
mutations.py    lines=91  bytes=3662  sha256=13ea901afcdf7efb6c239014b4e5b1a1360af70c888c2877a814f5cba5aa481f
plan.md         lines=30  bytes=1040  sha256=a2c3be5945057825c6412baf35c29b1c938cc3848b14c5acf7a4748f0112a013
```
The block file itself measured 214 lines, sha256
`648ad013c34672fd68d927310f573cfe7adee8c26fb4d3aefce99f164261566f` —
equal to the delegation message's two readings.
Each committed `.agent/authored/f015-r3-*` blob, read with `git show
<commit>:<path>` (block/plan/mutations.py from `6ca8a5b8`,
records.diff/product.diff/tests.diff from `eee76c36`), compared byte
for byte (sha256) against its source — all 6 matched exactly:
```
f015-r3-block.md      byte_identical=True
f015-r3-plan.md       byte_identical=True
f015-r3-mutations.py  byte_identical=True
f015-r3-records.diff  byte_identical=True
f015-r3-product.diff  byte_identical=True
f015-r3-tests.diff    byte_identical=True
```

G2 THE RECORDS — read with `git show 6c8e549d:<path>`, each equal to
the reviewer's simulation:
```
.agent/live_review.md    296098 bytes  cc40dce56989d91a9fa340ee6a31bfa45b427f7ac2548b5f25c6a906a0504738  MATCH
.agent/decisions.md     1984549 bytes  6b2efb6b7e5933eec3469d22a3748a12c655435c426db551cb48277d756a88db  MATCH
.agent/plan.md             1040 bytes  a2c3be5945057825c6412baf35c29b1c938cc3848b14c5acf7a4748f0112a013  MATCH
```
`open_finding_ids` (scripts/rotate_live_review.py) over
`.agent/live_review.md`'s text: at `1a95e306` -> `{R-0499, R-0950,
R-1008, R-1046}` (4); at `6c8e549d` (C2) -> the same 4; set difference
in both directions = `{}` — matches the reviewer's reading of 4 and 4,
both differences empty. Count of lines C2's diff adds to
`.agent/live_review.md` beginning `Gate: F015 R2 — `: 1 — matches.

G3 THE PRODUCT AND ITS TESTS — at C4 (`09eb2f0e`), read with `git show
09eb2f0e:<path>`, each equal to the reviewer's simulation:
```
apps/cli/command_catalog.py                119725 bytes  abe715b074a51d70b87463fa2c5fec1d5a481135736fefa5f3a977f7b2ffd654  MATCH
packages/orchestration/ui_server.py        160376 bytes  013fb11911304f7c8d141ea4b8ae1c7ce4822ef237a560889d87af49d3ab9307  MATCH
tests/ui_server/test_command_channel.py     95157 bytes  f629afd8ecde1820d2ccf9f685d181cff46b08e86b774a622142085696e6c329  MATCH
tests/ui_server/test_command_dispatch.py    37468 bytes  1bb3e1a4a492c34a4698693fc0cdf529692748c1cd4d6a935c5d3c146d3e9558  MATCH
```
`git diff --name-only 6c8e549d 154ca02c` names exactly the 3 paths C3
lists. `git diff --name-only 154ca02c 09eb2f0e` names exactly the 1
path C4 lists. Both match.

G4 THE TESTS — `bash .remedy-wt/f015-r3-scratch/g4.sh
/home/decodeux/Repos/remedy` at C4, serially:
```
2185 passed, 5 skipped in 113.95s (0:01:53)
REAL_EXIT=0
All checks passed!
RUFF_EXIT=0
{"check_count": 6, "checks": [...], "fail_count": 0, "ok": true, "passed": true, ...}
 all six checks "pass": handler_import (handlers=157),
 live_review_verdict, plan_consistency, relevant_untracked,
 repo_root_hygiene, high_blockers_open
INTEGRITY_EXIT=0
```
The reviewer's sim read `2184 passed, 6 skipped` at pytest exit 0; the
block explains the difference in advance — this tree carries the block
copy the sim lacked, which a test parametrized over the saved blocks
may count once more (2185 = 2184 + 1, 5 = 6 - 1). Both `RUFF_EXIT` and
`INTEGRITY_EXIT` match the reviewer's reading exactly, and all six
integrity checks read `pass` at `fail_count` 0 with `handlers=157`,
also matching.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r3-mut
09eb2f0e` (real exit 0), then `python3 -B
.remedy-wt/f015-r3-payloads/mutations.py .remedy-wt/f015-r3-mut`:
```
control_before                                         141 passed, exit 0
m1  (a door id runs the wrong edit)                      3 failed, exit 1
m2  (a missing version reaches the backend)              2 failed, exit 1
m3  (expected_version rides into the edit log)           6 failed, exit 1
m4  (the editor is not the token's fingerprint)          6 failed, exit 1
m5  (a conflict is worded as a closed plan)              1 failed, exit 1
m6  (argument refusals are not shape errors)             2 failed, exit 1
m7  (an invalid plan hides its violation)                1 failed, exit 1
m8  (a closed plan is a server fault)                    1 failed, exit 1
m9  (refusals fall to the generic clause)                5 failed, exit 1
m10 (an edit is not exposed)                             2 failed, exit 1
control_after                                          141 passed, exit 0
```
Every "restored byte-identical" line read `True` (10 of 10). All
counts, exit codes and the restore lines match the reviewer's reading
exactly. Then `git worktree remove --force .remedy-wt/f015-r3-mut`
(real exit 0), `git worktree prune` (real exit 0); `git worktree list`
afterward shows the primary checkout, `.remedy-wt/f015-r1-dry`,
`.remedy-wt/f015-r1-sim`, `.remedy-wt/f015-r2-dry`,
`.remedy-wt/f015-r2-sim`, `.remedy-wt/f015-r3-dry`,
`.remedy-wt/f015-r3-sim`, and the four `.remedy-wt/job-*` worktrees —
nothing else.

(G6 — the push and the final `git log`/status/worktree/PR-list
readings — is reported in the reply, not here, per the block's own
DONE-WHEN/WHAT TO REPORT instruction: G6 runs after this handback is
written and C5 is committed.)

## Authored-text proofs

`f015-r3-block.md`, `f015-r3-plan.md`, `f015-r3-mutations.py`,
`f015-r3-records.diff`, `f015-r3-product.diff` and `f015-r3-tests.diff`
copies: each read back with `git show <commit>:<path>` and compared
against the payload table's own reading — all 6 matched byte for byte
(see G1 above). `records.diff` was applied with `git apply` (never
retyped), preceded by a real `git apply --check` at exit 0 and followed
by the real `git apply` at exit 0. `product.diff` and `tests.diff` were
applied the same way — each `git apply --check` at exit 0, then
`git apply` at exit 0. `plan.md` was copied whole with
`shutil.copyfile` into `.agent/plan.md`, never retyped, never edited.
`mutations.py` was run as a tool against the G5 worktree, never applied
to any tracked file.

## Deviations & assumptions

None. The bundle ran in the block's declared order: BEFORE ANYTHING
ELSE, PAYLOADS measurement, C1a, C1b, C2, C3, C4, G1, G2, G3, G4, G5,
this handback (C5). No extra, dropped or reordered commit or action
occurred. The one numeric difference from the reviewer's reading —
G4's pytest summary line (2185 passed, 5 skipped here vs 2184 passed,
6 skipped in the reviewer's sim) — is not a deviation from the block:
the block itself names and explains this exact variance (this tree's
extra block-copy payload feeding a block-parametrized test) before the
gate runs.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 335 insertions, matches block formula (214+121) |
| C1b | done | 428 insertions, matches block's expected exactly |
| C2 | done | records + D3, matches 37/2/7 exactly |
| C3 | done | six job.plan-* door edits, matches 7/96/9 exactly |
| C4 | done | test files, matches 170 exactly |
| C5 | done | this commit |
| G1 | done | all 5 payloads and 6 authored copies matched byte for byte |
| G2 | done | all 3 file hashes, finding-id sets and Gate-line count matched |
| G3 | done | all 4 file hashes and both diff name-only checks matched |
| G4 | done | pytest/ruff/integrity all exit 0; count variance explained by the block itself |
| G5 | done | all 10 mutations + both controls matched the reviewer's reading exactly |
| G6 | done | reported in the reply, not the handback, per the block's own instruction |
| Push | done | reported in the reply, not the handback, per the block's own G6 instruction |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round
3. Then T003 — the plan's content hash recorded when the approval is
consumed and asserted when the job starts, the `plan.md` revision
goldens, and the end-to-end run of an edited plan. Open findings: 4.
Operator questions: 1.
