# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 9, session 4 - patch.list gains a CREATED date end to end
(DECISION F262 D1): both creation flows (do_run.py, job.py) stamp
created_at on the stored patch_intent_explanations dict;
list_patch_intents() surfaces it; format_intent_list() gains a
CREATED column ahead of DECIDED. Corrects a stale R8 claim - job.py:623
DOES emit patch_intent_created; only do_run.py's own
do_run_patch_intent_created is dead. Neither event is the source
list_patch_intents() reads (artifact metadata, not the event log) -
see DECISION F262 D1.

## Next Steps

- loop.list has no created_at of its own (LoopSpec is static
  remedy.toml config); already prints a "last run" label from
  job.created_at, which may be the right substitute - separate design
  pass from D1.
- change.list's event-log CREATED date stays open, UNRELATED to D1:
  do_run.py's event stays dead, job.py's real event carries no
  intent_id to join on - see D1's Alternative section.
- The execution.* trio always prints JSON unconditionally with no
  text branch - the pre-existing --json-ignored quirk Risks excuses.
- T003 (sort/filter/limit) starts once date coverage is far enough
  along to sort by.

## Risks

- Stores with no timestamp concept may render "unknown" permanently -
  that satisfies Acceptance, it is not a gap to close later.
- The three ignore-`--json`-entirely execution.* commands are a
  pre-existing quirk this feature does not need to fix unless it
  blocks T003's sort behavior for them specifically.
