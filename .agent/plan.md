# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 16, session 6 - T003 batch 4: `project.list` wired to
`apply_list_options` with `default_sort_field="created_at"` -
`_list_projects_readonly()` already sorted newest-first
(`test_list_sorted_newest_first`), so forcing the same default via the
shared helper changes nothing observable and needed no D2-style
opt-out. Dispatch is a lambda (`"project.list": lambda args: ...`), so
both the handler body AND the dispatch site needed a pair, unlike
tournament.list's single pair.

## Next Steps

- T003 batch 5+: wire the remaining plain-dict/model-row commands -
  blocker.list, decision.list, review.list, propose.list,
  external-builder.submission-list are shaped like
  project.list/tournament.list. patch.list (approval_queue.py's
  format_intent_list table renderer) and loop.list (JSON/text rows
  built from two different collections) still need their own look
  before wiring. config.list/worker.list/execution.list stay excused
  per Risks. Re-check EACH remaining command's OWN tests for an
  order-asserting test FIRST, per DECISION F262 D2's precedent, before
  assuming date-descending is safe to force.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
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