# Plan — F305 Multi-repo missions: the cockpit's chain band

## Goal
The cockpit shows a project's missions as cards; opening one loads its orders, each with the calls
and tokens of its jobs and a chain band of chips, one per job of the order in every repository it
reached; a click on a chip opens that project's cockpit on that job
(docs/roadmap/features/T13_F305.md; DECISIONS F305 D1 to D3; R-1248).

## Current Step
Round 5 on `feature/f305-multi-repo-chain-band`, session 1, the closing round: book round 4, the
Built State, the ledger's rotation, F305 accepted in STATUS with the README sync and the self-use
entry `SU-057`'s `consumed_by`, and the pull request, left unmerged.

## Next Steps
1. The next session: Phase 1 rule 1 (`.agent/STOP`), then the Open PR Gate merges F305's pull
   request, then the next feature's first commit books round 5's verdict.
2. Rule A5: the next unchecked line in `docs/roadmap/STATUS.md`.

## Risks
- R-1235, R-1246, R-1251 and R-1252 are owned by F306.
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci); the local evidence in
  the pull request's body is the record.
