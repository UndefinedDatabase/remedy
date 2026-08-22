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
R37 records R36 and ends the session. THE BUILD IS COMPLETE: T001's catalog and
its derived coverage contract, T002's ring, feed, NowCard, recency dot and
scroll discipline, and T003's envelope linkage, row resolver, click-jump and
disabled steering input are all on disk and gated. Nothing of the feature's
change set remains unwritten. One correction is appended against OPEN finding
R-0629, minting no id.

## Next Steps
1. The INTEGRATION-GATE round: the whole suite at the branch tip, and the
   feature file's Goal & Done read clause by clause against what is on disk —
   the round that may only confirm, never build.
2. The evidence round, then the STATUS-commit round
   (docs/roadmap/STATUS_closure_protocol.md; the two are never one round).
3. The pull request, opened at closure and merged only at the Open PR Gate.

## Risks
- The build being complete is a claim about the CHANGE SET, not about the
  acceptance criteria. Only the integration-gate round can read Goal & Done
  clause by clause, and it may find a clause nothing on disk satisfies.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK.
- Nothing here renders CSS. R-0661's pin proves the unresolved-property SET has
  not grown; it cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0439, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed
  to a paydown branch.
