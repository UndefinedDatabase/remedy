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
R27 records R26, which PASSED all twelve gates, and repairs the one defect that
round surfaced: the reviewer's own FEEDTESTSHIM slice inserted a function
BETWEEN two import statements in `feedRow.test.ts`, which compiles and tests
green but leaves an import stranded below a definition. Registered as R-0660 and
fixed in the same round, because the repair is a move and nothing depends on it.

## Next Steps
1. R28: the NowCard's recency dot — `recency.ts` drives BOTH the badge and the
   dot, with the CSS `docs/ui/design_reference/assets_spec.md` governs. This is
   the first round able to subtract two instants on ONE clock, which is what
   R22 through R26 built.
2. R29: `feedScroll.ts` drives the feed's scroll container and the new-rows pill
   component_spec.md line 86 binds; then R30, the row click-jump, and T003's
   disabled steering input.
3. Closure: the evidence round, then the STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round in this chain.
- VITEST IS MUTATION-PROVABLE since DECISION F021 D8: symlink
  `apps/ui/node_modules` into a disposable worktree and both `npx tsc --noEmit`
  and `npm run test:unit` run there, so a red control satisfies guardrail G5.
- `npm run lint` is RED across the whole tree at every commit, this branch's
  included: the eslint config has no TypeScript parser, so it reports a parsing
  error per file and is blind to style. That is R-0622, still open, and it is
  why no lint gate can catch a defect of the R-0660 shape.
- A worktree lacks `apps/ui/dist/`, so `tests/ui_contracts/` skips one more case
  there than in the primary checkout. COUNT BY PASSED PLUS SKIPPED.
- No code defect of F021 is open once R-0660 closes; R-0364, R-0403, R-0607,
  R-0608, R-0609, R-0611, R-0613, R-0622, R-0651, R-0653 through R-0659 stay
  routed to a paydown branch.
