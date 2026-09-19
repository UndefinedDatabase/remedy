-- STEP R5 T004+T005 -- F273 Findings paydown v1 --
Session 1 of F273 · round 5 · base `bb13258a` (the round 4 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 4's verdict and R-0774's resolution, land DECISION F273 D5, and build R-0648 and
T005 exactly as the reviewer's dry run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D5 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r5/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 ab46e52e241fbab15a076def721a7c11c5bc6f78c12519a4ff1440260c4ae7f2
  ledger.md            sha256 1952b2a06dcc2efecc1d971c054c0cf8a9142e2393ff3b62abdd5885fd7928a3
  slips.md             sha256 ff7edbda0b96f75e867bb042a5d7512a944167ced04bc1e931e91ee99ed67815
  decisions.md         sha256 7e3aedd25aad5c30ca596782a05843b3f7e943a2bc5b23b51a4f9102d6566251
  block.md             this block (save it; report its digest)
CODE — two diffs research helpers built at `bb13258a`, which the reviewer applied, ran and
red-proved in its own worktree. Apply with `git apply`; never retype or edit a hunk:
  `.remedy-wt/f273-proto-t004.diff` sha256 fa08de1f9da67b347ac2fddeda8568bab2f29a0ef28da1d448d69a85580e8f08
  `.remedy-wt/f273-proto-t005.diff` sha256 0d34c08e166d844fb30c4acf3a5824570f2ccbbff2881644ece534f1131a2660
Let T5 stand for the second diff's path; the Bundle splits it into three commits by path.

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r5-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md`,
   `.agent/prose_slips.md` and `.agent/decisions.md` := each one's `bb13258a` bytes + ledger.md,
   slips.md and decisions.md respectively.
C2 R-0648 — `git apply .remedy-wt/f273-proto-t004.diff`.
C3 R-0469 — `git apply --include=packages/orchestration/gauntlet_injection.py
   --include=tests/orchestration/test_gauntlet_injection.py T5`.
C4 every other ruff finding, the `src` line and the pin — `git apply
   --exclude=packages/orchestration/gauntlet_injection.py
   --exclude=tests/orchestration/test_gauntlet_injection.py
   --exclude=packages/orchestration/ci_budgets.py --exclude=tests/orchestration/test_ci_budgets.py
   --exclude=tests/test_no_orphan_modules.py T5`.
C5 R-0468, the zero rule — `git apply --include=packages/orchestration/ci_budgets.py
   --include=tests/orchestration/test_ci_budgets.py --include=tests/test_no_orphan_modules.py T5`.
   Before every code commit run `git status --porcelain` and stage every path the apply touched
   (`git add -A` over exactly those paths); nothing may be left untracked or unstaged.
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 5 · rounds so far 5" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C5; every gate's
   real output; open findings by distinct id (`count_open_findings`) on the committed ledger; one
   `Landed: R-xxxx` line naming its commit for each of R-0648, R-0469, R-0482 and R-0468, in the
   handoff only — never a `Done:` line anywhere; `## Next` naming Phase 1 rule 1 then the review of
   round 5, and "Operator questions open: <the count you read from the file>". Then `git push`.
   Open no pull request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, compound commands and `cd`
   before git; use `git -C <path>` and small python scripts under `.remedy-wt/f273-r5/` with an
   explicit `cwd=`. Never use `git stash`: its stack is shared.
3. Never weaken an assertion or delete a test other than the rewrites the diffs carry. A red gate
   or an ambiguity D5 does not settle -> stop, commit nothing half-done, report.
4. Build every edited `.agent/` file from `git show bb13258a:<path>` bytes.
5. Commit messages "F273 R5 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself. Never run `scripts/make_review_zip.sh` for real.
7. A reviewer's disposable worktree `.remedy-wt/f273-r5-dry` exists: never run anything in it.

Done when (G1 to G5 at C5, before C6; report literal output and the real exit code):
G1 transport + state + path sets: every payload and diff digest matched; a python check prints
   True that `.agent/plan.md` equals its payload, that `.agent/live_review.md`,
   `.agent/prose_slips.md` and `.agent/decisions.md` each equal their `bb13258a` bytes + ledger.md,
   slips.md and decisions.md, that each `.agent/authored/f273-r5-*` copy equals its payload, and
   that `git show --name-only --format=` of each of C2 to C5 lists exactly the paths its Bundle
   line's diff selection holds (read them from `git apply --numstat` with the same flags).
G2 code transport: `git rev-parse <C5>:tests <C5>:packages <C5>:scripts <C5>:pyproject.toml`
   prints exactly 1f937bccd7d8a13ae00c84ca4e327443ced674a1, bb60b3cc025b27d6baf1f5a8c3b3263f284ffaa0,
   3771accedb1590d9d01a85268d825018210e1bc3 and 1a651b4f4e12be1a41cd81073a2a50c491daab1c (the
   reviewer's dry-run trees).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_integrity_gate.py tests/orchestration/test_live_review_rotation.py
   tests/orchestration/test_final_audit_evidence.py
   tests/orchestration/test_development_artifact_boundary.py
   tests/orchestration/test_job_fulfillment.py tests/orchestration/test_ci_budgets.py
   tests/orchestration/test_ci_stages.py tests/orchestration/test_ci_workflow.py
   tests/orchestration/test_ci_run.py tests/orchestration/test_ci_stage_selection.py
   tests/cli/test_ci_cmd.py tests/orchestration/test_gauntlet_injection.py
   tests/orchestration/test_gauntlet_runner.py tests/orchestration/test_gauntlet_matrix.py
   tests/orchestration/test_gauntlet_orders.py tests/orchestration/test_dag_schedule.py
   tests/orchestration/test_decision_inbox.py tests/orchestration/test_proposal_decision.py
   tests/orchestration/test_approval_queue.py tests/cli/test_decision_cmd.py
   tests/orchestration/test_decision_evidence.py tests/cli/test_open_decisions_view.py
   tests/cli/test_teacher_cmd.py tests/orchestration/test_predictive_budget.py
   tests/runtimes/test_runtime_cli_process_boundary.py tests/ui_server/test_live_state.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
   tests/test_test_categories.py tests/orchestration/test_release_gate_wiring.py
   tests/cli/test_golden_path.py tests/runtimes/test_supervisor_portability.py` -> summary line,
   0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check . --output-format concise` from the primary checkout's root ->
   "All checks passed!", exit 0.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C5, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.integrity_gate` path printed first to prove it resolves inside
   the worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted before the next, counting the mutated bytes in the named file first (each must be 1),
   naming the failing ids:
   (a) `packages/orchestration/integrity_gate.py`: `        if severity in ("blocker", "high")` ->
   `        if severity in ("blocker",)` -> `tests/orchestration/test_integrity_gate.py` fails;
   (b) `scripts/rotate_live_review.py`: `        if finding_id in open_ids:` -> `        if True:`
   -> `tests/orchestration/test_live_review_rotation.py` fails;
   (c) `packages/orchestration/gauntlet_injection.py`: the line
   `                "the loop has no boundary there that degrades the failure")` ->
   `                f"{MISSING_SEAM}")` -> `tests/orchestration/test_gauntlet_injection.py` fails;
   (d) `packages/orchestration/ci_budgets.py`: `    ok = observed == 0` -> `    ok = observed <= 26`
   -> `tests/orchestration/test_ci_budgets.py` fails;
   (e) the same file: `import re` -> the two lines `import os` and `import re` ->
   `tests/orchestration/test_ci_budgets.py` fails in its live ruff test.
   Report exit codes and failing ids, and a mutation that stays green as green. Remove the worktree
   and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
