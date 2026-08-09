# Handoff — F104 Hard budget enforcement, R5 (repair: R-0225, R-0226)

Branch: `feature/f104-hard-budget-enforcement`. No PR, merge, force-push or
worktree. Durable history: the R4 verdict was **PASS**, with R-0225 (High) and
R-0226 (Medium) registered against it, and R-0225 was **reproduced by the
reviewer independently at f9309bfe** before it was written.

## Range
Review of `f9309bfe..HEAD` (5 commits + this handoff commit, oldest first).

## Commits

### b018a16a chore(f104): save the R5 block and register R-0225 and R-0226
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f104-r5-1.md | +162 | the R5 order, saved verbatim (item 1a) |
| .agent/last_block.md | +150/-102 | same text; replaces the stale R4 block |
| .agent/live_review.md | +29/-1 | R-0225 + R-0226 verbatim; Next free ID → R-0227 |
| .agent/plan.md | +16/-20 | Current Step → R5 repair |

### 476376f0 fix(f104): admit max_cost_usd to the closed manifest budget schema
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/run_manifest.py | +27/-1 | `max_cost_usd` added to `_BUDGET_ALLOWED_KEYS`; its own bool/str/type/finite/strictly-positive check + WHY comment; `import math` |

### 947aad4f test(f104): pin the manifest budget schema for max_cost_usd
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_job_budgets.py | +60 | 10 pins in `TestRunManifestBudgetIdentity`, the module's existing `_decode_budgets_field` home |

### 8c8d6507 test(f104): assert both cost stops reach the stopped state
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_predictive_budget.py | +34/-18 | xfail + `_STOPPED_STATE_BLOCKER` deleted; predictive terminal test strengthened; new reactive terminal test; class docstring corrected |

### 6022eea2 docs(f104): record DECISION F104 D7 and the R5 state
| Path | +/- | Reason |
|---|---|---|
| docs/roadmap/features/T2_F104.md | +6 | the manifest note appended verbatim to the `max_cost_usd` bullet |
| .agent/decisions.md | +24 | D7 with alternative + reversal |
| .agent/plan.md | +14/-14 | rewritten at R6, 45 lines |
| .agent/context.md | +6/-3 | the stale `## Steps` line renumbered |
| .agent/live_review.md | +6 | one R5 line in `## Steps`; no Resolved marker set |

### (this commit) chore(f104): write the R5 handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file (R-0149 self-reference exception) |

## External actions
`git push origin feature/f104-hard-budget-enforcement` — transcript in the
completion report. No PR, no merge, no gh command, no worktree.

## Verification (real, at 6022eea2, from the repo root)
| Gate | Command | Exit | Result |
|---|---|---|---|
| A | `pytest test_predictive_budget.py test_budget_guard.py test_job_budgets.py -q` | **0** | **261 passed, 0 xfailed** |
| B | `pytest test_budget_stop_integration.py test_f018_authority_integration.py test_stop_reasons.py -q` | **0** | 163 passed |
| C | `pytest tests/docs/ -q` | **0** | 294 passed |
| D | `pytest tests/cli/test_golden_path.py -q` (canary) | **0** | 42 passed |
| E | `pytest test_run_manifest.py test_run_manifest_schema.py test_run_manifest_external_schema.py test_run_manifest_strict_boundaries.py test_f018_package_pipeline_e2e.py -q` | **0** | 124 passed |

Red-proof, observed live: at 476376f0 (fix landed, xfail not yet retired) gate A
exited **1** with `[XPASS(strict)]
test_a_predictive_stop_reaches_the_stopped_state`. R4's strict xfail flipped
exactly as designed, so the JOB_STOPPED assertion demonstrably depends on the
allowlist fix. B (163) and E (124) also exited 0 at 476376f0.

## Authored-text proofs
`cmp .agent/authored/f104-r5-1.md .agent/last_block.md` → **exit 0**.

## Item status
| Item | Status | Reason |
|---|---|---|
| 1 block + findings | done | cmp exit 0; both findings verbatim, no Done marker, header → R-0227 |
| 2 fix R-0225 | done | allowlist +1 field only; deadline and integer rules untouched |
| 3 pin the schema | done | all 10 listed cases; see deviation on placement |
| 4 fix R-0226 | done | see deviation on placement of the reactive test |
| 5 docs, decisions, state | done | D7, the feature-file append, plan/context/live_review/handoff |

## Deviations & assumptions
- **Item 3 placement.** The block's fallback,
  `tests/orchestration/test_run_manifest_schema.py`, carries no budget coverage;
  `_decode_budgets_field` already has a home in `TestRunManifestBudgetIdentity`
  in `tests/orchestration/test_job_budgets.py`, so the 10 pins went there per the
  house pattern. Gate E was still run — it is the blast radius, not the home.
- **Item 4b placement.** The reactive terminal test sits in
  `TestPredictiveStopAtTheLiveDispatchSafePoint` beside its predictive twin: the
  two terminal proofs read as one pair and the existing `_run` harness is reused
  rather than duplicated, as the block required. The alternative home,
  `TestLiveSafePointReadsTheLedgerCost`, would have meant a second harness.
- **No mutation red-proof.** G5 confines destructive checks to a disposable
  worktree and this block forbade creating one. The XPASS above is the
  substitute, and it was observed, not reasoned.
- **No further defect found.**
- **This handoff is 103 lines** (AGENTS.md D15 stated-cause overage): six
  per-commit tables, the five-gate table with exit codes, the red-proof record,
  the proof line, the item table and the placement deviations. No section
  dropped.

## Next
Reviewer: verdict on R5. On PASS, `LAST_REVIEWED_SHA` advances and R6 starts
T003 (display + docs + estimate labels) per DECISION F104 D7.
