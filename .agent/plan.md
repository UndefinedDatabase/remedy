# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 7, session 2 — T002 batch 5: `job.list` and `queue.list` gain
`--json` end to end (same shape round 6 proved once for
`project.list`). `job.list`'s json carries `created_at` (text already
had it); `queue.list`'s json carries the RAW `created_at` (text keeps
its existing AGE display, `_age()`, unchanged - a pre-existing choice
outside this round's scope) plus `goal`. Neither surface adds an
`updated_at` - neither `Job` nor the queue entry model has a second
timestamp.

## Next Steps

- `loop.list`/`patch.list` have no timestamp on their own model and
  need a design decision before any date can appear (round 3's
  handback carries the full 28-command audit).
- The remaining un-audited handlers from that 28-command list (worker.
  list, worker.registry-list, change.list, review.list, config.list,
  builder.adapter-list, the execution.* trio) still need their own
  pass once T002's date coverage stabilizes.
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.