# Plan — F287 Provider session continuity across relaunch

## Goal
A relaunch of a task that a pause or a stop interrupted resumes, on the `claude-cli` provider, the
builder and reviewer sessions the task last used, so finished work is not paid for twice; every
other production provider records that it did not resume (docs/roadmap/features/T3_F287.md).
DECISION F287 D1 fixes the slices and their order.

## Current Step
Round 7, T003 (DECISION F287 D7): a relaunch that offers a parked session to a provider that
cannot resume names the role and the reason in the run record under `resume_declined`;
`ClaudeProvider` and `OllamaPingPongProvider` state why; `docs/system/session-resume-v1.md` names
which providers resume and the copy-mode limit.

## Next Steps
1. The amend0930b-slow-cap hardening stage (SLOW MODE): an acceptance audit of the feature file by
   a fresh worker, then a repair round for every gap it finds, at most three.
2. The closure sequence (docs/roadmap/STATUS_closure_protocol.md).

## Risks
- Repair rounds on `claude-cli` now send shortened prompts to a continued session (F106, F109,
  DECISION F287 D6); the closure's self-use run is the first real observation.
- R-1162 (Low, F297): a `claude-cli` job with no model configured cannot finish a stop.
- R-1160 (Medium) and R-1138, R-1139, R-1143, R-1149, R-1156, R-1157, R-1158 (Low) stay open,
  owned by F297.
