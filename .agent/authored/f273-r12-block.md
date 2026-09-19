-- STEP R12 test-run linkage and the smoke script -- F273 Findings paydown v1 --
Session 2 of F273 · round 12 · base `4c375fc4` (the round 11 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 11's verdict and five resolutions, register R-0988, land DECISION F273 D12, and
build R-0921, R-0917, R-0922, R-0899, R-0910, R-0980, R-0978 and R-0988 exactly as the reviewer's
dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D12 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r12/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 9a4261ca5efde0fd75ece797cc0084f5069680344013d053f2fdfea6b64b02ca
  ledger.md            sha256 5e2fe71f76035542bcef4afafe842cdd74c920550c5d1353d1a9f44861113297
  decisions.md         sha256 520bf5897071257ce8c391bedfb142fa28987da127dcbf8e7de684188782fc92
  block.md             this block (save it; report its digest)
CODE — diffs research helpers built, which the reviewer applied in this order at `4c375fc4`, ran
and red-proved in its own worktree. Apply with `git apply`; never edit a hunk:
  `.remedy-wt/f273-proto-g2a.diff` sha256 2c357cfec77aea3946e21d0f6b8b6458cc27042d050a4085705cc1413cd16be3
  `.remedy-wt/f273-proto-g2b.diff` sha256 14d6ae62bec6b230cb001ad79e1184f0741b08dbe92d5673a1e96bd4fafa352d

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r12-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` and
   `.agent/decisions.md` := each one's `4c375fc4` bytes + ledger.md and decisions.md respectively.
C2 R-0921, R-0917, R-0922 — `git apply` g2a.diff.
C3 R-0899, R-0910, R-0980, R-0978, R-0988 — `git apply` g2b.diff.
   Before each code commit run `git status --porcelain` and stage every path the apply touched;
   nothing may be left untracked or unstaged.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 2 of feature F273 · round 12 · rounds so far 12" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0921, R-0917, R-0922, R-0899, R-0910,
   R-0980, R-0978 and R-0988, in the handoff only — never a `Done:` line of your own; `## Next`
   naming Phase 1 rule 1 then the review of round 12, and "Operator questions open: <the count you
   read from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or model. The shell denies `VAR=x cmd`, `cp`, loops, `$( )`,
   `$VAR` (including `$?`) and `cd` before git; use `git -C <path>` and small python scripts under
   `.remedy-wt/f273-r12/` (prefix yours `wk_`) with an explicit `cwd=`. Never use `git stash`.
3. Never weaken an assertion or delete a test other than the changes the diffs carry. A red gate or
   an ambiguity D12 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show 4c375fc4:<path>` bytes.
5. Commit messages "F273 R12 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/remedy_smoke.sh` or
   `scripts/make_review_zip.sh` for real, never run the `remedy` CLI, `run_job` against this
   repository, or the self-use runner, and create no branch. Research helpers may hold worktrees
   under `.remedy-wt/f273-h-*`; never touch them.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md` and
   `.agent/decisions.md` each equal their `4c375fc4` bytes + ledger.md and decisions.md, that each
   `.agent/authored/f273-r12-*` copy equals its payload, and that `git show --name-only --format=`
   of C2 and of C3 each lists exactly the paths `git apply --numstat` reads from its diff.
G2 code transport: `git rev-parse <C3>:tests <C3>:packages <C3>:apps <C3>:scripts` prints exactly
   da037036e587716f4813ee3b76d69d8227c971e9, f7955a17f3b74dacbd4f4fb4441dd6e0b638d856,
   9c53d5b923b407e3cfaa6e26d221905fee69f8ed and 1168aa2c8ca6d3e27b40d1f123d2131a3bfad6c6 (the
   reviewer's dry-run objects).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_approval_queue.py tests/orchestration/test_real_test_execution.py
   tests/orchestration/test_test_execution_service.py tests/test_patch_apply.py
   tests/test_patch_intent_approval.py tests/test_patch_intent.py tests/cli/test_patch_cmd.py
   tests/cli/test_plan_approval.py tests/cli/test_do_cmd_cli_path.py tests/cli/test_do_cmd_summary.py
   tests/cli/test_do_flags.py tests/cli/test_do_sequence_cli.py tests/cli/test_test_run_runtime.py
   tests/cli/test_study_cmd.py tests/cli/test_advertised_commands.py tests/cli/test_command_catalog.py
   tests/test_remedy_smoke_script.py tests/test_command_discovery.py
   tests/ui_server/test_dashboard_contract.py tests/cli/test_golden_path.py` -> summary line,
   0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider` and an env carrying
   `REMEDY_OLLAMA_HOST=http://127.0.0.1:9` and `OLLAMA_HOST=http://127.0.0.1:9` (set through the
   script's `env=`), `__pycache__` purged before each run, the imported
   `packages.orchestration.patch_apply` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted from its saved bytes before the next, counting each FROM line (with its newline) in
   the named file first (each must be 1), naming the failing ids. S =
   tests/test_remedy_smoke_script.py.
   (a) `packages/orchestration/test_execution_service.py`:
   `        if _find_artifact_for_intent(job, intent_id) is None:` -> `        if True:` ->
   tests/orchestration/test_test_execution_service.py fails;
   (b) `packages/orchestration/patch_apply.py`: in the one line starting
   `    return (f"remedy test run {job_id} --intent-id ` replace `{result.intent_id}` by `{job_id}`
   -> tests/test_patch_apply.py fails;
   (c) `apps/cli/commands/do_cmd.py`: `        yes=getattr(args, "yes", False),` ->
   `        yes=False,` -> tests/cli/test_plan_approval.py fails;
   (d) `scripts/remedy_smoke.sh`: `state = job.get('status', '')` -> `state = job.get('state', '')`
   -> S fails;
   (e) the same file: the line
   `    # event, was dropped by F273 (R-0980): no product path emits that event.` ->
   `    # token_policy_applied run-log event` -> S fails;
   (f) `scripts/remedy_smoke.sh`: in the one line starting `    for grp in job project ` insert
   ` policy` before `; do` -> S fails;
   (g) `tests/cli/test_study_cmd.py`: the one line starting
   `        monkeypatch.setenv("REMEDY_OLLAMA_HOST", f"http://127.0.0.1:{` ->
   `        monkeypatch.setenv("REMEDY_OLLAMA_HOST", "http://127.0.0.1:9")` ->
   tests/cli/test_study_cmd.py fails;
   (h) `tests/cli/test_do_sequence_cli.py`: the line
   `    import packages.orchestration.study  # noqa: F401` deleted -> the ordered pair
   tests/cli/test_do_sequence_cli.py then tests/cli/test_study_cmd.py fails;
   (i) `tests/test_remedy_smoke_script.py`: in the one line containing `cwd=str(tmp_path))` that
   starts `        result = _run_in_bash(f"bash '{SMOKE_SCRIPT}'", env=env,` remove
   `, cwd=str(tmp_path)` -> S fails.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
