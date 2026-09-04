# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 8, session 3 - T002 batch 6: `patch.list` gains `--json` end to
end (same shape rounds 6-7 proved for project.list/job.list/
queue.list) plus a DECIDED column in text output surfacing the intent
dict's own `decided_at` (no `created_at` exists on a patch intent -
only a decision timestamp). Five other audited handlers closed out
this round with NO code change owed: worker.list, worker.registry-list,
review.list, config.list, builder.adapter-list carry no timestamp
field anywhere on their underlying models - Acceptance is satisfied
as-is per the Risks section below.

## Next Steps

- `change.list`'s event log DOES carry timestamps, but the only
  production emitter of an intent-creation event
  (`do_run_patch_intent_created` in do_run.py) is read by NO consumer,
  while every reader instead checks a bare `patch_intent_created` no
  production code emits - needs a design decision on which event
  names creation before a date can land there.
- `loop.list`/`patch.list` have no `created_at` on their own model and
  need a design decision before a CREATED date can appear; `loop.list`
  already prints a "last run" label that may be the right substitute.
- The execution.* trio (`execution.template-list`, `execution.list`,
  `execution.approval-list`) always print JSON unconditionally with no
  text branch at all - the pre-existing `--json`-ignored quirk the
  Risks section already excuses.
- T003 (sort/filter/limit behavior) starts once date coverage is far
  enough along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.