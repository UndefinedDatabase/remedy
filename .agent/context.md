# Context — verified repair campaign (operator order exec-1018b, 2026-10-18)

## Active Branch
feature/verified-repair from PR 362's head `cfd906254` (feature/adaptive-reliability, on PR 361's
`652029edc`, on PR 360's `9b172a16c`) in `.remedy-wt/verified-repair`. Merge order: 360, 361, 362,
this. The main checkout stays on main (editable install, supervisor), never switched or pulled.
Open PR gate: three open PRs, merge withheld by the operator, so AGENTS.md "PR Scope Drift
Prevention" option 2 applies (new branch from the tip, separate PR).

## Evidence
- Deterministic walks of the lab repository with a scripted builder and the real `npm test`
  (tests/cli/test_do_verified_repair.py); supervisor HTTP orders in disposable data roots.
- The operator's `.claude/settings.json` denies reading `.data/**`: the live data root is never
  listed or read; diagnoses rest on configuration, code and disposable reproductions.

## Scope
P0: R-1351, review-report export, combined review of 360-362. P1 as far as measured. API handoff.

## Steps
The order's phases; the current one is in plan.md. Outside the roadmap queue: F078 stays next.

## Do not touch
The roadmap queue, `.agent/STOP`, the supervisor and `luna-remedy-serve.service`, the live
checkout and its `.data`, provider defaults, `pi.*` caps, Universe's repositories, other sessions.

## Constraints
- Real model calls only as the order's controlled runs (disposable fixtures, local Ollama, caps).
- One pytest process tree at a time; focused tests per step; one full local gate at the end.
- Commits at most 500 insertions; structure ratchet: listed files and functions do not grow.
