# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 14, session 5 - T003 batch 2: `queue.list` and `memory.list` are
wired to `apply_list_options`. `queue.list` passes `default_sort_field=
None` (DECISION F262 D2) so its existing, tested PRIORITY default order
is preserved when no flags are given - `--sort created_at`/`priority`/
`status` are available as explicit overrides. `memory.list` passes
`default_sort_field="created_at"`, changing nothing about its no-flag
case (it already sorted newest-first internally) while adding `--sort
key`/`--since`/`--until`/`--limit`. `list_options.py`'s own contract
widened to make the priority-preserving case possible for any future
caller with a similar pre-existing order.

## Next Steps

- T003 batch 3+: wire the remaining commands - patch.list (approval_
  queue.py's format_intent_list table renderer needs its own look before
  wiring, since it isn't a plain per-row print like the commands done so
  far), loop.list (JSON rows and text rows are built from two DIFFERENT
  collections today - reconcile before wiring), then project.list,
  tournament.list, blocker.list, decision.list, review.list, propose.list,
  test.list, external-builder.submission-list, config.list. Re-check EACH
  one for a queue.list-shaped surprise (an existing meaningful non-date
  order) before assuming date-descending is safe, per DECISION F262 D2's
  precedent - grep its own tests for an order-asserting test FIRST.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
  execution.list/worker.list/config.list stay excused per Risks.
- Once every command is wired, add an integration-level smoke test
  proving the ten-second demo in Acceptance: a named run findable by
  one command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
- A command with its OWN meaningful non-date default order (queue.list's
  priority, DECISION F262 D2) opts out of the forced newest-first default
  via `default_sort_field=None` rather than losing that order - audit
  each remaining command for this shape before wiring it.