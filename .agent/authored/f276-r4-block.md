-- STEP R4 T003 -- F276 Data-root hygiene & disk budget --
Session 1 of F276 · round 4 · base `543863a0` (the round 3 handoff, the branch tip).

Goal: book round 3's verdict, resolve R-1002 with the reading the built command gives on the
operator's own root, and build T003 exactly as the reviewer's dry run built it: the copy-mode
lifecycle.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F276.md; the payload `decisions.md`
(DECISION F276 D5 — this round's spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f276-r4/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md            sha256 9b2e50af972c9b0b40cf7de5ec0a2d87d119dea501ba3801fd19eda2c31622b4
  decisions.md         sha256 989e18eb9651c333cf026324bd1c7e2d50d887b9a708d4ba0ed974c56153208d
  plan.md              sha256 51d8c896418fbf90029c21d3db930dc4d569dbd91520c6c83325ab593b1d9a49
  block.md             this block (save it; report its line count and digest)
CODE — ONE diff the reviewer produced from its own dry-run worktree at `543863a0`, applied there,
tested there and red-proved there. Apply it in three disjoint slices with the `--include` lists
below; do not retype or edit a hunk, and never apply it whole:
  `.remedy-wt/f276-r4/f276-r4.diff` sha256 a8262b6302b6a5c4036e8a87c056d68b44eba9796a105898a39f46c2cb774fe1

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of the four payloads above as
   `.agent/authored/f276-r4-<name>`; `.agent/live_review.md` := its `543863a0` bytes + ledger.md
   (it books round 3's PASS and resolves R-1002); `.agent/decisions.md` := its `543863a0` bytes +
   decisions.md; `.agent/plan.md` := plan.md.
C2 the release and the copy filters — `git apply --include=packages/orchestration/data_reclaim.py
   --include=packages/orchestration/staging_workspace.py .remedy-wt/f276-r4/f276-r4.diff`.
C3 the hook and its two layers — the same diff with
   `--include=packages/orchestration/pingpong_job.py
   --include=tests/orchestration/test_staging_lifecycle.py`.
C4 the docs — the same diff with `--include=docs/system/architecture.md
   --include=docs/roadmap/features/T2_F276.md`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F276 · round 4 · rounds so far 4" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output, one line per gate; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger;
   `## Next` naming Phase 1 rule 1, then the review of round 4, then T004, and "Operator questions
   open: <the count of `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push origin feature/f276-data-root-hygiene`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names, and nothing else. Every commit under 500 inserted lines;
   report each commit's own insertions from `git show --numstat`.
2. The shell denies `VAR=x cmd`, `cp` and compound commands; copy bytes and read exit codes with
   small python scripts under `.remedy-wt/f276-r4/`. `python3 -m apps.cli.grouped <group> <cmd>` is
   the runnable spelling of `remedy <group> <cmd>`.
3. Never weaken an assertion or delete a test. A red gate, or an ambiguity D5 does not settle ->
   stop, commit nothing half-done, report.
4. Build both edited `.agent/` record files from `git show 543863a0:<path>` bytes.
5. Commit messages "F276 R4 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never read, list or write the operator's `.data/`. Every test measures a tmp root, and every
   `REMEDY_DATA_DIR` is set in-process, never as a shell assignment. The new tests build real git
   repositories with `git init` in a tmp directory; if the sandbox refuses that, stop and report
   the refusal rather than skipping past it.
7. The production change is DESCRIBED by D5 and CARRIED by the diff: apply it, do not re-derive it.
   Each of C2 to C4 is green on its own; if one is not, stop at it and report which gate went red.

Done when (G1 to G5 at C4, before C5; report the literal output and the real exit code of each):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/live_review.md` equals its `543863a0` bytes + ledger.md, that `.agent/decisions.md`
   equals its `543863a0` bytes + decisions.md, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f276-r4-*` copy equals its payload. Report the saved block's line count and
   sha256 beside the ones this block's own bytes give.
G2 code transport: at C4, `git rev-parse <C4>:packages <C4>:apps <C4>:tests <C4>:docs` prints
   exactly 1cb7b9cf47cdcda2eb5b0c617f2a8673e45b416d, c6512f5298473ca4de84e8c8dbb811283c8e0f60,
   9ec093b7cefa773b20f9440f73a1f65a8001b43a and 67a539fe31ec58b441a21b1366a9c280526caff8 — the
   objects of the reviewer's dry run, the `apps` object being the base's, since this round touches
   nothing there. Also `git diff --name-only <C1> <C4>` names exactly the paths C2 to C4 name, and
   no other; report that list and its length.
G3 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_staging_lifecycle.py
   tests/orchestration/test_job_fulfillment.py tests/orchestration/test_data_reclaim.py
   tests/cli/test_data_cmd.py tests/orchestration/test_worktree_cleanup_paths.py
   tests/orchestration/test_job_worktree_handoff.py tests/orchestration/test_pingpong_job_dod_gate.py
   tests/orchestration/test_job_state_field.py tests/test_data_paths.py
   tests/test_data_root_classes.py tests/docs tests/cli/test_golden_path.py
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py
   tests/ui_contracts/test_humanize_catalog.py` in the primary checkout, serial (no `-n`) ->
   summary line, 0 failed, exit 0.
G4 `python3 -m ruff check packages/orchestration/staging_workspace.py
   packages/orchestration/data_reclaim.py packages/orchestration/pingpong_job.py
   tests/orchestration/test_staging_lifecycle.py` -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -q --no-header -rf -p no:cacheprovider
   tests/orchestration/test_staging_lifecycle.py tests/orchestration/test_data_reclaim.py
   tests/orchestration/test_job_fulfillment.py tests/cli/test_data_cmd.py`, `__pycache__` purged
   before each run, the imported `packages.orchestration.staging_workspace` path printed first to
   prove it resolves inside the worktree. The UNMUTATED control first (expect exit 0). Then, each
   reverted byte-identically before the next, the mutated bytes counted in the named file first
   (each count must be 1): (a) in `pingpong_job._finalize_job_workspace` the line
   `        if job.state == JOB_COMPLETED and not job.result_diff_error:` and the
   `_release_job_workspace_copy(job)` line under it deleted, so the copy branch only returns;
   (b) that same condition line replaced by `        if job_is_terminal(job.state):`, widening the
   hook to reclaim's vocabulary; (c) in `staging_workspace.py` the line
   `MAX_COPY_FILE_BYTES: int = 16 * 1024 * 1024` replaced by
   `MAX_COPY_FILE_BYTES: int = 1 << 62`. Report each exit code and the failing node ids, and a
   mutation that stays green as green. Restore every file, show that each is byte-identical to
   before, remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in your
   final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput rule 1).
-- end of block --
