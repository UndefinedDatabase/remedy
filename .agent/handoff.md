# Handback — F075 R5: R4 PASS persisted, R-0186 built (execution + guard). Phase 3 STOP; attempt 2 not run.

HEAD a25ce886 · `P/`=packages/orchestration/ `T/`=tests/orchestration/

## Range
Review of 49202f47..a25ce886 (4 commits, incl. this one).

## Commits

### 6a002f09 chore(f075): persist the R4 PASS, register R-0186
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r5-{1,2,3}.md | +176 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +314/-343 | applied; block verbatim |

### ce80e034 feat(f075): the loop runs the job it dispatches, and refuses a second one (R-0186)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +95/-3 | `execute` seam -> `execute_dispatched_job` (run_cycles); re-dispatch guard |
| T/test_orchestrator_loop.py | +190/-29 | 13 new tests; 29 call sites inject the executor double |
| T/test_mission_e2e.py | +27/-2 | executor double; no assertion changed |
| .agent/decisions.md | +69 | wiring decisions + the third missing link |

### a25ce886 docs(f075): R-0186 re-proof evidence and the two remaining blockers
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +53 | Phase 3 ledger quotes; rule 3.3 STOP |

### <this> chore(f075): handback R5
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/reproof-r0186 --only 1 --format json` -> exit 1, terminal `waiting_on_decisions`. Evidence outside the repo, nothing committed from it. No attempt-2 invocation (Phase 4 is gated on a green Phase 3).

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py T/test_gauntlet_{injection,runner}.py
      ->  268 passed, exit 0  (P2 gate). Injection/runner suites UNEDITED — g08 still fires at the dispatch seam.
    $ the six remaining harness/classifier files  ->  305 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

**Honest incident:** the first P2 run HUNG on a real provider call and was killed — the new `execute` seam defaults to production (`OllamaBuilder`), so every existing dispatching test fell into it. Fixed by injecting the executor double exactly as `dispatch` already is (29 sites): the seam's contract, not a workaround. No test takes a provider path now (R-0182); the gate runs in 1.6s.

## Phase 3 proof — REQUIRED terminal `achieved` + `dod_result.json`: NEITHER. Rule 3.3 STOP.
Re-proof ledger, verbatim (trimmed):

    it1: dispatch_job -> dispatched
         job 0db084c6 ... executed: terminal=all_green job_status=completed
    it2: dispatch_job -> dispatched
         job 20fba26e ... executed: terminal=max_cycles_reached job_status=running
    it3: dispatch_job -> refused
         milestone M001 already has job 20fba26e in flight (state running); a second
         job for it is refused. Instead: wait_on_decisions, or declare_milestone_done
         once that job finishes and its gate releases
    it4: wait_on_decisions -> waiting_on_decisions

Job states: `0db084c6 completed`, `20fba26e running`. No `dod_result.json`.
**R-0186 works** — R4's same-order run was six dispatches, six jobs, all `planned`, nothing executed, nothing refused. Now a job executes to `completed` and the six-dispatch loop is gone.
**Two blockers remain, neither in scope** (detail in decisions.md):
1. `CYCLE_SAFETY_CAP = 1`: a job needing >1 cycle ends `max_cycles_reached`/`running` — never terminal — and the schema has no resume kind, so it can never finish. Its own docstring says the cap stands "until the F075 milestone gate raises it": the gate must raise the cap, and the cap stops the gate passing. Raising it is a config default by machine — a reviewer DECISION.
2. No DoD verdict is reachable at all: `store_dod` has NO caller anywhere, and `run_job_gate`'s only caller is `job_fulfillment.run_job_fulfill` — "Spine v0 ... fixture-demo mode only", hardcoded CHANGELOG tasks, no production caller. So `dod_blocking_green` cannot be met by any run. Using the demo would make the gauntlet grade a demo (R2 rule); calling the gate from the loop is forbidden by this round's order.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r5-1 `5a6342c9…c339badab` == live_review.md AT the apply commit 6a002f09 · r5-2 `d7d08f7f…019ec44d` == plan.md · r5-3 `1d9bf4e8…ee53711a4` == context.md

## Deviations & assumptions
- **`paused` is NOT guarded**, deliberately: the move schema has no resume kind, so refusing a dispatch for a paused job leaves no legal advancing move after a human answers — a deadlock in place of a defect. Recorded as an observation (the absent resume verb), not fixed.
- **`test_mission_e2e.py` touched without changing any assertion**: its executor double now also takes the job out of `planned`, which a real executor always does. Test fidelity restored, not behaviour pinned. No test in any suite was edited to accommodate the new behaviour otherwise.
- All commits under 500 lines; the oversize exemption stays spent (R-0181).
- Handoff cap: 95 lines / ~1.55k tokens against 60 / 800 — declared, no section dropped; the Phase 3 ledger quotes are ordered content.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R4 PASS | done | |
| P2.1 execution wiring | done | |
| P2.2 re-dispatch guard | done | |
| P2.3 boundary + injections intact | done | injection suites unedited |
| P2.4 tests | done | 13 new; provider-free |
| P2.5 gate | done | exit 0 (after the killed provider hang) |
| P3 cheap re-proof | done | NOT achieved, no gate verdict -> 3.3 STOP |
| P4 attempt 2 | skipped | gated on a green Phase 3 |
| P5 handback | done | |

## Next
Window 1 rules on the two blockers: raising `CYCLE_SAFETY_CAP` (config default by machine) and a production DoD path (`store_dod` at dispatch + a non-fixture fulfillment). R6 = whichever it orders, then attempt 2.
