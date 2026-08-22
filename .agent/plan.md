# Plan — F021 Live activity feed + now-card

Branch: feature/f021-live-activity-feed, cut from `main` at `4548995d`, the merge
commit of pull request #210, which the reviewer merged at the Open PR Gate before
this branch was created. `.agent/live_review.md` is the source of truth for the
open set, the round map and the finding-id ceiling.

## Goal
The raw SSE event stream becomes a story a human can follow: a humanization
catalog maps event kinds to plain lines, a NowCard shows the newest ACTION-class
event with a recency dot, and feed rows carry their seq and click-jump to their
node. DONE when the catalog covers the kind set DECISION F021 D3 rules and an
unknown kind renders an honest generic line rather than vanishing, the feed
renders fixture streams per the binding CSS, jump-to-node focuses the right
node, and the steering input renders DISABLED with its tooltip until F030.

## Current Step
R16 wires `newestActionRow` into `AgentNowCard` through the ring the panel
already receives, so the card's detail line becomes the newest ACTION the stream
produced and falls back to the dashboard's own text when there is none. That
retires the orphan R15 left deliberately. It also records the R15 verdict, which
was PASS on every gate, and registers R-0651.

## Next Steps
1. R17 adds the scroll discipline that never yanks a reader who has scrolled up.
2. R18 adds the recency dot over a PURE time function, so the fade to idle after
   the quiet window is testable without a clock.
3. R19 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts. A contract that reads a
  prop name is the only thing standing between "published" and "rendered".
- Vitest IS reviewer-runnable as `npm run test:unit` from `apps/ui`; only the
  bare `npx vitest` spelling is denied (R-0651). Gate it that way and re-run it
  at review. It stays vacuous in a fresh worktree, which has no `node_modules`
  (R-0518), unless that directory is symlinked in.
- Reflog gates name the OPERATION field, never the whole row, and marker sweeps
  are LINE-ANCHORED, never containment (R-0613, R-0364).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613, R-0622 and R-0651 stay routed to a paydown branch.
