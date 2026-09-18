-- STEP R6 writer + deletion -- F269 Contract & contract templates --
Session 1 of F269 · round 6 · base `c93d117d` (branch feature/f269-contract, pushed).

Goal: the contract binds each of its jobs to the repository and grants it the three capabilities
the surviving commands check; then `remedy job attach-repo` and `remedy job permit` are deleted,
with every string that advertises them naming the heir.

Read first, completely: AGENTS.md (Scope Control); docs/roadmap/features/T2_F269.md ("Also owed
here"); the payload `decisions.md` (DECISION F269 D7 — this round's spec; where this block is
terser, it rules); DECISIONs amend0917-throughput D2 and F280 D4 in `.agent/decisions.md`;
`packages/orchestration/permissions.py`; `packages/orchestration/mission_contract.py`; the two call
sites of `merge_contract_slice_into_dod` (`orchestrator_loop.execute_move`, `do_sequence._step_shape`).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f269-r6/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md     sha256 77c7fab0471286bbfef4b0576af48328ba8c35667dfd0eafd90e3f0bef7c9e7f
  decisions.md  sha256 66027d1798f131c4c24ce0eae46c7298b7cd941407d0ccadc5f71c8ad765b8fb
  plan.md       sha256 abfa1a3fee20c976e034153a48e782f7d67eb58603ad35d1549163310148becb
  opq.md        sha256 daabfd5178d1d7f15c0dd56876f34ac8ef4ab9a8437b0c61997d1f4863be4140
  block.md      this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of ledger.md, decisions.md, plan.md, opq.md and block.md
   as `.agent/authored/f269-r6-<name>`; `.agent/live_review.md` := its `c93d117d` bytes +
   ledger.md; `.agent/decisions.md` := its `c93d117d` bytes + decisions.md; `.agent/plan.md` :=
   plan.md.
C2 the writer — D7 FIRST, called at both merge sites. Tests: a job dispatched through
   `execute_move` for a mission with a contract carries `target_repo` (the project's canonical
   repository when the job has no `repo_path`) and the three grants, `permissions.is_allowed` true
   for each; a `remedy do` job carries `target_repo` equal to its `repo_path` and the three grants;
   a mission with no contract writes nothing; an existing `target_repo` is not overwritten.
C3 the deletion — D7 SECOND: the two catalog entries, handlers and dispatch entries in
   `apps/cli/command_catalog.py` and `apps/cli/commands/job.py` (and the comment in
   `apps/cli/commands/job_context_cmd.py`); `tests/test_command_catalog.py` REQUIRED and DELETED;
   the tests asserting the commands themselves deleted (`tests/test_cli_main.py`'s
   `TestSetPermissionReservedNotice`, `tests/orchestration/test_autonomy.py`'s
   `test_permit_arg_order_correct`, the `attach-repo` help case of `tests/test_grouped_cli.py`); the
   fixture setups in `tests/test_command_discovery.py`, `tests/orchestration/test_test_runner.py`
   and `tests/test_test_runner.py` write the binding and grants on the job record directly.
C4 the heir in every string — every production string under `packages/`, the lines of
   `scripts/remedy_smoke.sh`, and the `docs/system/` and `docs/guides/` pages that tell a reader to
   run either command name the heir instead (D7's sentence; `job_attach_repo_tip` in
   `packages/orchestration/stop_reasons.py` rewritten or deleted with its callers), and the tests
   asserting that guidance text follow it, each keeping its property. `docs/archive/` is history and
   is not edited.
C5 handoff — `.agent/operator_questions.md` := its `c93d117d` bytes + opq.md; rewrite
   `.agent/handoff.md` per docs/agents/handback_template.md: "SESSION 1 of feature F269 · round 6 ·
   rounds so far 6" plus one sentence of context self-assessment; per-commit tables with `git show
   --numstat` counts for C1 to C4; every gate's real output; `## Next` naming Phase 1 rule 1 then
   the review of round 6, and "Operator questions open: <the count you read after the append>".
   Then `git push`.

Constraints:
1. Change set: the paths the Bundle names, the files C4's sweep reaches, and the regenerated
   import-reachability allowlist if its test requires it. Every commit < 500 inserted lines; split
   C3 or C4 by directory rather than exceed.
2. Do-not-touch: `permissions.py`'s capability set and defaults; the five surviving commands'
   checks; `dod_compiler.py`, `dod_gate.py`, `dod_runners.py`. No stub, alias, hidden command or
   compatibility reader is left for the deleted commands (AGENTS.md Scope Control).
   `project.attach-repo` is a different command and STAYS: it writes the project's canonical
   repository, which D7's writer falls back to (its `subcommand="attach-repo"` line in the catalog
   is one G4 (c) line that stays).
3. No test calls a real provider. The shell denies `VAR=x cmd`, `cp` and `sed -i`; use python.
4. Never weaken an assertion to pass; a test is deleted only where D7 SECOND names it. A red gate or
   an ambiguity D7 does not settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show c93d117d:<path>` bytes.
6. Commit messages "F269 R6 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G5 at C4, before C5; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, and that `.agent/live_review.md` and `.agent/decisions.md` equal
   their `c93d117d` bytes + their slice.
G2 `python3 -m pytest -q -p no:cacheprovider` over every test file C2 to C4 created or edited, plus
   `tests/test_command_catalog.py tests/cli/test_advertised_commands.py tests/test_grouped_cli.py
   tests/orchestration/test_mission_contract.py tests/orchestration/test_orchestrator_loop.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py
   tests/orchestration/test_import_reachability.py tests/docs/` → summary line, 0 failed. List the
   files you passed.
G3 `python3 -m ruff check` over every .py file C2 to C4 touched → "All checks passed!".
G4 the absence sweep, at `c93d117d` and at C4, each printed in full: (a) `git grep -n -E "job
   attach-repo|job permit|_cmd_attach_repo|_cmd_set_permission|job_attach_repo_tip" <rev> --
   apps packages scripts tests docs/system docs/guides README.md` — at C4 no line; (b) `git grep -n
   -E "job\.attach-repo|job\.permit" <rev> -- apps packages scripts tests docs/system docs/guides` —
   at C4 exactly the two `TestDeletedCommands` lines of `tests/test_command_catalog.py`; (c) `git
   grep -n -E "\"attach-repo\"|\"permit\"" <rev> -- tests apps packages` — at C4 every remaining
   line printed with one sentence on why it stays.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest`, `__pycache__` purged before each run, the imported
   `mission_contract` module path printed first to prove it resolves inside the worktree; the
   UNMUTATED control over the test file holding C2's tests first (must be exit 0); each mutation
   reverted before the next: (a) the writer grants nothing → C2's grant tests red; (b) the writer
   binds no `target_repo` → C2's binding tests red. Report each exit code and the failing ids;
   remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
