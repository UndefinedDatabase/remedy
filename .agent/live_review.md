# Live Review — Steps 1365-1398: Provider-Agnostic Repair Request Builder v0

Reviewer: parallel reviewer
Scope: From a FailureArtifact build a SAFE provider-AGNOSTIC RepairRequestPackage for
ANY external worker/model/human; external output re-enters ONLY via existing
`provider intake-repair` → Trust Gate → materialization → approval → do continue.
Interface-only candidate generator adapter (no execution). Must NOT: call any
provider/SDK/network/subprocess/browser/IDE; apply; create Patch Intent from request;
leak raw output/source/diff/secrets/tracebacks/abs paths; assume any single provider/
subscription/account/IDE. NO PR unless user explicitly asks (Step 1398).
Timestamp: 2026-06-14

## Verdict
PASS WITH RISKS — all 15 checks reviewed PASS in the audit log; ZERO findings, zero
open Blocker/High. Full suite green (5627 passed, 8 skipped, 1 deselected); integrity
passed (0 fail). Provider-agnostic request builder; output re-enters ONLY via provider
intake; no provider/network/subprocess/apply/intent-from-request; simulated external-
candidate E2E (request → intake → materialize → approve → do continue → completed_verified)
proven. NO PR created (Step 1398 — awaiting explicit user request).

## Check Matrix (1-15)
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | c9ce1a0 off clean main 871fb8d; PR#58 recorded; residuals carried; only .agent/ files touched; no drift |
| 2. Repair request models (no raw fields) | PASS | dataclasses hold IDs/statuses/scrubbed sections only; no raw stdout/source/diff fields |
| 3. Safe request builder (from RepairContextSummary) | PASS | reuses build_repair_context; all free-text via _scrub→_scrub_public; ctx attrs verified present |
| 4. Candidate output schema (one candidate; JSON or fenced diff) | PASS | CANDIDATE_OUTPUT_SCHEMA + Required-response-format section; "EXACTLY ONE candidate" |
| 5. Request package private storage (atomic, hashed, no abs paths) | PASS | 0o700 dir/0o600 files, tmp+os.replace, 256KiB cap, sha256, manifest sections scrubbed |
| 6. CLI (request / request-show) + catalog + RunContract | PASS | write_metadata/read_only, no-mutate/no-exec, JSON stable, errs→stderr; PREPARE/EXPORT_REPAIR_REQUEST allowed (not cloud), denial→CONTRACT_BLOCKED |
| 7. Candidate generator adapter boundary (no execution) | PASS | interface only; execute() raises CandidateGeneratorExecutionUnavailable; no net/sdk/subprocess |
| 8. External generator record + RepairAttempt linkage + idempotency | PASS | record saved; repair_attempt_id captured; idempotent (test_idempotent: same id; test_new_forces_fresh) |
| 9. Import guidance (exact human steps; no fake automation) | PASS | 6-step relay→intake-repair→trust-show→approve→do continue; all 4 cmds exist in catalog; no fake automation |
| 10. Integrations (Progress/Feature/Review/Cockpit) | PASS | 3ee5be1: ledger fixed item_ids+de-dup; feature planner agnostic (no auto exec); review bundle counts-only (REQUIRED_SECTIONS 18→19); cockpit read-only counts, no buttons/mutation; all evidence-based |
| 11. Request quality | PASS | tells actor output quarantined/rejected if unsafe; "Do NOT claim applied/tested"; no alternatives |
| 12. Redaction | PASS | _scrub_public on all free-text + _safe_file_names drops id_rsa/.ssh/.env/credentials/secret/.aws/.git; test_no_raw_leak injects sk-token//home//id_rsa/Traceback → asserts absent across surfaces |
| 13. Architecture guards (no provider/network/subprocess/apply/intent) | PASS | imports stdlib + internal only; no apply/intent creation; no shell/subprocess |
| 14. Request→intake E2E (simulated; no real provider) | PASS | test_request_to_completed_verified: request→intake(ACCEPTED,intent)→approve→do continue→completed_verified; file actually changed; output is a fixture file, no real provider |
| 15. Provider-agnostic language audit | PASS | core + docs; test_no_subscription_account_ide_assumption; docs/repair-request-builder-v0.md + candidate-generator-adapter-future.md; providers only as examples |

## Findings — Steps 1365-1398
(none yet)

### Reviewer audit log
- 2026-06-14: Block start. Worker at c9ce1a0 (Step 1365 reconciliation only). Verified
  branch forked clean main 871fb8d (PR#58 merged); commit touches only .agent/ planning
  files (context/plan/live_review) — no production code. Plan steps 1366-1398 each cover
  a stated block-if/check. Residual risks preserved verbatim from prior block. Check 1 PASS.
  No production code to review yet. Polling for builder commits. Next finding id: R-0084.
- 2026-06-14: Reviewed 4ef879b (Steps 1366-1387 core+CLI). repair_request_builder.py
  (600L): models/builder/storage/schema/templates/adapter. ZERO findings. Verified all
  block-ifs against committed code: no provider/network/subprocess/browser/SDK import
  (stdlib + internal orchestration only); no apply, no Patch Intent creation, no provider-
  intake call inside builder; all free-text scrubbed via _scrub_public; one-candidate
  constraint + required schema present; idempotent per (failure,target,model_hint);
  execute() raises; contract PREPARE/EXPORT_REPAIR_REQUEST not in cloud actions; next_steps
  reference only catalog-backed commands (do.continue/patch.approve/provider.intake-repair/
  provider.trust-show all confirmed). ctx attrs command_display/exit_code confirmed present
  on RepairContextSummary (no AttributeError). Checks 2-7,9,11,13,15 PASS. Checks 8,12
  PARTIAL (await tests). Checks 10,14 PENDING (integrations uncommitted; E2E not committed).
- 2026-06-14: Reviewed 3ee5be1 (integrations 1378-1381) + ed975f9 (tests/docs 1382-1397)
  + 30b8001 (plan). Integrations clean: progress_ledger extract/merge_repair_request_items
  (fixed item_ids repair-request-prepared/external-candidate-pending/imported, de-dup,
  evidence-based counts, catalog next_action); feature_planner external-candidate-pending
  rule (no auto exec); review_bundle _build_repair_request_summary (REQUIRED_SECTIONS 18→19,
  counts/labels/IDs only); ui_server _build_repair_request_section (read-only counts+latest
  target, no buttons). Builder delta: _safe_file_names drops protected tokens. load_materials
  confirmed present (provider_patch_material:253) — no silent ImportError skip. Tests: builder/
  idempotency/contract-block, request-quality (schema/one-candidate/no-apply-claim/relative/
  no-secrets/no-subscription-account-IDE), redaction (sk-token//home//id_rsa/Traceback absent),
  adapter execute raises, architecture guards (no subprocess/shell/SDK/apply/intent/intake in
  source), E2E request→intake(ACCEPTED)→approve→do continue→completed_verified+file changed,
  next-action catalog-backed. ALL 15 checks PASS in committed code. ZERO findings.
  Targeted wrapper run deferred: builder holds /tmp/remedy-pytest.lock (full suite in progress).
  Awaiting builder final handoff + full pytest count + changed-files table before final verdict.

## Builder Final Handoff (Steps 1365-1398)

- **Mainline reconciliation**: PR #58 merged; branch off clean main 871fb8d; no drift.
- **Tests**: targeted builder unit/quality/redaction/architecture/adapter/E2E (21) +
  CLI runtime (7) + provider-trust/material/review-bundle/cockpit/catalog/progress/
  feature/run-contract/do_continue. **Full pytest** → **5627 passed, 8 skipped, 1
  deselected** (exit 0). Wrapper `scripts/remedy_pytest.sh`, `-k "not test_full_chain_order"`.
- **Integrity gate**: `remedy integrity check` passed=True, fail_count=0.
- **Findings**: none.
- **Models / safe builder / request storage / candidate schema / CLI / catalog /
  RunContract / adapter boundary / external generator record / RepairAttempt linkage /
  import guidance / Progress / Feature / Review / Cockpit / request quality / redaction /
  architecture guards / E2E / language audit**: DONE.
- **E2E (1388)**: `test_request_to_completed_verified` — request → simulated external
  candidate file → provider intake (accepted) → approve → do continue → completed_verified;
  no real provider/model/network.
- **Hard completion criteria (1395)**: repair.request calls no provider/network/
  browser/subprocess; no raw output/source/diff/secret/traceback/abs-path leak; no
  Patch Intent created from request; candidate output goes through Trust Gate; next
  actions catalog-backed + real; repeated request idempotent; adapter execute()
  unavailable (no working external execute); live_review NOT PENDING. ALL satisfied.

### Changed Files (Steps 1365-1398)
| File | What changed | Why |
|---|---|---|
| `packages/orchestration/repair_request_builder.py` | NEW — models, safe request builder (from RepairContextSummary, scrubbed), private storage, candidate output schema, target templates, idempotency, ExternalCandidateGeneratorRecord, interface-only CandidateGeneratorAdapter (execute raises) | Core provider-agnostic request builder |
| `packages/orchestration/run_contract.py` | prepare_repair_request / export_repair_request actions (metadata-only; allowed default) | Gate request prep vs execution |
| `apps/cli/command_catalog.py` | repair.request (write_metadata) + repair.request-show (read_only) | CLI surface |
| `apps/cli/grouped.py` | parse --target / --new | Request flags |
| `apps/cli/commands/repair_cmd.py` | request / request-show handlers (no apply/intent) | Wire CLI |
| `packages/orchestration/progress_ledger.py` | repair-request-prepared / external-candidate-pending / imported items | Progress surface |
| `packages/orchestration/feature_planner.py` | external-candidate-pending → import follow-up (no auto exec) | Human next-step |
| `packages/orchestration/review_bundle.py` | repair_request_summary.json (REQUIRED_SECTIONS 18→19) | Reviewable summary |
| `packages/orchestration/ui_server.py` | read-only repair_request cockpit section | Surface counts |
| `docs/repair-request-builder-v0.md` | NEW — builder doc | Long-term knowledge |
| `docs/candidate-generator-adapter-future.md` | NEW — future direct-provider design note | Defer rationale + requirements |
| `docs/provider-trust-gate-v0.md`, `provider-patch-materialization-v0.md`, `repair-loop-v1.md`, `bounded-overnight-executor-v0.md` | cross-links | Doc graph |
| `tests/orchestration/test_repair_request_builder.py` | NEW — 21 unit/quality/redaction/architecture/adapter/E2E tests | Coverage |
| `tests/cli/test_repair_request_cli.py` | NEW — 7 CLI runtime tests | Coverage |
| `tests/orchestration/test_review_bundle.py`, `tests/ui_server/test_dashboard_cockpit_truth.py` | REQUIRED_SECTIONS==19 + cockpit shape | Keep invariants |
| `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md` | block state + product readiness + review | Runtime state |

### Readiness + PR recommendation (Steps 1393-1394/1398)
Readiness ~95% (direct external execution deliberately deferred; adapter interface
only). PR is MERGE-READY but **NOT created** — Step 1398 requires explicit user
request. Recommend a separate PR when approved; next block stays separate (Provider
Trust Verification v1 OR Automated Candidate Generator Adapter v0).
