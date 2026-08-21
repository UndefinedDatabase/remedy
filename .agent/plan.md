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
R34 records the R33 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — retires the stale claim in `LiveStatusPill.tsx` that R33's own
change set could not reach, and RUNS THE INTEGRATION GATE per
docs/agents/integration_gate.md: the full suite once on this branch and once at
the merge base `7c03adfa`, compared, with every branch-only and every base-only
id attributed by direct evidence.

## Next Steps
1. R35 is the closure round per docs/roadmap/STATUS_closure_protocol.md:
   evidence job, a FRESH review zip, the authored STATUS line and the pull
   request — unless the gate names a blocker, which is its own repair round.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The base worktree's copied `apps/ui/dist` looks STALE by mtime to
  `_frontend_is_stale`, which is what produced nine base-only failures at the
  F255 R18 gate. This round repairs the mtime before the base run and reports
  both readings, so a base-only failure is evidence rather than furniture.
