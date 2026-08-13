# Handoff — F045 Loop definitions · ROUND 10

Branch: feature/f045-loop-definitions. Base for this round: 3be5ab8b.
Landed `remedy loop run <name> [--yes]`: it materializes through
`loop_run.run_loop` and STOPS at a planned job. The T003 CLI is now complete.

Deviations, declared: 98 lines (`wc -l`; AGENTS.md D15 allows >60 with a stated
cause). Cause is mandated content — the two CHECK results, the 7-row commit
table, the 14-row ITEM 7 gate table with real output, and the item-status
table. No section is dropped.

## The two CHECKs the block ordered

CHECK 1 — `grep -rln "def _resolve_project_id" apps/cli/commands/` returns TWO
files: `mission_cmd.py` and `queue_cmd.py`. A third module,
`worker_facade_cmd.py`, imports `mission_cmd`'s copy rather than defining one.
So several already do, and `loop_cmd.py` is the THIRD definition, not the
second. Mirrored `queue_cmd`'s version verbatim in spirit (same wording, same
`EXIT_NO_PROJECT = 3`); no shared helper extracted. No contradiction with the
block.

CHECK 2 — the supported route the CLI tests use is
`project_registry.RemyProject(...)` + `save_project(...)` under
`REMEDY_DATA_DIR`. `tests/cli/test_mission_cmd.py` and
`tests/cli/test_queue_cmd.py` do it in a subprocess; `tests/cli/test_stats_cost.py`
(fixture `project_id`) and `tests/cli/test_project_current.py` (`_make_and_save`)
do the same in-process. The new tests reuse the in-process form, because
`test_loop_cmd.py` dispatches in-process. No registry internal is touched and
no new registration route was invented. No contradiction with the block.

## Commits this round

| SHA | Subject | Files |
|---|---|---|
| c0c2ce9a | chore(f045): save the R10 block verbatim | .agent/authored/f045-r10.md (NEW) |
| b13eb548 | chore(f045): point last_block at the R10 block | .agent/last_block.md |
| c5313898 | docs(f045): register R-0356, the open-set miscount | .agent/live_review.md |
| 0e8eb70a | docs(f045): record DECISION F045 D7 on what loop run --yes means | .agent/decisions.md |
| cd135cb4 | feat(f045): add the loop run command, materialize and stop | apps/cli/commands/loop_cmd.py · apps/cli/command_catalog.py |
| 6bd0c6a8 | test(f045): pin loop run materializing and stopping | tests/cli/test_loop_cmd.py |
| this one | docs(f045): hand back R10 with the loop run command | .agent/plan.md · .agent/handoff.md |

## ITEM 7 gates — real exit codes, real output

| Gate | Exit | Real output |
|---|---|---|
| (a) cmp authored vs last_block | 0 | no output; byte-compare also True |
| (b) grep -c "^- R-0356 — Low" | 0 | `1` |
| (c) recomputed open set | 0 | `OPEN ['R-0350', 'R-0353', 'R-0354', 'R-0355', 'R-0356']` |
| (d) grep INERT_TRIGGER_NOTICE in loop_cmd.py | 0 | one line only: `50:#: A listing deliberately does NOT reuse ``loop_spec.INERT_TRIGGER_NOTICE``: that` — the R9 WHY comment. The run path prints `outcome.notice`. |
| (e) pytest tests/cli/test_loop_cmd.py -q | 0 | **GREEN** — `14 passed in 0.12s` |
| (f) pytest catalog + loop_run + loop_spec -q | 0 | **GREEN** — `60 passed in 0.51s` |
| (g) pytest tests/cli/test_golden_path.py -q (canary) | 0 | **GREEN** — `42 passed in 15.88s` |
| (h) ruff check (3 files) | 0 | `All checks passed!` |
| (i) reachability through the real table | 0 | `{'loop.list': True, 'loop.validate': True, 'loop.run': True}` |
| (j) RED-PROOF in .remedy-wt/f045_r10 | 1 | **RED, as required.** Import probe printed `/home/decodeux/Repos/remedy/.remedy-wt/f045_r10/apps/cli/commands/loop_cmd.py` — under the worktree, so R-0337 is satisfied. `-k run`: `4 failed, 1 passed, 9 deselected`; the four are the new run tests, failing on `KeyError: 'loop.run'` from `collect_all_handlers()` and on `assert 'loop.run' in handlers`. The one pass is the PRE-EXISTING listing test `test_after_one_real_firing_the_row_shows_that_run`, which matches `-k run` by name and exists unchanged at 3be5ab8b. No NEW test passed there. Extra check, not ordered: the whole file in the same worktree gave `8 failed, 6 passed` — all eight new tests red, all six old ones green. |
| (k) git diff --name-only 3be5ab8b..HEAD | 0 | the nine Change files, nothing else |
| (l) git status --porcelain | 0 | EMPTY |
| (m) real-store safety | 0 | `REAL_STORE_LOOP_REF_JOBS 0` |
| (n) git worktree list | 0 | ONE line: the primary checkout |

(k), (l) and (n) were re-run after the final commit.

## Open findings — RECOMPUTED, not carried forward

5, from `.agent/live_review.md` by gate (c): **R-0350, R-0353, R-0354, R-0355,
R-0356**. R-0356 is the one registered this round. Next free id: R-0357.

## Item status

| Item | Status | Reason |
|---|---|---|
| ITEM 1 (C0a+C0b) | done | |
| ITEM 2 (C1) | done | R-0356 applied verbatim; byte-compared against the authored block |
| ITEM 3 (C2) | done | DECISION F045 D7; the quoted `loop_run.py` docstring sentence was verified present in the source |
| ITEM 4 (C3) | done | 129 insertions, budget 130 |
| ITEM 5 (C4) | done | 148 insertions, budget 190; eight tests |
| ITEM 6 (C5) | done | plan.md 49 lines; this handoff |
| ITEM 7 | done | every gate run; outputs above |

## Safety statement

No PR is open. Nothing was merged. `main` was never touched — every commit is
on `feature/f045-loop-definitions`, pushed after each commit. No force-push
occurred. The red-proof worktree `.remedy-wt/f045_r10` was removed; gate (n)
shows one worktree. `.agent/STOP` did not exist at any point this round.

## Next expected action

1. Phase 1 rule 1 first: read `.agent/STOP` from disk (finding R-0347 — a
   sentinel that appears mid-session is invisible until something trips on it).
2. Then Phase 1 rule 2, the Open PR Gate.
3. Then R11: apply the on-disk counter-measures for R-0353 and R-0356 to
   `docs/agents/planner_reviewer_prompt.md` §3, and write the session-closing
   handoff. The feature is NOT closed; the end-to-end fixture loop, the
   integration gate and closure remain after this session.

Fortschritt: ~60 % (T001 ✅ · T002 ✅ · T003 läuft) — Schätzung
