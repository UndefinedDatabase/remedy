# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 3, session 1 — T002 batch 1: text-output dates for the four
commands whose store already has them and whose --json already shows
them (blocker.list, decision.list, approval.policy-list,
self-repair.proposal-list), plus new coverage for the two that had
none before.

## Next Steps

- Round 4 (T002 batch 2): memory.list (add `updated_at` to its json
  dict, then text); tournament.list and external-builder.submission-list
  (both DROP their timestamp from the json shape today — restore it,
  then add text).
- Round 5 (T002 batch 3): job.list/queue.list/project.list need
  `--json` added before a date can appear there; loop.list/patch.list
  have no timestamp on their own model and need a design decision.
- Round 6+: builder.adapter-list, execution.* (ignore --json entirely,
  pre-existing), worker.list, worker.registry-list, change.list,
  review.list, config.list have NO timestamp concept — most likely
  render "unknown" (Acceptance) rather than invent one. T003 starts
  once date coverage is far enough along to sort by.

## Risks

- The full per-store audit (28 commands) lives in this round's
  handback, not restated here every round.
- Stores with no timestamp concept may render "unknown" permanently —
  that satisfies Acceptance, it is not a gap to close later.