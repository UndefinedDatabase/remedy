# Plan — F275 One world completion, part three

Branch: feature/f275-one-world-completion-part-three, cut from `main` at
`a5bf894946ab6de053a4232109d6341a63533768`, the merge commit of pull request 246.

## Goal

Finish what F274 could not reach inside its own limit: the two carry-overs F260's Design
names, DECISION F260 D3, the prototype-cluster deletion itself, the atomic record flip that
T002 rules but does not perform, and the classic runner. Operator ruling amend0908-f275-finish
orders T001 PERFORMED, not prepared. T001 and T002 are DONE, and the classic runner's whole
command surface is gone as of round 34.

## Current Step

ROUND 42 widens the UNIFIED STORE with the three capabilities the classic store has and it
lacked, measured by applying the flip in a disposable worktree and running it: a jobs-root
override, which 186 classic call sites pass and `data_paths.job_record_path` already
accepted; corruption visibility, which four production sites read off
`storage.load_job_safe`; and listing, which seventeen call sites use and the unified store
did not offer at all. DECISION F275 D23 records why this precedes the flip rather than
riding inside it. Green by construction — no consumer moves.

## Next Steps

1. The flip itself, now that its target API exists: applied from the round 36 site
   enumeration and the round 38 seam list, as the one declared-oversize commit AGENTS.md
   permits per feature, with the inseparability reason AND the real size stated in the
   handback BEFORE review. The `Job` type sites DECISION F275 D21 counts as part (c) and
   the `Task` type sites DECISION F275 D22 counts have no committed per-site enumeration,
   so that round either enumerates them first or states that it applied them from a
   measurement taken in its own worktree.
2. The resolver collapse DECISION F260 D5 places in T003 — `resolve_any_job_id`, the "TWO
   job stores" paragraph, every which-store branch and the absence test — with the classic
   store, which is the same commit range by that decision's own terms.
3. The closure sequence: the integration gate, the evidence job, a fresh review zip, the
   ledger rotation, the STATUS line and the PR.

## Risks

- Step 1 is the largest single commit this repository will take, and every round that
  measures it has found it larger: DECISION F275 D17 sized it at 1766 changed lines, D21 at
  3771 across 263 files, D22 added a type pair worth 427 more, and D23 found that three
  pieces of its target API did not exist.
- The open set is 86 by distinct id at this round's base `77a7d840`. This round registers
  none and resolves none. Four are High — R-0803, R-0804, R-0806 and R-0807 — all F273's,
  per DECISION F272 D12.
