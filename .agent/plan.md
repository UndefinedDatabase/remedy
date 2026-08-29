# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 3 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | closed round 5 |
| the approval decision core | done | round 6 |
| the approved subset diff | done | round 7 |
| landing the subset all-or-nothing | done | round 8 |
| the failed-rollback truth | done | round 9, R-0740 |
| the hunk-decision ledger | done | round 10, R-0741 |
| what the door's effect IS, and the recorder | open | this round, DECISION F033 D4 |
| the write door itself | open | next, needs three guards widened together |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Rule the door's effect and build what it calls. DECISION F033 D4: the door
   RECORDS a hunk decision and never applies it, because `hunk_apply` imports
   `source_apply` and a door importing the seam would defeat the P3 import guard
   by name rather than by substance. `record_hunk_decision` is that effect, and
   R-0742 pins the ledger divergence round 10 declared but left untested.
2. Then the door itself, in ONE commit per widened guard plus its dispatch:
   `UI_EXPOSED_COMMANDS` in `apps/cli/command_catalog.py` is pinned at exactly
   two ids by `TestUiExposedCommands`; `DOOR_METHODS` and `ALLOWED_IMPORTS` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards; and
   `packages.orchestration.hunk_apply` joins `FORBIDDEN_MODULES` so the mistake
   D4 forbids cannot be made silently later.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report's "partially approved (5/8 hunks)" line derived from the ledger, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- Exposure without dispatch answers 501, so the catalog entry and the dispatch
  belong to one round.
- R-0738 stays open and is T003's to repair.
