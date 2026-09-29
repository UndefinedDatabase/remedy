# Plan — operator amendment amend0929b-reclaim-default

Branch: feature/amend0929b-reclaim-default, cut from `main` at `2940ffd8`
(the merge commit of pull request 296, amend0929-context-hygiene).

## Goal

Restore the default of `remedy data reclaim` as it was at `4e643440`:
finished jobs' staging copies are candidates at any age. Remove `--stale`
and `data.staging_ttl_days` (DECISION amend0929b D1).

## Current Step

Part 1: tests first, then the restore, the doctor warning's two commands
and the closure step's two commands.

## Next Steps

1. Part 2: check the F042 branch's context file.
2. Part 3: report the ledger residue, read-only.
3. Part 4: gates, pull request, merge, carry `main` into the F042 branch.

## Risks

None known. The restore goes back to a shape that shipped until 2026-09-29.
