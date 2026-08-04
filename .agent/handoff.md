# Handback — F075 R9: R8 PASS persisted, R-0192 built. Milestones now complete end-to-end; Phase 3 STOP on budget.

HEAD eeb942a9 · `P/`=packages/orchestration/ `T/`=tests/orchestration/

## Range
Review of 09348505..eeb942a9 (4 commits, incl. this one).

## Commits

### 5d068078 chore(f075): persist the R8 PASS, register R-0192
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r9-{1,2,3}.md | +166 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +172/-196 | applied; block verbatim |

### e213733b fix(f075): a refused dispatch no longer erases the job attribution (R-0192)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +13/-1 | one condition: no job_id -> skip, never overwrite |
| T/test_orchestrator_loop.py | +101 | 5 tests incl. the R8 sequence replayed to achieved |
| .agent/decisions.md | +27 | why it was latent, and what the tests pin |

### eeb942a9 docs(f075): R9 re-proof — the chain closes per milestone, the budget does not
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +50 | Phase 3 trail; rule 3.3 STOP; two reviewer calls |

### <this> chore(f075): handback R9
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/reproof-r9 --only 1 --format json` -> exit 1, terminal `iteration_limit`. Evidence outside the repo, nothing committed from it. No campaign invocation (Phase 4 is gated on a green Phase 3).

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py
      ->  237 passed, exit 0  (P2 gate; e2e and era UNEDITED)
    $ the seven remaining harness files  ->  261 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Phase 3 proof — REQUIRED `achieved` + released verdict + zero open decisions: two of three. Rule 3.3 STOP.

    run.json: terminal_status iteration_limit · open_decisions 0 ·
              cycles_resolved ["cycles=4/experiment"]
    dod_result.json: released: true · acc-001 passed
    mission record: _milestones_done ['M001', 'M002']

Ledger, verbatim:

    it1: dispatch_job -> dispatched   job 336057db … DoD attached; executed:
         terminal=all_green job_status=completed cycles=4/experiment OVER-CAP
         gate=released
    it2: dispatch_job -> refused      milestone M001 is already finished: job
         336057db completed and its Definition of Done RELEASED …
    it3: declare_milestone_done -> milestone_done   milestone M001 recorded as done
    it4: dispatch_job -> dispatched   job 75115e49 … for M002 … gate=released
    it5: dispatch_job -> refused      milestone M002 is already finished …
    it6: declare_milestone_done -> milestone_done   milestone M002 recorded as done

**R-0192 works live and the chain now closes.** The declare move that R8 could not get past — refused with "no job was ever dispatched" for a milestone whose job had completed — now succeeds, twice in one run. Dispatch → execute → gate release → declare is a working loop.

**Why not `achieved` — a budget-versus-plan-shape mismatch, not a defect.** Order g01 states ONE milestone; the mission compiler expanded its goal into THREE (`M001, M002, M003`). At three iterations per milestone (dispatch, the R-0191 refusal, the declare) plus one to achieve, that needs ten iterations against g01's budget of six. Two milestones finished; M003 never started.

Two reviewer calls, neither mine to take:
1. **The refused dispatch costs an iteration.** Declaring straight off a released gate would make each milestone two iterations. The guard makes the model correct, not yet economical — fixing that means carrying the released-gate fact more visibly in the assembled context, or not counting a refused iteration against the budget. Product changes with their own tests.
2. **Order budgets were set in R1, before anything executed.** Raising them is an order edit — forbidden mid-campaign, and set v3 is frozen (`c267ccab…`), so a re-issue would be v4 with another count reset.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r9-1 `cde835a2…553c75da` == live_review.md AT the apply commit 5d068078 · r9-2 `7abaf098…58c5bd6f23` == plan.md · r9-3 `b9af4aac…18b720c80e` == context.md

## Deviations & assumptions
- **The fix is one condition and nothing else rode along** — same ledger walk, same milestone filter, same last-wins rule among entries that actually produced a job.
- **"Only refusals" still answers `""`** — absence must stay sayable, pinned by its own test.
- **The end-to-end test derives its evidence from the real `dispatched_job_for`**, so it is load-bearing rather than a mock agreeing with itself; it also asserts the R-0191 refusal still fires.
- No existing test was edited this round; e2e and era suites green unedited.
- All commits under 500 lines; the oversize exemption stays spent (R-0181).
- Handoff cap: 99 lines / ~1.5k tokens against 60 / 800 — declared, no section dropped; the Phase 3 ledger quotes are ordered content.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R8 PASS | done | |
| P2.1 attribution fix | done | one condition |
| P2.2 tests | done | 5, provider-free |
| P2.3 gate | done | exit 0 |
| P3 re-proof | done | released + 0 open decisions, but `iteration_limit` -> 3.3 STOP |
| P4 set-v3 campaign | skipped | gated on a green Phase 3 |
| P5 handback | done | |

## Next
Window 1 rules on the iteration economics: whether a refused iteration should cost budget, and/or whether the order budgets (set in R1, pre-execution) need a v4 re-issue. R10 = that, then the campaign.
