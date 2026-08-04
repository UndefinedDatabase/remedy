# Handback — F075 R4: R3 PASS persisted, R-0185 + R-0183 fixed, R-0184 diagnosed. STOPPED on rule 2c; attempt 2 not run.

HEAD 0ccf44d7 · `P/`=packages/orchestration/ `T/`=tests/orchestration/

## Range
Review of a4cb91ca..0ccf44d7 (5 commits, incl. this one).

## Commits

### e5ca780e chore(f075): persist the R3 PASS, register R-0181..R-0185
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r4-{1,2,3}.md | +170 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +398/-286 | applied; block verbatim |

### 7202beca fix(f075): classify transport and machine failures instead of unknown (R-0185)
| Path | +/- | Reason |
| --- | --- | --- |
| P/failure_postmortem.py | +56 | ConnectionError->provider_unavailable; new `io_failure`; 2 predicates |
| T/test_failure_postmortem.py | +89 | per-class + falsification; +1 reachability producer |
| T/test_orchestrator_loop.py | +40/-2 | both injected shapes end-to-end |
| .agent/decisions.md | +37 | taxonomy rationale + the 2 touched tests |

### 364c68ef fix(f075): an unmeasured token count says so in both matrix formats (R-0183)
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_{evidence,evaluator,matrix}.py | +56/-7 | `tokens_measured`; md "unmeasured", json null+source |
| T/test_gauntlet_{evidence,matrix}.py | +73 | measured/unmeasured/true-zero cases |
| fixtures/gauntlet/golden/matrix.json | +9 | REGENERATED (declared below) |
| .agent/decisions.md | +21 | rendering-only rationale |

### 0ccf44d7 docs(f075): R-0184 diagnosis — the loop creates jobs it never executes
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +76 | the analysis with raw quotes; rule 2c |

### <this> chore(f075): handback R4
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/diag-r0184 --only 1 --format json` -> exit 1, `iteration_limit`. Diagnostic only; evidence outside the repo, nothing committed from it. No attempt-2 invocation (gated on a green 2a+3; fork was 2c).

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_failure_postmortem.py T/test_orchestrator_loop.py  ->  RED FIRST: 1 failed, 245 passed
      test_a_class_it_cannot_determine_is_recorded_as_unknown: "assert 'provider_unavailable' == 'unknown'" — my own R3 test used "HTTP 503" as its unclassifiable example, which IS the dishonest unknown R-0185 fixes. Input changed, assertion unchanged. Rerun -> 246 passed, exit 0  (P2 gate)
    $ T/test_gauntlet_{evidence,matrix,evaluator}.py  ->  123 passed, exit 0  (P3 gate)
    $ the seven harness files  ->  244 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## R-0184 diagnosis (full text + raw quotes: .agent/decisions.md)
One `--only 1` live run reproduced attempt 1's g01 exactly.
- (a) **The model is not the blocker**: six schema-valid `dispatch_job` moves, on-topic rationales, none refused.
- (b) All six dispatched jobs sit at `state=planned`, tasks built, never touched. `execute_move` is `create = dispatch or continue_mission` — creation is where it stops.
- (c) `declare_milestone_done` never becomes true (needs a finished job + released gate), so dispatch stays the only useful move. `evaluate_dispatch` refuses done/unknown/unmet-deps milestones but NOT one with an in-flight job -> mission ends `active`, `_milestones_done=None`, `job_links=6`.
- (d) The DoD gate is **never invoked**: no `dod.json`/`dod_result.json` anywhere; `run_job_gate`'s one caller is `job_fulfillment.py:1003`, part of job execution.
- **Root cause:** the loop's docstring names the verb map ("`continue_mission` dispatches, `long_run_executor` executes, `dod_gate` evaluates") but it imports `long_run_executor` only for `next_cycle_index` and never calls `run_cycles`. T1_F070's Design specifies that step; the build omits it.
- **Fork -> 2c, STOP.** Closing it = running each job through `run_cycles` in the loop with budgets, stop/safe-point handling and cycle accounting, then the gate verdict, plus a re-dispatch guard: F070's missing half, product work with its own tests. NOT done: no `orchestrator.model` change (model is not the blocker; config defaults by machine are do-not-touch), no order edits, no weakened pass definition.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r4-1 `941af73a…53811d8d` == live_review.md AT the apply commit e5ca780e · r4-2 `a4a90b75…1b2fb428` == plan.md · r4-3 `e975c006…3ff5b8bc0` == context.md

## Deviations & assumptions
- **Golden regeneration declared:** `golden/matrix.json` +9 lines (one `tokens_source` per run). `golden/matrix.md` byte-identical — every fixture is measured, so the new wording appears only in the new tests' own evidence. No fixture edited.
- **Two existing tests touched by EXTENSION, not weakening** (per-test in decisions.md): a producer added for `IO_FAILURE`; the pinned-unknown loop test given a genuinely unrecognisable input.
- `ConnectionError` maps to the EXISTING `provider_unavailable`; only `io_failure` is new. F001's retry predicates untouched — widening those changes retry behaviour, not this finding.
- All commits under 500 lines; the oversize exemption stays spent (R-0181). Handoff cap: 91 lines / ~1.5k tokens against 60 / 800 — declared, no section dropped. Five mandatory commit tables, the ordered R-0184 summary and the item table cost that; the full analysis lives in decisions.md rather than here.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R3 PASS | done | |
| P2 R-0185 | done | red first, cause explained, rerun exit 0 |
| P3 R-0183 | done | goldens regenerated, declared |
| P4 R-0184 diagnosis | done | fork = 2c |
| P4.2a bounded fix | skipped | not a bounded bug — see analysis |
| P4.3 cheap re-proof | skipped | gated on 2a |
| P5 attempt 2 | skipped | gated on a green 2a+3 |
| P6 handback | done | |

## Next
Window 1 rules on R-0184. R5 = wiring `long_run_executor.run_cycles` into the loop (+ the re-dispatch guard) as its own reviewed order, then attempt 2.
