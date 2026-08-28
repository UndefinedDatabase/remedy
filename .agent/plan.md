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
T003 is COMPLETE: the model carries the triple, the card renders it, and the
receipt chip is the entry point F023 wires. R16 is the integration gate of
docs/agents/integration_gate.md — the full suite on this branch and at the
merge base `a399a330` with artifact parity restored and measured, the two
failure sets compared, every branch-only id attributed. It writes no production
code. The frontend is REBUILT before the branch run, because R14 and R15 edited
`apps/ui/src` and a stale dist makes the suite rebuild itself mid-run.

| Item | Status | Reason |
|------|--------|--------|
| C0a and C0b, save and mirror the block | ordered | |
| C1 the plan | ordered | first substantive commit |
| C2 the R15 verdict and the reviewer's prose slip | ordered | the record is touched first |
| C3 the gate evidence directory | ordered | S1 to S8 |
| C4 the handback | ordered | |

## Next Steps
1. The closure sequence, part one: the evidence job and a FRESH review zip, per
   docs/roadmap/STATUS_closure_protocol.md.
2. The closure sequence, part two: the authored STATUS line committed last on
   the branch, then the pull request, which is NOT merged in this session.

## Risks
- A branch-only failure that reproduces serially and touches this feature's
  code is a blocker, not a repair to fold into this round; it would cost a
  reviewer-gated round of its own before closure can start.
- The base worktree carries neither `node_modules` nor `dist`, both gitignored.
  Parity is restored by copy and then MEASURED by an mtime window, because the
  environment variable that disables the auto-build has been ignored once.
