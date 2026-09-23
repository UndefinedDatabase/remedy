# Handback — F279 Configuration & toolchain truth · Round 7 · Book round 6's PASS, record DECISION F279 D7, land T004's order half (`docs/orders/toolchain-refresh.md` and its fourteen-day self-use tier)

## Session

SESSION 1 of feature F279 · round 7 · rounds so far 7

This round booked round 6's PASS into the ledger, recorded DECISION F279 D7
(a self-use item is a job file, so the order is written as one and queued
byte for byte; a queue entry carries no date, so the day an order item was
queued is stamped into its `provenance`; the ledger tier always has a
finding to offer, so the order tier comes first), and landed T004's order
half: `docs/orders/toolchain-refresh.md` (a five-task job file), a docs
test pinning its section headings (`tests/docs/test_toolchain_refresh_order.py`),
and the self-use generator's order tier, which queues that file verbatim,
before the ledger tier, at most once every fourteen days
(`packages/orchestration/self_use_generator.py`). With this round every
slice of F279 — T001, T002, T003 and T004 — is built. All of G1-G5 ran
before this handoff was written and matched the block's stated
expectations exactly, byte for byte and reading for reading. Context
self-assessment: a comfortable majority of the working budget remains at
handback.

## Range

Review of `564b54e3`..`HEAD`.

## Commits

### f7209393 F279 R7 C1a: copy round 7 block and bookkeeping payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r7-block.md | +222/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f279-r7-ledger.diff | +10/-0 | Payload copy |
| .agent/authored/f279-r7-plan.md | +32/-0 | Payload copy |
| .agent/authored/f279-r7-decisions.diff | +42/-0 | Payload copy |

Measured insertions: 306 (block's line count 222 plus 84), matching the
block's formula exactly, well under the 500 cap.

### 86114ab8 F279 R7 C1b: copy round 7 product payloads into .agent/authored/
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f279-r7-toolchain-refresh.md | +66/-0 | Payload copy |
| .agent/authored/f279-r7-test_toolchain_refresh_order.py | +51/-0 | Payload copy |
| .agent/authored/f279-r7-self_use_generator.diff | +147/-0 | Payload copy |
| .agent/authored/f279-r7-test_self_use_generator.diff | +96/-0 | Payload copy |
| .agent/authored/f279-r7-test_self_use_runner.diff | +16/-0 | Payload copy |
| .agent/authored/f279-r7-docs_index.diff | +28/-0 | Payload copy |
| .agent/authored/f279-r7-mutations.py | +60/-0 | Payload copy (G5 tool, never applied to a tracked file) |

Measured insertions: 464, matching the block's expected 464 exactly.

### 9028dfa6 F279 R7 C2: book round 6's PASS and record DECISION F279 D7
| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +2/-0 | `ledger.diff` applied: round 6's `Gate:` entry appended |
| .agent/plan.md | +11/-10 | Rewritten to the round-7 plan.md payload |
| .agent/decisions.md | +34/-0 | `decisions.diff` applied: DECISION F279 D7 recorded |

Measured insertions (`git diff --cached --numstat` before commit): 34
decisions.md, 2 live_review.md, 11 plan.md — matching the block's expected
counts exactly.

### 3a4ea6fc F279 R7 C3: add the toolchain refresh order and queue it every fourteen days
| Path | +/- | Reason |
|---|---|---|
| docs/orders/toolchain-refresh.md | +66/-0 | NEW FILE (`shutil.copyfile` from payload), new `docs/orders/` directory: the five-task order job |
| tests/docs/test_toolchain_refresh_order.py | +51/-0 | NEW FILE (`shutil.copyfile` from payload): pins the order's section headings |
| packages/orchestration/self_use_generator.py | +79/-8 | `self_use_generator.diff` applied: the order tier, queued before the ledger tier, at most once every 14 days |
| tests/orchestration/test_self_use_generator.py | +81/-0 | `test_self_use_generator.diff` applied: the order tier's tests, plus an autouse fixture pointing the other tiers' tests at a default order-file location |
| tests/orchestration/test_self_use_runner.py | +4/-1 | `test_self_use_runner.diff` applied: the end-to-end runner test now names the order file |
| docs/README.md | +10/-0 | `docs_index.diff` applied: registers the new order doc in the index |

Measured insertions: 10 docs/README.md, 66 toolchain-refresh.md, 79
self_use_generator.py, 51 test_toolchain_refresh_order.py, 81
test_self_use_generator.py, 4 test_self_use_runner.py — matching the
block's expected counts exactly.

### (this commit) F279 R7 C4: rewrite handoff for round 7
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per docs/agents/handback_template.md |

## External actions

- `git worktree add --detach .remedy-wt/f279-r7-mut 3a4ea6fc` — created for
  G5; `git worktree remove --force .remedy-wt/f279-r7-mut` then
  `git worktree prune` removed it as G5's last action. `git worktree list`
  afterward showed only the primary checkout and the two pre-existing
  `.remedy-wt/job-*` worktrees.
- `git push origin feature/f279-configuration-toolchain-truth` — see the
  session's final reply for the real outcome; it runs after this commit.
- No `gh pr create`, no `gh pr merge`, no force-push, no `git stash`, no
  checkout of `main` or any other branch/commit in the primary checkout: none
  run, per constraint 5.
- `.remedy-wt/job-129b3ad7206d4f8d`, `.remedy-wt/job-e7268925db3a4831`, their
  branches and every existing stash were left untouched.

## Verification

BEFORE ANYTHING ELSE:
- `ls .agent/STOP` → `ls: cannot access '.agent/STOP': No such file or directory`, real exit 2 (ENOENT), absent — proceed.
- `git status --porcelain` → empty. `git branch --show-current` →
  `feature/f279-configuration-toolchain-truth`. `git log --oneline -1` →
  `564b54e3 F279 R6 C4: rewrite handoff for round 6`. All three matched.
- Block bytes (R-0954): measured line count (newline count)=222,
  sha256=`8848e9a3acfdff4020fd608f27bf4c4886d8f4425e0c17665cca340c73d83c0c`;
  matches both readings given in the delegation message exactly.
- `git worktree list` (before any change) → primary checkout at `564b54e3`
  plus `.remedy-wt/job-129b3ad7206d4f8d` (`09441a92`) and
  `.remedy-wt/job-e7268925db3a4831` (`cc8696a3`).
- `git stash list | head -1` →
  `stash@{0}: WIP on (no branch): 365051fa F277 R17 C3: rewrite handoff for round 17 with the rebuilt package readings`.

PAYLOADS — all 10 measured and matched the block's table exactly (line
count, byte count, sha256): decisions.diff (42/3122/`941b08c5...`),
docs_index.diff (28/1549/`08a9658f...`), ledger.diff (10/6198/`85cc5f5f...`),
mutations.py (60/2384/`60869cbc...`), plan.md (32/1381/`dda84bb0...`),
self_use_generator.diff (147/6618/`3ae43fb1...`),
test_self_use_generator.diff (96/5312/`efb8b13c...`),
test_self_use_runner.diff (16/961/`88222882...`),
test_toolchain_refresh_order.py (51/2143/`366ddef5...`),
toolchain-refresh.md (66/3444/`d95d0772...`).

`git apply --check` then `git apply` for every `.diff` payload (ledger,
decisions at C2; self_use_generator, test_self_use_generator,
test_self_use_runner, docs_index at C3): all 6 pairs at real exit code 0,
in the commit order the block specifies. `.agent/plan.md`,
`toolchain-refresh.md` and `test_toolchain_refresh_order.py` were
rewrites/new files by `shutil.copyfile`, never a `git apply`.

G1 TRANSPORT — every `.agent/authored/f279-r7-*` copy (11 files, including
the block copy) read back with `git show <adding-commit>:<path>` and
compared byte-for-byte against its source (`.remedy-wt/f279-r7-block.md` for
the block, `.remedy-wt/f279-r7-payloads/<name>` for the rest): all 11
matched exactly (`cmp` exit 0 for each).

G2 THE BOOKKEEPING — at C2 (`9028dfa6`): `.agent/live_review.md`
bytes=386693 sha256=`b51cd4adc45da4c870374491cb3f25ab7741f5104a9c331b6abe79b20fc50413`
MATCH; `.agent/plan.md` bytes=1381
sha256=`dda84bb0a8c205056b8be083a7eeb92f71d74e5ff3938686e3fc481a329121de` MATCH;
`.agent/decisions.md` bytes=1874787
sha256=`40244b32dfb24e09d635af015a8a696c35aceca78f9f47995d11779824e82b93` MATCH.
Open-finding-id set via `open_finding_ids` (`scripts/rotate_live_review.py`),
computed over `.agent/live_review.md` text at `564b54e3` and at C2: 26 and
26, both set differences empty — matching the block's 26/26 exactly. Lines
beginning `Gate: F279 R6 — ` at `564b54e3` and at C2: 0 and 1 — matching the
block's 0/1 exactly. `git diff --name-only <C1b> <C2>` → exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — matches
C2's list.

G3 THE ORDER — `git diff --name-only <C2> <C3>` → exactly `docs/README.md`,
`docs/orders/toolchain-refresh.md`, `packages/orchestration/self_use_generator.py`,
`tests/docs/test_toolchain_refresh_order.py`,
`tests/orchestration/test_self_use_generator.py`,
`tests/orchestration/test_self_use_runner.py` — matches C3's list exactly.
At C3 (`3a4ea6fc`): `docs/orders/toolchain-refresh.md` bytes=3444
sha256=`d95d0772bc9afb7d6ac46514fb7caefbf8120171cbfa97037144c1e93e8cded8` MATCH;
`tests/docs/test_toolchain_refresh_order.py` bytes=2143
sha256=`366ddef540fe8430a15b542cfd29b70338c3b5348d7e19cc32d0c016f6012ece` MATCH;
`packages/orchestration/self_use_generator.py` bytes=19096
sha256=`a10fbf7e4f012a4e578c57e1bda14fc0d57f7a51632e2d8e82c14544b4537f24` MATCH;
`tests/orchestration/test_self_use_generator.py` bytes=25328
sha256=`d1fe7505d28a1a7c6a7887801e581abe5864d32cc897a03015634142b5965048` MATCH;
`tests/orchestration/test_self_use_runner.py` bytes=18703
sha256=`0ab919d4298d65bdf0b3603d0b358b5b778b0f60212677b5f81596d3cd203491` MATCH;
`docs/README.md` bytes=18552
sha256=`c828e72ee745d6abadfc32b3f9365c79f56aeda9c5c7dbae5b37e98f5c071b67` MATCH.
No digest differed, so no `git diff --no-index` stop was needed.

G4 THE TESTS — the ordered pytest selection, run SERIALLY (real exit code
0): `649 passed in 163.60s (0:02:43)`. The reviewer ran the same selection
WITHOUT `tests/cli/test_golden_path.py` inside a disposable worktree
carrying C2 and C3 and read `605 passed, 2 skipped` at exit 0; this round
ran the full selection INCLUDING golden path in the primary checkout, which
carries the UI toolchain a worktree lacks (as the block anticipates),
accounting for the different pass/skip counts. `python3 -m ruff check`
over the Python paths C3 lists (`packages/orchestration/self_use_generator.py
tests/orchestration/test_self_use_generator.py
tests/orchestration/test_self_use_runner.py
tests/docs/test_toolchain_refresh_order.py`) → `All checks passed!`, real
exit 0. `python3 -m apps.cli.main integrity check --json` → all 5 checks
`pass` (`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `high_blockers_open`), `fail_count` 0, real exit 0.
`python3 -m apps.cli.main integrity block .remedy-wt/f279-r7-block.md` →
all 7 items OK (1 size, 3 cap-bounded replacements, 10 open set recomputed,
24 gate paths resolve, 30 new ids searched first, 31 gates before the text,
37 no unmeasured runs), `All 7 checkable items pass.`, real exit 0 —
matching the reviewer's own pre-emission run of this block exactly.

G5 THE RED PROOFS — `git worktree add --detach .remedy-wt/f279-r7-mut
3a4ea6fc` real exit 0. `python3 -B .remedy-wt/f279-r7-payloads/mutations.py
.remedy-wt/f279-r7-mut` real exit 0, full output:
```
control_before REAL_EXIT=0
42 passed in 0.33s
m1_no_cadence FROM count in packages/orchestration/self_use_generator.py: 1
m1_no_cadence REAL_EXIT=1
FAILED tests/orchestration/test_self_use_generator.py::TestOrderTier::test_within_fourteen_days_the_ledger_tier_answers_instead
1 failed, 41 passed in 0.35s
m1_no_cadence restored byte-identical: True
m2_the_order_tier_never_answers FROM count in packages/orchestration/self_use_generator.py: 1
m2_the_order_tier_never_answers REAL_EXIT=1
FAILED tests/orchestration/test_self_use_generator.py::TestOrderTier::test_the_real_order_file_is_a_job_the_tier_accepts
FAILED tests/orchestration/test_self_use_generator.py::TestOrderTier::test_an_order_never_queued_comes_before_the_ledger
FAILED tests/orchestration/test_self_use_generator.py::TestOrderTier::test_after_fourteen_days_the_order_is_due_again
3 failed, 39 passed in 0.38s
m2_the_order_tier_never_answers restored byte-identical: True
m3_any_file_is_taken_as_a_job FROM count in packages/orchestration/self_use_generator.py: 1
m3_any_file_is_taken_as_a_job REAL_EXIT=1
FAILED tests/orchestration/test_self_use_generator.py::TestOrderTier::test_an_order_file_that_is_not_a_job_is_refused
1 failed, 41 passed in 0.34s
m3_any_file_is_taken_as_a_job restored byte-identical: True
m4_an_order_heading_reworded FROM count in docs/orders/toolchain-refresh.md: 1
m4_an_order_heading_reworded REAL_EXIT=1
FAILED tests/docs/test_toolchain_refresh_order.py::test_the_order_carries_exactly_the_pinned_headings_in_order
1 failed, 41 passed in 0.33s
m4_an_order_heading_reworded restored byte-identical: True
control_after REAL_EXIT=0
42 passed in 0.33s
```
Every reading matches the reviewer's stated expectations exactly:
control_before/control_after 42 passed; m1 1 failed at
`TestOrderTier::test_within_fourteen_days_the_ledger_tier_answers_instead`;
m2 3 failed at `TestOrderTier::test_the_real_order_file_is_a_job_the_tier_accepts`,
`TestOrderTier::test_an_order_never_queued_comes_before_the_ledger` and
`TestOrderTier::test_after_fourteen_days_the_order_is_due_again`; m3 1
failed at `TestOrderTier::test_an_order_file_that_is_not_a_job_is_refused`;
m4 1 failed at `test_the_order_carries_exactly_the_pinned_headings_in_order`.
`git worktree remove --force .remedy-wt/f279-r7-mut` real exit 0, `git
worktree prune` real exit 0. `git worktree list` afterward → primary
checkout plus the two `.remedy-wt/job-*` worktrees only.

## Authored-text proofs

Fidelity protocol (docs/agents/split_workflow.md, R-0147/R-0144/R-0148):
byte-identity proof = mechanical disk-to-disk comparison of the applied
location against the `.agent/authored/` copy.

- This block (`f279-r7-block.md`): `.agent/authored/f279-r7-block.md` at
  C1a verified byte-identical to `.remedy-wt/f279-r7-block.md` (G1) and to
  the two readings given in the delegation message.
- All 7 product payloads (toolchain-refresh.md, test_toolchain_refresh_order.py,
  self_use_generator.diff, test_self_use_generator.diff,
  test_self_use_runner.diff, docs_index.diff, mutations.py) plus the 3
  bookkeeping payloads (ledger.diff, plan.md, decisions.diff) — 10 total:
  each `.agent/authored/f279-r7-<name>` copy verified byte-identical to its
  `.remedy-wt/f279-r7-payloads/<name>` source (G1).
- Every `.diff` payload applied by `git apply` (never retyped): ledger,
  decisions (at C2), self_use_generator, test_self_use_generator,
  test_self_use_runner, docs_index (at C3) — all 6, `git apply --check`
  then `git apply`, real exit 0 both times, and the resulting tracked-file
  digests MATCH the reviewer's stated readings exactly at G2/G3.
- `plan.md` (rewrite, never retyped) and `toolchain-refresh.md`/
  `test_toolchain_refresh_order.py` (new files, never retyped): all three
  by `shutil.copyfile` from their payloads; the resulting on-disk digests
  MATCH the reviewer's stated G2/G3 readings exactly.

## Item-Status Table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 306 insertions, matches 222+84 formula |
| C1b | done | 464 insertions, matches expectation |
| C2 | done | round 6's PASS booked, DECISION F279 D7 recorded, all three insertion counts match |
| C3 | done | order, its tier and their tests landed, all six counts match |
| C4 | done | this handback |
| G1 TRANSPORT | done | all 11 authored copies byte-identical to source |
| G2 THE BOOKKEEPING | done | all 3 digests match, 26/26 open-finding set empty diff, 0/1 Gate-line count matches, file-list matches |
| G3 THE ORDER | done | file-list and all 6 digests match, no stop needed |
| G4 THE TESTS | done | 649 passed exit 0, ruff clean exit 0, integrity check 5/5 pass exit 0, integrity block 7/7 OK exit 0 |
| G5 THE RED PROOFS | done | control/m1-m4/control_after all match reviewer's exact readings, worktree cleaned up |
| G6 TREE AND PUSH | done | reported in the session's final reply, not this file, since it runs after C4 |

## Deviations & assumptions

The round followed the block's ordered commit sequence (C1a, C1b, C2, C3,
C4) exactly and touched exactly the tracked path set constraint 3 names —
confirmed by `git diff --name-only 564b54e3 HEAD` before C4 was written.

No oversize commit this round (largest was C1b's 464 insertions, well under
the 500 cap; F279's one declared oversize commit remains round 1's C5).

No sandbox friction beyond the block's own anticipated shapes: every
measurement script was written to a file under
`.remedy-wt/f279-r7-scratch/` and run with `python3 <file>` or `bash -c`,
never as an inline heredoc or `VAR=x cmd` shape; no payload was retyped or
edited.

No other procedural deviation. Nothing was merged this round, per
constraint 5. No `remedy/job-*` branch or self-use worktree was created,
touched or deleted beyond the round's own `.remedy-wt/f279-r7-mut`, which
was created and removed within G5 per constraint 6. The full suite was not
run, per constraint 7 (amend0917 rule 1) — F279's one full-suite run
belongs to its closure.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round 7,
then F279's closure sequence per `docs/roadmap/STATUS_closure_protocol.md`.
Open findings: 26. Operator questions: 0.
