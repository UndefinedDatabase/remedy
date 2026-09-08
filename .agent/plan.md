# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered, the integration
gate has PASSED and the self-use precondition is met; the close is BLOCKED by R-0837 until this
round lands its fix.

## Current Step

The R-0837 repair. `create_manual_completion_bundle` builds its attestation authority set from
every attestable changed path, including one this branch DELETED, then requires both that the task
partition cover that set exactly and that each task's safe diff yield exactly its own paths — which
a deleted file's safe diff never does. The two checks are jointly unsatisfiable, so the canonical
closure evidence producer refuses every deletion feature, and F274 and F275 are both one. This
round guards the comprehension with `f.current_sha256`, the idiom the same function already uses
twenty lines below it for `file_hashes`, and ships a regression test that goes red without it. Its
ledger commit books round 19's PASS verdict, registers R-0837 and R-0838 and appends the R-0784
recurrence.

## Next Steps

1. CLOSURE ROUND A: the ledger rotation by `scripts/rotate_live_review.py` as its own commit, then
   the evidence job and the fresh review zip. The zip's `base_commit` is the FORK POINT
   `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain `rev-list` counts are
   EQUAL — never `git merge-base`, which names `origin/main`'s tip here and gives unequal counts.
2. CLOSURE ROUND B: the STATUS `[x]` flip, the README sync and the one `consumed_by` edit setting
   `SU-013` to `f274`, in ONE commit; then the pull request, which is NOT merged this session.

## Risks

- The authority set is read from the WORKING TREE and not from the commit, so an untracked `.py`
  file under the repo root joins it and shifts every count the closure round reports. The tree is
  clean before the evidence job runs, and closure round A gates that first.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12. The integrity gate's `high_blockers_open` check reports "no
  open blocker/high findings" and is WRONG while those four are open — that is R-0648, and
  DECISION F272 D17 requires the close to say so and to rest on the named list instead.
