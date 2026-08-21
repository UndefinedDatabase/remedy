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
R35 is the CLOSURE EVIDENCE round. It records the R34 verdict — PASS, the
integration gate green on both sides with 0 branch-only and 0 base-only
failures — writes this feature's Built State into
`docs/roadmap/features/T5_F008.md`, and then produces the two artefacts closure
cannot happen without: the evidence bundle from
`create_manual_completion_bundle` and a FRESH review zip, both at the commit
carrying the Built State.

## Next Steps
1. R36 is the CLOSURE COMMIT round per docs/roadmap/STATUS_closure_protocol.md:
   the authored STATUS `[x]` line, the README capability sync and the
   candidates carrier in ONE commit (R-0154), then the pull request, which is
   NOT merged in its own session.

## Risks
- A failing zip build is a closure BLOCKER, not a retry: the round stops and
  reports the raw error.
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
