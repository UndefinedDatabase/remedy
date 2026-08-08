# Handoff — F104 Hard budget enforcement, SESSION CLOSE (R2 + R3)

Branch: `feature/f104-hard-budget-enforcement`, cut from `main` at 94f69b0f.
Build mode: one-session self-drive (docs/agents/self_drive_protocol.md).
Tip: 8b51fa63. Pushed. No PR, no merge, no force-push this session.
LAST_REVIEWED_SHA = 8b51fa63.

## What this session found and did

It opened on a BROKEN-OFF round: HEAD was ef9a852c, `git status --porcelain`
reported ` M tests/orchestration/test_budget_guard.py` (+119 lines,
uncommitted), and R2 had committed items 1-5 of its block without ever writing
a handback. Items 7-8 were untouched. The session resumed R2 rather than
planning new work, then ran R3, and closed here. It did not start R4.

## Rounds and verdicts (verdicts are the reviewer's; gates re-run by the reviewer)

| Round | Commits (oldest first) | Verdict |
|---|---|---|
| R2 (resumed) | 5e2e242d, 77971336, 5971a127, 460e837c, 5ffd1178 | PASS at 5ffd1178 |
| R3 | 61ba3056, e4f0dd31, 76be26d9, c6f99aa8, 31a462d3, 8b51fa63 | PASS at 8b51fa63 |

Plus the five R2 commits inherited from the previous session: 18b8ca7a,
ab77b2b5, c6994fa8, 0f195a60, ef9a852c.

## Verification — re-run by the reviewer, real exit codes

| Gate | Command | R2 | R3 |
|---|---|---|---|
| A | `pytest test_predictive_budget.py test_budget_guard.py test_job_budgets.py -q` | 226 passed, exit 0 | 233 passed, exit 0 |
| B | `pytest test_budget_stop_integration.py test_f018_authority_integration.py test_stop_reasons.py -q` | 163 passed, exit 0 | 163 passed, exit 0 |
| C | `pytest tests/docs/ -q` | 294 passed, exit 0 | 294 passed, exit 0 |
| D | `pytest tests/cli/test_golden_path.py -q` | 42 passed, exit 0 | 42 passed, exit 0 |

Mutation red-proofs, all run by the reviewer in disposable worktrees under
`.remedy-wt/`, all removed afterwards:

| Mutation | Result |
|---|---|
| `predict_next_task_cost`: `>` -> `>=` | 1 RED — only the exact-boundary test |
| `_stop_check`: `_ledger_cost` -> `_ledger_cost or 0.0` | 1 RED — the P6 null test |
| `_stop_check`: R-0222 ledger read disabled | 4 of 5 live safe-point tests RED |
| `BudgetCounters`: restore `unpriced_call_count > provider_calls` | exactly 3 RED — the R-0224 pins |

R-0224 was also reproduced directly by the reviewer before it was registered:
`collect_counters_from_actuals({"provider_call_count": 0, ...},
measured_cost_usd=None, unpriced_call_count=3)` raised
`BudgetCounterError: unpriced_call_count (3) > provider_calls (0)`.

## What is built

T001 is complete (R1). T002 part 1 is complete: the ledger cost reaches the
live safe-point guard, the provisional price-basis and class-default config
keys resolve, and the PURE prediction engine `predict_next_task_cost` /
`BudgetPrediction` is implemented and tested. R3 closed the cross-source
counter defect that R2's own bridge introduced.

DECLARED: `predict_next_task_cost` has NO production caller. That is by design
and is stated in the module docstring, above the function, and in
`.agent/plan.md`; R4 wires it at the task-dispatch safe point. Saying so is
what keeps R-0222 from recurring silently.

Decisions recorded this session: F104 D3 (band is derived, not stored), D4 (the
price basis has no default), D5 (cost-side call counts are validated against
the cost side).

## Item status

| Item | Status | Reason |
|---|---|---|
| R2 items 1-5 (inherited, committed) | done | verified by the reviewer at PASS |
| R2 item 6 tests | done | inherited test strengthened by the R2 worker, then committed |
| R2 item 7 feature file + decisions | done | |
| R2 item 8 gates, state, handback | done | |
| R3 items 1-6 | done | |
| Session close | done | this handoff |
| R4 (T002 part 2 wiring) | not started | session round cap reached |

## Open findings

1 — R-0221 (Low, carried, not F104's to fix; routed to the F252 flake-debt
class). R-0222, R-0223 and R-0224 are all marked Done in
`.agent/live_review.md` with reviewer-authored resolution text.

## State

`git status --porcelain`: EMPTY. Branch pushed and in sync with origin. No
worktrees remain beyond the primary checkout. `docs/roadmap/STATUS.md` still
carries F104 as `[~]`, correctly — the feature is not closed.

## Next expected action

R4 — T002 part 2. Derive the band at the dispatch safe point per DECISION F104
D3 using `token_economy.estimate_task_token_band()`, call
`predict_next_task_cost` BEFORE the next task is dispatched, add the
`predicted_budget_exhausted:<limit>` stop reason and the decision entry
carrying the arithmetic, and add both acceptance fixtures — just-under, and
prediction-wrong proving the reactive backstop still fires.

Known trap for R4, surfaced by the R3 worker and confirmed: the `_counters`
helper in `tests/orchestration/test_predictive_budget.py` has no `priced`
parameter, so any new test pairing `spent > 0` with `unpriced > 0` will hit the
cost-side contradiction check. Give it a `priced` parameter the way
`_cost_counters` in `test_budget_guard.py` already has one.

After R4: R5 display and docs, R6 integration gate, R7/R8 closure.

## Deviations, declared

- **The session ended at its stated round cap (3 delegated rounds), not at the
  end of the feature.** Per self-drive protocol G7 that is a success, not a
  failure. R4 was not started because it is the largest remaining round and
  beginning it without headroom to also review it would have recreated exactly
  the unfinished-round state this session opened on.
- **The R3 worker's completion report claimed a `Done:` marker on R-0224 that
  its applied text did not contain.** The worker applied the reviewer's text
  correctly; the report overstated it. The reviewer caught the discrepancy at
  review and authored the marker in this closing round. Recorded because a
  worker summary is never evidence, and this is a concrete instance.
- **The R3 worker repaired five pre-existing tests beyond the three the block
  named**, by giving `_cost_counters` a `priced` parameter defaulting to
  `calls - unpriced`. Reviewer-checked: no assertion was relaxed or deleted.
- **Commit 76be26d9 leaves 7 tests RED at that SHA**, green again at 31a462d3.
  The block separated the fix and its tests into two ordered items; the worker
  declared this rather than silently reordering.
- **This handoff is 118 lines, over the 60-line cap**, under AGENTS.md DECISION
  D15 stated-cause overage: it covers TWO reviewed rounds plus a resumed one,
  and carries the mandated per-round commit list, the two-round verification
  table, the mutation-proof table, the item-status table and the open-findings
  record. No section was dropped.
