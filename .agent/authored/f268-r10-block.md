-- STEP R10 deletion: the autorun `do` flow -- F268 remedy do: the one-command start --
Session 2 of F268 · round 10 · base `4362894d` (branch feature/f268-remedy-do, pushed).

Goal: book round 9's verdict and resolve R-0933; delete the `do` autorun flow round 9 left
without a caller, with its tests; the do guide and the do help describe the sequence.

Read first, completely: AGENTS.md; docs/agents/self_drive_protocol.md amendment
amend0906-triage-throughput (1) (a deletion round) and amend0917-throughput (1);
`packages/orchestration/do_run.py`; `packages/orchestration/autorun.py` (`dry_run_autorun`,
`_autonomy_label`, the module docstring); `docs/guides/do-run-v1.md`;
`packages/orchestration/do_sequence.py` (the steps, `DO_SEQUENCE`) and the `do.run` catalog
entry, which the rewritten guide describes.

PAYLOADS — reviewer-authored, gitignored scratch in `.remedy-wt/f268-r10/`. Verify each
sha256 before use; any mismatch -> stop and report. Apply byte-exact.
  ledger.md  sha256 67ce92eee2bb4e07c0930a8aa4393630d4a2d5b29469b8aa0276183b00ba48c6
  plan.md    sha256 34982dfec1047203fa92f2b0e61a719a072836d89bccbe840ba719d205d72ec2
  block.md   this block (save it as `.agent/authored/f268-r10-block.md`; report its digest)

Bundle (commit order):
C1 bookkeeping — one commit: byte copies of the payloads as `.agent/authored/f268-r10-<name>`;
   `.agent/live_review.md` := `git show 4362894d:.agent/live_review.md` bytes + ledger.md;
   `.agent/plan.md` := plan.md.
C2 production deletion — one commit. The reviewer's research helper measured at `4362894d`:
   (a) `do_run.py` keeps ONLY `DoRunNextAction`, `_REMEDY_CMD_RE` and
   `validate_next_safe_action_command` (`packages/orchestration/repair_loop.py` imports the
   first; several tests call the third), with a new module docstring saying what it now holds
   and the imports those three need; everything else in it goes (`DO_PHASES`, `DoRunPhase`,
   `DoRunStopReason`, `DoRunResult`, `_DO_V1_MAX_AUTONOMY`, `DoRunContract`, `_check_contract`,
   `run_do`, `_run_context_phase`, `_run_build_phase`, `_run_patch_intent_phase`,
   `_run_proof_phase`, `export_do_run_json`, `summarize_do_run`, `_do_emit`). Re-measure with
   a grep before deleting each; a symbol with a surviving caller outside this list: stop.
   (b) `autorun.py`: `dry_run_autorun` and `_autonomy_label` go; the module docstring stops
   naming them and stops calling the module `remedy do`'s loop. `run_autorun` stays (R-0927
   owns it).
   (c) the stale `do` text round 9 listed: the `do.run` catalog description ("Start a
   controlled autorun for a goal.") and `apps/cli/commands/do_cmd.py`'s module docstring
   describe the sequence (plan and run an order, stop before apply unless `--apply`);
   `tests/docs/test_vocabulary.py` binds description words — run it.
C3 test deletion — one commit, BY DESIGN, each checked against its body first and listed in the
   handoff with its reason: in `tests/orchestration/test_do_run.py` every test that calls or
   imports a deleted symbol (the helper counted 52 of 69; keep `TestNextSafeActionValidation`
   except its two tests that call `run_do`, `TestCatalogMetadataTruth`,
   `TestPhaseModel::test_next_action`, `::test_contract_defaults`, the three
   `TestContractConsolidation` tests that do not read a `run_do` result, and
   `TestApprovalGate::test_no_apply_import_in_do_run`), its dead helpers and imports, and its
   docstring; `tests/orchestration/test_run_contract.py`
   `TestApprovalGateRegression::test_no_fake_apply_phase`;
   `tests/orchestration/test_test_failure_repair.py` class `TestDoRunIntegration` and its
   docstring line naming it; `tests/cli/test_job_commands.py`
   `TestRemedyDo::test_dry_run_no_side_effects`, `::test_dry_run_phases_by_autonomy`;
   `tests/orchestration/test_test_runner.py` `TestPatchApplyTestLoop::test_autorun_has_test_phase`
   (it scans `autorun.py` for strings only `dry_run_autorun` held). Any other red: constraint 3.
C4 docs — one commit: `docs/guides/do-run-v1.md` is rewritten IN FULL (same path, same title
   line kept only if true) to describe `remedy do` as C2 leaves it: the steps of
   `DO_SEQUENCE` in order, what each does in one line, the stop before apply, `--plan-only`,
   `--step-by-step`, the `--json` keys `_cmd_do_order` prints, the flag list read from the
   `do.run` catalog entry, and the `Next:` line validator `validate_next_safe_action_command`;
   nothing about phases, autonomy levels or cycles; every source and test path it names
   exists (`tests/docs/test_named_source_paths.py`). `docs/system/run-contract-v1.md` lines 5,
   55 and 68 at `4362894d` stop naming `do_run` as a caller. `docs/guides/autocoder-usage.md`
   lines 152 and 160 stop naming `--max-cycles` (keep the token `repair_budget_exhausted`,
   which `tests/cli/test_do_cmd_summary.py` requires). `scripts/remedy_smoke.sh` line 1987's
   comment and line 2072's message stop saying a repair loop ran.
C5 handoff — rewrite `.agent/handoff.md` per docs/agents/handback_template.md:
   "SESSION 2 of feature F268 · round 10 · rounds so far 10"; per-commit tables with
   `git show --numstat` counts for every commit before C5; every gate's real output. Then
   `git push`.

Constraints:
1. Change set: the paths the Bundle names. Every commit < 500 inserted lines.
2. No test calls a real provider or starts a UI server; env vars only via `monkeypatch.setenv`;
   the shell denies `VAR=x cmd` and `cp` — copy bytes with python.
3. Never weaken an assertion or delete a test to pass beyond C3's list. A red you can repair
   inside this change set without touching a DECISION: repair it in its own commit and name
   it. Any other red: stop and report.
4. Build the appended file from `git show 4362894d:<path>` bytes plus the payload.
5. Commit messages "F268 R10 C<n>: <summary>", blank line,
   `Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>`. Never amend a pushed commit.
6. Do not touch docs/roadmap/**, `.claude/**`, `do_sequence.py`, `worker_queue.py`,
   `run_autorun`, `repair_loop.py`.

Done when (a deletion round: amend0906-triage-throughput (1) — no mutation red-proof of deleted
code; run each after C4, before C5; report literal output + real exit code):
G1 transport + state: payload digests matched; a python byte check prints True for the append
   against its `4362894d` bytes; `.agent/plan.md` byte-equal to plan.md.
G2 `python3 -m pytest -q -p no:cacheprovider tests/orchestration/test_do_run.py
   tests/orchestration/test_run_contract.py tests/orchestration/test_test_failure_repair.py
   tests/cli/test_job_commands.py tests/orchestration/test_test_runner.py
   tests/cli/test_do_cmd_summary.py tests/orchestration/test_autorun.py
   tests/orchestration/test_repair_loop_v1.py tests/orchestration/test_mission_readiness.py
   tests/orchestration/test_repair_request_builder.py tests/orchestration/test_self_dogfood.py
   tests/orchestration/test_self_dogfood_execution.py tests/regression/test_named_bugs.py
   tests/orchestration/test_import_reachability.py tests/test_remedy_smoke_script.py
   tests/test_cli_execution_loop_closure.py tests/cli/test_do_flags.py
   tests/cli/test_do_sequence_cli.py tests/cli/test_golden_path.py
   tests/cli/test_advertised_commands.py tests/cli/test_quick_start.py tests/docs/` -> 0 failed.
G3 absence at `4362894d` AND at C4, both counts and every hit at C4 printed: a python regex
   over tracked files under apps/, packages/, scripts/, tests/, docs/ (excluding
   docs/roadmap/) and README.md for
   `\brun_do\b|export_do_run_json|summarize_do_run|dry_run_autorun|_run_context_phase|_run_build_phase|_run_patch_intent_phase|_run_proof_phase|\bDoRunResult\b|\bDoRunPhase\b|\bDoRunStopReason\b|_autonomy_label`
   -> 0 at C4.
G4 `python3 -m ruff check` over every .py file the round touched -> "All checks passed!".
G5 `git status --porcelain` empty and the local tip equals origin after the push; `git worktree
   list` one row and the `remedy/job-*` branch count, both printed.
Full suite: NOT run (amend0917-throughput).
-- end of block --
