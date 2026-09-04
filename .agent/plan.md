# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 19, session 6 - T003 batch 7: `patch.list` wired to
`apply_list_options` with `default_sort_field="created_at"` (ordinary
shape, dict rows, dispatch lambda needed both pairs, no order test).
`loop.list` was investigated but NOT wired this round - DECISION F262
D3 keeps its config-declaration order as default (D2 precedent) and
specifies a real restructure (unify text/json into one row list before
sorting) that round 20 implements, since it does not fit the
insert-before-render shape every other T003 batch used.

## Next Steps

- Round 20: implement DECISION F262 D3 - restructure `_cmd_loop_list`
  to build `(spec, last_run_created_at, last_run_state)` rows
  unconditionally, apply_list_options with `default_sort_field=None`,
  render both text and json from the same post-option list.
- After loop.list, T003 is done for every list command in scope.
  config.list/worker.list/execution.list stay excused per Risks.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- Once loop.list lands, add an integration-level smoke test proving
  the ten-second demo in Acceptance: a named run findable by one
  command with --since/--sort.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority D2, loop.list's config order D3) opts out via
  `default_sort_field=None` rather than losing that order.