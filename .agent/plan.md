# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 22, session 8 - R-0795 core fix: `config.list`, `worker.list`
and `execution.list` wired to `apply_list_options`. `worker.list`/
`config.list` use `default_sort_field=None` (no date field, like
queue.list/loop.list's D2/D3); `execution.list` uses
`default_sort_field="started_at"` (a real ISO date per row). Six
regression tests added (two per command). R-0795 is LANDED, not yet
Done - the reviewer converts it at the next gate (§4 item 4).

## Next Steps

- Round 23: extend `TestListCommandOptions`
  (tests/test_command_catalog.py) to dispatch every `_is_list_command`
  entry's HANDLER (not just its argparse signature) with an invalid
  `--sort` and assert a non-zero exit - T001's own never-built
  Acceptance bullet.
- Round 24: the Acceptance ten-second-demo smoke test, then closure
  per docs/roadmap/STATUS_closure_protocol.md.
- change.list's event-log CREATED date stays open, UNRELATED to D1 -
  see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- A command with its OWN meaningful non-date default order opts out
  via `default_sort_field=None` (queue.list D2, loop.list D3,
  worker.list/config.list now too).
- R-0795: LANDED this round for the three named commands - the
  catalog-wide enumeration proof (T001's own gap) stays open, round 23.