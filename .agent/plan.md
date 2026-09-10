# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared.

## Current Step

ROUND 29 finishes R-0872. `architecture.md` gets the flat-to-group-first rename that Steps
38 to 40 performed on the CLI and never on the docs, every mapping resolved against the
shipped catalog rather than guessed; `vocabulary.md` stops spelling
F263's planned command as a runnable one. The R-0872 ratchet then falls to zero and is
deleted with its ceiling and its test, because a ratchet at zero is a gate that cannot fail.

## Next Steps

1. R-0873's ruling, which round 29 names as declined rather than performed: read the
   capability sweep's eighteen pages one by one and rule each DELETE, DATE or LEAVE,
   recording the ruling as a dated DECISION. `docs/archive/` is archival by design and is
   expected to survive it.
2. T002: the DECISION F272 D7 raising-property probe over every candidate `.id` receiver,
   giving the real site set rather than D15's upper bound, then the dated decision choosing
   the route. No production line moves in that slice.
3. T003, the classic runner, which T002's ruling is the prerequisite for.
4. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   STATUS line and the PR.

## Risks

- The open set is 89 by distinct id at this round's base `99e677f0`, computed mechanically
  from the record. This round registers none and resolves one, leaving 88. Four are High —
  R-0803, R-0804, R-0806 and R-0807 — all F273's rather than this feature's, per DECISION
  F272 D12.
- Deleting the ratchet removes the only mechanism that was counting the doc backlog. What
  replaces it is a guard with no exceptions at all, which is stronger — but it means the
  R-0873 residue is now carried by that finding alone, and nothing on disk counts it.
