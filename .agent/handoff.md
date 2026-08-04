# Handback — F075 R6: R5 PASS persisted, R-0187 + R-0188 built. Phase 4 STOP; campaign not run.

HEAD d5e58526 · `P/`=packages/orchestration/ `T/`=tests/orchestration/ `S/`=scripts/

## Range
Review of 32e5e419..d5e58526 (5 commits, incl. this one).

## Commits

### 9e8ced5b chore(f075): persist the R5 PASS, register R-0187/R-0188
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r6-{1,2,3}.md | +196 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +369/-311 | applied; block verbatim |

### d54091e7 feat(f075): explicit cycles experiment override and order-set v2 (R-0187)
| Path | +/- | Reason |
| --- | --- | --- |
| P/long_run_executor.py | +41/-5 | `experiment_max_cycles`; `ResolvedCycles.to_json` |
| P/{orchestrator_loop,gauntlet_runner,gauntlet_orders}.py | +92/-8 | `JobExecution`; `execute_fn` seam; set v2 |
| S/gauntlet_orders/ (11 files) | +19/-9 | per-order max_cycles + v2 manifest |
| T/test_{long_run_executor,gauntlet_orders,gauntlet_runner}.py | +208/-7 | both clamps pinned; v2; pass-through |
| .agent/decisions.md | +40 | override + set-v2 rationale |

### 072a2025 feat(f075): store the milestone DoD at dispatch and gate at completion (R-0188)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +89/-1 | `attach_milestone_dod`; `run_gate_for_job` |
| T/test_orchestrator_loop.py | +168 | 13 tests: DoD reaches the job, gate at completion |
| .agent/decisions.md | +36 | wiring decisions; one-author verdict |

### d5e58526 docs(f075): R6 re-proof evidence — the orders have no repository
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +54 | Phase 4 trail; rule 4.3 STOP |

### <this> chore(f075): handback R6
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/reproof-r6 --only 1 --format json` -> exit 1, terminal `iteration_limit`. Evidence outside the repo, nothing committed from it. No campaign invocation (Phase 5 is gated on a green Phase 4).

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_gauntlet_{orders,runner}.py T/test_orchestrator_loop.py T/test_long_run_executor.py
      ->  279 passed, exit 0  (P2 gate; the executor's real test file is test_long_run_executor.py)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py T/test_gauntlet_{injection,runner}.py T/test_dod_gate.py
      ->  316 passed, exit 0  (P3 gate; the gate's real test file is test_dod_gate.py)
    $ the six remaining harness/executor files  ->  254 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Phase 4 proof — REQUIRED `achieved` + a RELEASED verdict: verdict present, NOT released. Rule 4.3 STOP.
Ledger, verbatim (trimmed):

    it1: dispatch_job -> dispatched
         job 412be9f0 ... dispatched for M001; DoD attached; executed:
         terminal=all_green job_status=completed cycles=4/experiment OVER-CAP
         gate=blocked (dod_blocking_red:acc-001)

`run.json`: `terminal_status: iteration_limit`, `cycles_budget: 4`, `cycles_resolved: ["cycles=4/experiment"]`. `dod_result.json` IS in the run dir — `released: false`, `blocking_red: ["acc-001"]`.

**Both R6 fixes work.** `DoD attached` (store_dod has a real caller at last), `cycles=4/experiment OVER-CAP` (the v2 budget reached the executor, recorded), jobs execute to `completed`, and the gate produces a persisted verdict — before R-0188 no run could produce one at all.

**Why blocked — the next blocker, not in scope.** The one red check:

    acc-001  kind=pytest  blocking=True  status=failed  reason=nonzero_exit
      no tests ran in 0.00s
      ERROR: file or directory not found: tests

**The gauntlet's missions have no repository.** The runner creates a project with `repo_paths: []` and `canonical_repo_path: None`; the job workspace holds only what the run produced (`['.pytest_cache', 'task_output']`). The orders say "in the sample project", but none is materialised — so a milestone whose DoD is "the unit suite is green" can never release: there is nothing to test. Same class as the R2 seam / R4 2c / R5 3.3: a missing piece of the campaign's world needing its own reviewed design (which repo the ten operate on, how it is materialised per run, how it stays isolated from the operator's tree).

Second observation, recorded not fixed: the six-dispatch pattern reappears for a DIFFERENT reason than R-0184 — every job now reaches `completed`, so the guard correctly allows a retry and the model retries because the gate blocked. Whether the loop should escalate after N identical failed attempts is a reviewer call.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r6-1 `701dbe26…f09dfe1b` == live_review.md AT the apply commit 9e8ced5b · r6-2 `7d88016f…980552221` == plan.md · r6-3 `f3855e51…2f8eddf6b7` == context.md

## Deviations & assumptions
- **Set v2 issued; campaign count reset** per T1_F075.md A9 — costs nothing, no attempt has ever passed. Set hash `b17540c381312b2c5dd40140396d1a489c0001c342572bb3276fc1ca9c6b994c`. Every existing freeze/tamper pin holds against v2 unchanged.
- **One existing test touched by EXTENSION**: `test_an_unknown_set_version_is_refused` used the literal `2`, which set v2 turned into the real version — the example became `GAUNTLET_ORDER_SET_VERSION + 1`, assertion unchanged. `test_the_set_is_frozen_at_version_one` was renamed to `..._at_the_declared_set_version` (its body already read the constant; only a now-false name changed). No assertion pinned the old gate-less behaviour — loop/e2e/era/injection/runner/dod_gate all green unedited.
- **`JobExecution` carrier** exists because `CycleLoopResult` is frozen; mutating the executor's own result type is F046's contract, not F075's.
- **Gate checks run in the job's workspace**, not a repo checkout — a gauntlet mission has none, and pointing them at one would run a mission's commands against the operator's tree.
- All commits under 500 lines; the oversize exemption stays spent (R-0181).
- Handoff cap: 109 lines / ~1.8k tokens against 60 / 800 — declared, no section dropped; the Phase 4 quotes are ordered content.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R5 PASS | done | |
| P2.1 cycles override | done | both clamps pinned |
| P2.2 order-set v2 | done | count reset per A9 |
| P2.3 runner pass-through | done | |
| P2.4 gate | done | exit 0 |
| P3.1 DoD at dispatch | done | |
| P3.2 gate at completion | done | one author |
| P3.3 tests | done | 13 new, provider-free |
| P3.4 gate | done | exit 0 |
| P4 re-proof | done | verdict present but blocked -> 4.3 STOP |
| P5 set-v2 campaign | skipped | gated on a green Phase 4 |
| P6 handback | done | |

## Next
Window 1 rules on the repository gap: what checkout the ten orders operate on and how it is materialised per run, isolated from the operator's tree. R7 = that, then the set-v2 campaign.
