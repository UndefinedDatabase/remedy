# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 7 of this feature, in its closure sequence.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001, T002 and T003 | done | rounds 1-24 |
| R-0749, both instances | done | resolved round 27 |
| the operator guide and its index rows | done | round 26 |
| the integration gate | done | round 27, PASS WITH RISKS |
| the feature file's Built State | open | this round |
| the evidence job and the review zip | open | this round |
| the STATUS line, the README sync and the PR | open | next round |
| R-0745 and R-0750, carried as documented risks | open | see Risks |

## Next Steps
1. This round books the round 27 verdict, registers R-0750, extends R-0736, and
   performs the closure preconditions that must hold BEFORE a STATUS line can be
   authored: the Built State section, the integrity check, the evidence job and
   a review zip built from a clean tree after the last content commit.
2. The NEXT round is the closure commit itself — the STATUS `[x]` line and the
   README capability sync in ONE commit, the final `.agent/` state, then the
   pull request. That PR is NOT merged in this session; it merges at the next
   feature's start via the Open PR Gate, which is the operator's review window.
3. `self-use NONE (queue exhausted)` is recorded at closure: the queue holds no
   pending item, which the closure protocol rules is exhausted rather than
   blocked.

## Risks
- R-0745 (Low) and R-0750 (Medium) stay OPEN at closure, so the STATUS line
  reads PASS_WITH_RISKS. Neither is reachable from this feature's Acceptance:
  the first hardens a guard over the write door, the second is a reviewer's gate
  wording that ordered a full log where the canonical procedure asks for a tail.
