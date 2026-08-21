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
R32 records the R31 verdict — PASS, every gate re-run by the reviewer out of the
committed blobs — and binds the injected environment to real globals with
`browserBrainStreamEnv`, the last piece between the factory R31 built and a
browser. A runtime with no EventSource yields a null source, which is the
`unsupported` the polling fallback engages on, so the cockpit degrades to
DELAYED instead of claiming a liveness it does not have.

## Next Steps
1. R33 wires the cockpit: `useBrainStream` called in `RemedyShell` over
   `createBrainStreamHostDeps` and `browserBrainStreamEnv`, its status passed
   to `RightLivePanel` as `streamStatus`, gated by a new source contract under
   `tests/ui_contracts/`. DECISION F008 D3 records why the call sits in the
   shell rather than in `RemedyApp`.
2. Then the integration gate before closure.

## Risks
- `npm run lint` in `apps/ui` is RED at base and is NOT a gate (R-0364): that
  config installs no TypeScript parser, which is R-0622 and routes to a
  paydown branch.
- The hook's RENDER behaviour stays unproved until a DOM environment exists:
  its contract gates its source, and the seam beneath it carries the logic.
- `RemedyShell` renders every cockpit surface, so R33's blast radius is the
  widest of any round since R4 even after DECISION F008 D3 narrowed it.
