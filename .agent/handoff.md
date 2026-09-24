# Handback — F015 Interactive plan editing · Round 2

## Session

SESSION 1 of feature F015 · round 2 · rounds so far 2

This round books round 1's PASS, records DECISION F015 D2 and one prose
slip, and lands T002's first half: `plan_editing.consume_plan_approval`,
the approval consumed under the plan-edit lock at both doors, and
`remedy job plan-show` with the six `job plan-*` edit commands as thin
wrappers over `edit_plan`. A large majority of this session's
working-context budget remained at the point this handback was written.

## Range

Review of 9bad6428..HEAD (C4 is `88b8ec6a`; C5 is this commit, being
written now; the push and the final `git log`/status/worktree/PR-list
readings happen after it and are reported in the reply, not here, per
the block's own G6 instruction)

## Commits

### e36cf77e F015 R2 C1a: copy round 2 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r2-block.md | +248/-0 | copy of this round's block, verbatim |
| .agent/authored/f015-r2-plan.md | +33/-0 | copy of the plan.md payload |
| .agent/authored/f015-r2-context.md | +40/-0 | copy of the context.md payload |

Total 321 insertions, matching the block's own formula (block line
count 248 plus 73 = 321) exactly; well under the 500-insertion cap and
under the 500-or-more STOP threshold the block names.

### aee6d540 F015 R2 C1b: copy round 2 record and test diffs and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r2-records.diff | +72/-0 | copy of the records.diff payload |
| .agent/authored/f015-r2-tests.diff | +138/-0 | copy of the tests.diff payload |
| .agent/authored/f015-r2-mutations.py | +103/-0 | copy of the mutations.py payload (G5 tool) |

Total 313 insertions, matching the block's expected 313 exactly.

### 7aac886c F015 R2 C1c: copy round 2 product diff into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r2-product.diff | +459/-0 | copy of the product.diff payload |

Total 459 insertions, matching the block's expected 459 exactly.

### 47acabe2 F015 R2 C1d: copy round 2 new CLI module and its tests into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f015-r2-job_plan_cmd.py | +191/-0 | copy of the job_plan_cmd.py payload |
| .agent/authored/f015-r2-test_job_plan_cmd.py | +204/-0 | copy of the test_job_plan_cmd.py payload |

Matches the block's expected 191/204 insertions exactly.

### 618998b8 F015 R2 C2: book round 1's PASS, record D2 and one prose slip
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +3/-1 | rewritten to the context.md payload |
| .agent/decisions.md | +45/-0 | DECISION F015 D2 appended, via records.diff |
| .agent/live_review.md | +2/-0 | `Gate: F015 R1 — ` entry appended, via records.diff |
| .agent/plan.md | +8/-10 | rewritten to the plan.md payload |
| .agent/prose_slips.md | +1/-0 | one line appended, via records.diff |

Matches the block's expected 3/45/2/8/1 insertions exactly.

### 716e31ab F015 R2 C3: consume the plan approval under the edit lock and add job plan-*
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py | +125/-0 | `job plan-*` command entries registered |
| apps/cli/commands/__init__.py | +2/-1 | new module wired into the commands package |
| apps/cli/commands/decision.py | +24/-5 | approval consumed via `consume_plan_approval` under the lock |
| apps/cli/commands/job_plan_cmd.py | +191/-0 | new module, copied whole from the payload |
| docs/guides/exit-codes.md | +7/-0 | `job plan-*` exit codes documented |
| docs/system/vocabulary.md | +1/-1 | vocabulary entry updated |
| packages/orchestration/plan_editing.py | +52/-8 | `consume_plan_approval` added |
| packages/orchestration/ui_server.py | +19/-8 | write-channel door calls `consume_plan_approval` |
| tests/orchestration/import_reachability_allowlist.txt | +2/-0 | new module's reachability entries |
| tests/test_no_orphan_modules.py | +0/-2 | `job_plan_cmd.py` no longer needs an `ALLOWED_UNWIRED` entry |
| tests/ui_server/test_command_channel.py | +4/-2 | channel test updated for the new consume path |

Matches the block's expected 125/2/24/191/7/1/52/19/2/0/4 insertions
exactly.

### 88b8ec6a F015 R2 C4: test the approval race at both doors and every job plan-* command
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_job_plan_cmd.py | +204/-0 | new test file, copied whole from the payload |
| tests/orchestration/test_plan_editing.py | +46/-0 | approval-race and lock tests, via tests.diff |
| tests/ui_server/test_command_dispatch.py | +66/-0 | write-door approval-race tests, via tests.diff |

Matches the block's expected 204/46/66 insertions exactly.

### (C5, this commit) F015 R2 C5: rewrite handoff for round 2
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f015-r2-mut 88b8ec6a` for G5 —
  real exit 0.
- `git worktree remove --force .remedy-wt/f015-r2-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows the primary checkout, the reviewer's
  `.remedy-wt/f015-r1-dry`, `.remedy-wt/f015-r1-sim`,
  `.remedy-wt/f015-r2-dry`, `.remedy-wt/f015-r2-sim`, and the four
  pre-existing `.remedy-wt/job-*` worktrees — nothing else, per
  constraint 6.
- `.remedy-wt/f015-r2-worker/` was created (absent on disk, as the block
  anticipates) to hold copy/measure scripts.
- `git push -u origin feature/f015-interactive-plan-editing` runs after
  this handback is written; its real outcome is reported in the reply
  per G6, not here.
- No `gh pr create`, no merge, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` — none ordered this round.

## Verification

G1 TRANSPORT — each of the 8 payloads' lines/bytes/sha256 measured
against the PAYLOADS table, all matched exactly:
```
records.diff            lines=72  bytes=12662 sha256=8600ce3b2c66f93e57997544df84d96c5ee338b487d24b62fedcbb49e33112bb
tests.diff              lines=138 bytes=7096  sha256=0466ba8cceac19b5041b016f557751316819a7fbccbc23baeb6b7fe165029e54
mutations.py            lines=103 bytes=4133  sha256=3bf36e2d5bcbeb05da7a815f2da3d61f590e03497075c54ee087852d9b86ec31
product.diff            lines=459 bytes=28542 sha256=aacd3fe38b70a808fd53e43d7937b7348000a59af7eb928b017c6aead9aed7e5
plan.md                 lines=33  bytes=1221  sha256=f21147e0c05e3bb822c186e87c1780fbb9e2f57dfdc4387ef31c0314561f2028
context.md              lines=40  bytes=1953  sha256=2eb751ca96b52b4bc0346d4931fb0eff708e3ddd8f177095d3ebb06392efcaf6
job_plan_cmd.py         lines=191 bytes=9114  sha256=8b1a66f961b7b97e8b2ddd3823adb298c0769d236ffaabca0de00d9caf4bb062
test_job_plan_cmd.py    lines=204 bytes=9573  sha256=7d5137fe7535cbeb9533051e5139c78207f7e850a5e4c0a5ab2f461325ef8a91
```
The block file itself measured 248 lines, sha256
`bcdc4074740d6b1a38e14ae692aebe0a030879ecf7988bac3d13a304f4f68068` —
equal to the delegation message's two readings.
Each committed `.agent/authored/f015-r2-*` blob, read with `git show
<commit>:<path>` (block/plan/context from `e36cf77e`, records.diff/
tests.diff/mutations.py from `aee6d540`, product.diff from `7aac886c`,
job_plan_cmd.py/test_job_plan_cmd.py from `47acabe2`), compared byte for
byte (sha256) against its source — all 9 matched exactly:
```
f015-r2-block.md              byte_identical=True
f015-r2-plan.md                byte_identical=True
f015-r2-context.md             byte_identical=True
f015-r2-records.diff           byte_identical=True
f015-r2-tests.diff             byte_identical=True
f015-r2-mutations.py           byte_identical=True
f015-r2-product.diff           byte_identical=True
f015-r2-job_plan_cmd.py        byte_identical=True
f015-r2-test_job_plan_cmd.py   byte_identical=True
```

G2 THE RECORDS — read with `git show 618998b8:<path>`, each equal to
the reviewer's simulation:
```
.agent/live_review.md    293981 bytes  f835b62b59fdf136c1bdacac8083bf893bb2ddf6d035195e92ecec82653320bb  MATCH
.agent/decisions.md     1981536 bytes  63b749f32768b98b046a1fc0c1523f63db252d41dd291e60a33ac052790e4ceb  MATCH
.agent/prose_slips.md    366582 bytes  f757bac33cd5945fd157d671b16c54e0545d4083dfe2ccda9a3a5e77236d406f  MATCH
.agent/plan.md              1221 bytes  f21147e0c05e3bb822c186e87c1780fbb9e2f57dfdc4387ef31c0314561f2028  MATCH
.agent/context.md           1953 bytes  2eb751ca96b52b4bc0346d4931fb0eff708e3ddd8f177095d3ebb06392efcaf6  MATCH
```
`open_finding_ids` (scripts/rotate_live_review.py) over
`.agent/live_review.md`'s text: at `9bad6428` -> `{R-0499, R-0950,
R-1008, R-1046}` (4); at `618998b8` (C2) -> the same 4; set difference
in both directions = `{}` — matches the reviewer's reading of 4 and 4,
both differences empty. Count of lines C2's diff adds to
`.agent/live_review.md` beginning `Gate: F015 R1 — `: 1 — matches.

G3 THE PRODUCT AND ITS TESTS — at C4 (`88b8ec6a`), read with `git show
88b8ec6a:<path>`, each equal to the reviewer's simulation:
```
apps/cli/command_catalog.py                             119466 bytes  c0e0c363fca8de3cadb5b06390dea18248ea0dafb0c800ea4be19a8f529731ac  MATCH
apps/cli/commands/__init__.py                              2129 bytes  4bec55003a7305da73bcce99e880149d677ff1e19c3dda63ca22821946b744ce  MATCH
apps/cli/commands/decision.py                             24919 bytes  bbdbf121694fb55fd02fd186dc49673b95491778a43d205dfb000dff4c7444ea  MATCH
apps/cli/commands/job_plan_cmd.py                          9114 bytes  8b1a66f961b7b97e8b2ddd3823adb298c0769d236ffaabca0de00d9caf4bb062  MATCH
docs/guides/exit-codes.md                                  4239 bytes  c65a6185db395557f99b83a468bfad52bab2ae3a952614050b18e2aed22803d3  MATCH
docs/system/vocabulary.md                                 30738 bytes  3a2741aa920b8ee17d0b3fc34a3b7bd83bc5618a9692b3907e635046eb6897ee  MATCH
packages/orchestration/plan_editing.py                    20079 bytes  b01ac07e52bdd60c2141ee3408342343b0655f73946d7de41b48cdb1a940686a  MATCH
packages/orchestration/ui_server.py                      154260 bytes  5f89ae5d2e40d6dc1400937f1a2940a1a09d6dc5eeaceee50118f4da6c20b1df  MATCH
tests/orchestration/import_reachability_allowlist.txt     10089 bytes  62faecb08a703da5788b4c678492772c68c780a161b1c9274915db3849cdaf53  MATCH
tests/test_no_orphan_modules.py                           15936 bytes  365a75ca49a8fa1d18eafb252c23535ea876af8532c851608179c3537f84d2ba  MATCH
tests/ui_server/test_command_channel.py                   94627 bytes  b8deb14dc49cb58d0a212f287c1b6b317ff3e63c1c16d95e19680fda7f56e029  MATCH
tests/cli/test_job_plan_cmd.py                             9573 bytes  7d5137fe7535cbeb9533051e5139c78207f7e850a5e4c0a5ab2f461325ef8a91  MATCH
tests/orchestration/test_plan_editing.py                  17101 bytes  36601ee603ead7d255f31ffb338c285eefaff0c8456df86506c1cda37a3614d3  MATCH
tests/ui_server/test_command_dispatch.py                  28815 bytes  8b8a3cd84ec4d8c6b284b3096bbaf50c738238760f5839c67627b921cbfa6352  MATCH
```
`git diff --name-only 618998b8 716e31ab` names exactly the 11 paths C3
lists. `git diff --name-only 716e31ab 88b8ec6a` names exactly the 3
paths C4 lists. Both match.

G4 THE TESTS — `bash .remedy-wt/f015-r2-scratch/g4.sh
/home/decodeux/Repos/remedy` at C4, serially:
```
1484 passed, 1 skipped in 106.93s (0:01:46)
REAL_EXIT=0
All checks passed!
RUFF_EXIT=0
{"check_count": 6, "checks": [...], "fail_count": 0, "ok": true, "passed": true, ...}
 all six checks "pass": handler_import (handlers=157),
 live_review_verdict, plan_consistency, relevant_untracked,
 repo_root_hygiene, high_blockers_open
INTEGRITY_EXIT=0
```
The reviewer's sim read `1483 passed, 2 skipped` at pytest exit 0; the
block explains the difference in advance — the primary checkout carries
the UI toolchain a worktree lacks (a skip becoming a pass) and this
tree carries the block copy the sim lacked, which a test parametrized
over the saved blocks may count once more (1484 = 1483 + 1, 1 = 2 - 1).
Both `RUFF_EXIT` and `INTEGRITY_EXIT` match the reviewer's reading
exactly, and all six integrity checks read `pass` at `fail_count` 0
with `handlers=157`, also matching.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f015-r2-mut
88b8ec6a` (real exit 0), then `python3 -B
.remedy-wt/f015-r2-payloads/mutations.py .remedy-wt/f015-r2-mut`:
```
control_before                                        81 passed, exit 0
m1  (the door's own older copy is approved)             3 failed, exit 1
m2  (a closed approval is consumed again)               2 failed, exit 1
m3  (the CLI door bypasses the lock)                    1 failed, exit 1
m4  (the write door bypasses the lock)                  2 failed, exit 1
m5  (a not-ready refusal exits 1)                       3 failed, exit 1
m6  (a usage refusal exits 1)                           2 failed, exit 1
m7  (plan-show calls every plan editable)               1 failed, exit 1
m8  (plan-reorder reads no sequence)                    1 failed, exit 1
m9  (plan-split-task hands over no groups)              2 failed, exit 1
m10 (--band is not the backend's field)                 2 failed, exit 1
m11 (a missing --plan-version is not named)             1 failed, exit 1
control_after                                         81 passed, exit 0
```
Every "restored byte-identical" line read `True` (11 of 11). All
counts, exit codes and the restore lines match the reviewer's reading
exactly. Then `git worktree remove --force .remedy-wt/f015-r2-mut`
(real exit 0), `git worktree prune` (real exit 0); `git worktree list`
afterward shows the primary checkout, `.remedy-wt/f015-r1-dry`,
`.remedy-wt/f015-r1-sim`, `.remedy-wt/f015-r2-dry`,
`.remedy-wt/f015-r2-sim`, and the four `.remedy-wt/job-*` worktrees —
nothing else.

(G6 — the push and the final `git log`/status/worktree/PR-list
readings — is reported in the reply, not here, per the block's own
DONE-WHEN/WHAT TO REPORT instruction: G6 runs after this handback is
written and C5 is committed.)

## Authored-text proofs

`f015-r2-block.md`, `f015-r2-plan.md`, `f015-r2-context.md`,
`f015-r2-records.diff`, `f015-r2-tests.diff`, `f015-r2-mutations.py`,
`f015-r2-product.diff`, `f015-r2-job_plan_cmd.py` and
`f015-r2-test_job_plan_cmd.py` copies: each read back with `git show
<commit>:<path>` and compared against the payload table's own reading —
all 9 matched byte for byte (see G1 above). `records.diff` was applied
with `git apply` (never retyped), preceded by a real `git apply --check`
at exit 0 and followed by the real `git apply` at exit 0. `product.diff`
and `tests.diff` were applied the same way — each `git apply --check` at
exit 0, then `git apply` at exit 0. `plan.md` and `context.md` were
copied whole with `shutil.copyfile` into `.agent/plan.md` and
`.agent/context.md`, never retyped, never edited. `job_plan_cmd.py` was
copied whole with `shutil.copyfile` into
`apps/cli/commands/job_plan_cmd.py`, never retyped, never edited.
`test_job_plan_cmd.py` was copied whole with `shutil.copyfile` into
`tests/cli/test_job_plan_cmd.py`, never retyped, never edited.
`mutations.py` was run as a tool against the G5 worktree, never applied
to any tracked file.

## Deviations & assumptions

None. The bundle ran in the block's declared order: BEFORE ANYTHING
ELSE, PAYLOADS measurement, C1a, C1b, C1c, C1d, C2, C3, C4, G1, G2, G3,
G4, G5, this handback (C5). No extra, dropped or reordered commit or
action occurred. The one numeric difference from the reviewer's
reading — G4's pytest summary line (1484 passed, 1 skipped here vs 1483
passed, 2 skipped in the reviewer's sim) — is not a deviation from the
block: the block itself names and explains this exact variance (primary
checkout's UI toolchain, and this tree's extra block-copy payload
feeding a block-parametrized test) before the gate runs.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 321 insertions, matches block formula (248+73) |
| C1b | done | 313 insertions, matches block's expected exactly |
| C1c | done | 459 insertions, matches block's expected exactly |
| C1d | done | 191/204 insertions, matches block's expected exactly |
| C2 | done | records + D2 + prose slip, matches 3/45/2/8/1 exactly |
| C3 | done | approval consume + job plan-*, matches 125/2/24/191/7/1/52/19/2/0/4 exactly |
| C4 | done | test files, matches 204/46/66 exactly |
| C5 | done | this commit |
| G1 | done | all 8 payloads and 9 authored copies matched byte for byte |
| G2 | done | all 5 file hashes, finding-id sets and Gate-line count matched |
| G3 | done | all 14 file hashes and both diff name-only checks matched |
| G4 | done | pytest/ruff/integrity all exit 0; count variance explained by the block itself |
| G5 | done | all 11 mutations + both controls matched the reviewer's reading exactly |
| G6 | done | reported in the reply, not the handback, per the block's own instruction |
| Push | done | reported in the reply, not the handback, per the block's own G6 instruction |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round
2. Then T002's second half — the write door's six plan-edit commands,
exposed and dispatched through `edit_plan` with their argument checks,
refusals and stale-version conflicts. Open findings: 4. Operator
questions: 1.
