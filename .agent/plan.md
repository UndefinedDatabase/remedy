# Plan — paydown0814 closure debt

Branch: feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the
F045 closure PR #197 merged at this session's Open PR Gate. Next free finding
id: R-0362. Findings R-0359, R-0360 and R-0361 are registered; R-0359 and
R-0360 are FIXED on disk and awaiting the reviewer's authored resolution.

## Goal
Pay down the debt the F045 closure carried out on disk, so the next feature
starts on a green `main`: trim `docs/agents/reviewer_conventions.md` under its
800-token prompt-segment cap (R-0359), pin the README tier table's Done column
to the ledger (R-0360), and record the gate round's own finding (R-0361). A
paydown branch in the established shape of feature/paydown-0730, -0731, -0731b
and -0801 — it claims no STATUS line and closes no `[ ]`.

## Current Step
R2 complete: both fixes committed, gated and pushed, the new pin red-proved in
a disposable worktree, and the PR opened. The PR is NOT merged this session
(docs/agents/self_drive_protocol.md G1); it merges at the next session's Open
PR Gate, which is the operator's manual-review window.

## Next Steps
1. The reviewer re-runs every gate, authors the `Done:` resolutions for R-0359
   and R-0360, and issues the round verdict. R-0361 stays OPEN as a recorded
   reviewer-process finding whose counter-measure is already in force.
2. Next roadmap feature per Rule A5 and STATUS order: F057 — Rate-limit-aware
   scheduler. New session, new branch, after this PR merges.

## Risks
- `main` stays RED until this PR merges. The five
  tests/orchestration/test_role_conventions.py ids are green ON THIS BRANCH,
  which is the fix's proof, but `main` itself only turns green at the merge.
- The conventions trim is a content decision: every rule survives, and the
  Discoverability section now POINTS at AGENTS.md instead of restating it.
  Reversing that choice means restoring the prose and re-breaking the cap.
