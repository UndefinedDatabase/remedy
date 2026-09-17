# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 21. C1 books round 20's PASS and registers/resolves R-0958 (a LOW
pre-existing defect found while researching R-0809's remaining scope:
`remedy job stop` on an unknown id printed TWO contradictory error lines for
one failure). C2 fixes it in `apps/cli/commands/job_stop_cmd.py`. R-0809
stays OPEN and its scope is UNCHANGED by this fix — it removes a duplicate
print of an already-superseded wording, not the "job not found:"/"run '...'
not found." wordings R-0809 still names.

## Next Steps

1. R-0809's remaining wordings ("job not found:" in `job_stop_cmd.py` and
   `project.py`; "run '...' not found." in `do_cmd.py`) still need their own
   measurement pass: is there a shared run-id resolver anywhere, and does
   unifying "job not found" risk the `EXIT_UNKNOWN_JOB`/`JobNotFoundError`
   exit-code contracts several call sites rely on — measure before assuming
   this round's job-id shape generalizes.
2. R-0805 (`ui status` dead-session pruning) still needs a design pass on
   the session-state model before implementation.
3. R-0895 (README quickstart) runs last (orchestrator brief: it quotes the
   finished catalog).
4. Session 4 continues; continuing is allowed while context comfortably
   suffices (amend0905-throughput's 6-to-8 target).

## Risks

- R-0958's fix only removes a REDUNDANT print; `_unknown_job`'s own "job not
  found:" wording is untouched and still printed at its two other call sites
  (`job_stop_cmd.py:37,105`) plus `project.py`'s two sites — R-0809 is not
  narrowed by this round.
- `packages/orchestration/data_paths.py`'s `JobIdInvalid`/`JobIdNotFound`
  internal exception messages are still pre-unification text (round 20's
  risk note) — unaffected by this round too.
