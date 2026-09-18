-- STEP R3 repairs + T004 (job apply) -- F270 History apply: one commit per task, merge on demand --
Session 1 of F270 · round 3 · base `4a615385` (branch feature/f270-history-apply, pushed).

Goal: book round 2's FAIL and repair its two findings — R-0975 (three refusals no test reaches)
and R-0976 (the `--commit-with-history` help breaks the vocabulary, `tests/docs/` red) — then
build the `job apply` half of T004: `--commit "<message>"`, `--commit-auto`, `--push`, and the
registered config key `apply.push_after_mission`.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F270.md; the payloads `ledger.md`
(R-0975 and R-0976 — their FIX clauses are this round's repair spec) and `decisions.md` (DECISION
F270 D3 — this round's feature spec; where this block is terser, it rules); DECISIONs F270 D1 and
D2 in `.agent/decisions.md`; `packages/orchestration/job_apply.py` whole. REFERENCES, not slices:
`.remedy-wt/f270-r3/prototype.diff` and `.remedy-wt/f270-r3/prototype_test_job_apply_commit.py`
are a research helper's prototype of D3 and of R-0975's tests at `4a615385` (it measured 0
failures over this round's G2 files and every refusal red when disabled). Read it, write your own
code, and copy nothing blindly.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f270-r3/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 234a6832343b98d84c86c46500a6f5f10bad54c472a7a8329b0890c1ba29df43
  decisions.md  sha256 3cb87ab1a63721730ef10b71d3f339f93f0a8bb5921d75b470656e462149479e
  slips.md      sha256 37cd7c43faca39ea0867ec6be8aa20cea47b638ccc120be9e8c9d501dd20b77e
  plan.md       sha256 e6c74ca2476711caff06b2944992fdba52f12010da9cb9e9f6b0dc889f5b38ff
  block.md      this block (save it in C1 with the others; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of EVERY payload above, the block included, as
   `.agent/authored/f270-r3-<name>`; `.agent/live_review.md` := its `4a615385` bytes + ledger.md
   (round 2's FAIL, R-0975, R-0976); `.agent/decisions.md` := its `4a615385` bytes + decisions.md;
   `.agent/prose_slips.md` := its `4a615385` bytes + slips.md; `.agent/plan.md` := plan.md.
C2 the repairs — R-0975: in `tests/orchestration/test_job_apply_history.py`, (h14) a branch whose
   tip is the recorded `worktree_head` but whose tree does not match `result_diff_sha256`,
   (h15) a target holding `MERGE_HEAD` from the operator's own conflicted merge, left untouched,
   (h16) a target that is a subdirectory of a repository — each refused with nothing changed.
   R-0976: reword the `--commit-with-history` description in `apps/cli/command_catalog.py` so
   `tests/docs/test_vocabulary.py` passes, keeping what it says the flag does.
C3 the flags — D3 (1) to (7): `packages/orchestration/job_apply.py` (the flags through
   `apply_job`, the shared checkout refusals, the commit, the push, the record, the summary and
   preview), the subject fitter shared with `build_task_commit_message` in
   `packages/orchestration/pingpong_job.py` with the per-task output unchanged, the key in
   `packages/orchestration/config.py` with its helper, one row for it in
   `docs/system/remedy-toml-configuration-system-v0.md`, the three ArgDefs on `job.apply` in
   `apps/cli/command_catalog.py`, and their pass-through in `_cmd_job_apply` in
   `apps/cli/commands/do_cmd.py`. `do.run`'s own flags and `_DO_FLAGS_NOT_YET_AVAILABLE` are NOT
   touched. Every git call carries a timeout. Split into C3a/C3b if over 500 inserted lines.
C4 tests — a new `tests/orchestration/test_job_apply_commit.py`, at least: `--commit "Add the
   contact page"` → exactly one new commit whose parent is the previous tip, first line exactly
   that, touching exactly the copied files, the operator's author, the contract line as the last
   body line, both trailers; `--commit-auto` → one commit whose first line passes D3 (4)'s rule,
   and a unit test of the rule rejecting `T002`, a verbless line and an 80-character line; each
   flag clash, a lone `--push`, an empty and a two-line message → refused; a dirty tree, a
   detached `HEAD`, a rebase in progress and an ignored copied path → refused with nothing copied;
   a failed post-test → files copied, no commit; a staging job committed onto a git target;
   `--push` with a bare fixture remote as upstream → exactly one push received, and the remote
   configured with `receive.denyNonFastForwards=true`; `--push` with no upstream → refused naming
   the command, nothing written; `--push` while a blocking criterion is `open` or `unmet` →
   refused before anything is written; a push that fails after the commit → the commit stays,
   status `applied_push_failed`; plain `--approve`, also with `apply.push_after_mission` set →
   no commit and no push, the operator's `HEAD` unchanged. Split into C4a/C4b under 500 lines.
C5 handoff — append to `.agent/live_review.md` exactly two lines, `Landed: R-0975 — <one line:
   what changed, which commit>` and `Landed: R-0976 — <the same>`, each preceded by a blank line
   (never a `Done:` line); rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 1 of feature F270 · round 3 · rounds so far 3" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output; open findings by distinct id; `## Next` naming Phase 1 rule 1 then the review of
   round 3, and "Operator questions open: <the count you read from the file>". Then `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F270.md): the apply gate's approval semantics, the snapshot guard, the
   worktree lifecycle beyond committing on it. No existing gate of `apply_job` is removed,
   reordered or relaxed; nothing force-pushes; nothing runs `git reset` on the operator's branch.
3. No test calls a real provider or a network remote; remotes are bare repositories under
   `tmp_path`. The shell denies `VAR=x cmd` and `cp`; use python; set environment in tests with
   `monkeypatch.setenv`.
4. Never weaken an assertion or delete a test to pass. A red gate or an ambiguity D3 does not
   settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show 4a615385:<path>` bytes.
6. Commit messages "F270 R3 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G4 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md`, `.agent/decisions.md` and
   `.agent/prose_slips.md` equal their `4a615385` bytes + ledger.md, + decisions.md and + slips.md,
   and that each `.agent/authored/f270-r3-*` copy, the block's included, equals its payload.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_job_apply_commit.py
   tests/orchestration/test_job_apply.py tests/orchestration/test_job_apply_history.py
   tests/orchestration/test_job_apply_consistency.py tests/orchestration/test_job_worktree_handoff.py
   tests/orchestration/test_job_worktree_integration.py tests/ui_contracts/test_apply_state_partial.py
   tests/orchestration/test_config.py tests/cli/test_config_cmd.py tests/test_help_renderer.py
   tests/cli/test_cli_ux.py tests/orchestration/test_mission_contract.py
   tests/orchestration/test_do_run.py tests/cli/test_golden_path.py tests/cli/test_do_sequence_cli.py
   tests/test_command_catalog.py tests/cli/test_advertised_commands.py
   tests/orchestration/test_import_reachability.py tests/test_subprocess_timeouts.py tests/docs/
   tests/ui_server/test_dashboard_contract.py tests/orchestration/test_test_runner.py
   tests/regression/test_resource_safety.py` plus any other test file this round edited → summary
   line, 0 failed (serial, no `-n`; the reviewer's base reading of this list without the new file,
   at `4a615385`, was 1 failed — R-0976's node — and 1135 passed).
G3 `python3 -m ruff check` over every .py file C2 to C4 touched → "All checks passed!".
G4 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -p no:cacheprovider tests/orchestration/test_job_apply_history.py
   tests/orchestration/test_job_apply_commit.py`, `__pycache__` purged before each run, the
   imported `job_apply` module path printed first; the UNMUTATED control first (must be exit 0);
   each check below replaced by `False` (or the named change made), reverted before the next:
   (a) the diff-hash check → h14 red; (b) the merge-in-progress refusal → h15 red; (c) the
   top-level refusal → h16 red; (d) the flag-clash refusal; (e) the dirty-tree refusal; (f) the
   check that the commit touches only the copied paths; (g) the no-upstream refusal; (h) the
   not-met blocking criterion refusal; (i) `--force` added to the push; (j) a plain `--approve`
   made to commit. Report each exit code and the failing ids; a mutation that stays green is
   reported as green, never papered over. Remove the worktree and show `git worktree list`.
G5 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
