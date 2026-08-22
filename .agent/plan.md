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
R32 records R31, which PASSED, and pays for the one live defect it shipped: the
jump-to-live pill asked for `--remedy-radius-pill`, which the design reference
has always defined and the shipped stylesheet never adopted, so the property
resolved to nothing and the pill rendered square. This round defines the token,
pins the unresolved-custom-property set so it can never grow silently, and
registers the class as R-0661 — four OTHER properties were already unresolved
before F021 began. R31's two text defects are appended as corrections naming
open findings R-0629 and R-0587; neither mints an id.

## Next Steps
1. R33: T003 — the row click-jump to the graph store, then the disabled
   steering input with the tooltip naming F030.
2. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- Nothing in this repository renders CSS, so a custom property that resolves to
  nothing is invisible to every suite. R-0661's pin closes that for the SET but
  still cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- This ledger carries two `- R-0618` lines under a LOOSE `- R-` reading and one
  under the canonical `^- R-\d+ — ` pattern. The canonical reading is the open
  set; R30's C2 says so on disk.
- No code defect of F021 is open once R-0661's own use is fixed; R-0364,
  R-0403, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661's four
  surviving properties stay routed to a paydown branch.
