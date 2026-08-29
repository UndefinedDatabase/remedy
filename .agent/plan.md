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
| one evidence-directory resolver for viewer and doors | open | this round |
| the CLI command and its handler | open | next |
| the write door's exposure and dispatch | open | after the CLI command |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. ONE evidence-directory resolver. `build_diff_view` takes a DIRECTORY, and
   `ui_server._resolve_evidence_dir` already decides which one the viewer reads.
   A second rule in `apps/cli/` could disagree with it, and a decision recorded
   over hunks nobody was shown is the harm `HUNK_RECORD_REFUSAL_NO_DIFF` exists
   to prevent. So the rule MOVES to `packages/orchestration/evidence_index.py`,
   which owns that index already, and `ui_server` delegates.
2. Then the CLI command and its handler TOGETHER: `apps/cli/grouped.py` builds
   its parsers from the catalog, so a handlerless entry is reachable in help and
   answers `Error: no handler`. It lands in the `patch` group, whose size and
   exact subcommand set `TestCatalogLookups.test_get_commands_for_group` in
   `tests/test_command_catalog.py` pins — widened in the SAME commit.
3. Then the write door. `UI_EXPOSED_COMMANDS` is a SUBSET of the catalog pinned
   at exactly two ids by `TestUiExposedCommands`, so exposure needs step 2 first.
   `DOOR_METHODS` and `ALLOWED_IMPORTS` are EQUALITY guards widened in the same
   commit as the dispatch, and `packages.orchestration.hunk_apply` joins
   `FORBIDDEN_MODULES` so DECISION F033 D4's forbidden mistake cannot be made
   silently later.
4. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit. R-0738 is T003's to repair.
