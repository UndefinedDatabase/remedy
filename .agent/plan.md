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
R33 records R32, which PASSED, and opens T003 at the only place it can start:
the server. Jump-to-node needs a linkage the envelope has never carried, so this
round lands DECISION F021 D2's single additive field, `task_id`, at
`_safe_event_summary` — the one writer both transports share. It is resolved
from TWO sources, because the run log carries the id at the TOP LEVEL while
`_load_job_plan_events` nests it under `metadata`; reading only the first would
leave jump-to-node dead for exactly the trace-driven jobs. Two corrections are
appended against OPEN findings R-0661 and R-0607, neither minting an id.

## Next Steps
1. R34: the client half of T003 — `feedRow.ts` carries the linkage, and a feed
   row click resolves it to a node id through the task list the dashboard
   already carries and emits `onSelectNode`.
2. R35: the steering input, rendered DISABLED with the tooltip naming F030.
3. Closure: the integration-gate round, the evidence round, then the
   STATUS-commit round.

## Risks
- No DOM environment exists here, so components are gated by `npx tsc --noEmit`
  and by Python source contracts. VITEST DOES NOT TYPECHECK, so `tsc` stays a
  load-bearing gate of every round that touches `apps/`.
- The envelope is a wire format with a byte golden. Any further field is a
  deliberate edit of `GOLDEN_STREAM` and of the key-set pin beside it, and the
  short tail those lines share occurs in three INPUT fixtures too.
- `npm run lint` is RED tree-wide at every commit: the eslint config has no
  TypeScript parser, so it reports a parsing error per file and is blind to
  style. That is R-0622, still open.
- Two tests in `tests/ui_server/test_command_channel.py` were seen to fail once
  under a full-suite worktree run and passed everywhere else. Unregistered on
  one observation; a second sighting mints the id.
- No code defect of F021 is open. R-0364, R-0403, R-0587, R-0607 through
  R-0609, R-0611, R-0613, R-0618, R-0622, R-0629, R-0630, R-0644, R-0651,
  R-0653 through R-0659 and R-0661 stay routed to a paydown branch.
