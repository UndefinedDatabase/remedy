# Plan — paydown0814 closure debt

Branch: feature/paydown0814-closure-debt, cut from main at 1e7f7bca after the
F045 closure PR #197 merged. Next free finding id: R-0362. R-0359 and R-0360
are FIXED and RESOLVED by the reviewer at bc0f5223; R-0361 stays open as a
recorded reviewer-process finding whose counter-measure is already in force.

## Goal
Pay down the debt the F045 closure carried out on disk, so the next feature
starts on a green `main`: trim `docs/agents/reviewer_conventions.md` under its
800-token prompt-segment cap (R-0359), pin the README tier table's Done column
to the ledger (R-0360), and record the gate round's own finding (R-0361). A
paydown branch in the established shape of feature/paydown-0730, -0731, -0731b
and -0801 — it claims no STATUS line and closes no `[ ]`.

## Current Step
R3 complete: the reviewer re-ran every R2 gate itself, including its own
red-proof in a disposable worktree, issued PASS, and its authored `Done:`
resolutions for R-0359 and R-0360 are now on disk in `.agent/live_review.md`.
PR #198 is still NOT merged.

## Next Steps
1. R4 — Open PR Gate: merge PR #198 with
   `gh pr merge 198 --merge --delete-branch`, then `git checkout main` and
   `git pull --ff-only`. That merge is what finally turns `main` green, and it
   closes the operator's manual-review window.
2. Then F057 — Rate-limit-aware scheduler, per Rule A5 and STATUS order. New
   session, new branch, cut from the merged `main`.

## Risks
- `main` is RED until PR #198 merges. The five
  tests/orchestration/test_role_conventions.py ids are green on this branch,
  which is the fix's proof, but `main` itself only turns green at the merge.
- R-0361 remains open by design. Its counter-measure — a block may only order
  a command the reviewer has itself executed — was applied again in R3.
