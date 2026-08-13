# Handoff — F045 Loop definitions · R2 (findings + T002)

Branch: `feature/f045-loop-definitions`, cut from main at `cb3ef34f`. Pushed
after every commit. No PR opened, nothing merged. Open findings: 3 (R-0344,
R-0345, R-0346 — all OPEN in `.agent/live_review.md`).

## Commits
| SHA | Subject | Files (+/-) |
|-----|---------|-------------|
| `f99a3407` | chore(f045): save the R2 block verbatim | `.agent/authored/f045-r2-1.md` 252/0 · `.agent/last_block.md` 239/303 |
| `10301253` | docs(f045): register R-0344 to R-0346, the R1 block defects | `.agent/live_review.md` 5/1 |
| `7e2c94ec` | docs(f045): record decisions D1 to D3 | `.agent/decisions.md` 59/0 |
| `6794e7f0` | feat(f045): materialize a loop as a planned job with loop_ref | `packages/orchestration/loop_run.py` 168/0 |
| `5d613f49` | test(f045): pin loop_ref provenance and approval semantics | `tests/orchestration/test_loop_run.py` 182/0 |
| (this) | docs(f045): update the plan and handoff for R2 | `.agent/plan.md` · `.agent/handoff.md` |

Insertion budget ordered by the block vs. observed: C0 ≈ block size / 491;
C1 ≤ 30 / 5; C2 ≤ 90 / 59; C3 ≤ 190 / 168; C4 ≤ 240 / 182. No commit bundled a
new module with its test file. No commit exceeded 500 insertions.

## Gates (real exit codes and output)
| Gate | Command | Exit | Output |
|------|---------|------|--------|
| a | `cmp .agent/authored/f045-r2-1.md .agent/last_block.md` | 0 | (none) |
| b | `grep -c "^- R-0344 — Medium" .agent/live_review.md` | 0 | `1` |
| c | `grep -c "^- R-0345 — Low" .agent/live_review.md` | 0 | `1` |
| d | `grep -c "^- R-0346 — Low" .agent/live_review.md` | 0 | `1` |
| e | `grep -c "^(none yet on this branch)" .agent/live_review.md` | 1 | `0` (grep exits 1 on zero matches; the required VALUE is 0) |
| f | `grep -c "^## Steps" .agent/live_review.md` | 0 | `1` |
| g | `grep -c "^## DECISION F045 D" .agent/decisions.md` | 0 | `3` |
| h | `python3 -m pytest tests/orchestration/test_loop_run.py tests/orchestration/test_loop_spec.py -q` | 0 | `23 passed in 0.16s` |
| i | `python3 -m pytest tests/docs/ -q` | 0 | `294 passed in 0.25s` |
| j | `python3 -m pytest tests/cli/test_golden_path.py -q` (canary) | 0 | `42 passed in 20.40s` |
| k | `python3 -m ruff check packages/orchestration/loop_run.py tests/orchestration/test_loop_run.py` | 0 | `All checks passed!` |
| l | `git status --porcelain` | 0 | (empty; run before C5, re-run after C5 — see below) |

Gates (a)-(k) ran at `5d613f49`, before the C5 plan/handoff commit; (l) is
re-run after C5 and its post-commit result is reported in the handback.

## Items
| Item | Status | Reason |
|------|--------|--------|
| ITEM 1 | done | |
| ITEM 2 | done | |
| ITEM 3 | done | |
| ITEM 4 | deviated | two additions beyond the ordered semantics — see Deviations 2 and 3 |
| ITEM 5 | done | |
| ITEM 6 | done | |
| ITEM 7 | done | |

## Deviations, declared
0. This handoff is 78 lines, over the ≤60 cap. Cause: the mandated per-commit
   changed-files table (6 commits), the mandated twelve-row gate table carrying
   each gate's real exit code and output, and the mandated seven-row item-status
   table. No section was dropped to meet the cap.
1. Gate (k) ran as `python3 -m ruff check` — the bare `ruff` binary is refused
   by this worker's sandbox. Same tool, same arguments, exit 0.
2. `loop_to_job` also raises `LoopRunError` when a job-action spec has an empty
   `goal_template`. The block did not order it. `loop_spec` already refuses
   that combination, so the branch is unreachable via `load_loop_specs`; without
   it a hand-built spec would leak a stdlib `TypeError` out of `re.findall`,
   which is the failure mode the block's "no `KeyError` from deep inside the
   stdlib" rule exists to prevent. No test asserts on it.
3. `loop_budgets_to_job_budgets` raises `LoopRunError` if `datetime.fromisoformat`
   rejects the deadline string. Also unreachable through `load_loop_specs`
   (`loop_spec` validates the deadline), and it re-validates no range — it only
   refuses to let a stdlib `ValueError` escape the mapper.
4. `.agent/plan.md` still said "Current Step: R1" during C0-C4 and was rewritten
   at C5, as the block's change set requires. Flagged because AGENTS.md's commit
   gate item 1 wants the plan current at EVERY commit; the block scopes each
   commit's change set, and widening it would have been the larger violation.

## Next expected action
Reviewer re-runs (a)-(l) against the C5 commit, then plans R3 = T003 (`remedy
loop list | validate | run`, `run_loop` action dispatch including the mission
path per DECISION F045 D3, last-run display, end-to-end fixture loop).

Fortschritt: ~35 % (T001 ✅ · T002 ✅ · T003 offen) — Schätzung
