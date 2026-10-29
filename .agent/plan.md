# Plan — operator order welt-2 (2026-10-29): Remedy runs on its own

## Goal
decodeux: improvement jobs from remedy-chat must run unattended end to end and stop only with a
plain reason. Six faults of the night 2026-10-28/29 become F320 to F325 (Package 3, Tier 2).

## Current Step
Run only the added and changed tests once; ruff on touched files; fix and run again.

## Next Steps
1. Hand the commit hashes of contract 1.33 to the orchestrator.

## Risks
- Branch welt2/remedycore is merged and pushed by the orchestrator, not by this session.
