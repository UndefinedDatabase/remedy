# Handback — F265 Teacher learning UI v1 · Round 1

## Session

SESSION 1 of feature F265 · round 1 · rounds so far 1

This round cut `feature/f265-teacher-learning-ui` from `main` at `0236e3c3`,
claimed F265, re-headed the live review record, recorded DECISION F265 D1
and operator question Q1, registered finding R-1046, and landed T001's
substance: `packages/orchestration/lessons.py` (a sealed lesson per
completed Run from that Run's own `result.diff`, billed to role `teacher`
inside the teacher's per-job budget pot), the `run_job` hook that writes one
after every applied task when `teacher.lessons` is on, and the module's
tests and twelve red proofs. Roughly two-thirds of this session's working-
context budget remained at the point this handback was written.

## Range

Review of 0236e3c3..HEAD (C5 not yet made when this file was written; see
the reply for C5's SHA and the push outcome)

## Commits

### 46c2e1da F265 R1 C1a: copy round 1 block and state payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f265-r1-block.md | +246/-0 | copy of this round's block, verbatim |
| .agent/authored/f265-r1-context.md | +49/-0 | copy of the context.md payload |
| .agent/authored/f265-r1-plan.md | +37/-0 | copy of the plan.md payload |

### 85aa4a30 F265 R1 C1b: copy round 1 diffs and mutation tool into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f265-r1-claim.diff | +179/-0 | copy of the claim.diff payload |
| .agent/authored/f265-r1-mutations.py | +101/-0 | copy of the mutations.py tool |
| .agent/authored/f265-r1-product.diff | +119/-0 | copy of the product.diff payload |

### f4054c12 F265 R1 C1c: copy round 1 product module into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f265-r1-lessons.py | +360/-0 | copy of the lessons.py product module |

### 8b27700c F265 R1 C1d: copy round 1 test payload into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f265-r1-test_lessons.py | +391/-0 | copy of the test_lessons.py payload |

### 2a2aa42f F265 R1 C2: claim F265, re-head the live review record, record D1, Q1 and R-1046
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md | +22/-23 | rewritten to the context.md payload |
| .agent/decisions.md | +55/-0 | DECISION F265 D1 appended, via claim.diff |
| .agent/live_review.md | +29/-24 | re-headed; R-1046 appended, via claim.diff |
| .agent/operator_questions.md | +23/-1 | Q1 recorded in place of the empty line, via claim.diff |
| .agent/plan.md | +24/-14 | rewritten to the plan.md payload |
| docs/roadmap/STATUS.md | +1/-1 | F265 line flipped to `[~]`, via claim.diff |

### 79c8be1d F265 R1 C3: write a sealed lesson per completed Run from its real diff
| Path | +/- | Reason |
|---|---|---|
| docs/guides/environment.md | +3/-0 | regenerated from the registry, via product.diff |
| packages/orchestration/config.py | +32/-0 | `teacher.lessons` config key, via product.diff |
| packages/orchestration/lessons.py | +360/-0 | new module: sealed lesson per Run, from its own diff, billed to `teacher` |
| packages/orchestration/pingpong_job.py | +32/-0 | `run_job` hook wired in, via product.diff |
| tests/orchestration/import_reachability_allowlist.txt | +1/-0 | allowlist entry for the new module, via product.diff |

### 79713a5e F265 R1 C4: test the lesson generator, its pot and its hook
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_lessons.py | +391/-0 | tests for the lesson generator, its pot and its hook |

### (C5, this commit) F265 R1 C5: rewrite handoff for round 1
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this handback |

## External actions

- `git worktree add --detach .remedy-wt/f265-r1-mut 79713a5e` — REAL_EXIT=0.
- `git worktree remove --force .remedy-wt/f265-r1-mut` — REAL_EXIT=0.
- `git worktree prune` — REAL_EXIT=0.
- `git push -u origin feature/f265-teacher-learning-ui` — run after this
  commit; reported in the reply with its real outcome.
- No `gh pr create`: the block orders none this round (the branch opens one
  at F265's closure). `gh pr list --state open ...` run at G6, reported in
  the reply.
- No other worktree add/remove this round; `.remedy-wt/f265-r1-dry`,
  `.remedy-wt/f265-r1-sim` and the `.remedy-wt/job-*` worktrees were left
  untouched.

## Verification

G1 TRANSPORT — each of the 7 payloads' lines/bytes/sha256 measured against
the PAYLOADS table, all matched exactly (claim.diff, plan.md, context.md,
product.diff, mutations.py, lessons.py, test_lessons.py). Each committed
`.agent/authored/f265-r1-*` blob, read with `git show <commit>:<path>`,
compared byte for byte against its source — all 8 copies (block.md,
plan.md, context.md, claim.diff, product.diff, mutations.py, lessons.py,
test_lessons.py) matched exactly, same sha256 on both sides.

G2 THE CLAIM — read with `git show 2a2aa42f:<path>`, all 6 files matched
the reviewer's simulated reading exactly:
```
.agent/live_review.md         304905 bytes  05107e03...  MATCH
docs/roadmap/STATUS.md         49035 bytes  d791bef9...  MATCH
.agent/decisions.md          1960311 bytes  b5743b7a...  MATCH
.agent/operator_questions.md    2192 bytes  3f283145...  MATCH
.agent/plan.md                  1508 bytes  d3c22982...  MATCH
.agent/context.md               2380 bytes  93335fab...  MATCH
```
`open_finding_ids` (scripts/rotate_live_review.py) over the file's text:
at `0236e3c3` → `{R-0499, R-0950, R-1008}` (3); at `2a2aa42f` → `{R-0499,
R-0950, R-1008, R-1046}` (4); set difference C2-minus-base = `{R-1046}`,
base-minus-C2 = `{}` — matches the reviewer's reading exactly. F265's
STATUS line at C2 read back in full: `- [~] F265 — Teacher learning UI v1
(post-task lessons)` — matches. `git diff --name-only 8b27700c 2a2aa42f`
named exactly `.agent/context.md`, `.agent/decisions.md`,
`.agent/live_review.md`, `.agent/operator_questions.md`, `.agent/plan.md`,
`docs/roadmap/STATUS.md` — matches.

G3 THE PRODUCT — at C4 (`79713a5e`), read with `git show 79713a5e:<path>`,
all 6 files matched the reviewer's simulated reading exactly:
```
packages/orchestration/lessons.py                       17032 bytes  8a3c60e8...  MATCH
packages/orchestration/pingpong_job.py                 202583 bytes  230ab34c...  MATCH
packages/orchestration/config.py                        63325 bytes  6180ae0c...  MATCH
docs/guides/environment.md                              21327 bytes  f8f13965...  MATCH
tests/orchestration/import_reachability_allowlist.txt   10022 bytes  d9ffe3df...  MATCH
tests/orchestration/test_lessons.py                     16372 bytes  ad4fca0c...  MATCH
```
`git diff --name-only 2a2aa42f 79c8be1d` named exactly the 5 paths C3
edits (docs/guides/environment.md, packages/orchestration/config.py,
packages/orchestration/lessons.py, packages/orchestration/pingpong_job.py,
tests/orchestration/import_reachability_allowlist.txt). `git diff
--name-only 79c8be1d 79713a5e` named exactly
tests/orchestration/test_lessons.py. Both match.

G4 THE TESTS — `bash .remedy-wt/f265-r1-scratch/g4.sh
/home/decodeux/Repos/remedy`:
```
994 passed, 1 skipped in 106.42s (0:01:46)
REAL_EXIT=0
All checks passed!
RUFF_EXIT=0
{"check_count": 6, "checks": [{"message": "handlers=150", "name":
"handler_import", "status": "pass"}, {"message": "last Gate verdict PASS",
"name": "live_review_verdict", "status": "pass"}, {"message":
"unchecked=0, context_complete=False", "name": "plan_consistency",
"status": "pass"}, {"message": "untracked=0, relevant=0", "name":
"relevant_untracked", "status": "pass"}, {"message": "no reviewer scratch,
evidence dir or archive at the root", "name": "repo_root_hygiene",
"status": "pass"}, {"message": "no open blocker/high findings", "name":
"high_blockers_open", "status": "pass"}], "fail_count": 0, "ok": true,
"passed": true, "schema_version": 1, "version": 1}
INTEGRITY_EXIT=0
REAL_EXIT=0
```
Pytest read `994 passed, 1 skipped` at exit 0, differing from the
reviewer's sim reading of `992 passed, 3 skipped` — total outcomes equal
(995 both ways). The block itself anticipates this: "the primary checkout
carries the UI toolchain a worktree lacks, so a skip may pass there" —
2 tests that skip in the reviewer's sim worktree ran and passed here. Ruff
exit 0, matching. All six integrity checks read `pass` at `fail_count` 0
with `handlers=150`, matching exactly.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f265-r1-mut
79713a5e` REAL_EXIT=0, then `python3 -B
.remedy-wt/f265-r1-payloads/mutations.py .remedy-wt/f265-r1-mut`:
```
control_before: 29 passed, REAL_EXIT=0
m1 (ungrounded constructs taught): 2 failed, REAL_EXIT=1, restored byte-identical: True
m2 (removed lines count as added): 2 failed, REAL_EXIT=1, restored byte-identical: True
m3 (a stored lesson is regenerated): 1 failed, REAL_EXIT=1, restored byte-identical: True
m4 (a spent pot still calls): 2 failed, REAL_EXIT=1, restored byte-identical: True
m5 (the pot counts every role): 1 failed, REAL_EXIT=1, restored byte-identical: True
m6 (an oversize diff is sent): 1 failed, REAL_EXIT=1, restored byte-identical: True
m7 (no ledger still calls): 1 failed, REAL_EXIT=1, restored byte-identical: True
m8 (the seal is unchecked): 1 failed, REAL_EXIT=1, restored byte-identical: True
m9 (the row is not keyed on the Run): 1 failed, REAL_EXIT=1, restored byte-identical: True
m10 (the hook ignores the switch): 1 failed, REAL_EXIT=1, restored byte-identical: True
m11 (the hook is never called): 1 failed, REAL_EXIT=1, restored byte-identical: True
m12 (the hook names the task as the Run): 2 failed, REAL_EXIT=1, restored byte-identical: True
control_after: 29 passed, REAL_EXIT=0
REAL_EXIT=0
```
Every reading matches the reviewer's sim reading exactly (control 29
passed at both ends, m1-m12 failure counts and exit codes all matching,
every restore byte-identical True). Then `git worktree remove --force
.remedy-wt/f265-r1-mut` REAL_EXIT=0, `git worktree prune` REAL_EXIT=0;
`git worktree list` afterward showed the primary checkout, the 4
`.remedy-wt/job-*` worktrees and the reviewer's `.remedy-wt/f265-r1-dry`
and `.remedy-wt/f265-r1-sim` — nothing else.

## Authored-text proofs

Block (`.agent/authored/f265-r1-block.md`), plan.md, context.md,
claim.diff, product.diff, mutations.py, lessons.py and test_lessons.py
copies: each read back with `git show <commit>:<path>` and compared
against the payload table's own reading — all 8 matched byte for byte (see
G1 above). `claim.diff` and `product.diff` were applied with `git apply`
(never retyped), each preceded by a real `git apply --check` at exit 0 and
followed by the real `git apply` at exit 0. `plan.md`, `context.md`,
`lessons.py` and `test_lessons.py` were copied whole with
`shutil.copyfile`, never retyped.

## Deviations & assumptions

1. G4's pytest summary read `994 passed, 1 skipped` rather than the
   reviewer's sim reading of `992 passed, 3 skipped`. Total outcomes are
   identical (995) and the block's own G4 text anticipates exactly this:
   the primary checkout carries the UI toolchain a worktree lacks, so up
   to some tests that skip in the sim may pass here. Not treated as a
   gate failure; no repair made.

No other deviation. The bundle ran in the block's declared commit order
(C1a, C1b, C1c, C1d, C2, C3, C4, then G1-G5, then C5) with no extra,
dropped or reordered commits or actions.

## Next

Phase 1 rule 1: read `.agent/STOP` from disk. Then the review of round 1.
Then T001's reach: the lesson on the job's event stream, a read-only route
listing a job's lessons, and `remedy do`'s mission path proved end to end.
Open findings: 4. Operator questions: 1.
