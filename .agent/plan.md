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
| T001 stable ids, viewer v2, consolidation | done | round 5 |
| decision core · subset diff · all-or-nothing apply | done | rounds 6, 7, 8 |
| failed-rollback truth · ledger · the door's effect | done | rounds 9-11, D4 |
| the recorder takes the viewer's envelope | open | this round |
| the CLI command and its handler | open | next |
| the write door's exposure and dispatch | open | after the CLI command |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The recorder takes the VIEWER'S ENVELOPE, not only diff text.
   `diff_view_source.build_diff_view` holds an attempt's diff already parsed and
   already read under its own byte ceiling; re-parsing text a caller has as an
   envelope would put a second copy of that ceiling beside the first. One
   implementation, two doors, plus the refusal an ABSENT artifact needs so the
   operator is not told their ids are wrong.
2. Then the CLI command and its handler TOGETHER. Measured at `624818e6`:
   `CATALOG` holds 340 entries and `collect_all_handlers()` 340 handlers, so
   entries without a handler number ZERO — no test asserts it, nothing has broken
   it, and `apps/cli/grouped.py` builds its parsers from the catalog, so a
   handlerless entry is reachable in help and answers `Error: no handler`. It
   lands in the `patch` group beside `patch.approve` and `patch.apply`.
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
