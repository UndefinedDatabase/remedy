# Plan — F260 One world: mission → job → run

Branch: feature/f260-one-world. Rounds 1 to 23 are reviewed; round 1 FAILED and was
repaired, and 2 to 23 PASSED. DECISION F260 D8 closes this feature at the scope it
built; the follow-up feature registered directly after F260 carries the remainder.

## Goal

Close F260. This is the LAST round of the branch: the STATUS line goes to `[x]`,
the README is synced in the same commit, self-use item SU-011 is marked consumed,
and the pull request is opened and left UNMERGED as the operator's review window.

## Current Step

Round 24 books round 23's verdict and the resolution of `R-0817`, then lands the
STATUS flip, the README capability sync, the `consumed_by` edit and the handback in
ONE commit — the last on this branch (Rule A4) — and opens the pull request. The
ledger rotation ran in round 22 and is not repeated. The evidence job and the
review package were built in round 23 and are not rebuilt.

## Next Steps

1. The operator's review window: the pull request stays OPEN and UNMERGED. It is
   merged at the start of the next feature through the AGENTS.md Open PR Gate, or
   manually by the operator at any time before that.
2. The next feature is the follow-up registered directly after F260 in the ledger,
   which Rule A5 proposes first; it starts in a fresh session.

## Risks

- Nothing may follow the closure commit on this branch. A commit after it breaks
  Rule A4's rendering, which the ledger cross-check pins.
- README and STATUS may never disagree in any committed state, which is why both
  land in the same commit (R-0154).
