# Integration Gate — Canonical Procedure

> The full-suite gate run before feature closure
> (planner_reviewer_prompt.md §3, tier 3). Paste blocks reference this
> file instead of restating it. Only the reviewer issues the gate verdict;
> only the gate entry may carry the "full suite" claim.

1. **Branch run.** From the repo root:
   `python3 -m pytest -n auto -q`
   Record: raw tail, full FAILED list, exit code, wall time.
   `grep '^FAILED' <log> | sort > branch_failed.txt`
2. **No base run (amend0917-throughput, 2026-09-17).** The base is main
   at the merge base, and the hosted CI record of that commit is the only
   base evidence; no base worktree, base run or compare step exists. Every
   branch failure is the feature's unless that record shows the same node
   red. Gate evidence files use `.txt` names, never `.log`, and run logs
   are written outside the repo worktree while the suite runs and copied in
   only after it exits (R-0169, R-0176).
3. **Attribution — for EVERY branch-only id.** Serial re-run of the exact
   node id. Classify (F046 pattern):
   - serial-pass ⇒ xdist-flake class (F135/F052); record, not a blocker.
   - serial-fail ⇒ reproduce at the merge base before blaming the
     feature.
   - a reproducible branch-only failure coupled to feature code =
     BLOCKER: STOP, hand back — the fix is its own reviewer-gated round.
4. **Verdict & budget.** Only the reviewer issues the gate verdict. Wall
   clock over ~5 min ⇒ note for a perf pass.
