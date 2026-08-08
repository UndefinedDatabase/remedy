# Handoff — F104 Hard budget enforcement, R2 (T002 part 1), CONTINUATION

Branch: `feature/f104-hard-budget-enforcement`. SPLIT round — no verdict, no PR,
no merge, nothing force-pushed. Pushed to origin.

R2 commits, oldest first (5 inherited + 4 mine):
18b8ca7a, ab77b2b5, c6994fa8, 0f195a60, ef9a852c (inherited),
5e2e242d, 77971336, 5971a127, 460e837c (this session), plus the state commit
that carries this file and `plan.md` — the branch tip, which cannot name its own
SHA from inside itself.

## What this session found on resume

The previous R2 worker ended mid-round with no handback. Items 1-5 of the
original R2 block were committed; `git status --porcelain` reported
` M tests/orchestration/test_budget_guard.py` (an uncommitted +119-line
`TestLiveSafePointReadsTheLedgerCost`); items 7-8 were untouched. HEAD was
ef9a852c, matching the continuation block.

## Changed files, per commit

| Commit | Path | +/- | Reason |
|---|---|---|---|
| 18b8ca7a | (inherited) .agent/last_block.md | +362/-422 | original R2 block saved |
| ab77b2b5 | (inherited) .agent/live_review.md + authored f104-r2-1 | +104/-2 | R-0222 + R-0223 registered |
| c6994fa8 | (inherited) packages/orchestration/pingpong_job.py | +54/-9 | R-0222 fix: ledger cost into `_stop_check` counters |
| 0f195a60 | (inherited) budget_resolution.py, config.py | +128/-0 | price-basis + class-default keys, `resolve_predictive_budget_config` |
| ef9a852c | (inherited) packages/orchestration/budget_guard.py | +164/-1 | `BudgetPrediction`, `predict_next_task_cost`, `VALID_ESTIMATE_BASES` |
| 5e2e242d | .agent/last_block.md | +78/-207 | this continuation block replaces the original (R-0223) |
| 77971336 | tests/orchestration/test_budget_guard.py | +145/-0 | live safe-point pin of R-0222, incl. the P6 counter-kwarg assertions I added |
| 5971a127 | tests/orchestration/test_predictive_budget.py | +416/-0 | 39 tests: 5 bases, boundary, missing band, P6 inertness, `to_json`, resolver |
| 460e837c | docs/roadmap/features/T2_F104.md | +8/-0 | D3/D4 amendment (pair f104-r2-2) |
| 460e837c | .agent/decisions.md | +30/-0 | D3+D4 entry (f104-r2-3) |
| 460e837c | .agent/authored/f104-r2-2.md, f104-r2-3.md | +50/-0 | authored originals for re-verification |

Largest commit 5971a127 at +416 insertions — under the 500 cap (DECISION F104 D1).

## Transport proofs

| File | Shape | Proof |
|---|---|---|
| f104-r2-2 → T2_F104.md | REWRITE | before FROM 1x / TO 0x; after TO 1x. FROM still counts 1x AFTER — see Deviations, TO is a strict superset of FROM. Strict check "FROM occurrences not extended into TO" = 0. |
| f104-r2-3 → decisions.md | append | heading 0x before, 1x after; exactly one blank line before it |
| f104-r2-4 → plan.md | full-file `cp` | `cmp` exit 0 |

## Verification (real commands, real trimmed output, real exit codes)

| Gate | Command | Output | Exit |
|---|---|---|---|
| A | `python3 -m pytest tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py -q` | `226 passed in 32.80s` | 0 |
| B | `python3 -m pytest tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_stop_reasons.py -q` | `163 passed in 6.61s` | 0 |
| C | `python3 -m pytest tests/docs/ -q` | `294 passed in 0.25s` | 0 |
| D | `python3 -m pytest tests/cli/test_golden_path.py -q` | `42 passed in 21.40s` | 0 |

Mutation red-proofs, all in a disposable worktree at `.remedy-wt/f104r2c`, now
removed (`git worktree list` shows only the primary checkout):
1. revert c6994fa8's `pingpong_job.py` hunk → 4 of 5 LiveSafePoint tests RED.
2. `measured_cost_usd=_ledger_cost or 0.0` → the P6 null test RED (it was GREEN
   under this mutation before I strengthened the inherited test).
3. remove the `max_cost_usd is not None` guard → `test_no_cost_limit_never_
   queries_the_ledger` RED.
4. `>` → `>=` in `would_breach` → the exact-boundary test RED, and only it.
5. `_format_prediction_usd` zero-coercion + an invented default price → 7 RED.
6. largest class default `max` → `min` → 6 missing-band tests RED.

## Item status (this block's five bundle items)

| Item | Status | Reason |
|---|---|---|
| 1 save this block | done | |
| 2 commit the pending live-ledger test | deviated | inherited work CHANGED — see Deviations |
| 3 prediction-engine test file | done | 39 tests, all requested cases covered |
| 4 feature-file amendment + decisions | done | applied verbatim from the authored files |
| 5 gates, state, handback | done | |

## Declarations required by the block

- **`predict_next_task_cost` has NO production caller at the end of this round.**
  Deliberate: R3 wires it at the task-dispatch safe point. It is stated in the
  `budget_guard.py` module docstring, above the function, in `plan.md`, and here.
  `test_predictive_budget.py` says so too, so a reader does not mistake the
  absence for the R-0222 mistake repeating.
- **The inherited uncommitted test was CHANGED, not passed through unchanged.**
  See Deviations for exactly what and why.

Open findings: 3 — R-0221 (Low, carried), R-0222 (Medium), R-0223 (Low).
This round marked NO finding `Done:` in `.agent/live_review.md`: that file is
not in this block's Change list, and only reviewer-authored text sets Resolved.
R-0222 and R-0223 are FIXED in code/state (c6994fa8 + 77971336, and 5e2e242d)
and await the reviewer's own marking.

`git status --porcelain`: EMPTY at handback.
Next expected action: reviewer re-runs gates A-D at the branch tip, rules on the new
finding candidate below, then R3 (safe-point wiring, `predicted_budget_
exhausted:<limit>`, both acceptance fixtures).

## New finding candidate for the reviewer (next free ID R-0224)

`_stop_check` builds counters via `collect_counters_from_actuals(...,
unpriced_call_count=<ledger unpriced count>)`, but `BudgetCounters.__post_init__`
raises `BudgetCounterError` when `unpriced_call_count > provider_calls`, and
`provider_calls` at the safe point is the run's ACCUMULATED count, not the
ledger's. When the ledger holds more unpriced rows for the job than the run has
accumulated provider calls — e.g. the first safe point of a resumed run whose
prior ledger rows include unpriced calls — the raise is caught by c6994fa8's own
broad `except Exception`, the cost is silently discarded, and `--max-cost-usd`
stops enforcing for exactly the mixed-priced jobs it was added for. I hit this
while writing the test (`ledger_result=(None, 3, 3)` →
`BudgetCounterError: unpriced_call_count (3) > provider_calls (0)`), reported it
rather than pinning the degraded behaviour, and left the test on a scenario that
does not depend on it. NOT fixed: the block forbids further
`packages/orchestration/**` edits while the gates are green.

## Deviations, declared

- **Item 2, inherited test changed (2 edits).** (a) `_drive` now also records
  the kwargs of every `collect_counters_from_actuals` call and returns them as a
  third value; the real collector still runs, so the counters the stop check
  evaluates are the production ones. (b) The five tests assert on those kwargs:
  `measured_cost_usd == 5.0 / 0.5`, `is None` for the unpriced ledger, and
  `"measured_cost_usd" not in ...` for the no-limit and broken-read fallbacks.
  WHY: as inherited, the test named
  `test_unpriced_ledger_keeps_the_cost_null_and_does_not_stop` asserted only
  `signal is None`, which a coerced `0.0` also satisfies — mutation 2 above was
  GREEN before the change and is RED after. The name and the P6 comment claimed
  more than the assertions proved. Everything else in the class is inherited
  unchanged and verified by running it; the R-0222 pin itself (mutation 1) was
  already sound.
- **Item 3, commit split.** Reviewer-directed: the original R2 block asked for
  6a+6b in one commit; this block split them into 77971336 and 5971a127.
- **f104-r2-2 FROM count after apply is 1x, not the 0x the block asked me to
  report.** The pair's TO block begins with the entire FROM block and appends
  four lines, so FROM is a substring of TO and can never reach 0x. Reported the
  meaningful proof instead: TO 0x→1x, and 0 FROM occurrences that are not the
  prefix of the TO occurrence. Nothing was applied twice; `git diff --stat` for
  T2_F104.md is `+8/-0`.
- **`.agent/live_review.md` not touched**, per this block's Change list — so the
  `Done:` markers for R-0222/R-0223 are the reviewer's to write.
- **`.agent/context.md` not touched**, as instructed.
- **Handoff length is 144 lines, over the 60-line cap.** Cause: the mandated
  per-commit changed-files table (11 rows over 9 commits), the transport-proof
  table, the six-entry mutation record, the four-gate verification table, the
  item-status table, the two explicit declarations, and the resume-state and
  new-finding sections this block requires. No section dropped.
