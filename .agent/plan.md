# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 23 drafts DECISION F260 D3, the deletion paragraph T001 names as its last item and
F275's Goal & Done makes a closing condition: every module F260's Design listed, the feature
that inherited its idea, and the ideas deleted rather than inherited, with the finding ids
that hold each enumeration. DECISION F275 D12 rules the three questions R-0866, R-0867 and
R-0868 hand to this round; DECISION F275 D13 records that the fix clauses bound to "the D3
round" are discharged across this round and the next, because they do not fit one block.
The round also books session 12's pending record and repairs two stale comments and two
vacuous test assertions.

## Next Steps

1. The repairs the D3 fix clauses leave outstanding: R-0832's event-name couplings and the
   dead code they left, R-0859's two dangling `related=` references and its
   referential-closure test, R-0858's F267 repair, R-0843's `Groups` table, and R-0868's
   retirement of the four now-vacuous cluster scaffolding artefacts.
2. T002, the atomic record flip, alone, because every later commit's size depends on it.
3. T003, the classic runner, which T002's ruling is the prerequisite for.

## Risks

- The open set is 91 by distinct id at this round's base `6f865e50`, computed mechanically
  from the record. This round registers two and resolves one, leaving 92. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- DECISION F260 D3 lands in an append-only file and cannot be corrected, only superseded, so
  every module-to-feature mapping in it is taken from a dated finding or a dated decision
  rather than from the reviewer's reading of what a module looked like it did.
- R-0855 is RESOLVED, not open. Session 12's handoff routed two new residues to it as an open
  finding; they are registered as R-0870 instead.
