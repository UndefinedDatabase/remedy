# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 10, the first closure repair round. It books round 9's PASS, registers
R-1039 and records the self-use run's recurrence of R-1035, repairs R-1039 —
the runtime-integration gate's registry check still pinned `os.replace` — and
re-runs the feature's full suite, rewriting the transcript, which must show the
five bad nodes gone and none newly bad.

## Next Steps

1. The closure sequence's second half: the evidence job and a fresh review
   zip, from a clean tree after the last content commit.
2. The closing round: the ledger rotation, the STATUS line with the README
   counters in the same commit, and the pull request, which is never merged
   in the session that opens it.

## Risks

Twenty-seven findings are open after this round's registration, one of them
this feature's own until its resolution is booked. Ten rounds are spent of the
soft limit of 25; amendment rule 2 allows two more repair rounds.
