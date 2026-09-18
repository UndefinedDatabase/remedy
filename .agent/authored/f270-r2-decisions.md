
## DECISION F270 D2 (2026-09-18, reviewer, round 2) — `job apply --approve --commit-with-history` merges the job branch, and its refusals
CONTEXT: `docs/roadmap/features/T2_F270.md` T002 and T003 ask for a `--no-ff` merge of the job
branch onto the operator's current branch after a clean-tree check, refused on conflict with the
conflicting paths and no file overwritten (DECISION F263 D-E), and refused for a staging target.
Measured at `ff9d56a2` by a research helper's prototype in a disposable worktree, which the
reviewer read: `apply_job` in `packages/orchestration/job_apply.py` runs its gates (job and tasks,
target guard, manifests, file coverage, blocked paths, baseline, modes, record preflight), then
copies files rebuilt from `result.diff`, then verifies them, and writes one record under
`job_apply_records/`; a blocked apply exits 0; the job stores `job_initial_tree` and
`result_diff_sha256` but no final tree; and the baseline gate already refuses any operator change,
committed or not, to a path the job writes, so such a hand edit never reaches git at all.
CHOSEN: (1) THE FLAG. `--commit-with-history` on `job apply` needs `--approve`; without it the
command previews as today, the preview naming the flag and every refusal the real run would meet.
Every existing gate runs unchanged and in its present order; the merge replaces only the copy of
files, and the post-apply verification and post-test run after it as they run after a copy. (2)
REFUSALS, each one sentence, each changing nothing on disk, checked after the existing gates and
again immediately before the merge: the job ran in copy mode (a staging target) — nothing is
copied and the sentence says a plain `--approve` copies; the target is not a git repository; the
operator's checkout is on a detached `HEAD`; `git status --porcelain --untracked-files=all` in the
target prints anything — the sentence names the paths; `--skip-blocked` is given, or a file the
copy would skip exists, because a merge cannot leave a path out; the job branch is missing, its
tip is not the job's `worktree_head`, or the sha256 of the diff from `job_initial_tree` to the
tip's tree is not `result_diff_sha256` — the branch is then not the reviewed work. (3) THE MERGE.
`git merge --no-ff --no-log` of `remedy/job-<job id>` in the target, under the operator's own git
identity, configuration and hooks. Message: first line `Merge the <n> task commits of Remedy job
<first eight characters of the job id>` (at most 72 characters); a blank line; one body sentence
naming the branch and the operator's branch; a blank line; the contract line of DECISION F270 D1
(3); a blank line; the trailers `Remedy-Job: <job id>` and `Co-authored-by: Remedy
<remedy@local>`. (4) A MERGE THAT FAILS — a conflict or a refusing hook — is aborted with `git
merge --abort`; `HEAD`, the index and every file are then what they were before, and the refusal
names the paths git reports unmerged, or quotes the hook's own output. Remedy never runs `git
reset` on the operator's branch. (5) AFTER A MERGE, a failed post-apply verification or post-test
is reported with the merge commit's sha and the operator's previous tip, so the operator can undo
it with one command; Remedy undoes nothing itself. (6) THE RECORD. The apply record gains
`commit_with_history`, `merged_branch`, `target_branch`, `history_commits`, `merge_commit` and
`merge_conflicts`; the summary of a merged apply names the commit count, both branches and the
merge commit and says that nothing was pushed, and the summary line "No commits or pushes were
made" stays for an apply without the flag, where it is still true. (7) EXIT CODES stay as they
are: a refused apply is a blocked apply and exits as one does today. (8) THE HAND EDIT OF F263
D-E is proved twice: a committed operator edit to a file the job writes is refused by the
baseline gate before any merge and stays intact; a real git conflict, which the file gates cannot
see (the job writes `pkg/mod.txt`, the operator commits a file named `pkg`), is aborted by (4).
ALTERNATIVES: letting the flag imply `--approve`, rejected because the approval semantics are on
the feature's Do-not-touch list; relaxing the baseline gate so git decides every overlap,
rejected because it weakens a gate; resetting the operator's branch after a failed post-test,
rejected because Remedy never rewrites the operator's branch; storing the final tree on the job,
rejected because the diff hash already binds the branch to the reviewed work. REVERSE: remove the
flag, the merge path and its record fields, and delete this paragraph; `job apply` copies as
before.
