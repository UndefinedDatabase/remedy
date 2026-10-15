# Plan — amend1014c-review-closure-before-merge

## Goal
Operator amendment amend1014c (2026-10-15): repair the four review findings of PR #339 (R1 secret
persistence, R2 Pi timeout floor, R3 call accounting, R4 a 643-insertion commit), prove each with
tests and the real acceptance A to E, then replace the PR by the no-force procedure. Not a merge.

## Grouped findings (review channels of #339: empty)
- R1 HIGH: the baseline seeded and committed every dirty path (a `.env` reached a job branch). Fix:
  seed only the job's deliverable paths, one name-only classifier (`sensitive_paths.py`) shared with
  apply and the context pack, sensitive pathspecs excluded from the target-state snapshot, sensitive
  order targets refused before any worktree or provider call.
- R2 MEDIUM: `PI_MIN_WALL_SECONDS` raised explicit timeouts to 900 s. Fix: Pi default 900 s only when
  none was set (`provider_timeouts`), explicit value, remaining job wall budget and deadline are
  ceilings, minimum wins, provenance in the call record.
- R3 MEDIUM: ledger "calls" are Pi processes. Fix (fallback path, the ledger keys rows by attempt):
  rename the count to `harness_invocations` on do, digest, cockpit, contract, UI; add `model_turns`
  from Pi's own call records.
- R4: replay history with every commit at most 500 insertions (end of this order).

## Current Step
Code and focused tests are green; next: commit in small steps, fast lane, real acceptance A to E,
review, one final full suite, then the replacement branch `feature/do-golden-path-review-closure`.

## Next Steps
1. Commit R1 to R3 repairs (each at most 500 insertions), push `feature/do-golden-path`.
2. Real acceptance A to E, `remedy-review`, final full suite on the exact tree.
3. Close PR #339, replay on the new branch, enumerate insertions, open the replacement PR. No merge.

## Risks
- `.agent/STOP` untracked and untouched; F078 branch untouched.
- `remedy cost` and `remedy stats` keep ledger-level `calls` columns (recorded as a deviation).
