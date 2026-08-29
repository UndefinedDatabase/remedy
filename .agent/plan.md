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
| the CLI command and its handler | done | round 14 |
| R-0744, the CLI door's job-id resolution | open | this round |
| the write door's exposure and dispatch | open | this round |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |
| the operator docs for `patch approve-hunks` | open | closure sequence |

## Next Steps
1. R-0744: the CLI handler resolves the evidence directory from the RESOLVED job
   id, so a short prefix or an uppercase UUID stops being reported as a missing
   diff. The eleven existing tests are blind to it, so the fix ships with tests
   that discriminate.
2. The write door, in ONE commit with its guards. `UI_EXPOSED_COMMANDS` gains the
   id; `DOOR_METHODS`, `ALLOWED_IMPORTS` and `FORBIDDEN_MODULES` in
   `tests/ui_server/test_command_channel.py` are EQUALITY guards that must widen
   with it, and `packages.orchestration.hunk_apply` joins the forbidden set so
   DECISION F033 D4's mistake cannot be made silently later.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, the
   report line derived from the ledger, and partial state rendered truthfully in
   viewer, node and report. R-0738 is T003's to repair.
4. Then the closure sequence, which owes `docs/` an operator-facing description
   of `remedy patch approve-hunks` — no round has been allowed a `docs/` path yet.

## Risks
- The door's import guard is an EQUALITY guard: a new import reddens the branch
  tip unless it is ruled in the same commit.
