# Plan — F305 Multi-repo missions: the cockpit's chain band

## Goal
The cockpit shows a project's missions as cards; opening one loads its orders, each with the calls
and tokens of its jobs and a chain band of chips, one per job of the order in every repository it
reached; a click on a chip opens that project's cockpit on that job
(docs/roadmap/features/T13_F305.md; DECISIONS F305 D1 to D3; R-1248).

## Current Step
Round 3 on `feature/f305-multi-repo-chain-band`, session 1, T003 and the closure's first round:
book round 2; the browser proof `tests/ui_server/test_mission_chain_live.py` and the user guide
`docs/guides/missions-panel-user-guide-v1.md` with its two index rows; the checklist's
consolidation pass; the closure's self-use item run to its approval gate; `apps/ui` built and the
feature's one full suite with its cost reading.

## Next Steps
1. The evidence round: book round 3, the resolution of R-1248 and every self-use run defect, the
   staging reclaim, the evidence job and the review package.
2. The closing round: the Built State, the ledger's rotation, the STATUS line with the README sync
   and the self-use queue's `consumed_by`, and the pull request.

## Risks
- `_RemedyHandler.do_GET`, `packages/orchestration/ui_server.py` and
  `apps/ui/src/api/remedyApi.ts` are rows of the structure ledger and may not grow.
- A cost in US dollars is never shown to the operator (DECISION amend1007b D7).
- A red closure suite is repaired under amend0917-throughput rule 2, at most three rounds.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).
