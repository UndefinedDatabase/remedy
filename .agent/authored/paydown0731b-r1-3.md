10. Mutation/red-proof spot-checks (temporarily breaking code to prove a
    test catches it) are encouraged — but ONLY inside a disposable
    `git worktree` at HEAD, never in the primary checkout. This
    binds EVERY role — worker and reviewer alike (R-0160 fix,
    operator ruling 2026-07-31): mutation red-proofs and any other
    deliberately destructive verification run ONLY inside
    disposable git worktrees, and the primary checkout satisfies
    `git status --porcelain` == empty at every handback and every
    verdict. State in the operator brief when a mutation check
    ran. The read-only rule (§0) is unchanged: such worktrees are
    throwaway verification scratch space, removed and pruned before
    the verdict (`git worktree list` proof on request).
