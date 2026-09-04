# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 18, session 6 - T003 batch 6: `review.list`, `propose.list` and
`external-builder.submission-list` wired to `apply_list_options`, all
`default_sort_field="created_at"`. All three dispatch with `args`
passed straight through (no lambda extraction), so each needed ONLY
ONE pair (the handler body) - no dispatch-site pair, unlike
project/blocker/decision. None had an order-asserting test. Row
shapes vary: review.list's rows are dicts, propose.list's are
ProposedTask pydantic models (`created_at.isoformat()`), and
external-builder.submission-list's are dicts keyed `received_at`
mapped to the shared `created_at` sort-field name for flag
consistency, per Design's "same words for same flags".

## Next Steps

- T003 is now done for every plain single-collection list command.
  Remaining: patch.list (approval_queue.py's table renderer) and
  loop.list (rows built from two different collections) still need
  their own look before wiring - neither is a plain single-collection
  list. config.list/worker.list/execution.list stay excused per Risks.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once patch.list/loop.list are wired (or excused), add an
  integration-level smoke test proving the ten-second demo in
  Acceptance: a named run findable by one command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out via `default_sort_field=None` -
  audit patch.list/loop.list for this shape before wiring them.