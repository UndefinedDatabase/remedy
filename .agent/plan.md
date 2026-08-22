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
R26 is THE RING ROUND. `FeedRow` gains `receivedAtMs`, `feedRowOf` takes it as a
required parameter, `receiveBrainFrame` threads it, and the driver hands over the
stamp R23 put on the transport event. Every caller moves in the same commit,
because a signature change that leaves one behind is a red typecheck. The
arrival instant now reaches the ring, which is what the recency dot subtracts.

## Next Steps
1. R27: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs. The dot's two
   operands are now on ONE clock, which is what R22 through R26 existed to do.
2. R28: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R29, the row click-jump, and T003's
   disabled steering input.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- VITEST IS NOW MUTATION-PROVABLE (DECISION F021 D8, R26): symlinking
  `apps/ui/node_modules` into a disposable worktree makes both `npx tsc --noEmit`
  and `npm run test:unit` run there, so a red control no longer needs the primary
  checkout and guardrail G5 is satisfied. R-0518 stays OPEN — a worktree still
  has no `node_modules` of its own — but it no longer blocks a vitest red proof.
- A worktree also lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more
  case there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- R-0654 through R-0659 are ALL defects in the reviewer's own block text or
  record rather than in any worker's execution. R-0656's rule is now §3 checklist
  item 32, so the next block reads it from the checklist.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653 through R-0659 stay routed to a
  paydown branch.
