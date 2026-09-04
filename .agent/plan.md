# Plan — F262 List commands v2 (dates, sort, filter)

Branch: feature/f262-list-commands-v2, cut from `main` after pull
request 235 was merged at the Open PR Gate.

## Goal

Every list command shows a CREATED and an UPDATED date and carries the
same `--sort <field> [--desc] --since <when> --until <when> --limit <n>`
flags, with newest-first as the DEFAULT everywhere, without a flag
(docs/roadmap/features/T2_F262.md).

## Current Step

Round 1, session 1 — claim F262 in the STATUS ledger and set this file
and `.agent/context.md`. Branch already cut. Round 2 builds T001: the
shared listing-option surface (four flags defined once, wired into the
argument layer), plus a test deriving the list-command set mechanically
from `apps/cli/command_catalog.py`, failing loudly with the valid set
named — first, per the feature file's Orchestrator brief.

## Next Steps

- Round 2 (T001): state the exact mechanical rule for "list command"
  over the catalog (`subcommand` equal to `list` or ending `-list` is
  the working hypothesis; `checklist` a same-suffix false positive,
  `snapshot list-applies` a narrower listing to classify explicitly),
  wire the four flags once, ship the coverage test.
- T002: CREATED/UPDATED on every row, per store; an unknown date renders
  as unknown, never invented. Widest slice — plan its commit split first.
- T003: the sort/filter/limit behaviour plus the newest-first default.
  Depends on both T001 and T002.

## Risks

- Measured at this branch's base (`7c65d9cc`): 28 catalog `subcommand=`
  values are exactly `list` or end `-list` — a sizing signal only, not a
  spec; round 2 states and gates the real rule.
- Some stores may lack a CREATED/UPDATED timestamp today; T002 surfaces
  each gap per store, not assumed here.
- `--json`'s existing keys are not renamed, only added to (Do not touch);
  every T002/T003 store change is checked against that before landing.