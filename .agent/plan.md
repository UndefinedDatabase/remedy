# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 13, session 5 - T003 batch 1: `packages/orchestration/list_options.py`
is a new shared helper (`apply_list_options`, `parse_time_bound`,
`ListOptionError`) that filters by --since/--until, orders by
--sort/--desc (newest-first is the DEFAULT with no flags), and caps by
--limit, over any row list (dicts or objects, via key-function maps) -
one implementation instead of 18 hand-rolled ones. Wired into `job.list`
first as the design's proof: `_cmd_list_jobs` reassigns its own `jobs`
list once before either --json or text rendering, so both branches see
the same filtered/sorted/limited rows by construction. An unknown
--sort field exits non-zero naming the valid set, never silently
ignored.

## Next Steps

- T003 batch 2+: wire `apply_list_options` into the remaining 17 list
  commands, one or a few at a time, same pacing T002 used (R2-R12).
  Order by risk/simplicity: patch.list/loop.list/queue.list/
  memory.list next (already-dated, well-tested, isolated handlers);
  loop.list needs care since its JSON rows (per-loop last-run lookup)
  and text rows (iterating LoopSpec objects) are built from two
  different collections today - reconcile that shape before wiring.
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
