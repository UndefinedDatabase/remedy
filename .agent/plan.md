# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8 — the split-and-close default operator
amendment amend0905-throughput makes standing at the soft limit, which this feature reached at
session seven of seven. F275 is registered; what remains is the closure itself.

## Current Step

The integration-gate round, per docs/agents/integration_gate.md: the full suite on the branch in
the primary checkout, the full suite at the base in a throwaway worktree with build parity
restored, and the two failure sets compared. It MEASURES and does not repair — no file outside
`.agent/` changes. It also books round 17's PASS verdict and the one dated prose slip that round
declared.

## Next Steps

1. The self-use item closure precondition 6 requires. Every queue item is consumed, so
   `generate_and_append_if_empty` runs FIRST; whatever it yields is planned and run to the normal
   approval gate, and every defect its findings reader returns is registered before the close.
2. The ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
3. The evidence job and the fresh review zip. The zip's `base_commit` is the FORK POINT
   `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain `rev-list` counts are
   EQUAL — never `git merge-base`, which names `origin/main`'s tip here and gives unequal counts.
4. The closure commit: the STATUS `[x]` flip with the README sync and the one `consumed_by` edit,
   in ONE commit; then the pull request.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
- R-0736 is OPEN: the integration gate's own parity recipe manufactures false base failures unless
  the copied `apps/ui/dist` is stamped NEWER than the newest file under `apps/ui/src`.
