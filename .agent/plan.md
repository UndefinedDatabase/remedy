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
R35 records R34 and finishes T003's click-jump by wiring the resolver R34
landed. `ActivityFeedCard` renders a row that resolves to a node as a BUTTON
that emits `onSelectNode`, and a row that resolves to nothing as the article it
always was, so the affordance never claims a jump the row cannot make.
`RightLivePanel` hands the card the task list and the focus callback the
checklist beside it already uses. A `tests/ui_contracts/` source contract pins
that the component really calls the rule — the half no vitest run can see, and
the half that was missing while `feedScroll.ts` sat unimported for fourteen
rounds. One correction is appended against OPEN finding R-0402.

## Next Steps
1. R36: the steering input, rendered DISABLED with the tooltip naming F030 —
   the last unbuilt item of T003 and of the feature.
2. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- A source contract can only see the text of a call, never its effect. This one
  asserts against COMMENT-STRIPPED source (R-0584) and reads the
  `<ActivityFeedCard` line rather than the whole panel file, because the
  TaskChecklistCard line beside it carries the same two props.
- A worktree has no `node_modules`, so neither `tsc` nor a full vitest run can
  be dry-run there. The primary checkout is the only honest place for both.
- `npm run lint` is RED tree-wide at every commit under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622, R-0629,
  R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed to a
  paydown branch.
