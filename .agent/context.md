# Context

## Active Branch
feature/steps-247-252-data-honest-contract

## Scope
Steps 351-358: Event-ledger replay, safe checkpoints, checkpoint resume v1.

## Completed
- Layout regression guard: 5 tests prevent 5th main-column row
- Event replay model: JobReplayState from events (safe metadata only)
- Checkpoint detection: JobCheckpoint with safe_to_resume, resume_mode, next_command
- CLI: event replay, job checkpoints, job resume (with --dry-run)
- Resume dry-run: preview without mutation
- Safe resume v1: conservative from_approval mode
- Dashboard resume section: replay_available, latest_checkpoint, can_resume
- UI ResumeCard: shows checkpoint kind, next command (copy-to-clipboard)
- Catalog entries: event.replay, job.checkpoints, job.resume

## Constraints
- UI remains read-only
- Resume only from explicit safe checkpoints
- No arbitrary event resume
- No browser resume button
- source_apply requires permission + approved intent
- No shell=True, no 0.0.0.0

## Remaining Risks
- Resume modes still conservative (only from_approval fully wired)
- Background worker not implemented
- Replay depends on event quality/completeness
- No pixel-perfect visual regression

## Recommended Next Block
Steps 359-366 — Builder Prompt Quality And Real-Ollama Hardening
Or if replay reveals UI gaps:
Steps 359-366 — Replay UI Polish And Graph Filtering
