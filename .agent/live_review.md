# Live Review — Steps 1537-1572: Provider Trust Verification v1

Reviewer: parallel reviewer
Scope: Safe second-stage verification layer for external candidate output BEFORE it becomes a
pending repair intent. Verification must NOT: execute providers/models, call external network,
run subprocess/shell, apply patches, approve work, run tests, create PRs, run git ops, leak raw
candidate/output/diff/source/secrets/tracebacks/abs paths, echo secret values, or treat model
output as truth. Local advisor (if used) may only critique/lower-confidence/escalate — never
pass/reject a candidate by itself. Decision rules: blocker/high → rejected; medium → needs_review;
low-only → passed (if policy allows); passed ≠ approved/applied/verified. Failed verification
creates NO intent; passed verification may create a real pending intent only where materialization
is supported; existing approval/do_continue path unchanged. NO PR unless user explicitly asks.
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PASS — all 15 checks PASS; ZERO open findings (next id R-0088). Verification is a SAFE
second-stage layer: unsafe/unverified accepted candidates create NO intent (verify-before-
materialize in `intake_provider_repair._verification_allows_materialization`); overclaim /
unrelated / repeated-failed / too-broad / secret candidates are caught and never pass silently;
no provider/model execution, no network, no subprocess, no provider SDK, no apply/approval/PR/
git; reports are safe summaries only (no raw candidate/diff/source/secret/path/traceback); the
local-advisor critique hook is DEFERRED (forward seam `advisor_critique=None`) so it cannot pass/
reject by itself. Reviewer-independent verification: targeted `scripts/remedy_pytest.sh`
(test_provider_trust_verification 27 + test_provider_verification_cli 7 + provider trust/material
+ orchestrator/progress/feature/review-bundle(24)/cockpit/run_contract/catalog = 395 passed +
the two new files); full pytest 5812 passed, 8 skipped, 1 deselected (exit 0); integrity clean
(only "relevant untracked" pre-commit, clears on commit). NO PR (Step 1572).

## Check Matrix (1-15)
| Check | Status | Note |
|---|---|---|
| 1. Handoff/mainline (clean main after advisor merge; residuals preserved; no drift) | PASS | branch off 50ea930 (merged main); reconciliation in context/plan |
| 2. Models/taxonomy (safe fields; canonical codes; passed/needs_review/rejected/incomplete) | PASS | 20 canonical + 6 scanner codes; export has no raw/diff/source fields |
| 3. Consistency/relevance (request/candidate constraints; artifact linkage; unrelated blocked) | PASS | missing pkg = LOW (no crash); docs/source mismatch; self-link via self_dogfood: label |
| 4. Overclaim/scope/testability (apply/test/verified claims; minimality; no raw echo) | PASS | intent-framing allowed; codes only; too-broad/lock; testability surfaced not executed |
| 5. Loop risk (repeated failed candidates detected; no endless recommendations) | PASS | same-hash rejected→HIGH→human review; per-failure count→MEDIUM |
| 6. Secret/entropy (high-entropy/private-key/env-like detected; never echoed) | PASS | reuses scan_secrets + entropy/cred/url heuristic; values never echoed |
| 7. Decision rules (blocker/high reject; medium needs_review; low-only pass; pass≠approved) | PASS | deterministic; incomplete on missing candidate/trust; pass = eligible only |
| 8. Integration (failed→no intent; passed→real pending intent; approval/do_continue unchanged) | PASS | verify-before-materialize; existing 72 provider tests green |
| 9. CLI runtime (provider verify / verification-show; JSON parses; no traceback; no shell; timeout) | PASS | 7 subprocess tests; bounded; no raw diff in output |
| 10. RunContract/Catalog (verify actions distinct from provider exec; catalog-backed; no may_execute) | PASS | provider_verify_candidate/provider_verification_show in defaults; may_execute=False |
| 11. Orchestrator/local-advisor (recommends verify; advisor critique/lower/escalate only) | PASS | verify option (score 60, contract-gated); advisor hook deferred (cannot pass/reject) |
| 12. Progress/Feature/Review/Cockpit (safe counts/status; no raw; no mutation buttons) | PASS | fixed item_ids; 4 planner rules; bundle 24; cockpit counts only, no buttons |
| 13. Redaction (no secrets/paths/tracebacks/source/diff/log) | PASS | _scrub_public on summaries; private report.json 0o600; public = codes/counts/IDs |
| 14. Architecture (no provider SDK/network/subprocess/apply/test/git/PR; no source_apply/patch_apply import; no auto approval) | PASS | guard tests assert forbidden imports/exec tokens absent |
| 15. Tests (targeted + full pytest ≤1×) | PASS | targeted 395 + 34 new; full 5812 passed/8 skipped/1 deselected (exit 0) |

## Changed files (Steps 1537-1572) — File | What changed | Why
| File | What changed | Why |
|---|---|---|
| packages/orchestration/provider_trust_verification.py | NEW: models/taxonomy/checks/decision/score/impact/persistence/idempotency/CLI+inline entry points | the verification rail |
| packages/orchestration/provider_trust.py | `_verification_allows_materialization` between trust-accept and materialize; verification linkage fields on report+result | unverified candidates create no intent |
| packages/orchestration/run_contract.py | `PROVIDER_VERIFY_CANDIDATE`/`PROVIDER_VERIFICATION_SHOW` actions (allowed by default, non-cloud) | contract gate distinct from provider exec |
| apps/cli/commands/provider_cmd.py | `provider verify` + `provider verification-show` handlers | CLI surface |
| apps/cli/command_catalog.py | provider.verify (write_metadata) + provider.verification-show (read_only) entries | catalog-backed commands |
| packages/orchestration/orchestrator_brain.py | verification signals + verify/needs-review/repeat-rejection options; PROVIDER_TRUST_VERIFICATION score 60 | recommend verify; escalate; no exec |
| packages/orchestration/progress_ledger.py | extract/merge_provider_verification_items (fixed item_ids) | surface verification state, no raw |
| packages/orchestration/feature_planner.py | 4 verification repair rules → valid FeaturePlanSource | suggestions, no auto-retry/approval |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 23→24 + _build_provider_verification_summary | bundle safe verification summary |
| packages/orchestration/ui_server.py | _build_provider_verification_section cockpit counts/status | read-only surface, no buttons |
| tests/orchestration/test_provider_trust_verification.py | NEW 27 unit/integration/arch tests | safety + behavior coverage |
| tests/cli/test_provider_verification_cli.py | NEW 7 subprocess tests | CLI runtime coverage |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==24 + section assert | bundle test update |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_provider_verification_section_present | cockpit test update |
| docs/provider-trust-verification-v1.md, docs/expensive-builder-routing-v0-plan.md | NEW design docs | document rail + future routing |
| docs/{provider-trust-gate-v0,provider-patch-materialization-v0,repair-request-builder-v0,orchestrator-brain-v0,local-model-advisor-v0}.md | cross-ref updates | document the new stage |

## Findings — Steps 1537-1572
(none) — ZERO open Blocker/High. Next id: R-0088.

## Reviewer audit log
- `50ea930` PR #63 merged Local Model Advisor v0 (1499-1536) to main; prior block R-0087 (changed-
  files table) RESOLVED @ `eb33351`; prior verdict PASS. New block branch
  `feature/steps-1537-1572-provider-trust-verification-v1` created off `50ea930` (clean merged main).
  `git log main..HEAD` empty → no drift, no block code yet. Check 1 PASS. Awaiting builder commits.
- Watch: `verifier.py` / `verifier_profiles.py` pre-exist (last touched `72f47a7`/`6444e49`, prior
  blocks). Provider-trust-verification v1 should add a NEW second-stage candidate-verification layer
  — flag scope overlap, direct `source_apply`/`patch_apply` imports, provider/model/network/
  subprocess calls, auto-apply/approve, or any path where failed verification still creates an intent.
- Reviewed `provider_trust_verification.py` (NEW) + intake integration — ZERO findings. Verified:
  verify-before-materialize gate (`_verification_allows_materialization` returns True ONLY on
  `verification_passed and allowed_to_materialize`; contract `provider_verify_candidate` denial →
  False → no intent); decision rules deterministic (blocker/high→rejected, medium→needs_review,
  low-only→passed, missing→incomplete); HIGH loop risk forces human review even on low-only;
  scanner runs on PRIVATE raw + reuses `scan_secrets`, never echoes values (overclaim/secret
  findings carry codes only); persistence private 0o600 report.json + safe job-metadata copy,
  idempotent by (trust_report_id, candidate_hash, request_package_id/self_attempt_id); imports
  only stdlib + sibling orchestration modules (no provider SDK / urllib / socket / subprocess);
  no `source_apply`/`patch_apply`/approve/PR/git anywhere. Self-dogfood candidates route via the
  `self_dogfood:<attempt>` provider label through self-relevance (fixes the only full-suite
  regression). Local-advisor critique hook DEFERRED (forward seam `advisor_critique=None`).
- Backward-compat: existing provider trust/material suites (72) + orchestrator/progress/feature/
  review-bundle/cockpit/run_contract/catalog all green; review_bundle count test updated 23→24.

## Reviewer Final Verdict — Steps 1537-1572 (Provider Trust Verification v1)
**PASS.** Zero open Blocker/High; zero findings filed. Verification is a SAFE, deterministic
second-stage gate: unsafe/unverified accepted candidates create no pending intent; overclaim/
unrelated/repeated-failed/secret candidates never pass silently; no provider/model execution,
network, subprocess, provider SDK, apply, approval, PR, or git; reports leak no raw candidate/
diff/source/secret/path/traceback; the optional local-advisor critique is deferred and cannot
pass/reject by itself. Full suite 5812 passed/8 skipped/1 deselected. Merge-ready. NO PR
(Step 1572). Next id: R-0088.
