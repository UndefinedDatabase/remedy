# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 22. C1 books round 21's PASS. C2 lands R-0809's run-id wording:
`apps/cli/commands/do_cmd.py`'s `_cmd_run_show` now prints `Error: No run
matches '<id>'. Try: remedy run list.` instead of `Error: run '<id>' not
found.`; one test file updated to match. R-0809 stays OPEN — of its four
former wordings, "invalid job ID" and "no job matches prefix" (round 20) and
now "run '...' not found" are gone; only "job not found:" (job_stop_cmd.py's
own text at line 69, and project.py's two sites) remains.

## Next Steps

1. R-0809's last remaining wording, "job not found:" — used by
   `job_stop_cmd.py:69` (inside `_unknown_job`, still correct as the ONLY
   print for that failure path) and `project.py`'s two sites (line 160 and
   456) — needs a measurement pass: confirm no test pins the literal
   "job not found:" substring in a way that would need updating in lockstep,
   and confirm unifying it does not collide with `JobNotFoundError`'s own
   exit-code contract, before authoring the fix. Once this lands, R-0809 is
   fully resolved and gets a `Done:` paragraph.
2. R-0805 (`ui status` dead-session pruning) still needs a design pass on
   the session-state model before implementation.
3. R-0895 (README quickstart) runs last (orchestrator brief: it quotes the
   finished catalog).
4. Session 4 continues; continuing is allowed while context comfortably
   suffices (amend0905-throughput's 6-to-8 target).

## Risks

- `packages/orchestration/data_paths.py`'s `JobIdInvalid`/`JobIdNotFound`
  internal exception messages are still pre-unification text (round 20's
  risk note) — unaffected by any round so far.
- Do not write `Done: R-0809` until ALL four former wordings are confirmed
  gone by a fresh repo-wide grep; a partial fix is progress, not resolution.
