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
R40 is closure round one. It records the R39 verdict, then builds the two
artefacts the STATUS line quotes: the closure evidence bundle for job
`f021-closure` and a FRESH review zip, both covering the accepted HEAD this
round creates. No STATUS line, no README edit and no pull request happen here.

## Next Steps
1. Closure round two: the authored STATUS `[x]` line and the README capability
   sync in the SAME commit (R-0154), then the pull request.
2. The PR is NOT merged in this session; it merges at the next feature's start
   via the Open PR Gate, which is the operator's manual-review window.

## Risks
- The zip is a closure BLOCKER, not a formality: a PACKAGE_STATUS other than
  READY_FOR_REVIEW stops closure rather than being worked around.
- R-0663 is an ACCEPTANCE deviation and closure round two must rule on it: the
  shipped `.activityItem` sets `gap: 12px` where T5_F021's binding CSS says
  `gap:10px`. Either a DECISION accepts the CSS-module realization or a repair
  round changes it; the closure may not do both and may not do neither.
- Inherited High findings from closed features are documented risks rather than
  F021 defects, which is why the F021 verdict is PASS_WITH_RISKS, exactly as
  F008 and F009 closed before it.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364), which
  is R-0622 and routes to a paydown branch.
