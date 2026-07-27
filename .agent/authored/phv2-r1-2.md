Purpose: the fast-resume snapshot for the planner/reviewer. Rewritten
(never appended) by the worker at every handback; only the latest state;
≤60 lines (≤100 when per-commit tables of >5 commits require it —
sections are never dropped); git history is the archive. Contents:
feature + round, branch, last commit SHAs, changed-files table,
verification results (real, trimmed), open findings count, next expected
action.
