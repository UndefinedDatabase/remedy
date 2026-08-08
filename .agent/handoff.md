# Handoff — F104 Hard budget enforcement, R4 (T002 part 2)

Branch: `feature/f104-hard-budget-enforcement`. Build mode: one-session
self-drive. No PR, no merge, no force-push, no worktree created.

## Range
Review of `03efcd62..00289e1e` (6 commits, oldest first).

## Commits

### 745999fd chore(f104): save the R4 step block
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f104-r4-1.md | +114 | the R4 order, saved verbatim (item 1) |
| .agent/last_block.md | +205/-201 | same text; replaces the stale R3 block |
| .agent/plan.md | +9/-9 | Current Step moved to R4 |

### 445d84d6 refactor(f104): extract the safe-point counters build
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +12/-1 | pure move of the counters build into `_build_budget_counters()`; no logic change |

### ffe03941 feat(f104): derive the next task's token band, pure
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/budget_guard.py | +35 | `derive_next_task_token_band` — pure, never raises |
| tests/orchestration/test_predictive_budget.py | +79 | 9 tests: bands, boundary, summaries, degradation |

### 14b8940c feat(f104): stop before a task that would breach max_cost_usd
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +91/-1 | `JobPlan.budget_prediction` + both serializers; `_predictive_config` resolved once; predictive check inside `_stop_check` AFTER the reactive one; loop safe point passes the next task |
| packages/orchestration/budget_guard.py | +14/-7 | the two "no production caller" claims replaced |
| .agent/plan.md | +2/-2 | same claim removed |

### 621479df test(f104): pin the predictive stop at the live safe point
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_predictive_budget.py | +338/-6 | both acceptance fixtures through the real `run_job`, 2 inert regressions, the A9 seam pin, `_counters(priced=)` |
| .agent/plan.md | +11 | the blocker below |

### 00289e1e docs(f104): record DECISION F104 D6 and the R4 state
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F104.md | +10 | D6 appended next to D3/D4, verbatim |
| .agent/decisions.md | +31 | D6 with alternative + reversal |
| .agent/plan.md | +21/-24 | rewritten at R5, 49 lines |
| .agent/live_review.md | +8/-5 | one R4 line in `## Steps`; no finding text authored |

## External actions
`git push origin feature/f104-hard-budget-enforcement` — see the completion
report for the real transcript. No PR, no merge, no gh command, no worktree.

## Verification (real, re-runnable from the repo root)
| Gate | Command | Result |
|---|---|---|
| A | `pytest test_predictive_budget.py test_budget_guard.py test_job_budgets.py -q` | **249 passed, 1 xfailed**, exit 0 |
| B | `pytest test_budget_stop_integration.py test_f018_authority_integration.py test_stop_reasons.py -q` | **163 passed**, exit 0 |
| C | `pytest tests/docs/ -q` | **294 passed**, exit 0 |
| D | `pytest tests/cli/test_golden_path.py -q` | **42 passed**, exit 0 |

No intermediate commit was red: A and B were run green at 445d84d6 and again at
14b8940c before the tests landed (the wiring is inert without a price basis).

## Authored-text proofs
`cmp .agent/authored/f104-r4-1.md .agent/last_block.md` → **exit 0**.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 save the block | done | cmp exit 0 |
| 2 counters refactor | done | pure move, verified by `git diff` |
| 3 band derivation + tests | done | |
| 4 wiring + stale comments | done | `stop_check=_stop_check` still a zero-arg callable (`pingpong_loop.py:2258`) |
| 5 fixtures + regressions | deviated | terminal JOB_STOPPED is an `xfail(strict=True)` — blocker below; A9 pinned at the seam, as the block permits |
| 6 docs, decisions, state | deviated | no ist-doc exists to carry the stop reason; `.agent/context.md` untouched |

## Deviations & assumptions
- **BLOCKER, pre-existing, reported not fixed.**
  `run_manifest._BUDGET_ALLOWED_KEYS` is a closed schema F104 T001 never
  extended, so any job carrying `max_cost_usd` fails its F012 manifest write
  (`manifest.budgets has unknown keys: ['max_cost_usd']`). On the stop path this
  raises `StopFinalizationError` inside `_stop_job` AFTER the stop reason and
  source are set but BEFORE the JOB_STOPPED checkpoint: the job is left RUNNING
  with no manifest, so `--max-cost-usd` cannot finalize a stop at all. It
  reproduces with the predictive path fully inert and with no budgets beyond
  `{"max_cost_usd": 100.0}`, so it is not R4's. Not fixed — the block forbids
  fixing defects outside the change set, and `run_manifest.py` is shared F012.
  Every other acceptance assertion is pinned; the terminal one xfails
  `strict=True` and self-clears when the allowlist is fixed.
- **A9 pinned at the `derive`→`predict` seam, not through `run_job`**: a real
  `TaskEntry` always yields a derivable band (absent text estimates to 0 tokens,
  honestly LOW), so no run-level fixture reaches `TokenBand.UNKNOWN` without
  faking the task. The block permits this and asks it be said here.
- **No ist-doc carries the stop reason.** `docs/README.md` indexes none
  describing the F018/F104 job-budget stop path; the three `budget_exhausted`
  hits under `docs/system/` are the overnight-executor loop budget, the
  orchestrator loop budget and a dogfood status enum, and `autocoder-usage.md`'s
  is the repair budget. No doc created, per the block.
- **`.agent/context.md` left unchanged**: scope and constraints did not change.
  Its `## Steps` line is now stale (it maps R2→predictive stop, R3→display);
  reported, not edited, since the block gated the file on scope/constraints.
- **This handoff is 109 lines** (AGENTS.md D15 stated-cause overage): six
  per-commit tables, the gate table, the proof line, the item table and the
  blocker record. No section dropped.

## Next
Reviewer: verdict on R4, plus a ruling on the manifest blocker — its own repair
round, or folded into R5 (T003 display + docs + estimate labels).
