-- STEP R5 T003 REPAIR -- F276 Data-root hygiene & disk budget --
Session 1 of F276 · round 5 · base `a112e1fa` (the round 4 handoff, the branch tip).

Goal: book round 4's verdict, register R-1003, R-1004 and R-1005, and repair R-1003 exactly as the
reviewer's dry run repaired it: the staging copy is freed by `job apply`, never by the hook.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F276.md; the payload `decisions.md`
(DECISION F276 D6 — this round's spec; where this block is terser, it rules); and the payload
`ledger.md`, whose R-1003 paragraph is the regression this round repairs.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f276-r5/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md            sha256 762cdb1275ca6fbacbc46163b0a4b68af32d23a7a2b1042d8594909b07f5963d
  decisions.md         sha256 1b636d191e4a68157046b23589a9c0cd7d61995f3e1d7ef21c2dc1e6080fb531
  plan.md              sha256 9e9b9cdc1bf0db6381e0c3e44fab2964948431316dde416f7daaef6437cfa4bc
  prose_slips.md       sha256 93e4004e4c0da7f33779e84fd78af4528ccfc4978f77eabe21a72287e6568ff2
  block.md             this block (save it; report its line count and digest)
CODE — ONE diff the reviewer produced from its own dry-run worktree at `a112e1fa`, applied there,
tested there and red-proved there. Apply it in two disjoint slices with the `--include` lists below;
do not retype or edit a hunk, and never apply it whole:
  `.remedy-wt/f276-r5/f276-r5.diff` sha256 c25db3b7e789e57c9e19257f256c86e40a4ebf6a9975b8e2a41188c7a944bb34

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of the five payloads above as
   `.agent/authored/f276-r5-<name>`; `.agent/live_review.md` := its `a112e1fa` bytes + ledger.md
   (it books round 4's verdict and registers the three findings); `.agent/decisions.md` := its
   `a112e1fa` bytes + decisions.md; `.agent/prose_slips.md` := its `a112e1fa` bytes +
   prose_slips.md; `.agent/plan.md` := plan.md.
C2 the repair and its tests — `git apply --include=packages/orchestration/pingpong_job.py
   --include=packages/orchestration/job_apply.py
   --include=tests/orchestration/test_staging_lifecycle.py
   --include=tests/orchestration/test_job_apply.py .remedy-wt/f276-r5/f276-r5.diff`. Production and
   tests land together here by necessity: code first leaves the old hook assertions red, tests
   first leaves the new ones red.
C3 the docs — the same diff with `--include=docs/system/architecture.md
   --include=docs/roadmap/features/T2_F276.md`.
C4 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F276 · round 5 · rounds so far 5" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C3; every gate's
   real output, one line per gate; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; a line
   `Landed: R-1003` naming its commit (in the handoff only — never a `Done:` line anywhere);
   `## Next` naming Phase 1 rule 1, then the review of round 5, then T004, and "Operator questions
   open: <the count of `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push origin feature/f276-data-root-hygiene`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names, and nothing else. Every commit under 500 inserted lines;
   report each commit's own insertions from `git show --numstat`.
2. The shell denies `VAR=x cmd`, `cp` and compound commands; copy bytes and read exit codes with
   small python scripts under `.remedy-wt/f276-r5/`. `python3 -m apps.cli.grouped <group> <cmd>` is
   the runnable spelling of `remedy <group> <cmd>`.
3. Never weaken an assertion or delete a test. A red gate, or an ambiguity D6 does not settle ->
   stop, commit nothing half-done, report.
4. Build every edited `.agent/` record file from `git show a112e1fa:<path>` bytes.
5. Commit messages "F276 R5 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never read, list or write the operator's `.data/`. Every test measures a tmp root, and every
   `REMEDY_DATA_DIR` is set in-process, never as a shell assignment.
7. The production change is DESCRIBED by D6 and CARRIED by the diff: apply it, do not re-derive it.

Done when (G1 to G5 at C3, before C4; report the literal output and the real exit code of each):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/live_review.md`, `.agent/decisions.md` and `.agent/prose_slips.md` each equal their
   `a112e1fa` bytes plus their payload, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f276-r5-*` copy equals its payload. Report the saved block's line count and
   sha256 beside the ones this block's own bytes give.
G2 code transport: at C3, `git rev-parse <C3>:packages <C3>:apps <C3>:tests` prints exactly
   9e1b3373800e449a81a7ebb2f2f56975d0b58297, c6512f5298473ca4de84e8c8dbb811283c8e0f60 and
   0f4b7d2c49dc32ab41f5ba8acacda65f4ee32b66, and `git rev-parse <C3>:docs/system/architecture.md
   <C3>:docs/roadmap/features/T2_F276.md` prints 8a44350174409c3ddc6900e8098c786c43f4cbc4 and
   9867b144cba64de8a17e3d2e3266a1f8275b47ab — the objects of the reviewer's dry run, the `apps`
   object being the base's, since this round touches nothing there. Also `git diff --name-only
   <C1> <C3>` names exactly the paths C2 and C3 name, and no other; report that list and its length.
G3 THE CONSUMER FIRST: `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_job_apply.py tests/orchestration/test_staging_lifecycle.py
   tests/orchestration/test_data_reclaim.py tests/cli/test_data_cmd.py
   tests/orchestration/test_job_fulfillment.py tests/orchestration/test_worktree_cleanup_paths.py
   tests/orchestration/test_job_worktree_handoff.py tests/cli/test_golden_path.py tests/docs
   tests/test_no_orphan_modules.py tests/orchestration/test_import_reachability.py` in the primary
   checkout, serial (no `-n`) -> summary line, 0 failed, exit 0. Then the measured pair, as two
   separate readings with their exit codes: `tests/orchestration/test_job_apply.py` alone at C3,
   and the same file alone at `a112e1fa` in a disposable worktree (19 red there is the regression
   this round repairs, and it is expected).
G4 `python3 -m ruff check packages/orchestration/pingpong_job.py
   packages/orchestration/job_apply.py tests/orchestration/test_staging_lifecycle.py
   tests/orchestration/test_job_apply.py` -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C3, run from the worktree
   root with `python3 -B -m pytest -q --no-header -rf -p no:cacheprovider
   tests/orchestration/test_staging_lifecycle.py tests/orchestration/test_job_apply.py`,
   `__pycache__` purged before each run, the imported `packages.orchestration.job_apply` path
   printed first to prove it resolves inside the worktree. The UNMUTATED control first (expect
   exit 0). Then, each reverted byte-identically before the next, the mutated bytes counted in the
   named file first (each count must be 1): (a) in `job_apply.py` the line
   `    _release_consumed_staging_copy(job, copy_out)` replaced by a `pass` statement; (b) in
   `pingpong_job._finalize_job_workspace` the two lines `    if handle is None:` and its `return`
   replaced by that branch releasing a completed copy job again, which must redden the guard
   `test_a_completed_copy_job_keeps_its_staging_copy_through_the_hook` and the nodes of
   `test_job_apply.py`. Report each exit code and the failing node ids, and a mutation that stays
   green as green. Restore both files, show that each is byte-identical to before, remove the
   worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in your
   final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput rule 1).
-- end of block --
