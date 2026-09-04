# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 14 books round 13's PASS verdict (RECORD13 - closure
precondition 6's RUN step; its two `describe_self_use_run_defects`
strings ADD EVIDENCE to the already-open `R-0784`, no new id minted),
which DISCHARGES precondition 6 pending only the `consumed_by=F114`
edit the closure commit itself makes. This round also authors
`docs/roadmap/features/T3_F114.md`'s Built State section (closure
precondition 4), appended after "Do not touch". No code changes.

## Next Steps

- `remedy integrity check --json` (precondition 3) - not yet run this
  session; do it alongside the closure-commit round.
- The closure commit: evidence job, fresh review zip, STATUS line,
  README sync, `consumed_by=F114`, the PR
  (STATUS_closure_protocol.md algorithm). A fresh session, per F112's
  own precedent (closure spanned rounds 20/21/22/29/30/31 there).
- Session note: round 14, session 3 - 5th delegated round, at the top
  of the 4-5 default; session ends here with this handback.

## Risks

- `docs/roadmap/features/T3_F114.md` is under `docs/roadmap/**`, so
  this round gates `tests/orchestration/test_roadmap_index.py` beside
  `tests/docs/`, per the standing `.agent/context.md` constraint.
- The Built State section's own file-count/test-count claims (19601/
  19554, the file list) are re-measured at authoring time, not copied
  from memory, since this branch's own rounds keep moving them.