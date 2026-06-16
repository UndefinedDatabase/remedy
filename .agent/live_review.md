# Live Review — Steps 1877-1916: Real Test Execution + Snapshot/Rollback Proof v1

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): bounded allowlisted test execution + test-run result models/storage + private output
refs + safe public summaries + failure artifact integration + snapshot proof metadata + rollback
proof metadata + mission contract gate integration + proof chain integration + CLI visibility +
catalog/run_contract entries + progress/feature/review/cockpit summaries + integrity + docs/tests.
Must NOT: Claude/Pi/OpenCode/Ollama/provider/local-model execution; worker execution; ARBITRARY
command execution; shell=True; auto-apply; auto-approval; autonomous repair execution; auto-PR/git;
MemPalace; embeddings/vector DB; UI redesign; MCP.
HIGH-RISK BLOCK — first real subprocess execution. Hard invariants: ONLY allowlisted test commands
run; arbitrary commands blocked; NO shell=True; timeout + output caps mandatory; cwd controlled + env
sanitized; no background exec; raw stdout/stderr NEVER public; failed/timeout → safe failure artifact;
snapshot metadata must not claim real restore; rollback proof distinguishes restore_available vs
restore_tested (no fake rollback-ready); mission test gate consumes honestly (failed test blocks, no
fake pass); proof chain safe IDs only (no event-only fake promotion); no worker/provider/model exec.
Timestamp: 2026-06-16

## Verdict (reviewer-owned)
**PASS** @ 7230268 — ZERO open findings (R-0104 Resolved). All 11 checks PASS; targeted suite 264
passed @ 7230268 (602 @ cb2c640 unchanged); no forbidden execution path (no shell=True / arbitrary cmd
/ provider / worker / network); no raw leak; honest snapshot/rollback (no fake restore/rollback-ready);
no fake test pass; English-only; changed-files table present. Merge-ready (zero open). Auto-merge
applies on reviewer PASS per merge-autonomy; NO PR opened (user has not asked).

## Check matrix (reviewed @ cb2c640, re-verified @ 7230268)
1. Mainline closure — PASS. Overnight Mission v0 reviewer PASS @ 90768fd merged via PR #72 → main
   `aacafbd`. Fresh branch off merged main; no work before closure. (Baseline `test_execution_service.py`
   /`repository_snapshot.py` reviewed for runner safety — see checks 3/4.)
2. Test execution model — PASS. `TestRunResult`/`SnapshotProof`/`RollbackProof` bounded; `to_dict`
   scrubs safe_summary(≤300) + `_safe_path_label` on repo_path; raw output referenced by `output_ref`
   only; explicit statuses incl BLOCKED_BY_POLICY/CONTRACT/TIMEOUT.
3. Command resolution — PASS. `resolve_allowed_command`: unknown id blocked; `purpose != "test"`
   blocked; `_argv_is_safe` rejects shell metachars (`; | & $ \` > < && ||`) + forbidden/destructive
   programs (rm/dd/sudo/curl/wget/pip/npm/git/ssh/chmod…). Runner adds `_EXECUTION_SAFE_EXECUTABLES`
   allowlist + high-risk block.
4. Bounded runner — PASS. `_run_isolated_process`: `subprocess.Popen(argv_list)` — NO shell=True;
   `cwd` set; `env=_build_safe_env` (strips secret-key patterns, allowlist prefixes); stdin=DEVNULL;
   stdout/stderr→file (not public); `start_new_session=True`; `close_fds=True`; timeout via
   `wait(timeout=)` clamped [5s,600s]; TimeoutExpired→SIGTERM→SIGKILL process-group; synchronous (no
   background); output capped 1 MiB + truncation marker.
5. Snapshot/Rollback proof — PASS. Snapshot metadata-only: `restore_available=False` always (inventory
   hash, no content). Rollback: `restore_tested=False` always; `restore_available` only when
   `build_snapshot_truth` recovery verified AND snapshot not metadata-only; limitations surfaced. No
   fake rollback-ready.
6. Failure artifact integration — PASS. Failed/timeout → runner `failure_artifact_id` threaded into
   result; raw output stays `output_ref`; `next_safe_action` catalog-valid (`remedy test result/status/
   discover`).
7. Mission/proof integration — PASS. Latest REAL test run overrides `tests_status` (passed→green,
   failed/timeout→failing); `require_tests_green` + failing → missing_proofs → blocks satisfaction (no
   fake pass). New `rollback_restore_available` gate; snapshot/rollback gates block when not recorded/
   available. Proof references safe IDs only.
8. CLI/catalog/run_contract — PASS. `test result/list/integrity`+`snapshot/rollback show`=read_only;
   `snapshot/rollback create`=write_metadata; execution stays on existing capability-gated `RUN_TEST`/
   `repo_test_run`; no generic `may_execute_commands` for shell.
9. Surfacing — PASS. Ledger/bundle/cockpit safe summaries (status/counts/IDs); no raw output; no fake
   live run / fake pass / fake rollback availability.
10. Integrity — PASS. `audit_test_run_safety` (passed_with_nonzero_exit, raw_or_secret_in_public,
    absolute_path_in_public) + `audit_rollback_safety` (restore_tested_without_available,
    restore_available_on_metadata_snapshot) + `test_execution_integrity` (snapshot_metadata_claims_
    restore). Failed-satisfies-tests_green & satisfied-mission-with-failing-latest-test enforced via
    mission evaluate + `audit_evaluation_safety`; non-catalog next-action covered by catalog parser.
11. Architecture guards — PASS. `real_test_execution.py` facade = stdlib + provider_trust scrub; NO
    own subprocess/shell/network/provider/SDK/embeddings/vector-DB/git-write; delegates execution to
    the single bounded runner. No MemPalace/MCP/UI-redesign.

## Findings — Steps 1877-1916

### R-0104
- **Severity**: Low
- **Status**: Resolved @ 7230268 (reviewer-verified; Done≠Resolved — independently confirmed below)
- **Area**: `packages/orchestration/real_test_execution.py` `run_allowed_test` ×
  `test_execution_service.execute_test_run`.
- **Problem**: `run_allowed_test` calls `resolve_allowed_command(command_id)` to validate the requested
  command, but then invokes `execute_test_run(TestExecutionRequest(job_id, source, timeout))` WITHOUT
  forwarding `command_id` — the runner independently `select_best_test_candidate(...)`. So the validated
  `command_id` is not the command actually executed when a repo exposes more than one test command, yet
  `TestRunResult.command_id` reports the REQUESTED id. NO safety impact: the runner enforces its own
  gates (purpose=test, risk, `_EXECUTION_SAFE_EXECUTABLES`, no-shell, timeout, output cap, env sanitize)
  so the executed command is always a safe test command. It is a correctness/honesty nuance
  (reported-vs-executed command identity) and makes the facade's per-id allowlist check advisory.
- **Fix options**: thread the resolved candidate/command_id into the runner (have `execute_test_run`
  accept an explicit command_id and run that), OR set `result.command_id` to the actually-selected
  command and document that v1 always runs the best-discovered test command. Add a test asserting the
  reported command matches the executed one.

- **Resolution (reviewer-verified @ 7230268)**: `TestExecutionRequest.command_id` added; `run_allowed_test`
  forwards the validated `command_id` into `execute_test_run`. Gate 8: when `command_id` supplied, runner
  selects the EXACT discovered candidate by id (`next((c for c in candidates if c.id == command_id))`) —
  not found → block `requested_command_not_found`; `purpose != "test"` → block `requested_command_not_test`
  (HONEST, never self-selects/swaps). Empty id → legacy `select_best_test_candidate` (back-compat). CRITICAL:
  both paths converge on `candidate`, after which the high-risk gate (`candidate.risk == "high"` →
  `high_risk_command`) AND `_EXECUTION_SAFE_EXECUTABLES` allowlist (`candidate.argv[0]` → `executable_not_
  in_safe_list`) STILL run (svc lines 735/742) — explicit-id path does NOT bypass any safety gate; argv
  comes only from a discovered candidate (no arbitrary injection); no shell=True; timeout/cwd/safe-env/
  output-cap/output_ref unchanged. `TestExecutionResult.command_id = candidate.id` (executed) → persisted in
  test record → `run_allowed_test` sets `res.command_id = out.command_id`. Honesty chain closed:
  validated == executed == `TestRunResult.command_id` == public summary id. Builder's `Done:` was correct;
  Reviewer independently confirmed + marks Resolved.

Next id: R-0105.

## Reviewer test run (targeted)
- `remedy_pytest.sh test_real_test_execution.py + test_real_test_execution_cli.py +
  test_overnight_mission.py + test_autonomy.py + test_review_bundle.py -q` → **192 passed**.
- regression: `test_test_execution_service.py + test_repository_snapshot.py + test_proof_chain.py +
  test_progress_ledger.py + test_feature_planner.py + test_run_contract.py + test_command_catalog.py +
  test_dashboard_cockpit_truth.py -q` → **410 passed**. Targeted total **602 passed**, 0 failed.
- Integrity: `test_execution_integrity` + `audit_*` codes present (see Check 10). German scan CLEAN.
  Builder full-suite self-report NOT independently re-run; reviewer targeted = 602 passed (zero open
  Medium/High/Blocker → full-suite acceptance criteria met for PASS WITH RISKS).
- R-0104 closure re-run @ 7230268: `remedy_pytest.sh test_real_test_execution.py +
  tests/cli/test_real_test_execution_cli.py + test_test_execution_service.py + test_run_contract.py +
  tests/test_command_catalog.py + tests/cli/test_command_catalog.py + test_overnight_mission.py +
  test_integrity_gate.py -q` → **264 passed**, 0 failed. New tests cover: runner explicit-id executes
  that cmd; non-best id NOT swapped to select_best; unknown id → `requested_command_not_found` (argv
  never run); non-test id → `requested_command_not_test` (argv never run); facade forwards id; facade
  reports runner-selected id; unknown id never reaches runner; `to_dict` carries `command_id` + no raw/
  path leak. Builder full-suite self-report (6243 passed/8 skipped) NOT independently re-run; reviewer
  targeted 264 passed + zero open findings → acceptance criteria met for PASS.

## Reviewer audit log
- VERDICT PASS @ 7230268 — R-0104 Resolved (reviewer-verified): command_id forwarded into runner;
  executed == reported == validated; allowlist/high-risk gates still run after explicit-id selection
  (no bypass); no shell=True; bounded runner unchanged. Targeted 264 passed. ZERO open findings.
- VERDICT PASS WITH RISKS @ cb2c640 — one documented Low R-0104 (command_id not forwarded to runner;
  no safety impact). All checks PASS; runner verified no-shell/bounded/allowlisted/output-capped/
  env-sanitized; honest snapshot/rollback proofs.
- Block opened. Check 1 (mainline closure) PASS @ branch base `aacafbd` (PR #72 merged overnight v0).
- WATCH (HIGH-RISK, real subprocess): allowlist-only resolution; NO shell=True; mandatory
  timeout+output caps; cwd controlled + env sanitized; no background exec; raw stdout/stderr never
  public; failed/timeout → safe failure artifact; snapshot ≠ real restore; rollback restore_available
  vs restore_tested (no fake rollback-ready); mission test gate: failed test blocks, no fake pass;
  proof chain safe IDs only; integrity catches passed-with-failing-exit / failed-satisfies-tests_green
  / raw-in-public / snapshot-claims-restore_available / rollback-claims-restore_tested-without-evidence
  / satisfied-mission-with-failing-latest-test / non-catalog-next-action; CLI no generic may_execute
  shell; all project-facing text English.
