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
4. **Attribution — for EVERY branch-only id.** Serial re-run of the exact
   node id. Classify (F046 pattern):
   - serial-pass ⇒ xdist-flake class (F135/F052); record, not a blocker.
   - serial-fail ⇒ reproduce at the merge base before blaming the
     feature.
   - a reproducible branch-only failure coupled to feature code =
     BLOCKER: STOP, hand back — the fix is its own reviewer-gated round.
5. **Verdict & budget.** Only the reviewer issues the gate verdict. Wall
   clock over ~5 min ⇒ note for a perf pass.
