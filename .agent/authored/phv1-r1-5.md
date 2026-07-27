9. Authored-text application is verified against the committed
   `.agent/authored/<feature>-r<round>-<n>.md` file (the worker's saved
   copy of your paste), never against your own retype. Order the
   disk-to-disk comparison; a proof computed against a reconstructed copy
   is a false verification claim (R-0147 class).
10. Mutation/red-proof spot-checks (temporarily breaking code to prove a
    test catches it) are encouraged — but ONLY inside a disposable
    `git worktree` at HEAD, never in the primary checkout. The primary
    checkout must satisfy `git status --porcelain` == empty when your
    review turn ends; state in the operator brief when a mutation check
    ran. The read-only rule (§0) is unchanged: such worktrees are
    throwaway verification scratch space, removed and pruned before the
    verdict (`git worktree list` proof on request).
