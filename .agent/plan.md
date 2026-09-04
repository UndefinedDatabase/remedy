# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 17, session 6 - T003 batch 5: `blocker.list` and `decision.list`
wired to `apply_list_options`, both `default_sort_field="created_at"`.
Both are job-scoped, return typed rows (StopReason/HumanDecision) whose
`created_at` is already a plain ISO string (no `.isoformat()` needed).
Neither store's existing order is meaningful, and neither has an
order-asserting test, so no D2-style opt-out was needed. Both
dispatch via lambda, so each needed two pairs (handler + dispatch).

## Next Steps

- T003 batch 6: wire review.list, propose.list,
  external-builder.submission-list - same drill, grep each command's
  own tests for an order-asserting test FIRST (DECISION F262 D2).
- patch.list (approval_queue.py's table renderer) and loop.list
  (two-collection rows) still need their own look before wiring -
  neither is a plain single-collection list like the batches so far.
  config.list/worker.list/execution.list stay excused per Risks.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once every command is wired, add an integration-level smoke test
  proving the ten-second demo in Acceptance.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out via `default_sort_field=None` -
  audit each remaining command for this shape before wiring it.