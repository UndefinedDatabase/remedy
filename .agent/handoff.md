# Handback — F075 R7: R6 PASS persisted, R-0189 + R-0190 built, gate RELEASES. Phase 4 STOP; campaign not run.

HEAD 40d47533 · `P/`=packages/orchestration/ `T/`=tests/orchestration/ `S/`=scripts/

## Range
Review of 73c19023..40d47533 (7 commits, incl. this one).

## Commits

### df856730 chore(f075): persist the R6 PASS, register R-0189/R-0190
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r7-{1,2,3}.md | +195 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +348/-354 | applied; block verbatim |

### 2eb5ab46 feat(f075): sample-project source for the gauntlet to work on (R-0189)
| Path | +/- | Reason |
| --- | --- | --- |
| S/gauntlet_sample_project/{sampleproj/ (7), conftest.py} | +299 | config/retry/parsing/importer/report/cli/errors; importable with no install |

### 0cc11d4d test(f075): the sample project's green suite, README and changelog (R-0189)
| Path | +/- | Reason |
| --- | --- | --- |
| S/gauntlet_sample_project/tests/ (6 files) | +174 | 30 tests, offline, ~0.05s |
| S/gauntlet_sample_project/{README,CHANGELOG}.md | +55 | what g04 documents and g10 describes |

### 7404fdf9 feat(f075): freeze the template and materialise it per run (R-0189)
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_orders.py | +54/-9 | `template_tree_digest`; v3; digest in the set hash |
| P/gauntlet_runner.py | +79/-11 | `materialise_sample_project`; project points at the copy |
| P/orchestrator_loop.py | +7/-2 | `worktree_root` threaded to the gate |
| S/gauntlet_orders/manifest.json | +3/-2 | v3 + template digest |
| T/test_gauntlet_{orders,runner}.py | +143/-10 | v3 pins, tamper refusal, copy self-sufficiency |
| .agent/decisions.md | +52 | goal-vs-template audit + decisions |

### e19af5e6 feat(f075): escalate after two consecutive gate-blocked completions (R-0190)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +67 | streak per milestone; existing F051 hand_over |
| T/test_orchestrator_loop.py | +132 | 9 tests incl. reset and per-milestone cases |
| .agent/decisions.md | +17 | why two, and why per milestone |

### 40d47533 docs(f075): R7 re-proof evidence — the gate releases, the claim is never made
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +44 | Phase 4 trail; rule 4.3 STOP |

### <this> chore(f075): handback R7
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/reproof-r7 --only 1 --format json` -> exit 1, terminal `iteration_limit`. Evidence outside the repo, nothing committed from it. No campaign invocation (Phase 5 is gated on a green Phase 4).

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_gauntlet_{orders,runner}.py  ->  81 passed, exit 0  (P2 gate a)
    $ cd <scratch>/tmpl-proof/run-01/workspace && python3 -m pytest tests -q
      ->  30 passed, exit 0  (P2 gate b — the suite green FROM a scratch materialised copy, no install, no outside PYTHONPATH)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py T/test_gauntlet_injection.py
      ->  259 passed, exit 0  (P3 gate; all four suites UNEDITED)
    $ the seven remaining harness/executor/gate files  ->  376 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Goal-vs-template audit (all ten meaningful; NO order edited)
| Order | What the goal names | Where it is in the template |
| --- | --- | --- |
| g01 | hard-coded retry backoff cap | `retry.py` `BACKOFF_CAP_SECONDS = 30` |
| g02 | config precedence arg>env>file | `config.py` `resolve()`, `ENV_VARS` |
| g03 | CLI progress output to suppress | `cli.py` progress->stdout, errors->stderr |
| g04 | env vars + rules to document | `config.ENV_VARS` + README "Configuration" |
| g05 | duplicated path normalisation ×2 | identical marked block in `importer.py` + `report.py` |
| g06 | parse entry point returning None | `parsing.py` `parse_record()` |
| g07 | exact user-facing error text | `errors.py` message constants |
| g08 | import command writing to a dir | `cli.py import` + `importer.plan_import` |
| g09 | report writer + CLI render | `report.py` + `cli.py report` |
| g10 | release history, next version unstated | `CHANGELOG.md` 0.1.0/0.2.0/0.3.0 |

## Phase 4 proof — REQUIRED `achieved` + released verdict: RELEASED yes, `achieved` no. Rule 4.3 STOP.

    dod_result.json: released: true, blocking_red: [], error: ""
      check acc-001  kind=pytest  status=passed  exit_code=0
    run.json: terminal_status iteration_limit · cycles_budget 4 ·
              cycles_resolved ["cycles=4/experiment"] ·
              template_digest 1c4f41bf991a5b3626a72d5de60eba76948e82ec3181cff1f2dc4d5dd4ef0454

Ledger, every iteration: `dispatch_job -> dispatched :: job … dispatched for M001; DoD attached; executed: terminal=all_green job_status=completed cycles=4/experiment OVER-CAP gate=released`.

**R-0189 did what it was for**: `acc-001` — the check that read "file or directory not found: tests" in R6 — passed with exit 0. First released verdict in this feature's history.

**Why still not `achieved`**: six dispatches of M001, all completing with a RELEASED gate, and the model never chose `declare_milestone_done`. End state `status: active`, `_milestones_done: None`, `job_links: 6`. R-0190 correctly did not fire — it escalates a BLOCKED streak, and nothing was blocked.

One missing guard remains, symmetric with the two built: `evaluate_dispatch` refuses a second job while one is IN FLIGHT (R-0186) and the loop escalates two consecutive BLOCKED completions (R-0190), but nothing refuses a dispatch for a milestone whose latest job COMPLETED with a RELEASED gate — the one case where the only correct move is `declare_milestone_done`. Not built: not this round's scope, and 4.3 says stop.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r7-1 `35bed48d…a56319bf` == live_review.md AT the apply commit df856730 · r7-2 `1382a11c…48427985` == plan.md · r7-3 `cf8121ef…575e8e043` == context.md

## Deviations & assumptions
- **Set v3 issued; count reset** per A9 — nothing lost, no attempt has passed. Set hash `c267ccabf9b021c9c1f01c126d09c1308436457a22a0373ef490ebd989aaebb6`, template digest `1c4f41bf…d4ef0454`. Tampering with any template file is refused at load (pinned), and a manifest with no `template_digest` is refused outright.
- **Two existing order tests changed because a literal became reality**: `test_the_set_is_at_version_two` -> `..._three`, and the set-hash test now also passes the template digest (v3 folds it in). No assertion weakened; no other suite edited.
- **The template is committed to the repo but never executed from it** — each run works on its own copy under `<run_dir>/workspace`, git-initialised with a baseline commit. Two runs cannot see each other's edits (pinned).
- **Gate checks run in that copy**, not the operator's tree, via the `worktree_root` the runner binds.
- All commits under 500 lines; the oversize exemption stays spent (R-0181).
- Handoff cap: 126 lines / ~2k tokens against 60 / 800 — declared, no section dropped; the audit table and Phase 4 quotes are ordered content.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R6 PASS | done | |
| P2.1 template + goal audit | done | all ten meaningful, no order edited |
| P2.2 materialisation per run | done | |
| P2.3 freeze v3 + digest | done | |
| P2.4 gate (suites + scratch copy) | done | exit 0 both |
| P3 blocked-gate escalation | done | 9 tests, suites unedited |
| P4 re-proof | done | released verdict, but not `achieved` -> 4.3 STOP |
| P5 set-v3 campaign | skipped | gated on a green Phase 4 |
| P6 handback | done | |

## Next
Window 1 rules on the released-gate dispatch guard (refuse a dispatch when the milestone's latest job completed with a released gate; tell the model to declare it done). R8 = that, then the set-v3 campaign.
