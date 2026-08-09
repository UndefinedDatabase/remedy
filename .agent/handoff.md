# Handoff — F104 Hard budget enforcement, R6 (T003)

Feature F104, round **R6**, branch `feature/f104-hard-budget-enforcement`, build
mode one-session self-drive, one delegated worker. T003 delivered: display, the
grep-style basis pin, and the ist-doc per DECISION F104 D8. **Awaiting review.**
No PR, no merge, no force-push, no worktree.

## Range
Review of `549f2bac..26a4e750` (the state-close commits 8a9a964c / bea706a8 /
95672c30 are already reviewed; R6's own six commits are below, oldest first).

## Commits

### 64d962aa chore(f104): save the R6 block verbatim
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f104-r6-1.md | +197 | the R6 block, verbatim (item 1) |
| .agent/last_block.md | +318/-123 | same bytes; replaces the stale close block |

### df86e5af feat(f104): extract the next-predictable-task selection rule
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/pingpong_job.py | +46 | `select_next_predictable_task`, pure, never raises; `run_job` untouched |
| tests/orchestration/test_predictive_budget.py | +172 | seam pin vs the LIVE `_stop_check` + blocked/failed/skipped/all-passed cases |

### 72c96140 feat(f104): show the money limit, spend and next-task expectation
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/job.py | +124 | `_cmd_job_budget` (a)-(d) + 2 money formatters; JSON gains `prediction`/`recorded_prediction` |
| tests/orchestration/test_job_budgets.py | +372 | `TestJobBudgetCliRendersPredictions`, 19 tests through the REAL command via capsys |

### 191e4b5c test(f104): pin that every predicted number carries its basis label
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_predictive_budget.py | +150 | `TestEveryPredictedNumberCarriesItsBasis`: vocabulary completeness + surface grep |

### 1eae2ecb docs(f104): document the job-budget stop path per DECISION F104 D8
| Path | +/- | Reason |
|---|---|---|
| docs/system/job-budget-enforcement-v0.md | +112 | NEW ist-doc |
| docs/README.md | +2 | Quick-Find (`job budget`) + System table, both alphabetical |

### 26a4e750 chore(f104): record DECISION F104 D8 and the R6 state
| Path | +/- | Reason |
|---|---|---|
| .agent/decisions.md | +21 | D8, reviewer text verbatim |
| .agent/live_review.md | +7/-2 | ONLY the R6 `## Steps` line replaced |
| .agent/plan.md | +25/-14 | rewritten, 49 lines, R6-complete-awaiting-review |

## External actions
`git push -u origin feature/f104-hard-budget-enforcement` → `95672c30..26a4e750`.
No PR, no merge, no gh command, no worktree add/remove.

## Verification
Run by me from the repo root at 26a4e750, real exit codes:

| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `pytest tests/orchestration/test_predictive_budget.py -q` | **0** | 75 passed in 1.94s |
| B | `pytest tests/orchestration/test_job_budgets.py tests/orchestration/test_budget_guard.py -q` | **0** | 223 passed in 32.92s |
| C | `pytest tests/orchestration/test_budget_stop_integration.py -q` | **0** | 39 passed in 0.22s |
| D | `pytest tests/docs/ -q` | **0** | 294 passed in 0.30s |
| E | `pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed in 19.47s |

Baseline over the same four budget files before any R6 code: 300 passed, exit 0.
`test_f018_authority_integration.py` also re-run green (153 with C).

## Authored-text proofs
`cmp .agent/authored/f104-r6-1.md .agent/last_block.md` → **exit 0**. DECISION
F104 D8 and the R6 `## Steps` line were applied verbatim.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 save the block | done | cmp exit 0 |
| 2 selection helper + seam pin | done | pure addition; `run_job` byte-unchanged |
| 3 `_cmd_job_budget` (a)-(d) + JSON | deviated | see D1 below — the CLI now READS the F103 ledger |
| 4 basis-label acceptance pins | done | 5/5 labels reachable; set equality asserted |
| 5 ist-doc + README rows | deviated | 112 lines vs the block's "roughly 60-90" (D2 below) |
| 6 D8, state files, handback | done | `.agent/context.md` left untouched — see D3 |

## Open findings
**1** — R-0221 (Low, carried from F103 R5; not F104's to fix; F252 flake-debt
class; costs the integration gate seven phantom base-only failures). R-0222,
R-0223, R-0224, R-0225, R-0226 all Done.

## State
`git status --porcelain` **EMPTY**; branch pushed; no worktrees;
`docs/roadmap/STATUS.md` untouched, F104 still `[~]`.

## Deviations & assumptions — declared
- **D1 (item 3).** Item 3(b) is unreachable as written: `counters_from_persisted`
  has no cost field, so `measured_cost_usd` was ALWAYS None in the CLI and both
  the `$%.4f` remaining branch and the "priced job" test the block orders could
  never fire. `_cmd_job_budget` therefore now composes the ledger read the same
  way `run_job._build_budget_counters` does — `_resolve_job_ledger_project_id` +
  `collect_ledger_cost_for_job` — only when `max_cost_usd` is set, wrapped, and
  degrading to the unmeasured path. `query_cost` is SELECT-only and never creates
  a ledger, so `action_class="read_only"` still holds; pinned by
  `test_the_command_does_not_mutate_the_persisted_job` (job.json bytes identical).
  This is new I/O in a read-only command and is flagged for the R7 gate.
- **D2 (item 5).** The ist-doc is 112 lines, not 60-90. The block mandated eleven
  topics plus two tables; trimming further would have dropped mandated content.
- **D3 (item 6).** `.agent/context.md` untouched — its round list already names
  R6 as display/docs/estimate labels and its branch context is correct, which is
  the block's stated condition for leaving it.
- Commit 72c96140 is **496 insertions** — under the 500 cap but close; not split,
  because the command and the tests that drive it are one logical step.
- **This handoff is 115 lines** (AGENTS.md D15 stated cause): six per-commit
  changed-files tables, the five-gate table, the six-row item-status table and
  three declared deviations. No section dropped.

## Next
**R7 — the integration gate** (docs/agents/integration_gate.md), attributing
R-0221's seven base-only failures. Then **R8** closure.
