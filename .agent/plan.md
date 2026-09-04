# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 11, session 5 - review.list gains a CREATED date end to end:
ReviewerRecommendation gains a created_at field stamped once in
run_reviewer() at construction time (datetime/timezone, matching
patch.list/loop.list's stamp-at-creation pattern), carried through
store_recommendations()'s persisted dict, and rendered as a
(created=...) suffix in _cmd_review_list's text branch - its --json
branch needed no change since it already prints list_recommendations()'s
own dicts verbatim. New tests/cli/test_review_cmd.py covers both
branches.

## Next Steps

- Round 11's own audit of all 18 catalog list commands against T002:
  job/queue/loop/project/patch/memory/tournament/blocker/decision/
  propose/review all carry a date now; execution.list/worker.list/
  config.list stay excused (Risks); change.list's event-log CREATED
  date stays open per DECISION F262 D1; event.list already surfaces
  `timestamp` per row under a different field name, satisfying
  Acceptance as-is.
- test.list's --json already carries created_at but its TEXT branch
  prints a bare count with no per-row listing at all - a pre-existing
  gap wider than a missing date, flagged rather than folded into T002.
- T003 (sort/filter/limit) can start once the gaps above are resolved
  or explicitly excused - review.list (this round) was the last
  unexcused, undated list command the audit found.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands, and
  test.list's missing per-row text listing, are pre-existing quirks
  this feature does not need to fix unless they block T003.