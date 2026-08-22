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
R38 is the INTEGRATION-GATE round, the first of the three that close F021. The
full suite runs at the branch tip and at the merge base in a disposable worktree
per docs/agents/integration_gate.md, and the feature file's Goal & Done is
resolved clause by clause to the path, symbol and test node id that satisfy it.
The round MAY ONLY CONFIRM: it writes no product code, mints no finding id, and
hands back on the first branch-only failure coupled to F021 code or the first
clause nothing on disk satisfies. R37's PASS is recorded at C2.

## Next Steps
1. The evidence round, then the STATUS-commit round
   (docs/roadmap/STATUS_closure_protocol.md; the two are never one round).
2. The pull request, opened at closure and merged only at the Open PR Gate.

## Risks
- A green gate is not an accepted feature. Only the clause-by-clause read can
  show that an acceptance criterion has nothing on disk behind it, and a suite
  that passes says nothing about a criterion no test reaches.
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK.
- Nothing here renders CSS. R-0661's pin proves the unresolved-property SET has
  not grown; it cannot prove any rule's computed value.
- `npm run lint` is RED tree-wide under R-0622, still open.
- No code defect of F021 is open. R-0364, R-0369, R-0402, R-0403, R-0419,
  R-0439, R-0587, R-0607 through R-0609, R-0611, R-0613, R-0618, R-0622,
  R-0629, R-0630, R-0644, R-0651, R-0653 through R-0659 and R-0661 stay routed
  to a paydown branch.
