# Handback — F075 R10: R9 PASS persisted, R-0193 + R-0194 built. First flawless runs ever; campaign 3/10 on two findings.

`P/`=packages/orchestration/ `T/`=tests/orchestration/

## Range
Review of ae4c6e9a..HEAD (8 commits, incl. this one).

## Commits

### 43c9c9ca chore(f075): persist the R9 PASS, register R-0193/R-0194
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r10-{1,2,3}.md | +183 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +497/-220 | applied; block verbatim |

### 89269098 feat(f075): the context names a milestone ready to declare (R-0193)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +45 | SECTION_DIRECTIVES + released_milestone_directives, wired into run_mission |
| T/test_orchestrator_loop.py | +134 | 12 tests incl. 4 falsifying negatives + the economics |
| .agent/decisions.md | +36 | same seam as the guard; proof-only lines |

### 5001cc32 chore(f075): order-set v4 re-issues budgets from measured economics (R-0194)
| Path | +/- | Reason |
| --- | --- | --- |
| scripts/gauntlet_orders/g0*.json (10) | +40/-30 | budgets + budget_rationale ONLY |
| scripts/gauntlet_orders/manifest.json | +12/-12 | v4, fresh digests, set hash |
| P/gauntlet_orders.py | +6/-3 | version 4 and why |
| T/test_gauntlet_orders.py | +67/-2 | floor, anti-slack ceiling, frozen cycles |

### eb50818c docs(f075): R10 re-proof — achieved, released, zero refusals
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +46 | Phase 3/4 trail; the expansion caveat |

### 251eda85 · 13286cdc · 90f480ed — attempt-02 evidence, split for the 500 cap
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +70 | 251eda85: matrix + Findings A and B |
| .agent/gauntlet/attempt-02/matrix.{json,md} | +407 / +389 | 13286cdc · 90f480ed |

### <this> chore(f075): handback R10
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. `git push --force-with-lease` ONCE: cf695501 bundled the matrix and decisions at 866 lines; the R-0181 exemption is spent, so I reset and re-split it into 251eda85/13286cdc/90f480ed before review. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/reproof-r10 --only 1 --format json` -> exit 0, `achieved`.
- `self_run_gauntlet.py --live <scratch>/campaign-a02 --format both --out … --label attempt-02` -> exit 1, 3/10; ONE invocation, ten orders. Evidence outside the repo; only matrix.md/json committed.

## Verification
All `python3 -m pytest <path> -q`.

    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py
      ->  249 passed, exit 0   (P2 gate; e2e and era UNEDITED)
    $ T/test_gauntlet_{orders,runner}.py -> 86 passed, exit 0  (P3 gate)
    $ the seven harness files -> 266 · tests/cli/test_golden_path.py -> 42 (canary)
    $ git status --porcelain  ->  empty     [all exit 0]

## Phase 4 re-proof — achieved + released + zero open decisions: ALL THREE. First flawless run of this feature.

    terminal achieved · open_decisions [] · released true (acc-001 passed)
    nine/nine criteria · flawless true · 472s

DIRECT declare — the ledger holds NO refusal: it1 dispatch M001 gate=released,
it2 declare M001, … it7/it8 M004, it9 achieved. Two iterations per milestone
over four milestones, R-0193 as specified.

## Phase 5 — attempt 02: 3/10 (attempt 01 was 0/10). FLAWLESS: g01, g05, g07.
Held in all ten: start_command_only, no_unknown_postmortems, no_open_decisions, host_data_root_untouched, no_era_defect_classes, injections_degraded, evidence_well_formed. Zero refusals across all 74 iterations. Only `terminal_green` (7) and `dod_blocking_green` (3) ever failed. Detail in .agent/decisions.md; two findings for Window 1:

**A — plan expansion is erratic; no static budget fits.** Same order, same frozen world: g01 expanded 1→3 here, 1→4 in the re-proof, 1→3 in R9; g02/g03/g04 1→≥7; g05 2→2. Each `iteration_limit` run finished SIX milestones at two iterations each, then ran out mid-plan — economical and correct, still unable to finish. v4 assumed factor 3. R-0194 was right and is not enough; the fix is product-side (bound the expansion, or size from the compiled plan), not a v5.

**B — the exception boundary ends the mission where the pass definition needs it to continue.** `P/orchestrator_loop.py:984-993` classifies, ledgers, sets `terminal=True`, RETURNS. g06 (`provider_unavailable`), g08/g09 (`io_failure`) each died at iteration 1 with zero milestones, so no gate ran and `dod_blocking_green` fails as an absence. Counter-example g07: truncation is handled BELOW the boundary (`retry_within_budget`) and that mission reached `achieved`, FLAWLESS. g06's rationale sets the bar — "ledgered and retried within budget". As built, g06/g08/g09 cannot be flawless by construction.

## Authored-text proofs
`sha256sum` on disk vs the state file AT the apply commit 43c9c9ca — all three equal:
- r10-1 `b3e2c7dc…52bf7` == live_review.md · r10-2 `9fe17718…c99a8` == plan.md · r10-3 `13d724a1…9e48f` == context.md

## Deviations & assumptions
- **One test edited**: `test_the_set_is_at_version_three` -> `…_four`, the literal the constant made stale. No other existing test touched; e2e and era green unedited.
- **`budget_rationale` is a new order field**, ignored by the loader — the sizing reason ships with the order it sizes.
- **`max_cycles` NOT re-sized**: R9 measured those right; an edit without evidence is the guess v4 replaces.
- **Findings A and B are reported, not fixed** — each needs its own reviewed round; neither is an order edit, and orders stay frozen mid-campaign.
- All commits under 500 lines; the exemption stays spent (R-0181) — see the force-with-lease note.
- Handoff cap: 101 lines / ~1.4k tokens against 100 / 800 — token overage declared, no section dropped.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R9 PASS | done | three texts sha256-verified |
| P2 R-0193 | done | 12 tests, gate 249 |
| P3 R-0194 v4 | done | budgets only, proven byte-identical elsewhere |
| P4 re-proof | done | achieved + released + 0 open, DIRECT declare |
| P5 set-v4 campaign | done | 3/10, matrix committed |
| P6 handback | done | |

## Next
Window 1 rules on Findings A and B — the erratic expansion and the terminating boundary. R11 = whichever it orders, then attempt 03.
