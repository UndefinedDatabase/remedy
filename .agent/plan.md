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

ROUND 50 re-runs the flip dry run against a tree whose id shape is one spelling, and records
what it measured in `.agent/f275_t003_flip_residue_r50.md`. The migration DECISIONs F275 D26,
D27 and D28 performed removed 369 failures and nothing else: measured against a control taken
at the same commit, the flip still causes 2557 failures and 106 errors. Three prerequisites
are diagnosed and ruled in DECISION F275 D29. The round 49 PASS verdict and the resolution of
`R-0876` are booked here.

## Next Steps

1. P1 — replace the transform's receiver-NAME heuristic with the DECISION F272 D7
   raising-property probe that `docs/roadmap/features/T2_F275.md` T002 already orders, and
   measure the real site set.
2. P2 — migrate the surviving `UUID(...)` coercions over a job or task id, one
   assignment-connected component per commit, as DECISION F275 D28 rules for an id widen.
3. P3 — the `**` splat call-graph pass over the test helper factories.
4. Re-run the dry run, then THE FLIP as the one declared-oversize commit AGENTS.md permits
   per feature, declared with its inseparability reason before review.
5. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
6. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 reaches the soft limit amend0908-f275-finish rule 1 names — 20 sessions — in this
  session, at 50 of its 60 rounds. Rule 2 forbids the split-and-close default here BY NAME:
  the session writes the scope report and CONTINUES.
- The three prerequisites are the diagnosed causes of MEASURED classes; nothing establishes
  that a fourth does not appear once they are fixed, and only another dry run settles it.
- The open set is 86 by distinct id once this round books `Done: R-0876`. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
