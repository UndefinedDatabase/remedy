# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 6, session 2 — T002 batch 4: `project.list` gains its first
`--json` support (it had none before this round - no other list
command in this feature has needed to add `--json` from scratch, only
extend an existing one) plus a `created_at` field and a text-mode
`created=` field. `RemyProject` has no second/updated timestamp, so
neither surface shows one.

## Next Steps

- Round 7: `job.list` (text already prints an ISO date; needs --json
  added) and `queue.list` (text prints an age, derived from
  created_at, not raised as a gap; needs --json added) - same new-flag
  shape as this round, now proven once.
- `loop.list`/`patch.list` have no timestamp on their own model and
  need a design decision before any date can appear (round 3's
  handback carries the full 28-command audit).
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.