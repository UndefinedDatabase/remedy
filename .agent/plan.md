# Plan — F015 Interactive plan editing

Branch: feature/f015-interactive-plan-editing, cut from `main` at
`fce49ce0`, the merge commit of pull request 273 (F267 List commands v2
completion).

## Goal

The human reshapes a job's task plan before approving it: six edit
commands, valid only while the plan's approval is open, each revalidated
and logged, reachable through the write channel and `remedy job plan-*`,
and execution follows the edited plan exactly, proven by hash
(`docs/roadmap/features/T5_F015.md`). Open findings: 4, all owned by F284.

## Current Step

ROUND 6 BLOCKED at G3. C1-C4 committed (book round 5's PASS, repair the
two bad nodes — `runtime stop` waits out a supervisor that has recorded
its application's exit, and the CLI subprocess hang guard is 30 seconds).
G3's serial selection came back `2 failed, 833 passed, 1 skipped` at exit
1, not the reviewer's `833 passed, 3 skipped` at exit 0: `doctor.main()`'s
secrets scan (`tests/test_agent_tooling.py`) walks into two unrelated live
worktrees, `.claude/worktrees/agent-a31862c9188a3670b` and
`.claude/worktrees/agent-af90a3c16d4bb4c65`, and flags ordinary source
text there as possible secrets. Per the block's constraint 4 this STOPS
the round before G4/C5; those worktrees are explicitly protected
(constraint 6) and are not this round's to repair.

## Next Steps

1. The review of round 6's blocked state; a fix or an accepted-cause
   ruling for the `.claude/worktrees/*` false-positive is needed before
   G3 can pass again.
2. Once G3 is green: G4, then C5 (UI build + full suite + handback).
3. The closure sequence's evidence half: the evidence job built against
   the fork point, and the fresh review package.
4. The closing round: book the evidence round, rotate the ledger, flip
   F015's STATUS line with its README pins, and open the pull request.

## Risks

- A bad node the re-run still lists takes another repair round, at most
  two more, under operator amendment amend0917-throughput rule 2.
- The `.claude/worktrees/*` secrets-scan false positive may recur on the
  next attempt if those worktrees are still present.
