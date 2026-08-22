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
R23 puts the arrival stamp on the TRANSPORT EVENT: the host reads the clock R22
injected, once per frame, and `BrainStreamEvent`'s frame member carries the
number. The driver stays a pure reducer that transports it without asking the
time. Nothing renders yet.

## Next Steps
1. R24: the ring's row carries the stamp — `FeedRow` gains `receivedAtMs`,
   `feedRowOf` takes it and `receiveBrainFrame` threads it. First round to touch
   the ring, whose append placement DECISION F021 D5 governs.
2. R25: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
3. R26: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R27, the row click-jump, and T003's
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
- A block states pair shapes it MEASURED for its own pairs and never carries the
  previous round's reading over: R22's twelve were all APPEND, R23's six are all
  REWRITE (R-0656 and R-0657 are the cost of the reviewer's own drift here).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653, R-0654, R-0655, R-0656 and R-0657 stay
  routed to a paydown branch.
