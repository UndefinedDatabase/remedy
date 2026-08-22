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
R22 gives the transport an INJECTED CLOCK. DECISION F021 D6 replaced the single
wiring round with four, because `recencyLevel` takes two NUMBERS and this client
holds no numeric instant: a row's `timestamp` is a server-clock string that
`ui_server.py` passes through unparsed. R22 adds `now()` to the environment, the
deps and the host contract; nothing consumes it yet.

## Next Steps
1. R23: the frame event carries `receivedAtMs`, stamped by the host from that
   clock — `brainStreamDriver.ts` and `brainStreamHost.ts` with their tests.
2. R24: the ring's row carries the stamp — `feedRow.ts` and `brainStream.ts`.
3. R25: the NowCard reads `recency.ts` for BOTH its badge and its new dot, with
   the CSS `docs/ui/design_reference/assets_spec.md` governs.
4. R26: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R27, the row click-jump, and T003's
   disabled steering input.
5. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK: R22's dry run was
  green under vitest while `tsc` was red on a deps literal it had missed, so
  `tsc` is the load-bearing gate of every round in this chain.
- Vitest is reviewer-runnable as `npm run test:unit` (R-0651) but only GREEN: a
  worktree has no `node_modules` (R-0518), so no vitest case has been
  mutation-proved. The Python contract is the mutation-proved guard (R-0653).
- A worktree also lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more
  case there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622, R-0651, R-0653, R-0654 and R-0655 stay routed to a
  paydown branch.
