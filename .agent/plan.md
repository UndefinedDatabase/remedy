# Plan — F060 Long-run certificate

## Goal
A finished job can prove itself to someone who was not there: `remedy job certificate <id>` packs
its report, token truth, verdicts, ownership, run manifest and a hash manifest with claims into one
small bundle, and `remedy verify <bundle>` checks every member and every claim on any machine, with
the failing member named (docs/roadmap/features/T3_F060.md; DECISION F060 D1).

## Current Step
Round 1 (session 1): claim F060, book F141's round 11, record the inventory and DECISION F060 D1,
and land T001: the certificate profile in `packages/orchestration/job_certificate.py`, its
manifest, its byte budget that references large members, and goldens.

## Next Steps
1. Round 2: a finished job's sources and claims, the issue counter and `certificate.max_bytes`.
2. Round 3 (T002): the verifier, its claim cross-checks and one tamper fixture per member class.
3. Round 4 (T003): `remedy job certificate`, `remedy verify`, the standalone check in a fresh
   folder, and the page that says a certificate is not a signature.
4. The closure sequence.

## Risks
- The integrity check fails on High findings F060 does not own (DECISION F310 D7, Q20).
- `commands/job.py` and `command_catalog.py` are on the structure ledger; round 4's commands go
  into new modules.
