# Plan — operator amendment amend1026-go-live-and-ask

## Goal
The live supervisor on this machine runs current code with claude-cli for Universe's two
clients; the HTTP API gains `GET /api/v1/projects` and the read-only
`POST /api/v1/projects/{project}/ask`; Universe's small asks (push_allowed, the story's scope,
the order's review report) are met; contract 1.30; F318 closed with a real ask (2026-10-26).

## Current Step
Parts B to E on `feature/amend1026-go-live-and-ask`. Part A is done on the machine
(supervisor restarted as the user unit `remedy-serve-live`, port 8450, data root
`~/Repos/remedy/.data`; host_tools for orb-universe and orb-remedy, revoked from luna; order
a5d65e5e50342eec of key luna-twmhd8 cancelled; Remedy's own project has the slug `remedy`).

## Next Steps
1. D1 + D2: `autonomy.push_allowed` in the execution offer; `scope` in both stories.
2. D3: `GET /api/v1/orders/{order}/review` (the captured review report as Markdown).
3. C1: `GET /api/v1/projects` and `remedy client projects`.
4. C2 + C3: the read-only ask (`packages/orchestration/project_ask.py`), its route, its CLI
   twin `remedy client ask` and the tests (only Read, Glob, Grep; the repository unchanged).
5. B: contract 1.30, the API page, CHANGELOG.
6. Merge-ready: one full suite run, review and repair until green; ruff green.
7. E: restart the supervisor on main, the real ask, evidence, F318 in STATUS.md, merge, push,
   handback `~/.remedy-loop/amend1026-go-live-and-ask.handback.md`.

## Risks
- `answer_public_api_post` is a ratchet row (151 lines): every edit there stays line-neutral.
- There is no upload route, so `attachments` is left out (a finding for the handback).
