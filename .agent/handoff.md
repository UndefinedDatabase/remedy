# Handback — F075 R8: R7 PASS persisted, R-0191 built and obeyed. Phase 3 STOP; campaign not run.

HEAD 467adaa4 · `P/`=packages/orchestration/ `T/`=tests/orchestration/

## Range
Review of 854a9860..467adaa4 (4 commits, incl. this one).

## Commits

### 1fe38c56 chore(f075): persist the R7 PASS, register R-0191
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/authored/f075-r8-{1,2,3}.md | +174 | saved first |
| .agent/{live_review,plan,context,last_block}.md | +236/-308 | applied; block verbatim |

### 03038187 feat(f075): refuse a dispatch when the milestone is already proven done (R-0191)
| Path | +/- | Reason |
| --- | --- | --- |
| P/orchestrator_loop.py | +34 | `_released_gate_refusal`; the triad's third leg |
| T/test_orchestrator_loop.py | +104 | 9 tests incl. end-to-end achieve and LATEST-rules |
| .agent/decisions.md | +36 | guard table + why the loop must not self-declare |

### 467adaa4 docs(f075): R8 re-proof — the guard lands, a refused dispatch erases the attribution
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/decisions.md | +54 | Phase 3 trail; rule 3.3 STOP; the next defect, located |

### <this> chore(f075): handback R8
| Path | +/- | Reason |
| --- | --- | --- |
| .agent/handoff.md | rewrite | this handback (R-0149 self-ref) |
| .agent/last_block.md | +1/-1 | OUTCOME |

## External actions
- `git push` after every phase. No PR (comes at closure).
- `self_run_gauntlet.py --live <scratch>/reproof-r8 --only 1 --format json` -> exit 1, terminal `escalated`. Evidence outside the repo, nothing committed from it. No campaign invocation (Phase 4 is gated on a green Phase 3).

## Verification
All `python3 -m pytest <path> -q`.

    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (P1 gate)
    $ T/test_orchestrator_loop.py T/test_mission_e2e.py T/test_era_integrity.py T/test_gauntlet_{injection,runner}.py
      ->  307 passed, exit 0  (P2 gate; all five suites UNEDITED)
    $ the seven remaining harness/executor/gate files  ->  291 passed, exit 0
    $ tests/cli/test_golden_path.py  ->  42 passed, exit 0  (canary)
    $ git status --porcelain  ->  empty

## Phase 3 proof — REQUIRED `achieved` + released verdict: RELEASED yes, `achieved` no. Rule 3.3 STOP.

    run.json: terminal_status escalated · cycles_resolved ["cycles=4/experiment"] ·
              template_digest 1c4f41bf991a5b36… · open_decisions 1
    dod_result.json: released: true · acc-001 passed

Ledger, verbatim:

    it1: dispatch_job -> dispatched
         job fe02e963 … DoD attached; executed: terminal=all_green
         job_status=completed cycles=4/experiment OVER-CAP gate=released
    it2: dispatch_job -> refused
         milestone M001 is already finished: job fe02e963 completed and its
         Definition of Done RELEASED. Another job would repeat work that is
         already proven. Instead: declare_milestone_done for M001
    it3: declare_milestone_done -> escalated
         refused twice in a row (no job was ever dispatched for milestone M001,
         so there is nothing whose outcome could meet its Definition of Done);
         escalated: td:55642ed3

**R-0191 works and the model obeyed it.** R7's six identical dispatches became one dispatch, one instructive refusal, and the model then chose `declare_milestone_done` — exactly the move the refusal named.

**What blocked it: a latent defect the guard exposed.** `dispatched_job_for` keeps the LAST ledger entry whose move kind is `dispatch_job` for the milestone and reads its `outcome.job_id`. A REFUSED dispatch is still a `dispatch_job` move, and its outcome has no `job_id` — so it overwrote the real attribution with `""`. At it3 the evidence said "no job was ever dispatched", `evaluate_milestone_done` correctly refused a claim it could not verify, and the second-refusal rule escalated. The run also ends with 1 open decision, so it would fail `no_open_decisions` too.

Pre-existing, not introduced: before R-0191 nothing refused a dispatch, so no ledger ever held a refused `dispatch_job` entry beside a real one. The fix is one condition — an entry with no `job_id` (outcome status not `dispatched`) is not a dispatch and must not erase the attribution — plus tests for the refused-then-claim sequence above. Not applied: 3.3 says commit nothing further.

## Authored-text proofs
`sha256sum` on disk vs the committed `.agent/authored/` file:
- r8-1 `bc4c813c…3657ba3f` == live_review.md AT the apply commit 1fe38c56 · r8-2 `c28791b0…1051a525` == plan.md · r8-3 `e97aae16…15e6c2f80` == context.md

## Deviations & assumptions
- **The guard reads the verdict, never re-derives it**: `collect_milestone_evidence` already asks `load_gate_result` for the milestone's latest job, so a newer un-released job supersedes an older released one by construction. A test asserts the guard's source never mentions `blocking_red` or `checks`.
- **Only `gate_released is True` fires it.** `None` (no stored DoD) proves nothing, `False` belongs to R-0190 — two guards arguing over one fact would be worse than the hole.
- **The loop does not declare the milestone itself.** The claim is the model's move and carries its accountability; the loop refuses what cannot help and names what can. Auto-declaring was rejected as a breach of the F070 authority boundary.
- No existing test was edited this round; all five P2 suites are green unedited.
- All commits under 500 lines; the oversize exemption stays spent (R-0181).
- Handoff cap: 98 lines / ~1.5k tokens against 60 / 800 — declared, no section dropped; the Phase 3 ledger quotes are ordered content.

## Item status
| Item | Status | Reason |
| --- | --- | --- |
| P1 persist R7 PASS | done | |
| P2.1 released-gate guard | done | |
| P2.2 tests | done | 9, provider-free |
| P2.3 gate | done | exit 0 |
| P3 re-proof | done | released verdict, terminal `escalated` -> 3.3 STOP |
| P4 set-v3 campaign | skipped | gated on a green Phase 3 |
| P5 handback | done | |

## Next
Window 1 rules on the attribution defect: a refused `dispatch_job` entry must not clear `dispatched_job_for`'s answer. R9 = that one condition with its tests, then the set-v3 campaign.
