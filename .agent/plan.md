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
| the approval decision core and its tests | done | this round |
| the all-or-nothing subset apply | open | next, on `source_apply.py` |
| the write-door command and its exposure | open | needs the import guard widened |
| the hunk-decision ledger in evidence | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. The subset apply: land ONLY the approved hunks, all-or-nothing, with a
   conflict inside the approved set falling back to nothing-applied and naming
   the hunk. Built on `packages/orchestration/source_apply.py`, whose
   `apply_structured_patch` takes no subset today.
2. Then the write door: `approve_hunks` reaches the applier through a service
   seam, never by importing it — `packages.orchestration.source_apply` is in
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`.
3. Then the hunk-decision ledger in evidence, which T003's report line reads.

## Risks
- The door's import guard is an EQUALITY guard, so any new import is widened in
  the SAME commit that adds it, or the branch tip ships red.
- `packages/orchestration/repo_applicator.py` applies nothing by design, so the
  subset seam is new work rather than a parameter on something existing.
- R-0738 stays open and is T003's to repair.
