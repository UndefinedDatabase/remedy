- R1: PASS (reviewer, 2026-07-31). Range b63f9665..168f9890. All 9
  authored texts cmp 0 disk-to-disk against the reviewer scratchpad
  originals; every payload verified exactly once at its anchor in
  the committed files (python count proof). Reviewer's own gate
  runs: tests/docs 293, canary 42, touched test files 30 (24 unit +
  6 CLI). R-0159 repro killed in a throwaway linked worktree at
  HEAD on a branch (.git gitfile → 6/6 CLI ids green); negative
  control: a DETACHED worktree still fails the 2 guard-dependent
  ids — the guard refuses detached HEAD as before, so the fix is
  additive and default-preserving. Worktree removed + pruned.
  Ledger: R-0159 Resolved (23a06611 + 21aa8e88), VT run_id
  candidate resolved inline as DECISION D1 (408c89c9), no ID spent,
  next free ID R-0160. Merge same-session per standing operator
  approval (2026-07-31). LAST_REVIEWED_SHA = 168f9890.
