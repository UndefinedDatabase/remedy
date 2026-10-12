# Plan — F305 Multi-repo missions: the cockpit's chain band

## Goal
The cockpit shows a project's missions as cards; opening one loads its orders, each with the calls
and tokens of its jobs and a chain band of chips, one per job of the order in every repository it
reached; a click on a chip opens that project's cockpit on that job
(docs/roadmap/features/T13_F305.md; DECISIONS F305 D1 and D2; R-1248).

## Current Step
Round 1 on `feature/f305-multi-repo-chain-band`, session 1: claim F305, re-head the ledger, book
F297's round 14, DECISIONS F305 D1 and D2 with the feature file's amendment; the structural step
that hands every route below a project to `packages/orchestration/cockpit_project_routes.py`;
T001, the server's view in `packages/orchestration/mission_cockpit.py` with its two routes, its
tests and the cockpit page's section.

## Next Steps
1. T002: the client's door for the two routes and the mission card with its chain band of chips
   and the per-order calls and tokens in the cockpit, with their unit and contract tests; this
   resolves R-1248.
2. T003: the headless-browser proof over a fixture order of three jobs in two repositories, and a
   click on the second project's chip opening that project's cockpit on that job.
3. The closure sequence.

## Risks
- `_RemedyHandler.do_GET`, `packages/orchestration/ui_server.py` and
  `apps/ui/src/api/remedyApi.ts` are rows of the structure ledger: a project's routes grow in
  `cockpit_project_routes.py`, and the client's door is a module of its own.
- A cost in US dollars is never shown to the operator (DECISION amend1007b D7); the card shows
  calls and tokens.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).
