# Handback — F075 R3: R2 PASS persisted, R-0179/R-0180 fixed, run_mission boundary, all four injections live, campaign attempt 1 recorded (0/10).

HEAD 0a2ce17c · `P/`=packages/orchestration/ `T/`=tests/orchestration/ `S/`=scripts/

## Range
Review of ef23e274..0a2ce17c (8 commits, incl. this one).

## Commits

### c95f23db chore(f075): persist the R2 PASS, register R-0179/R-0180
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r3-{1,2,3}.md | +170 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +360/-244 | applied; block verbatim |

### 587ec34a fix(f075): a never-fired injection is a rejected disposition (R-0179)
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_{evaluator,injection}.py | +12/-3 | `injection_never_fired` -> REJECTED |
| T/test_gauntlet_injection.py | +34/-2 | pin + end-to-end verdict |
| .agent/{decisions,live_review}.md | +22 | pre-freeze rationale, Done: R-0179 |

### 97b6708a fix(f075): a dying order no longer takes the campaign with it (R-0180)
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_runner.py | +63/-12 | per-order boundary; `body` bound before try |
| T/test_gauntlet_runner.py | +58 | crash path raising; run_order raising |
| .agent/live_review.md | +8 | Done: R-0180 |

### d5213ad3 test(f075): pin the recorded set to the two mishandlings it records
| Path | +/- | Reason |
| --- | --- | --- |
| T/test_gauntlet_evaluator.py | +11/-1 | the R-0179 gate fix (see Verification) |

### 995b64ea feat(f075): run_mission catches an iteration failure and ends honestly
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +149/-71 | the boundary + `record_iteration_failure` |
| T/test_orchestrator_loop.py | +138 | 11 boundary tests |
| .agent/decisions.md | +43 | terminal name, scope, no-retry, PM place |

### 35cdc031 feat(f075): drive all four injection classes at their existing seams
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_injection.py | +190/-65 | `RaiseOnceInjector`, `InjectedSeams`, facts |
| P/gauntlet_runner.py | +47/-8 | dispatch/update_dossier seams in RunnerDeps |
| T/test_gauntlet_{injection,runner,self_run}.py | +318/-89 | all four driven; preflight tests |
| .agent/decisions.md | +36 | seam wiring + test-safety lesson |

### 0a2ce17c chore(f075): keep attempt 1 matrix and land live reports in the evidence area
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/gauntlet/attempt-01/matrix.{md,json} | +895 | the KEPT campaign artifact |
| S/self_run_gauntlet.py + its test | +38 | `--live` writes the matrix, pinned |
| .agent/decisions.md | +25 | why it was written after the fact |

### <this> chore(f075): handback R3
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/gauntlet-attempt-01 --format both` -> exit 1, 10 runs recorded. Evidence root OUTSIDE the repo; only matrix.md + matrix.json committed.

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_gauntlet_{injection,runner,evaluator}.py  ->  RED FIRST: 1 failed, 110 passed, exit 1
      test_the_recorded_set_covers_both_named_mishandlings: "Extra items in the right set: 'injection_never_fired'" — my own R-0179 change; a 2nd assertion pinned the same closed set. Fixed in d5213ad3, rerun -> 111 passed, exit 0  (P2 gate)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py  ->  184 passed, exit 0  (P3 gate; real filenames, e2e+era added as a stricter check)
    $ T/test_gauntlet_{injection,runner}.py T/test_self_run_gauntlet.py  ->  86 passed, exit 0  (P4 gate)
    $ the seven harness files  ->  235 passed, exit 0  (P5 gate; goldens UNCHANGED, nothing regenerated) — re-run after the P6 CLI fix -> 236 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Campaign attempt 1 — preconditions and result
Preconditions: porcelain empty; HEAD 35cdc031 == origin; ollama reachable (`orchestrator.model` unset, planner default); set_hash `d19c999a…8058fdc0` over ten orders; `preflight_injections` -> `[]`. Evidence root (NOT committed): `<session scratch>/gauntlet-attempt-01`; ~70 min wall.

Summary table, verbatim from the committed matrix.md:

    | run | order | kind | terminal | flawless | interventions | wall | tokens in/out |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | run-01-g01-pure-code-change | g01-pure-code-change | pure_code_change | iteration_limit | NO | 0 | 323.9s | 0/0 |
    | run-02-g02-test-add | g02-test-add | test_add | iteration_limit | NO | 0 | 420.4s | 0/0 |
    | run-03-g03-small-app-feature-smoke | g03-small-app-feature-smoke | small_app_feature_with_smoke | iteration_limit | NO | 0 | 229.1s | 0/0 |
    | run-04-g04-doc-generation | g04-doc-generation | doc_generation | iteration_limit | NO | 0 | 495.6s | 0/0 |
    | run-05-g05-two-milestone-mission | g05-two-milestone-mission | two_milestone_mission | iteration_limit | NO | 0 | 273.2s | 0/0 |
    | run-06-g06-provider-api-error-mid-move | g06-provider-api-error-mid-move | pure_code_change | iteration_failed | NO | 0 | 211.9s | 0/0 |
    | run-07-g07-truncated-model-response | g07-truncated-model-response | test_add | iteration_limit | NO | 0 | 587.9s | 0/0 |
    | run-08-g08-harness-death-mid-dispatch | g08-harness-death-mid-dispatch | small_app_feature_with_smoke | iteration_failed | NO | 0 | 377.9s | 0/0 |
    | run-09-g09-harness-death-mid-write | g09-harness-death-mid-write | two_milestone_mission | iteration_failed | NO | 0 | 151.1s | 0/0 |
    | run-10-g10-escalate-then-finish | g10-escalate-then-finish | doc_generation | iteration_limit | NO | 0 | 734.4s | 0/0 |

**0/10 flawless. NOT A PASS — reported, not gated.** Criteria held: start_command_only 10/10, host_data_root_untouched 10/10, injections_degraded 10/10, no_open_decisions 10/10, no_era_defect_classes 10/10, evidence_well_formed 10/10; no_unknown_postmortems 7/10; terminal_green 0/10; dod_blocking_green 0/10.
Attempt 1 says: (a) nothing reached `achieved` in budget and no DoD gate ever ran — the first real finding, for an R4 fix order; (b) all four faults FIRED and each degraded to `ledgered_failure` — the 2026-08-03 addition met live, the R3 boundary doing its job on three; (c) the raise-class runs lose `no_unknown_postmortems` because `failure_postmortem` reads "HTTP 503" as `unknown` (predicted in decisions.md BEFORE the run, not tuned around). Tokens 0/0 = the loop measured none, so none was written (R-0178); real spend is non-zero.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r3-1 `f1224711…720d97ae` == live_review.md AT the apply commit c95f23db (later appends are the permitted Done-marks only) · r3-2 `918012f5…6c5699e8` == plan.md · r3-3 `47e68f9d…5b2492af` == context.md

## Deviations & assumptions
- **Two commits over the 500-line cap, both declared.** 35cdc031 (753): `build_injectors` changing shape breaks three test files at once, so any split leaves a red intermediate commit — inseparable. 0a2ce17c (958): 895 of its lines are the generated campaign artifact the block orders committed whole. Per AGENTS.md the second is a Medium finding; I am reporting it rather than rewriting pushed history.
- **A test started a real campaign.** When the preflight stopped refusing, the R2-era `--live` CLI test fell through to production deps and ran real missions inside pytest. Killed in ~2 min. Host isolation HELD (every write landed in the run's own root under tmp_path; porcelain clean, real data root untouched) but real provider calls were made. Both obsolete tests are replaced by preflight-level ones that cannot start a campaign; recorded in decisions.md.
- **Escalation not used by the boundary**: F051 escalation asks a human a question; a raised failure is a failure to ledger. Honest terminal instead (decisions.md).
- **Attempt 1's matrix was written after the invocation**, from evidence already recorded and proven byte-identical to what the run printed. No rerun, no order edit; `--live` now writes it itself.
- Not taken unilaterally: the matrix reports the injections criterion but not per-fault dispositions (those live in each run.json).
- Handoff cap: 128 lines / ~2.3k tokens against 100 / 800. Eight mandatory commit tables plus the verbatim campaign table cost that alone; declared, no section dropped.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R2 PASS | done | |
| P2.1 R-0179 | done | |
| P2.2 R-0180 | done | |
| P2.3 gate | done | red first, fixed, exit 0 |
| P3 run_mission boundary | done | |
| P4 unblock three injections | done | |
| P5 full harness gate | done | goldens unchanged |
| P6 campaign attempt 1 | done | 0/10, matrix committed |
| P7 handback | done | |

## Next
Window 1 reviews R3 and rules on the two oversize commits. R4 = targeted fix orders from attempt 1 (nothing reaches `achieved`; no DoD gate runs; transport errors classify as `unknown`), then attempt 2.
