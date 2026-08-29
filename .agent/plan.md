# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 4 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | done | round 12 |
| one evidence-directory resolver for viewer and doors | done | round 13 |
| the CLI command and its handler | open | this round |
| the write door's exposure and dispatch | open | next |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The CLI command `patch.approve-hunks` and its handler, in ONE commit, because
   `apps/cli/grouped.py` answers `Error: no handler` for a catalog entry that has
   none. The `patch` group's size and exact subcommand set are pinned by an
   EQUALITY guard in `tests/test_command_catalog.py`, widened in that same commit.
   The handler mints no refusal vocabulary: every refusal comes from
   `hunk_approval` or `hunk_decision_record`. R-0743 is fixed here too — a test
   pinning that the index record beats the CWD-relative fallback.
2. Then the write door. `UI_EXPOSED_COMMANDS` is a SUBSET of the catalog pinned
   at exactly two ids by `TestUiExposedCommands`, so exposure needs step 1 first.
   `DOOR_METHODS` and `ALLOWED_IMPORTS` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards widened in the
   same commit as the dispatch, and `packages.orchestration.hunk_apply` joins
   `FORBIDDEN_MODULES` so DECISION F033 D4's forbidden mistake cannot be made
   silently later.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit. R-0738 is T003's to repair.
