# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 12 books round 11's PASS verdict (RECORD11 - integration gate
clean, F114's first "full suite green" claim) and one reviewer prose
slip (PROSESLIP11), then does closure precondition 6's GENERATION step
only: the queue has no pending item, so `generate_and_append_if_empty()`
appends SU-008 (the R-0418 paragraph SU-005/006/007 already quoted) as
PENDING. No production code changes. Running SU-008 is round 13, per
the split F112 used at its own rounds 20/21.

## Next Steps

- Round 13: run SU-008 via `self_use_job`/`self_use_runner` to the
  approval gate (real local `ollama`, small budget); register
  `describe_self_use_run_defects`' output - expect it adds evidence to
  the ALREADY-OPEN `R-0784` (§3 item 30), not a new id.
- Author T3_F114.md's Built State section (precondition 4).
- `remedy integrity check --json` (precondition 3).
- Then the closure commit: evidence job, fresh review zip, STATUS
  line, README sync, `consumed_by=F114`, the PR. Likely its own
  session, per F112's closure spanning rounds 20/21/22/29/30/31.
- Session note: round 12, session 3 - 3rd delegated round, at the 4-5
  default.

## Risks

- `append_generated_item` rewrites the WHOLE queue file (`json.dumps`
  ensure_ascii) - the ALREADY-OPEN `R-0785` class; expect a full-file
  diff, not a clean append.
- Round 13's run is a real, budget-capped LLM call against local
  `ollama` - bounded, expected to end BLOCKED (the correct outcome).