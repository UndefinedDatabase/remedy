# Context

## Active Branch
feature/steps-1537-1572-provider-trust-verification-v1 (forked from clean main at 50ea930
after PR #63 merged Local Model Advisor Adapter v0). No drift.

## Mainline reconciliation (Step 1537)
- PR #63 MERGED → main. Current main commit: 50ea930.
- Local Model Advisor Adapter v0 landed: local_model_advisor.py (optional, loopback-only,
  disabled-by-default advisory critique for orchestrator decisions; advisory-only, never
  executes, never imports provider/cloud SDK). `remedy local-advisor status/run`,
  `remedy orchestrator decide --use-local-advisor`. R-0087 (handoff table) resolved.
  Full suite 5777 passed, 8 skipped, 1 deselected.

## Scope
Steps 1537-1572: Provider Trust Verification v1 — second-stage verification layer for
UNTRUSTED external candidate output before/during materialization into pending repair intents.

## Core principle
Trust Gate = candidate SAFE to ingest. Verification = candidate PLAUSIBLE, RELEVANT, BOUNDED,
WORTHY of becoming a pending intent. Accepted ≠ verified ≠ approved ≠ applied. Approval + apply
stay separate. Evidence is truth. Local-advisor/model output, if used, is critique only.

## Carried residual risks
- External/provider builder EXECUTION still not built (plan-only routing; request packages only).
- Broader source patch materialization deferred (apply path .md-only).
- Provider Trust Verification NOT built before this block (this block builds it).
- Self overnight not built; cleanup/retention automation not built.
- Regex/heuristic scanning can miss novel secret formats (entropy heuristic mitigates, not perfect).
- Pre-existing deselected `test_project_brain.py::...::test_full_chain_order`.
- UI `npm run lint` pre-existing TS parser/dependency blocker (no deps allowed).

## Provider Trust Verification constraints (block 1537-1572)
- Unsafe/unverified accepted candidates MUST NOT create pending intents. v1 prefers verify-before-intent.
- NO provider/model execution, cloud API, external network, browser, subprocess (except CLI runtime tests).
- NO automatic apply/approval/repair-loop/PR/merge/git-commit-gate/background orchestration/UI mutation/MCP.
- NO provider SDK imports; no shell=True; no dependency upgrades.
- Verification reports = SAFE summaries only. NO raw provider output/diff/source/stdout/stderr/
  artifact-body/secrets/tracebacks/absolute private paths in any public surface.
- Verification cannot approve/apply/test/create PRs.
- Local advisor (if used) critique-only: may only lower confidence / add human-review concern; cannot pass/reject/create commands/override deterministic checks.
- Overclaim / unrelated / repeated-failed candidates must not pass silently.
- Every next_safe_action exists in command catalog + references real entities.
- NO PR unless the user explicitly asks (Step 1572).

## Foundation reused
- provider_trust (intake_provider_repair flow; _scrub_public/scan_secrets/_SECRET_PATTERNS/
  _ABS_PATH_RE/_TRACEBACK_RE; Severity; TrustStatus; _safe_path_label; read quarantine raw privately).
- provider_patch_material (materialize_accepted_candidate; MaterialState; candidate_hash=sha256(raw_patch); load materials).
- repair_request_builder (RepairRequestPackage; get_request_package/load_request_packages) for consistency.
- run_contract (ensure_contract/evaluate_run_action/ContractAction; ALL_KNOWN auto-derived; add provider_verify_candidate/provider_verification_show).
- data_paths.resolve_data_root; storage.load_job/save_job; command_catalog/grouped CLI.
- progress_ledger.merge_*, feature_planner, review_bundle (REQUIRED_SECTIONS +provider_verification_summary.json), ui_server cockpit.
- local_model_advisor (optional critique hook — deferred/conservative; see docs).

## Resource safety (standing)
- No background pytest. Use `scripts/remedy_pytest.sh` (flock-serialized); full suite once
  at block end with `-k "not test_full_chain_order"`. No shell=True, no subprocess.

## Product readiness — Provider Trust Verification v1 (Step 1567)
CAN: run a second-stage SAFE verification on UNTRUSTED candidate output before it becomes a
pending intent (`remedy provider verify`, `remedy provider verification-show`; inline during
`provider intake-repair`). Checks request/candidate consistency, failure/self relevance,
overclaim, minimality/scope, testability, loop risk, secret/entropy. Decision rules:
blocker/high→rejected, medium→needs_review, low-only→passed, missing→incomplete. PASSED is the
ONLY path to materialization+pending intent; non-passing creates NO intent. Surfaced in
Progress/Feature/Review(24 sections)/Cockpit; safe report in job metadata + private
0o600 report.json. Orchestrator recommends verify for accepted-but-unverified and escalates
needs-review/repeated-rejection to human review.
CANNOT (by design): execute providers/models/patches/tests; approve/apply/create PRs/git;
import provider SDK / network / subprocess; let unsafe/unverified candidates create intents;
let overclaim/unrelated/repeated-failed candidates pass silently; leak raw candidate/diff/
source/secrets/tracebacks/abs paths. Local advisor critique hook DEFERRED (forward seam only;
if built, critique-only — cannot pass/reject).
Readiness ~88% (verification rail complete; advisor critique hook + expensive routing deferred).

## Status
Steps 1537-1572 COMPLETE. Full pytest 5812 passed, 8 skipped, 1 deselected (exit 0); integrity
clean (only "relevant untracked" pre-commit). Live review verdict PASS. NO PR (Step 1572).

## Next block
Expensive Builder Routing v0 OR Automated Candidate Generator Adapter v0.
