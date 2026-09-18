-- STEP R1 T001 -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 1 · base `b7f966c0` (main, the merge of pull request 257).

Goal: claim F270 and land T001 — one commit per applied task on the job worktree branch
`remedy/job-<job id>`, recorded on the task and resumable without a duplicate.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F270.md; the payload `decisions.md`
(DECISION F270 D1 — this round's spec; where this block is terser, it rules). A REFERENCE, not a
slice: `.remedy-wt/f270-r1/prototype.diff` is a research helper's prototype of D1 without its
trailers, adoption rule and branch refusal; read it, write your own code, and copy nothing blindly.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r1/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 4e8c80bebb5d3f567466be064959a06325cf975af80998acdb720ad94b221898
  context.md           sha256 58a5fc7a1cd1d18b751f42497424b1b69c5a344a90786b0b631b5c1e211431c6
  live_review_head.md  sha256 c03d50a828e662b31f429afc0268d25b98c180f0c33403424b6477fd26e1bf9b
  ledger.md            sha256 8aa11ec22474026af14c17aa34bb08bee92e9f8f794032cdccf9929e4e9d641e
  decisions.md         sha256 23ef23c246e73acf9f8ecc4ac6cc9f6af776979f99097c48875c693dc16317dd
  status_from.txt      sha256 bb165d4a397012af4fd3d610a17c818b6d9934c377cee7d370350cd446eaaa8e
  status_to.txt        sha256 56bc36aefda3c03341b678e180c3c595f9942713d15a6d353d0b14936a66ec1d
  f273_from.txt        sha256 6cace0409493b0c5ab63db62315c22786d1834990482622f85092b05506f3756
  f273_to.txt          sha256 9c8d864e9a96272a50f7400c7e023f0d017824576de1e7749ddf00f602122255
  block.md             this block (save it; report its digest)

Bundle (commit order):
C1 claim — branch `feature/f270-history-apply` from `main` at `b7f966c0` (the reviewer already ran
   the Open PR Gate: it merged pull request 257; zero pull requests are open). One commit holding
   exactly: byte copies of every payload above as `.agent/authored/f270-r1-<name>`;
   `.agent/plan.md` := plan.md; `.agent/context.md` := context.md; `.agent/live_review.md` :=
   live_review_head.md bytes + the old file's bytes from the line `## Findings` (inclusive) to the
   end + ledger.md bytes (it books F269 round 13's verdict and `Done: R-0973`, and registers
   R-0974); `.agent/decisions.md` := old bytes + decisions.md bytes; `docs/roadmap/STATUS.md`: the
   line equal to status_from.txt replaced by status_to.txt (reviewer's containment test:
   `TO contains FROM: False`, a REWRITE — FROM 1x before, 0x after, TO 1x after);
   `docs/roadmap/features/T2_F273.md`: the bytes of f273_from.txt replaced by f273_to.txt
   (reviewer's containment test: `TO contains FROM: True`, an APPEND — FROM 1x before and after,
   and the lines C1's diff adds to that file are exactly the TO-only lines, in order).
C2 the commit on the branch — per D1 (1) to (5): in `packages/orchestration/worktrees.py` the
   commit helper (branch refusal, forced identity, no signing, no hooks, empty commits allowed, a
   timeout on every git call, returns the new sha) and a reader of HEAD's `Remedy-Job` and
   `Remedy-Task` trailers; in `packages/orchestration/pingpong_job.py` the `TaskEntry` field
   `worktree_commit` with its export and import, the message builder, the adopt-or-commit step at
   the seam D1 (1) names, `job.worktree_head` set from it, and the D1 (5) failure path. D1 (6): fix
   the docstrings and doc sentences that say the job worktree is never committed on — at least the
   `head_commit` comment and `retain_for_recovery` in `worktrees.py`, `_finalize_job_workspace`'s
   docstring and comments in `pingpong_job.py`, and lines 124 and 140 of
   `docs/system/first-fulfilled-job-demo-v0.md`; name every sentence you changed in the handoff.
   Split code and tests into C2a/C2b if one commit would exceed 500 inserted lines.
C3 tests — in `tests/orchestration/test_job_worktree_integration.py`, reusing its `repo` fixture
   and `_run_two_task_job`: (t1) a two-task fake run yields exactly two commits above the base on
   `remedy/job-<id>`, subjects `task 1: …` and `task 2: …`, author and committer
   `Remedy <remedy@local>`, the last body line `contract: none`, both trailers; each task's
   `worktree_commit` is its commit, after a reload of the record too; `worktree_head` is the tip;
   the tip's tree is the tree `result.diff` was computed to; the operator's HEAD is unchanged.
   (t2) with the operator's identity set through `GIT_AUTHOR_*`/`GIT_COMMITTER_*` and a
   `pre-commit` hook that exits 1 in the repository, the commits still land as Remedy. (t3)
   adoption: HEAD already carrying this job's and this task's trailers with a clean worktree and
   `worktree_commit` blank → the step adopts HEAD and the branch gains no commit. (t4) the helper
   called on the main checkout raises and the checkout's HEAD and index are unchanged. (t5) the
   message: a title over 72 characters is cut with `...`, and a job whose mission has a contract
   reads `contract: <met> of <total> criteria green` over its slice. (t6) a non-git target commits
   nothing and leaves `worktree_commit` blank. (t7) a helper that raises blocks the job with stop
   reason `task_<id>_worktree_commit_failed`.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F270 · round 1 · rounds so far 1" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id; `## Next` naming Phase 1 rule 1 then the review of
   round 1, and "Operator questions open: <the count you read from the file>". Then
   `git push -u origin feature/f270-history-apply`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F270.md): the apply gate's approval semantics, the snapshot guard
   (`write_tree` is NOT edited — R-0974 is F273's), the worktree lifecycle beyond committing on it;
   `job_apply.py` is not edited this round.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python;
   set environment in tests with `monkeypatch.setenv`.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D1 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` and `docs/roadmap/` file from `git show b7f966c0:<path>` bytes.
6. Commit messages "F270 R1 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C3, before C4; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` and `.agent/context.md` equal their payloads, that `.agent/live_review.md`
   equals head + the `b7f966c0` bytes from `## Findings` + ledger.md, that `.agent/decisions.md`
   equals its `b7f966c0` bytes + decisions.md, that STATUS and T2_F273.md equal their `b7f966c0`
   bytes with the pair applied, and that each `.agent/authored/f270-r1-*` copy equals its payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_worktree_integration.py
   tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_worktrees.py
   tests/orchestration/test_worktree_lifecycle.py tests/orchestration/test_worktree_isolation.py
   tests/orchestration/test_worktree_safety.py tests/orchestration/test_worktree_persistence.py
   tests/orchestration/test_worktree_cleanup_paths.py tests/orchestration/test_worktree_resume_cli.py
   tests/orchestration/test_job_worktree_integrity.py tests/orchestration/test_job_apply.py
   tests/orchestration/test_job_apply_consistency.py tests/orchestration/test_pingpong_job_dod_gate.py
   tests/orchestration/test_pingpong_job_hunk_ledger.py tests/orchestration/test_resume_cli.py
   tests/orchestration/test_resume_kill.py tests/orchestration/test_checkpoints.py
   tests/orchestration/test_handoff.py tests/orchestration/test_session_resume.py
   tests/orchestration/test_run_manifest_resume_workspace.py
   tests/orchestration/test_run_manifest_prework_resume.py tests/test_subprocess_timeouts.py
   tests/orchestration/test_mint_call_sites.py tests/cli/test_project_current.py
   tests/orchestration/test_import_reachability.py tests/cli/test_golden_path.py tests/docs/
   tests/orchestration/test_roadmap_index.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` plus any other
   test file this round edited → summary line, 0 failed (serial, no `-n`; the reviewer's base
   reading of this list at `b7f966c0`, taken in two runs, was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 and C3 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from the worktree
   root with `python3 -B -m pytest -p no:cacheprovider tests/orchestration/test_job_worktree_integration.py`,
   `__pycache__` purged before each run, the imported `worktrees` module path printed first to
   prove it resolves inside the worktree; the UNMUTATED control first (must be exit 0); each
   mutation reverted before the next: (a) the seam's commit step skipped → t1 red; (b) the helper
   no longer forces the committer identity through the environment → t2 red; (c) the adoption
   check removed → t3 red; (d) the branch refusal removed → t4 red. Report each exit code and the
   failing ids; a mutation that stays green is reported as green, never papered over. Remove the
   worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
