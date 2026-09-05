# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md, scoped by DECISION F262 D4).

## Current Step

Round 23, session 8 - SCOPE CORRECTION, no code this round: booked
GATE22 (round 22 PASSED), converted R-0795 to Done. Registered
FINDING R-0796 - 13 of 28 list-shaped catalog commands were never
wired at all, not just the 3 R-0795 named. Registered DECISION F262
D4 scoping Acceptance to 24 of 28 commands (3 static registries + 1
hybrid catalog excluded by name); the other 9 have genuine dates and
stay IN scope, deferred. T2_F262.md amended with a pointer to D4.

## Next Steps (round-budget mismatch - a DECISION-routed proposal per
amend0827 rule 6's mechanism, not a question)

- Option A: authorize sessions beyond the 7-session/25-round soft
  caps (already session 8, round 23) to wire the 9 remaining commands
  (test.list, repair.item-list, builder.session-list,
  execution.approval-list, mission.list, change.list, event.list,
  external-builder.package-list, self-repair.proposal-list) plus the
  T001 catalog-driven handler test plus the Acceptance smoke test.
- Option B: split the 9 remaining into a NEW follow-up feature
  (STATUS.md line), build the T001/Acceptance tests scoped to the 24
  D4-covered commands only, and close F262 within the 3 rounds left.
- change.list's event-log CREATED date (a separate, older gap) stays
  open either way - see DECISION F262 D1's Alternative section.

## Risks

- Stores with no timestamp concept render "unknown" permanently - now
  formalized as D4's static-registry exclusion, not an informal note.
- R-0796's 9 gaps are real product debt regardless of option chosen -
  Option B moves them, it does not remove them.
- Round 23 has NO code/test path in its change set (only `.agent/**`
  plus T2_F262.md's pointer) - a finding-routed-to-planning round per
  §4 item 7, matching the DECISION F112 D5 precedent shape.