-- STEP R2 T001 -- F273 Findings paydown v1 --
Session 1 of F273 · round 2 · base `f32363e9` (the round 1 handoff, branch
`feature/f273-findings-paydown-v1`).

Goal: book round 1's verdict and the resolutions of R-0804 and R-0810, land DECISION F273 D2,
repair the five tests round 1 left red, and build R-0812 and R-0807 exactly as the reviewer's dry
run built them.

Read first, completely: AGENTS.md; the payload `decisions.md` (DECISION F273 D2 — this round's
spec; where this block is terser, it rules).

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f273-r2/`. Verify each sha256
before use; any mismatch -> stop and report. Apply byte-exact; never retype.
  plan.md              sha256 936d0ef48346c9c93ec59e69a7ec3bb79f292ae45e834168e4cfb8bc28df13d8
  ledger.md            sha256 ffb7355b6b31f9bb2dba0f645b6c738c832f48e6b2cf63967c21df7cb6c2085f
  slips.md             sha256 34e899e8f8f8798baad7c05373aa01893320d75e71f82c7e71f24af65fff2711
  decisions.md         sha256 a6243a43168b5ff0e7afd9762ed7d3cf4f8b9febb79b88d1080a3b3b4de9c9fe
  block.md             this block (save it; report its digest)
CODE — three diffs research helpers built at `f32363e9`, which the reviewer applied in this order,
ran and red-proved in its own worktree. Apply with `git apply`; never retype or edit a hunk:
  `.remedy-wt/f273-proto-r1fix.diff` sha256 300b51c57d774b1ff1ea330c1e849e661dc724ab677dcb1e50be3149a8d60b8b
  `.remedy-wt/f273-proto-r0812.diff` sha256 3eeae7bf40f0439f131be765eb59769e3b0b9942ccea7fc512a9e406ade0fe16
  `.remedy-wt/f273-proto-r0807.diff` sha256 68d4e7f231a1654c2ae410ef9a33a487333e924e7446a0238cfc67e7609590da

Bundle (commit order):
C1 bookkeeping — one commit holding exactly: byte copies of every payload above as
   `.agent/authored/f273-r2-<name>`; `.agent/plan.md` := plan.md; `.agent/live_review.md` := its
   `f32363e9` bytes + ledger.md bytes; `.agent/prose_slips.md` := its `f32363e9` bytes + slips.md
   bytes; `.agent/decisions.md` := its `f32363e9` bytes + decisions.md bytes.
C2 round 1's reds — `git apply .remedy-wt/f273-proto-r1fix.diff`.
C3 R-0812 — `git apply .remedy-wt/f273-proto-r0812.diff`.
C4 R-0807 code and tests — `git apply --exclude=docs/roadmap/features/T2_F103.md
   .remedy-wt/f273-proto-r0807.diff`.
C5 R-0807 docs — `git apply --include=docs/roadmap/features/T2_F103.md
   .remedy-wt/f273-proto-r0807.diff`.
C6 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md: Session section
   "SESSION 1 of feature F273 · round 2 · rounds so far 2" plus one sentence of context
   self-assessment; per-commit tables with `git show --numstat` counts for C1 to C5; every gate's
   real output; open findings by distinct id AND by the canonical line formula
   (`scripts/rotate_live_review.py::count_open_findings`), measured on the committed ledger; lines
   `Landed: R-0812` and `Landed: R-0807`, each naming its commit, in the handoff only — never a
   `Done:` line anywhere; `## Next` naming Phase 1 rule 1 then the review of round 2, and
   "Operator questions open: <the count you read from the file>". Then `git push`. Open no pull
   request.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider. The shell denies `VAR=x cmd`, `cp`, compound commands and `cd`
   before git; copy bytes and read exit codes with small python scripts under
   `.remedy-wt/f273-r2/` (`.remedy-wt/f273-r1/run.py <N> cmd...` prints the last N lines and
   `EXIT <code>`), and pass `cwd` explicitly — round 1 ran two gates in the wrong checkout.
3. Never weaken an assertion or delete a test. A red gate or an ambiguity D2 does not settle ->
   stop, commit nothing half-done, report. Never use `git stash`: its stack is shared.
4. Build every edited `.agent/` file from `git show f32363e9:<path>` bytes.
5. Commit messages "F273 R2 C<n>: <summary>", blank line, then
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Never list, read or write any `.data/` yourself.

Done when (G1 to G5 at C5, before C6; report literal output and the real exit code):
G1 transport + state: every payload and diff digest matched; a python check prints True that
   `.agent/plan.md` equals its payload, that `.agent/live_review.md`, `.agent/prose_slips.md` and
   `.agent/decisions.md` each equal their `f32363e9` bytes + ledger.md, slips.md and decisions.md
   respectively, and that each `.agent/authored/f273-r2-*` copy equals its payload.
G2 code transport: `git rev-parse <C5>:tests <C5>:packages <C5>:apps <C5>:docs` prints exactly
   44f3310aababca7cab8ff948f05a00bb7fa099b7, 5753db4d19ac2331a1157a7362790d4fbcfd97db,
   669c3a23f24a5dca64f2fc47dbd708c9084a1239 and b459d7c5dd6453012cc686a768b55d7cd0a8fadd (the
   reviewer's dry-run subtrees).
G3 in the primary checkout, serial (no `-n`): `python3 -m pytest -q -p no:cacheprovider
   tests/orchestration/test_config.py tests/orchestration/test_one_job_store.py
   tests/ui_server/test_handler_table_walk.py tests/test_data_root_isolation.py
   tests/orchestration/test_teacher_narration.py tests/cli/test_teacher_cmd.py
   tests/cli/test_do_sequence_cli.py tests/ui_contracts/test_humanize_catalog.py
   tests/test_timeline.py tests/test_trust_report.py tests/ui_server/test_brain_view_model.py
   tests/orchestration/test_pingpong_cli.py tests/orchestration/test_token_ledger.py
   tests/orchestration/test_job_evidence.py tests/cli/test_do_evidence_package.py
   tests/cli/test_stats_cost.py tests/orchestration/test_budget_guard.py
   tests/orchestration/test_provider_evidence_integration.py tests/cli/test_golden_path.py
   tests/docs/ tests/orchestration/test_roadmap_index.py tests/test_cockpit.py
   tests/test_project_brain.py tests/orchestration/test_budget_tick.py tests/cli/test_job_show.py`
   -> summary line, 0 failed, exit 0, no `R-0803:` line.
G4 `python3 -m ruff check --output-format concise` over the Python files C2 to C4 touch -> exactly
   one finding, `tests/cli/test_teacher_cmd.py:622:9: I001`, the import block that reads at line
   545 at `f32363e9` (pre-existing; T005 clears every ruff finding) — report the full output.
G5 mutation red-proofs in ONE disposable worktree under `.remedy-wt/` at C5, run from its root
   with `python3 -B -m pytest -q -p no:cacheprovider`, `__pycache__` purged before each run, the
   imported `packages.orchestration.token_ledger` path printed first to prove it resolves inside
   the worktree. The UNMUTATED control first over the test files named below (exit 0). Then, each
   reverted before the next, counting the mutated bytes in the named file first (each must be 1):
   (a) `token_ledger.py`: the line `    return f"{call_id_for_task_run(job_id, task_id)}:{seq}"`
   replaced by `    return call_id_for_task_run(job_id, task_id)` ->
   `tests/orchestration/test_token_ledger.py` and `tests/cli/test_do_sequence_cli.py` must fail;
   (b) `pingpong_loop.py`:
   the line `            **_attempt_usage_evidence(a.usage_actuals),` deleted ->
   `tests/orchestration/test_token_ledger.py` must fail; (c) `teacher_narration.py`: the two lines
   of the `"task_round_completed":` entry deleted -> `tests/cli/test_teacher_cmd.py` must fail;
   (d) `pingpong_job.py`: the line `            _log_task_rounds(task_log, task, result)` deleted
   -> `tests/cli/test_teacher_cmd.py` and `tests/cli/test_do_sequence_cli.py` must fail. Report
   exit codes and failing ids, and a mutation that stays green as green. Remove the worktree and
   show `git worktree list`.
G6 after the push: `git status --porcelain` empty and the local tip equals origin — reported in
   your final message only, since the handoff commit precedes it.
Full suite: NOT run (amend0917-throughput).
-- end of block --
