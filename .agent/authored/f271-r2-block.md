-- STEP R2 T001 (c) -- F271 No more legacy: ownership, reachability, replace-is-delete --
Session 1 of F271 · round 2 · base `c798fd2d` (branch `feature/f271-no-more-legacy`).

Goal: book round 1's verdict, resolve R-0893, register R-0980 to R-0982, and land the
orphan-module test of Design (c) with three unreached modules deleted — DECISION F271 D2.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F271.md; the payload `decisions.md`
(DECISION F271 D2 — this round's spec). The code of C2 and C3 is ALREADY AUTHORED as
`.remedy-wt/f271-r2/prototype_final.diff` (sha256
3678d74186e8f0df80ad019ca844a5130e10ac76527498a2905a1ff3d7703c4e, a staged diff against
`c798fd2d` built and run by a research helper and re-run by the reviewer). Read it in full; apply
it, split across C2 and C3 as below, and change nothing in it — a defect you find in it is
reported, not repaired.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f271-r2/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 495356e539ca5184ebf1b47942288d2e10ca3cd450ed49e388f4730ff2bcba1f
  ledger.md            sha256 9209c91fcd812b4ef66c256efd1a4b2f8f776148a730948e0ef26ecfb753dfb2
  decisions.md         sha256 30628c17dbb4e4b263490ce7829b41d2fdfe8ac82e001cf2eaed99e9d0ece2a0
  prototype_final.diff sha256 3678d74186e8f0df80ad019ca844a5130e10ac76527498a2905a1ff3d7703c4e
  block.md             this block (save it; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of plan.md, ledger.md, decisions.md and
   block.md as `.agent/authored/f271-r2-<name>`; `.agent/plan.md` := plan.md;
   `.agent/live_review.md` := its `c798fd2d` bytes + ledger.md bytes (it books the F271 R1 gate
   entry and `Done: R-0893`, and registers R-0980, R-0981 and R-0982); `.agent/decisions.md` :=
   its `c798fd2d` bytes + decisions.md bytes.
C2 deletion — the prototype's six deletions only: `packages/orchestration/diagnostic_comparison.py`,
   `packages/orchestration/task_plan_evidence.py`, `packages/orchestration/execution_config_evidence.py`,
   `tests/orchestration/test_diagnostic_comparison.py`, `tests/orchestration/test_task_plan_evidence.py`,
   `tests/orchestration/test_execution_config_evidence.py`. It precedes C3 because the new test
   refuses an allowance for a module that is no longer an orphan.
C3 the test — the prototype's three remaining paths: `tests/test_no_orphan_modules.py` (new),
   `tests/conftest.py` (`ARCHITECTURE_FILES`), `packages/orchestration/ci_stages.py` (`budgets`
   stage `test_paths`).
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F271 · round 2 · rounds so far 2" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output; open findings by distinct id, measured on the committed ledger; `## Next` naming
   Phase 1 rule 1 then the review of round 2, and "Operator questions open: <the count you read
   from the file>". Then `git push`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. Do-not-touch (T2_F271.md): the reachability allowlist and `tests/orchestration/test_import_reachability.py`,
   the dead-model check, the catalog's command set; `MEASURED_MAX_WALL_S` is not edited (D2 (6)).
3. No test calls a real provider. The shell denies `VAR=x cmd` and `cp`; copy bytes with python.
4. Never weaken an assertion or delete a test to pass, other than the deletions D2 (4) orders. A
   red gate or an ambiguity D2 does not settle → stop, commit nothing half-done, report.
5. Build every edited `.agent/` file from `git show c798fd2d:<path>` bytes.
6. Commit messages "F271 R2 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.

Done when (G1 to G5 at C3, before C4; report literal output and the real exit code):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/plan.md` equals plan.md, that `.agent/live_review.md` equals its `c798fd2d` bytes +
   ledger.md, that `.agent/decisions.md` equals its `c798fd2d` bytes + decisions.md, and that
   each `.agent/authored/f271-r2-*` copy equals its payload.
G2 the code is the prototype: `git diff --binary c798fd2d <C3> -- . ':!.agent' | git patch-id
   --stable` prints the same first field as `git patch-id --stable < prototype_final.diff`
   (the reviewer read `6d27af6437b714b225d8d96a2524cde9985403cc` from the latter); and C2's
   `git show --numstat` lists exactly the six deleted paths with 0 insertions.
G3 `python3 -m pytest -q -p no:cacheprovider tests/test_no_orphan_modules.py tests/test_imports.py
   tests/orchestration/test_import_reachability.py tests/orchestration/test_ci_stages.py
   tests/orchestration/test_ci_stage_selection.py tests/test_test_categories.py
   tests/test_reserved_namespaces.py tests/orchestration/test_ci_budgets.py
   tests/orchestration/test_job_evidence.py tests/cli/test_golden_path.py tests/docs/` → summary
   line, 0 failed (serial, no `-n`), run with `git status --porcelain` empty.
G4 `python3 -m ruff check tests/test_no_orphan_modules.py tests/conftest.py
   packages/orchestration/ci_stages.py` → "All checks passed!"; and
   `git grep -n -E "diagnostic_comparison|task_plan_evidence|execution_config_evidence" -- .
   ':!.agent' ':!docs/roadmap'` prints exactly the lines D2 (4) keeps — two in
   `tests/docs/test_docs_consistency.py`, one in `tests/orchestration/test_job_evidence.py` — and
   no other.
G5 red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from its root with
   `python3 -B -m pytest -q -p no:cacheprovider -rf tests/test_no_orphan_modules.py`,
   `__pycache__` purged before each run; the UNMUTATED control first (exit 0); each change
   reverted before the next: (a) a new file `packages/orchestration/zz_orphan_probe.py` holding
   `X = 1` → `test_no_module_is_an_orphan` fails naming it; (b) the `ALLOWED_UNWIRED` entry for
   `scripts/rotate_live_review.py` removed (its two lines) → `test_no_module_is_an_orphan` fails
   naming it; (c) an entry `("scripts/build_review_zip.py", "probe"),` added to `ALLOWED_UNWIRED`
   → `test_every_allowed_unwired_entry_is_a_live_orphan` fails naming it. Report exit codes and
   failing ids; report a change that stays green as green. Remove the worktree and show
   `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
