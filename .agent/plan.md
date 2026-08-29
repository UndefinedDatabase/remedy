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
| wire the parser, bump DIFF_VIEW_VERSION to 2 | done | this round |
| rule the client's fallback id synthesis | open | next round |
| retire the diff-repair local hunk helper | open | |
| T002 approve_hunks, subset atomicity, ledger | open | |
| T003 rejection to repair, partial-state truth | open | owns R-0738 |

## Next Steps
1. Rule the client fallback at `apps/ui/src/api/diffViewModel.ts`, which
   synthesises a positional id when the server sends an empty one, and move the
   TypeScript pins on version 1 and on the `"<n>:<m>"` id form.
2. Retire the local hunk helper in `packages/orchestration/diff_repair.py` onto
   the shared identity, keeping its regression suite green.
3. Then T002: the `approve_hunks` command, its validation and the
   all-or-nothing subset apply.

## Risks
- The diff endpoint added by F256 SERVES this envelope, so the version bump is a
  real consumer-visible change and not a private one.
- The client fallback means an empty server id becomes a POSITIONAL id on screen
  rather than an error, so a content-hash contract can still be violated
  silently until the next round rules it.
- `packages/orchestration/diff_parser.py` is PURE and TOTAL by its own docstring.
  The identity call must not change that.
