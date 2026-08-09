# Handoff — F105 R25 (worker → planner/reviewer)

R25 is the SESSION TERMINATOR. It puts the R24 gate on disk and REGISTERS the
two findings that gate produced, R-0253 and R-0254. Neither is fixed: R-0254 is
production code and needs a SPLIT round, and this session has no reviewer left
to gate one. No production file, no test file, nothing under `docs/` was
touched. Nothing executable changed, so NO mutation red-proof was ordered or
invented (DECISION F105 D10, checklist item 5).
Branch: feature/f105-cache-optimal-prompt-ordering. Base df32f595.

THIS ROUND'S OWN GATE IS OWED TO THE NEXT SESSION'S REVIEWER, by construction
per docs/agents/planner_reviewer_prompt.md §4.13 (the terminator): the round
that writes a gate record cannot record the gate on itself. No repair round was
opened to close it, exactly as §4.13 requires. R25's verdict lives here only.

Deviations, declared: this file is 80 lines against the AGENTS.md cap of 60.
Cause per DECISION D15, all of it mandated: the five-row changed-files table,
the A-G gate table with real exit codes and real output, the pair-proof table,
the item-status table and the §4.13 statement. Nothing dropped, no padding.

## Commits — changed files, one row per path
| Commit | Path | +/- | Reason |
|---|---|---|---|
| fc104bc0 `save the R25 authored block` | `.agent/authored/f105-r25-1.md` | +214/-0 | C1a — `cp` of the scratch original, block ALONE, 214 lines, under D5's 400 |
| 9d0c3705 `mirror the R25 block to last_block` | `.agent/last_block.md` | +167/-211 | C1b — `cp` of the same bytes, verbatim rewrite of ONE state file |
| 040ce2ea `record the R24 gate and register R-0253 and R-0254` | `.agent/live_review.md` | +84/-1 | C2 — PAIR_A rewrite, PAIR_B and PAIR_C appends |
| (this commit) `sync the plan and hand back R25` | `.agent/plan.md` | +13/-12 | C3 — PAIR_D full replacement, 40 lines |
| (this commit) | `.agent/handoff.md` | rewrite | C3 — this file (R-0149: cannot table its own SHA) |

Insertions: 214, 167, 84, this one — each under 500.

## Item status
| Item | Status | Reason |
|---|---|---|
| C1a | done | |
| C1b | done | |
| C2 | done | both entries left exactly as sliced, both end "OPEN."; no `Done:` text written |
| C3 | done | |

## Verification (real exit codes, real output)
| Gate | Command | Exit | Real output |
|---|---|---|---|
| A | `sha256sum` on authored + last_block; `cmp` them | 0 / 0 | both `a89edbcf2a2e9b5af1bd5befc90b4044f23d4861f32b83ab9ba34543abba0e9c`, equal to the scratch original; `cmp` silent |
| B | `wc -l .agent/authored/f105-r25-1.md` | 0 | `214` |
| C | pair counts; `cmp` plan vs sliced PAIR_D; `wc -l` plan; TO-only ADDED lines from `git show --numstat` on C2 | 0 | PAIR_A (DISJOINT rewrite): FROM 1x before, **0x after**, TO 1x after; PAIR_B FROM 1x before and 1x after (inside its TO), PAIR_C likewise. `git show --numstat 040ce2ea` = `84  1  .agent/live_review.md`, exit 0; 84 added lines total = 1 (PAIR_A TO) + 31 (PAIR_B TO-only) + 52 (PAIR_C TO-only); PAIR_A FROM removed 1x. **Strays 0**: every TO-only line occurs exactly once among the diff's ADDED lines, for both append pairs. `cmp` plan vs slice silent; `wc -l .agent/plan.md` = `40`, under 50 |
| D | `grep -c` `PAIR_A_FROM`, `PAIR_D_PLAN`, `END_PAIR`, `<<<` in live_review + plan | 0 | all eight counts `0` |
| E | `pytest tests/docs/ -q` ; `pytest tests/ui_server/test_dashboard_contract.py -q` | 0 / 0 | `294 passed in 0.30s` ; `70 passed in 4.55s` |
| F | `pytest tests/cli/test_golden_path.py -q` | 0 | `42 passed in 21.43s` |
| G | `git status --porcelain` ; `git worktree list` ; `git log --numstat df32f595..HEAD` | 0 / 0 / 0 | clean at handback; primary `/home/decodeux/Repos/remedy` ALONE; `+` per commit 214, 167, 84, this one |

## Authored-text proofs
Transport: `.remedy-wt/r25scratch/block.md`, `.agent/authored/f105-r25-1.md` and
`.agent/last_block.md` all sha256 `a89edbcf2a2e9b5a…`, `cmp` exit 0, 214 lines
each. All four pairs SLICED by `<<<MARKER>>>` with a python reader that rejects
any marker line inside a body; zero marker strings in either target.
| Pair | Target | Declared | Measured | FROM before/after | TO added | Stray |
|---|---|---|---|---|---|---|
| A | live_review | REWRITE (FROM/TO disjoint) | DISJOINT confirmed | 1 / 0 | 1 line added, 1 removed | 0 |
| B | live_review | APPEND (TO ⊃ FROM as prefix) | APPEND, prefix confirmed | 1 / 1 | 31 TO-only lines, all added | 0 |
| C | live_review | APPEND (TO ⊃ FROM as prefix) | APPEND, prefix confirmed | 1 / 1 | 52 TO-only lines, all added | 0 |
| D | plan | full replacement | byte-equal under `cmp` | — | — | 40 lines |

R-0253 note: the TO-only count was taken as ADDED LINES IN THE DIFF, as ordered.
Under that reading both append pairs are clean (0 strays) even though PAIR_C
repeats sentences already on disk — the reading R-0253 asks §4.9 to adopt.

## Deviations & assumptions
1. Shell layer only (carried from R15-R24): inline `$?`, `echo "…$?"` and
   multi-operation one-liners are rejected in this environment. Slicing,
   application, measurement and gate running went through scripts in gitignored
   `.remedy-wt/r25worker/`; no authored text was retyped anywhere.
No block defect found: every FROM matched disk, every declared pair shape held,
every gate was satisfiable as written.

## Next
Open findings: 6 — R-0221, R-0239, R-0246, R-0247, R-0253, R-0254. Two are new
this round and BOTH are OPEN by design. Next expected action: a NEW session's
reviewer gates R25 over `df32f595..HEAD` (state-file-only round), then R26
fixes R-0254 as a SPLIT round and R-0253 as §4.9 plus a sixth D8 checklist
item. No PR exists and none was created; the PR is created at CLOSURE.
