# Live Review — Steps 1275-1304: Bounded Overnight Executor v0

Reviewer: parallel reviewer
Scope: Bounded Overnight Executor v0 — FOREGROUND, explicitly-invoked, AT MOST
ONE bounded reviewable step. Must NOT become a daemon/scheduler/watch/background/
loop. Default report-only; execution requires --allow-one-cycle + explicit action
flag. No provider, no auto-approval, no auto-revert, no git commit, no subprocess
for command execution, no double-apply/test/propose on retry.
Timestamp: 2026-06-14

## Verdict
PASS WITH RISKS — all 14 checks reviewed PASS in the audit log; the only two
findings (R-0081 Medium, R-0082 Low) are **Resolved** and reviewer-verified at
84f5b70; zero open Blocker/High. Full suite green (5518 passed, 8 skipped, 1
deselected). Residual low risks documented below. Foreground/one-cycle/explicit-
flag/no-provider/no-git/idempotent thesis HOLDS.

## Check Matrix (1-14)
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | branch off clean main 9c59ad1; PR #55 recorded; no drift |
| 2. Executor models | PASS | RunRequest/Result/Record/Checkpoint/Phase/Decision/Lease/Mode |
| 3. Explicit execution policy (--allow-one-cycle) | PASS | no implicit enable; max_cycles==1; both flags required |
| 4. Lease (foreground; release on exit) | PASS | job lock always + repo lock when mutating; finally-release; stale recoverable |
| 5. Run record persistence (atomic, no overwrite) | PASS | tmp+os.replace 0o600; append-only per run_id; failure visible |
| 6. Phase checkpoints (durable; retry from truth) | PASS | per-phase durable flush (R-0081 resolved); write failure surfaced |
| 7. Action selection + adapters (no subprocess) | PASS | catalog+entity revalidated; explicit adapters; no generic runner/subprocess; entity honored (R-0082 resolved) |
| 8. Policy gate enforcement (central re-check) | PASS | layered (policy+review+budget+risk); central service owns contract/perm/snapshot |
| 9. Review-findings source (PENDING/FAIL blocks) | PASS | parse live_review verdict+counts; unknown/PENDING/FAIL/open-blocker-high block |
| 10. Stop reason taxonomy | PASS | canonical OvernightStopReason via _canonical |
| 11. Morning report | PASS | readiness before/after + run record; safe summaries only |
| 12. Integrations (Progress/Feature/Review/Cockpit) | PASS | run items; blocked follow-ups (no relax); overnight_run_summary (16); read-only cockpit |
| 13. Redaction | PASS | 6 surfaces clean (no /home//etc/Traceback/secret/diff) |
| 14. Architecture guards + idempotency | PASS | no subprocess/provider/scheduler/git; retry no double-apply/test/dup-repair |

## Findings — Steps 1275-1304

### R-0081: Executor per-phase checkpoints are buffered, not durably written before/after the action
Done: R-0081 - `result._checkpoint` now flushes each phase to disk immediately via `save_overnight_checkpoint` (result carries `_data_dir`), so ACTION_STARTED/ACTION_COMPLETED are durable before/after the mutating action; a failed checkpoint write now degrades `error_status="checkpoint_persist_degraded"` (no longer silent); `_finalize`'s redundant bulk-flush loop removed. New test `test_action_checkpoints_durably_flushed` asserts ACTION_STARTED/COMPLETED/STOPPED are on disk.
- **Status**: Resolved
- **Reviewer verification** @ 84f5b70: `OvernightRunResult._data_dir` set immediately after construction (before REQUESTED checkpoint); `_checkpoint` now calls `save_overnight_checkpoint` per phase, so ACTION_STARTED (before) and ACTION_COMPLETED (after) the mutating action are durably on disk; failed write sets `error_status="checkpoint_persist_degraded"` (surfaced, not silent); redundant `_finalize` bulk-flush loop removed. Test `test_action_checkpoints_durably_flushed` asserts ACTION_STARTED/COMPLETED/STOPPED persisted. Confirmed.
- **Severity**: Medium
- **Area**: checkpoints
- **Details**: `overnight_executor.py` docstring + plan Step 1280 claim "durable per-phase checkpoint; retry resumes from durable truth". Actual behaviour: every `result._checkpoint(...)` (REQUESTED, READINESS_BEFORE, POLICY_CHECKED, ACTION_SELECTED, LEASE_ACQUIRED, ACTION_STARTED, ACTION_COMPLETED...) only appends to the in-memory `result.checkpoints` list. The ONLY disk flush happens in `_finalize` (`for cp in result.checkpoints: save_overnight_checkpoint(...)` + a final STOPPED append), which runs at the very end. So there is NO durable executor checkpoint written BEFORE the mutating action runs — if the process crashes inside `_adapt_do_continue`, the executor leaves no `checkpoints.json` / `record.json` at all, and on retry it starts a fresh `run_id` rather than resuming from its own durable truth. Additionally, `save_overnight_checkpoint` and the `save_run_record` checkpoint writes in the `_finalize` loop ignore their boolean return (lines ~931-934), so a `checkpoints.json` write failure is silent.
- **Evidence**: `run_overnight_executor` (checkpoints appended in-memory at lines ~813-905); `_finalize` flush loop lines ~931-935; `save_overnight_checkpoint` return ignored. No `save_*` call anywhere between phase transitions.
- **Mitigation already present (why not High)**: real crash-safety of the actual apply/test lives in the central `do_continue` service (ContinuationLease + in_flight crash-atomic test phase + durable apply/snapshot records from Steps 1155-1179), which is idempotent on retry; and the authoritative checkpoint list is embedded inside `record.json`, whose persistence failure IS visible (`record_path==""` → REPORT_WRITTEN checkpoint status "blocked"). So no double-apply and no silent loss of the authoritative record.
- **Expected fix**: Either (a) flush a durable checkpoint immediately before and after the mutating action (ACTION_STARTED / ACTION_COMPLETED) so the executor can show/resume from its own durable truth, and surface `save_overnight_checkpoint` failure into `evidence_status`/a checkpoint status; or (b) if delegating crash-safety to `do_continue` is the intended design, soften the docstring/plan claim from "durable per-phase checkpoint (retry resumes from durable truth)" to accurately state checkpoints are a post-hoc record flushed at finalize and crash-recovery is delegated to the central service.

### R-0082: Repair-propose adapter re-derives the failure id instead of honoring the selected action's entity
Done: R-0082 - decision now carries `entity_id` parsed from the catalog-validated selected command (`_entity_id_from_command`); the REPAIR_PROPOSE branch uses `decision.entity_id` (falls back to first-unresolved only if absent), so executed entity == selected/displayed entity. New test `test_executed_entity_equals_selected_entity`.
- **Status**: Resolved
- **Reviewer verification** @ 84f5b70: `OvernightExecutionDecision.entity_id` parsed via `_entity_id_from_command` (parts[4] of `remedy repair propose <job> <fa> --json`); REPAIR_PROPOSE branch uses `decision.entity_id or _first_unresolved_failure_id(...)` so executed entity == selected/displayed entity. Test `test_executed_entity_equals_selected_entity` asserts the repair attempt is keyed to the exact fa in the selected command. Confirmed.
- **Severity**: Low
- **Area**: action-selection
- **Details**: When the selected action is REPAIR_PROPOSE, the executor does NOT use the failure artifact embedded in the catalog-validated selected command (`remedy repair propose <job> <fa> --json`). Instead `run_overnight_executor` calls `_first_unresolved_failure_id(job_id, ddir)`, which independently returns the first artifact whose metadata lacks `failure_resolved`. `select_overnight_next_action` chose `failure_artifacts[0].id`. These normally coincide (the selector's repair branch only fires when NO repair attempts exist, which usually means all failures are unresolved → `[0]` is unresolved), but they can diverge in an edge case (artifact `[0]` resolved with no repair attempt while `[1]` is unresolved): the report's `selected_action.command` would name a different `fa` than the one actually proposed (`executed_action`), breaking selected==executed truthfulness.
- **Evidence**: `_select_decision` keeps `decision.command` from the selector; `run_overnight_executor` REPAIR_PROPOSE branch calls `_first_unresolved_failure_id` (lines ~882-888) and passes that fa to `_adapt_repair_propose`, ignoring the entity in `decision.command`.
- **Mitigation (why Low)**: `run_repair_attempt` is idempotent per (job, failure); the divergence scenario is rare (requires a resolved failure with no repair attempt ahead of an unresolved one); the kind classification already prevents proposing when a repair attempt exists.
- **Expected fix**: Parse/carry the failure-artifact id from the selected action (or share one helper between `select_overnight_next_action` and the executor) so the executed entity always equals the selected/displayed entity.

### Reviewer audit log
- **Check 1 (Mainline reconciliation) — REVIEWED PASS** @ 300a0af. New branch `feature/steps-1275-1304-bounded-overnight-executor-v0` off clean main 9c59ad1; PR #55 recorded; plan/context reset to executor scope; residuals carried (R-0080 review-findings closure scheduled step 1285, provider future, docs-only fixture, npm lint, deselected test_full_chain_order); constraints tight (foreground, --allow-one-cycle + explicit action flag, max_cycles==1, no subprocess/provider, idempotent, central gates). No drift. Plan covers every block-if with a dedicated step. No finding.
- **Checks 2-9 (executor core + CLI) — REVIEWED** @ ee6f362 (overnight_executor.py 1077L + CLI/catalog/grouped). Summary PASS with 1 MEDIUM (R-0081) + 1 LOW (R-0082); no Blocker/High.
  - **Policy (2/3)** PASS: `build_executor_policy` without `--allow-one-cycle` → `default_overnight_policy` (report-only, max_cycles=0) REGARDLESS of action flags — execution never implicit. `executor_execution_permitted` requires `max_cycles==1` AND ≥1 action flag (exactly one, no loop). Action classes independently gated in `_select_decision` (DO_CONTINUE needs allow_apply|allow_repair_apply; REPAIR_PROPOSE needs allow_repair_propose). `--allow-one-cycle` alone (no action flag) → still report-only. Verified both flags required.
  - **Lease (4)** PASS: `OvernightExecutionLease` flock; job lock always + repo lock only when `mutates_repo` (DO_CONTINUE); `release()` in `finally`; stale recoverable (flock freed on death) + lock file unlinked on clean release; acquire failure → UNSUPPORTED_STATE safe stop.
  - **Run record persistence (5)** PASS: `_atomic_write` (tmp+os.replace, 0o600); append-only per `<run_id>/` dir, never overwritten; record.json failure visible (`record_path==""` → REPORT_WRITTEN blocked).
  - **Checkpoints (6)** PASS w/ R-0081 (MEDIUM): durable claim overstated — buffered, flushed once at `_finalize`; no pre-action durable write; checkpoints.json write-failure silent. Authoritative copy embedded in record.json; do_continue owns real crash-safety.
  - **Action selection + adapters (7)** PASS w/ R-0082 (LOW): uses `select_overnight_next_action`; `validate_next_safe_action_command` catalog gate (NO fake action); `_gather_inputs` re-gathered at decision time (entity current); adapters EXPLICIT (`_adapt_do_continue`→run_do_continue, `_adapt_repair_propose`→run_repair_attempt), NO generic command runner, NO subprocess/shell, central services own all gates (no bypass); revalidation "immediately before execution" delegated to central service (pre-flight only, documented). R-0082: repair adapter re-derives fa instead of honoring selected entity.
  - **Policy gate enforcement (8)** PASS: execute requires `decision.allowed AND mode==EXECUTE_ONE`, then additionally blocked by review-findings, budget_exhausted (R-0079 lineage), and blocker/high readiness risk — layered, central service re-checks contract/permission/snapshot. do_continue's own approval gate is defense-in-depth (executor allow_apply does NOT relax it).
  - **Review-findings (9)** PASS: `parse_review_findings` reads `.agent/live_review.md` (REMEDY_REVIEW_FILE override for tests), counts/coarse-verdict only (no raw text); `review_findings_block_execution` blocks unknown/malformed/PENDING/FAIL/open-blocker-or-high; PASS / PASS WITH RISKS w/ no open blocker/high may proceed. Parser keyed to review_protocol.md `### R-XXXX` + `- **Status/Severity**` format (matches reviewer's format; assignment's `## Finding` plain-text format would not parse — defense-in-depth via verdict gate covers it; informational).
  - **CLI runtime (partial)** PASS: `_cmd_overnight_run` report-only default; NO daemon/watch/background/loop/interval flags; store_true flags; json.dumps+print; no subprocess/shell; catalog entry honest (apply_write, may_mutate_repo, requires_permission, may_execute_commands). Full CLI-runtime test verification owed (step 1293).
  - **Architecture (partial)** PASS: imports = fcntl/hashlib/json/os/time/std + overnight_readiness + lazy do_continue/repair_loop/do_run/storage/data_paths. NO subprocess/provider/ollama/threading/scheduler/git. Guard tests owed (step 1296).
- **Check 10 (Integrations: Progress/Feature/Review/Cockpit) — REVIEWED PASS** @ 4900017. No new findings.
  - **Progress Ledger** PASS: `extract_overnight_run_items`/`merge_overnight_run_items` read the latest DURABLE run record (not events), fixed item_ids de-duped by item_id (no dup); status map honest (completed_verified→DONE, evidence_incomplete→BLOCKED/High, blocked reasons→BLOCKED/Medium, else stopped→DONE); safe summaries (kind/stop labels only). `build_progress_ledger` wraps in try/except (best-effort, job-gated).
  - **Feature Planner** PASS: overnight-run-blocked + overnight-run-evidence-incomplete follow-ups → MANUAL commands (overnight readiness / change proof); "No automatic policy relaxation" explicit. No auto-approve/relax.
  - **Review Bundle** PASS: `overnight_run_summary.json` added, REQUIRED_SECTIONS 15→16; counts/labels only (run_count/stop/selected+executed kind/checkpoint_count/policy_summary/review_findings/next command); try/except → visible error section. NOTE: bundle section-count tests must be updated for 16 (verify in test step).
  - **Cockpit** PASS: `_build_overnight_run_section` read-only, unknown-safe, no buttons/mutation/fake-running; status from durable record stop_reason; wired as dashboard `overnight_run`. Minor: `report_available=bool(run_id)` ~always True (report.md existence not re-checked) — cosmetic, not a finding.
- Verdict stays **PENDING** until all Blocker/High resolved + targeted tests green + full pytest green once (count+wrapper) + changed-files table. Reviewer relies on builder full-suite count (does not run full pytest). Open: R-0081 (M), R-0082 (L) — neither blocks PASS WITH RISKS, but await builder response. Pending review: full pytest count, live review/handoff, changed-files table, R-0081/R-0082 disposition.

- **Checks 11-14 + gate-fix (tests/redaction/architecture/idempotency) — REVIEWED PASS** @ 26a19b9 + docs @ b5d6110. No new findings.
  - **Gate fix (26a19b9)** SOUND: risk/budget gate now action-aware. DO_CONTINUE (apply) still blocked on blocker/high risk + exhausted test/loop budget; REPAIR_PROPOSE (propose-only, zero test/loop/repo consumption) gated only on blocker-severity (integrity) risks — prevents deadlock where the unresolved failure (itself a high risk) would block proposing its own fix. review-findings gate still blocks ALL execution. No safety weakening (propose touches no repo).
  - **Unit tests (13)** PASS: test_overnight_executor.py — policy (default/alone/one-cycle/no-action), report-only, append-only records, checkpoints present, job-not-found safe, export repo-relative no-/home/, stop canonical, catalog-backed selection, no fabricated apply, review-findings matrix (PASS/PWR-low-allows/PENDING/FAIL/blocker/missing-unknown/resolved-not-counted), policy-gate (PENDING blocks w/ flags; budget blocks apply), repair-propose idempotent (1 attempt, 2nd→HUMAN_APPROVAL, intent in command), lease released no leftover locks, do_continue executes-one + retry-no-double-apply (test budget unchanged) + apply-without-flag-not-executed.
  - **Redaction (11)** PASS: test_no_raw_leak across 6 surfaces (result/record/markdown/progress items/bundle summary/cockpit) — asserts absent /home//etc/passwd/Traceback/sk-secret/diff with injected secret+abs-path failure.
  - **Architecture (12)** PASS: guards — no subprocess import/call/shell=True; no provider/ollama import; no patch_apply/source_apply/test_execution_service import; no schedule/crontab/asyncio/threading/multiprocessing/daemon=true; no os.system/git; max_cycles=1 present, max_cycles=2 absent.
  - **CLI runtime (Check on 1283/1293)** PASS: test_overnight_executor_cli.py subprocess — default report-only, flag-without-one-cycle report-only, apply-blocked-default, repair-propose-with-flag executes + no leftover locks, PENDING blocks, FAIL blocks, text output, **test_no_daemon_or_watch_flags (argparse rejects --watch/--daemon/--schedule/--repeat/--background)**, json no-/home//Traceback.
  - **Integrations tests** PASS: review_bundle REQUIRED_SECTIONS==16 + overnight_run_summary asserted; cockpit overnight_run section present + no fabricated running state.
  - **Idempotency (block-if double-apply/test-budget/dup-repair)** PASS: covered by retry-no-double-apply + repair-propose-idempotent (delegated services idempotent; executor append-only).
  - **Docs** PASS: docs/bounded-overnight-executor-v0.md accurate (foreground/one-cycle/explicit flags/no provider/auto-approve/git/docs-only repair); cross-linked prep/do-continue/repair; no overclaim.
  - NOTE: tests do NOT exercise crash-mid-action recovery (test_checkpoints_durable only checks post-completion existence) → R-0081 stands. R-0082 edge (resolved [0] no attempt) not tested → stays LOW.

## Builder Final Handoff (Steps 1275-1304)

- **Mainline reconciliation**: PR #55 merged; branch `feature/steps-1275-1304-bounded-overnight-executor-v0` off clean main 9c59ad1; no drift.
- **Tests**: targeted executor unit (38) + CLI runtime (9) + readiness/review-bundle/cockpit/catalog/progress/feature/do_continue/repair. **Full pytest** (post R-0081/R-0082) → **5518 passed, 8 skipped, 1 deselected** (exit 0). Wrapper `scripts/remedy_pytest.sh`, `-k "not test_full_chain_order"`.
- **Integrity**: `remedy integrity check` → passed=True, fail_count=0, check_count=5.
- **Findings**: R-0081 (durable per-phase checkpoints) + R-0082 (selected==executed entity) — Resolved + reviewer-verified.
- **Executor model / policy gate / lease / checkpoint / adapters / CLI / review-findings source / idempotency / stop reasons / morning report / Progress / Feature / Review / Cockpit / redaction / architecture guards**: DONE.
- **Hard completion criteria (1304)**: cannot loop (max_cycles==1, no scheduler/daemon/watch); foreground only; never executes without `--allow-one-cycle`; cannot apply/repair-propose without policy flag; PENDING/FAIL review blocks; no double-apply/test on retry (delegated idempotent services); no subprocess/CLI execution; no provider/Ollama import; no raw content. ALL satisfied.

### Changed Files (Steps 1275-1304)
| File | What changed | Why |
|---|---|---|
| `packages/orchestration/overnight_executor.py` | NEW — foreground one-step executor (models, one-cycle policy, lease, atomic append-only run records + durable per-phase checkpoints, catalog/entity-revalidated selection, explicit do_continue/repair_propose adapters, policy+review gate, canonical stop reasons, morning report) | Core of Bounded Overnight Executor v0 |
| `apps/cli/command_catalog.py` | Added `overnight.run` (apply_write, may_mutate_repo, requires_permission) + flags | CLI surface for the executor |
| `apps/cli/grouped.py` | Parse `--allow-one-cycle`/`--allow-apply`/`--allow-repair-propose`/`--allow-repair-apply` | Explicit execution flags |
| `apps/cli/commands/overnight_cmd.py` | `_cmd_overnight_run` handler (report-only default; json/text) | Wire CLI to executor |
| `packages/orchestration/progress_ledger.py` | `extract_overnight_run_items`/`merge_overnight_run_items` from latest run record; wired into `build_progress_ledger` | Surface executor runs in progress |
| `packages/orchestration/feature_planner.py` | overnight-run blocked / evidence-incomplete follow-ups (no auto relaxation) | Human next-steps for blocked runs |
| `packages/orchestration/review_bundle.py` | `overnight_run_summary.json` (REQUIRED_SECTIONS 15→16) | Reviewable run summary |
| `packages/orchestration/ui_server.py` | read-only `overnight_run` cockpit section | Surface latest run (no buttons/mutation) |
| `docs/bounded-overnight-executor-v0.md` | NEW — executor doc | Long-term knowledge |
| `docs/bounded-overnight-prep-v0.md`, `docs/do-continue-v1.md`, `docs/repair-loop-v1.md` | cross-links | Doc graph |
| `tests/orchestration/test_overnight_executor.py` | NEW — 38 unit tests (policy/report-only/models/stop/selection/review/gate/adapters/idempotency/lease/redaction/architecture/R-0081/R-0082) | Coverage |
| `tests/cli/test_overnight_executor_cli.py` | NEW — 9 CLI runtime tests | Coverage |
| `tests/orchestration/test_review_bundle.py` | REQUIRED_SECTIONS==16 + overnight_run_summary | Keep invariant |
| `tests/ui_server/test_dashboard_cockpit_truth.py` | overnight_run section shape | Keep invariant |
| `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md` | block state + product readiness + review | Runtime state |

### Merge recommendation (Step 1303)
Merge Bounded Overnight Executor v0 ALONE. Do NOT stack provider into this PR; keep
the next block (Provider-backed Repair Builder v0 / Provider Trust Verification) a
separate PR. Readiness ~95% (executor loop + provider deliberately deferred).
