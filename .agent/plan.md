# Plan — F274 One world completion, part two

Branch: feature/f274-one-world-completion-part-two, cut from `main` at
`13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, with `main` merged back in at `f85200e4` to take
operator amendment amend0907-cluster-first.

## Goal

Close F274 at the edge work it actually built and carry the cluster deletion, the atomic record
flip and the classic runner to F275, per DECISION F274 D8. F275 is registered, the integration gate
has PASSED and the self-use precondition is met; the close is BLOCKED by R-0837 until BOTH of its
sites are guarded.

## Current Step

R-0837's SECOND SITE. Round 20 guarded the evidence producer and it now builds, but the reviewer
dry-ran the whole closure package before authoring the closure round and the MANDATORY review zip
still refuses this branch: `scripts/build_review_zip.py` recomputes the attestable set
independently, without the `current_sha256` guard, and then requires it to EQUAL the authority set
the producer wrote. The two comprehensions are one rule with two spellings, so narrowing one side
alone converts a producer failure into a packager refusal. This round applies the same conjunct at
the second site and ships a two-test regression module — one test for the deleted path, one
discriminator proving a genuinely missing live path STILL blocks — and its ledger commit books
round 20's PASS verdict and appends the second site to R-0837 without minting an id.

## Next Steps

1. CLOSURE ROUND A: the ledger rotation by `scripts/rotate_live_review.py` as its own commit, then
   the evidence job and the fresh review zip, built from a CLEAN tree. The package's `base_commit`
   is the FORK POINT `13dfaabd93d7b6452a1d23ca698e29ed47ecf035`, whose ancestry-path and plain
   `rev-list` counts the reviewer measured EQUAL at 163 — never `git merge-base`, which names
   `origin/main`'s tip `d0d8b24d` here and gives unequal counts.
2. CLOSURE ROUND B: the STATUS `[x]` flip, the README sync and the one `consumed_by` edit setting
   `SU-013` to `f274`, in ONE commit; then the pull request, which is NOT merged this session.

## Risks

- The authority set is read from the WORKING TREE and not from the commit, so an untracked `.py`
  file under the repo root joins it and shifts every count the closure round reports. `pytest` has
  no `norecursedirs` here either, so a leftover worktree under `.remedy-wt/` is collected by a full
  run. The tree is clean and the worktrees are pruned before the evidence job.
- The open High findings are R-0803, R-0804, R-0806 and R-0807, all F273's rather than this
  feature's, per DECISION F272 D12. The integrity gate's `high_blockers_open` check reports "no
  open blocker/high findings" and is WRONG while those four are open — that is R-0648, and
  DECISION F272 D17 requires the close to say so and to rest on the named list instead.
