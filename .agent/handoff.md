# Handoff — F105 R27 (SPLIT round)

Branch: feature/f105-cache-optimal-prompt-ordering. Base of this round: d0ebba63.
Commits, in order: 19837409 (C1a), 477030f0 (C1b), c9555983 (C2), f5752809 (C3),
4790c257 (C3 Landed line), 1ca10c50 (C4), plus this C5 commit.

## Changed files
| Path | What |
|---|---|
| .agent/authored/f105-r27-1.md | R27 block saved verbatim (new) |
| .agent/last_block.md | same bytes, mirrored |
| .agent/live_review.md | R26 gate record, R-0253/R-0254 Done, R-0255 + Landed |
| docs/agents/planner_reviewer_prompt.md | D8 preamble/closing note now count six |
| packages/orchestration/flight_plan.py | make_flight_plan_call_recorder + import |
| apps/cli/commands/do_cmd.py | prompt_traces rename, flight-plan on_call wiring |
| tests/orchestration/test_prompt_trace.py | wiring guard for the new recorder |
| .agent/plan.md | PAIR_N full replacement |
| .agent/handoff.md | this file |

## Items
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | deviated | fix f5752809 + Landed line 4790c257: a commit cannot name its own SHA |
| C4 | done | |
| C5 | done | |

## Gates (real exit codes, real output)
| Gate | Exit | Output |
|---|---|---|
| A transport | 0 | both files `efef62a6c61e08b33682175f034b9ba1441cac7245b6dceca5e05093199fb71a`, `cmp` silent |
| B size | 0 | 457 lines — OVER the 400 cap, declared below |
| C application | 0 | all 14 pairs + PAIR_N proved, table below |
| D markers | 0 | `grep -c -E '^<<<'` = 0 in all six targets |
| E touched suite | 0 | 38 passed in 0.16s |
| F red-proof M1 | 1 | RED as ordered, see below |
| G orchestration | 0 | 10499 passed, 7 skipped in 584.43s |
| G tests/cli | 0 | 1329 passed in 240.06s |
| H tests/docs | 0 | 294 passed in 0.25s |
| H dashboard | 0 | 70 passed in 3.90s |
| I canary | 0 | 42 passed in 19.23s |
| J hygiene | 0 | `git status --porcelain` empty, `git worktree list` primary alone; insertions per commit 457, 371, 69, 3, 1, 95 |

## Pair proofs (each grep scoped to the named file)
| Pair | Shape (declared = measured) | Proof |
|---|---|---|
| A live_review | APPEND-prefix | FROM 1x; TO-only 46 added lines in c9555983 |
| B/C/D live_review | REWRITE | FROM 0x, TO 1x each |
| c9555983 decomposition | — | ADDED 69 = 46 A + 6 B + 16 C + 1 D, strays 0 |
| E/F planner_reviewer_prompt | REWRITE | FROM 0x, TO 1x each |
| G flight_plan | APPEND-suffix | FROM 1x; TO-only 1 added line |
| H flight_plan | APPEND-prefix | FROM 1x; TO-only 43 added lines; file ADDED 44, strays 0 |
| I/J/K/L do_cmd | REWRITE | FROM 0x, TO 1x each; file ADDED 26 accounted, strays 0 |
| M test_prompt_trace | APPEND-prefix | FROM 1x; TO-only 25 added lines; file ADDED 25, strays 0 |
| N plan.md | full replace | `cmp` silent vs the sliced text, 42 lines < 50 |

Red-proof M1: disposable worktree at 1ca10c50, both the `on_call=` argument and the
`make_flight_plan_call_recorder,` import removed → exit 1, `1 failed, 37 passed`,
failing test `TestSegmentManifest::test_the_cli_flight_plan_recorder_passes_the_composed_prompt`.
Worktree removed and pruned.

Open findings: 5 (R-0221, R-0239, R-0246, R-0247, R-0255 — R-0255 marked Landed,
Resolved only by the reviewer).
Next action: reviewer gates R27 against the real diff d0ebba63..HEAD. No PR created.

Deviations, declared (DECISION D15): this file is 75 lines. Cause: the mandated
gate table (12 rows), pair-proof table (9 rows), changed-files table (9 rows) and
item-status table (6 rows) plus the red-proof paragraph do not fit in 60.
Also declared: (1) the saved block is 457 lines against DECISION F105 D5's cap of
400 — a worker must save it verbatim, so it cannot be fixed downstream (D8 item 1);
(2) C3 is two commits because the ordered `Landed: R-0255 ... commit <sha>` line
must name a SHA that does not exist until the fix commit exists — the R26 precedent
(bb7b2cdc then e4775047).
