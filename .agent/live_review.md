# Live Review — F104 Hard budget enforcement

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only; the worker applies
> them verbatim and marks `Done: R-XXXX` when a fix lands. Only reviewer-
> authored text sets Resolved.
> Branch: feature/f104-hard-budget-enforcement. Next free ID: R-0225.

## Findings

- R-0221 (Low, carried from F103 R5 through `.agent/candidates.md`):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD`
  and runs a real `npm install` + `npm run build` in whatever checkout it runs
  in, refreshing `apps/ui/dist` mtimes mid-suite. That costs every integration
  gate seven phantom base-only failures through the mtime comparison in
  `_frontend_is_stale()` (`ui_server.py:2748`).
  REGISTERED here, deliberately NOT fixed by F104: the code is not this
  feature's and AGENTS.md Scope Control bars the "while I'm here" edit. It is
  carried as a documented LOW risk to F104 closure
  (STATUS_closure_protocol.md precondition 1) and routed to the F252
  flake-debt follow-up class. The F104 integration gate attributes these seven
  to the pre-existing base-only class per docs/agents/integration_gate.md
  rather than treating them as new failures.
  OPEN — the only open finding on this branch.

- R-0222 (Medium, found in the R1 review): `collect_ledger_cost_for_job` had no
  production caller, so `measured_cost_usd` was always None at runtime and
  `--max-cost-usd` could never exhaust in production.
  Done: R-0222 — fixed in c6994fa8, pinned by
  `TestLiveSafePointReadsTheLedgerCost` in
  `tests/orchestration/test_budget_guard.py`, which drives the real `run_job`
  pre-work safe point rather than grepping source. Reviewer-verified in the R2
  review: reverting the fix turns 4 of its 5 tests RED, and coercing the null
  to `0.0` turns the P6 test RED.

- R-0223 (Low, found in the R1 review): `.agent/last_block.md` held a stale
  block while a later round executed, so the round's order could not be
  audited against what was delivered.
  Done: R-0223 — every self-drive round since R2 saves its own block as its
  first commit (18b8ca7a, 5e2e242d, 61ba3056).

- R-0224 (Medium, found in the R2 review): R2's ledger bridge fed a COST-side
  count into a TOKEN-side invariant. `_stop_check` passed the ledger's
  `unpriced_call_count` into counters whose `provider_calls` is the run
  accumulator, and `BudgetCounters.__post_init__` raised whenever the former
  exceeded the latter. The two are counted from different sources and no
  invariant ties them: the accumulator counts attempts in THIS run and skips
  the fake provider, while the ledger holds one row per finalized task run
  across EVERY run of the job. The raise landed inside the ledger read's own
  broad `except`, so it was swallowed, the counters fell back to the no-cost
  path, and `--max-cost-usd` silently stopped enforcing for exactly the
  mixed-priced and resumed jobs the limit exists for.
  Done: R-0224 — fixed in 76be26d9 per DECISION F104 D5: `BudgetCounters`
  gains `priced_call_count`, the cross-source check is deleted outright (never
  clamped — understating the unpriced count would be the P6 failure in mirror
  image), the surviving contradiction check moves to the cost side, and
  `_stop_check` stops discarding the ledger's priced count. Pinned by 31a462d3.
  Reviewer-verified in the R3 review: restoring the deleted
  `unpriced_call_count > provider_calls` check in a disposable worktree turns
  exactly three tests RED — the model-level pin, the bridge pin, and
  `test_ledger_unpriced_count_above_this_runs_calls_still_enforces` at the live
  safe point — and nothing else.

## Steps

- R1: claim + candidate sweep + T001 — the `max_cost_usd` limit, the ledger
  cost bridge, the CLI flag and their tests. PASS at fc4929d5.
- R2: fix R-0222, add the predictive config keys and the pure prediction
  engine, register R-0222 and R-0223. PASS at 5ffd1178; gates A-D re-run by
  the reviewer (226 / 163 / 294 / 42) and three mutation red-proofs run in a
  disposable worktree. R-0224 found in that review.
- R3: fix R-0224 — the cost-side counter split, DECISION F104 D5. PASS at
  8b51fa63; gates A-D re-run by the reviewer (233 / 163 / 294 / 42) and the
  restore-the-invariant red-proof run in a disposable worktree.
- R4: T002 part 2 — delivered the counters-build refactor, the pure
  `derive_next_task_token_band` (DECISION F104 D6), the predictive wiring at the
  task-dispatch safe point with the `predicted_budget_exhausted:max_cost_usd`
  reason and the persisted `JobPlan.budget_prediction` arithmetic, both
  acceptance fixtures driven through the real `run_job`, the two inert-path
  regressions and the A9 seam pin. Awaiting review. The worker reports a
  pre-existing blocker it did not fix: `run_manifest._BUDGET_ALLOWED_KEYS`
  rejects `max_cost_usd`, so a budget stop cannot reach JOB_STOPPED.
