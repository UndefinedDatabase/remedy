# Handback — F282 Findings paydown v2 · Round 11 · The closure suite's first repair round: book round 10, give each packer run its own stamp, run the suite again

## Session

SESSION 2 of feature F282 · round 11 · rounds so far 11

This round booked round 10's PASS and the resolutions of R-0662, R-0819
and R-0820 into the ledger, recorded DECISION F282 D11, repaired the
closure suite's one bad node
(`tests/orchestration/test_review_zip_hygiene.py::TestThePackerRefusesRootLeftovers::test_the_packages_own_output_directory_is_not_its_own_detritus`)
by giving each of its two packer runs its own archive stamp through a
`date` shim on PATH, and ran the full suite again. The suite read GREEN:
18772 passed, 20 skipped, exit code 0 — the previously-bad node is gone
and no node is newly bad, satisfying amend0917-throughput rule 2's
shrinking requirement on the first of at most three allowed repair
rounds. Roughly three-quarters of this session's working-context budget
remained at handback.

## Range

Review of `720e15e6`..`HEAD`.

## Commits

### 0103e863 F282 R11 C1: copy round 11 block and payloads into .agent/authored/

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-r11-block.md | +187/-0 | Bookkeeping copy of this round's step block (R-0954 transport) |
| .agent/authored/f282-r11-decisions.diff | +30/-0 | Payload copy |
| .agent/authored/f282-r11-ledger.diff | +16/-0 | Payload copy |
| .agent/authored/f282-r11-mutations.py | +44/-0 | Payload copy |
| .agent/authored/f282-r11-plan.md | +30/-0 | Payload copy |
| .agent/authored/f282-r11-product.diff | +53/-0 | Payload copy |

Measured insertions by `git diff --cached --stat` before commit: 360
(187+173), matching the block's stated formula "this block's line count
plus 173" exactly. Under the 500 cap.

### 4908ee9b F282 R11 C2: book round 10, resolve R-0662, R-0819 and R-0820 and record DECISION F282 D11

| Path | +/- | Reason |
|---|---|---|
| .agent/live_review.md | +8/-0 | `ledger.diff` applied: the `Gate: F282 R10` entry and the `Done:` lines of R-0662, R-0819 and R-0820 |
| .agent/decisions.md | +22/-0 | `decisions.diff` applied: DECISION F282 D11 (the one-second archive-name collision, its cause, the chosen repair and the rejected alternative) |
| .agent/plan.md | +7/-9 | Rewritten to the round-11 `plan.md` payload (via `shutil.copyfile`) |

Measured insertions/deletions by `git diff --numstat` before commit:
22/0 decisions.md, 8/0 live_review.md, 7/9 plan.md — matching the
block's expected numbers exactly.

### 65f05744 F282 R11 C3: give each packer run of the output-directory test its own archive stamp

| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_review_zip_hygiene.py | +24/-14 | `product.diff` applied: `test_the_packages_own_output_directory_is_not_its_own_detritus` now runs each of its two packer invocations under its own `date` shim on PATH, so the two archive names never collide inside one wall-clock second |

Measured insertions/deletions by `git diff --numstat` before commit:
24/14 — matching the block's expected numbers exactly.

### (this commit) F282 R11 C4: record the repaired closure suite and rewrite handoff for round 11

| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f282-closure-suite.txt | rewritten whole | The full suite's summary line, real exit code and full bad-node-id list (now `NONE`) |
| .agent/handoff.md | rewritten | This handback, per `docs/agents/handback_template.md` — a handback cannot table the commit that writes it (R-0149 self-reference exception) |

## External actions

- `git worktree add --detach .remedy-wt/f282-r11-mut 65f05744` for G4 —
  real exit 0.
- `git worktree remove --force .remedy-wt/f282-r11-mut` then
  `git worktree prune` after G4 — both real exit 0;
  `git worktree list` afterward shows the primary checkout and exactly
  the worktrees constraint 6 names (`f282-r11-dry`, `f282-r11-sim`, and
  the four `job-*` worktrees), no leftover.
- `git push origin feature/f282-findings-paydown-v2` after C4 — real
  outcome reported in the worker's final reply (G6 readings, per the
  block, do not live in this committed file).
- No `gh pr create`, no `gh pr merge`, no checkout of `main`, no branch
  deletion, no force-push, no `git stash` in any form.

## Verification

**G1 — transport**: each of the five payloads' lines/bytes/sha256
measured against the block's PAYLOADS table — all five rows matched
exactly (ledger.diff 16/6694, decisions.diff 30/2503, plan.md 30/1148,
product.diff 53/2880, mutations.py 44/1951 — all sha256 digests equal to
the table). The block itself: 187 lines (newline count), sha256
`8623024b604e2e2c184ebf4dfe0144688aa50dc5124d14626eaf0c7fc5bc2984`,
matching the delegation message's two stated readings exactly (R-0954).
Every committed `.agent/authored/f282-r11-*` blob read with `git show
0103e863:<path>` compared byte-for-byte against its
`.remedy-wt/f282-r11-payloads/` (or block) source: all six pairs
byte-identical = True.

**G2 — the bookkeeping and the repair**: at C2 (`4908ee9b`),
`.agent/live_review.md` 434178 bytes, sha256
`dd09d9ddef4080eecd6a09c8a59888b1997303da83b89e5868d4bf732ce4e298`;
`.agent/decisions.md` 1936565 bytes, sha256
`1b5be316ad586800aa90266bb847dea7421b6ff9a3d7995bd5635c84fae6f745`;
`.agent/plan.md` 1148 bytes, sha256
`8d267f9997a0b582873f9ffca770e8ea977376602aad1cb457f0960d874d3802` — at
C3 (`65f05744`), `tests/orchestration/test_review_zip_hygiene.py` 52845
bytes, sha256
`f7f90cc4a4f26b7ee25eeb2518e2516607e738cd3fe0f20d5d99c6fd1d19c14c` — all
four equal to the block's table exactly. Open finding ids via
`scripts/rotate_live_review.py`'s `open_finding_ids(text)`: 6 at
`720e15e6`, 3 at C2 (`4908ee9b`); set difference: `R-0662`, `R-0819` and
`R-0820` the ids leaving, none arriving — matching the block's reading
exactly. `git diff --name-only 0103e863 4908ee9b` names exactly
`.agent/decisions.md`, `.agent/live_review.md`, `.agent/plan.md` — C2's
list. `git diff --name-only 4908ee9b 65f05744` names exactly
`tests/orchestration/test_review_zip_hygiene.py` — C3's list.

**G3 — the linter on this block and the tests**: at C3, in the primary
checkout, `python3 -m apps.cli.main integrity block
.remedy-wt/f282-r11-block.md`, real exit 0:
```
  [OK] item 1 (size): 187 lines, limit 400
  [OK] item 3 (cap-bounded replacements): plan.md at 30 lines
  [OK] item 10 (open set recomputed): states 3; .agent/live_review.md holds 3 open by distinct id, and the block registers 0 and resolves 0, leaving 3
  [OK] item 24 (gate paths resolve): 6 paths named in the block's commands, every one resolves
  [OK] item 30 (new ids searched first): the block registers no finding id
  [OK] item 31 (gates before the text): G1 to G4 before C4
  [OK] item 37 (no unmeasured runs): no line is a run of one repeated character
All 7 checkable items pass.
```
Then the ordered pytest selection (6 paths), real exit 0:
```
481 passed in 95.55s (0:01:35)
```
matching the reviewer's simulation reading of `481 passed` at exit 0
exactly. Then `python3 -m ruff check
tests/orchestration/test_review_zip_hygiene.py`: real exit 0, "All
checks passed!". Then `python3 -m apps.cli.main integrity check --json`:
real exit 0, `check_count: 6`, all six checks (`handler_import`,
`live_review_verdict`, `plan_consistency`, `relevant_untracked`,
`repo_root_hygiene`, `high_blockers_open`) `pass`, `fail_count: 0`,
`ok: true`, `passed: true`.

**G4 — the red proofs**: `git worktree add --detach
.remedy-wt/f282-r11-mut 65f05744`, real exit 0. Then `python3 -B
.remedy-wt/f282-r11-payloads/mutations.py .remedy-wt/f282-r11-mut`:
```
control_before REAL_EXIT=0
1 passed in 2.17s
m1_both_runs_read_one_second FROM count in tests/orchestration/test_review_zip_hygiene.py: 1
m1_both_runs_read_one_second REAL_EXIT=1
FAILED tests/orchestration/test_review_zip_hygiene.py::TestThePackerRefusesRootLeftovers::test_the_packages_own_output_directory_is_not_its_own_detritus
1 failed in 1.95s
m1_both_runs_read_one_second restored byte-identical: True
m2_the_shim_is_not_on_path FROM count in tests/orchestration/test_review_zip_hygiene.py: 1
m2_the_shim_is_not_on_path REAL_EXIT=1
FAILED tests/orchestration/test_review_zip_hygiene.py::TestThePackerRefusesRootLeftovers::test_the_packages_own_output_directory_is_not_its_own_detritus
1 failed in 1.37s
m2_the_shim_is_not_on_path restored byte-identical: True
control_after REAL_EXIT=0
1 passed in 2.17s
```
matching the reviewer's readings exactly: control_before `1 passed` at
exit 0, m1 1 failed at exit 1, m2 1 failed at exit 1, control_after
`1 passed` at exit 0, every restore byte-identical True. Then `git
worktree remove --force .remedy-wt/f282-r11-mut`, real exit 0; `git
worktree prune`, real exit 0; `git worktree list` afterward shows the
primary checkout plus exactly the worktrees constraint 6 names, no
`f282-r11-mut` remaining.

**G5 — the suite again**: `python3 -m pytest -n auto -q`, real exit 0:
```
18772 passed, 20 skipped, 1 warning in 359.16s (0:05:59)
```
Bad node ids: `NONE` — `grep -c ^FAILED` over the log = 0, `grep -c
^ERROR` = 0. Round 10's one bad node,
`tests/orchestration/test_review_zip_hygiene.py::TestThePackerRefusesRootLeftovers::test_the_packages_own_output_directory_is_not_its_own_detritus`,
is ABSENT from this run (it now passes), and no node is newly bad — the
shrinking rule holds. All readings written verbatim to
`.agent/authored/f282-closure-suite.txt`, committed in this C4.

## Authored-text proofs

- `.agent/authored/f282-r11-block.md` (C1) ==
  `.remedy-wt/f282-r11-block.md`: byte-identical True (sha256
  `8623024b604e2e2c184ebf4dfe0144688aa50dc5124d14626eaf0c7fc5bc2984`,
  187 lines).
- `.agent/authored/f282-r11-ledger.diff`, `-decisions.diff`, `-plan.md`,
  `-product.diff`, `-mutations.py` (C1) == their
  `.remedy-wt/f282-r11-payloads/` sources: byte-identical True, all
  five.
- `ledger.diff`, `decisions.diff`, `product.diff` were applied at
  C2/C3 with `git apply --check` then `git apply` directly from the
  payload's own bytes under `.remedy-wt/f282-r11-payloads/` — never
  retyped, every `--check` and every real apply at real exit 0.
- `.agent/plan.md` at C2 == its payload source verbatim (rewrite by
  `shutil.copyfile`): byte-identical True (confirmed by the G2 sha256
  reading above and by the payload table reading for plan.md).
- `mutations.py` was run, never applied, per the block's own
  description of it as a TOOL for G4.
- No payload was edited or retyped anywhere this round; every copy used
  `shutil.copyfile` and every diff was applied by `git apply` reading
  the payload file directly.

## Item-status table

| Item | Status | Reason |
|---|---|---|
| C1 | done | 360 insertions, matches block formula (187+173) exactly |
| C2 | done | 22/0, 8/0, 7/9 insertions/deletions by `git diff --numstat`, matches block exactly |
| C3 | done | 24/14, matches block exactly |
| C4 | done | this handback; repaired suite transcript committed |
| Round 10 booking | done | `Gate: F282 R10` entry appended to `.agent/live_review.md` via `ledger.diff` |
| R-0662 | done | resolved — booked as one of the three ids leaving the open set at C2 |
| R-0819 | done | resolved — booked as one of the three ids leaving the open set at C2 |
| R-0820 | done | resolved — booked as one of the three ids leaving the open set at C2 |
| DECISION F282 D11 | done | recorded at C2 via `decisions.diff` |
| The repair | done | `test_the_packages_own_output_directory_is_not_its_own_detritus` gives each packer run its own archive stamp via a `date` shim on PATH, applied at C3 |
| Full suite (C4) | done (GREEN) | 18772 passed, 20 skipped, exit 0 — the repaired node absent, no node newly bad, shrinking rule satisfied |
| G1 | done | all readings match; all six authored copies byte-identical |
| G2 | done | all four sha256/byte readings match; open-set 6 to 3, R-0662/R-0819/R-0820 leaving exactly as named; both name-only diffs match exactly |
| G3 | done | integrity block linter real exit 0 all 7 items `[OK]`; targeted selection 481 passed exit 0; ruff exit 0; integrity check all-pass exit 0 |
| G4 | done | control_before/control_after 1 passed exit 0; m1/m2 each 1 failed exit 1; every restore byte-identical True; mut worktree removed and pruned |
| G5 | done | full suite 18772 passed, 20 skipped, exit 0; bad node ids NONE |
| G6 | done | readings reported in the final reply only, per the block |
| Push | done | reported in the final reply only, per the block |

## Deviations & assumptions

None. Every measured number matched the block's stated expectation
exactly, and the commit sequence landed in the block's exact order
C1-C2-C3-C4. The full suite in C4 read GREEN, so the block's constraint
4 exception for a red suite was not needed. No payload was edited or
retyped; every copy used `shutil.copyfile` and every diff was applied
via `git apply` reading the payload file directly. This round is SESSION
2 of F282, its eleventh round.

## Next

Phase 1 rule 1 (read `.agent/STOP` from disk), then the review of round
11, then the evidence job and the review package, then the closing
round. Open findings count: 3. Operator-questions count: 0.
