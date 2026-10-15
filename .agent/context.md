# Context — amend1014b-pi-default-repeatable-do

## Active Branch
feature/do-golden-path (its pull request is open, not merged). F078 parked on feature/f078-autonomy-levels; untouched.

## Scope
Pi as default builder/reviewer/repair harness (local Ollama muse-glimmer:latest), the dirty working
tree as the job baseline, `target_changed_during_run`, empty-diff pass rejection, health chain, docs.
No SDK embedding, no daemon, no data-model redesign (one bounded `start_baseline` field).

## Do not touch
`.agent/STOP`, the F078 branch, `no_file_changed`, apply approval, scope guards, non-human content policy.

## Constraints
- Structure ratchet: listed functions may not grow. One test run at a time (`scripts/remedy_pytest.sh`).
- Real acceptance A to E use isolated fixtures and data roots under `/home/decodeux/.remedy-wt-probe`.

## Steps
Commits B1 to B6 and the repairs after them are the steps of this branch; the item-status table
(D1 to D7, tests 1 to 18, acceptances A to E) lives in the handback, `.agent/handoff.md`.
