# Plan — F305 Multi-repo missions: the cockpit's chain band

## Goal
The cockpit shows a project's missions as cards; opening one loads its orders, each with the calls
and tokens of its jobs and a chain band of chips, one per job of the order in every repository it
reached; a click on a chip opens that project's cockpit on that job
(docs/roadmap/features/T13_F305.md; DECISIONS F305 D1 to D3; R-1248).

## Current Step
Round 4 on `feature/f305-multi-repo-chain-band`, session 1, the closure's evidence round: book
round 3, the recurrence of R-1252 the self-use run named and the resolution of R-1248; save the
block and the evidence script; the staging reclaim, the evidence job on the accepted head and the
review package.

## Next Steps
1. The closing round: the Built State, the ledger's rotation, the STATUS line with the README sync
   and the self-use entry `SU-057`'s `consumed_by`, and the pull request, left unmerged.

## Risks
- A failing review package is a closure blocker: fix it, or the feature goes `[!]`.
- A cost in US dollars is never shown to the operator (DECISION amend1007b D7).
- Hosted CI runs only when dispatched by hand (amend1011-manual-hosted-ci).
