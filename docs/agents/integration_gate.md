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
   merge base; same records; `base_failed.txt`. Create the worktree ON
   a throwaway BRANCH (`git worktree add -b tmp/base-gate <path>
   <merge-base>`): the self-dogfood branch guard refuses a detached
   HEAD by design, so a detached base worktree fails the
   guard-dependent ids (DECISION D3, F053 R2 review, 2026-07-31).
   Remove + prune the worktree (and delete the tmp branch) and prove
   with `git worktree list`. Gate evidence files use `.txt` names,
   never `.log`: `.gitignore` drops `*.log` silently and the
   review-zip guard rejects any `\.log$` member (R-0169, F069 R3
   deviation 1). Run logs are written OUTSIDE the repo worktree
   while a suite runs (the session scratchpad) and copied into the
   `.agent/gate_*` evidence dir only after the run exits: a log
   growing INSIDE the repo during the run changes the worktree
   digest mid-run and fails the manifest-identity ids as false
   positives (R-0176, F071 R3: four false failures in
   test_run_manifest_logical_identity and
   test_job_rerun_workspace_identity from an in-repo log).
3. **Compare.** `comm -13 base_failed.txt branch_failed.txt` = branch-only
   failures. Report `comm -23` too — failures the branch fixed.
   Environment-coupled base failures (R-0155 amendment, operator
   approved 2026-07-30; path corrected per R-0158): the throwaway
   base worktree lacks artifacts the suite needs — build outputs
   (`apps/ui/node_modules`, `apps/ui/dist`; the ROOT `node_modules`
   holds only a `.vite` cache). Affected ids fail at base and land
   in `comm -23` on every gate run — where a GENUINE base failure in
   those same files would be masked. Therefore: either restore
   parity before the base run (COPY the primary checkout's
   `apps/ui/node_modules` and `apps/ui/dist` into the base
   worktree — never symlink them: the UI auto-build runs
   npm install and writes THROUGH a symlink into the primary
   checkout (F053 R3 evidence); `REMEDY_UI_NO_AUTO_BUILD=1` is set
   for the base run but NOT trusted alone — a spawned build path
   ignored it once (R-0169, F069 R2: dist/ rewritten mid-run).
   VERIFY the neutralization: hash `apps/ui/dist` before and after
   the base run; a changed hash voids the parity claim and forces
   per-id attribution; or run the same install/build there), or
   attribute
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
