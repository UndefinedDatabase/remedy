# Handback — F082 R6 (record R5, retire the stale context, close T001)

READ THIS FIRST, next session. The FIRST action is
docs/agents/self_drive_protocol.md Phase 1 rule 1 — re-read `.agent/STOP` from
disk — BEFORE rule 2's Open PR Gate. Phase 0 runs once; G6 binds at any point;
the sentinel is re-read every round (R-0347), never carried over from this
reading. F082 is MID-FEATURE. No PR exists for `feature/f082-self-benchmark`
and none is created until closure; gate 17 proves `gh pr list --state open` is
`[]`. The next round is R7 — T002.

Deviations, declared: this handoff is 129 lines against the 60-line cap, under
DECISION D15 stated cause — five per-commit tables, the 18-gate verification
table, the eight authored-text proofs and the item-status table. No section
dropped, no prose padding.

## Range
Review of d0b2152d..HEAD (branch feature/f082-self-benchmark).

## Commits
### 593e07f5 chore(f082): save the R6 block verbatim
| Path | +/- | Reason |
| `.agent/authored/f082-r6.md` | +325/-0 | C0a, block saved byte-for-byte |

### 1b0f4134 chore(f082): mirror the R6 block into last_block
| Path | +/- | Reason |
| `.agent/last_block.md` | +257/-153 | C0b, mirrored from the COMMITTED authored file |

### 819b4cea docs(f082): record the R5 verdict and register R-0412 and R-0413
| Path | +/- | Reason |
| `.agent/live_review.md` | +6/-0 | C1, R412, R413 then GATE-R5, append only, FIRST after C0 |

### bf008d9d docs(f082): retire the superseded context regions and re-sync plan
| Path | +/- | Reason |
| `.agent/context.md` | +8/-7 | C2a CTXSTILL and C2b CTXSTEPS rewrite pairs |
| `.agent/plan.md` | +8/-10 | C2c, full replacement with the PLAN slice |

### c3799b97 feat(f082): add the bench dry run over recorded evidence
| Path | +/- | Reason |
| `packages/orchestration/bench_dry_run.py` | +137/-0 | C3, NEW, order file to row over recorded evidence |
| `tests/orchestration/test_bench_dry_run.py` | +126/-0 | C3, NEW, 5 tests, the block's five cases |

C4 (this handoff) is not tabled above: a handoff cannot table the commit that
writes it (R-0149 pattern). It changes `.agent/handoff.md` alone.

## External actions
- `git push origin feature/f082-self-benchmark` after each of the five commits
  above — all succeeded. No force, no merge, no history rewrite, no branch
  deleted, no work on main.
- `gh pr list --state open --json number,headRefName,baseRefName,isDraft` at
  round start and `--json number,headRefName` at gate 17 — exit 0, `[]` both.
  No PR created, edited or merged.
- `git worktree add .remedy-wt/redproof-r6 HEAD --detach` for gate 15, then
  `git worktree remove --force` and `git worktree prune`. The mutation never
  entered the primary checkout (G5).

## Verification
| # | Gate | Real value |
|---|------|-----------|
| 1 | `git status --porcelain` / `git worktree list` | EMPTY / exactly 1 line, the primary checkout `/home/decodeux/Repos/remedy` on `[feature/f082-self-benchmark]` — both read AT handback. That line's SHA is the C4 commit's own and cannot exist when this text is written (R-0371); the completion report carries it |
| 2 | Transport property | scratchpad, `.agent/authored/f082-r6.md` and `.agent/last_block.md` byte-identical, shared sha256 `7969531a3551f295d65449f1ea158aec15cff8c31dea7dcfd41a66775c9b149e`, 28701 bytes, 325 lines (cap 400). `cmp`/`cp` denied to this session class; proven by `sha256sum` plus a `python3` byte compare over all three, and both committed blobs re-read with `git show` hash to the same digest (R-0408) |
| 3 | `.agent/STOP` | ABSENT at round start, ABSENT at handback |
| 4 | Append proof | first 115 lines of the new `.agent/live_review.md` equal the pre-C1 revision (115 lines, so the whole pre-C1 file is an exact prefix); `post == pre + add` proven byte-wise, added region sha256 `dd7e655df70edad090853460c9928ef4454c040d3664003ad9c09ea6e47f74af`; C1 numstat `6 0`, DELETION column 0; FINDING-R412, FINDING-R413 and GATE-R5 are 1 physical line each, 1 occurrence each; new file 121 lines |
| 5 | Record greps | `^Gate: R5 — PASS` 1, `^- R-0412 — ` 1, `^- R-0413 — ` 1, `^## Steps` 1 (in live_review.md; also 1 in context.md), `^Landed: ` 0, `^Done: ` 0 |
| 6 | Open set | FORTY-THREE, from 43 `^- R-…` paragraph starts minus 0 `^Done:` lines. Duplicates none, max R-0413, next free R-0414. Ids: R-0361 R-0362 R-0363 R-0364 R-0367 R-0368 R-0369 R-0371 R-0374 R-0375 R-0376 R-0377 R-0378 R-0379 R-0380 R-0381 R-0382 R-0385 R-0386 R-0387 R-0389 R-0391 R-0392 R-0393 R-0394 R-0395 R-0396 R-0397 R-0399 R-0400 R-0401 R-0402 R-0403 R-0404 R-0405 R-0406 R-0407 R-0408 R-0409 R-0410 R-0411 R-0412 R-0413 |
| 7 | Context pairs | CTXSTILL-FROM 0 after (1 before), CTXSTILL-TO 1 after; `grep -c "the five frozen order files"` 0 after, 1 before. CTXSTEPS-FROM 0 after (1 before), CTXSTEPS-TO 1 after. `wc -l .agent/context.md` 55. CORRECTION to the block's note: CTXSTILL-TO measured WITH its terminating newline is 0 before and 1 after, not 1 before — the prefix caveat only holds when the newline is stripped; both readings are reported and both discriminate. Re-read end to end: no other sentence says five orders are owed and no round maps to another round's work. One residual, NOT repaired (outside the ordered pairs): the Scope paragraph still names only `capability_bench.py` as the NEW module and does not mention `bench_dry_run.py` — an omission, not a contradiction |
| 8 | `wc -l .agent/plan.md` | 35 (cap 50) |
| 9 | context.md contract readers | `## Active Branch` present; slug `feature/f082-self-benchmark`; substring `Steps` present (1); roadmap F-ids F077, F082, F105; `pytest` 1 and `resource` 1 |
| 10 | `git diff --name-only d0b2152d..HEAD` | 7 paths measured BEFORE C4, counted mechanically: `.agent/authored/f082-r6.md`, `.agent/context.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`, `packages/orchestration/bench_dry_run.py`, `tests/orchestration/test_bench_dry_run.py`. C4 adds `.agent/handoff.md`, this file, which a handoff cannot table for itself (R-0149), so the at-handback reading is those same 7 plus that one and the completion report carries the measured count. Paths outside the block's Change list: NONE |
| 11 | `git diff --name-only d0b2152d..HEAD -- tests/orchestration/` | exactly 1 path, `tests/orchestration/test_bench_dry_run.py`. The gauntlet's own test files are byte-unmodified |
| 12 | 10-file orchestration suite | exit 0, `284 passed`. Arithmetic: planner baseline 279 without the new file, plus the 5 tests written this round = 284. No pre-existing test lost |
| 13 | canary + three contract readers | exit 0, `184 passed` (= planner baseline 42 + 142) |
| 14 | scoped ruff over the two R6 files | exit 0, `All checks passed!` (first run was RED with 1 UP035 on `typing.Iterable`; fixed to `collections.abc` before the C3 commit, so nothing red was committed) |
| 15 | Red-proof, disposable worktree | mutation applied in `.remedy-wt/redproof-r6` ONLY: `dry_run_rows` re-sorted its rows into directory order. Result exit 1, `1 failed, 4 passed`. Failing test: `test_rows_follow_order_ids_not_the_directory_sort`, assertion `assert tuple(row.order_id for row in rows) == (second, first)` → `AssertionError: At index 0 diff: 'fx-01-pure-code-change' != 'fx-02-operator-command'`. Worktree removed and pruned; `git worktree list` reads 1 line |
| 16 | `python3 -m apps.cli.main integrity check --json` | exit 0, `passed: true`, `fail_count: 0`, `check_count: 5`; `high_blockers_open` status `pass`, message "no open blocker/high findings" |
| 17 | `gh pr list --state open --json number,headRefName` | exit 0, output verbatim: `[]` |
| 18 | Insertions per commit | 593e07f5 325 · 1b0f4134 257 · 819b4cea 6 · bf008d9d 16 · c3799b97 263. None over 500. The C4 commit's own count cannot exist when this text is written (R-0371) and is in the round's completion report |

## Authored-text proofs
All eight extracted from the COMMITTED `.agent/authored/f082-r6.md` by
`.remedy-wt/f082-r6-apply.py` (`git show HEAD:<path>`, never the working copy,
never the scratchpad) and applied disk-to-disk; none retyped. Byte lengths
include each slice's terminating newline.
| Slice | sha256 | bytes | Applied-region proof |
| FINDING-R412 | `ba1e5953acc996816732e1e805cc0f608f982afa869a531c715ad82be38d41ad` | 2384 | in `.agent/live_review.md`, 1 occurrence, 1 physical line |
| FINDING-R413 | `b10519d7c958d7555221aa0bd6a56a5c2b93de836a83b8723e27f28dff89362b` | 1594 | in `.agent/live_review.md`, 1 occurrence, 1 physical line |
| GATE-R5 | `da638a3e0b509cb580a3badd68317fb33089adf790323929f4e3aaed0fda6c33` | 4495 | in `.agent/live_review.md`, 1 occurrence, 1 physical line |
| CTXSTILL-FROM | `063a80aab4bbdd9bac688e8bfa26a2c9cbd870385477a39f4349d87fe681b685` | 234 | REWRITE pair, disjoint from its TO: 1 occurrence before, 0 after |
| CTXSTILL-TO | `b6e1ebf94e609e7d933dcfad1ec3fc0dc07fcd3e75027ad96fe1974e0427c381` | 67 | 1 occurrence in `.agent/context.md` after the edit |
| CTXSTEPS-FROM | `d2ece5f1463dc1c95a21b9d18e53ae59a84d7886ceb6d616adf0d6ef773e043b` | 339 | REWRITE pair, disjoint from its TO: 1 occurrence before, 0 after |
| CTXSTEPS-TO | `1a7a541b52e6ee718631e24982d98ac7752bd9114150583d439328d493239dec` | 634 | 1 occurrence in `.agent/context.md` after the edit |
| PLAN | `ee697c2cd949373b3bdf5e876a406a0e53678de77691898bf50b2eb7000753af` | 1810 | `.agent/plan.md` equals the slice exactly, whole file |

Both context pairs are REWRITES and each pair's FROM and TO are disjoint; the
two FROM slices are disjoint from each other. The appended region of
`.agent/live_review.md` equals, byte for byte, a newline plus the three slices
joined by blank lines — proven as `post == pre + add`, not by grep alone. No
BEGIN/END marker line reached any target file (0 in all five non-block files;
the 16 in the two block files ARE the block). Trailing whitespace: 0 lines in
all seven files touched; every one ends with a newline.

## Item status
| Item | Status | Reason |
| C0a | done | |
| C0b | done | mirrored from the committed authored file, not the scratchpad |
| C1 | done | findings persisted FIRST, the first commit after C0a/C0b |
| C2 | done | both pairs applied, plan replaced whole |
| C3 | done | every symbol was where the block said; no gauntlet or bench file edited |
| C4 | done | this handoff |

## Deviations & assumptions
1. This handoff is over the 60-line cap; the stated cause is at the top under
   DECISION D15. No section dropped.
2. `cmp`, `cp`, bare `echo $?` and some compound `&&`/`;` chains are denied to
   this session class, as is the `remedy` entry point. Every affected PROPERTY
   was satisfied by another route and the route is named: `sha256sum` plus
   `python3` byte compares for transport, a `python3` `subprocess` runner for
   exit codes, `python3 -m apps.cli.main` for the CLI (R-0408). No gate skipped.
3. Gate 7's own note about CTXSTILL-TO counting 1 before the edit is corrected
   in the table: with the terminating newline it is 0 before, 1 after.
4. C1 landed before `.agent/plan.md` was re-synced in C2, so the tree carried a
   stale Current Step for one commit. That is the block's ordering — findings
   persist FIRST (planner_reviewer_prompt.md §4 item 4) — and the plan was
   correct again one commit later.
5. Commit messages carry no trailer, matching this repository's history.

## Next
Reviewer verdict on R6. Then R7 — T002: history append under the data root's
project area, trend computation, the regression rules, and the improving, flat
and degrading goldens. F082 stays mid-feature; no PR until closure.
