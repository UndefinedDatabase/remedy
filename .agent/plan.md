# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 2 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| T001 stable ids, viewer v2, consolidation | done | closed round 5, DECISION F033 D3 |
| the approval decision core | done | round 6, 30 cases |
| the approved subset diff | done | round 7, 17 cases |
| landing the subset all-or-nothing | done | this round, on `source_apply.py` |
| the write-door command and its exposure | open | next, needs the import guard widened |
| the hunk-decision ledger in evidence | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The write door: expose `approve_hunks` and dispatch it. The door may NOT
   import the applier — `packages.orchestration.source_apply` is in
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py` — so the
   command reaches `apply_approved_hunks` through a service seam, and
   `TestCommandDoorImportGuard`'s ALLOWED_IMPORTS is widened in the SAME commit
   that adds the import, with the decision that widens it.
2. Then the hunk-decision ledger in evidence, which T003's report line reads.
3. Then T003: rejection reasons quoted verbatim into the next repair prompt, and
   partial state rendered truthfully in viewer, node and report.

## Risks
- The door's import guard is an EQUALITY guard, so a new import reddens the
  branch tip unless it is ruled in the same commit.
- A truncated or binary view cannot be re-emitted faithfully; the subset builder
  refuses rather than shrinking a diff silently, and every later caller must
  keep that refusal rather than defaulting past it.
- R-0738 stays open and is T003's to repair.
