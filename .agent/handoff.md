# Handback — F075 R11: R-0196 + R-0197 built. Attempt 03 is 10/10 FLAWLESS from one invocation — the milestone gate's own bar, met.

`P/`=packages/orchestration/ `T/`=tests/orchestration/

## Range
Review of e4119c86..HEAD (8 commits, incl. this one).

## Commits

### 4792dd02 chore(f075): persist the R10 PASS, register R-0195..R-0197
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r11-{1,2,3}.md | +216 | saved first, sha256 verified |
| .agent/{live_review,plan,context,last_block}.md | +457/-371 | applied; block verbatim |

### 583bc2c9 feat(f075): a retryable failure costs the iteration, not the mission (R-0196)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +91/-7 | narrow retryable set, OUTCOME_ITERATION_RETRYING, per-milestone streak |
| P/gauntlet_injection.py | +14/-2 | a green terminal WITH a post-mortem is recovery, not silence |
| T/test_orchestrator_loop.py | +215/-7 | 11 new; 3 updated with the reason inline |
| T/test_gauntlet_injection.py | +34/-3 | 3 new on the two green readings |
| .agent/decisions.md | +36 | the four decisions and what is deliberately excluded |

### 25d04521 feat(f075): the compiler honors the order's declared milestone shape (R-0197)
| Path | +/- | Reason |
| --- | --- | --- |
| P/mission_compiler.py | +60/-4 | max_milestones, resolve_milestone_cap, capped draft subclass |
| P/gauntlet_runner.py | +7/-1 | passes len(order.milestones) + 1 |
| T/test_mission_compiler.py | +89 | 8 incl. the None-is-identical proof |
| T/test_gauntlet_runner.py | +35/-2 | cap derived, not hard-coded |
| .agent/decisions.md | +31 | why enforced twice, why a subclass |

### 3b929970 · eefaaf59 docs(f075): the re-proofs, then attempt 03
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +37 / +42 | 3b929970: Phase 4 trail · eefaaf59: Phase 5 matrix + the I/O observation |

### 67eb8f86 · d84e114c — attempt-03 evidence, sliced under the cap
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/gauntlet/attempt-03/matrix.{json,md} | +327 / +350 | 67eb8f86 · d84e114c |

### <this> chore(f075): handback R11
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. NO force-push (R-0195 honoured). No PR (comes at closure).
- `self_run_gauntlet.py --live <job tmp>/reproof-r11-g06 --only 6 --format json` -> exit 0, achieved.
- `self_run_gauntlet.py --live <job tmp>/reproof-r11-g02 --only 2 --format json` -> exit 0, achieved.
- `self_run_gauntlet.py --live <job tmp>/campaign-a03 --format both --out <job tmp>/campaign-a03-matrix --label attempt-03` -> exit 0, 10/10. ONE invocation, ten orders, evidence root outside the repo; only matrix.md/json committed.

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py -> 42 passed, exit 0            (P1 gate)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py
      T/test_gauntlet_injection.py T/test_gauntlet_runner.py
      -> 338 passed, exit 0                                          (P2 gate)
    $ T/test_mission_compiler.py T/test_gauntlet_runner.py
      -> 154 passed, exit 0                                          (P3 gate)
    $ tests/cli/test_golden_path.py -> 42 passed, exit 0    (P5 gate / canary)
    $ matrix.json parses, runs_recorded 10                           (P5 gate)
    $ git status --porcelain -> empty

## Phase 4 — both re-proofs green

Re-proof 1 (`--only 6`), every required fact:

    terminal achieved · open_decisions [] · dod released true
    injection: raised at call_fn call 1: ConnectionError ... HTTP 503;
      ledgered with 1 post-mortem(s), then the run recovered and finished
    disposition retry_within_budget · post-mortem provider_unavailable
    it1 iteration_failed_retrying · it2 dispatched (all_green, released)
    it3 milestone_done · it4 achieved

Re-proof 2 (`--only 2`): `compiled milestones ['M001','M002']`, origin provider — g02 declares ONE, so the cap was 2 and `<= declared + 1` holds. `achieved` in 5 iterations against g02's v4 budget of 12, released, zero open decisions.

## Phase 5 — attempt 03: 10/10 FLAWLESS, `passed: true`, `failure_kinds: []`

    run                            terminal    it done retry open
    g01 pure-code-change           achieved     5    2     0    0
    g02 test-add                   achieved     3    1     0    0
    g03 small-app-feature-smoke    achieved     5    2     0    0
    g04 doc-generation             achieved     5    2     0    0
    g05 two-milestone-mission      achieved     7    3     0    0
    g06 provider-api-error         achieved     4    1     1    0
    g07 truncated-model-response   achieved     5    2     0    0
    g08 harness-death-mid-dispatch achieved     6    2     1    0
    g09 harness-death-mid-write    achieved     8    3     1    0
    g10 escalate-then-finish       achieved     5    2     0    0

Evidence root `<job tmp>/campaign-a03`. Preconditions verified before the run: porcelain empty, pushed, set v4 hash `e50916bf…` equal to its recomputation, `preflight_injections -> []`. All four injections FIRED and all four settled `retry_within_budget` — none `never_fired`, none `silent_success`. Attempt 01 = 0/10, attempt 02 = 3/10.

## Authored-text proofs
`sha256sum` on disk == the BEGIN digest == the state file at the apply commit 4792dd02, all three:
- r11-1 `f5663147…50bc7` == live_review.md · r11-2 `a13ff18b…b69de` == plan.md · r11-3 `fcdb32ee…87b855` == context.md

## Deviations & assumptions
- **4792dd02 is 1044 lines — OVER the cap, DECLARED not rewritten (R-0195).** The block ordered the three applied texts and the verbatim block as ONE commit ("Commit 1"), and its content is the reviewer's own authored text; the remedy is the reviewer's to order.
- **Three existing tests were updated**, each because R-0196 deliberately changes the terminal it asserted; the reason is stated inline and their subject (the failure CLASS) is unchanged. Two runner-double signatures gained the new kwarg.
- **`retry_within_budget` for the raise classes is a reading of the product's facts**, not a new disposition — the closed set is untouched.
- **NEW, unfixed: the campaign read ~872 GB while writing ~2 MB** (~12 MB/s, I/O pressure ~15%). Results are unaffected and isolation held, but the volume is out of proportion to a 2 MB evidence tree. Needs a finding ID.
- Every other commit under 500 lines; the oversize exemption stays spent (R-0181).
- Handoff cap: 120 lines / ~1.6k tokens against 100 / 800 — declared, no section dropped; the two proof blocks are ordered content.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R10 PASS | done | three texts sha256-verified |
| P2 R-0196 | done | 14 new tests, gate 338 |
| P3 R-0197 | done | 10 new tests, gate 154 |
| P4 re-proofs | done | both green, all required facts quoted |
| P5 attempt 03 | done | 10/10 flawless, matrix committed sliced |
| P6 handback | done | |

## Next
Window 1 rules on 10/10. If it stands, F075's DONE condition is met and the next step is the integration gate, then closure with the prepared-but-not-applied CYCLE_SAFETY_CAP config diff + ADR.
