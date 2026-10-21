# Plan — F060 Long-run certificate

## Goal
A finished job can prove itself to someone who was not there: `remedy job certificate <id>` packs
its report, token truth, verdicts, ownership, run manifest and a hash manifest with claims into one
small bundle, and `remedy verify <bundle>` checks every member and every claim on any machine, with
the failing member named (docs/roadmap/features/T3_F060.md; DECISIONs F060 D1 to D3).

## Current Step
Round 3 (session 1): book round 2, resolve R-1404 and register R-1405, record DECISION F060 D3,
and land T002: the shared claim derivations, the verifier with its claim cross-checks and verdict,
and one tamper fixture per member class.

## Next Steps
1. Round 4 (T003): `remedy job certificate`, `remedy verify`, the standalone check in a fresh
   folder, and the page that says a certificate is not a signature.
2. The closure sequence.

## Risks
- The integrity check fails on High findings F060 does not own (DECISION F310 D7, Q20).
- `commands/job.py` and `command_catalog.py` are on the structure ledger; round 4's commands go
  into new modules.
