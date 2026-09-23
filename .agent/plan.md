# Plan — F278 Durable writes & loud failures

Branch: feature/f278-durable-writes-loud-failures, cut from `main` at
`9817a927`, the merge commit of pull request 265 (F283's closure).

## Goal

One durable write in this repository, used everywhere, and no artifact that is
silently incomplete (`docs/roadmap/features/T2_F278.md`).

## Current Step

ROUND 12, the closing round. It books round 11's PASS, rotates the finding
ledger into its archive, accepts F278 in `docs/roadmap/STATUS.md` with the
README's three pinned places and the self-use item's `consumed_by` in the same
commit, and opens the pull request, which this session never merges.

## Next Steps

1. The Open PR Gate at the start of the next feature's session merges this
   branch's pull request, after the operator's review window.
2. Rule A5 then claims the first unchecked feature in
   `docs/roadmap/STATUS.md`.

## Risks

Twenty-six findings are open and none is this feature's own. Twelve rounds
were spent across two sessions, under the soft limit of 25.
