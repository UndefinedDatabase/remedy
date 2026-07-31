- Mutation red-proofs and any other deliberately destructive
  verification run ONLY inside disposable git worktrees — never in
  the primary checkout; git status --porcelain == empty at every
  handback (R-0160 fix, operator ruling 2026-07-31; the same rule
  binds the reviewer in planner_reviewer_prompt.md §4 item 10).
