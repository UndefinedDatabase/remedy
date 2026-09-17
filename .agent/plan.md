# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 23. C1 books round 22's PASS. C2 lands R-0809's "job not found" family
across TEN sites in SEVEN files: `packages/orchestration/pingpong_job.py`'s
`JobNotFoundError` message (the single source `print(f"Error: {exc}")`
reaches at 34 call sites across `brain.py`, `change.py`, `decision.py`,
`event.py`, `file.py`, `job.py` and `patch.py` — none edited directly, all
fixed by this one change), plus five sites with their OWN hardcoded text
(`test_cmds.py`, `snapshot_cmds.py` x2, `job.py` x2) and four more with a
THIRD kind of hardcoded text (`project.py` x2, `job_context_cmd.py`,
`job_stop_cmd.py`). Three test files updated to match. R-0809 stays OPEN —
only the "mission" wording (`apps/cli/commands/mission_cmd.py`'s
`_load_mission_or_exit`, `Error: no mission {id} in this project.`) remains;
once it lands, R-0809 gets its `Done:` paragraph.

## Next Steps

1. R-0809's LAST remaining piece: `mission_cmd.py`'s `_load_mission_or_exit`
   prints `Error: no mission {mission_id} in this project.` plus a separate
   hint line `List them with: remedy mission list` — unify to `Error: No
   mission matches '<id>'. Try: remedy mission list.` (one line, matching
   job/run's shape), find every caller of `_load_mission_or_exit` and every
   test asserting the current two-line wording before touching it. Once this
   lands, write `Done: R-0809` — confirmed by a fresh repo-wide grep that
   all four original wordings ("job not found", "run '...' not found",
   "invalid job ID", "no job matches prefix") plus the mission one are gone.
2. R-0805 (`ui status` dead-session pruning) still needs a design pass on
   the session-state model before implementation.
3. R-0895 (README quickstart) runs last (orchestrator brief: it quotes the
   finished catalog).
4. Session 4 continues; continuing is allowed while context comfortably
   suffices (amend0905-throughput's 6-to-8 target).

## Risks

- `packages/orchestration/data_paths.py`'s `JobIdInvalid`/`JobIdNotFound`
  internal exception messages are still pre-unification text (round 20's
  risk note) — unaffected by any round so far, and unrelated to
  `JobNotFoundError` (a different exception class entirely).
- Do not write `Done: R-0809` until the mission wording also lands and a
  fresh repo-wide grep confirms all five original wordings are gone.
