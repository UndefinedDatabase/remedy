-- STEP R6 T004 -- F276 Data-root hygiene & disk budget --
Session 1 of F276 · round 6 · base `caa9d073` (the round 5 handoff, the branch tip).

Goal: book round 5's verdict, resolve R-1003, and build T004 exactly as the reviewer's dry run
built it: a disk floor that behaves like every other budget.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F276.md; the payload `decisions.md`
(DECISION F276 D7 — this round's spec; where this block is terser, it rules). The carrier's code
comments cite D7 by name, so D7 must land in the same round as the code that cites it, which C1
does.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f276-r6/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md            sha256 380f071c3c64b56f9f79a5d935505b07c3d13d6d1ddcdc3958049990b82cd0e8
  decisions.md         sha256 1f5d119157524d658421a0918e4033244a3c1455d524f144c11456a6f69b6151
  plan.md              sha256 aa0ec9c4ca0cc04b01af32d17bc7c39983b2920a869b7dd65a742db932f74045
  block.md             this block (save it; report its line count and digest)
CODE — ONE diff the reviewer produced from its own dry-run worktree at `caa9d073`, applied there,
tested there and red-proved there. Apply it in three disjoint slices with the `--include` lists
below; do not retype or edit a hunk, and never apply it whole:
  `.remedy-wt/f276-r6/f276-r6.diff` sha256 dab8ece50d394eab1c56fdb67713731355304fd29900a8398cdd17a83aca7e43

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of the four payloads above as
   `.agent/authored/f276-r6-<name>`; `.agent/live_review.md` := its `caa9d073` bytes + ledger.md
   (it books round 5's PASS and resolves R-1003); `.agent/decisions.md` := its `caa9d073` bytes +
   decisions.md; `.agent/plan.md` := plan.md.
C2 the budget, the manifest schema and the stop path — `git apply` of the diff with
   `--include=packages/core/models.py --include=packages/orchestration/config.py
   --include=packages/orchestration/budget_resolution.py
   --include=packages/orchestration/budget_guard.py --include=packages/orchestration/safe_points.py
   --include=packages/orchestration/failure_postmortem.py
   --include=packages/orchestration/pingpong_job.py --include=packages/orchestration/run_manifest.py
   --include=tests/orchestration/test_failure_postmortem.py`.
C3 the doctor section and the docs — the same diff with
   `--include=apps/cli/commands/worker_facade_cmd.py --include=docs/system/architecture.md
   --include=docs/system/job-budget-enforcement-v0.md
   --include=docs/roadmap/features/T2_F276.md`.
C4 the tests — the same diff with `--include=tests/orchestration/test_disk_floor.py`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F276 · round 6 · rounds so far 6" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output, one line per gate; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; NO
   `Landed:` line and no `Done:` line anywhere — R-1003 is resolved by the reviewer's own text
   inside C1's ledger append, and this round lands no other finding's fix; `## Next` naming Phase 1
   rule 1, then the review of
   round 6, then the closure sequence's first round, and "Operator questions open: <the count of
   `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push origin feature/f276-data-root-hygiene`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names, and nothing else. Every commit under 500 inserted lines;
   report each commit's own insertions from `git show --numstat`.
2. The shell denies `VAR=x cmd`, `cp` and compound commands; copy bytes and read exit codes with
   small python scripts under `.remedy-wt/f276-r6/`. `python3 -m apps.cli.grouped <group> <cmd>` is
   the runnable spelling of `remedy <group> <cmd>`.
3. Never weaken an assertion or delete a test. A red gate, or an ambiguity D7 does not settle ->
   stop, commit nothing half-done, report.
4. Build both edited `.agent/` record files from `git show caa9d073:<path>` bytes.
5. Commit messages "F276 R6 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never read, list or write the operator's `.data/`. Every test measures a tmp root, and every
   `REMEDY_DATA_DIR` is set in-process, never as a shell assignment.
7. The production change is DESCRIBED by D7 and CARRIED by the diff: apply it, do not re-derive it.
   Each of C2 to C4 is green on its own; if one is not, stop at it and report which gate went red.

Done when (G1 to G5 at C4, before C5; report the literal output and the real exit code of each):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/live_review.md` equals its `caa9d073` bytes + ledger.md, that `.agent/decisions.md`
   equals its `caa9d073` bytes + decisions.md, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f276-r6-*` copy equals its payload. Report the saved block's line count and
   sha256 beside the ones this block's own bytes give.
G2 code transport: at C4, `git rev-parse <C4>:packages <C4>:apps <C4>:tests` prints exactly
   9e8270485bc6089ecda1530383321866c7e061b3, 5b69fdc726129ca33f136a09d380af87c5c82961 and
   873edefb54b98707ceba442d19ba4841878d1c37, and `git rev-parse <C4>:docs/system/architecture.md
   <C4>:docs/system/job-budget-enforcement-v0.md <C4>:docs/roadmap/features/T2_F276.md` prints
   b315d40a3db0100848f9d83410efb08fc561f932, 5517d8074f6a73544458544632cfaf09c870e010 and
   920afe71529eb47b68a2e9b0c0a7ee5677e6ee87 — the objects of the reviewer's dry run. Also
   `git diff --name-only <C1> <C4>` names exactly the paths C2 to C4 name, and no other; report
   that list and its length.
G3 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_disk_floor.py
   tests/orchestration/test_failure_postmortem.py tests/orchestration/test_budget_guard.py
   tests/orchestration/test_budget_stop_integration.py tests/orchestration/test_job_budgets.py
   tests/orchestration/test_config.py tests/orchestration/test_safe_points.py
   tests/orchestration/test_run_manifest.py tests/orchestration/test_job_apply.py
   tests/orchestration/test_staging_lifecycle.py tests/cli/test_worker_facade_cmd.py
   tests/cli/test_golden_path.py tests/docs tests/test_run_contract.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py` in the primary
   checkout, serial (no `-n`) -> summary line, 0 failed, exit 0.
G4 `python3 -m ruff check packages/core/models.py packages/orchestration/config.py
   packages/orchestration/budget_resolution.py packages/orchestration/budget_guard.py
   packages/orchestration/safe_points.py packages/orchestration/failure_postmortem.py
   packages/orchestration/pingpong_job.py packages/orchestration/run_manifest.py
   apps/cli/commands/worker_facade_cmd.py tests/orchestration/test_disk_floor.py
   tests/orchestration/test_failure_postmortem.py` -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -q --no-header -rf -p no:cacheprovider
   tests/orchestration/test_disk_floor.py tests/orchestration/test_failure_postmortem.py`,
   `__pycache__` purged before each run, the imported `packages.orchestration.budget_guard` path
   printed first to prove it resolves inside the worktree. The UNMUTATED control first (expect
   exit 0). Then, each reverted byte-identically before the next, the mutated bytes counted in the
   named file first (each count must be 1): (a) in `budget_guard.py` the text
   `if free < budgets.min_free_disk_bytes:` replaced by `if free > budgets.min_free_disk_bytes:`;
   (b) in `pingpong_job.py` the line `    _pre_stop = _stop_check()` replaced by
   `    _pre_stop = None`; (c) in `pingpong_job.py` the text `_terminal = "disk_exhausted"`
   replaced by `_terminal = "budget_exhausted"` — note that applying (c) makes the replacement text
   occur twice, so revert it by restoring the file's saved bytes rather than by a second
   replacement. Report each exit code and the failing node ids, and a mutation that stays green as
   green. Restore both files, show that each is byte-identical to before, remove the worktree and
   show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in your
   final message only, since the handoff commit precedes it.
Full suite: NOT run this round (amend0917-throughput rule 1); it runs once, in the closure
sequence's integration-gate round, which is the next round.
-- end of block --
