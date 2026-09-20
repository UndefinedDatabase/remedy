-- STEP R3 T002b -- F276 Data-root hygiene & disk budget --
Session 1 of F276 · round 3 · base `94441e34` (the round 2 handoff, the branch tip).

Goal: book round 2's verdict, register R-1002 — measured on the operator's own data root — and
repair it under DECISION F276 D4: `data reclaim --orphans`, default off.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F276.md; the payload `decisions.md`
(DECISION F276 D4 — this round's spec; where this block is terser, it rules); and the payload
`ledger.md`, whose R-1002 paragraph is the finding this round repairs.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f276-r3/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md            sha256 29e0041a0a7eed721c239650df59d9a8a2be1165cbf8edc614d2b6f4b978eda9
  decisions.md         sha256 ccf099d74a1f27f376711276367aeec7715f619c019120f9857765ca460e70f8
  plan.md              sha256 bd1dffe01d515b4708906774f6b60db231166ccb38968876a8bfd18e88f0e8fc
  block.md             this block (save it; report its line count and digest)
CODE — ONE diff the reviewer produced from its own dry-run worktree at `94441e34`, applied there,
tested there and red-proved there. Apply it in three disjoint slices with the `--include` lists
below; do not retype or edit a hunk, and never apply it whole:
  `.remedy-wt/f276-r3/f276-r3.diff` sha256 f73bcd11fbcb3ab9072bb98608d6c8aa558ce51677d725a158dacbb9fdc95b93

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of the four payloads above as
   `.agent/authored/f276-r3-<name>`; `.agent/live_review.md` := its `94441e34` bytes + ledger.md
   (it books round 2's PASS and registers R-1002); `.agent/decisions.md` := its `94441e34` bytes +
   decisions.md; `.agent/plan.md` := plan.md.
C2 the orphan rule — `git apply --include=packages/orchestration/data_reclaim.py
   --include=apps/cli/command_catalog.py --include=apps/cli/commands/data_cmd.py
   --include=tests/cli/test_data_cmd.py .remedy-wt/f276-r3/f276-r3.diff`.
C3 the behaviour tests — the same diff with
   `--include=tests/orchestration/test_data_reclaim.py`.
C4 the docs — the same diff with `--include=docs/system/architecture.md
   --include=docs/roadmap/features/T2_F276.md`.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F276 · round 3 · rounds so far 3" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C4; every gate's
   real output, one line per gate; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; a line
   `Landed: R-1002` naming its commit (in the handoff only — never a `Done:` line anywhere);
   `## Next` naming Phase 1 rule 1, then the review of round 3, then T003, and "Operator questions
   open: <the count of `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push origin feature/f276-data-root-hygiene`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names, and nothing else. Every commit under 500 inserted lines;
   report each commit's own insertions from `git show --numstat`.
2. The shell denies `VAR=x cmd`, `cp` and compound commands; copy bytes and read exit codes with
   small python scripts under `.remedy-wt/f276-r3/`. `python3 -m apps.cli.grouped <group> <cmd>` is
   the runnable spelling of `remedy <group> <cmd>`.
3. Never weaken an assertion or delete a test. A red gate, or an ambiguity D4 does not settle ->
   stop, commit nothing half-done, report.
4. Build both edited `.agent/` record files from `git show 94441e34:<path>` bytes.
5. Commit messages "F276 R3 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never read, list or write the operator's `.data/`. Every test measures a tmp root, and every
   `REMEDY_DATA_DIR` is set in-process, never as a shell assignment.
7. The production change is DESCRIBED by D4 and CARRIED by the diff: apply it, do not re-derive it.
   Each of C2 to C4 is green on its own; if one is not, stop at it and report which gate went red.

Done when (G1 to G5 at C4, before C5; report the literal output and the real exit code of each):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/live_review.md` equals its `94441e34` bytes + ledger.md, that `.agent/decisions.md`
   equals its `94441e34` bytes + decisions.md, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f276-r3-*` copy equals its payload. Report the saved block's line count and
   sha256 beside the ones this block's own bytes give.
G2 code transport: at C4, `git rev-parse <C4>:packages <C4>:apps <C4>:tests <C4>:docs` prints
   exactly bdb14143c4f4af92a38e114060b0feca88157bb4, c6512f5298473ca4de84e8c8dbb811283c8e0f60,
   73d3a71f1212275906c453ff300655e00d39636d and 32845b649f7f57e021f598ccd60d87aaaa52530b — the
   objects of the reviewer's dry run. Also `git diff --name-only <C1> <C4>` names exactly the paths
   C2 to C4 name, and no other; report that list and its length.
G3 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_data_reclaim.py
   tests/cli/test_data_cmd.py tests/test_data_root_classes.py
   tests/orchestration/test_data_footprint.py tests/test_command_catalog.py
   tests/cli/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_cli_ux.py
   tests/cli/test_advertised_commands.py tests/test_no_orphan_modules.py
   tests/orchestration/test_import_reachability.py tests/orchestration/test_dead_command_check.py
   tests/docs tests/orchestration/test_roadmap_index.py tests/cli/test_golden_path.py` in the
   primary checkout, serial (no `-n`) -> summary line, 0 failed, exit 0.
G4 `python3 -m ruff check packages/orchestration/data_reclaim.py apps/cli/commands/data_cmd.py
   apps/cli/command_catalog.py tests/orchestration/test_data_reclaim.py tests/cli/test_data_cmd.py`
   -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C4, run from the worktree
   root with `python3 -B -m pytest -q --no-header -rf -p no:cacheprovider
   tests/orchestration/test_data_reclaim.py tests/cli/test_data_cmd.py`, `__pycache__` purged before
   each run, the imported `packages.orchestration.data_reclaim` path printed first to prove it
   resolves inside the worktree. The UNMUTATED control first (expect exit 0). Then, each reverted
   byte-identically before the next, the mutated bytes counted in the named file first (each count
   must be 1): (a) in `data_reclaim.py` the line `ORPHAN_MIN_AGE_DAYS: float = 1.0` replaced by
   `ORPHAN_MIN_AGE_DAYS: float = 0.0`; (b) in `data_reclaim.apply_reclaim` the two lines that call
   `_orphan_deletion_refusal` — the `if not reason and cand.job_state == ORPHAN_JOB_STATE:` line and
   the assignment under it — deleted; (c) in `apps/cli/commands/data_cmd.py` the block that prints
   the `job_unresolved` hint line, guarded by `if not orphans:`, made unreachable. Report each exit
   code and the failing node ids, and a mutation that stays green as green. Restore every file, show
   that each is byte-identical to before, remove the worktree and show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in your
   final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput rule 1).
-- end of block --
