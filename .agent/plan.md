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
R29 rules the NowCard badge's liveness source, the question R28 left open, and
applies the ruling. DECISION F021 D9 chooses the conjunction: the badge lights
only when the agent is RUNNING and the recency rule also reads live, so the
badge and the dot can never claim opposite things and "Live" can never render
beside the word "Idle". The round also records R28 and adds its own gate defect
to R-0618 rather than minting a second id for a class already open.

## Next Steps
1. R30: `feedScroll.ts` into the feed's scroll container with the new-rows pill
   component_spec.md line 86 binds. Headless since R17 and the last rule this
   feature has built and left unread.
2. R31: the row click-jump to the graph store, then T003's disabled steering
   input with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- The dot's fade is driven by an interval the card owns. No headless test can
  reach a React hook here, so its guard is the source contract plus the purity
  of `recency.ts`, which vitest does cover.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- A worktree lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more case
  there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open; R-0364, R-0403, R-0607 through R-0609,
  R-0611, R-0613, R-0618, R-0622, R-0651 and R-0653 through R-0659 stay routed
  to a paydown branch.
