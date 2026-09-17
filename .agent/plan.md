# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 20. C1 books round 19's PASS. C2 lands R-0809's job-id slice:
`resolve_job_id`'s shared except block in `packages/orchestration/data_paths.py`
plus the 18 duplicated call sites across `brain.py` (11), `file.py` (1),
`event.py` (1), `memory.py` (1), `snapshot_cmds.py` (2) and `test_cmds.py` (2)
now all print `Error: No job matches '<id>'. Try: remedy job list.`; five test
files updated to match. R-0809 stays OPEN — it names four former wordings
("job not found:", "run '...' not found.", "invalid job ID:", "no job matches
prefix"), and this slice retires only the last two.

## Next Steps

1. R-0809's remaining wordings — "job not found:" (used by `job_stop_cmd.py`,
   `project.py` and others for a well-formed id whose record is missing) and
   "run '...' not found." (a distinct id kind with no resolver measured yet) —
   need their own measurement pass before either is touched; do not assume
   this round's shape or call-site count generalizes.
2. R-0805 (`ui status` dead-session pruning) still needs a design pass on the
   session-state model before implementation.
3. R-0895 (README quickstart) runs last (orchestrator brief: it quotes the
   finished catalog).
4. Session 4 continues; continuing is allowed while context comfortably
   suffices (amend0905-throughput's 6-to-8 target).

## Risks

- `packages/orchestration/data_paths.py`'s `JobIdInvalid`/`JobIdNotFound`
  internal exception messages (the `raise` sites, not the `resolve_job_id`
  print) still say "invalid job ID"/"no job matches prefix" — deliberately
  untouched, because nothing prints `str(exc)` for them any more after this
  round. A future edit that starts printing `str(exc)` for either must update
  those raise-site messages too.
- R-0809's true remaining scope (the "job not found:" and "run" wordings) is
  unmeasured; grep fresh before assuming either has (or needs) a shared
  resolver like `resolve_job_id`/`lookup_job_id`.
