# Plan — F279 Configuration & toolchain truth

Branch: feature/f279-configuration-toolchain-truth, cut from `main` at
`c9bc5c20`, the merge commit of pull request 266 (F278's closure).

## Goal

Three things this repository asserts about itself become measurable: which
environment variables exist, which tool versions CI installs, and which
checklist items a machine can check (`docs/roadmap/features/T2_F279.md`).

## Current Step

ROUND 7 books round 6's PASS, records DECISION F279 D7, and lands T004's
order half: `docs/orders/toolchain-refresh.md` as a job file, indexed and
pinned by a docs test, and the self-use generator's order tier, which queues
it verbatim, first, at most every fourteen days. With it every slice of
F279 — T001, T002, T003 and T004 — is built.

## Next Steps

1. The closure sequence per `docs/roadmap/STATUS_closure_protocol.md`: the
   built state and the one checklist consolidation pass, the self-use item,
   the one full-suite run with its repair rounds, the evidence bundle and
   review package, the ledger rotation, the STATUS flip and the pull request.

## Risks

`constraints.txt` (round 1) is F279's one declared oversize commit; no
second may follow. Hosted CI first runs the new install steps at the
closure's pull request. The closure's self-use item is the toolchain
refresh order, the heaviest job the track has queued so far.
