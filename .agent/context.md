# Context — amend1014c-review-closure-before-merge

## Active Branch
feature/do-golden-path (PR #339 open, product-review BLOCKED, not merged). The replacement branch
feature/do-golden-path-review-closure is created at the end, from main, by replay. F078 untouched.

## Scope
R1 to R3 repairs of the Pi golden path, their tests, the real acceptance A to E, docs, then the no-force
history replacement. No new roadmap feature; no merge.

## Do not touch
`.agent/STOP` (untracked), the F078 branch, `no_file_changed`, apply approval, scope guards, the
non-human content policy.

## Constraints
- Structure ratchet: listed functions may not grow. One test run at a time (`scripts/remedy_pytest.sh`).
- Every commit at most 500 insertions. No rebase, reset, amend or force-push.
- Real acceptance uses fresh fixtures and isolated data roots under `/home/decodeux/.remedy-wt-probe`.
