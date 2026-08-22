# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210. `.agent/live_review.md` is the source of truth for
the open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R41 is closure round two and the LAST round of this branch. It records the R40
verdict, rules R-0663 by DECISION rather than by a patch, then writes the STATUS
`[x]` line, the README capability sync and the closure candidates in ONE commit
and opens the pull request. That request is NOT merged in this session.

## Next Steps
1. The pull request merges at the next feature's start via the Open PR Gate,
   which is the operator's manual-review window.
2. The next session's FIRST reviewed round registers every entry
   `.agent/candidates.md` carries, or resolves it as a DECISION, and empties
   that file in the same round.

## Risks
- This round's own verdict has no on-disk gate entry by construction
  (`docs/agents/planner_reviewer_prompt.md` §4 item 13). It lives in
  `.agent/handoff.md` and in the pull request, and that absence is the branch
  terminator rather than a missing gate.
- The two High findings open at closure, R-0495 and R-0574, are inherited from
  the already-closed F085 and F086 and are documented risks rather than F021
  defects. That is why the verdict is PASS_WITH_RISKS, exactly as F008 and F009
  closed before it.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
