# Plan — amend1014b-pi-default-repeatable-do

## Goal
Operator amendment amend1014b (2026-10-15), closing PR #339 on `feature/do-golden-path`: Pi (local
Ollama `muse-glimmer:latest`) is the default builder/reviewer/repair harness and a dirty working
tree is the captured baseline, so `do ... --apply` then `do ... --commit-auto` run back to back.

## Current Step
Done and pushed: commits B1 to B10, acceptances A to E passed against the real model, the closure
gate ran (1 failure, repaired in B10), the handback is written, PR #339 is updated and not merged.

## Next Steps
1. Operator: review PR #339 and decide on the merge.
2. After the merge, F078 resumes on `feature/f078-autonomy-levels`.

## Review Strategy
PR #339 had no review comments on any channel (checked 2026-10-15).

## Risks
- The tip tree differs from the gated tree by one test assertion (B10); see the handback.
- `.agent/STOP` is untracked and untouched.
