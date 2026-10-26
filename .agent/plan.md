# Plan — operator amendment amend1026-go-live-and-ask

## Goal
The live supervisor on this machine runs current code with claude-cli for Universe's two
clients; the HTTP API gains `GET /api/v1/projects` and the read-only
`POST /api/v1/projects/{project}/ask`; Universe's small asks (push_allowed, the story's scope,
the order's review report) are met; contract 1.30; F318 closed with a real ask (2026-10-26).

## Current Step
Parts A to E are done on `feature/amend1026-go-live-and-ask`: F318 is accepted with the real ask
(`evidence/current/amend1026_ask/`). The closing step: the last full suite on the final tree, the
merge into `main`, the push, the supervisor restarted on main and the handback
`~/.remedy-loop/amend1026-go-live-and-ask.handback.md`.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then Rule A5, which reads F316 (findings
   paydown v11) as the next line.

## Risks
- `answer_public_api_post` is a ratchet row (151 lines): every edit there stays line-neutral.
- There is no upload route, so `attachments` is left out (a finding for the handback).
