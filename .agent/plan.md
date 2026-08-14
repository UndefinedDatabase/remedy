# Plan — paydown0814 closure debt

Branch: feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the
F045 closure PR #197 merged at this session's Open PR Gate. Next free finding
id: R-0362. Open findings: 3 — R-0359 (Medium), R-0360 (Low), R-0361 (Low).

## Goal
Pay down the debt the F045 closure carried out on disk, so the next feature
starts on a green `main`: trim `docs/agents/reviewer_conventions.md` under its
800-token prompt-segment cap (R-0359), pin the README tier table's Done column
to the ledger (R-0360), and record the gate round's own finding (R-0361). A
paydown branch in the established shape of feature/paydown-0730, -0731, -0731b
and -0801 — it claims no STATUS line and closes no `[ ]`.

## Current Step
R1: the state reset, the three registered findings and the emptied
`.agent/candidates.md`, committed and pushed. No fix lands this round — the
findings persist FIRST so nothing is lost if the session dies.

## Next Steps
1. R2 — trim the conventions document under the cap WITH headroom, and add the
   README tier pin, each in its own gated commit.
2. R2 — red-proof the new pin inside a disposable git worktree, rewrite the
   handoff, push, open the PR. The PR is NOT merged this session
   (docs/agents/self_drive_protocol.md G1).
3. Next roadmap feature per Rule A5 and STATUS order: F057 — Rate-limit-aware
   scheduler. New session, new branch, after this PR merges at that session's
   Open PR Gate.

## Risks
- `main` is RED until this branch merges: five
  `tests/orchestration/test_role_conventions.py` ids fail at 1e7f7bca. Round
  gates are therefore scoped, and those five going GREEN is R-0359's own proof.
- The README pin passes on arrival, so it proves nothing without a red-proof;
  that proof runs only in a disposable worktree (self_drive_protocol.md G5).
- Trimming a reviewer-facing rules document is a content decision. The trim
  keeps every rule and is recorded as such; a lost rule would be a finding.
