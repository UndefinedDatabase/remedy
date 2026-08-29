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
| the approved subset diff | done | this round |
| landing the subset all-or-nothing | open | next, through `source_apply.py` |
| the write-door command and its exposure | open | needs the import guard widened |
| the hunk-decision ledger in evidence | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Land the subset: feed the per-file diffs this round emits through
   `apply_structured_patch`, all-or-nothing, so a conflict inside the approved
   set leaves NOTHING applied and names the hunk that conflicted. The applier
   already snapshots and reverts; the round proves the atomicity, it does not
   build it.
2. Then the write door: `approve_hunks` reaches the applier through a service
   seam, never by importing it — `packages.orchestration.source_apply` is in
   `FORBIDDEN_MODULES` in `tests/ui_server/test_command_channel.py`.
3. Then the hunk-decision ledger in evidence, which T003's report line reads.

## Risks
- The door's import guard is an EQUALITY guard, so any new import is widened in
  the SAME commit that adds it, or the branch tip ships red.
- A truncated or binary view cannot be re-emitted faithfully; the subset builder
  refuses rather than shrinking a diff silently, and the apply round must keep
  that refusal rather than defaulting past it.
- R-0738 stays open and is T003's to repair.
