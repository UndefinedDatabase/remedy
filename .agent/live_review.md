# Live Review — Steps 1335-1364: Trusted Provider Patch Materialization v0

Reviewer: parallel reviewer
Scope: Materialize ACCEPTED provider candidates into REAL applyable Repair Patch
Intents (approval → do continue → snapshot → apply → test → proof), raw diff/output
PRIVATE only. Must NOT: invoke provider/Ollama/Claude API, network, subprocess,
auto-apply, auto-approve; expose raw diff/source/secrets/tracebacks/abs paths; let a
materialized intent bypass approval or apply automatically. Patch material private
workspace only; intent exposes safe metadata; apply via existing do continue.
Timestamp: 2026-06-14

## Verdict
PASS WITH RISKS — all 15 checks reviewed PASS in the audit log; ZERO findings, zero
open Blocker/High. Full suite green (5599 passed, 8 skipped, 1 deselected); integrity
passed (0 fail). do_continue apply compatibility proven (approve → do continue →
snapshot → apply → completed_verified). Conservative .md-only materialization thesis
HOLDS; raw diff stays private; accepted ≠ materialized ≠ applied ≠ verified.

## Check Matrix (1-15)
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | branch off clean main b38cf94; PR #57 recorded; no drift |
| 2. Material models (no raw fields) | PASS | Material/Entry/Result/Verification/IntentLink; safe metadata only |
| 3. Private material storage (0o700/0o600, hashed) | PASS | atomic, uuid dir, 256KiB cap; _read marked private; never exported |
| 4. Material verification | PASS | manifest/hash/paths/report-accepted/single-candidate/not-revoked; tamper detected |
| 5. Unified diff → structured patch | PASS | single .md create/modify; binary/delete/rename/multi → unsupported |
| 6. JSON structured_operations materialization | PASS | single .md create/modify op; bounded; else unsupported |
| 7. Applyable provider repair intent (real/resolvable/pending) | PASS | apply-format artifact; resolvable verified; no fake ID; pending |
| 8. Approve + do_continue compatibility | PASS | fixture proof: snapshot+apply via existing path; completed_verified |
| 9. Trust report state updates | PASS | accepted/materialized/intent_pending_approval/unsupported/failed; not auto-verified |
| 10. CLI (material-show) + catalog + RunContract | PASS | read-only show (no raw); provider_materialize_patch allowed; execution denied |
| 11. RepairAttempt linkage + idempotency | PASS | candidate_hash dedupe; single intent path; no dup |
| 12. Integrations (Progress/Feature/Review/Cockpit) | PASS | counts/IDs only; bundle 18; no auto approve/retry; read-only cockpit |
| 13. Retention docs | PASS | private workspace; no auto-deletion v0; bundle excludes raw |
| 14. Redaction | PASS | no raw diff/source/secret/abs-path across surfaces; scrubbed lines |
| 15. Architecture guards | PASS | no provider SDK/network/subprocess/apply/test-exec imports |

## Findings — Steps 1335-1364
(no open findings yet)

### Reviewer audit log
- **Check 1 (Mainline reconciliation) — REVIEWED PASS** @ b472ad0. Branch `feature/steps-1335-1364-provider-patch-materialization-v0` off clean main b38cf94; PR #57 recorded; plan/context reset to Provider Patch Materialization v0. Honest key constraint documented: existing `apply_patch_intent` is `.md`-ONLY → materialized intent apply-compatible ONLY for a single `.md` create/modify; source/binary/delete/rename/multi-file → `unsupported_patch_shape` (accepted_but_not_materialized, NO intent). Hard rules map to every block-if (no provider/SDK/network/subprocess; raw material private 0o700/0o600 never public; no raw diff/source/secrets/tracebacks/abs public; apply only via approved do continue; no auto-apply/approve; accepted≠materialized≠applied≠verified; supported shapes only else no intent; idempotent by candidate_hash; catalog-backed, no fake IDs). 30-step plan; every block-if has a covering step. Carry-forward residuals preserved (builder deferred, regex scan limits, retention now Step 1352). No drift. No finding.
- **Checks 2-12 (materialization core + CLI + contract + integrations) — REVIEWED PASS** @ bc81334 + 8f4cb67 + 306728a (provider_patch_material.py 554L). ZERO findings so far; no Blocker/High.
  - **Private material storage (2)** PASS: `store_material` 0o700 dir + 0o600 files (patch.diff/manifest.sha256/material.json) via atomic tmp+os.replace+chmod; sha256 hash; MAX_MATERIAL_BYTES 256KiB cap → reject; fresh uuid material_id dir (no overwrite). `save_material` stores safe manifest (paths via `_safe_path_label`, counts/IDs/state — NO raw diff). `_read_material_patch` marked PRIVATE and NOT called from any export/CLI path (verified; currently unused/reserved — apply reads artifact.content, not patch.diff).
  - **Verification (3)** PASS: `verify_provider_patch_material` checks manifest_exists/patch_exists/sha exists, hash_matches (tamper), not_revoked, single_candidate (target_path_count==1), paths_safe (validate_paths no blocker/high), trust_report_accepted (report exists + status accepted/materialized/intent_pending_approval). ok = all(checks); reason lists failures. Revoked/missing/tampered → blocks.
  - **Conversion (4)** PASS: unified-diff → rejects binary/rename/delete; requires exactly ONE `+++` target; must be `.md` (else non_markdown_target); create-detection; needs added lines; ≤MAX_MATERIAL_LINES. structured_ops → exactly one op, create/modify only, `.md` only, bounded content. Unsupported → `_Extracted(False, reason)` → state UNSUPPORTED, NO intent (reason recorded, not silent).
  - **Patch Intent (5)** PASS: applyable artifact built in the `Summary:/Proposed Changes:  - <line>` format `apply_patch_intent` consumes; lines scrubbed via `_scrub_public`; kind=provider_repair; `patch_intent_approvals={}` (pending); `make_intent_id(art.id,0)` verified resolvable via `get_patch_intent` (else FAILED, no fake ID); linked to material/trust/quarantine/failure/repair. Raw diff stays private; converted+scrubbed lines in artifact.content (matches established applyable-intent model).
  - **Approval/do_continue (6)** PASS: approvals empty → approval_required; materialize NEVER applies/approves; apply only via existing `do continue` (snapshot mandatory in that path). Commit claims E2E `.md` candidate→approve→do continue→snapshot→apply→completed_verified (apply-compat proof test owed step 1361).
  - **RunContract (7)** PASS: ACCEPTED requires BOTH CREATE_PROVIDER_REPAIR_INTENT AND PROVIDER_MATERIALIZE_PATCH allowed (else NEEDS_HUMAN_REVIEW + materialization_blocked). PROVIDER_MATERIALIZE_PATCH allowed by default; provider EXECUTION = CLOUD_PROVIDER, no_cloud denied. Materialization distinct from execution.
  - **Repair linkage + idempotency (8)** PASS: candidate_hash = sha256(raw_patch); `_find_material_by_hash` → repeat returns existing material/intent (no dup); NO double-intent — old `_create_repair_artifact_and_intent` call REPLACED by `materialize_accepted_candidate` (single intent path). repair_attempt_id carried from report.
  - **Integrations (9)** PASS: review_bundle `_build_provider_material_summary` counts/IDs/states only (REQUIRED_SECTIONS 17→18); progress materialized/pending/failed items (fixed ids, no dup); feature approve/inspect follow-ups (no auto approve/retry); cockpit material counts. No raw, no buttons/mutation.
  - **Redaction (10, partial)** PASS: material manifest + intake export carry material_id/state/counts/safe paths only; artifact summary + proposed lines scrubbed via `_scrub_public`; raw diff private. (Redaction test owed step 1353.)
  - **Architecture (11, partial)** PASS: imports hashlib/json/os/re/std + provider_trust helpers; lazy core.models/approval_queue/data_paths/storage. NO provider-SDK/network/subprocess, NO source_apply/patch_apply/test-exec import, NO generic command runner. materialize calls no apply/test. (Guard tests owed step 1355.)
- **Tests + docs + apply-compat (Checks 4-12 verification) — REVIEWED PASS** @ e5e729d. ZERO findings; all block-if axes covered.
  - **Apply-compat proof (6, KEY)** PASS: `test_approve_then_do_continue_applies` — real `.md` provider candidate → intake → materialized intent → EXPLICIT `set_approval_state(approved)` → `run_do_continue(intent_id)` → asserts `stop_reason==completed_verified`, `snapshot_id` present (snapshot mandatory), AND `docs/guide.md` actually contains the applied line. Proves materialized intent applyable via existing approval+do_continue+snapshot+apply+test path; no approval bypass; no auto-apply.
  - **Unit tests** PASS: accepted .md → applyable intent (+ `_extract_proposed_lines` matches the apply format), source → UNSUPPORTED no intent, private storage+hash (manifest has no `@@`), verification pass + tamper-detect (hash mismatch), idempotent (1 material on repeat intake).
  - **Redaction (10)** PASS: `test_no_raw_leak_across_surfaces` no `@@`/`+++`/`diff --git`/`/home/`/`Traceback` across 5 surfaces (intake result/material manifest/progress/bundle/cockpit); `test_secret_diff_rejected_no_material` secret diff → REJECTED, no intent, no material.
  - **Architecture (11)** PASS: guard tests (no apply/test-exec imports, no provider-SDK/network/subprocess).
  - **CLI (10)** PASS: test_provider_material_cli.py — md/json materialize, source/delete unsupported, protected/secret rejected, material-show read-only.
  - **Integrations tests** PASS: REQUIRED_SECTIONS==18; cockpit material counts. Prior provider-trust tests updated for v0 materialization (source→unsupported, .md→intent).
  - **Docs (Check retention)** PASS: docs/provider-patch-materialization-v0.md (+ retention) + cross-links.
- Verdict stays **PENDING** until full pytest green once (count+wrapper) + final handoff + changed-files table. Reviewer relies on builder full-suite count (does not run full pytest). ZERO open findings to date. Next finding id: R-0084.

## Builder Final Handoff (Steps 1335-1364)

- **Mainline reconciliation**: PR #57 merged; branch off clean main b38cf94; no drift.
- **Tests**: targeted materialization unit (22) + CLI runtime (7) + provider-trust
  (updated for v0) + review-bundle/cockpit/catalog/progress/feature/run-contract/
  do_continue/repair. **Full pytest** → **5599 passed, 8 skipped, 1 deselected** (exit 0).
  Wrapper `scripts/remedy_pytest.sh`, `-k "not test_full_chain_order"`.
- **Integrity gate (1362)**: `remedy integrity check` passed=True, fail_count=0.
- **Findings**: none.
- **Material model / private storage / verification / unified-diff conversion / JSON
  ops materialization / applyable intent / approval+do_continue compat / RunContract /
  RepairAttempt linkage / Progress / Feature / Review / Cockpit / retention docs /
  redaction / architecture guards**: DONE.
- **Apply compatibility proof (1361)**: `test_approve_then_do_continue_applies` —
  materialize .md → approve → do continue → snapshot created → apply via existing
  path → completed_verified; no overclaim.
- **Hard completion criteria (1364)**: supported shape (single .md) produces applyable
  intent; raw patch/output never public; secrets never echoed (rejected + scrubbed);
  materialized intent stays pending (no auto-approve); never applies automatically;
  protected paths rejected; unparseable → no intent; intent IDs verified resolvable;
  no provider SDK/network/subprocess; do_continue compat tested. ALL satisfied.

### Changed Files (Steps 1335-1364)
| File | What changed | Why |
|---|---|---|
| `packages/orchestration/provider_patch_material.py` | NEW — material models, private storage (0o700/0o600, hashed), unified-diff + JSON-ops conversion (single .md create/modify), verification, materialize_accepted_candidate (idempotent) | Core materialization |
| `packages/orchestration/provider_trust.py` | intake accepted branch → materialize (replaces placeholder); report material_id/material_state/report_state; result + export fields | Wire materialization into intake |
| `packages/orchestration/run_contract.py` | provider_materialize_patch action (allowed default; execution stays denied) | Gate materialization vs execution |
| `apps/cli/command_catalog.py` | provider material-show (read_only) | CLI surface |
| `apps/cli/commands/provider_cmd.py` | material-show handler (no raw) | Wire CLI |
| `packages/orchestration/progress_ledger.py` | provider material items (materialized/pending/failed) | Progress surface |
| `packages/orchestration/feature_planner.py` | materialized-intent approve + materialization-failed inspect follow-ups | Human next-steps |
| `packages/orchestration/review_bundle.py` | provider_material_summary.json (REQUIRED_SECTIONS 17→18) | Reviewable summary |
| `packages/orchestration/ui_server.py` | materialized/failed counts on read-only provider_trust section | Cockpit |
| `docs/provider-patch-materialization-v0.md` | NEW — materialization + retention doc | Long-term knowledge |
| `docs/provider-trust-gate-v0.md`, `docs/do-continue-v1.md`, `docs/repair-loop-v1.md` | cross-links | Doc graph |
| `tests/orchestration/test_provider_patch_material.py` | NEW — 22 unit/redaction/architecture/apply-compat tests | Coverage |
| `tests/cli/test_provider_material_cli.py` | NEW — 7 CLI runtime tests | Coverage |
| `tests/orchestration/test_provider_trust.py`, `tests/cli/test_provider_trust_cli.py` | updated for v0 materialization (.md→intent, source→unsupported) | Keep consistent |
| `tests/orchestration/test_review_bundle.py`, `tests/ui_server/test_dashboard_cockpit_truth.py` | REQUIRED_SECTIONS==18 + cockpit material counts | Keep invariants |
| `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md` | block state + product readiness + review | Runtime state |

### Provider Patch Materialization readiness + merge recommendation
Readiness ~95% (apply surface limited to single .md by the existing apply path;
broader source apply + real provider builder deferred). Merge ALONE; do NOT stack
the provider builder into this PR — next block (Provider-backed Repair Builder v0)
stays separate.
