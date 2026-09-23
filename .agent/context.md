# Context — amendment amend0923-selfuse-write

## Active Branch
feature/amend0923-selfuse-write, cut from `origin/main` at `64cffc44`
(the merge commit of pull request 268, F263's closure).

## Scope
Operator amendment amend0923-selfuse-write, 2026-09-23, run by the
operator's delegate with full operator authority. Two halves: the
self-use track's ability to deliver (R-1043, R-1044) and the repository
root's hygiene (R-0829). R-1045 is registered here and owned by F282.

## Do not touch
The reviewer's write mode, which `_build_provider_evidence` in
`packages/orchestration/pingpong_loop.py` hard-codes to `none`; the
approval gate; `scripts/self_use_queue.json`, whose SU-028 was queued
before the order file declared a budget.

## Active assumptions
- The self-use builder works in an isolated worktree under `.remedy-wt/`
  and its output still passes the human approval gate, so a write tool
  there widens nothing that was not already gated.
- `parse_job_file` ignores every line before the first `## Task` heading,
  so a `Budget:` line in an order file is invisible to the planner.

## Constraints
- Never rewrite history, never force-push, never `git stash`, never `rm`.
- Every fix gets a red proof: the red side is run and recorded BEFORE the
  fix is applied.
- No assertion is weakened to reach green. A test that pinned a decision
  this amendment changes is updated and named in the handback; that is the
  decision changing, not the assertion weakening.
- Every judgment call is a dated, reversible `DECISION
  amend0923-selfuse-write D<n>` paragraph in `.agent/decisions.md`.
- Resource safety binds here as everywhere: never two pytest processes
  alive at once, every long pytest run bounded by a timeout, and no
  `pkill -f` pattern that could match the running shell itself.

## Steps
The item-status table lives in the handback at
`~/.remedy-loop/amend0923-selfuse-write.handback.md`.
