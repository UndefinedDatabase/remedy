# Plan — operator amendment amend1026-go-live-and-ask

## Goal
The live supervisor on this machine runs current code with claude-cli for Universe's two
clients; the HTTP API gains `GET /api/v1/projects` and the read-only
`POST /api/v1/projects/{project}/ask`; Universe's small asks (push_allowed, the story's scope,
the order's review report) are met; contract 1.30; F318 closed with a real ask (2026-10-26).

## Current Step
Parts B, C and D are built and committed on `feature/amend1026-go-live-and-ask`; the full suite
runs. Part A is done on the machine (supervisor as the user unit `remedy-serve-live`, port 8450,
data root `~/Repos/remedy/.data`; host_tools for orb-universe and orb-remedy, revoked from luna;
order a5d65e5e50342eec of key luna-twmhd8 cancelled; Remedy's own project is the slug `remedy`).

## Next Steps
1. The full suite green (review and repair until it is), ruff green.
2. Merge into `main`, restart the supervisor on main's code, the real ask (E1) and its evidence
   under `evidence/current/amend1026_ask/`, F318 in STATUS.md (E2), push.
3. The handback `~/.remedy-loop/amend1026-go-live-and-ask.handback.md`.

## Risks
- `answer_public_api_post` is a ratchet row (151 lines): every edit there stays line-neutral.
- There is no upload route, so `attachments` is left out (a finding for the handback).
