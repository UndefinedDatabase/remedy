# Handoff — F104 Hard budget enforcement, SESSION CLOSE (R4 + R5)

Feature F104, rounds **R4** and **R5**, branch `feature/f104-hard-budget-enforcement`,
build mode one-session self-drive (docs/agents/self_drive_protocol.md), one
delegated worker per round. Verdicts, as the reviewer stated them:
**R4 PASS at f9309bfe**, **R5 PASS at 549f2bac**. `LAST_REVIEWED_SHA = 549f2bac`.
Tip at handback: this handoff commit (the last entry under `## Commits`); its
SHA is in the completion report. No PR, no merge, no force-push.

## Range
Review of `549f2bac..HEAD` — this state-only close round. R4 and R5 are reviewed;
their per-commit tables are in the handoffs at f9309bfe and 549f2bac.

## Commits

**R4, oldest first (PASS at f9309bfe):** 745999fd save the R4 block · 445d84d6
extract the safe-point counters build · ffe03941 derive the next task's token
band, pure · 14b8940c stop before a task that would breach max_cost_usd ·
621479df pin the predictive stop at the live safe point · 00289e1e DECISION D6 +
R4 state · f9309bfe the R4 handback

**R5, oldest first (PASS at 549f2bac):** b018a16a save the R5 block, register
R-0225/R-0226 · 476376f0 admit max_cost_usd to the closed manifest budget schema ·
947aad4f pin that schema · 8c8d6507 assert both cost stops reach the stopped
state · 6022eea2 DECISION D7 + R5 state · 549f2bac the R5 handback

### 8a9a964c chore(f104): save the close block and record the R5 resolutions
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f104-r6-close-1.md | +125 | the close block, verbatim (item 1a) |
| .agent/last_block.md | +109/-146 | same text; replaces the stale R5 block |
| .agent/live_review.md | +27/-8 | reviewer's Done text for R-0225/R-0226 replacing their `OPEN.` lines; R5 PASS + R6 lines in `## Steps` |

### bea706a8 docs(f104): rewrite the plan at R6 after the R5 PASS
| Path | +/- | Reason |
|---|---|---|
| .agent/plan.md | +10/-7 | Current Step → R6 (T003); both verdicts; 48 lines |

### (this commit) chore(f104): write the session-close handback
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md | rewrite | this file (R-0149 self-reference exception) |

## External actions
`git push origin feature/f104-hard-budget-enforcement` — transcript in the
completion report. No PR, no merge, no gh command, no worktree.

## Verification

Gates **the reviewer re-ran itself**:

| Round | A | B | C | D | E | Exit |
|---|---|---|---|---|---|---|
| R4 | 249 passed / **1 xfailed** | 163 | 294 | 42 | — | all **0** |
| R5 | 261 passed / **0 xfailed** | 163 | 294 | 42 | 124 | all **0** |

Mutation proofs, all run by the reviewer in disposable worktrees under
`.remedy-wt/`, all removed and pruned afterwards:

| Mutation | Result |
|---|---|
| dispatch safe point stops passing `next_task` | 1 RED — the just-under acceptance fixture |
| `derive_next_task_token_band` forced to always return UNKNOWN | 7 RED, including the live acceptance test |
| `"max_cost_usd"` removed from `_BUDGET_ALLOWED_KEYS` | 11 RED, including BOTH terminal-state tests |

R-0225 was **reproduced by the reviewer directly, before it was registered**.
Captured output:
`run_manifest_write_failed: ManifestError: manifest.budgets has unknown keys: ['max_cost_usd']`
with the job left in status `running`.

This round's own gates, real, from the repo root at bea706a8:

| Gate | Command | Exit | Result |
|---|---|---|---|
| 1 | `python3 -m pytest tests/docs/ -q` | **0** | 294 passed |
| 2 | `python3 -m pytest tests/cli/test_golden_path.py -q` | **0** | 42 passed |
| 3 | `pytest test_dashboard_contract.py test_test_runner.py test_resource_safety.py -q` | **0** | 142 passed |

## Authored-text proofs
`cmp .agent/authored/f104-r6-close-1.md .agent/last_block.md` → **exit 0**. The
R-0225/R-0226 resolution texts and the two `## Steps` lines were applied verbatim.

## What is built
T001 complete. T002 complete: the predictive check is wired at the task-dispatch
safe point, stops BEFORE dispatch with reason
`predicted_budget_exhausted:max_cost_usd`, persists its arithmetic in
`job.budget_prediction`, and BOTH the predictive and the reactive cost stop reach
`JOB_STOPPED` for real. **T003 not started.**

## Item status
| Item | Status | Reason |
|---|---|---|
| R4-1 save the block | done | cmp exit 0 |
| R4-2 counters refactor | done | pure move |
| R4-3 band derivation + tests | done | |
| R4-4 wiring + stale comments | done | |
| R4-5 fixtures + regressions | deviated | terminal `JOB_STOPPED` shipped as `xfail(strict=True)` behind the R-0225 blocker — **RESOLVED**, retired in 8c8d6507; A9 pinned at the `derive`→`predict` seam, which stands as the R4 block permitted |
| R4-6 docs, decisions, state | deviated | no ist-doc existed for the stop reason and `.agent/context.md` was untouched — both **RESOLVED**: context.md renumbered in R5 (6022eea2), the ist-doc question scheduled into R6 by DECISION D7 |
| R5-1 block + findings | done | cmp exit 0; both findings verbatim; header → R-0227 |
| R5-2 fix R-0225 | done | allowlist widened by exactly one field |
| R5-3 pin the schema | deviated | pins went to `TestRunManifestBudgetIdentity` in `tests/orchestration/test_job_budgets.py`, the existing `_decode_budgets_field` home, not the block's fallback file; gate E still run |
| R5-4 fix R-0226 | deviated | the reactive terminal test sits beside its predictive twin so the existing `_run` harness is reused, not duplicated |
| R5-5 docs, decisions, state | done | D7, feature file, plan/context/live_review/handoff |
| Close-1 block + resolutions | done | cmp exit 0; R-0225/R-0226 Done in the reviewer's words; header already R-0227 |
| Close-2 this handoff | done | rewritten, never appended |
| Close-3 plan rewrite | done | 48 lines; Current Step R6; R5 no longer pending |

## Open findings
**1** — R-0221 (Low, carried from F103 R5; not F104's to fix per AGENTS.md Scope
Control; routed to the F252 flake-debt class; costs the integration gate seven
phantom base-only failures, to be attributed, not chased). R-0222, R-0223,
R-0224, R-0225 and R-0226 are all **Done** with reviewer-authored resolution text.

## State
`git status --porcelain` **EMPTY**; branch pushed; no worktrees beyond the primary
checkout; `docs/roadmap/STATUS.md` still carries F104 as `[~]` — correct, the
feature is not closed.

## Deviations & assumptions — declared
- In the reviewer's voice: "The session ran THREE delegated rounds against a
  stated cap of two. The third was this state-only close round, which writes no
  production code: the reviewer is read-only, so without it the R5 verdict and
  the R-0225/R-0226 resolution text would exist nowhere on disk, and the handoff
  is the only return channel. The overage is declared rather than hidden."
- **The stale R5 `## Steps` line was replaced, not duplicated** — it still read
  "Awaiting review" and would have contradicted the PASS line beside it.
- **R4's `## Steps` line still ends "Awaiting review"**, left exactly as found
  because the block ordered R1-R4 untouched. Flagged as deliberate, not missed.
- **`.agent/context.md` untouched** — correct about the round numbering after its
  R5 update, so the block's condition for touching it was not met.
- **Per-round commit lists instead of 13 per-commit tables**: R4 and R5 are
  reviewed and each has its own handoff in git history; only this round's three
  commits are unreviewed and each carries a full table. No section dropped.
- **This handoff exceeds 60 lines** (AGENTS.md D15 stated cause): two rounds'
  commit lists, three changed-files tables, the reviewer's gate table, the
  mutation table, the R-0225 reproduction, this round's gate table and a
  fourteen-row item-status table.

## Next
**R6 — T003**: display, docs and `estimate_basis` labels per DECISION F104 D7,
pinned by a grep-style test. Then **R7** the integration gate
(docs/agents/integration_gate.md), then **R8** closure
(docs/roadmap/STATUS_closure_protocol.md).
