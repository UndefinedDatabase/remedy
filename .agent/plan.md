# Plan — F008 SSE event stream

Branch: feature/f008-sse-event-stream, cut from `main` at `7c03adfa`, the merge
commit of pull request #208. `.agent/live_review.md` is the source of truth for
the open set, the next free finding id and the round map.

## Goal
A per-job SSE endpoint streaming the event ledger from a cursor — the ledger's
own monotonic seq carried and never renumbered, a 15 s heartbeat, Last-Event-ID
resume replaying exactly the missed span — plus a client hook with reconnect
backoff, gap detection and an honest polling fallback that labels itself
delayed. DONE when a fake job streams into a test client with zero gaps across
forced disconnects, the transcript byte-equals the ledger's envelope sequence,
the heartbeat holds cadence, and the fallback engages on a disabled EventSource
and recovers to live.

## Current Step
R33 records the R32 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — amends R-0629 with the F008 R32 instance, a defect in the
reviewer's own block text, and WIRES THE COCKPIT: `RemedyShell` subscribes to
its dashboard's job with `useBrainStream` over `createBrainStreamHostDeps` and
`browserBrainStreamEnv`, and passes the transport status to `RightLivePanel`,
where the badge R29 built finally reads a real one. T003 is complete when this
round lands.

## Next Steps
1. R34 runs the INTEGRATION GATE per docs/agents/integration_gate.md — the full
   suite, once, before closure — and a regression there is a normal repair
   round.
2. Then the closure round per docs/roadmap/STATUS_closure_protocol.md: evidence
   job, a FRESH review zip, the STATUS line and the pull request.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
  The integration gate is the first run that exercises the wired shell at all.
