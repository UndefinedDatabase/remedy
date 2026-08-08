You are the WORKER for F104 R2 (SPLIT round) in the Remedy repository at /home/decodeux/Repos/remedy.

Read from disk BEFORE acting, in this order: AGENTS.md (highest authority), .agent/plan.md, .agent/live_review.md, .agent/handoff.md, docs/roadmap/features/T2_F104.md. Do not rely on anything in this prompt as a substitute for reading them.

You are the ONLY writer. The reviewer (the session that wrote this block) is read-only and re-runs every verification itself; your summary is never evidence. Never force-push. Never work on main. Never merge. Do not create a PR this round. `git add -A` is FORBIDDEN — stage exact paths only.

Branch: stay on `feature/f104-hard-budget-enforcement` (already checked out, tree clean at fc4929d5).
R1 verdict: PASS. LAST_REVIEWED_SHA = fc4929d5. Open findings entering this round: 3 (R-0221 carried, plus R-0222 and R-0223 which YOU register in item 2 below).

── STEP T002-part-1/2 — F104 ──────────────────────────────────
Goal:        Make the money limit actually enforceable at runtime
             (fix R-0222), then add the PURE predictive-cost engine
             and its config keys. The safe-point integration, the
             `predicted_budget_exhausted` stop reason and the two
             acceptance fixtures are R3 and are NOT in this round.
Bundle:      1 save this block · 2 register findings FIRST ·
             3 fix R-0222 (ledger cost reaches the guard) ·
             4 predictive config keys + resolver ·
             5 the pure prediction engine · 6 tests ·
             7 feature-file amendment + decisions · 8 state + handback
Change:      packages/orchestration/pingpong_job.py,
             packages/orchestration/budget_guard.py,
             packages/orchestration/budget_resolution.py,
             packages/orchestration/config.py,
             tests/orchestration/test_predictive_budget.py (new),
             tests/orchestration/test_budget_guard.py,
             docs/roadmap/features/T2_F104.md,
             .agent/** (last_block, live_review, plan, decisions,
             authored, handoff). NOTHING else.
Constraints: P6 — an unmeasured figure is NEVER rendered or computed
             as a measured zero. No price is ever invented. Do-not-touch
             from the feature file: calibration from history,
             per-task-class caps, burn-rate anomaly detection.
             AGENTS.md commit discipline: one logical step per commit,
             <500 INSERTIONS per commit (DECISION F104 D1).
Done when:   Gates A-D below all exit 0, tree clean, branch pushed,
             .agent/handoff.md rewritten.
Handback:    completion report + rewritten .agent/handoff.md
───────────────────────────────────────────────────────────────

## 1. SAVE THIS BLOCK (own commit, FIRST)

Save this entire prompt verbatim to `.agent/last_block.md` (it currently still holds the F103 R8 block — that staleness is finding R-0223). Commit exactly that one file:

    chore(f104): save the R2 step block

## 2. REGISTER THE FINDINGS (own commit, SECOND, before any code)

Findings persist before repairs so nothing is lost if this round dies.

Write the text between the BEGIN/END markers below — the marker lines themselves are NEVER content — to `.agent/authored/f104-r2-1.md`, then apply it as a COMPLETE replacement:

    cp .agent/authored/f104-r2-1.md .agent/live_review.md
    cmp .agent/authored/f104-r2-1.md .agent/live_review.md ; echo "cmp exit $?"

Record that exit code in the handback. Then commit exactly `.agent/authored/f104-r2-1.md` and `.agent/live_review.md`:

    docs(f104): register the dead-bridge and stale-block findings

--- BEGIN f104-r2-1 ---
# Live Review — F104 Hard budget enforcement

> Reviewer: the main session of a one-session self-drive build
> (docs/agents/self_drive_protocol.md). Worker: one delegated subagent per
> round. Findings are authored here by the reviewer only; the worker applies
> them verbatim and marks `Done: R-XXXX` when a fix lands. Only reviewer-
> authored text sets Resolved.
> Branch: feature/f104-hard-budget-enforcement. Next free ID: R-0224.

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

- R-0222 (Medium, found in the R1 review, F104 R2 fixes it):
  `collect_ledger_cost_for_job` in `packages/orchestration/budget_guard.py` has
  NO production caller. The live safe-point check builds its counters at
  `packages/orchestration/pingpong_job.py:1824` via
  `collect_counters_from_actuals(...)` without the `measured_cost_usd` and
  `unpriced_call_count` arguments R1 added, so at runtime `measured_cost_usd`
  is always None. `evaluate_budget` then takes its "no call reported a cost;
  cannot determine exhaustion" branch for every real job, and `--max-cost-usd`
  can never exhaust in production no matter what the ledger holds. R1's gates
  were green because every cost test constructs its counters by hand.
  This is the R-0220 class: a green gate is not a working feature, and the
  question a review must ask of new code is who calls it.
  The R1 handback did not declare the gap, which is the second half of the
  finding — `.agent/handoff.md` is the only return channel and an omission
  there is itself incomplete (planner_reviewer_prompt.md §4.8). The declared
  deviation list named the `remedy job budget` text renderer as deferred but
  said nothing about the bridge having no caller, so a reader of the handback
  would conclude the money limit enforces. It does not, yet.

- R-0223 (Low, found in the R1 review, F104 R2 fixes it):
  `.agent/last_block.md` still contained the F103 R8 closure block while F104
  R1 was executing, so the R1 step block exists nowhere on disk and the round's
  order cannot be audited against what was delivered. In the split workflow
  that file is the record of what was actually ordered
  (planner_reviewer_prompt.md §4.12); self-drive removes the relay, not the
  record. Every self-drive round saves its own block as its first commit.

## Steps

- R1: claim + candidate sweep + T001 — the `max_cost_usd` limit, the ledger
  cost bridge, the CLI flag and their tests. PASS at fc4929d5; gates A-D
  re-run by the reviewer (345 / 32 / 294 / 42 passed) and two mutation
  red-proofs run in a disposable worktree confirmed the boundary comparison
  and the P6 null-preservation are genuinely pinned.
- R2: fix R-0222 (ledger cost reaches the live guard), add the predictive
  config keys and the pure prediction engine, register R-0222 and R-0223.
  In flight.
- R3: T002 part 2 — the predictive check at the dispatch safe point, the
  `predicted_budget_exhausted:<limit>` stop reason, the decision entry
  carrying the arithmetic, and both acceptance fixtures.
--- END f104-r2-1 ---

## 3. FIX R-0222 — the ledger cost must reach the live guard

Read `packages/orchestration/pingpong_job.py` around the `_stop_check()` closure (near line 1823) and `packages/orchestration/job_evidence.py:65` (`_resolve_job_ledger_project_id`) before editing.

Facts established by the reviewer, verify them yourself rather than trusting this list:
- `job_evidence.py` already passes `ledger_project_id` / `ledger_job_id` into `write_evidence_bundle`, so a live run DOES write one ledger row per finalized task run. The read side is what is missing.
- `collect_ledger_cost_for_job(job_id=..., project_id=..., path=...)` returns `(measured_cost_usd, priced_call_count, unpriced_call_count)` and never raises on a missing ledger.
- `collect_counters_from_actuals` already accepts `measured_cost_usd=` and `unpriced_call_count=`.

Change `_stop_check()` so that it reads the job's real cost from the ledger and passes it into the counters. Requirements:

a. Resolve the ledger project the SAME way the write side does. Reuse `_resolve_job_ledger_project_id` from `packages/orchestration/job_evidence.py` rather than writing a second resolver — AGENTS.md "one spelling per concept" forbids the synonym. Import it lazily inside the function, matching the existing lazy-import style at that site.

b. The read must NEVER be able to break a run. A ledger read that raises for any reason leaves the cost at None and the run continues; a stop check is not the place a job dies. Wrap it the way `_record_finalized_call_in_ledger` wraps its own write (log the error, swallow it), and say in a one-line WHY comment above the call that budgets read a mirror and a broken mirror must not stop a healthy job.

c. Do NOT read the ledger when the job carries no cost limit. `_job_budgets` is in scope; when it is None or its `max_cost_usd` is None, skip the query entirely and keep the current behaviour byte for byte. A SQLite query per task for a limit nobody set is waste, and it also keeps every existing budget test on its current path.

d. Preserve P6 exactly: whatever `collect_ledger_cost_for_job` returns for the cost is passed straight through, None included. Never coerce, never default to 0.0.

Commit (source + its tests may land together only if the tests are in the same logical step; prefer source first, tests in item 6):

    fix(f104): read the ledger cost at the live budget safe point

## 4. PREDICTIVE CONFIG KEYS + RESOLVER

In `packages/orchestration/config.py`, add four `ConfigKeySpec` entries in the shape of the existing `budget.max_cost_usd` spec, placed adjacent to it:

- `budget.price_basis_usd_per_1k_tokens`, env `REMEDY_BUDGET_PRICE_BASIS_USD_PER_1K_TOKENS`, `value_type=float`, `default=None`, description "Provisional USD price per 1000 tokens used for cost predictions (F104; provisional until calibration)".
- `budget.class_default_tokens_low`, env `REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_LOW`, `value_type=int`, `default=8000`.
- `budget.class_default_tokens_medium`, env `REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_MEDIUM`, `value_type=int`, `default=32000`.
- `budget.class_default_tokens_high`, env `REMEDY_BUDGET_CLASS_DEFAULT_TOKENS_HIGH`, `value_type=int`, `default=120000`.

Each description ends with "(F104; provisional until calibration)" — the feature file requires these to be documented as provisional.

In `packages/orchestration/budget_resolution.py`, add ONE public resolver next to `resolve_job_budgets`:

    resolve_predictive_budget_config(*, config_path=None, project_root=None) -> PredictiveBudgetConfig

returning a frozen dataclass `PredictiveBudgetConfig` with fields `price_basis_usd_per_1k_tokens: float | None` and `class_default_tokens: dict[str, int]` keyed by the `TokenBand` values `"low"`, `"medium"`, `"high"`. Reuse the existing `_pos_float` / `_pos_int` validators and the same `cfg.get_value` + `ConfigSource.DEFAULT` handling the other resolvers use. The price basis stays None when unset — do not substitute a number.

Commit:

    feat(f104): add the provisional price-basis and class-default config keys

## 5. THE PURE PREDICTION ENGINE

In `packages/orchestration/budget_guard.py`, add a frozen dataclass and one function. This round adds NO caller for them — that is deliberate and R3 wires them at the dispatch safe point; say so in the module-level docstring or a WHY comment so the absence is documented where a reader would search for it (AGENTS.md "deliberate absences are documented").

    @dataclass(frozen=True)
    class BudgetPrediction:
        would_breach: bool
        estimate_basis: str
        band: str
        expected_tokens: int | None
        expected_cost_usd: float | None
        spent_cost_usd: float | None
        limit_usd: float | None
        arithmetic: str
        def to_json(self) -> dict[str, Any]: ...

    def predict_next_task_cost(budgets, counters, *, band, config) -> BudgetPrediction

Rules, all of which are acceptance criteria, not polish:

- `estimate_basis` is ALWAYS a non-empty label and is carried in `to_json`. Its values are exactly: `"class_default"` (a band was known and priced), `"class_default_missing_band"` (no band, so the LARGEST class default was used — over-stopping beats overspending, the feature file's A9 edge case), `"no_price_basis"` (no price basis configured), `"no_cost_limit"` (`budgets.max_cost_usd` is None), `"unpriced_spend"` (what has been spent so far is unknown). No other value.
- `would_breach` is True ONLY when a real number can be compared: basis is `class_default` or `class_default_missing_band`, and `spent + expected > limit`. Note `>` and not `>=` — the reactive check owns the exact-limit case and duplicating it here would make the two disagree about the boundary.
- Spent money: use `counters.measured_cost_usd` when it is not None. When it is None, spend is unknown AND the basis becomes `unpriced_spend` with `would_breach=False` — EXCEPT when `counters.provider_calls == 0`, where a job that has made no provider call has definitionally spent nothing, so spend is 0.0 and prediction proceeds. Write the one-line WHY for that exception directly above it.
- Never invent a price. With `config.price_basis_usd_per_1k_tokens` None, the basis is `no_price_basis`, `expected_cost_usd` is None, `would_breach` is False, and `arithmetic` says the price basis is unset. This is the honest default and it makes the predictive path inert until an operator configures a price.
- `expected_cost_usd = expected_tokens / 1000 * price_basis`.
- `band` accepts the `TokenBand` values from `packages/orchestration/token_economy.py` (`"low"`, `"medium"`, `"high"`, `"unknown"`); `"unknown"`, None, or any unrecognised string all mean "no band" and take the largest-class-default path. Import `TokenBand` rather than re-spelling the literals.
- `arithmetic` is a single human-readable line carrying spent, expected, limit and basis — the feature file requires a human to see WHY. Example shape: `spent $1.2000 + expected $0.9000 (32000 tokens, band=medium, basis=class_default) > limit $2.0000`. When a figure is unknown it is rendered as `not-measured`, never as `$0.0000`.
- Keep `budget_guard.py` import-light exactly as its existing comment demands: import `TokenBand` and `PredictiveBudgetConfig` lazily inside the function if a module-level import would drag in config/SQLite machinery. Check first; do not add a lazy import you do not need.

Commit:

    feat(f104): add the predictive next-task cost engine

## 6. TESTS

New file `tests/orchestration/test_predictive_budget.py` (the name the feature file suggests). Cover, at minimum:

- every one of the five `estimate_basis` values, each asserting both the basis and `would_breach`;
- the just-under case: spent + expected > limit → `would_breach` True;
- the just-over-limit-already case and the exact-boundary case (`spent + expected == limit` → `would_breach` False, because the reactive check owns that boundary);
- missing/unknown band → the LARGEST class default is used and the basis says the band was missing;
- `price_basis` unset → inert, `expected_cost_usd is None`, and the arithmetic string does not contain `$0.0000`;
- unknown spend with provider calls > 0 → `unpriced_spend`, no breach; unknown spend with zero provider calls → treated as 0.0 and prediction proceeds;
- `to_json` carries `estimate_basis` (this is the grep-style pin the feature file's T003 will extend);
- `resolve_predictive_budget_config` — defaults when nothing is configured, and TOML/env override precedence for the price basis, following the existing patterns in `tests/orchestration/test_job_budgets.py`.

Extend `tests/orchestration/test_budget_guard.py` with a test that the R-0222 fix is real: assert that the pingpong safe-point path passes ledger cost into the counters. Prefer a test that exercises `_stop_check` behaviour over one that greps source text; if the closure is genuinely not reachable from a test, state that in the handback and pin it with the narrowest honest alternative, naming why.

Commit:

    test(f104): cover the prediction engine and the live ledger read

## 7. FEATURE-FILE AMENDMENT + DECISIONS (reviewer-authored, apply verbatim)

The spec assumes tasks carry a band; they do not — `JobTask` has no band field and `TokenBand` lives in `token_economy.py`. That is a wrong-spec finding routed to planning per planner_reviewer_prompt.md §4.7, and the reviewer has already chosen the option. Apply the amendment.

Write the text between the markers to `.agent/authored/f104-r2-2.md`. It is ONE FROM→TO pair, a REWRITE, against `docs/roadmap/features/T2_F104.md`. The FROM occurs exactly 1x. Report FROM 1x / TO 0x before and FROM 0x / TO 1x after.

--- BEGIN f104-r2-2 ---
FROM:
- Predictive check at the task-dispatch safe point: expected =
  band→tokens class default × configured price basis; if spent +
  expected > limit → the standard stop path with reason
  predicted_budget_exhausted:<limit> + a decision entry carrying the
  arithmetic (spent, expected, basis) so the human sees WHY.

TO:
- Predictive check at the task-dispatch safe point: expected =
  band→tokens class default × configured price basis; if spent +
  expected > limit → the standard stop path with reason
  predicted_budget_exhausted:<limit> + a decision entry carrying the
  arithmetic (spent, expected, basis) so the human sees WHY.
  DECISION F104 D3 (2026-08-09): a JobTask carries no band field, so
  the band is DERIVED at the safe point from
  token_economy.estimate_task_token_band() over the next task's context
  estimate; a task whose band cannot be derived takes the A9 path below.
  DECISION F104 D4 (2026-08-09): the price basis has NO default. With
  none configured the predictive path is inert and labels itself
  estimate_basis=no_price_basis — Remedy invents no price (P6), and an
  invented one would make every prediction a fabrication.
--- END f104-r2-2 ---

Then append the matching entry to `.agent/decisions.md`. Write the text between the markers to `.agent/authored/f104-r2-3.md` and append it verbatim to the END of `.agent/decisions.md`, separated by exactly one blank line. Verify the heading line occurs exactly 1x afterwards.

--- BEGIN f104-r2-3 ---
## DECISION F104 D3 + D4 — predicted cost has a derived band and no invented price (2026-08-09)

Context: T2_F104's Design says expected cost is "band→tokens class default ×
configured price basis", which reads as though a task carries a band. It does
not: `JobTask` has no band field, and the only band vocabulary in the repo is
`TokenBand` (low/medium/high/unknown) in
`packages/orchestration/token_economy.py`, alongside
`estimate_task_token_band(task_type, context_estimate)`.

D3 — the band is DERIVED, not stored. The predictive check derives the band at
the dispatch safe point from `estimate_task_token_band()` over the next task's
context estimate. Alternatives considered: (a) add a `band` field to `JobTask`
— rejected, it changes a persisted model and every plan written before it would
carry a null anyway, which is the same missing-band case with more migration;
(b) always use the largest class default — rejected as needlessly blunt when a
context estimate exists. A task whose band cannot be derived takes the feature
file's own A9 path: the LARGEST class default, with the basis label saying the
band was missing, because over-stopping beats overspending.

D4 — the price basis has no default. `budget.price_basis_usd_per_1k_tokens` is
unset unless an operator sets it; with it unset the predictive path is inert and
labels itself `estimate_basis=no_price_basis`. Alternative considered: ship a
plausible default price — rejected under P6. A default price is a number nobody
measured, and every prediction derived from it would be a fabrication wearing an
honest label. An inert predictor is safe because the reactive check is the
backstop and is unchanged.

Reverse either decision by deleting its half of this entry and the matching
lines in `docs/roadmap/features/T2_F104.md`.
--- END f104-r2-3 ---

Commit (feature file + decisions + both authored files together — one logical step):

    docs(f104): record the derived-band and no-default-price decisions

## 8. GATES, STATE, HANDBACK

Run all four and record the REAL command, trimmed output and REAL exit code:

    A  python3 -m pytest tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py -q
    B  python3 -m pytest tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_stop_reasons.py -q
    C  python3 -m pytest tests/docs/ -q
    D  python3 -m pytest tests/cli/test_golden_path.py -q

Gate C is mandatory because this round's change set includes `docs/roadmap/**` (planner_reviewer_prompt.md §3, docs-round gate). Gate D is the canary. A red gate is a STOP: hand back the raw output and do not paper over it. Do not run the full suite — that is the R4 integration gate, not this round.

Any deliberately destructive verification (mutation red-proofs) runs ONLY inside a disposable `git worktree`; the primary checkout must satisfy `git status --porcelain` == empty at handback. Put any worktree under `.remedy-wt/` (gitignored) — writes to /tmp are denied on this machine — and remove it before you finish.

Then rewrite `.agent/plan.md` from the text below (`.agent/authored/f104-r2-4.md`, applied by `cp`, then `cmp`, record the exit code). Do NOT touch `.agent/context.md` — scope, branch and constraints are unchanged from R1 and rewriting it risks its multi-test contract for no gain.

--- BEGIN f104-r2-4 ---
# Plan — F104 Hard budget enforcement

Branch: feature/f104-hard-budget-enforcement, cut from main at 94f69b0f after
PR #187 — the F103 closure — was merged at the Open PR Gate. Build mode:
one-session self-drive (docs/agents/self_drive_protocol.md), one delegated
worker per round. Open findings: 3 — R-0221 (Low, carried, not F104's to fix),
R-0222 (Medium, fixed in R2), R-0223 (Low, fixed in R2).
Next free ID: R-0224.

## Goal
Budgets grow teeth and foresight. A money limit `max_cost_usd` joins the F018
limits under the same precedence rules; the counters read real cost actuals out
of the F103 SQLite ledger with the unpriced notation surviving the trip; and a
PREDICTIVE check at the task-dispatch safe point stops BEFORE a task that would
breach the limit, recording the arithmetic that justified the stop. The
reactive check stays exactly as it is — prediction never replaces the backstop.

## Current Step
R2 — T002 part 1: fix R-0222 so the ledger cost reaches the live safe-point
guard, add the provisional price-basis and class-default config keys with their
resolver, and add the PURE prediction engine (`BudgetPrediction`,
`predict_next_task_cost`) with its tests. The engine has no caller until R3 —
that is stated in the code and here, so it is a scheduled absence and not the
R-0222 mistake repeating.

## Next Steps
- R3 — T002 part 2: derive the band at the dispatch safe point per DECISION
  F104 D3, wire `predict_next_task_cost` in BEFORE the next task is dispatched,
  add the `predicted_budget_exhausted:<limit>` stop reason and the decision
  entry carrying the arithmetic, and both acceptance fixtures — just-under, and
  prediction-wrong proving the reactive backstop still fires.
- R4 — T003: display and docs; every user-facing predicted number carries its
  `estimate_basis` label, pinned by a grep-style test.
- R5 — integration gate per docs/agents/integration_gate.md.
- R6/R7 — closure per docs/roadmap/STATUS_closure_protocol.md.

## Risks
- Cost is NULLABLE by design (P6): the ledger stores NULL for an unpriced call
  and nothing may render that as a measured zero. Every new figure keeps the
  None and says so.
- Predictions come from documented class defaults, not calibration.
  `estimate_basis=class_default` is an acceptance criterion, not polish.
- R-0221 costs the integration gate seven phantom base-only failures.
  Attribute them, do not chase them.
- The live ledger read happens inside a stop check. It is guarded and cheap
  (skipped entirely when no cost limit is set), but any regression there is a
  regression in the stop path — the most safety-critical code in the job loop.
--- END f104-r2-4 ---

Rewrite `.agent/handoff.md` (rewrite, never append). It MUST carry, per AGENTS.md:
- feature + round, branch, every commit SHA in order, and that this was a SPLIT round with no verdict, no PR, no merge;
- a per-commit changed-files table with `+/-` and a reason per path;
- the transport proofs: the `cmp` exit codes for f104-r2-1 and f104-r2-4, the before/after FROM/TO counts for the f104-r2-2 REWRITE pair, and the 1x heading check for the f104-r2-3 append;
- the verification table with the REAL trimmed output and REAL exit codes for gates A-D;
- an item-status table covering bundle items 1-8, each exactly once, with `done` / `skipped` (reason) / `deviated` (reason);
- open-findings count and which findings this round marked `Done:`;
- the final `git status --porcelain` result;
- next expected action;
- a "Deviations, declared" section naming ANY departure from this block, including its own line count if it exceeds 60 lines and why.

Declare in the handback, explicitly, whether `predict_next_task_cost` has a production caller at the end of this round. It does not, by design, and R3 adds one — saying so is what stops R-0222 from recurring silently.

Finally: commit the state files, `git push`, and confirm `git status --porcelain` is empty. Do NOT create a PR. Do NOT merge anything. Do NOT run `gh pr merge`.

Every commit message ends with the trailer:
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

Commit subjects must not contain leading-slash tokens, absolute paths, or secret-like strings — the evidence metadata scanner rejects them.

If anything in this block contradicts AGENTS.md, AGENTS.md wins and you hand back naming the contradiction instead of guessing. If a gate goes red and the fix is not obviously inside this round's change set, STOP and hand back with the raw output rather than widening scope.
