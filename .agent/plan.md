# Plan — F305 Multi-repo missions: the cockpit's chain band

## Goal
The cockpit shows a project's missions as cards; opening one loads its orders, each with the calls
and tokens of its jobs and a chain band of chips, one per job of the order in every repository it
reached; a click on a chip opens that project's cockpit on that job
(docs/roadmap/features/T13_F305.md; DECISIONS F305 D1 to D3; R-1248).

## Current Step
Round 2 on `feature/f305-multi-repo-chain-band`, session 1: book round 1, DECISION F305 D3; T002,
the client's seam `apps/ui/src/api/missionCard.ts` and door `apps/ui/src/api/missionCardDoor.ts`
with their vitest files; the missions panel `apps/ui/src/components/missions/MissionPanel.tsx`,
its button in the right panel, its mount in the shell and `openJob` in the project context, with
`tests/ui_contracts/test_mission_card_door.py` and the cockpit page's paragraph.

## Next Steps
1. T003: the headless-browser proof over a fixture order of three jobs in two repositories — the
   panel shows three chips naming two projects, and a click on the second project's chip opens
   that project's cockpit on that job — and the user-facing page; this resolves R-1248.
2. The closure sequence.

## Risks
- `_RemedyHandler.do_GET`, `packages/orchestration/ui_server.py` and
  `apps/ui/src/api/remedyApi.ts` are rows of the structure ledger: a project's routes grow in
  `cockpit_project_routes.py`, and the client's doors live in `missionCardDoor.ts`.
- A cost in US dollars is never shown to the operator (DECISION amend1007b D7); the card shows
  calls and tokens.
- A selection that starts a live UI server after `apps/ui/src` changed needs `apps/ui` built
  first, or the server rebuilds `dist` inside a test's timing window.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).
