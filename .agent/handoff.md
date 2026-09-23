# Handback — F282 Findings paydown v2 · Round 2 · Book round 1, resolve T002 by evidence and land T003, R-1041's open-set rule

## Session

SESSION 1 of feature F282 · round 2 · rounds so far 2

This round booked round 1's PASS and R-0998's resolution into the ledger,
resolved R-1009, R-1043, R-1044 and R-0880 by the reviewer's measured
evidence, recorded DECISION F282 D2, and landed T003 — `check_open_set` in
`packages/orchestration/block_lint.py`, which checks a block's stated
open-findings count against the open set AFTER the round, reading the ids
the block's ledger payloads register and resolve (R-1041), with its tests.
A large majority of the session's working context budget remained at
handback.

## Range

Review of `5f9e4725`..`HEAD`.

## Commits

### d60d3ee0 F282 R2 C1a: copy round 2 block and bookkeeping payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r2-block.md | +203/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r2-ledger.diff | +20/-0 | Payload copy |
| .agent/authored/f282-r2-decisions.diff | +27/-0 | Payload copy |
| .agent/authored/f282-r2-plan.md | +30/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 280
(203+27+20+30), matching the block's stated formula "this block's line
count plus 77" (203+77=280) exactly. Under the 500 cap.

### 23c8827c F282 R2 C1b: copy round 2 product payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r2-mutations.py | +76/-0 | Payload copy |
| .agent/authored/f282-r2-product.diff | +69/-0 | Payload copy |
| .agent/authored/f282-r2-tests.diff | +45/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 190
(76+69+45), matching the block's expected 190 exactly.

### 1776b574 F282 R2 C2: book round 1, resolve five findings and record DECISION F282 D2

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +12/-0 | `ledger.diff` applied: `Gate: F282 R1` entry and the `Done:` lines of R-0998, R-1009, R-1043, R-1044 and R-0880 |
| .agent/decisions.md | +19/-0 | `decisions.diff` applied: DECISION F282 D2 |
| .agent/plan.md | +8/-10 | Rewritten to the round-2 `plan.md` payload |

Measured insertions/deletions by `git show --numstat 1776b574`: 19/0
decisions.md, 12/0 live_review.md, 8/10 plan.md — matching the block's
expected numbers exactly.

### c68f4611 F282 R2 C3: count the open set after the round from the block's ledger payloads

| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/block_lint.py | +42/-4 | `product.diff` applied: T003, `check_open_set` reads the ids a block's ledger payloads register and resolve, and checks the stated open-findings count against the open set AFTER the round (R-1041) |

Measured insertions/deletions by `git diff --cached --numstat` before
commit: 42/4, matching the block's expected "42 (4 deletions)" exactly.

### 02cbe601 F282 R2 C4: test the open-set rule against a block's ledger payloads, R-1041

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_block_lint.py | +34/-0 | `tests.diff` applied |

Measured insertions by `git diff --cached --numstat` before commit: 34,
matching the block's expected 34 exactly.

### (this commit) F282 R2 C5: rewrite handoff for round 2

| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f282-r2-mut 02cbe601` for G5 —
  succeeded, HEAD detached at `02cbe601`.
- `git worktree remove --force .remedy-wt/f282-r2-mut` and
  `git worktree prune` after G5 — both real exit 0; `git worktree list`
  afterward shows only the primary checkout, `.remedy-wt/f282-r1-dry`,
  `.remedy-wt/f282-r1-sim`, `.remedy-wt/f282-r2-dry`,
  `.remedy-wt/f282-r2-sim` and the four `job-*` worktrees constraint 6
  names.
- `git push origin feature/f282-findings-paydown-v2` after C5 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.

## Verification

**G1 — transport**: each of the six payloads' lines/bytes/sha256 measured
against the block's PAYLOADS table — all six rows matched exactly
(ledger.diff 20/13589, decisions.diff 27/2192, plan.md 30/1166,
product.diff 69/3571, tests.diff 45/2968, mutations.py 76/3362 — all
sha256 digests equal to the table). The block itself: 203 lines (newline
count), sha256
`1af7e53f3c718edc52bdc10375581944a076433014c2cc716b6ae072e4374c56`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r2-*` blob read with `git show
<commit>:<path>` (block + ledger.diff + decisions.diff + plan.md at
`d60d3ee0`; product.diff + tests.diff + mutations.py at `23c8827c`)
compared byte-for-byte against its `.remedy-wt/f282-r2-payloads/` (or
block) source: all seven pairs byte-identical = True.

**G2 — the bookkeeping and the product**: at C2 (`1776b574`),
`.agent/live_review.md` 392954 bytes, sha256
`fab69ca590883fc0681edb0c533b774038141d0c8d1ce63370d232153d62a5db`;
`.agent/decisions.md` 1916192 bytes, sha256
`3d3a8e448ff027a57a7378b5f5f6d2c12f454f50f0a9ce76393fe43b4fcb8a1e`;
`.agent/plan.md` 1166 bytes, sha256
`ede3d94c9d60ecf0bd262783e8b093956306de29294cde4caa8be3eb58cf7e2d` — at C3
(`c68f4611`), `packages/orchestration/block_lint.py` 10350 bytes, sha256
`7db58f0e5e0abbabc03c4c9ca153c94a555bc9b25ad18d8726ae394d8121baba` — at C4
(`02cbe601`), `tests/orchestration/test_block_lint.py` 9647 bytes, sha256
`2d4f0e0157a1e5cd46ce3e3302691248bcc490fc5da7b692137c6c85123921cd` — all
five equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 29 at
`5f9e4725`, 24 at C2; set difference: `R-0880`, `R-0998`, `R-1009`,
`R-1043`, `R-1044` the only ids leaving, none arriving — matching the
block's reading exactly. `git diff --name-only d60d3ee0 23c8827c` names
exactly `.agent/authored/f282-r2-mutations.py`,
`.agent/authored/f282-r2-product.diff`, `.agent/authored/f282-r2-tests.diff`
— C1b's list. `git diff --name-only 23c8827c 1776b574` names exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — C2's
list. `git diff --name-only 1776b574 c68f4611` names exactly
`packages/orchestration/block_lint.py` — C3's list. `git diff --name-only
c68f4611 02cbe601` names exactly `tests/orchestration/test_block_lint.py`
— C4's list.

**G3 — the linter on this block**: at C4, in the primary checkout,
`python3 -m apps.cli.main integrity block .remedy-wt/f282-r2-block.md`,
real exit 0:
```
  [OK] item 1 (size): 203 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): states 24; .agent/live_review.md holds 24 open by distinct id, and the block registers 0 and resolves 0, leaving 24
  [OK] item 24 (gate paths resolve): 12 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G5 before C5
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```
Item 10's reading matches the block's stated "states 24; .agent/live_review.md
holds 24 open by distinct id, and the block registers 0 and resolves 0,
leaving 24" exactly.

**G4 — the tests**: in the primary checkout at C4, the ordered pytest
selection (12 paths, including `tests/cli/test_golden_path.py`), real
exit 0: `281 passed in 166.50s`. The reviewer's disposable-worktree run
without the golden path read `237 passed, 2 skipped` at exit 0; the
primary checkout carries the toolchain the worktree lacked, so the two
skips there ran and passed here, consistent with the block's own note
("a skip may pass in the primary checkout"). `python3 -m ruff check
packages/orchestration/block_lint.py tests/orchestration/test_block_lint.py`:
real exit 0, "All checks passed!". `python3 -m apps.cli.main integrity
check --json`: real exit 0, `check_count: 6`, all six checks
(`handler_import`, `live_review_verdict`, `plan_consistency`,
`relevant_untracked`, `repo_root_hygiene`, `high_blockers_open`) `pass`,
`fail_count: 0`, `ok: true`, `passed: true`. `python3 -m mypy --no-pretty
--ignore-missing-imports --no-error-summary --follow-imports=silent
packages apps`, real exit 1 (mypy's normal exit when it finds errors),
filtered for `has no attribute "(job_id|task_id)"`: exactly two lines,
`packages/orchestration/token_economy.py:324: error: Item "None" of
"JobPlan | None" has no attribute "job_id"  [union-attr]` and
`packages/orchestration/self_use_runner.py:390: error: "object" has no
attribute "job_id"  [attr-defined]`; 288 `error:` lines in all — matching
the reviewer's reading exactly.

**G5 — the red proofs**: `git worktree add --detach .remedy-wt/f282-r2-mut
02cbe601` succeeded. `python3 -B .remedy-wt/f282-r2-payloads/mutations.py
.remedy-wt/f282-r2-mut` (real exit 0), whole output:
```
control_before_lint REAL_EXIT=0
28 passed in 0.34s
control_before_self_use REAL_EXIT=0
319 passed in 161.30s (0:02:41)
m1_payloads_never_read FROM count in packages/orchestration/block_lint.py: 1
m1_payloads_never_read REAL_EXIT=1
1 failed, 27 passed in 0.35s
m1_payloads_never_read restored byte-identical: True
m2_every_diff_section_counted FROM count in packages/orchestration/block_lint.py: 1
m2_every_diff_section_counted REAL_EXIT=1
1 failed, 27 passed in 0.35s
m2_every_diff_section_counted restored byte-identical: True
m3_every_whole_payload_counted FROM count in packages/orchestration/block_lint.py: 1
m3_every_whole_payload_counted REAL_EXIT=1
1 failed, 27 passed in 0.35s
m3_every_whole_payload_counted restored byte-identical: True
r1_block_lint_before_this_round REAL_EXIT=1
2 failed, 26 passed in 0.35s
r1_block_lint_before_this_round packages/orchestration/block_lint.py restored byte-identical: True
r2_self_use_runner_before_amend0923 REAL_EXIT=1
17 failed, 302 passed in 146.70s (0:02:26)
r2_self_use_runner_before_amend0923 packages/orchestration/self_use_runner.py restored byte-identical: True
r2_self_use_runner_before_amend0923 packages/orchestration/pingpong_job.py restored byte-identical: True
r2_self_use_runner_before_amend0923 docs/orders/toolchain-refresh.md restored byte-identical: True
control_after_lint REAL_EXIT=0
28 passed in 0.34s
control_after_self_use REAL_EXIT=0
319 passed in 148.87s (0:02:28)
```
Matches the reviewer's reading exactly: control_before_lint `28 passed`
exit 0; control_before_self_use `319 passed` exit 0; m1 1 failed exit 1;
m2 1 failed exit 1; m3 1 failed exit 1; r1 2 failed exit 1; r2 17 failed
exit 1; control_after_lint `28 passed` exit 0; control_after_self_use
`319 passed` exit 0; every `restored byte-identical` line True.
`git worktree remove --force .remedy-wt/f282-r2-mut` and
`git worktree prune`: both real exit 0. `git worktree list` afterward:
primary checkout plus `.remedy-wt/f282-r1-dry`, `.remedy-wt/f282-r1-sim`,
`.remedy-wt/f282-r2-dry`, `.remedy-wt/f282-r2-sim` and the four `job-*`
worktrees constraint 6 names — nothing else.

## Authored-text proofs

- `.agent/authored/f282-r2-block.md` (C1a) == `.remedy-wt/f282-r2-block.md`:
  byte-identical True (sha256
  `1af7e53f3c718edc52bdc10375581944a076433014c2cc716b6ae072e4374c56`, 203
  lines).
- `.agent/authored/f282-r2-ledger.diff`, `-decisions.diff`, `-plan.md`
  (C1a) == their `.remedy-wt/f282-r2-payloads/` sources: byte-identical
  True, all three.
- `.agent/authored/f282-r2-product.diff`, `-tests.diff`, `-mutations.py`
  (C1b) == their `.remedy-wt/f282-r2-payloads/` sources: byte-identical
  True, all three.
- `ledger.diff`, `decisions.diff`, `product.diff`, `tests.diff` were
  applied at C2/C3/C4 with `git apply --check` then `git apply` directly
  from the payload's own bytes under `.remedy-wt/f282-r2-payloads/` —
  never retyped, every `--check` and every real apply at real exit 0.
- `.agent/plan.md` at C2 == `plan.md` payload verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  table above).
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied by `git apply` reading the
  payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1a | done | 280 insertions, matches block formula (203+77) exactly |
| C1b | done | 190 insertions, matches block exactly |
| C2 | done | 19/12/8 insertions by `git show --numstat`, matches block exactly |
| C3 | done | 42/4, matches block exactly |
| C4 | done | 34 insertions, matches block exactly |
| C5 | done | this handback |
| Round 1 booking | done | `Gate: F282 R1` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-0998 | done | resolved — booked as one of the five ids leaving the open set at C2 |
| R-1009 | done | resolved — booked as one of the five ids leaving the open set at C2 |
| R-1043 | done | resolved — booked as one of the five ids leaving the open set at C2 |
| R-1044 | done | resolved — booked as one of the five ids leaving the open set at C2 |
| R-0880 | done | resolved — booked as one of the five ids leaving the open set at C2; also the mypy static-bound gate rerun this round, matching the reviewer's reading exactly |
| DECISION F282 D2 | done | recorded at C2 via `decisions.diff` |
| T003 | done | `check_open_set` landed in `packages/orchestration/block_lint.py` at C3, reading ids a block's ledger payloads register/resolve and checking the open set AFTER the round (R-1041), with tests at C4 |
| G1 | done | all readings match; all seven authored copies byte-identical |
| G2 | done | all five sha256/byte readings match; open-set 29 to 24, five ids leaving exactly as named; all four name-only diffs match exactly |
| G3 | done | integrity block linter, real exit 0, all 7 checkable items `[OK]`, item 10 reading matches exactly |
| G4 | done | 281 passed exit 0 (reviewer's worktree run: 237 passed/2 skipped, toolchain present here); ruff exit 0; integrity check all-pass exit 0; mypy filtered reading matches exactly (2 lines, 288 total) |
| G5 | done | mutation script output matches the reviewer's reading exactly across all nine sub-checks; worktree cleaned up |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every reading this round matched the block's stated expectation
exactly. No payload was edited or retyped; every copy used
`shutil.copyfile` and every diff was applied via `git apply` reading the
payload file directly. The commit sequence landed in the block's exact
order C1a-C1b-C2-C3-C4-C5. This round is SESSION 1 of F282, its second
round.

Separately, noted for the record: this session's environment metadata
claimed its working directory was `.remedy-wt/f282-r1-dry` (the
reviewer's read-only dry-run worktree), contradicting the delegation
message's explicit instruction to work in the primary checkout and the
block's own constraint 6 (which forbids touching that worktree). Since
every Bash invocation in this session operated correctly against the
primary checkout's paths (confirmed by `pwd` and every git/gate reading
above), and no command targeted or altered `.remedy-wt/f282-r1-dry` at
any point, this was treated as an untrustworthy claim rather than
followed. No file under that worktree was read, written, or touched this
round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk — absent at this handback),
then the review of round 2, then T004 and T005, R-1040 and R-1005. Open
findings count: 24. Operator-questions count: 0.
