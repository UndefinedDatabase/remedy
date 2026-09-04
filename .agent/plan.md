# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 12, session 5 - test.list's TEXT branch gains a real per-row
listing (test_run_id, status, exit_code, created), replacing the old
bare-count-only print; an honest "No test runs for X." message covers
the empty case. --json needed no change - it already carried every
field the text branch now uses, sourced from the same out["runs"]
list built earlier in _cmd_test_list. This closes the last gap
round 11's audit found: every catalog list command now either shows a
date, or is explicitly excused in Risks below.

## Next Steps

- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
  This is the one remaining named, excused gap.
- T003 (sort/filter/limit) can start now: every list command either
  carries a date (job/queue/loop/project/patch/memory/tournament/
  blocker/decision/propose/review/test/event, event.list's own
  `timestamp` field counting) or is excused (execution.list/
  worker.list/config.list: no timestamp concept or a pre-existing
  --json-unconditional quirk; change.list: DECISION F262 D1).
- T003 design should start with the shared `_with_list_options()`
  surface in apps/cli/command_catalog.py (already injects --sort/
  --since/--until/--limit into every list subcommand per T001) and
  decide where the actual sort/filter/limit BEHAVIOUR lives - likely
  one shared helper each list handler's text/json branches call,
  rather than 18 hand-rolled implementations.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.