# Plan — F033 Hunk-level diff approval

Branch: feature/f033-hunk-approval-v2, cut from `main` at `bd8d9529`, the merge
commit of pull request 221. SESSION 1 of this feature.

## Goal
Surgical consent over changes: hunks carry STABLE content-hash ids, an
`approve_hunks` command applies the approved set to the branch all-or-nothing,
and rejected hunks become precise repair feedback quoted verbatim in the next
round — every partial state rendered truthfully in viewer, node and report.

## Current Step

| Item | Status | Reason |
|------|--------|--------|
| restart, claim, register R-0738 | done | round 1, DECISION F033 D1 |
| the shared identity function and its tests | done | round 2, 10 tests |
| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | round 3, 50 tests |
| rule the client's invented id | done | this round, DECISION F033 D2 |
| retire the diff-repair local hunk helper | open | next round, T001's last item |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Retire the local hunk helper in `packages/orchestration/diff_repair.py` onto
   `hunk_identity`, keeping `tests/orchestration/test_diff_repair.py` green.
   That closes T001.
2. Then T002: the `approve_hunks` command, its validation, and the
   all-or-nothing subset apply built on
   `packages/orchestration/source_apply.py`.
3. `packages/orchestration/repo_applicator.py` applies nothing by design, so the
   subset seam is new work rather than a parameter on something existing.

## Risks
- The diff endpoint added by F256 serves this envelope, so a shape change is
  consumer-visible. Version 2 is the declared seam and it has been taken.
- The client tests build their own payloads, so a server shape change cannot
  redden them. Keeping the fixtures realistic is the only guard against the
  client drifting a version behind the server.
- R-0738 stays open and is T003's to repair.
