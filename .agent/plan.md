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

ROUND 56 sizes a premise underneath DECISION F275 D32's three retype rule families and finds
it short. D26's premise P2 selects records by `issubclass(obj, BaseModel)`, so it never saw a
dataclass; a sweep over the live objects of every class kind reads 13 records carrying a
UUID-typed field, 8 of them dataclasses, and SEVEN are fed by the flip. That is finding
`R-0878`, the artefact is `.agent/f275_t003_uuid_records.md`, and DECISION F275 D33 rules the
seven migrated one record per commit BEFORE any of D32's rule families is written. The round
55 PASS verdict and its dated prose slip are booked here.

## Next Steps

1. Migrate the seven records `R-0878` names, one per commit, in the order the artefact's
   construction counts give, with the ratchet DECISION F275 D33 requires as the last of them.
2. Build DECISION F275 D32's three retype rule families and re-run the flip dry run with its
   control at the same commit. The task-id half needs its own ruling first: the unified task
   id is an ORDINAL, not a minted identifier.
3. THE FLIP as the one declared-oversize commit AGENTS.md permits per feature, declared with
   its inseparability reason before review, registering the `acceptance_checks` finding
   DECISION F275 D22 places with it.
4. The resolver collapse DECISION F260 D5 places in T003, with the classic store, then the
   closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- The sweep behind `R-0878` reads a CONSTRUCTION; a field assigned after construction is not
  one, and that reading has not been taken.
- Three of the seven records are fed only by code the suite never executes, so a green run
  cannot speak for them.
- The open set is 87 by distinct id. Four are High — R-0803, R-0804, R-0806 and R-0807 — all
  F273's, per DECISION F272 D12.
