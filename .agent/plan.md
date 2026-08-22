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
R25 discharges what the record owes before any new code, per DECISION F021 D7.
It promotes R-0656's rule into docs/agents/planner_reviewer_prompt.md §3 as
checklist item 32, records R24's verdict, and repairs a gap R19's halt left: R18
PASSED and its verdict was authored in full, but R19 stopped before the commit
that would have applied it. NO CODE CHANGES.

## Next Steps
1. R26 is THE RING ROUND, moved from R25 by DECISION F021 D7: `FeedRow` gains
   `receivedAtMs`, `feedRowOf` takes it, and `receiveBrainFrame` threads it from
   the transport event. First round to touch the ring, whose append placement
   DECISION F021 D5 governs.
2. R27: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
3. R28: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R29, the row click-jump, and T003's
   disabled steering input.
4. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` is the
  load-bearing gate of every round in this chain.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A worktree also lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more
  case there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- R-0654 through R-0659 are ALL defects in the reviewer's own block text or
  record rather than in any worker's execution, and R-0656 recurred one round
  after it was registered. That is why R25 promotes it to the checklist.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653 through R-0659 stay routed to a
  paydown branch.
