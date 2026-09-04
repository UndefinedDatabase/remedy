# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 20, session 6 - T003 batch 8 (final): `loop.list` restructured
per DECISION F262 D3 - `_cmd_loop_list` now builds one
`(spec, last_run_created_at, last_run_state)` row list unconditionally
(moving the `last_run_for_loop` lookup out of the json-only branch),
runs `apply_list_options` once with `default_sort_field=None`
(config-declaration order stays default, D2/D3 precedent), and renders
BOTH text and json from that same row list - the text branch now reads
its row's own precomputed last-run fields instead of calling
`_last_run_label` a second time, removing the prior duplicate lookup.

## Next Steps

- T003 is now DONE for every list command in scope. Remaining before
  T003 closes out: an integration-level smoke test proving the
  ten-second demo in Acceptance (a named run findable by one command
  with --since/--sort), then move to closure per
  docs/roadmap/STATUS_closure_protocol.md.
- config.list/worker.list/execution.list stay excused per Risks -
  confirm this is still true at closure time, not just asserted.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order (queue.list's
  priority D2, loop.list's config order D3) opts out via
  `default_sort_field=None` rather than losing that order - this is
  now DONE for both of the two commands that needed it.