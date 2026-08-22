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
R34 records R33 and takes the client half of T003 as far as one round's cap
allows: `FeedRow` gains `taskId` from the envelope field R33 landed, and the new
pure module `apps/ui/src/api/feedFocus.ts` resolves a row to a graph node
through the task list the dashboard already carries — never by matching on seq
or timestamp, which DECISION F021 D2 rejected. `actionClass.test.ts` rides along
because it constructs a `FeedRow` under an explicit return type and would
otherwise stop typechecking. Three corrections are appended against OPEN
findings R-0369, R-0419 and R-0630, none minting an id.

## Next Steps
1. R35: the wiring — `ActivityFeedCard` renders a resolvable row as a button
   that emits `onSelectNode`, `RightLivePanel` passes the task list down, and a
   `tests/ui_contracts/` source contract pins that the component really calls
   the resolver.
2. R36: the steering input, rendered DISABLED with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- `feedFocus.ts` lands this round with NO caller. That is deliberate and is
  bounded to one round by the step above; it is not the R17 drift, where
  `feedScroll.ts` sat unimported for fourteen rounds before R31 wired it.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- A worktree has no `node_modules`, so neither `tsc` nor a full vitest run can
  be dry-run there. The primary checkout is the only honest place for both.
- `npm run lint` is RED tree-wide at every commit under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0403, R-0419, R-0587,
  R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622, R-0629, R-0630,
  R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed to a paydown
  branch.
