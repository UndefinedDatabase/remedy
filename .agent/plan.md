# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`.

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 24. C1 books round 23's PASS, adds a prose-slip line for round 23's
plan.md overage (53 lines vs the 50-line cap), and lands R-0809's LAST piece:
`mission_cmd.py`'s `_load_mission_or_exit` (6 callers) and `handoff.py`'s
`MissionForHandoffNotFoundError` both unify to `Error: No mission matches
'<id>'. Try: remedy mission list.`. Six `test_mission_cmd.py` assertions
updated to match. This closes R-0809 — `Done:` written this round.

## Next Steps

1. R-0805 (`ui status` dead-session pruning) needs a design pass on the
   session-state model before implementation.
2. R-0895 (README quickstart) runs last — it quotes the finished catalog.
3. Session 4 continues while context comfortably suffices.

## Risks

- `data_paths.py`'s `JobIdInvalid`/`JobIdNotFound` messages are still
  pre-unification text — a separate, unrelated exception family.
- Count every future plan.md replacement against the 50-line cap before
  emission (round 23's own slip).
