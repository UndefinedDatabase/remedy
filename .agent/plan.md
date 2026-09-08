# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered and the
integration gate has PASSED; what remains is the self-use precondition and the closure itself.

## Current Step

The self-use round closure precondition 6 requires. Every queue item is consumed, so
`generate_and_append_if_empty` runs FIRST and appends the tier-1 item; that item is then planned
and RUN through `run_next_self_use_item` to the normal approval gate under a real provider, never
applied, with its `consumed_by` left EMPTY for the closure commit to set. The run's evidence and
whatever `describe_self_use_run_defects` returns are recorded verbatim. It also books round 18's
PASS verdict and the two R-0819 recurrences that round's gates earned.

## Next Steps

1. Register, as normal R-id findings, every string `describe_self_use_run_defects` returned for
   the self-use run — or record that it returned the empty tuple, which means nothing to register
   rather than nothing checked. This is the first commit of the closure round.
2. The ledger rotation by `scripts/rotate_live_review.py`, as its own commit, after the verdict
   bookings and before the STATUS flip.
3. The evidence job and the fresh review zip. The zip's `base_commit` is the FORK POINT
   `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain `rev-list` counts are
   EQUAL — never `git merge-base`, which names `origin/main`'s tip here and gives unequal counts.
4. The closure commit: the STATUS `[x]` flip, the README sync and the one `consumed_by` edit in
   ONE commit; then the pull request, which is NOT merged this session.

## Risks

- The map was blind twice and is fixed once: R-0834's file-type blindness is closed, R-0832's
  event-name coupling is OPEN. Treat every "zero edges" reading as a claim about the WALKER.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12.
- The self-use run needs a REAL provider: `run_next_self_use_item` refuses to run unflagged when
  role config resolves to `fake`. Role config resolves `builder` and `reviewer` to `ollama`.
