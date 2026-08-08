# Handoff — F104 Hard budget enforcement, R3 (T002-fix, R-0224)

Branch: `feature/f104-hard-budget-enforcement`. SPLIT round — no verdict, no PR,
no merge, nothing force-pushed. Pushed to origin.

R3 commits, oldest first (base 5ffd1178):
61ba3056, e4f0dd31, 76be26d9, c6f99aa8, 31a462d3, plus the state commit carrying
this file and `plan.md` — the branch tip, which cannot name its own SHA.

## Changed files, per commit

| Commit | Path | +/- | Reason |
|---|---|---|---|
| 61ba3056 | .agent/last_block.md | +205/-201 | R3 block replaces the R2 continuation block (R-0223) |
| e4f0dd31 | .agent/authored/f104-r3-1.md | +82/-0 | authored original for re-verification |
| e4f0dd31 | .agent/live_review.md | +51/-35 | R-0224 registered; R-0222/R-0223 marked Done |
| 76be26d9 | packages/orchestration/budget_guard.py | +29/-14 | `priced_call_count` field + validation + to_json; cross-source check deleted; contradiction check restated cost-side; collector kwarg |
| 76be26d9 | packages/orchestration/pingpong_job.py | +5/-1 | `_stop_check` binds and forwards the ledger's priced count |
| c6f99aa8 | .agent/authored/f104-r3-2.md | +32/-0 | authored original |
| c6f99aa8 | .agent/decisions.md | +33/-0 | DECISION F104 D5 appended |
| 31a462d3 | tests/orchestration/test_budget_guard.py | +105/-8 | R-0224 pins (unit, bridge, live safe point), `priced_call_count` coverage, `_cost_counters` helper split |

Largest commit 61ba3056 at +205 insertions — under the 500 cap (DECISION F104 D1)
and in any case a single-`.agent/**`-file verbatim save.

## Transport proofs

| File | Shape | Proof |
|---|---|---|
| f104-r3-1 → live_review.md | full-file `cp` | `cmp` exit 0 |
| f104-r3-2 → decisions.md | append | heading 0x before, 1x after; exactly one blank line before it |
| f104-r3-3 → plan.md | full-file `cp` | `cmp` exit 0 |

## Verification (real commands, real trimmed output, real exit codes)

| Gate | Command | Output | Exit |
|---|---|---|---|
| A | `python3 -m pytest tests/orchestration/test_predictive_budget.py tests/orchestration/test_budget_guard.py tests/orchestration/test_job_budgets.py -q` | `233 passed in 32.73s` | 0 |
| B | `python3 -m pytest tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_f018_authority_integration.py tests/orchestration/test_stop_reasons.py -q` | `163 passed in 6.48s` | 0 |
| C | `python3 -m pytest tests/docs/ -q` | `294 passed in 0.25s` | 0 |
| D | `python3 -m pytest tests/cli/test_golden_path.py -q` | `42 passed in 20.68s` | 0 |

Gate A is 233, up from R2's 226: +7 net new tests in `test_budget_guard.py`.

## Red-proof (reintroduced invariant)

Disposable worktree `.remedy-wt/f104r3` at c6f99aa8, R3's test file copied in,
the deleted `unpriced_call_count > provider_calls` check restored verbatim:

    3 failed, 89 passed in 2.26s        (pytest exit 1)
    FAILED ...::test_unpriced_count_above_provider_calls_is_accepted_and_preserved
    FAILED ...::test_collect_counters_passes_cost_side_counts_above_provider_calls
    FAILED ...::test_ledger_unpriced_count_above_this_runs_calls_still_enforces
    BudgetCounterError: unpriced_call_count (3) > provider_calls (0)

Exactly the three R-0224 pins go RED and nothing else. Worktree removed;
`git worktree list` shows only the primary checkout.

## BudgetCounters construction-site survey (`packages/`, `apps/`, `tests/`)

| Site | Passes cost fields? | Why unaffected |
|---|---|---|
| `budget_guard.collect_counters_from_actuals` | yes | changed this round; forwards all three |
| `budget_guard.counters_from_persisted` | no | `PersistedBudgetActualsV1` has no cost fields at all; `measured_cost_usd` stays None so the new check cannot fire |
| `long_run_executor.py:875` fallback | no | token/call/time only; both cost counts default 0 |
| `tests/orchestration/test_f018_authority_integration.py` (11 sites) | no | F018 token-side tests; gate B green |
| `tests/orchestration/test_budget_stop_integration.py` (14 sites) | no | same; gate B green |
| `tests/orchestration/test_job_budgets.py` | no | gate A green |
| `tests/orchestration/test_predictive_budget.py:54` `_counters` | `unpriced` only | every call site pairs `unpriced>0` with `spent=None`, so the cost-side check never fires; gate A green |
| `tests/orchestration/test_budget_guard.py` | yes | changed this round |

Readers of `unpriced_call_count`: `has_unpriced`, `cost_description`,
`evaluate_budget`'s two warning strings, `predict_next_task_cost`'s
`unpriced_spend` note, `to_json`, and `apps/cli/commands/job.py:2160` which emits
`counters.to_json()` wholesale. All read the field, none compare it to
`provider_calls`; the CLI gains one extra JSON key and no code path branches on
its absence. NO site outside this block's change list needed a change.

## Item status

| Item | Status | Reason |
|---|---|---|
| 1 save this block | done | 61ba3056 |
| 2 register the findings | done | e4f0dd31, before any code |
| 3 the cost-side counter fix | done | 76be26d9, a-f all applied as specified |
| 4 decision entry | done | c6f99aa8 |
| 5 tests | deviated | all of a/b/c done, plus 5 pre-existing tests repaired — see Deviations |
| 6 gates, state, handback | done | |

## Declarations required by the block

- **`predict_next_task_cost` has NO production caller at the end of this round.**
  Unchanged from R2 and deliberate: R4 wires it at the task-dispatch safe point.
  Stated in the `budget_guard.py` module docstring, in `plan.md` and here.
- Open findings: 4 — R-0221 (Low, carried), R-0222, R-0223, R-0224. This round
  marked `Done:` on R-0222, R-0223 and R-0224, all three verbatim from the
  reviewer-authored f104-r3-1 text; the worker asserted no resolution of its own.

`git status --porcelain`: EMPTY at handback.
Next expected action: reviewer re-runs gates A-D at the branch tip and re-runs the
R-0224 red-proof, then R4 (band derivation at the dispatch safe point,
`predicted_budget_exhausted:<limit>`, decision arithmetic, both fixtures).

## Deviations, declared

- **Item 5, five pre-existing tests repaired beyond the three the block named.**
  The new cost-side contradiction check fires whenever a positive
  `measured_cost_usd` meets `priced_call_count == 0` and `unpriced_call_count > 0`
  — which is exactly what five partially-priced tests in `test_budget_guard.py`
  constructed, because they predate the field and left it at its default. Fixed
  at the source: `_cost_counters` grew a `priced` parameter defaulting to
  `calls - unpriced`, so the helper's own scenario stays self-consistent, plus
  `test_collect_counters_from_actuals_passes_money_through` now passes and asserts
  the priced count. Affected: `test_partially_priced_renders_a_lower_bound`,
  `test_has_unpriced_mirrors_has_unmeasured`,
  `test_unpriced_mixed_over_limit_is_a_definite_breach`,
  `test_unpriced_mixed_under_limit_only_warns`, and that collector test. This is
  a semantic tightening the design implies, not a weakening: no assertion was
  relaxed and no expectation deleted. All five are inside the block's Change list.
  `test_positive_cost_with_every_call_unpriced_is_impossible` was renamed to
  `test_positive_cost_with_nothing_priced_is_impossible` for the same reason.
- **Commit 76be26d9 leaves 7 tests RED at that SHA.** The block orders the fix as
  item 3 and every test edit as item 5, so the repairs above could not land in the
  fix commit without merging two ordered items. Green again at 31a462d3 and at the
  tip. Declared rather than silently reordered.
- **`plan.md` was rewritten at item 6, not before the earlier commits**, so
  commits 61ba3056-31a462d3 carry the R2 plan text. The block's item 6 supplies
  the authored plan content and its `cp`/`cmp` transport, which cannot be applied
  earlier; this matches R1 and R2.
- **`.agent/context.md` not touched**, as instructed.
- **Handoff length is 135 lines, over the 60-line cap** (AGENTS.md DECISION D15,
  stated-cause overage). Cause: the mandated per-commit changed-files table, the
  transport-proof table, the four-gate verification table, the red-proof block,
  the construction-site survey this block requires in the handback, the
  item-status table and the two declarations. No section dropped.
