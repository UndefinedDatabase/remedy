# Handback — F267 List commands v2 completion · Round 1

## Session

SESSION 1 of feature F267 · round 1 · rounds so far 1

This round cuts F267's branch, claims F267, re-heads the live review
record with F265's closing verdict, records DECISION F267 D1, and lands
T002 and T003 as one new test file. A large majority of this session's
working-context budget remained at the point this handback was written.

## Range

Review of 9f06c509..HEAD (C4 is this commit, being written now; the push
happens after it and is reported in the reply, not here, per the block's
own G6 instruction)

## Commits

### 01c66ed2 F267 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f267-r1-block.md | +206/-0 | copy of this round's block, verbatim |
| .agent/authored/f267-r1-claim.diff | +131/-0 | copy of the claim.diff payload |
| .agent/authored/f267-r1-context.md | +39/-0 | copy of the context.md payload |
| .agent/authored/f267-r1-plan.md | +31/-0 | copy of the plan.md payload |

Total 407 insertions, matching the block's own formula (block line count
206 plus 201 = 407) exactly; well under the 500-insertion cap and under
the 500-or-more STOP threshold the block names.

### 3d9ef9ff F267 R1 C1b: copy round 1 mutation tool and test payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f267-r1-mutations.py | +59/-0 | copy of the mutations.py payload |
| .agent/authored/f267-r1-test_list_commands_everywhere.py | +164/-0 | copy of the test payload |

Total 223 insertions, matching the block's expected 223 exactly.

### 7705b3a0 F267 R1 C2: claim F267, re-head the live review record, record D1
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +15/-25 | rewritten to the context.md payload |
| .agent/decisions.md | +38/-0 | DECISION F267 D1 appended, via claim.diff |
| .agent/live_review.md | +31/-30 | re-headed with F265's closing verdict, via claim.diff |
| .agent/plan.md | +17/-14 | rewritten to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F267's line flipped `[ ]` -> `[~]`, via claim.diff |

Matches the block's expected 15 context.md, 38 decisions.md, 31
live_review.md, 17 plan.md, 1 STATUS.md exactly.

### 632e9f49 F267 R1 C3: prove every list handler and the ten-second demo
| Path | +/- | Reason |
|---|---|---|
| tests/cli/test_list_commands_everywhere.py | +164/-0 | new test file, copied whole from the payload |

Matches the block's expected 164 exactly.

### (C4, this commit) F267 R1 C4: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git checkout -b feature/f267-list-commands-v2-completion` (BEFORE
  ANYTHING ELSE, step 2) — succeeded, branch cut from `9f06c509`.
- `git worktree add --detach .remedy-wt/f267-r1-mut 632e9f49` (for G5) —
  succeeded.
- `git worktree remove --force .remedy-wt/f267-r1-mut` and
  `git worktree prune` (after G5) — both succeeded.
- `.remedy-wt/f267-r1-worker/` was created with `mkdir -p` (absent on
  disk, as the block anticipates) to hold the copy and verification
  scripts. `.remedy-wt/f267-r1-dry`, `.remedy-wt/f267-r1-sim`,
  `.remedy-wt/f267-r1-payloads`, `.remedy-wt/f267-r1-scratch` and the
  four `.remedy-wt/job-*` worktrees were left untouched.
- `git push -u origin feature/f267-list-commands-v2-completion` (after
  C4) runs after this handback is written; its real outcome is reported
  in the reply per G6, not here. No pull request is created this round —
  the branch opens one at F267's closure.

## Verification

G1 TRANSPORT — each of the 5 payloads' lines/bytes/sha256 measured
against the PAYLOADS table — all matched exactly:
```
claim.diff                          lines=131 bytes=12916 sha256=cd8874f2e4661cfa0c21408d79b89a317a2c526e150f2763f752dc3827c99adb
context.md                          lines=39  bytes=1820  sha256=884f577e6f16f42ead9a69d8ab0a2b7ab4a47c315bd0a072519ab4496970cfb1
mutations.py                        lines=59  bytes=2645  sha256=308498a53f4d3e2874e6e402342dda628db5a396d6f09241e82e2645346d67c9
plan.md                             lines=31  bytes=1036  sha256=f953dc1eac281536142c677d03a19baf389f860e5828608731b410664b7024be
test_list_commands_everywhere.py    lines=164 bytes=7077  sha256=e7e0677af6469ae62495dc844da95a8637b90ed6d1718607f093134eb9fa6e32
```
The block file itself measured 206 lines, sha256
`31ed0267317ce9cf3ab989287aa0dbba2a521e12645689d52b1a0cb9e86cb4fd` —
equal to the delegation message's two readings.
Each committed `.agent/authored/f267-r1-*` blob, read with `git show
<commit>:<path>` from the commit that added it (block/plan/context/claim
at `01c66ed2`, mutations/test at `3d9ef9ff`), compared byte for byte
(sha256) against its source — all 6 copies matched exactly.

G2 THE CLAIM — read with `git show 7705b3a0:<path>`, each equal to the
reviewer's simulation:
```
.agent/live_review.md    298850 bytes  efac3d878218f508cc4839a3530768df3db611e03459fd2bd31c62939e1bc659  MATCH
docs/roadmap/STATUS.md    49391 bytes  3edb355e785edfcaa5f8f28d99a3ecc9156d1ee60389bb7bb0526e1baecf8088  MATCH
.agent/decisions.md     1973311 bytes  37396126bb4586394beb38842a81ff7ed62368ab23b6765ae5b68169cf5b31c1  MATCH
.agent/plan.md              1036 bytes f953dc1eac281536142c677d03a19baf389f860e5828608731b410664b7024be  MATCH
.agent/context.md           1820 bytes 884f577e6f16f42ead9a69d8ab0a2b7ab4a47c315bd0a072519ab4496970cfb1  MATCH
```
`open_finding_ids` (scripts/rotate_live_review.py) over
`.agent/live_review.md`'s text: at `9f06c509` -> `{R-0499, R-0950,
R-1008, R-1046}` (4); at `7705b3a0` (C2) -> `{R-0499, R-0950, R-1008,
R-1046}` (4); set difference in both directions = `{}` — matches the
reviewer's reading of 4 and 4, both differences empty. F267's STATUS
line at C2, read back in full: `- [~] F267 — List commands v2 completion
— sort/filter/limit for the remaining nine commands` — matches exactly.
`git diff --name-only 3d9ef9ff 7705b3a0`: `.agent/context.md`,
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md` — exactly the five named paths, nothing else.

G3 THE TESTS ON DISK — at C3 (`632e9f49`),
`tests/cli/test_list_commands_everywhere.py` read with `git show
632e9f49:<path>`: 7077 bytes, sha256
`e7e0677af6469ae62495dc844da95a8637b90ed6d1718607f093134eb9fa6e32` —
matches. `git diff --name-only 7705b3a0 632e9f49`: exactly
`tests/cli/test_list_commands_everywhere.py`, nothing else.

G4 THE SELECTION — `bash .remedy-wt/f267-r1-scratch/g4.sh
/home/decodeux/Repos/remedy`, serially, in the primary checkout at C3:
```
1028 passed, 1 skipped in 134.08s (0:02:14)
REAL_EXIT=0
All checks passed!
RUFF_EXIT=0
{"check_count": 6, "checks": [{"message": "handlers=150", "name": "handler_import", "status": "pass"}, {"message": "last Gate verdict PASS", "name": "live_review_verdict", "status": "pass"}, {"message": "unchecked=0, context_complete=False", "name": "plan_consistency", "status": "pass"}, {"message": "untracked=0, relevant=0", "name": "relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch, evidence dir or archive at the root", "name": "repo_root_hygiene", "status": "pass"}, {"message": "no open blocker/high findings", "name": "high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true, "passed": true, "schema_version": 1, "version": 1}
INTEGRITY_EXIT=0
```
pytest read `1028 passed, 1 skipped` at exit 0 (reviewer's sim read
`1026 passed, 3 skipped`; totals agree at 1029 both ways — the block's
own caveat anticipates this exact split: the primary checkout carries
the UI toolchain a worktree lacks, and this tree carries the block copy
the sim lacked). Ruff at exit 0. All six integrity checks `pass` at
`fail_count` 0 with `handlers=150` — matches the reviewer's reading in
full.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f267-r1-mut
632e9f49` then `python3 -B .remedy-wt/f267-r1-payloads/mutations.py
.remedy-wt/f267-r1-mut`:
```
control_before REAL_EXIT=0
44 passed in 1.70s
m1_change_list_ignores_sort FROM count in apps/cli/commands/change.py: 1
m1_change_list_ignores_sort REAL_EXIT=1
2 failed, 42 passed in 1.48s
m1_change_list_ignores_sort restored byte-identical: True
m2_decision_list_ignores_sort FROM count in apps/cli/commands/decision.py: 1
m2_decision_list_ignores_sort REAL_EXIT=1
2 failed, 42 passed in 1.49s
m2_decision_list_ignores_sort restored byte-identical: True
m3_mission_list_ignores_sort FROM count in apps/cli/commands/mission_cmd.py: 1
m3_mission_list_ignores_sort REAL_EXIT=1
2 failed, 42 passed in 1.49s
m3_mission_list_ignores_sort restored byte-identical: True
m4_config_list_ignores_sort FROM count in apps/cli/commands/config_cmd.py: 1
m4_config_list_ignores_sort REAL_EXIT=1
2 failed, 42 passed in 1.49s
m4_config_list_ignores_sort restored byte-identical: True
m5_run_list_has_no_date FROM count in apps/cli/commands/do_cmd.py: 1
m5_run_list_has_no_date REAL_EXIT=1
2 failed, 42 passed in 1.49s
m5_run_list_has_no_date restored byte-identical: True
m6_a_relative_bound_points_forward FROM count in packages/orchestration/list_options.py: 1
m6_a_relative_bound_points_forward REAL_EXIT=1
2 failed, 42 passed in 1.49s
m6_a_relative_bound_points_forward restored byte-identical: True
control_after REAL_EXIT=0
44 passed in 1.47s
REAL_EXIT=0
```
Matches the reviewer's reading exactly: control_before `44 passed` at
exit 0; m1-m6 each `2 failed` at exit 1; control_after `44 passed` at
exit 0; every `restored byte-identical` line True. Then
`git worktree remove --force .remedy-wt/f267-r1-mut` (exit 0),
`git worktree prune` (exit 0); `git worktree list` back to the 6
expected names (primary checkout, `f267-r1-dry`, `f267-r1-sim`, four
`job-*` worktrees).

(G6 — the push and the final `git log`/status/worktree/PR-list readings
— is reported in the reply, not here, per the block's own instruction.)

## Authored-text proofs

Block (`.agent/authored/f267-r1-block.md`), `f267-r1-claim.diff`,
`f267-r1-context.md`, `f267-r1-plan.md`, `f267-r1-mutations.py` and
`f267-r1-test_list_commands_everywhere.py` copies: each read back with
`git show <commit>:<path>` and compared against the payload table's own
reading — all 6 matched byte for byte (see G1 above). `claim.diff` was
applied with `git apply` (never retyped), preceded by a real
`git apply --check` at exit 0 and followed by the real `git apply` at
exit 0. `plan.md` and `context.md` were each copied whole with
`shutil.copyfile` into `.agent/plan.md` and `.agent/context.md`, never
retyped, never edited. `test_list_commands_everywhere.py` was copied
whole with `shutil.copyfile` into
`tests/cli/test_list_commands_everywhere.py`, never retyped, never
edited. `mutations.py` is a TOOL run for G5 directly from
`.remedy-wt/f267-r1-payloads/` against the C3 worktree, never applied to
any tracked file; its `.agent/authored/` copy is a record only.

## Deviations & assumptions

1. `.remedy-wt/f267-r1-worker/` did not exist on disk when it was first
   needed (for the C1a copy script); created it with `mkdir -p` before
   use, exactly as the block's own directory list anticipates ("create
   it if absent"). Gitignored, untracked, no effect on the tracked path
   set.
2. G4's pytest summary (`1028 passed, 1 skipped`) differs from the
   reviewer's sim reading (`1026 passed, 3 skipped`) in the split between
   passed and skipped, though both total 1029. This is not an
   unanticipated deviation: the block's own G4 text names both causes in
   advance — the primary checkout carries the UI toolchain a worktree
   lacks (a skip may pass there), and this tree carries the block copy
   the sim lacked (a test parametrized over saved blocks may count once
   more). Ruff and the integrity checks matched the reviewer's reading
   exactly.

No other deviation. The bundle ran in the block's declared order: BEFORE
ANYTHING ELSE, C1a, C1b, C2, C3, G1 through G5, then this handback and
C4 — with no extra, dropped or reordered commit or action.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | this commit |
| G1 | done | |
| G2 | done | |
| G3 | done | |
| G4 | done | |
| G5 | done | |
| G6 | done | reported in the reply, not the handback, per the block's own instruction |
| Push | done | reported in the reply, not the handback, per the block's own G6 instruction |

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round
1. Then the closure sequence's first half — the Built State, the
checklist consolidation, the self-use track and the one full suite.
Open findings: 4. Operator questions: 1.
