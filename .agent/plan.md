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

ROUND 74 REPAIRS ROUND 73, WHICH FAILED. D47 discharged D45's precondition on a coverage
reading taken inside a fresh worktree; re-run there it gives 23 unexecuted rather than 0,
because a worktree has no built UI dist. The reading moves to the PRIMARY CHECKOUT, where the
suite runs, and the question sharpens from "is the line executed" to "how many tests witness
it": zero for none, exactly one for eleven, a median of seventeen, over 7065 site-and-test
pairs. Each of the eleven thin sites is red-proved against its own single witness, mutating
the ATTRIBUTE NODE the ruled set records rather than the first textual match. DECISION F275
D48 corrects D47 by appending, never by rewriting.

## Next Steps

1. Re-run the flip's dry run against the corrected inputs of rounds 67 and 69 together — the
   plain re-derivation and the re-keyed set — the first reading of what both corrections
   cost in FAILURES rather than in sites.
2. The resolver collapse DECISION F260 D5 places in T003, which DECISION F275 D37 names as
   the home of the id-SHAPE seam behind the three largest residue classes. Production code,
   so a SPLIT round with mutation red-proofs.
3. THE FLIP, which D48 permits on D47's corrected footing, carrying D48's obligations: the
   full suite is the backstop, and the eleven thin sites are named rather than averaged.
4. Then the classic store, then the closure sequence.

## Risks

- F275 is past the soft limit amend0908-f275-finish rule 1 names. Rule 2 forbids the
  split-and-close default BY NAME: a session writes the scope report and CONTINUES.
- A MEASUREMENT TAKEN IN A WORKTREE IS A MEASUREMENT OF THAT WORKTREE. The UI dist and
  `node_modules` are absent there, so any suite-wide reading taken in one is about the
  environment. Round 73 shipped a decision on such a reading.
- THE SUITE HAS ENVIRONMENT-SENSITIVE TESTS. A perf budget and a workspace-identity pair go
  red or green by load under coverage, and pass in isolation. No gate may demand a green
  full-suite run as its pass condition.
- The open set is 87 by distinct id, with `R-0880` open. Four are High — R-0803, R-0804,
  R-0806 and R-0807 — all F273's, per DECISION F272 D12.
