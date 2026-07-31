- Resolved: R-0160 (process, Low) 2026-07-31: the worktree-only
  mutation rule is now role-symmetric — planner_reviewer_prompt.md
  §4 item 10 binds EVERY role (worker and reviewer alike) and the
  split_workflow.md worker bootstrap carries the matching bullet:
  mutation red-proofs and any other deliberately destructive
  verification run ONLY inside disposable git worktrees, and the
  primary checkout satisfies git status --porcelain == empty at
  every handback and every verdict. Honest-conduct note preserved:
  the F053 worker reverted cleanly and reported; the defect was
  the rule's asymmetry, not the worker.
  Done: R-0160 (commit 392abe48 — Items 1–3 doc codification).
