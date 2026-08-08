You are the WORKER for F104 R2-continuation (SPLIT round) in the Remedy repository at /home/decodeux/Repos/remedy.

Read from disk BEFORE acting, in this order: AGENTS.md (highest authority), .agent/plan.md, .agent/live_review.md, .agent/handoff.md, .agent/last_block.md (it currently holds the ORIGINAL R2 block — read it in full, it is your specification for items 7 and 8), docs/roadmap/features/T2_F104.md. Do not rely on anything in this prompt as a substitute for reading them.

You are the ONLY writer. The reviewer (the session that wrote this block) is read-only and re-runs every verification itself; your summary is never evidence. Never force-push. Never work on main. Never merge. Do not create a PR this round. `git add -A` is FORBIDDEN — stage exact paths only.

Branch: stay on `feature/f104-hard-budget-enforcement` (already checked out, HEAD = ef9a852c).

── WHY THIS BLOCK EXISTS ──────────────────────────────────────
The previous R2 worker session ended mid-round without a handback. Items 1-5 of
the original R2 block ARE committed (18b8ca7a, ab77b2b5, c6994fa8, 0f195a60,
ef9a852c). Item 6 is HALF-WRITTEN AND UNCOMMITTED: `git status --porcelain`
currently reports ` M tests/orchestration/test_budget_guard.py`, a +119-line
addition of `class TestLiveSafePointReadsTheLedgerCost`. Items 7 and 8 are
untouched. You finish items 6, 7 and 8 and hand back. You do NOT redo items 1-5.
───────────────────────────────────────────────────────────────

── STEP T002-part-1/2 (continuation) — F104 R2 ────────────────
Goal:        Finish R2: pin the R-0222 fix with a live test, cover the pure
             prediction engine, apply the reviewer-authored feature-file and
             decisions text, run the gates, and hand back. The safe-point
             integration, the `predicted_budget_exhausted` stop reason and the
             two acceptance fixtures remain R3 and are NOT in this round.
Bundle:      1 save this block · 2 commit the pending live-ledger test ·
             3 the prediction-engine test file · 4 feature-file amendment +
             decisions · 5 gates, state, handback
Change:      tests/orchestration/test_budget_guard.py,
             tests/orchestration/test_predictive_budget.py (new),
             docs/roadmap/features/T2_F104.md,
             .agent/** (last_block, decisions, plan, authored, handoff).
             NOTHING else. In particular: no further edits to
             packages/orchestration/** unless a gate goes red and the fix is
             unambiguously inside R2's own change set — if it is not, STOP and
             hand back with the raw output.
Constraints: P6 — an unmeasured figure is NEVER rendered or computed as a
             measured zero. No price is ever invented. Do-not-touch from the
             feature file: calibration from history, per-task-class caps,
             burn-rate anomaly detection. AGENTS.md commit discipline: one
             logical step per commit, <500 INSERTIONS per commit
             (DECISION F104 D1). Do NOT touch `.agent/context.md`.
Done when:   Gates A-D below all exit 0, tree clean, branch pushed,
             .agent/handoff.md rewritten.
Handback:    completion report + rewritten .agent/handoff.md
───────────────────────────────────────────────────────────────

## 1. SAVE THIS BLOCK (own commit, FIRST)

Save this entire prompt verbatim to `.agent/last_block.md`, replacing the original R2 block (that block is preserved in git history at commit 18b8ca7a, and finding R-0223 requires the file to hold the block currently in force). Commit exactly that one file:

    chore(f104): save the R2 continuation block

## 2. COMMIT THE PENDING LIVE-LEDGER TEST (own commit, SECOND)

`tests/orchestration/test_budget_guard.py` already carries an uncommitted `class TestLiveSafePointReadsTheLedgerCost` written by the previous session. It is INHERITED WORK, not verified work. Before you commit it:

a. Read the full added block with `git diff tests/orchestration/test_budget_guard.py` and read the surrounding file so you understand its conventions.
b. Run it yourself: `python3 -m pytest tests/orchestration/test_budget_guard.py -q -k LiveSafePoint` and record the REAL output and exit code.
c. Satisfy yourself it is a REAL pin of the R-0222 fix and not a tautology — it must drive `pingpong_job.run_job`'s pre-work safe point, not grep source text. Confirm the five cases it claims: over-limit stops, under-limit does not, an unpriced ledger keeps the cost null and does not stop, no cost limit never queries the ledger, and a raising ledger read never stops a healthy job.
d. If any part of it is wrong, misleading, or does not actually exercise `_stop_check`, FIX it and say exactly what you changed and why in the handback. If it is sound as inherited, say that explicitly — "inherited unchanged, verified by running it" — rather than silently passing it off as your own.

Then stage exactly that one path and commit:

    test(f104): pin the live ledger read at the budget safe point

## 3. THE PREDICTION-ENGINE TEST FILE (own commit, THIRD)

New file `tests/orchestration/test_predictive_budget.py`. Read `packages/orchestration/budget_guard.py` (`BudgetPrediction`, `predict_next_task_cost`, `VALID_ESTIMATE_BASES`) and `packages/orchestration/budget_resolution.py` (`PredictiveBudgetConfig`, `resolve_predictive_budget_config`) first — test what the code DOES, and if what it does contradicts the rules below, that is a finding for the handback, not something you quietly adjust the test to accept.

Cover, at minimum:

- every one of the five `estimate_basis` values — `class_default`, `class_default_missing_band`, `no_price_basis`, `no_cost_limit`, `unpriced_spend` — each asserting BOTH the basis and `would_breach`;
- `VALID_ESTIMATE_BASES` contains exactly those five and every test's observed basis is a member;
- the breach case: spent + expected > limit → `would_breach` True;
- the exact-boundary case: spent + expected == limit → `would_breach` False, because the reactive check in `evaluate_budget` owns that boundary and duplicating it here would let the two disagree;
- the already-over-limit case;
- missing/unknown band: `None`, `"unknown"` and an unrecognised string each take the LARGEST class default, report `band == "unknown"` and basis `class_default_missing_band`;
- `price_basis` unset → inert: `expected_cost_usd is None`, `would_breach` False, and the `arithmetic` string contains `not-measured` for the expected figure rather than a fabricated `$0.0000`;
- unknown spend with `provider_calls > 0` → `unpriced_spend`, no breach; unknown spend with `provider_calls == 0` → spend treated as 0.0 (a job that made no provider call definitionally spent nothing) and prediction proceeds to a real basis;
- `to_json()` carries `estimate_basis` — this is the grep-style pin the feature file's T003 will extend — and carries `expected_cost_usd is None` unchanged when there is no price basis;
- `arithmetic` is a non-empty single line carrying spent, expected, limit and basis;
- `resolve_predictive_budget_config`: the documented defaults when nothing is configured (8000 / 32000 / 120000, price basis None), a TOML override, and an env override, following the existing patterns at `tests/orchestration/test_job_budgets.py:193-362` (`tmp_path / "remedy.toml"` and `monkeypatch.setenv("REMEDY_BUDGET_*", ...)`).

A note on the price-basis-unset assertion: if the counters you build there have `provider_calls == 0`, the spent figure is a legitimate measured `0.0` and WILL render as `$0.0000`. Do not assert the whole string is free of `$0.0000` in that case — assert on `expected_cost_usd is None` and on the expected figure rendering as `not-measured`. An honest test beats a convenient one.

Commit exactly that one new path:

    test(f104): cover the predictive next-task cost engine

(The original R2 block asked for items 6a and 6b in ONE commit. The reviewer split it into the two commits above because they are two logical steps and the combined insertion count approaches the 500-line cap. Note this split in your handback's Deviations section as reviewer-directed.)

## 4. FEATURE-FILE AMENDMENT + DECISIONS (reviewer-authored, apply verbatim)

This is item 7 of the original R2 block, unchanged. The spec assumes tasks carry a band; they do not — `JobTask` has no band field and `TokenBand` lives in `token_economy.py`. That is a wrong-spec finding routed to planning per planner_reviewer_prompt.md §4.7, and the reviewer has already chosen the option. Apply the amendment.

Write the text between the markers to `.agent/authored/f104-r2-2.md` — the marker lines themselves are NEVER content. It is ONE FROM→TO pair, a REWRITE, against `docs/roadmap/features/T2_F104.md`. The FROM occurs exactly 1x. Report FROM 1x / TO 0x before and FROM 0x / TO 1x after.

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

Commit the feature file, decisions and both authored files together — one logical step:

    docs(f104): record the derived-band and no-default-price decisions

## 5. GATES, STATE, HANDBACK

Run all four and record the REAL command, trimmed output and REAL exit code:

    A  python3 -m pytest tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py -q
    B  python3 -m pytest tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_stop_reasons.py -q
    C  python3 -m pytest tests/docs/ -q
    D  python3 -m pytest tests/cli/test_golden_path.py -q

Gate C is mandatory because this round's change set includes `docs/roadmap/**` (planner_reviewer_prompt.md §3, docs-round gate). Gate D is the canary. A red gate is a STOP: hand back the raw output and do not paper over it. Do not run the full suite — that is the R5 integration gate, not this round.

Any deliberately destructive verification (mutation red-proofs) runs ONLY inside a disposable `git worktree`; the primary checkout must satisfy `git status --porcelain` == empty at handback. Put any worktree under `.remedy-wt/` (gitignored) — writes to /tmp are denied on this machine — and remove it before you finish.

Then rewrite `.agent/plan.md` from the text below (write it to `.agent/authored/f104-r2-4.md`, apply by `cp`, then `cmp`, and record the exit code). Do NOT touch `.agent/context.md` — scope, branch and constraints are unchanged from R1 and rewriting it risks its multi-test contract for no gain.

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
- feature + round, branch, and EVERY commit SHA of R2 in order — including the five made by the previous session (18b8ca7a, ab77b2b5, c6994fa8, 0f195a60, ef9a852c) and yours — and that this was a SPLIT round with no verdict, no PR, no merge;
- a per-commit changed-files table with `+/-` and a reason per path, for YOUR commits; for the five inherited commits one summary row each is enough, marked inherited;
- the fact that this session RESUMED an R2 that ended without a handback, and what state it found: ` M tests/orchestration/test_budget_guard.py` uncommitted, items 7-8 untouched;
- the transport proofs: the `cmp` exit code for f104-r2-4, the before/after FROM/TO counts for the f104-r2-2 REWRITE pair, and the 1x heading check for the f104-r2-3 append;
- the verification table with the REAL trimmed output and REAL exit codes for gates A-D;
- an item-status table covering the five bundle items of THIS block, each exactly once, with `done` / `skipped` (reason) / `deviated` (reason);
- open-findings count and which findings this round marked `Done:`;
- the final `git status --porcelain` result;
- next expected action;
- a "Deviations, declared" section naming ANY departure from this block, including its own line count if it exceeds 60 lines and why.

Declare in the handback, explicitly, whether `predict_next_task_cost` has a production caller at the end of this round. It does not, by design, and R3 adds one — saying so is what stops R-0222 from recurring silently.

Also declare explicitly what you did with the inherited uncommitted test: unchanged-and-verified, or changed (and exactly how).

Finally: commit the state files, `git push`, and confirm `git status --porcelain` is empty. Do NOT create a PR. Do NOT merge anything. Do NOT run `gh pr merge`.

Every commit message ends with the trailer:
Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

Commit subjects must not contain leading-slash tokens, absolute paths, or secret-like strings — the evidence metadata scanner rejects them.

If anything in this block contradicts AGENTS.md, AGENTS.md wins and you hand back naming the contradiction instead of guessing. If a gate goes red and the fix is not obviously inside this round's change set, STOP and hand back with the raw output rather than widening scope.

Your final message is your completion report: the item-status table, the real gate results with exit codes, the commit SHAs, the transport proofs, and your declared deviations.
