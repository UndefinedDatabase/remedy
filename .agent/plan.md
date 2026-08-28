# Plan — F032 Approval with the evidence triple

Branch: feature/f032-evidence-triple, cut from `main` at `a399a330`, the merge
commit of pull request #216 which closed the amend0827 process-diet order.
`.agent/live_review.md` is the review record and the finding-id ceiling;
`.agent/decisions.md` carries the DECISION series, F032 D1 through D8.

## Goal
No decision without its receipts. Every decision a human is asked to answer
carries the evidence triple — `evidence_refs[]`, `expected_outcome` and
`downside` — the inbox card renders all three, and a producer that omits one
fails its own test. `docs/roadmap/features/T5_F032.md` holds Goal & Done, the
task slicing and the design amendments that reconcile it with the source.

## Current Step
R19 CLOSES F032. T001, T002 and T003 are complete, the integration gate passed
at R17 with an empty branch-only failure set, and R18 produced the evidence
bundle and the review package from the accepted HEAD `c3cf408f`. This round
books the R18 verdict, flips the STATUS line to `[x]` and syncs the README's
capability prose and its two ledger-derived counts in the SAME commit — they
may never disagree in a committed state — and then opens the pull request.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R18 verdict and the reviewer's slip | ordered | the record is touched first |
| C3 the closure commit and the handback | ordered | STATUS and README together, last on the branch |
| the pull request | ordered | after C3; NOT merged this session |

## Next Steps
1. The pull request merges at the NEXT feature's start, through the Open PR
   Gate of AGENTS.md. The gap is the operator's manual review window, and the
   operator may merge manually at any time instead.
2. The next feature is chosen by Rule A5 from `docs/roadmap/STATUS.md`, in a
   fresh session. `docs/roadmap/STATUS.md` names F037 as the next open line.

## Risks
- The package's filename, SHA-256 and archived path rest on R18's transcript:
  the archive directory lies outside this session's allowed working
  directories, so the reviewer could not re-read them.
- R-0714 is open and Medium. It does not touch F032's own code; it makes the
  integration gate's auto-build lever unenforceable and belongs to whoever
  repairs `tests/ui_server/test_dashboard_contract.py`.
