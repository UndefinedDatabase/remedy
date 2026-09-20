-- STEP R2 T002 -- F276 Data-root hygiene & disk budget --
Session 1 of F276 · round 2 · base `96fd8f9c` (the round 1 handoff, the branch tip).

Goal: book round 1's verdict, resolve R-1001, land DECISION F276 D3, and build T002 exactly as the
reviewer's dry run built it: `remedy data reclaim`, dry run by default.

Read first, completely: AGENTS.md; docs/roadmap/features/T2_F276.md; the payload `decisions.md`
(DECISION F276 D3 — this round's spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f276-r2/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  ledger.md            sha256 4fe2f5164e66b28e911d209393e06806707e18513d4e28e54c20cb830e972d00
  decisions.md         sha256 8a6310a417dac83f37235030d59f36252c2be9fddbf3fb57b91b27fb77d7267b
  plan.md              sha256 8857ce549bb307dc56cb71d8c331323d67122efa752d324fcf901e3e78b2b305
  block.md             this block (save it; report its line count and digest)
CODE — ONE diff the reviewer produced from its own dry-run worktree at `96fd8f9c`, applied there,
tested there and red-proved there. Apply it in five disjoint slices with the `--include` lists
below; do not retype or edit a hunk, and never apply it whole:
  `.remedy-wt/f276-r2/f276-r2.diff` sha256 bf3a73bfa2d27e7a087ef2d8c11ea0518c8032e78d9e90e653692d36eb49d7d2

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of the four payloads above as
   `.agent/authored/f276-r2-<name>`; `.agent/live_review.md` := its `96fd8f9c` bytes + ledger.md
   (it books round 1's PASS, the measurement of the operator's data root, and the resolution of
   R-1001); `.agent/decisions.md` := its `96fd8f9c` bytes + decisions.md; `.agent/plan.md` :=
   plan.md.
C2 the terminal-state vocabulary — `git apply --include=packages/orchestration/pingpong_job.py
   --include=apps/cli/commands/status_cmd.py .remedy-wt/f276-r2/f276-r2.diff`.
C3 the D3 registry moves and the footprint helper — the same diff with
   `--include=packages/orchestration/data_paths.py
   --include=packages/orchestration/data_footprint.py`.
C4 the reclaim module and its importer — the same diff with
   `--include=packages/orchestration/data_reclaim.py --include=apps/cli/commands/data_cmd.py
   --include=tests/orchestration/import_reachability_allowlist.txt`.
C5 the catalog entry and the flag test — the same diff with
   `--include=apps/cli/command_catalog.py --include=tests/cli/test_data_cmd.py`.
C6 the behaviour tests and the docs — the same diff with
   `--include=tests/orchestration/test_data_reclaim.py --include=docs/system/architecture.md
   --include=docs/roadmap/features/T2_F276.md`.
C7 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F276 · round 2 · rounds so far 2" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C6; every gate's
   real output, one line per gate; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; `## Next`
   naming Phase 1 rule 1, then the review of round 2, then T003, and "Operator questions open: <the
   count of `### Q` headings you read from `.agent/operator_questions.md`>". Then
   `git push origin feature/f276-data-root-hygiene`. Open no pull request.

Constraints:
1. Change set: the paths the Bundle names, and nothing else. Every commit under 500 inserted lines;
   report each commit's own insertions from `git show --numstat`.
2. The shell denies `VAR=x cmd`, `cp` and compound commands; copy bytes and read exit codes with
   small python scripts under `.remedy-wt/f276-r2/`. `python3 -m apps.cli.grouped <group> <cmd>` is
   the runnable spelling of `remedy <group> <cmd>`.
3. Never weaken an assertion or delete a test. A red gate, or an ambiguity D3 does not settle ->
   stop, commit nothing half-done, report.
4. Build both edited `.agent/` record files from `git show 96fd8f9c:<path>` bytes.
5. Commit messages "F276 R2 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never read, list or write the operator's `.data/`. Every test measures a tmp root.
7. The production change is DESCRIBED by D3 and CARRIED by the diff: apply it, do not re-derive it.
   Each of C2 to C6 is green on its own; if one is not, stop at it and report which gate went red.

Done when (G1 to G5 at C6, before C7; report the literal output and the real exit code of each):
G1 transport + state: every payload digest matched; a python check prints True that
   `.agent/live_review.md` equals its `96fd8f9c` bytes + ledger.md, that `.agent/decisions.md`
   equals its `96fd8f9c` bytes + decisions.md, that `.agent/plan.md` equals plan.md, and that each
   `.agent/authored/f276-r2-*` copy equals its payload. Report the saved block's line count and
   sha256 beside the ones this block's own bytes give.
G2 code transport: at C6, `git rev-parse <C6>:packages <C6>:apps <C6>:tests <C6>:docs` prints
   exactly e92f2ef2352b2f551ad8975ac88ffb9b587f1c7c, 49e01420b6d44b6aca9043159e9cb968d43c63e4,
   c087f446bb98a4515891bfc464632bba74997856 and 09b32267e9f49a7d3497bbb8147eb2316a64c407 — the
   objects of the reviewer's dry run. Also `git diff --name-only <C1> <C6>` names exactly the paths
   C2 to C6 name, and no other; report that list and its length.
G3 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_data_reclaim.py
   tests/cli/test_data_cmd.py tests/test_data_root_classes.py
   tests/orchestration/test_data_footprint.py tests/test_command_catalog.py
   tests/cli/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_cli_ux.py
   tests/cli/test_advertised_commands.py tests/test_no_orphan_modules.py
   tests/orchestration/test_import_reachability.py tests/orchestration/test_dead_command_check.py
   tests/docs tests/orchestration/test_roadmap_index.py tests/orchestration/test_job_plan.py
   tests/orchestration/test_job_plan_state_reads.py tests/test_data_paths.py
   tests/test_data_root_isolation.py tests/test_run_log.py tests/test_timeline.py
   tests/orchestration/test_repository_snapshot.py tests/orchestration/test_job_evidence.py
   tests/cli/test_golden_path.py` in the primary checkout, serial (no `-n`) -> summary line, 0
   failed, exit 0.
G4 `python3 -m ruff check apps/cli/command_catalog.py apps/cli/commands/data_cmd.py
   apps/cli/commands/status_cmd.py packages/orchestration/data_footprint.py
   packages/orchestration/data_paths.py packages/orchestration/data_reclaim.py
   packages/orchestration/pingpong_job.py tests/cli/test_data_cmd.py
   tests/orchestration/test_data_reclaim.py` -> "All checks passed!".
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C6, run from the worktree
   root with `python3 -B -m pytest -q -p no:cacheprovider tests/orchestration/test_data_reclaim.py
   tests/cli/test_data_cmd.py`, `__pycache__` purged before each run, the imported
   `packages.orchestration.data_reclaim` path printed first to prove it resolves inside the
   worktree. The UNMUTATED control first (expect exit 0). Then, each reverted byte-identically
   before the next, the mutated bytes counted in the named file first (each count must be 1):
   (a) `return True` inserted as the first statement of `pingpong_job.job_is_terminal`;
   (b) in `data_reclaim.apply_reclaim` the line `    for cand in plan.candidates:` replaced by a
   loop over every direct child of every ephemeral class directory, so the plan is ignored;
   (c) in `apps/cli/commands/data_cmd.py` the line
   `    outcome = apply_reclaim(plan) if apply_it else None` replaced by
   `    outcome = apply_reclaim(plan)`, so the dry run deletes;
   (d) DECISION D3 undone for `runs`: its entry moved from `DURABLE_CLASSES` back into
   `EPHEMERAL_CLASSES` and `"runs": ""` added to `data_reclaim._JOB_KEYED_PREFIXES`.
   Report each exit code and the failing node ids, and a mutation that stays green as green.
   Restore every file, show that each is byte-identical to before, remove the worktree and show
   `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in your
   final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput rule 1).
-- end of block --
