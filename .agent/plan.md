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
R15 builds the ACTION class T5_F021 rules the NowCard over — heartbeats and
bookkeeping excluded — as DATA in `actionClass.ts`, classified by EXCLUSION over
a suffix rule so a kind computed at runtime is never silently demoted. Nothing
renders it yet: R16 wires it, the build-then-wire rhythm R13 and R14 used. It
also records the R14 verdict, which was PASS on every gate.

## Next Steps
1. R16 wires `newestActionRow` into `AgentNowCard` with the recency dot, which
   is the first thing that RENDERS the class R15 built.
2. R17 adds the scroll discipline that never yanks a reader who has scrolled up.
3. R18 gives each row its click-jump to the node, the graph-focus API T003 opens
   with, then T003: the disabled steering input with its honest tooltip.

## Risks
- No DOM environment exists in this repository, so components are gated by
  `npx tsc --noEmit` and by Python source contracts. A contract that reads a
  prop name is the only thing standing between "published" and "rendered".
- A module nothing calls is the R-0220 blind spot. R15 is deliberately headless
  and R16 is the round that makes it load-bearing; if R16 does not happen, this
  plan is where that debt is visible.
- `npx vitest run` and `npx tsc` are BOTH vacuous in a fresh worktree, which has
  no `node_modules` (R-0518), so both run only in the primary checkout, and
  `npx vitest` is DENIED to the reviewer's session class besides.
- Reflog gates name the OPERATION field, never the whole row: this repository's
  commit subjects discuss amends by design (R-0613).
- No code defect of F021 is open; R-0364, R-0403, R-0607, R-0608, R-0609,
  R-0611, R-0613 and R-0622 stay routed to a paydown branch.
