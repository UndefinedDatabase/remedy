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
R36 records R35 and builds the LAST unbuilt item of this feature. The steering
input ships as `components/panels/ChatInput.tsx`, the file component_spec.md
names, rendered VISIBLE and DISABLED in BOTH branches of the activity card with
the sentence ux_spec.md §11.3 binds — announced through `aria-describedby` and
not only through a tooltip a keyboard reader never sees. DECISION F021 D11
records which of two conflicting wordings ships and why. After this round every
item of T001, T002 and T003 is built.

## Next Steps
1. The integration-gate round: the whole suite at the branch tip, the feature
   file's Goal & Done read clause by clause against what is on disk.
2. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- A source contract sees the text of a call, never its effect. Nothing here
  proves the disabled input REMAINS inert at runtime; it proves the two
  `disabled` attributes and the announced reason are in the source.
- A worktree has no `node_modules`, so neither `tsc` nor a full vitest run can
  be dry-run there. The primary checkout is the only honest place for both.
- `npm run lint` is RED tree-wide at every commit under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0439, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed
  to a paydown branch.
