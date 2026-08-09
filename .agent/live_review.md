# Live Review — F104 Hard budget enforcement

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only; the worker applies
> them verbatim and marks `Done: R-XXXX` when a fix lands. Only reviewer-
> authored text sets Resolved.
> Branch: feature/f104-hard-budget-enforcement. Next free ID: R-0229.

## Findings

- R-0221 (Low, carried from F103 R5 through `.agent/candidates.md`):
  `TestAutoBuildBehavior::test_auto_build_runs_by_default` in
  `tests/ui_server/test_dashboard_contract.py` pops `REMEDY_UI_NO_AUTO_BUILD`
  and runs a real `npm install` + `npm run build` in whatever checkout it runs
  in, refreshing `apps/ui/dist` mtimes mid-suite. That costs every integration
  gate six or seven phantom base-only failures — F103 R5 measured seven, the F104
  R7 gate measured six — through the mtime comparison in
  `_frontend_is_stale()` (`ui_server.py:2748`).
  REGISTERED here, deliberately NOT fixed by F104: the code is not this
  feature's and AGENTS.md Scope Control bars the "while I'm here" edit. It is
  carried as a documented LOW risk to F104 closure
  (STATUS_closure_protocol.md precondition 1) and routed to the F252
  flake-debt follow-up class. The F104 integration gate attributes these six
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

- R-0225 (High, found in the R4 review): `max_cost_usd` was added to
  `JobBudgets` by F104 T001 but never added to
  `run_manifest._BUDGET_ALLOWED_KEYS`, which is a CLOSED schema. Every job
  carrying a money limit therefore fails its F012 run-manifest write with
  `ManifestError: manifest.budgets has unknown keys: ['max_cost_usd']`. On the
  stop path that surfaces as `StopFinalizationError` inside `_stop_job` AFTER
  `stop_reason` and `stop_source` are set but BEFORE the `JOB_STOPPED`
  checkpoint, so the job is left in `running` with no manifest and the stop
  request still pending. The consequence is total: `--max-cost-usd` cannot
  finalize a stop at all — not the new predictive one, and not the reactive one
  R2 built either. Reproduced by the reviewer at f9309bfe, with the predictive
  path fully inert and `budgets={"max_cost_usd": 100.0}` as the only limit.
  This is F104's own T001 gap, not a foreign defect: the field is this
  feature's, and a limit that cannot stop a job is not a limit.
  Done: R-0225 — fixed in 476376f0. `_BUDGET_ALLOWED_KEYS` widened by exactly
  one field and `max_cost_usd` given its own validation next to the integer
  loop (bool, str, non-numeric type, `math.isfinite`, strictly positive),
  mirroring `JobBudgets._validate_budget_fields`. Pinned by 947aad4f and
  8c8d6507. Reviewer-verified in the R5 review: removing `"max_cost_usd"` from
  `_BUDGET_ALLOWED_KEYS` in a disposable worktree at 549f2bac turns exactly 11
  tests RED — the nine schema pins in `TestRunManifestBudgetIdentity` plus BOTH
  live terminal-state tests, `test_a_predictive_stop_reaches_the_stopped_state`
  and `test_a_reactive_cost_stop_reaches_the_stopped_state` — and nothing else.
  The worktree was removed and pruned before the verdict.

- R-0226 (Medium, found in the R4 review): F104's live cost pins stop at the
  stop SIGNAL and never assert a terminal job state.
  `TestLiveSafePointReadsTheLedgerCost` in `tests/orchestration/test_budget_guard.py`
  asserts `signal.reason == "budget_exhausted:max_cost_usd"` and returns; no
  test in the feature drove a money-limited job to `JOB_STOPPED`. That is
  exactly why R-0225 — a cost limit that can never finalize — survived two
  reviewed rounds with green gates. The defect class is the R-0222 class one
  level up: R-0222 was an engine with no caller, this is a caller whose effect
  is never observed. A signal-only assertion cannot distinguish a working stop
  from a stop that raises three frames later.
  Done: R-0226 — fixed in 8c8d6507. The `strict=True` xfail was retired and the
  predictive terminal test strengthened to assert `run_manifest_error == ""` and
  `stop_error == ""` alongside `JOB_STOPPED`, so it proves finalization rather
  than a status string; a second run-level test now pins the REACTIVE cost stop
  end to end with the predictive path inert. Reviewer-verified: both tests are
  among the 11 that go RED when the R-0225 fix is reverted, which is the
  property their signal-only predecessors lacked. The R5 worker also observed
  the strict xfail flip to `XPASS(strict)` at 476376f0 — the fix landing before
  the marker was retired — which is independent evidence the assertion was load
  bearing rather than decorative.

- R-0227 (Low, found in the R6 review): the F103 ledger cost read that R6 added to
  `_cmd_job_budget` (`apps/cli/commands/job.py`) is wrapped in a bare
  `except Exception: pass`. A read that FAILS therefore renders exactly like a job
  whose provider reported no prices — `spent: not-measured`, `remaining:
  not-measured` — and nothing in either output says a read broke: the JSON
  `diagnostic` field belongs to the counters decode and stays null. The silence is
  an asymmetry inside one function rather than a considered choice: the
  prediction block twenty lines below reports its own failure as
  `unavailable (<Type>: <msg>)` and is pinned by
  `test_a_broken_prediction_degrades_to_one_unavailable_line`, and
  `run_job._build_budget_counters` — the read this one deliberately mirrors —
  logs the identical failure at ERROR with `exc_info=True`. The displayed value
  stays honest, which is why this is Low and not a P6 violation. The cost is that
  a misconfigured ledger project is indistinguishable from a provider that
  reports no prices, and that is the one diagnosis an operator who just hit a cost
  limit most needs to make.
  Done: R-0227 — fixed in d3fe8011. The ledger read's `except Exception: pass`
  became a handler that records `f"{type(exc).__name__}: {exc}"`, truncated to 160
  chars, BEFORE logging at ERROR with `exc_info=True`, and surfaces it as a
  `cost_read:` text line and a dedicated `cost_read_error` JSON key — deliberately
  NOT folded into `diagnostic`, which belongs to the counters decode, because one
  field standing for two unrelated failures is the defect in mirror image. `spent`
  and `remaining` are unchanged, so a genuinely unpriced job still renders
  `not-measured` with `cost_read_error` null and stays distinguishable from a broken
  read. Reviewer-verified in the R7 review: restoring the silent swallow in a
  disposable worktree at 103a854d turns exactly 2 tests RED —
  `test_a_failed_ledger_read_prints_a_cost_read_line_naming_the_error` and
  `test_a_failed_ledger_read_sets_cost_read_error_in_json` — and nothing else. The
  worktree was removed and pruned before the verdict.

- R-0228 (Low, found in the R9 review, 2026-08-09): the R4 round line under
  `## Steps` still carried the not-yet-reviewed marker although that review
  demonstrably happened — R-0225 and R-0226 are both recorded as "found in the R4
  review", and R5 was the repair round that fixed them. The R9 block set out to
  stop this branch merging into `main` claiming ungated rounds and cleared R6 and
  R7, but R4 carried the same stale marker and was missed. Nothing about the code
  or about any verdict is wrong; the defect is that the record on disk contradicts
  itself, and `.agent/live_review.md` is the artifact a later reader trusts about
  which rounds were gated. Registered here rather than swept into
  `.agent/candidates.md` because the correction is one reviewer-authored entry in
  the same file and the branch has not merged into `main` yet.
  Done: R-0228 — fixed in R10: the R4 line now reads PASS and names R-0225 and
  R-0226 as the findings that review produced. Reviewer-verified from the diff
  itself — after the repair commit the stale marker occurs zero times in this file,
  and the R4 line is the only round entry that commit touches.

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
  regressions and the A9 seam pin. PASS — that review is what produced R-0225 and
  R-0226; the stale not-yet-reviewed marker this line carried until R10 is corrected
  as R-0228. The worker reports a
  pre-existing blocker it did not fix: `run_manifest._BUDGET_ALLOWED_KEYS`
  rejects `max_cost_usd`, so a budget stop cannot reach JOB_STOPPED.
- R5: repair round — fix R-0225 (the manifest budget allowlist) and R-0226
  (terminal-state coverage), DECISION F104 D7. PASS at 549f2bac; gates A-E
  re-run by the reviewer (261 with ZERO xfailed / 163 / 294 / 42 / 124) and the
  revert-the-allowlist red-proof run in a disposable worktree: 11 RED, both
  terminal-state tests among them.
- R6: T003 — display and docs. `remedy job budget` gained the money limit, spent,
  remaining, the live next-task expectation with its `estimate_basis` label and the
  recorded stop arithmetic; the next-task selection rule was extracted to one helper and
  pinned against the live safe point; the basis label is pinned grep-style; the ist-doc
  `docs/system/job-budget-enforcement-v0.md` landed per DECISION F104 D8. PASS — gated in
  the closing session together with R7 and R8; see the reviewer-gate entry under R8.
- R7: repair + integration gate — R-0227 registered and fixed (the failed ledger
  read now logs at ERROR and surfaces `cost_read:` / `cost_read_error`, and a
  genuinely unpriced job is still distinguishable from a broken read), then the
  full suite run per docs/agents/integration_gate.md with evidence in
  `.agent/gate_f104_r7/`. PASS — gated in the closing session together with R6 and R8;
  see the reviewer-gate entry under R8.
- R8: CLOSURE per docs/roadmap/STATUS_closure_protocol.md. Final verdict on the
  feature: **PASS WITH RISKS** — every F104 finding (R-0222, R-0223, R-0224,
  R-0225, R-0226, R-0227) is Resolved with reviewer-authored text; the single
  remaining open finding R-0221 is a documented LOW risk that belongs to the F252
  flake-debt class, is not F104's code to fix under AGENTS.md Scope Control, and
  was attributed by controlled evidence at the R7 integration gate rather than
  chased.
- Reviewer gate on R6+R7+R8 (the closing session, 2026-08-09): PASS. Range
  `549f2bac..b5a241c3` read as a real diff; gates A-D re-run by the reviewer from the
  repo root with real exit codes — `tests/docs/` 294 passed, canary 42 passed,
  `test_job_budgets.py` + `test_predictive_budget.py` 210 passed, and
  `remedy integrity check --json` passed 5 of 5 — every number equal to the handback's.
  `cmp .agent/authored/f104-r8-1.md .agent/last_block.md` exit 0. The closure package
  `remedy-review-20260809-033908-READY_FOR_REVIEW.zip` was re-hashed on disk and its
  sha256 equals the one written into `docs/roadmap/STATUS.md`. R7's integration-gate
  evidence was checked directly rather than believed: the branch full-suite run records
  `EXIT_CODE=0` with an EMPTY `branch_failed.txt`, and `comm_base_only_failures.txt`
  holds six ids, all in `tests/ui_server/test_live_state.py` — the R-0221 class.
  Independent mutation red-proof of R6's `select_next_predictable_task`, run in a
  disposable worktree at b5a241c3 and removed and pruned before this verdict: deleting
  the `TASK_BLOCKED`/`TASK_FAILED` guard turns exactly two tests RED
  (`test_a_blocked_first_pending_task_has_no_next_task` and
  `test_a_failed_first_pending_task_has_no_next_task`) and nothing else, so the guard is
  load bearing rather than decorative. `LAST_REVIEWED_SHA` advances 549f2bac -> b5a241c3.
- Reviewer gate on R9 (the closing session's successor, 2026-08-09): PASS. Range
  `b5a241c3..8e651661` read as a real diff — five `.agent/` files and nothing else;
  `packages/`, `apps/`, `tests/`, `docs/`, `README.md` and `docs/roadmap/STATUS.md`
  byte-unchanged. The authored pairs 1, 2, 3, 4a and 4b are applied byte for byte:
  each TO string occurs exactly once, the superseded `attributes these seven` occurs
  zero times, and zero trailing-whitespace lines survive. Gates re-run by the
  reviewer from the repo root with real exit codes: `cmp` of the authored block
  against `.agent/last_block.md` exit 0, `tests/docs/` 294 passed, the golden-path
  canary 42 passed, `remedy integrity check --json` `"passed": true` with
  `"fail_count": 0` over 5 checks, `git status --porcelain` EMPTY, HEAD equal to
  `origin/feature/f104-hard-budget-enforcement`. R9 delivered exactly its block; the
  one thing its block did not cover is registered above as R-0228.
  `LAST_REVIEWED_SHA` advances b5a241c3 -> 8e651661.
- R10: register R-0228 and correct the stale R4 round marker. `.agent/` state only —
  no code, test, doc or `docs/roadmap/STATUS.md` byte changed.
- Reviewer gate on R10 (2026-08-09): PASS. Range `8e651661..16f1c375` read as a real
  diff — five `.agent/` files, nothing under `packages/`, `apps/`, `tests/`, `docs/`
  or `README.md`, and `docs/roadmap/STATUS.md` byte-unchanged. The registration commit
  46be4953 carries pairs 1-3 and contains no `Done:` text; the repair commit fb1daac0
  carries pairs 4-5 — the finding is registered before its fix is claimed, in that
  order, in two commits. Gates re-run by the reviewer from the repo root with real
  exit codes: `cmp .agent/authored/f104-r10-1.md .agent/last_block.md` exit 0,
  `tests/docs/` 294 passed, the golden-path canary 42 passed,
  `remedy integrity check --json` `"passed": true` with `"fail_count": 0` over 5
  checks, `Awaiting review` 0 occurrences in this file, zero trailing-whitespace
  lines, `git status --porcelain` EMPTY, HEAD equal to origin, and `git worktree list`
  showing the primary checkout alone. `LAST_REVIEWED_SHA` advances
  8e651661 -> 16f1c375.
- Terminating convention for this branch (reviewer, 2026-08-09): an on-disk round log
  cannot record the gate on the commit that writes it, so R11 — the round that writes
  this entry — is the LAST round here, and its own verdict is carried by
  `.agent/handoff.md`, the reviewer's completion report and PR #188 instead. A reader
  who finds no `Reviewer gate on R11` line below is reading the terminator, not a
  second instance of R-0228: R-0228 was a line that positively CLAIMED to be awaiting
  review while its review had demonstrably happened, which is a different defect from
  a final round whose verdict lives off the round log by construction. Registered as a
  closure candidate so the convention is written down once in
  docs/agents/planner_reviewer_prompt.md rather than re-derived on every branch.
