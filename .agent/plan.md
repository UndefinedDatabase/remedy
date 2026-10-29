# Plan — operator order welt-2 (2026-10-29): Remedy runs on its own

## Goal
decodeux: improvement jobs from remedy-chat must run unattended end to end and stop only with a
plain reason. Six faults of the night 2026-10-28/29 become F320 to F325 (Package 3, Tier 2).

## Current Step
F320 attachments are never deliverables.

## Next Steps
1. F321 low findings never block; config `cycles.repair_rounds` is the default.
2. F322 builder tests in the worktree (PYTHONPATH, Remedy's own test run).
3. F323 waiting jobs follow their order.
4. F324 unattended stays on the job; HTTP `unattended`/`repair_rounds`; interface 1.33.
5. F325 every stop says why (story `stop.text`, order view `stop_text`).
6. Run only the added and changed tests once; ruff on touched files.

## Risks
- Branch welt2/remedycore is merged and pushed by the orchestrator, not by this session.
