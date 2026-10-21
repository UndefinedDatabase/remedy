# Plan — F060 Long-run certificate

## Goal
A finished job can prove itself to someone who was not there: `remedy job certificate <id>` packs
its report, token truth, verdicts, ownership, run manifest and a hash manifest with claims into one
small bundle, and `remedy verify <bundle>` checks every member and every claim on any machine, with
the failing member named (docs/roadmap/features/T3_F060.md; DECISIONs F060 D1 to D4).

## Current Step
Round 4 (session 1): book round 3 and resolve R-1405, record DECISION F060 D4, and land T003:
`remedy job certificate` and `remedy verify`, their tests, the standalone check in a fresh folder
with no data folder, and the page `docs/system/job-certificate-v1.md`.

## Next Steps
1. The closure sequence (`docs/roadmap/STATUS_closure_protocol.md`): the one full suite, the
   evidence package, the Built State and the STATUS flip, the pull request left unmerged.

## Risks
- The integrity check fails on High findings F060 does not own (DECISION F310 D7, Q20).
- `command_catalog.py` is on the structure ledger; its edit must stay line-neutral.
