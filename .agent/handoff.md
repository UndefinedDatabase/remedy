# Handback — F074 round 1: claim, book F113 R6, write the slice list, land T001 and T002

## Session

SESSION 1 of feature F074 · round 1 · rounds so far 1

Context self-assessment: this worker checked both prompt digests and every prepared file's digest before any write, copied every file by a script with a byte proof, ran each gate exactly once, and context stayed ample throughout.

Fortschritt: ~45 % (T001 and T002 landed · T003 open) — Schätzung

## Range

Review of `148a1c386`..`HEAD` on `feature/f074-estimate-calibration`.

## Commits

### 03e2eb213 F074 R1 C1: claim F074, book F113 R6, re-head the ledger, DECISION F074 D1, the slice list
| Path | +/- | Reason |
|---|---|---|
| `.agent/authored/f074-r1.md` | +117/-0 | NEW FILE, this round's block, byte copy of `block.md` (sha256 `0aa8b4d0...82c88ee`) |
| `.agent/context.md` | +10/-10 | rewritten for F074 round 1 |
| `.agent/decisions.md` | +12/-0 | DECISION F074 D1 appended |
| `.agent/live_review.md` | +15/-14 | re-headed; F113 round 6's verdict booked |
| `.agent/plan.md` | +12/-11 | rewritten for F074 round 1 |
| `docs/roadmap/STATUS.md` | +1/-1 | F074's line flipped from `[ ]` to `[~]` |
| `docs/roadmap/features/T3_F074.md` | +17/-0 | the slice list |

### ec87a137e F074 R1 C2: estimate calibration — the per-class distributions from the cost ledger, the floor, the damping and the snapshot
| Path | +/- | Reason |
|---|---|---|
| `packages/orchestration/estimate_calibration.py` | +412/-0 | NEW FILE, T001: per-class/role distributions, sample floor, damping, snapshot |

### 95bcee2e1 F074 R1 C3: the shared estimator reads the calibration — the three settings, the resolver's table, and the task's class in the three consumers
| Path | +/- | Reason |
|---|---|---|
| `apps/cli/commands/job.py` | +1/-1 | `remedy job budget` passes `task_class` to `predict_next_task_cost` |
| `docs/guides/environment.md` | +3/-0 | the three `budget.calibration_*` env rows |
| `packages/orchestration/budget_guard.py` | +17/-4 | `predict_next_task_cost` takes `task_class`, reads the calibration, `calibrated(n)` label family |
| `packages/orchestration/budget_resolution.py` | +35/-2 | `PredictiveBudgetConfig.calibration`, `resolve_predictive_budget_config` attaches the project's table |
| `packages/orchestration/config_keys_budget.py` | +32/-0 | the three `budget.calibration_*` `ConfigKeySpec`s |
| `packages/orchestration/cost_preview.py` | +22/-1 | `estimate_cost_band` takes `task_class`, calibrated P20-P80 band |
| `packages/orchestration/do_rehearsal.py` | +2/-1 | `_task_rows` passes the task's class |
| `packages/orchestration/pingpong_job.py` | +1/-1 | `run_job`'s predictive stop passes `next_task.task_class` |
| `packages/orchestration/subtree_rerun.py` | +15/-4 | `subtree_rerun_cost_estimate` passes each task's class, names calibrated tasks in its basis |
| `tests/orchestration/import_reachability_allowlist.txt` | +1/-0 | `packages.orchestration.estimate_calibration` line |
| `tests/orchestration/test_task_injection_runner.py` | +2/-2 | the recording `predict_next_task_cost` wrapper takes and forwards `task_class` |

### bd429dbf5 F074 R1 C4: the calibration measured from fixture ledgers — exact percentiles, the floor, the damping, the window, the snapshot
| Path | +/- | Reason |
|---|---|---|
| `tests/orchestration/test_estimate_calibration.py` | +251/-0 | NEW FILE, T001/T002 tests: percentiles, floor, damping, window, snapshot, fixture ledgers |

### 5fead9dd3 F074 R1 C5: one seam test per consumer, the calibration page and its index rows, and the two pages that said calibration did not exist
| Path | +/- | Reason |
|---|---|---|
| `docs/README.md` | +2/-0 | the index rows for `estimate-calibration-v1.md` |
| `docs/system/cost-anomaly-alarm-v1.md` | +2/-2 | its "deliberately not built" paragraph updated now F074 exists |
| `docs/system/estimate-calibration-v1.md` | +74/-0 | NEW FILE, the calibration page |
| `docs/system/job-budget-enforcement-v0.md` | +14/-5 | the estimate-source section and the `calibrated(n)` label family documented |
| `tests/orchestration/test_estimate_calibration_consumers.py` | +251/-0 | NEW FILE, one seam test per consumer |

## Item status

| Item | Status | Reason |
|---|---|---|
| Both prompt digests checked (`block.md`, `digests.txt`) | done | both matched before any read |
| Every prepared file's digest checked | done | 29 of 29 matched |
| C0 | done | branch created from `main` at `148a1c386`, confirmed before any write |
| C1 | done | |
| C2 | done | |
| C3 | done | |
| C4 | done | |
| C5 | done | |
| Gate 1 | done | |
| Gate 2 | done | |
| Gate 3 | done | |
| Gate 4 | done | |
| Gate 5 | done | |
| C6 (this handback) | done | |
| Push | done | see External actions |
| Pull request | skipped | the block orders no PR this round |

## External actions

- `git checkout -b feature/f074-estimate-calibration` from `main` at `148a1c386`: done, HEAD unchanged by the checkout.
- `git push -u origin feature/f074-estimate-calibration`: outcome in the worker's reply (written after this file is committed).
- No merge, no PR create, no stash, no provider call, no rebase, no amend, no force push.

## Verification

Gate 1a: `git status --porcelain` (through `git -C <repository root>`) — empty output.

Gate 1b: `python3 .remedy-wt/f074-r1/prep/verify.py .` — every line `True` (including every C1-C5 path-set and byte-equality check), last line `ALL True`.

Gate 2: `python3 .remedy-wt/f074-r1/prep/ruff_touched.py .` — `ruff over 12 files: exit 0`, `All checks passed!`

Gate 3: `python3 .remedy-wt/f074-r1/prep/run_selection.py . .remedy-wt/f074-r1-worker/selection-output.txt` — `paths 187`, `exit 0`, `8189 passed, 2 skipped in 86.31s (0:01:26)`. No FAILED, ERROR or "process(es) behind" line. The two SKIPPED lines, verbatim:
```
SKIPPED [1] tests/test_agent_tooling.py:43: D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted deliberately in 219dd32 (finding R-0074 — superseded by the split workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The read-only reviewer contract now lives there. Backlog: re-pin this contract on the split-workflow docs, or retire the test.
SKIPPED [1] tests/test_install_smoke.py:175: install smoke is opt-in: set REMEDY_INSTALL_SMOKE=1 on a host with network access
```

Gate 4: `python3 -m apps.cli.main integrity check --json` — `"fail_count": 0`, `"ok": true`, `"passed": true`; `handler_import` pass (handlers=195), `live_review_verdict` pass (last Gate verdict PASS), `plan_consistency` pass, `relevant_untracked` pass (untracked=0, relevant=0), `repo_root_hygiene` pass, `high_blockers_open` pass (no open blocker/high findings).

Gate 5: `python3 -c "import scripts.rotate_live_review as r; print(len(r.open_finding_ids(open('.agent/live_review.md').read())))"` — `7`.

## Authored-text proofs

`.agent/authored/f074-r1.md`: `wc -l` reads `117`, `sha256sum` reads `0aa8b4d08e7280e86c35c7e4aa6cd90aa665518961fb19c52e5b1440682c88ee`, equal to both `block.md` and the digest the delivering prompt named.

Every C1-C5 prepared file was copied by a Python byte copy (`shutil.copyfile`) and proven equal over bytes at copy time by comparing sha256 of source and destination; `verify.py` at gate 1 re-proved every one of them plus the whole-digest-list check, and reported `True` throughout.

## Deviations & assumptions

None. The block's ordered commit sequence (C0 through C6, gates 1-5, the push) was followed exactly; no extra commit, no dropped commit, no reordering.

## Next

1. Phase 1 rule 1 (`.agent/STOP`).
2. Rule 2, the Open PR Gate.
3. Book round 1's verdict in the next round's first commit.
4. T003: `remedy stats calibration` and the plan's band annotation.

Operator questions open: 0. Open findings: 7.

## For the operator, in plain sentences

Remedy now measures what each kind of task really costs from its own history, instead of always using the same fixed guess for every task of a given size. Once a kind of task has run often enough in a project, its cost estimates come from what those tasks actually used, and every such estimate says how many tasks it rests on; a kind of task that has not run often enough keeps the old fixed guess and says so. This measurement only reads the project's own record of past spending and never changes it. The three places that show a cost estimate before work starts all now use this measurement. A later step will add a command that shows the measurement itself and will teach the planning view to show it too. The whole test collection passed on the code that will ship, and a code-quality check and a repository-health check both passed as well. The branch has been pushed for review; no pull request was opened this round, as the plan for this step did not call for one.
