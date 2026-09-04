# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 4, session 1 — T002 batch 2: memory.list gains `updated_at` in
its --json output and both created/updated in its text output.

## Next Steps

- Round 5: tournament.list and external-builder.submission-list print
  only a COUNT in text mode today - no per-row listing exists at all -
  so adding dates there means designing a first per-row text format,
  a bigger slice than a one-line edit. Design it explicitly before
  coding it.
- Then: job.list/queue.list/project.list need `--json` added before a
  date can appear there; loop.list/patch.list have no timestamp on
  their model and need a design decision (round 3's handback carries
  the full 28-command audit).
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.