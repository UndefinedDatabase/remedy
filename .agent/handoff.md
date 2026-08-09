# Handoff — F105 R23 (worker → planner/reviewer)

R23 put the R22 gate on disk, registered R-0251 and R-0252, and fixed BOTH in
the same round: §3 gains pre-emission checklist item 5 (DECISION F105 D10) and
`_drop_one_newline_per_segment_boundary` gains its own direct test class. No
migration step taken; no production file touched.
Branch: feature/f105-cache-optimal-prompt-ordering. Base b35d9d56.
SESSION TERMINATOR: this round's OWN gate is owed to the NEXT session's
reviewer per docs/agents/planner_reviewer_prompt.md §4.13. No repair round was
opened to close it.
Deviations, declared: this file is 83 lines against the AGENTS.md cap of 60.
Cause per DECISION D15, all of it mandated: the eight-row changed-files table,
the A-G gate table with real exit codes, the pair-proof table, the item-status
table and the two declared deviations. No section dropped, no padding.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| 4fb5475e `save the R23 block verbatim` | `.agent/authored/f105-r23-1.md` | +368/-0 | C1a — `cp`, block ALONE, 368 lines, under D5's 400 |
| dbb0c99a `mirror the R23 block to last_block` | `.agent/last_block.md` | +292/-300 | C1b — `cp`, verbatim rewrite of ONE state file |
| 361ac729 `record the R22 gate and register…` | `.agent/live_review.md` | +78/-1 | C2 — PAIR_A rewrite, PAIR_B, PAIR_C |
| eb6beef2 `extend the pre-emission checklist…` | `.agent/decisions.md` | +36/-0 | C3 — PAIR_E, DECISION F105 D10 |
| eb6beef2 | `docs/agents/planner_reviewer_prompt.md` | +9/-0 | C3 — PAIR_D, §3 checklist item 5 |
| 7d292b18 `pin the segment-boundary fallback branch` | `tests/orchestration/test_builder_prompt_golden.py` | +36/-0 | C4 — R-0251's pin: one class, five tests |
| (this commit) `update the plan and close the session with R23` | `.agent/plan.md` | +18/-16 | C5 — PAIR_F full replacement |
| (this commit) | `.agent/handoff.md` | rewrite | C5 — this file (R-0149: cannot table its own SHA) |

Insertions: 368, 292, 78, 45, 36, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |

## Verification (real exit codes, real output)
| Gate | Command | Exit | Real output |
|---|---|---|---|
| A | `sha256sum` pair; `cmp` | 0 / 0 | both `fd3271aedac2f81f…`; `cmp` silent |
| B | `wc -l` authored | 0 | `368` |
| C | 4 greps; `sed -n 8p`; 2 greps; marker grep x4; `wc -l` plan | 0/0/0/0/0/0/1/0 | `1`, `1`, `1`; line 8 ends `Next free ID: R-0253.`; D10 `1`; `Reachable red-proofs only` `1`; markers `0`,`0`,`0`,`0` (grep exit 1 = no match, as intended); plan `47`, under 50 |
| D | `tests/docs/`; `test_dashboard_contract.py` | 0 / 0 | `294 passed in 0.30s` (baseline 294); `70 passed in 4.10s` (baseline 70) |
| E | golden; `tests/cli/test_golden_path.py` | 0 / 0 | `21 passed in 0.14s` (baseline 16 + the 5 new pins); `42 passed in 19.45s` (baseline 42) |
| F | red-proof in `.remedy-wt/r23red`, detached at 7d292b18 | 1 (RED, as ordered) | Deleting the `elif` fallback branch: `2 failed, 19 passed in 0.30s`. Exactly the two ordered tests failed — `test_the_leading_newline_of_the_later_segment_is_the_fallback` (`PromptSegmentError: builder prompt segment boundary carries no newline to drop between segments 0 and 1`) and `test_each_boundary_chooses_its_own_branch` (same error, `between segments 1 and 2`). Mutation reverted, worktree status empty, `git worktree remove` + `prune` run |
| G | `git status --porcelain`; `git worktree list`; `git log --numstat b35d9d56..HEAD` | 0/0/0 | empty at handback; primary alone; `+` per commit above, each under 500 |

## Authored-text proofs
Transport: `.agent/authored/f105-r23-1.md` and `.agent/last_block.md` both
sha256 `fd3271ae…`, `cmp` exit 0, both 368 lines. Every pair SLICED by marker
with a python reader; marker count 0 in all four targets.
| Pair | Target | Declared | Measured | FROM before/after | TO after | Stray |
|---|---|---|---|---|---|---|
| A | live_review | REWRITE | REWRITE | 1 / 0 | 1 | see C2 row |
| B | live_review | APPEND (TO⊃FROM prefix) | APPEND, prefix | 1 / 1 | 1 | see C2 row |
| C | live_review | APPEND (TO⊃FROM prefix) | APPEND, prefix | 1 / 1 | 1 | C2: 78 added, 0 stray |
| D | planner_reviewer_prompt | APPEND, FROM as prefix | INSERT-BEFORE, FROM as SUFFIX — dev. 1 | 1 / 1 | 1 | 9 added, 0 stray |
| E | decisions | APPEND (TO⊃FROM prefix) | APPEND, prefix | 1 / 1 | 1 | 36 added, 0 stray |
| F | plan | full replacement | byte-equal | — | — | sha256 `bcaf68ac…` on both; 18 added, 0 stray |

## Deviations & assumptions
1. PAIR_D's declared shape is wrong in one word: the block's table says the TO
   contains the FROM "as its prefix", but the FROM is the TO's SUFFIX — the new
   checklist item 5 goes BEFORE the "Why this is on disk" paragraph. Measured,
   not assumed. Application is unaffected (single-occurrence replacement) and
   the result is semantically correct: item 5 sits after item 4 and before the
   closing note. Reported, not "fixed"; the containment property that makes the
   replacement safe holds either way.
2. Shell layer: inline `$?`, pipes into `sed`/`awk`, `for` loops, `cat`-heredoc
   redirection and `cd`-then-`git` are rejected here (carried from R15-R22).
   Slicing, gate running and the red-proof went through python helpers in
   gitignored `.remedy-wt/r23slices/`; no authored text was retyped.

## Next
The next SESSION gates R23 over `b35d9d56..HEAD` — state, docs and one test
file; a red-proof IS owed on the new pin, and gate F above shows it goes red.
Then it takes migration-order step 6, `pingpong_loop.py::_build_reviewer_prompt`,
last of the six, after proving that decomposition byte-exact first (see plan).
Open findings: 4 (R-0221, R-0239, R-0246, R-0247). R-0251 and R-0252 were
registered and RESOLVED in this round.
