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

ROUND 63 DIAGNOSES the three largest residue classes and DECISION F275 D37 rules them. They
are ONE id-SHAPE seam, not a fourth rule family and not a data migration: a resolver that
searches only the classic store, and a handler layer that parses its argument into a
`uuid.UUID` and hands the OBJECT to the store. The candidate fourth rule was built, applied
and run; it fixed 16 and BROKE 2, and 247 of 263 survived. The artefact is
`.agent/f275_t003_flip_residue_r63.md`. The round 62 verdict and its two prose slips are
booked here. No line under `packages/`, `apps/`, `tests/`, `docs/` or `scripts/` moves.

## Next Steps

1. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 now names
   as the home of both halves of the seam: one resolver reaching both stores, and the
   handler layer routed through it instead of through `UUID(...)`. Production code, so a
   SPLIT round with mutation red-proofs.
2. Build `R-0880`'s second obligation, the transform's refusal to rename a site whose owner
   verdict cannot be confirmed, and resolve the 39 pairs or re-derive the site set with a
   column in its key. DECISION F275 D36 forbids the flip commit until one of those lands.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, registering
   the `acceptance_checks` finding DECISION F275 D22 places with it.
4. The classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- 1186 failures is not a landable state, and the largest classes are now understood to need
  PRODUCTION-CODE work rather than another transform rule — a bigger step, not a smaller one.
- The 42 errors have not moved across three runs and are still undiagnosed.
- The open set is 88 by distinct id, with `R-0879` and `R-0880` both open. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
