# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order.

## Current Step
Round 6, T002 (DECISION F287 D5): tests only. `run_job` on `claude-cli`, with a stand-in that keeps
sessions per directory as the CLI does: a paused and a stopped job relaunched in their worktree
resume the parked session; a paused copy-mode job falls back once and completes. Register R-1162.

## Next Steps
1. T003 — `ClaudeProvider` and `OllamaPingPongProvider` record in the run's evidence that an
   offered session was not resumed and why; the operator guide names which providers resume and
   the copy-mode limit (D5 (4)).
2. The amend0930b-slow-cap hardening stage (SLOW MODE), then closure.

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109);
  the closure's self-use run is the first real observation (Q8).
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
