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
| restart F033 from current main | done | round 1, DECISION F033 D1 |
| book the F257 R12 closure verdict | done | round 1, amend0827 rule 1 |
| register R-0738 | done | round 1 |
| claim F033 in STATUS | done | round 1 |
| survey the hunk-identity surface | done | round 1, in the handback |
| T001 stable ids, JSON v2, shared helper | open | round 2 onward |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Author T001 from the survey: the content-hash id function, its home, the
   `DIFF_VIEW_VERSION` bump and the stability property tests.
2. Consolidate the diff-repair hunk helper onto the shared identity, keeping
   `tests/orchestration/test_diff_repair.py` green.
3. T002's command, its validation and the all-or-nothing subset apply.

## Risks
- The shared-helper consolidation crosses two modules that ship today; their
  regression suites are the safety net and are named in every order touching them.
- `packages/orchestration/diff_parser.py` is PURE and TOTAL by its own docstring
  and never raises on malformed input. Content-hash ids must not change that.
- The parked branch `feature/f033-hunk-approval` at `ed040812` holds a 574-line
  inventory taken at `32cde54e`, before F256 rewrote the diff surface. It is
  INPUT to be re-derived, never a source of fact.
