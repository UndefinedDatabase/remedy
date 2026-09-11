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

ROUND 57 performs the migration DECISION F275 D33 rules, which is finding `R-0878`'s fix:
the seven production records that still declare a UUID-typed job or task id are retyped to
`str`, ONE RECORD PER COMMIT, and the last of the seven brings the ratchet that stops an
eighth arriving unseen. The one behaviour change in the whole migration is a single line —
a `.hex[:8]` read becomes `str(...)[:8]`, which is correct before and after the flip. The
round 56 PASS verdict and one dated prose slip are booked here.

## Next Steps

1. Build DECISION F275 D32's three retype rule families — the id VALUE at a target
   construction, a `.hex` or `.int` read on a now-`str` id, and a `.value` read on a
   now-`str` status — and re-run the flip dry run with its control at the same commit.
   The task-id half needs a ruling first: the unified task id is an ORDINAL, not a minted
   identifier, so a `Task(id=uuid4())` site has no mechanical counterpart.
2. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, declared with
   its inseparability reason before review, registering the `acceptance_checks` finding
   DECISION F275 D22 places with it.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- A retype changes an ANNOTATION, which Python does not enforce, so a green suite after
  this round proves the migration harmless and not that every reader was found.
- Three of the seven records are fed only by code the suite never executes.
- The open set is 87 by distinct id, with `R-0878` landed here and its resolution owed at
  the next gate. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's, per
  DECISION F272 D12.
