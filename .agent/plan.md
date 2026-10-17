# Plan — execution quality, honest verification, review reports, execution API (operator order 2026-10-17)

## Goal
The 2026-10-17 README order (job 84b0cc4272164bb2, order a6a87e65809f6bd6) runs as one bounded job and
one task, runs the requested tests or says it could not, reports actual Pi usage, and can leave a review
report the review ZIP packages automatically. No new orchestrator; `.agent/STOP` kept; no real model call,
no supervisor restart, no deploy; outside the roadmap queue (F078 untouched). Work happens in worktree .remedy-wt/exec-quality (the supervisor runs
the main checkout's code).

## Current Step
4. Review reports (Phase 4): `--capture-review` / `capture_review` / order header `capture-review: true`;
   reports under `<data root>/review_reports/`; `make_review_zip.sh` packages the latest 10 with an index.

Done: 1 routing (97128b81a), 2 verification (1bcff59dc, f7e0f4749), 3 Pi loop limits and measured usage.

## Next Steps
5. Execution API (Phase 5): `execution` key of `/api/v1/interface`; HTTP refuses providers that run
   outside the tool sandbox (claude-cli, claude); effective config in the `do` answer.
6. Experience audit (Phase 6): measure what earlier evidence reaches a new job; no memory rewrite.
7. Acceptance matrix, docs, one full local gate, PR; German handback with the Universe API handoff.

## Risks
- `order_scope` is a pattern floor: new vocabulary can still send an order to the full lane (no classifier).
- Pi exposes no turn limit; Remedy's cap ends the process from outside, so a capped call loses its last turn.
