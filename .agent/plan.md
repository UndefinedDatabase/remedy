# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 2, session 1 — T001 ships: the shared listing-option surface
attached to every list-shaped catalog command by construction
(`apps/cli/command_catalog.py`, `_with_list_options`), plus a
catalog-derived coverage test. The flags parse everywhere now; no
store's OUTPUT changes yet — that is T002/T003.

## Next Steps

- Round 3 (T002): audit which stores already record CREATED/UPDATED,
  surface both on every list row; an unknown date renders as unknown,
  never invented. Widest slice — plan the commit split before starting.
- T003: the behaviour behind the four flags (per-command `--sort`
  choices, `--since`/`--until` parsing, `--limit`, newest-first default)
  now that T001's flags exist to carry it.

## Risks

- T001 leaves the flags accepted but inert everywhere except
  `event.list`'s pre-existing `--since`/`--limit`, kept as-is rather
  than replaced to avoid an argparse collision (see round 2's handback).
- The mechanical rule catches 28 commands; `snapshot list-applies`
  (starts with, not ends with, `list`) is excluded — round 3 states
  whether it belongs, explicitly, rather than widening the rule.