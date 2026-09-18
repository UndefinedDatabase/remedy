-- STEP R2 T002+T003 -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 2 · base `ff9d56a2` (branch feature/f270-history-apply, pushed).

Goal: T002 with T003 — `remedy job apply <job> --approve --commit-with-history` merges the job
branch `remedy/job-<job id>` onto the operator's current branch with `--no-ff`, and refuses a
dirty tree, a conflict, a staging target, a detached checkout and a branch that is not the
reviewed work, changing nothing when it refuses.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F270.md; the payload `decisions.md`
(DECISION F270 D2 — this round's spec; where this block is terser, it rules); DECISION F270 D1 in
`.agent/decisions.md`; `packages/orchestration/job_apply.py` whole. REFERENCES, not slices:
`.remedy-wt/f270-r2/prototype.diff` and `.remedy-wt/f270-r2/prototype_test_job_apply_history.py`
are a research helper's prototype of D2 at `ff9d56a2` (it measured 0 failures and six red
mutations); it predates D2 (4)'s hook-output rule and D2 (5)'s undo sentence, and its `_hgit` has
an unused `env` parameter. Read it, write your own code, and copy nothing blindly.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r2/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 c159df253a6f6c63588da70a8b01116f0dee01a9a3f63273db438d60a14fe225
  decisions.md  sha256 471ee2504412895432c54c3b1502a2c7e42ff209b28f22433bf09f69bafc0790
  plan.md       sha256 9c75d0ffedf01a88822b5fd70364b717d8d57ca5ab46a0ddab7af2fb14ddf28a
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f270-r2-<name>`;
   `.agent/live_review.md` := its `ff9d56a2` bytes + ledger.md (round 1's verdict);
   `.agent/decisions.md` := its `ff9d56a2` bytes + decisions.md; `.agent/plan.md` := plan.md.
C2 the merge path — D2 (1) to (7) in `packages/orchestration/job_apply.py` (the flag through
   `apply_job` and the source/copy step, the refusals, the merge, the abort, the record fields,
   the summary), the `--commit-with-history` ArgDef on `job.apply` in
   `apps/cli/command_catalog.py` (help text: what it does and that it needs `--approve`), and its
   pass-through in `_cmd_job_apply` in `apps/cli/commands/do_cmd.py`. Reuse round 1's contract-line
   builder in `pingpong_job.py`; do not copy it. Every git call carries a timeout. Update the
   `job_apply.py` module and `apply_job` docstrings that say an apply never commits, so they state
   the flag's exception. `do`'s own not-yet-available `--commit-with-history` stays as it is —
   T004 takes the whole `do` pass-through.
C3 tests — a new `tests/orchestration/test_job_apply_history.py` (reuse the `repo` fixture,
   `_git` and `_run_two_task_job` of `tests/orchestration/test_job_worktree_integration.py`):
   (h1) happy path: a merge commit with two parents whose second-parent side is exactly the two
   task commits, files equal to the job's result, author and committer the operator's identity,
   the operator's `commit-msg` hook ran, the D2 (3) first line, `contract: none` as the last body
   line, both trailers, the record's `merge_commit` equal to the new `HEAD`, the job branch kept;
   (h2) where a fast-forward was possible the result still has two parents; (h3) the flag without
   `--approve` previews and changes nothing; refusals each proving `HEAD`, the symbolic ref,
   `git ls-files -s`, `git status --porcelain --untracked-files=all`, the absence of `MERGE_HEAD`
   and every file's sha256 unchanged: (h4) dirty tree, naming the path; (h5) the committed hand
   edit to a job file, refused by the baseline gate, the edit intact; (h6) the `pkg` versus
   `pkg/mod.txt` git conflict, aborted, naming what git reports unmerged; (h7) a copy-mode job,
   nothing copied, and a later plain `--approve` still copies; (h8) plain `--approve` copies and
   leaves the operator's `HEAD` unchanged; (h9) detached `HEAD`; (h10) the branch tip moved; (h11)
   the branch deleted; (h12) `--skip-blocked` with the flag; (h13) a `pre-merge-commit` hook that
   exits 1 with a message — refused, aborted, the hook's message quoted; and one CLI test through
   `tests/cli/runtime_helpers.py` `run_grouped_cli` for a merging and a refused run with their
   exit codes and JSON keys. Split into C3a/C3b if one commit would exceed 500 inserted lines.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F270 · round 2 · rounds so far 2" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id; `## Next` naming Phase 1 rule 1 then the review of
   round 2, and "Operator questions open: <the count you read from the file>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F270.md): the apply gate's approval semantics, the snapshot guard, the
   worktree lifecycle beyond committing on it. No existing gate of `apply_job` is removed,
   reordered or relaxed; nothing pushes; nothing runs `git reset` on the operator's branch.
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python;
   set environment in tests with `monkeypatch.setenv`.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D2 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show ff9d56a2:<path>` bytes.
6. Commit messages "F270 R2 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C3, before C4; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` and `.agent/decisions.md` equal
   their `ff9d56a2` bytes + ledger.md and + decisions.md, and that each `.agent/authored/f270-r2-*`
   copy equals its payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_apply_history.py
   tests/orchestration/test_job_apply.py tests/orchestration/test_job_apply_consistency.py
   tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_job_worktree_integration.py
   tests/ui_contracts/test_apply_state_partial.py tests/cli/test_golden_path.py
   tests/cli/test_do_sequence_cli.py tests/test_command_catalog.py tests/cli/test_advertised_commands.py
   tests/orchestration/test_import_reachability.py tests/test_subprocess_timeouts.py
   tests/orchestration/test_do_run.py tests/ui_server/test_dashboard_contract.py
   tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py` plus any other
   test file this round edited → summary line, 0 failed (serial, no `-n`; the reviewer's base
   reading of this list without the new file, at `ff9d56a2`, was 0 failed).
G3 `python3 -m ruff check` over every .py file C2 and C3 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from the worktree
   root with `python3 -B -m pytest -p no:cacheprovider tests/orchestration/test_job_apply_history.py`,
   `__pycache__` purged before each run, the imported `job_apply` module path printed first; the
   UNMUTATED control first (must be exit 0); each mutation reverted before the next: (a) no
   `git merge --abort` → h6 and h13 red; (b) no dirty-tree check → h4 red; (c) `--no-ff` removed →
   h2 red; (d) no branch-tip and diff-hash check → h10 red; (e) no detached-`HEAD` check → h9 red;
   (f) the flag ignored, files copied instead → h1 red. Report each exit code and the failing ids;
   a mutation that stays green is reported as green, never papered over. Remove the worktree and
   show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
