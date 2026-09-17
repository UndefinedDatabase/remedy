# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`, the merge commit of pull request
253 (F280's closure).

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 19. C1 books round 18's PASS and registers/resolves R-0957 (round
16's `VISIBLE_GROUP_ORDER` rewrite dropped the `hidden` check on the
default `remedy --help` view, a MEDIUM regression three rounds old). C2
restores the check. After this round: R-0805, R-0809 and R-0895 remain
open on the Acceptance list; the job-id-only slice of R-0809 researched
this session (see Risks) is ready to author next.

## Next Steps

1. R-0809's job-id slice is fully researched and ready to author: fix
   `packages/orchestration/data_paths.py`'s `resolve_job_id` except block
   (one shared choke point reached by `job.py` and `teacher_cmd.py`) plus
   18 duplicated `except ValueError: print(f"Error: invalid job ID:
   {job_id_str!r}", ...)` sites across `brain.py` (11), `snapshot_cmds.py`
   (2), `test_cmds.py` (2), `file.py` (1), `event.py` (1), `memory.py` (1)
   — all replaced with one unified message, `Error: No job matches
   '<id>'. Try: remedy job list.`. This does NOT touch `job_stop_cmd.py`'s
   or `project.py`'s "job not found" wording (a semantically DIFFERENT
   failure — a valid id whose job record is missing, not an id that
   doesn't resolve) — that stays a separate, later decision. Nor does it
   touch run-id or mission-id, which have no shared resolver yet. Tests to
   update: `tests/test_data_paths.py` (2 exact-message assertions),
   `tests/test_brain_viewer.py`, `tests/test_context_coverage.py`,
   `tests/cli/test_product_spine.py`, `tests/cli/test_teacher_cmd.py` (2
   assertions) — all confirmed by this session's fresh grep. R-0809 stays
   OPEN after this slice; it is not fully resolved until run-id and
   mission-id are unified too.
2. R-0805 (`ui status` dead-session pruning) still needs a design pass on
   the session-state model before implementation.
3. R-0895 (README quickstart) runs last (orchestrator brief: it quotes the
   finished catalog).
4. Session 3 continues; continuing is allowed while context comfortably
   suffices (amend0905-throughput's 6-to-8 target).

## Risks

- R-0957's root cause was a gate-list gap, not just a code bug: no round's
  G1/G2 since round 16 ran `tests/cli/test_cli_ux.py`, the one file
  exercising the DYNAMIC `hidden` flag path. A future round touching
  `_print_root_help`, `GROUPS`, or `VISIBLE_GROUP_ORDER` names
  `tests/cli/test_cli_ux.py` in its own targeted gate, not just the
  narrower catalog-content tests.
- R-0809's true scope (mission and run id kinds) still needs its own
  measurement pass before either is touched; do not assume the job-id
  slice's shape generalizes without checking whether run-id and
  mission-id already have (or need) a shared resolver first.
