# Handoff — F104 Hard budget enforcement, R1 (T001)

Branch: `feature/f104-hard-budget-enforcement`, cut from `main` at 94f69b0f.
Commits (oldest first): 48ba2d10, 07f32b93, bd6a31c7, 9f832796, aee9cb1c, 8e8f1aaf.
Pushed. SPLIT round — no verdict written, no PR, no merge.

## Changed files, per commit

| Commit | Path | +/- | Reason |
|---|---|---|---|
| 48ba2d10 | docs/roadmap/STATUS.md | +1/-1 | claim F104 `[ ]` -> `[~]` (pair 1) |
| 48ba2d10 | .agent/live_review.md | +24/-498 | reviewer text f104-r1-2 (R-0221 registered) |
| 48ba2d10 | .agent/plan.md | +31/-33 | reviewer text f104-r1-3 |
| 48ba2d10 | .agent/context.md | +30/-31 | reviewer text f104-r1-4 |
| 48ba2d10 | .agent/authored/f104-r1-{1,2,3,4}.md | +121/-0 | authored originals for `cmp` |
| 07f32b93 | AGENTS.md | +11/-0 | DECISION F104 D1 counting rule (pair 5, APPEND) |
| 07f32b93 | .agent/decisions.md | +37/-0 | F104 D1 + D2 entry (block f104-r1-6) |
| 07f32b93 | .agent/candidates.md | +8/-2 | swept empty (f104-r1-7) |
| 07f32b93 | .agent/authored/f104-r1-{5,6,7}.md | +73/-0 | authored originals |
| bd6a31c7 | docs/roadmap/features/T2_F104.md | +1/-1 | Goal flag renamed `--max-cost-usd` (pair 8) |
| bd6a31c7 | .agent/authored/f104-r1-8.md | +9/-0 | authored original |
| 9f832796 | packages/core/models.py | +18/-1 | `JobBudgets.max_cost_usd` + finite/positive/bool validation |
| 9f832796 | packages/orchestration/budget_guard.py | +135/-0 | counters money fields, `cost_description`, `has_unpriced`, `cost_lower_bound`, `_LIMIT_ORDER`, `collect_ledger_cost_for_job` |
| 9f832796 | packages/orchestration/budget_resolution.py | +40/-1 | `_pos_float`, `_resolve_float`, config key, all-None gate |
| 9f832796 | packages/orchestration/config.py | +7/-0 | `budget.max_cost_usd` ConfigKeySpec (float) |
| aee9cb1c | apps/cli/command_catalog.py | +4/-0 | `--max-cost-usd` ArgDef at all 4 budget sites |
| aee9cb1c | apps/cli/commands/do_cmd.py | +11/-1 | thread `max_cost_usd` through 3 fns, the flag tuple, 3 handlers |
| aee9cb1c | apps/cli/commands/job.py | +3/-0 | thread it through `job create` so its new flag is not dead |
| 8e8f1aaf | tests/orchestration/test_budget_guard.py | +246/-0 | cost description, counter validation, evaluation, ledger bridge |
| 8e8f1aaf | tests/orchestration/test_job_budgets.py | +163/-0 | model field, resolution precedence, config-key registration |

## Transport proofs (all applied from `.agent/authored/`)

| Pair/file | Shape | Proof |
|---|---|---|
| f104-r1-1 STATUS.md | REWRITE | FROM 1x->0x, TO 0x->1x; `wc -l` 315 before and after |
| f104-r1-2 live_review.md | full-file `cp` | `cmp` exit 0 |
| f104-r1-3 plan.md | full-file `cp` | `cmp` exit 0 |
| f104-r1-4 context.md | full-file `cp` | `cmp` exit 0 |
| f104-r1-5 AGENTS.md | APPEND | FROM exactly 1x after edit; each TO-only line 1x; `diff` of authored TO block vs AGENTS.md:195-206 empty |
| f104-r1-6 decisions.md | append block | heading line occurs exactly 1x; one blank line before it |
| f104-r1-7 candidates.md | full-file `cp` | `cmp` exit 0 |
| f104-r1-8 T2_F104.md | REWRITE | `budget-usd` 1x->0x, `max-cost-usd` 0x->1x |

## Verification (run by me; real trimmed output, real exit codes)

| Gate | Command | Output | Exit |
|---|---|---|---|
| A | `python3 -m pytest tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_stop_reasons.py -q` | `345 passed in 36.92s` | 0 |
| B | `python3 -m pytest tests/cli/test_command_catalog.py tests/cli/test_do_cmd_cli_path.py -q` | `32 passed in 0.90s` | 0 |
| C | `python3 -m pytest tests/docs/ -q` | `294 passed in 0.25s` | 0 |
| D | `python3 -m pytest tests/cli/test_golden_path.py -q` | `42 passed in 20.66s` | 0 |

CLI-site parity: `grep -c 'max-cost-usd' apps/cli/command_catalog.py` = 4,
`grep -c 'max-wall-clock-minutes' apps/cli/command_catalog.py` = 4.
Live reachability probe: `do.job-plan` with `--max-cost-usd not-a-number`
printed `Error: max_cost_usd is not a valid number: 'not-a-number'` and exited 2.

## Item status

| Item | Status | Reason |
|---|---|---|
| 1 branch + STATUS claim + state reset | done | |
| 2 candidate sweep (AGENTS.md D1, decisions, empty candidates) | done | |
| 3 feature-file D2 amendment | done | |
| 4 T001 engine (models, budget_guard, budget_resolution, config) | done | |
| 5 T001 CLI wiring (command_catalog, do_cmd) | deviated | also threaded `apps/cli/commands/job.py` — see Deviations |
| 6 T001 tests | done | |

Open findings: 1 — R-0221 (Low), carried and REGISTERED in `.agent/live_review.md`,
deliberately NOT fixed by this round.

`git status --porcelain`: EMPTY at handback.
Next expected action: reviewer re-runs gates A-D against 8e8f1aaf, then R2 (T002
predictive check at the dispatch safe point).

## Deviations, declared

- **Bundle item 5 widened by one file.** The block named `command_catalog.py`
  and `do_cmd.py`, but it also required an ArgDef at EVERY site declaring the
  sibling budget flags — one of which is `job.create`, handled in
  `apps/cli/commands/job.py`. Adding the flag there without threading it would
  have shipped exactly the dead code the round's goal forbids, so the same
  3-line pattern (signature, `resolve_job_budgets` kwarg, handler `getattr`)
  was applied there. +3 lines, no behaviour invented.
- **Other `resolve_job_budgets` callers, grepped.** Non-test callers are
  `do_cmd.py:261` (`project_root=repo` only, no CLI flags — it now picks up
  `budget.max_cost_usd` from TOML automatically and needed no change),
  `do_cmd.py` x3 and `job.py` x1 (all threaded), and the
  `runtime_integration_gate.py` grep PATTERN, which is a string, not a call.
- **Help-text wording follows each site.** `job.create` and `do.run` say
  "Maximum cost in USD for this job (F104 budget)"; `do.job-plan` says
  "Maximum cost in USD (F104 budget)" and `do.job-run` "…(F104 budget override)",
  matching their own neighbours, as the block instructed.
- **`config.py` DID need the key.** `load_config` raises `BudgetConfigError` on
  an undeclared `budget.*` TOML key and `cfg.get_value` returns nothing for an
  unregistered key, so `budget.max_cost_usd` was added as a `float` ConfigKeySpec
  in the `budget.max_total_tokens` shape.
- **`remedy job budget` text output does not yet print `max_cost_usd`.** Its
  JSON path already carries it via `model_dump`; the text renderer is display
  work and belongs to T003, not T001. Named here so it is not mistaken for a miss.
- **Commit sizes.** Largest commit is 8e8f1aaf at +409 insertions; every commit
  is under the 500-insertion cap installed by DECISION F104 D1 in commit 2.
- **Handoff length** is 106 lines, over the 60-line cap. Cause: the mandated
  per-commit changed-files table (20 rows), the eight-row transport-proof table,
  the four-gate verification table and the item-status table. No section dropped.
