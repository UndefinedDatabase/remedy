# Handback — F075 R2: R1 PASS persisted, R-0178 fixed, T003a runner. STOPPED before the campaign.

HEAD b16c3cf4 · `P/`=packages/orchestration/ `T/`=tests/orchestration/ `S/`=scripts/

## Range
Review of 740ff133..b16c3cf4 (7 commits, incl. this one).

## Commits

### 55f706db chore(f075): persist the R1 PASS, register R-0178
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r2-{1,2,3}.md | +105 | saved first |
| .agent/{live_review,plan,context}.md | +58/-26 | applied |
| .agent/last_block.md | +175/-170 | block, verbatim |

### a11e089e fix(f075): malformed evidence numbers are load errors (R-0178)
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_evidence.py | +40/-10 | non-numeric -> load_error |
| T/test_gauntlet_evidence.py | +63/-2 | one falsification per field |
| .agent/live_review.md | +9 | Done: R-0178 |

### ebd7de26 feat(f075): injection driver at existing loop seams
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_injection.py | +206 | truncated driver; blocked refused |
| T/test_gauntlet_injection.py | +172 | dispositions from behaviour |
| .agent/decisions.md | +53 | T003a decisions + the seam |

### 6aaedbdf feat(f075): live gauntlet runner
| Path | +/- | Reason |
| --- | --- | --- |
| P/gauntlet_runner.py | +443 | isolated root/run, real-root hashing |

### 5245c024 test(f075): runner isolation, budgets, evidence, crash containment
| Path | +/- | Reason |
| --- | --- | --- |
| T/test_gauntlet_runner.py | +402 | no provider calls; real evaluator |

### b16c3cf4 feat(f075): wire the live campaign into the CLI
| Path | +/- | Reason |
| --- | --- | --- |
| S/self_run_gauntlet.py | +85/-4 | `--live` + preflight refusal |
| T/test_self_run_gauntlet.py | +81/-3 | modes, preflight, live matrix |

### <this> chore(f075): handback R2
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after Phase 1, Phase 2, T003a gate. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/gauntlet-attempt-01` -> exit 2, refused, nothing written.

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_gauntlet_{evidence,evaluator,matrix}.py  ->  111 passed, exit 0  (P2 gate; goldens UNCHANGED, no regeneration)
    $ T/test_gauntlet_{runner,injection,evidence,evaluator,matrix,orders}.py T/test_self_run_gauntlet.py  ->  205 passed, exit 0  (T003a SLICE GATE)
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r2-1 `41e4bed4…f77c3371` == live_review.md (at apply, before the Done-mark) · r2-2 `cb9730c9…1c72cfb7` == plan.md
- r2-3 `3eddb2c4…1620efcb` matches its BEGIN hash; applied to context.md as the one-occurrence FROM->two-TO-lines replacement, copied from the saved file.

## STOP — the missing seam (Phase 4 not run)
Per the HARD RULE. **`orchestrator_loop.run_mission` has no exception boundary** — no `try`/`except` in its body, none around `dispatch`, and `run_structured_call` retries PARSE failures only. Proven by running the code: a raising `call_fn` escaped at `orchestrator_loop.py:834`, a raising `update_dossier` at `:811`; either way no ledger entry, no F010 postmortem, no terminal. So 3 of 4 injection classes cannot be driven honestly. Full analysis + the exact fix: `.agent/decisions.md`, 2026-08-04 entry. Not faked by a harness `except` — that would grade Remedy's crutch. `truncated_model_response` IS injectable today.
Preconditions met and recorded: porcelain empty, pushed, provider reachable, set_hash `d19c999a…8058fdc0` over ten orders. Refused at preflight: no `.agent/gauntlet/attempt-01/`, no matrix claimed, zero tokens spent.

## Deviations & assumptions
- Runner split: `gauntlet_runner.py` executes, `gauntlet_injection.py` faults; judging stays the evaluator's. No commit over 500 lines.
- `load_mission` added to `RunnerDeps`; every dep defaults to the production verb (asserted).
- Budgets via existing keys: iterations->`LoopLimits`, tokens/wall->`REMEDY_BUDGET_*` (seconds round UP, never 0). Unmeasured tokens omit `tokens` rather than writing 0 (R-0178 at the source).
- Cap: 93 lines (<=100 for >5 commits) but ~1.2k tokens against the 800 cap. Declared rather than met: seven mandatory per-commit tables plus the STOP cost that alone. Trimmed transcripts and moved the seam analysis to decisions.md; no section dropped.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R1 PASS | done | |
| P2 fix R-0178 | done | goldens unchanged |
| P3.1 runner + `--live` | done | |
| P3.2 injection driver | deviated | 1/4 classes driveable; 3 refused loudly |
| P3.3 runner tests | done | |
| P3.4 slice gate | done | exit 0 |
| P4 campaign attempt 1 | skipped | STOP: missing exception boundary |
| P5 handback | done | |

## Next
Window 1 rules on the seam. R3 = the `run_mission` exception boundary as its own order, then the three injections, then attempt 1.
