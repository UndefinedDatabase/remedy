# Handoff — F105 R28 (SPLIT round)

Branch: feature/f105-cache-optimal-prompt-ordering. Base of this round: 73259d7a.
Commits, in order: ac467af9 (C1a), 1f08d91c (C1b), 786aca2e (C2), e7667ac6 (C3),
e795fe5a (C4), plus this C5 commit.

## Changed files
| Path | What |
|---|---|
| .agent/authored/f105-r28-1.md | R28 block saved verbatim (new) |
| .agent/last_block.md | same bytes, mirrored |
| .agent/live_review.md | R27 gate record, R-0255 Done, R-0256 registered, next ID R-0257 |
| packages/orchestration/prompt_trace.py | append_trace_jsonl beside write_trace_jsonl |
| tests/orchestration/test_prompt_trace.py | 3 tests: append keeps, append creates, replan wiring guard |
| apps/cli/commands/do_cmd.py | replan on_call wiring + APPEND of replan traces |
| .agent/plan.md | PAIR_H full replacement |
| .agent/handoff.md | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## Gates (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 | both `c323410875ab8da7313a988a79d6f74e0976ba3320721b0d8f0ad35808df7fe2`, `cmp` silent |
| B size | 0 | 368 lines — under DECISION F105 D5's cap of 400 |
| C application | 0 | all 7 pairs + PAIR_H proved, table below |
| D markers | 0 | `grep -c -E '^<<<'` = 0 in all five targets |
| E touched suite | 0 | 41 passed in 0.19s |
| F red-proof M1 | 1 | RED as ordered, see below |
| G red-proof M2 | 1 | RED as ordered, see below |
| H tests/orchestration | 0 | 10502 passed, 7 skipped in 637.87s (+3 vs R27's 10499) |
| H tests/cli | 0 | 1329 passed in 263.11s |
| I tests/docs | 0 | 294 passed in 0.25s |
| I dashboard | 0 | 70 passed in 3.94s |
| I canary | 0 | 42 passed in 19.48s |
| J hygiene | 0 | at e795fe5a: porcelain empty, `git worktree list` primary alone; insertions per commit 368, 263, 57, 51, 25 — each under 500 |

## Pair proofs (each grep scoped to the named file)
| Pair | Shape (declared = measured) | Proof |
|---|---|---|
| A live_review | APPEND-prefix | FROM 1x after; TO-only 38 added lines in 786aca2e |
| B live_review | REWRITE | FROM 0x after, TO 1x (18 added) |
| C live_review | REWRITE | FROM 0x after, TO 1x (1 added) |
| 786aca2e decomposition | — | ADDED 57 = 38 A + 18 B + 1 C, strays 0 |
| D prompt_trace | APPEND-prefix | FROM 1x after; TO-only 13 added in e7667ac6; file ADDED 13, strays 0 |
| E test_prompt_trace | APPEND-prefix | FROM 1x after; TO-only 38 added in e7667ac6; file ADDED 38, strays 0 |
| F do_cmd | REWRITE | FROM 0x after, TO 1x; 14 added (7 of its 21 TO lines are byte-identical to FROM lines and stay diff CONTEXT) |
| G do_cmd | APPEND-prefix | FROM 1x after; TO-only 11 added |
| e795fe5a decomposition | — | ADDED 25 = 14 F + 11 G, strays 0 |
| H plan.md | full replace | `cmp` silent vs the sliced text, 41 lines < 50 |

Red-proof M1: disposable worktree at e795fe5a, `append_trace_jsonl`'s `path.open("a")`
→ `path.open("w")` → exit 1, `1 failed, 40 passed`, failing test
`TestSegmentManifest::test_appending_traces_keeps_the_earlier_ones`.
Red-proof M2: same worktree after reverting M1 (porcelain empty, 41 passed again),
the `on_call=make_flight_plan_call_recorder(...)` argument deleted from the REPLAN
call only (diff touches `apps/cli/commands/do_cmd.py` alone; the R27 site untouched)
→ exit 1, `1 failed, 40 passed`, failing test
`TestSegmentManifest::test_the_replan_path_records_and_appends_its_traces`.
Both worktrees removed and pruned.

Open findings: 5 (R-0221, R-0239, R-0246, R-0247, R-0256).
Next action: reviewer gates R28 against the real diff 73259d7a..HEAD. No PR created.

Deviations, declared (DECISION D15): this file is 80 lines. Cause: the mandated
gate table (13 rows), pair-proof table (10 rows), changed-files table (8 rows),
item-status table (6 rows) and the two mandated red-proof paragraphs do not fit
in 60. Also declared: the first M1/M2 run was discarded and re-run because a
stale `.pyc` (same byte size, same clock second as the revert) made M2 report a
second, false failure; the recorded run has bytecode writing disabled and shows a
clean green baseline, a green post-revert state, and one failing test per mutant.
No source was edited to force or to suppress either red.
