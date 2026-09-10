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

ROUND 45 repairs a RED BRANCH TIP the reviewer caused. The guard round 44 landed for R-0875
sweeps every tracked `*.py` file for a keyword its model does not declare, and its own
premise test wrote one literally, so once tracked the guard reported itself — §3 item 2, a
zero-gate counting a string the same block writes into the file the gate reads. The premise
now passes its keywords as a `**{...}` splat, which the sweep skips for the right reason, and
a new test pins that this file is itself swept so no per-file exemption can arrive later.
The round 44 FAIL verdict is booked here. No id is minted and none resolved.

## Next Steps

1. Author `Done: R-0875` at the next gate, once round 45's own gates have shown the repair
   works — the scheduling §3 item 31 requires, and the reason the `Landed:` line still
   stands.
2. THE FLIP. Its target API exists (round 42), its record shapes are measured (round 43), its
   construction mapping is ruled (DECISION F275 D25) and its tree is clean (round 44). The
   dry run measured it at 284 files and 4856 insertions, declared before review as the one
   oversize commit AGENTS.md permits per feature. It also registers
   `Task.acceptance_checks`'s structured form as a finding naming the feature that owns
   acceptance criteria, per amend0908-f275-finish rule 4.
3. The resolver collapse DECISION F260 D5 places in T003, with the classic store, which is
   the same commit range by that decision's own terms. Then the closure sequence: the
   integration gate, the evidence job, a fresh review zip, the ledger rotation, the STATUS
   line and the PR.

## Risks

- A guard added in the same commit as the cleanup it guards must be red-proved as a TRACKED
  file. Round 44's was proved untracked, where `git ls-files` cannot see it, and that is the
  whole of this round's cause.
- The open set is 87 by distinct id at this round's base `123a0c3f`. Four are High — R-0803,
  R-0804, R-0806 and R-0807 — all F273's, per DECISION F272 D12.
