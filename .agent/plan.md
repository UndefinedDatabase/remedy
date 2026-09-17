# Plan — F281 CLI help surface

Branch: feature/f281-cli-help-surface, cut from `main` at
`c617dd74df26b8e677161b265a88d5926f4d78ab`.

## Goal

Every catalog description, role label and help page reads as the finished
vocabulary of DECISION amend0905-vocab D4 (`docs/roadmap/features/T2_F281.md`).
DONE when T001 and the Acceptance list hold.

## Current Step

ROUND 26. C1 books round 25's PASS. C2 lands R-0895 — the LAST open
Acceptance item: `README.md`'s Quickstart block is rewritten to name only
commands and flags the current catalog holds (mirroring
`apps/cli/grouped.py`'s own already-correct `_QUICK_START` golden path), and
`tests/cli/test_advertised_commands.py`'s operator-facing sweep is widened
to also scan `README.md`, closing the exact gap R-0895's own FIX clause
named. This closes R-0895 — `Done:` written this round. Every other
Acceptance bullet in `docs/roadmap/features/T2_F281.md` was independently
re-verified true by the reviewer before this round was authored (visible
group order pinned as data, `Worker:` gone from the report renderers,
200-char option wrap tested, `doctor core`'s dead-commands section present
and empty, F259's docs test in `enforced` mode, R-0934's resolution line
present). With this round's C2, ALL Acceptance items hold.

## Next Steps

1. F281's Acceptance list is fully satisfied after this round. The next
   round should run the closure sequence
   (`docs/roadmap/STATUS_closure_protocol.md`): evidence job, fresh review
   zip, the authored STATUS `[~]`→`[x]` line, and the PR — read that
   protocol document in full before authoring the closure round, since it
   is not summarized here.
2. Session 4 continues while context comfortably suffices.

## Risks

- `data_paths.py`'s `JobIdInvalid`/`JobIdNotFound` messages are still
  pre-unification text — a separate, unrelated exception family, out of
  scope for F281 (not named by any open Acceptance item).
