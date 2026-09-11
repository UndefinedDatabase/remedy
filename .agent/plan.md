# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 52 completes `R-0877`. Round 51 made the run-log seam join its id verbatim; 26 call
sites in 12 files still wrapped that id in `UUID(...)`, so one job's run log landed in two
directories and each reader saw only its own half — measured at `87d76c66` as two
directories for one id, with neither reader seeing both events. All 26 wraps are removed by
one `ast` pass, the six imports it orphans go with it, and a repo-wide sweep test keeps the
count at zero. The round 51 PASS verdict is booked here.

## Next Steps

1. The reviewer's authored `Done: R-0877`, covering both halves, at the next gate.
2. P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe `docs/roadmap/features/T2_F275.md` T002 already orders. The probe
   and its site set exist at `0b009325` in `.agent/f275_t002_flip_inventory.md`; T003
   re-derives them at its own base, as that file says it must.
3. P3 — the `**` splat call-graph pass over the test helper factories.
4. Re-run the flip dry run, then THE FLIP as the one declared-oversize commit AGENTS.md
   permits per feature, declared with its inseparability reason before review.
5. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
6. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The remaining `UUID(...)` sites are NOT this class: they hold a value that is legitimately
  a `uuid.UUID` in the classic record, so they move WITH the flip and not before it.
- The open set is 87 by distinct id. Four are High — R-0803, R-0804, R-0806 and R-0807 —
  all F273's, per DECISION F272 D12.
