# Plan — F114 Cost preview per command

Branch: feature/f114-cost-preview-per-command, cut from `main` after
pull request 234 was merged at the Open PR Gate.

## Goal

Expensive actions stop starting silently: commands that will spend real
money show an upfront estimate band with its basis and require
confirmation above a configured threshold in attended mode; unattended
runs rely on budgets, not prompts (docs/roadmap/features/T3_F114.md).

## Current Step

Round 17 books round 16's PASS verdict (RECORD16 — precondition 3
confirmed, all six closure preconditions now hold) into the ledger,
then builds the evidence job and the review zip — algorithm steps 1-2
of docs/roadmap/STATUS_closure_protocol.md. No `[x]` flip, no README
sync, no `consumed_by` edit, no pull request this round.

## Next Steps

- The closure commit itself, in ONE commit: the `[x]` flip on
  docs/roadmap/STATUS.md, the README capability sync,
  `scripts/self_use_queue.json`'s `consumed_by=F114` edit and the
  final `.agent/` state.
- Open the pull request. Not merged this session — the operator's
  manual-review window; the next feature's Open PR Gate merges it.

## Risks

- The evidence directory and the zip are gitignored and NEVER
  committed; only `.agent/**` changes land in git this round.
- `remedy-review-*.zip` files write directly under
  `/home/decodeux/Repos/remedy-history/zips`; nothing there is
  deleted.