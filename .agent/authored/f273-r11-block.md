-- STEP R11 job run and apply truth -- F273 Findings paydown v1 --
Session 2 of F273 · round 11 · base `e707b52e` (the round 10 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 10's verdict and three resolutions, land DECISION F273 D11, and build R-0974,
R-0913, R-0890, R-0898 and R-0935 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D11 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r11/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md                sha256 9826168e07b2251fcad748ef2c9cea49fba0f4fde3056c49dd46bf5cac3f99ff
  ledger.md              sha256 5d4e2c3dff35fff37ac90a76ccd62453d1f345c88ffde9d3d0fc0f631ce49725
  decisions.md           sha256 c49d496dcf4caa855623aef3cd3b332e6a69682e77fbc9b78e6ac6c806cadd24
  operator_questions.md  sha256 d10ed1ab57359117315914704a564ae267df639143478adf22feb381ae4641dc
  block.md               this block (save it; report its digest)
CODE — diffs research helpers built, which the reviewer applied in this order at `e707b52e`, ran
and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g1a.diff` sha256 be37fc4606ab2f3f496b3875f4ee7c7c3a4dcc229600534854075e01cb1de4d9
  `.remedy-wt/f273-proto-g1b.diff` sha256 54247b4ab5ba9b180640833131a2c53831444f796ae9c24343ab566b20c5d6ee

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of plan.md, ledger.md, decisions.md and
   block.md as `.agent/authored/f273-r11-<name>`; `.agent/plan.md` := plan.md;
   `.agent/live_review.md` and `.agent/decisions.md` := each one's `e707b52e` bytes + ledger.md
   and decisions.md respectively.
C2 R-0974, R-0913, R-0890 — `git apply` g1a.diff.
C3 R-0898, R-0935 — `git apply` g1b.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched;
   nothing may be left untracked or unstaged.
C4 handoff — `.agent/operator_questions.md` := operator_questions.md (the questions-file rule of
   docs/agents/self_drive_protocol.md puts it in the handback commit), and rewrite
   `.agent/handoff.md` per docs/agents/handback_template.md: Session section "SESSION 2 of feature
   F273 · round 11 · rounds so far 11" plus one sentence of context self-assessment; per-commit
   tables with `git show --numstat` counts for C1 to C3; every gate's real output; open findings
   by distinct id (`count_open_findings`) on the committed ledger; one `Landed: R-xxxx` line naming
   its commit for each of R-0974, R-0913, R-0890, R-0898 and R-0935, in the handoff only — never a
   `Done:` line of your own; `## Next` naming Phase 1 rule 1 then the review of round 11, and
   "Operator questions open: <the count you read from the file after C4>". Then `git push`. Open no
   pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`, `$VAR`
   (including `$?`) and `cd` before git; use `git -C <path>` and small python scripts under
   `.remedy-wt/f273-r11/` (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D11 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show e707b52e:<path>` bytes.
5. Commit messages "F273 R11 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real,
   never run the `remedy` CLI, `run_job` against this repository, or the self-use runner, and
   create no branch. Research helpers may hold worktrees under `.remedy-wt/f273-h-*`; never touch
   them.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `e707b52e` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r11-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 each lists exactly the paths `git apply --numstat` reads from its diff. After
   C4, the same check prints True that `.agent/operator_questions.md` equals its payload; report
   that line in your final message only.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:apps` prints exactly
   37e828a5d68272d0818de2b341153567d99b11c6, 57920941d61b6d9f8c60fb859967a61487451dd8 and
   5d61c2fcd474357a19011c382a6140929da1faff (the reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_episode_snapshot_full_validity.py
   tests/orchestration/test_episode_snapshot_lifecycle.py tests/orchestration/test_job_apply_commit.py
   tests/orchestration/test_job_apply_consistency.py tests/orchestration/test_job_apply_history.py
   tests/orchestration/test_job_apply.py tests/orchestration/test_job_budgets.py
   tests/orchestration/test_job_fulfillment.py tests/orchestration/test_job_worktree_handoff.py
   tests/orchestration/test_job_worktree_integration.py tests/orchestration/test_job_worktree_integrity.py
   tests/orchestration/test_resume_cli.py tests/orchestration/test_resume_kill.py
   tests/orchestration/test_run_contract.py tests/orchestration/test_self_use_runner.py
   tests/orchestration/test_worktree_cleanup_paths.py tests/orchestration/test_worktree_isolation.py
   tests/orchestration/test_worktree_lifecycle.py tests/orchestration/test_worktree_persistence.py
   tests/orchestration/test_worktree_resume_cli.py tests/orchestration/test_worktree_safety.py
   tests/orchestration/test_worktrees.py tests/orchestration/test_f018_authority_integration.py
   tests/orchestration/test_import_reachability.py tests/orchestration/test_self_use_job.py
   tests/cli/test_contract_cmd.py tests/cli/test_do_cmd_cli_path.py tests/cli/test_do_cmd_summary.py
   tests/cli/test_job_budget_set.py tests/cli/test_job_commands.py tests/cli/test_job_report.py
   tests/cli/test_job_show.py tests/cli/test_advertised_commands.py tests/cli/test_cli_ux.py
   tests/test_command_discovery.py tests/test_role_override_flags.py tests/test_run_contract.py
   tests/test_no_orphan_modules.py tests/ui_server/test_dashboard_contract.py
   tests/cli/test_golden_path.py` -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.worktrees` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted from its saved bytes before the next, counting each FROM line (with its newline) in
   the named file first (each must be 1), naming the failing ids. H =
   tests/orchestration/test_job_worktree_handoff.py.
   (a) `packages/orchestration/worktrees.py`:
   `            ["git", "read-tree", "HEAD"], cwd=handle.path, env=env,` -> the same line with
   `"HEAD"` replaced by `"--empty"` -> H fails;
   (b) `packages/orchestration/pingpong_job.py`:
   `    if not W._branch_exists(job.repo_path, job.worktree_branch):` -> `    if False:` -> H fails;
   (c) the same file: `    if job.worktree_cleanup_status not in JOB_RECOVERABLE_STATES:` ->
   `    if False:` -> H fails;
   (d) `apps/cli/commands/do_cmd.py`: `    if _refusal:` -> `    if False:` -> H fails;
   (e) `packages/orchestration/self_use_runner.py`: `        for field in ("model", "effort"):` ->
   `        for field in ():` -> tests/orchestration/test_self_use_runner.py fails;
   (f) `packages/orchestration/pingpong_job.py`:
   `TASK_DONE_STATUSES = frozenset({TASK_PASSED, TASK_APPLIED, RunState.COMPLETED.value})` ->
   `TASK_DONE_STATUSES = frozenset({RunState.COMPLETED.value})` -> tests/cli/test_job_show.py fails;
   (g) `packages/orchestration/run_contract.py`:
   `            budgets = JobBudgets.model_validate(budgets)` -> `            return None, None` ->
   tests/orchestration/test_f018_authority_integration.py and tests/cli/test_job_budget_set.py fail;
   (h) `apps/cli/commands/job.py`: `        if f018_field:` -> `        if False:` ->
   tests/cli/test_job_budget_set.py fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
