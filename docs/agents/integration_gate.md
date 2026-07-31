# Integration Gate — Canonical Procedure

> The full-suite gate run before feature closure
> (planner_reviewer_prompt.md §3, tier 3). Paste blocks reference this
> file instead of restating it. Only the reviewer issues the gate verdict;
> only the gate entry may carry the "full suite" claim.

1. **Branch run.** From the repo root:
   `python3 -m pytest -n auto -q`
   Record: raw tail, full FAILED list, exit code, wall time.
   `grep '^FAILED' <log> | sort > branch_failed.txt`
2. **Base run.** Identical command in a throwaway `git worktree` at the
   merge base; same records; `base_failed.txt`. Remove + prune the
   worktree and prove with `git worktree list`.
3. **Compare.** `comm -13 base_failed.txt branch_failed.txt` = branch-only
   failures. Report `comm -23` too — failures the branch fixed.
   Environment-coupled base failures (R-0155 amendment, operator
   approved 2026-07-30; path corrected per R-0158): the throwaway
   base worktree lacks artifacts the suite needs — build outputs
   (`apps/ui/node_modules`, `apps/ui/dist`; the ROOT `node_modules`
   holds only a `.vite` cache). Affected ids fail at base and land
   in `comm -23` on every gate run — where a GENUINE base failure in
   those same files would be masked. Therefore: either restore
   parity before the base run (share or copy the primary checkout's
   `apps/ui/node_modules` and `apps/ui/dist` into the base
   worktree, or run the same install/build there), or attribute
   EVERY `comm -23` id to the environment class by direct evidence
   (the missing artifact named per id). An unattributed `comm -23`
   id counts as a genuine base failure and blocks the gate verdict.
   (The former non-restorable `.git`-directory class is gone: since
   the R-0159 fix the self-dogfood guard accepts a linked worktree's
   `.git` gitfile pointer.)
4. **Attribution — for EVERY branch-only id.** Serial re-run of the exact
   node id. Classify (F046 pattern):
   - serial-pass ⇒ xdist-flake class (F135/F052); record, not a blocker.
   - serial-fail ⇒ reproduce at the merge base before blaming the
     feature.
   - a reproducible branch-only failure coupled to feature code =
     BLOCKER: STOP, hand back — the fix is its own reviewer-gated round.
5. **Verdict & budget.** Only the reviewer issues the gate verdict. Wall
   clock over ~5 min ⇒ note for a perf pass.
