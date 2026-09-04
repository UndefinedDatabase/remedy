# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 10, session 4 - loop.list gains --json end to end (catalog
_JSON_OPT + supports_json=True, handler json_output kwarg + json
branch, dispatch lambda), carrying last_run_created_at/last_run_state
per loop sourced from the SAME last_run_for_loop() call the existing
text "last run:" label already uses - no new timestamp invented.
T001's --sort/--since/--until/--limit flags were already present on
loop.list via _with_list_options' auto-injection (subcommand=="list"
matches); only --json and its JSON date fields were the real gap.

## Next Steps

- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see DECISION F262 D1's Alternative section.
- The execution.* trio always prints JSON unconditionally with no
  text branch - the pre-existing --json-ignored quirk Risks excuses.
- T003 (sort/filter/limit) starts once date coverage is far enough
  along to sort by - patch.list and loop.list both now have dates;
  audit whether any remaining list command still lacks one before
  starting T003, or start T003 against the commands that already
  qualify.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.