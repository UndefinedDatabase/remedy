# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7, closing the feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002 and T003 | done | rounds 1-24 |
| the operator guide and its index rows | done | round 26 |
| the integration gate | done | round 27, PASS WITH RISKS |
| the Built State, evidence job and review zip | done | round 28 |
| the STATUS line, the README sync and the PR | done | this round |
| R-0745 and R-0750, carried as documented risks | open | see Risks |

## Next Steps
1. This round books the round 28 PASS, flips the STATUS line to `[x]` with the
   README capability sync in the SAME commit, and opens the pull request.
2. THE PR IS NOT MERGED IN THIS SESSION. It merges at the next feature's start
   through the Open PR Gate, which is the operator's manual-review window; the
   operator may also merge it by hand at any time.
3. The next session starts a NEW feature: read `.agent/STOP` first, then run the
   Open PR Gate, which will find this PR and merge it before any new branch.
4. Nothing further is owed on this branch. Its last round has no on-disk gate
   entry by construction, and that absence is the terminator rather than a
   missing review.

## Risks
- R-0745 (Low) and R-0750 (Medium) stay OPEN at closure, which is why the STATUS
  line reads PASS_WITH_RISKS. Neither is reachable from this feature's
  Acceptance: the first hardens an import guard over the write door, the second
  is a reviewer's gate wording that ordered a full run log where the canonical
  integration-gate procedure asks for a tail.
