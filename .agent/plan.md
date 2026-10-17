# Plan — execution quality, honest verification, review reports, execution API (operator order 2026-10-17)

## Goal
The 2026-10-17 README order (job 84b0cc4272164bb2, order a6a87e65809f6bd6) runs as one bounded job and
one task, runs the requested tests or says it could not, reports actual Pi usage, and can leave a review
report the review ZIP packages automatically. No new orchestrator; `.agent/STOP` kept; no real model call,
no supervisor restart, no deploy; outside the roadmap queue (F078 untouched). Work happens in worktree .remedy-wt/exec-quality (the supervisor runs
the main checkout's code).

## Current Step
7. One full local gate on the final commit; PR; German handback with the Universe API handoff.

Done: 1 routing, 2 verification, 3 Pi loop limits, 4 review reports + ZIP, 5 execution API and
HTTP provider rule, 6 experience audit (no code), 7 acceptance matrix (scale matrix v2).

## Next Steps
- Operator: approve or skip one real Pi/Ollama run of the incident order with capture_review.
- Merge only on the operator's word (the supervisor runs main).

## Risks
- `order_scope` is a pattern floor: new vocabulary can still send an order to the full lane (no classifier).
- Pi exposes no turn limit; Remedy's cap ends the process from outside, so a capped call loses its last turn.
