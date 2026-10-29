# Plan — operator order welt-2 (2026-10-29): Remedy runs on its own

## Goal
decodeux: improvement jobs from remedy-chat must run unattended end to end and stop only with a
plain reason. Six faults of the night 2026-10-28/29 become F320 to F325 (Package 3, Tier 2).

## Current Step
Done: F320 to F325 built, closing tests green (1027 passed), ruff clean.

## Next Steps
1. The orchestrator merges branch welt2/remedycore and pushes; decodeux installs.

## Risks
- Branch welt2/remedycore is merged and pushed by the orchestrator, not by this session.
