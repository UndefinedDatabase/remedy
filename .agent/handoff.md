# Handoff — F105 R26 (worker → planner/reviewer)

R26 is the SPLIT repair round. It records the R25 gate, fixes R-0253 (§4.9
scoped to the diff's ADDED lines plus a sixth D8 checklist item) and R-0254
(the shared boundary helper's builder-only message plus the one assertion that
pins it). Production code changed, so the reviewer gates it; nothing here is
self-certified. Base 0341928d.
Branch: feature/f105-cache-optimal-prompt-ordering.

Deviations, declared: this file is 99 lines against the AGENTS.md cap of 60 —
within the 100 that AGENTS.md allows when per-commit tables of more than five
commits require it, and this round has nine commits.
Cause per DECISION D15, all of it mandated: the ten-row changed-files table,
the A-J gate table with real exit codes and real output, the pair-proof table,
the item-status table and the red-proof record. Nothing dropped, no padding.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| debc9c9b `save the R26 authored block` | `.agent/authored/f105-r26-1.md` | +264/-0 | C1a — `cp` of the scratch original, block ALONE, 264 lines, under D5's 400 |
| b63c945f `mirror the R26 block to last_block` | `.agent/last_block.md` | +196/-146 | C1b — `cp` of the same bytes, verbatim rewrite of ONE state file |
| 4c53c746 `record the R25 reviewer gate` | `.agent/live_review.md` | +47/-0 | C2 — PAIR_A, append-shaped |
| c6ec5d3e `scope the append-pair count to the diff and add a D8 item` | `docs/agents/planner_reviewer_prompt.md` | +17/-2 | C3a — PAIR_B rewrite, PAIR_C append |
| 7c851b5e `mark R-0253 landed` | `.agent/live_review.md` | +1/-0 | C3b — the one `Landed:` line, naming c6ec5d3e |
| bb7b2cdc `make the segment-boundary error message role-neutral` | `packages/orchestration/pingpong_loop.py` | +1/-1 | C4a — PAIR_D; name, signature and all three branches untouched |
| bb7b2cdc | `tests/orchestration/test_builder_prompt_golden.py` | +2/-2 | C4a — PAIR_E; the assertion now anchors with `^` and `$` |
| e4775047 `mark R-0254 landed` | `.agent/live_review.md` | +1/-0 | C4b — the one `Landed:` line, naming bb7b2cdc |
| 1c06c0c9 `sync the plan and hand back R26` | `.agent/plan.md` | +6/-5 | C5 — PAIR_F full replacement, 41 lines |
| 1c06c0c9 | `.agent/handoff.md` | +74/-56 | C5 — this file, as first committed |
| (this commit) | `.agent/handoff.md` | rewrite | C5b — corrects the C5 row to the real numstat and fills gate J (R-0149: cannot table its own SHA) |

Insertions: 264, 196, 47, 17, 1, 3, 1, 80, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | no `Done:` text written anywhere |
| C3 | deviated | split into C3a (fix) + C3b (`Landed:` line) — see deviation 2 |
| C4 | deviated | split into C4a (fix) + C4b (`Landed:` line) — see deviation 2 |
| C5 | done | plan at 1c06c0c9; this file corrected once more at C5b, see the table |

## Verification (real exit codes, real output)
| Gate | Command | Exit | Real output |
|---|---|---|---|
| A | `sha256sum` authored + last_block; `cmp` | 0 / 0 | both `c249919e7e8d111f9cac38d8593b9f0c67d409ae85530256a0367eac4b1b4a0d`, equal to the scratch original; `cmp` silent |
| B | `wc -l .agent/authored/f105-r26-1.md` | 0 | `264` |
| C | pair counts scoped per file; `cmp` plan vs sliced PAIR_F; `wc -l` plan; diff-scoped ADDED lines | 0 | PAIR_A FROM 1x, TO 1x (append); PAIR_B FROM **0x**, TO 1x; PAIR_C FROM 1x, TO 1x (append); PAIR_D FROM **0x**, TO 1x; PAIR_E FROM **0x**, TO 1x. `cmp` plan vs slice silent, `wc -l .agent/plan.md` = `41` < 50. `git show --numstat 4c53c746 -- .agent/live_review.md` = `47 0`: 47 ADDED = PAIR_A's 47 TO-only lines, each exactly 1x, **strays 0**. `git show --numstat c6ec5d3e -- docs/agents/planner_reviewer_prompt.md` = `17 2`: 17 ADDED = PAIR_C's 8 TO-only lines (each exactly 1x) + PAIR_B's 9, **strays 0** |
| D | `grep -c` `PAIR_A_FROM`, `PAIR_F_PLAN`, `END_PAIR`, `<<<` in the five files | 0 | **RED as literally written** — see deviation 1. 17 of 20 substring counts are `0`; three are `1`, all on `.agent/live_review.md` and all on ONE line, 1263, which PAIR_A's own TO wrote: ``  leakage: `PAIR_A_FROM`, `PAIR_D_PLAN`, `END_PAIR` and `<<<` all count 0 in``. Marker-LINE count (`^<<<`) is `0` in all five files |
| E | `pytest tests/orchestration/test_builder_prompt_golden.py -q` | 0 | `21 passed in 0.17s` |
| F | red-proof M1 in a disposable worktree at e4775047 | 1 | `1 failed, 20 passed in 0.21s`; failing test `tests/orchestration/test_builder_prompt_golden.py::TestDropOneNewlinePerSegmentBoundary::test_a_boundary_with_no_newline_at_all_is_illegal`. RED as required. Worktree removed and pruned |
| G | `pytest tests/orchestration/ -q` | 0 | `10498 passed, 7 skipped in 640.95s` |
| H | `pytest tests/docs/ -q` ; `pytest tests/ui_server/test_dashboard_contract.py -q` | 0 / 0 | `294 passed in 0.25s` ; `70 passed in 3.85s` |
| I | `pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 22.45s` |
| J | `git status --porcelain` ; `git worktree list` ; `git log --numstat 0341928d..HEAD` | 0 / 0 / 0 | measured at 1c06c0c9: `git status --porcelain` printed NOTHING; `git worktree list` printed the primary `/home/decodeux/Repos/remedy  1c06c0c9` ALONE after the red-proof cleanup; `+` per commit 264, 196, 47, 17, 1, 3, 1, 80, this one |

## Authored-text proofs
Transport: `.remedy-wt/r26scratch/block.md`, `.agent/authored/f105-r26-1.md` and
`.agent/last_block.md` all sha256 `c249919e7e8d111f…`, `cmp` exit 0, 264 lines
each. Every pair SLICED from the COMMITTED authored file by `<<<MARKER>>>` with
a python reader that rejects any marker line inside a body; no marker LINE
reached any target.
| Pair | Target | Declared | Measured | FROM before/after | TO | Stray |
|---|---|---|---|---|---|---|
| A | live_review | APPEND (TO ⊃ FROM as prefix) | APPEND, prefix confirmed | 1 / 1 | 47 TO-only lines added | 0 |
| B | prompt doc | REWRITE (disjoint) | NOT append-shaped, confirmed | 1 / 0 | 1x | — |
| C | prompt doc | APPEND (TO ⊃ FROM as prefix) | APPEND, prefix confirmed | 1 / 1 | 8 TO-only lines added | 0 |
| D | pingpong_loop | REWRITE | NOT append-shaped, confirmed | 1 / 0 | 1x | — |
| E | golden test | REWRITE | NOT append-shaped, confirmed | 1 / 0 | 1x | — |
| F | plan | full replacement | byte-equal under `cmp` | — | — | 41 lines |

## Deviations & assumptions
1. **Gate D is red as literally written, and the block itself is the cause.**
   PAIR_A's TO writes the strings `PAIR_A_FROM`, `END_PAIR` and `<<<` into
   `.agent/live_review.md` on one prose line, then gate D orders those same
   strings to count 0 in that same file. That is DECISION F105 D8 item 2, "no
   self-counting gate", sixth recurrence — and it is exactly the class the new
   item 6 this round installs describes. Nothing was edited to force the count
   down; the real numbers are in the table. The property the gate exists to
   protect DOES hold: zero marker LINES in all five targets.
2. `<sha>` inside a `Landed:` line cannot name the commit that carries the
   line, so C3 and C4 each became two commits: the fix, then the one-line
   `Landed:` naming that fix's real short SHA. No history was rewritten and no
   commit was amended.
3. Shell layer only (carried from R15-R25): inline `$?`, `echo "…$?"` and
   multi-operation one-liners are rejected here. Slicing, application,
   measurement and gate running went through scripts in gitignored
   `.remedy-wt/r26worker/`; no authored text was retyped anywhere.
4. Observation, not acted on (no pair was given for it): the D8 preamble still
   reads "Run all four checks" and the closing note "R20 hit all four items",
   while the list now holds six.

## Next
Open findings: 6 — R-0221, R-0239, R-0246, R-0247, R-0253, R-0254. The last two
are `Landed:` and await reviewer-authored `Done:` text at the R26 gate; no
`Done:` paragraph was written by this worker (§4.4). Next expected action: the
reviewer gates R26 over `0341928d..HEAD`, then the `on_call` wiring round. No
PR exists and none was created; the PR is created at CLOSURE.
