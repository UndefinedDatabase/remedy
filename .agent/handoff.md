# Handoff — amend1020-orb-insight (operator docs round)

Operator session, round 1, session 1 (not the loop; `.agent/STOP` untouched). Branch
`feature/amend1020-orb-insight` from `main` at `8ee02682d`, merged to `main` through its PR at the
operator's order ("Commit und Push auf main"; AGENTS.md forbids a direct commit to `main`, so the
round lands by PR merge). Commit SHAs: see `git log` on `main` after the merge.

## State
Four features registered THIN in Package 1 directly before F078, in the order F310, F312, F311,
F313 (DECISION amend1020 D1). Rule A5 now proposes F310 (`roadmap_index.next_feature` checked).
Three findings minted in `.agent/live_review.md`: R-1369 (High, owner F312), R-1370 and R-1371
(Medium, owner F310). No finding for the Orb's time-limit defect: it is Universe's (U513).

## Item status
| Item | Status | Reason |
|------|--------|--------|
| F310 feature file `T12_F310.md` | done | |
| F312 feature file `T2_F312.md` | done | |
| F311 feature file `T12_F311.md` | done | |
| F313 feature file `T12_F313.md` | done | |
| STATUS.md block before F078 (three headings, operator comment) | done | |
| R-1369 (order without file names, F312) | done | |
| R-1370 (two decisions for one budget stop, F310) | done | |
| R-1371 (wall clock counts waiting, F310) | done | |
| DECISION amend1020 D1 (`.agent/decisions.md`, cited in each feature file) | done | |
| README counters (313 registered; Tier 2 48, Tier 12 16) and `TOTAL_FEATURES` 313 | done | |
| `docs/README.md` | skipped | no document was added under `docs/` outside `docs/roadmap/features/`, which the index covers by its `T{tier}_F{nnn}.md` pattern |
| Commit and push to `main` | deviated | via feature branch, PR and merge (AGENTS.md: never commit directly to `main`) |

## Changed files
| File | Change |
|---|---|
| `docs/roadmap/features/T12_F310.md`, `T2_F312.md`, `T12_F311.md`, `T12_F313.md` | new, REGISTERED THIN |
| `docs/roadmap/STATUS.md` | amend1020 block before F078 |
| `README.md` | counters |
| `tests/docs/test_docs_consistency.py` | `TOTAL_FEATURES` 313 with its registration comment |
| `.agent/live_review.md`, `.agent/decisions.md`, `.agent/plan.md`, `.agent/context.md`, `.agent/handoff.md` | findings, D1, state |

## Verification
- `python3 -m pytest tests/docs -q -p no:cacheprovider` (Python 3.10): 341 passed. Only the docs
  tests, as ordered; no full run.
- `roadmap_index.next_feature(build_index('.'))` answers F310; the four files parse with no
  grammar violation.

## Read on the code (worth carrying into the rounds)
- F312: the person's order "Super, jetzt mach ein schickes design" has no fence by itself; the
  refusal came from `_deliverable_task_plan` judging against a milestone's planner-written job
  outline (`_step_shape` → `plan_order_job`).
- F310: job limits are `budget.*` filled by the task plan's suggested `budgets`
  (`do_sequence.py:518`); the lab job's 100,000 tokens exceed the order cap of 85,000, so the
  9 minutes very likely came from the local planner.

## Deviations
- Landed through a PR merge instead of a direct push to `main` (see above).
- The findings are written straight into `.agent/live_review.md` in this round, not only carried
  in this handoff (amend0827 rule 1 allows either).

Open findings: 84 before this round, 87 after (R-1369 to R-1371 open).

## Next
The operator starts the loop with `remedy-loop-feature`; it takes F310 first, whose first round
fills F310 D1 to D5 before any code.
