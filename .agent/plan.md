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
R30 records R29, which PASSED, and corrects the two defects it surfaced. Both
are the reviewer's and neither mints an id: a ledger count gate anchored on the
loose `- R-` prefix rather than on the registration pattern goes to R-0630, and
a correction paragraph that wore the registration shape — plus an append
convention that landed two blank lines into `.agent/decisions.md` — goes to
R-0587. The corrections are appended and name the landed text.

## Next Steps
1. R31: `feedScroll.ts` into the feed's scroll container with the new-rows pill
   component_spec.md line 86 binds. Headless since R17 and the last rule this
   feature has built and left unread.
2. R32: the row click-jump to the graph store, then T003's disabled steering
   input with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- The dot's fade is driven by an interval the card owns. No headless test can
  reach a React hook here, so its guard is the source contract plus the purity
  of `recency.ts`, which vitest does cover.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- This ledger now carries two `- R-0618` lines under a LOOSE `- R-` reading and
  one under the canonical `^- R-\d+ — ` pattern. The canonical reading is the
  open set; C2 of this round says so on disk.
- No code defect of F021 is open; R-0364, R-0403, R-0587, R-0607 through R-0609,
  R-0611, R-0613, R-0618, R-0622, R-0630, R-0651 and R-0653 through R-0659 stay
  routed to a paydown branch.
