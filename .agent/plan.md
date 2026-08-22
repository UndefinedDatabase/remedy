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
R39 records R38's PASS and registers what the integration gate and the
acceptance read turned up. THE GATE IS GREEN: the branch-only failure set is
empty against the merge base `4548995d` and no acceptance clause is UNSATISFIED.
Four ids are minted — R-0662, R-0663, R-0664 and R-0665 — and three further
candidates are not, because R-0445, R-0444 and R-0645 already describe them.
The round writes no product code.

## Next Steps
1. The evidence round: the closure bundle and a fresh review zip, per
   docs/roadmap/STATUS_closure_protocol.md.
2. The STATUS-commit round; the two are never one round.
3. The pull request, opened at closure and merged only at the Open PR Gate.

## Risks
- R-0663 is an ACCEPTANCE deviation rather than a process one: the closure round
  must either rule the CSS-module realization sufficient for "per the binding
  CSS" or order the one-line repair in its own reviewer-gated round.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK.
- Nothing here renders CSS. R-0661's pin proves the unresolved-property SET has
  not grown; it cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide under R-0622, still open.
- No code defect of F021 blocks the gate. R-0364, R-0369, R-0402, R-0403,
  R-0419, R-0439, R-0444, R-0445, R-0587, R-0607 through R-0609, R-0611,
  R-0613, R-0618, R-0622, R-0629, R-0630, R-0644, R-0645, R-0651, R-0653
  through R-0659, R-0661, R-0662, R-0664 and R-0665 stay routed to a paydown
  branch.
