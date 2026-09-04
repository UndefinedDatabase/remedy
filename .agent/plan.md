# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 21, session 7 - SCOPE REPORT per amend0827-process-diet rule 6:
this feature has now run 7 sessions (the operator's soft limit), so
this round books GATE20 (round 20 PASSED), registers R-0795 (T001's
catalog test was never built; `config.list`/`worker.list`/
`execution.list` all PARSE the T003 flags via `_with_list_options`'s
mechanical catalog attachment but their handlers silently discard
them - measured directly, `--sort bogus` raises nothing), and reports
scope instead of opening an eighth build round.

## Next Steps (operator decision needed, per amend0827 rule 6)

- Option A: authorize an 8th session to (1) build the T001 catalog
  test deriving the list-command set from the CLI catalog, (2) wire
  `config.list`/`worker.list`/`execution.list`'s handlers to
  `apply_list_options` (they already receive the parsed flags), (3)
  build the Acceptance ten-second-demo smoke test, then close F262.
- Option B: register a DECISION narrowing T003's Acceptance to
  explicitly exempt these three commands (naming the real reason, if
  one exists, the way D2/D3 did for queue.list/loop.list), correct
  plan.md's Risks section to state the exemption precisely, and close
  F262 without the catalog test or the smoke test.
- change.list's event-log CREATED date stays open, UNRELATED to D1 -
  see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix.
- R-0795 (this round): config.list/worker.list/execution.list PARSE
  all four T003 flags (attached mechanically, like every list command)
  but their handlers ignore them - `--sort bogus` against any of the
  three raises nothing, violating Acceptance's own "exits non-zero"
  bullet. Not yet resolved.