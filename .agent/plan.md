# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`.

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 25. C1 books round 24's PASS. C2 lands R-0805: `remedy ui status`
shows live sessions only by default; dead sessions are archived (never just
deleted) into `<data_root>/ui/sessions_dead/`, capped at the ten most
recently ended, each carrying an `ended_at` timestamp; `ui start`, `ui
status` and `ui stop` all prune on every call; a new `--all` flag on `ui
status` lists the archived ten with their end time. New tests cover the
archive, the cap, and the `--all` flag through the grouped CLI. This closes
R-0805 — `Done:` written this round.

## Next Steps

1. R-0895 (README quickstart) is the only Acceptance item left — it quotes
   the finished catalog, so it runs last.
2. Session 4 continues while context comfortably suffices.

## Risks

- `data_paths.py`'s `JobIdInvalid`/`JobIdNotFound` messages are still
  pre-unification text — a separate, unrelated exception family, not part
  of any open Acceptance item.
