# Plan — execution excellence (operator order 2026-10-17, after PR 359 and PR 352)

## Goal
Trivial orders stay trivial, a small change over a few files is one job, verification is
truthful across packages, every model call counts against the budget, and an order's jobs are
readable and controllable through the public API. Worktree `.remedy-wt/exec-excellence`, branch
`feature/execution-excellence` from main `6933bb0` (PR 352 merged), outside the roadmap queue (F078
stays next). `.agent/STOP` stays; no deploy.

## Current Step
Done on the branch: verification readings, Pi call accounting and context, the bounded lane over a
few named files, the order's jobs over the public API, review report fields, the digest's ended
stop, scale matrix v3, docs, decisions exec-1017b D1–D5. Now: one full local gate, then the PR.

## Next Steps
- PR (not merged: the operator decides and deploys).
- Operator: optional bounded real Pi run of corpus `lab-*` and `small-multi-file-*` in remedy-lab.

## Risks
- One task over up to three files leans on the local builder doing all of them; the reviewer and
  the handoff coverage gate still fail a missing file.
- Pre-existing, not this branch: `test_claude_cli_no_changes` is red when run alone (green in the suite).
