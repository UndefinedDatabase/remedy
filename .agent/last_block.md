You are the WORKER for F104 R3 (SPLIT round) in the Remedy repository at /home/decodeux/Repos/remedy.

Read from disk BEFORE acting, in this order: AGENTS.md (highest authority), .agent/plan.md, .agent/live_review.md, .agent/handoff.md, .agent/last_block.md, docs/roadmap/features/T2_F104.md. Do not rely on anything in this prompt as a substitute for reading them.

You are the ONLY writer. The reviewer (the session that wrote this block) is read-only, re-runs every verification itself and has already run its own mutation red-proofs; your summary is never evidence. Never force-push. Never work on main. Never merge. Do not create a PR this round. `git add -A` is FORBIDDEN — stage exact paths only.

Branch: stay on `feature/f104-hard-budget-enforcement` (already checked out, tree clean at 5ffd1178).
R2 verdict: PASS. LAST_REVIEWED_SHA = 5ffd1178. The reviewer re-ran gates A-D (226 / 163 / 294 / 42 passed, all exit 0) and confirmed three mutation red-proofs: reverting the R-0222 fix → 4/5 live tests RED; `_ledger_cost or 0.0` → the P6 test RED; `>` → `>=` → only the exact-boundary test RED.

── STEP T002-fix — F104 R3 ────────────────────────────────────
Goal:        Close R-0224, the cross-source counter defect that R2's own
             ledger bridge introduced. Today a `--max-cost-usd` job whose
             ledger holds more unpriced rows than the run accumulator has
             counted provider calls raises `BudgetCounterError` INSIDE the
             R2 try-block, gets it swallowed, and silently falls back to
             counters with no cost at all — the money limit stops enforcing
             for exactly the mixed-priced jobs it exists for.
Bundle:      1 save this block · 2 register findings FIRST ·
             3 the cost-side counter fix · 4 decision entry ·
             5 tests · 6 gates, state, handback
Change:      packages/orchestration/budget_guard.py,
             packages/orchestration/pingpong_job.py,
             tests/orchestration/test_budget_guard.py,
             .agent/** (last_block, live_review, decisions, plan, authored,
             handoff). NOTHING else. The task-dispatch wiring, the
             `predicted_budget_exhausted` stop reason and the acceptance
             fixtures remain R4 and are NOT in this round.
Constraints: P6 — an unmeasured figure is NEVER rendered or computed as a
             measured zero, and an unpriced call count is never quietly
             reduced to make a validator happy. AGENTS.md commit discipline:
             one logical step per commit, <500 INSERTIONS per commit
             (DECISION F104 D1). Do NOT touch `.agent/context.md`.
Done when:   Gates A-D below all exit 0, tree clean, branch pushed,
             .agent/handoff.md rewritten.
Handback:    completion report + rewritten .agent/handoff.md
───────────────────────────────────────────────────────────────

## 1. SAVE THIS BLOCK (own commit, FIRST)

Save this entire prompt verbatim to `.agent/last_block.md`, replacing the R2 continuation block (preserved in git history at 5e2e242d). Commit exactly that one file:

    chore(f104): save the R3 step block

## 2. REGISTER THE FINDINGS (own commit, SECOND, before any code)

Findings persist before repairs so nothing is lost if this round dies.

Write the text between the BEGIN/END markers below — the marker lines themselves are NEVER content — to `.agent/authored/f104-r3-1.md`, then apply it as a COMPLETE replacement:

    cp .agent/authored/f104-r3-1.md .agent/live_review.md
    cmp .agent/authored/f104-r3-1.md .agent/live_review.md ; echo "cmp exit $?"

Record that exit code in the handback. Then commit exactly `.agent/authored/f104-r3-1.md` and `.agent/live_review.md`:

    docs(f104): register the cross-source counter finding

--- BEGIN f104-r3-1 ---
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
  first commit (18b8ca7a, 5e2e242d, and this round's own save).

- R-0224 (Medium, found in the R2 review; F104 R3 fixes it):
  R2's ledger bridge feeds a COST-side count into a TOKEN-side invariant.
  `_stop_check` in `packages/orchestration/pingpong_job.py` passes the ledger's
  `unpriced_call_count` into `collect_counters_from_actuals`, while
  `BudgetCounters.provider_calls` is the run accumulator
  `_accumulated_provider_calls`. `BudgetCounters.__post_init__`
  (`budget_guard.py:137`) then raises `BudgetCounterError` whenever
  `unpriced_call_count > provider_calls`.
  The two numbers are counted from DIFFERENT sources and no invariant ties
  them: the accumulator counts attempts and skips every attempt whose provider
  is `"fake"` (`pingpong_job.py:1810`), while the ledger holds one row per
  finalized task run that carried provider evidence, across ALL runs of the
  job including runs whose `budget_actuals` were never persisted.
  The raise happens INSIDE the broad `except Exception` that R2 added for the
  ledger read, so it is swallowed, `counters` falls back to the no-cost path,
  and `--max-cost-usd` silently stops enforcing for precisely the mixed-priced
  and resumed jobs the limit was added for. Reviewer-reproduced:
  `collect_counters_from_actuals({"provider_call_count": 0, ...},
  measured_cost_usd=None, unpriced_call_count=3)` raises
  `BudgetCounterError: unpriced_call_count (3) > provider_calls (0)`.
  This is the R-0220 class once more — a green gate over a path production
  never takes — and the swallow is what made it invisible.
  The root cause is narrower than it looks: R2 discarded the priced count the
  ledger already returns (`_ledger_cost, _, _ledger_unpriced`) and then
  validated the surviving half against an unrelated counter. The cost side
  should be validated against the cost side.

## Steps

- R1: claim + candidate sweep + T001 — the `max_cost_usd` limit, the ledger
  cost bridge, the CLI flag and their tests. PASS at fc4929d5.
- R2: fix R-0222, add the predictive config keys and the pure prediction
  engine, register R-0222 and R-0223. PASS at 5ffd1178; gates A-D re-run by
  the reviewer (226 / 163 / 294 / 42) and three mutation red-proofs run in a
  disposable worktree. R-0224 found in that review.
- R3: fix R-0224 — the cost-side counter split. In flight.
- R4: T002 part 2 — derive the band at the dispatch safe point per DECISION
  F104 D3, wire `predict_next_task_cost` in, add the
  `predicted_budget_exhausted:<limit>` stop reason and the decision entry
  carrying the arithmetic, and both acceptance fixtures.
--- END f104-r3-1 ---

## 3. THE COST-SIDE COUNTER FIX

Read `packages/orchestration/budget_guard.py` lines 40-200 and the `_stop_check` closure in `packages/orchestration/pingpong_job.py` before editing.

The design decision is the reviewer's and is not yours to re-open; implement it. If implementing it reveals it is wrong, STOP and hand back saying why rather than substituting a different design.

a. `BudgetCounters` gains a field `priced_call_count: int = 0`, declared next to `unpriced_call_count`, with the same bool/non-negative-int validation the other count fields get. Give it the one-line WHY: the cost-side call counts come from the F103 ledger and are counted per finalized task run, while `provider_calls` counts attempts in this run — they are different measurements of different things and must never be compared.

b. DELETE the `unpriced_call_count > provider_calls` check (`budget_guard.py:137-140`). It is the defect. Do not replace it with a clamp, a `min()`, or any other quiet reduction of the unpriced count: understating how many calls went unpriced would make the data look better measured than it is, which is the P6 failure in mirror image.

c. REPLACE the "all provider calls are unpriced but a cost was reported" check (`budget_guard.py:141-149`) with its cost-side equivalent: raise when `measured_cost_usd is not None and measured_cost_usd > 0 and priced_call_count == 0 and unpriced_call_count > 0`. The message should name the cost-side counts, not `provider_calls`. This keeps the real contradiction it was guarding against — money reported with nothing priced to explain it — while dropping the cross-source comparison.

d. Add `priced_call_count` to `BudgetCounters.to_json()`.

e. `collect_counters_from_actuals` gains a `priced_call_count: int = 0` keyword parameter alongside the existing `measured_cost_usd` / `unpriced_call_count`, passed straight through, and its docstring mentions it in the same breath as the other F104 money actuals.

f. In `_stop_check`, stop discarding the ledger's priced count. R2 wrote `_ledger_cost, _, _ledger_unpriced = _collect_ledger_cost(...)`; bind all three and pass `priced_call_count=` through to `collect_counters_from_actuals` next to the other two. Change nothing else about that closure — the skip-when-no-cost-limit guard, the broad swallow and the P6 pass-through all stay exactly as they are.

Commit:

    fix(f104): count priced and unpriced calls on the cost side

## 4. DECISION ENTRY

Write the text between the markers to `.agent/authored/f104-r3-2.md` and append it verbatim to the END of `.agent/decisions.md`, separated by exactly one blank line. Verify the heading line occurs exactly 1x afterwards.

--- BEGIN f104-r3-2 ---
## DECISION F104 D5 — cost-side call counts are validated against the cost side (2026-08-09)

Context: finding R-0224. `BudgetCounters` carried a single call-count invariant,
`unpriced_call_count <= provider_calls`, written when every counter came from one
source: the run accumulator in `pingpong_job.run_job`. F104's ledger bridge broke
that assumption by feeding `unpriced_call_count` from the F103 SQLite ledger while
`provider_calls` kept counting attempts in the current run. The two disagree
legitimately — the accumulator skips `provider == "fake"` attempts and starts from
whatever `budget_actuals` were persisted, the ledger holds one row per finalized
task run across every run of the job — so the invariant fired on healthy data.

D5 — the counter object now carries BOTH cost-side counts, `priced_call_count` and
`unpriced_call_count`, and the cross-source check is gone. What survives is the
cost-side contradiction check: a positive `measured_cost_usd` with nothing priced
to explain it is still an error.

Alternatives considered: (a) clamp the unpriced count to `provider_calls` —
rejected, it understates how many calls went unpriced, which dresses poorly
measured data as well measured and is the P6 failure in mirror image; (b) stop
passing `unpriced_call_count` from the ledger at all — rejected, the unpriced
notation surviving the trip is an F104 acceptance criterion, and dropping it would
make `cost_description` claim a precision it does not have; (c) widen
`provider_calls` to the ledger total — rejected, `provider_calls` is the basis of
the `max_provider_calls` limit and moving it would change an unrelated F018 limit.

Why it matters beyond the bug: the raise was swallowed by the ledger read's own
broad `except Exception`, so the failure mode was not a crash but a silent
downgrade to "no cost known" — the money limit quietly ceasing to enforce for
exactly the mixed-priced jobs it was added for.

Reverse this decision by restoring the `unpriced_call_count > provider_calls`
check and dropping `priced_call_count`.
--- END f104-r3-2 ---

Commit (decisions + authored file together):

    docs(f104): record the cost-side counter decision

## 5. TESTS

In `tests/orchestration/test_budget_guard.py`:

a. `test_unpriced_count_above_provider_calls_rejected` (around line 497) asserts the invariant this round deliberately removes. REPLACE it with a test asserting the new behaviour: an unpriced count above `provider_calls` is ACCEPTED and preserved exactly, with a comment naming R-0224 and DECISION F104 D5 so a future reader does not "restore" the old check. Do not simply delete the test.

b. Add `priced_call_count` coverage: validation (bool rejected, negative rejected), it appears in `to_json()`, and the new cost-side contradiction check raises when `measured_cost_usd > 0` with `priced_call_count == 0` and `unpriced_call_count > 0`, and does NOT raise when `priced_call_count > 0`.

c. Add to `TestLiveSafePointReadsTheLedgerCost` the case that proves R-0224 is closed at the LIVE safe point, in the style of the tests already there (assert on the recorded `collect_counters_from_actuals` kwargs, and drive the real `run_job`): a ledger result whose unpriced count EXCEEDS the run's provider-call count — for example `(4.0, 2, 3)` with a fresh job — must reach the guard with `measured_cost_usd == 4.0`, `priced_call_count == 2`, `unpriced_call_count == 3`, and must STOP a job whose `max_cost_usd` is below it. Before the fix this case was swallowed and no cost reached the guard at all; say so in the test's comment.

Prove the new tests are real pins before you commit: temporarily reintroduce the deleted `unpriced_call_count > provider_calls` check in a DISPOSABLE `git worktree` under `.remedy-wt/` (gitignored — writes to /tmp are denied on this machine), confirm the R-0224 test goes RED, and remove the worktree. Report the red-proof output and exit code in the handback. The primary checkout must satisfy `git status --porcelain` == empty at handback.

Commit:

    test(f104): pin the cost-side counter split at the live safe point

## 6. GATES, STATE, HANDBACK

Run all four and record the REAL command, trimmed output and REAL exit code:

    A  python3 -m pytest tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py -q
    B  python3 -m pytest tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_stop_reasons.py -q
    C  python3 -m pytest tests/docs/ -q
    D  python3 -m pytest tests/cli/test_golden_path.py -q

Gate B matters more than usual this round: it exercises the stop path whose counter model you changed. Gate D is the canary. A red gate is a STOP: hand back the raw output and do not paper over it. Do not run the full suite — that is the R5 integration gate, not this round.

`BudgetCounters` is a shared model. Before you finish, grep for every construction site and every reader of `unpriced_call_count` across `packages/`, `apps/` and `tests/`, and report in the handback what you found and why each is unaffected. If any site outside this block's change list DOES need a change, STOP and hand back — do not widen scope.

Then rewrite `.agent/plan.md`: it must state R3 as the current step (the R-0224 cost-side counter fix), renumber the remaining steps so the T002 part-2 wiring is R4, display and docs R5, the integration gate R6 and closure R7/R8, and record open findings as 4 total with R-0222, R-0223 and R-0224 marked done and R-0221 carried. Keep it under 50 lines and keep the existing Goal and Risks sections, adding a risk line for the shared-counter-model change. Write it to `.agent/authored/f104-r3-3.md` first, apply by `cp`, then `cmp` and record the exit code.

Do NOT touch `.agent/context.md`.

Rewrite `.agent/handoff.md` (rewrite, never append). It MUST carry, per AGENTS.md: feature + round; branch; every commit SHA in order and that this was a SPLIT round with no verdict, no PR, no merge; a per-commit changed-files table with `+/-` and a reason per path; the transport proofs (the `cmp` exit codes for f104-r3-1 and f104-r3-3, and the 1x heading check for the f104-r3-2 append); the verification table with REAL trimmed output and REAL exit codes for gates A-D; the red-proof result for the reintroduced invariant; the `BudgetCounters` construction-site survey; an item-status table covering bundle items 1-6, each exactly once, with `done` / `skipped` (reason) / `deviated` (reason); open-findings count and which findings this round marked `Done:`; the final `git status --porcelain` result; next expected action; and a "Deviations, declared" section naming ANY departure from this block, including its own line count if it exceeds 60 lines and why.

Declare explicitly whether `predict_next_task_cost` has a production caller at the end of this round. It does not — R4 adds one.

Finally: commit the state files, `git push`, and confirm `git status --porcelain` is empty. Do NOT create a PR. Do NOT merge anything. Do NOT run `gh pr merge`.

Every commit message ends with the trailer:
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

Commit subjects must not contain leading-slash tokens, absolute paths, or secret-like strings — the evidence metadata scanner rejects them.

If anything in this block contradicts AGENTS.md, AGENTS.md wins and you hand back naming the contradiction instead of guessing. If a gate goes red and the fix is not obviously inside this round's change set, STOP and hand back with the raw output rather than widening scope.

Your final message is your completion report: the item-status table, the real gate results with exit codes, the commit SHAs, the transport proofs, the red-proof, the construction-site survey, and your declared deviations.
