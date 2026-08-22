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
R31 wires `feedScroll.ts` into the live feed's scroll container — the rule this
feature built at R17 and has left unread since — with the "jump to live"
affordance the feature file binds, the 52vh scroll box its binding CSS fixes,
and contract pins plus a red control, because no DOM test here can reach a
React hook. The same round records R30, which PASSED, and appends the one
correction it owes: a count RECORD30 stated about `.agent/decisions.md` was
hand-read and is wrong by one in both numerals, which is open finding R-0644's
standing rule failing while its SHA clause was obeyed. No id is minted.

## Next Steps
1. R32: T003 — the row click-jump to the graph store, then the disabled
   steering input with the tooltip naming F030.
2. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- The scroll wiring is a React effect over a ref. Nothing here can execute it,
  so its guard is the source contract plus the purity of `feedScroll.ts`, which
  vitest does cover, plus a red control that deletes the follow branch.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- This ledger carries two `- R-0618` lines under a LOOSE `- R-` reading and one
  under the canonical `^- R-\d+ — ` pattern. The canonical reading is the open
  set; R30's C2 says so on disk.
- No code defect of F021 is open; R-0364, R-0403, R-0587, R-0607 through R-0609,
  R-0611, R-0613, R-0618, R-0622, R-0630, R-0644, R-0651 and R-0653 through
  R-0659 stay routed to a paydown branch.
