# Live Review — Steps 1609-1644: Automated Local Candidate Generator v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: Generate a repair candidate ONLY via an explicit, loopback-only, routing-gated LOCAL model
adapter, then immediately route the output through the EXISTING Provider Trust Gate + Verification +
Materialization pipeline. Must NOT: be enabled by default, break deterministic flow when the local
model is missing, allow non-loopback endpoints, import provider/cloud SDKs, use subprocess/shell/
external network/browser, bypass Builder Routing, run without a request package, bypass Trust Gate /
Verification, materialize/create intent before trust+verification pass, auto-approve/apply/test a
generated intent, loop generation without new evidence, ignore pending intent/approval, leak raw
prompt/output/source/diff/log/secrets/tracebacks/abs paths, or emit fake next actions. NO PR unless
user asks (Step 1644).
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PASS — reviewed @ commit `dde0bc6`; ZERO open findings. All 14 checks PASS. The local generator is
DISABLED by default + loopback-only (reuses the validated local_model_advisor `_validate_endpoint` +
`_stdlib_transport` — no new HTTP client); a missing/unavailable model returns a safe blocked/
unavailable result and NEVER breaks deterministic flow; generation runs ONLY when Builder Routing
selected the `local_candidate_generator` tier (no bypass), a request package exists, no pending intent,
contract allows, and budget/attempt caps not exhausted; generated output is treated as UNTRUSTED and
routed through the EXISTING `intake_provider_repair` pipeline (quarantine → Trust Gate → Verification →
Materialization) — the adapter NEVER parses to an intent directly and NEVER creates/approves/applies/
tests an intent; a pending patch intent is created ONLY when the PTV-v1 gate (trust ACCEPTED + verif
PASSED + supported materialization) sets `repair_intent_id`; idempotent by (request_package_id, model,
prompt_hash); raw prompt/output only in private 0o600 storage (public = hashes/labels/counts/IDs);
no provider/cloud SDK / subprocess / external net / browser / apply / git / PR; all emitted
next_safe_action are catalog-valid (R-0088 lesson applied: `builder-routing report --job-id`,
`local-candidate generate --request-package-id/--job-id/--routing-id`). REVIEWER-INDEPENDENT
verification: targeted `scripts/remedy_pytest.sh` (test_local_candidate_generator + test_local_candidate_cli
+ test_review_bundle + test_dashboard_cockpit_truth + test_builder_routing) = **139 passed**; builder-
reported full pytest 5887 passed/8 skipped/1 deselected (exit 0) — relied on per standing rule.
Changed-files table present in `.agent/context.md` (16 rows, reconciled vs `git diff --name-only
4d4d7ad..dde0bc6` = 14 prod + 4 test + docs). Merge-ready. NO PR (Step 1644).

## Check Matrix (1-14)
| Check | Status | Note |
|---|---|---|
| 1. Handoff/mainline (clean main after routing merge; residuals preserved; no drift) | PASS | branch off 4d4d7ad (merged main); 0 drift commits |
| 2. Config/endpoint (disabled default; opt-in; loopback-only; timeout/size bound; unavailable safe) | PASS | enabled=False; _effective_enabled=enabled+ep_ok+model; reuses _validate_endpoint; timeout≤60; never raises |
| 3. Prompt (request-package based; one candidate; relative paths; no secrets/claims/raw) | PASS | _CANDIDATE_SCHEMA_INSTRUCTIONS (one candidate/relative/no-secrets/no-claims); _scrub_public+bound |
| 4. Storage (private prompt/output; 0o700/0o600; atomic/hash/bounded; no raw public) | PASS | _store_run prompt.md+raw_output.txt 0o600/dir 0o700 atomic bounded; manifest+public = hashes/IDs |
| 5. Intake bridge (enters provider intake/quarantine; deterministic label; linked generation_id; no direct parse-to-intent) | PASS | intake_provider_repair(provider=`local_candidate_generator:<model>`, STDIN); no direct parse-to-intent |
| 6. Trust/verification/materialization (reject stops; intent only after passed verif + supported material) | PASS | _status_from_intake maps trust/verif outcomes; intent only when intake.repair_intent_id (PTV gate) |
| 7. Routing gate (routing selected local_candidate_generator; no pending; budget/attempt/loop; live_review/contract) | PASS | _check_routing_gate requires LOCAL_CANDIDATE_GENERATOR tier; pending suppresses; budget caps; contract; review via routing |
| 8. CLI runtime (status/generate; JSON; no traceback; no shell; no real Ollama in CI) | PASS | status read_only / generate write_metadata; JSON; errors→stderr; transport injectable (no Ollama in CI) |
| 9. RunContract/budget (local distinct from cloud; usage counted; exhausted blocks generation only) | PASS | LOCAL_CANDIDATE_GENERATE/STATUS default-allowed non-cloud; usage from runs; budget blocks generation only |
| 10. Integrations (orchestrator/progress/feature/review/cockpit safe; no buttons/mutations) | PASS | routing emits string only (planning-only); fixed item_ids; bundle 25→26; cockpit counts/no buttons |
| 11. Idempotency (no dup quarantine/trust/verif/intent; pending blocks new gen; failed not retried endlessly) | PASS | _find_reusable_run by (pkg,model,prompt_hash); pending blocks; budget caps bound failed retries |
| 12. Redaction (no secrets/paths/tracebacks/source/diff/log in public) | PASS | _scrub_public; endpoint_label never raw host; raw only private 0o600 |
| 13. Architecture (no SDK/net/subprocess/apply/test/git/PR; no raw prompt/output in public dataclasses) | PASS | stdlib + reused loopback transport; lazy internal imports; no SDK/subprocess/source_apply/patch_apply/intent-creation |
| 14. Tests (targeted local-candidate/routing/trust/verif/material/catalog/redaction; full pytest ≤1×) | PASS | reviewer targeted = 139 passed; builder full 5887 passed/8 skipped/1 deselected (exit 0) |
| (handoff) Changed-files table present | PASS | table in context.md (16 rows); reconciled vs git diff 4d4d7ad..dde0bc6 |

## Findings — Steps 1609-1644
(none) — ZERO open Blocker/High/Medium/Low. Reviewed committed diff `4d4d7ad..dde0bc6` line-level +
targeted 139 passed.

NIT (not a finding): `LocalCandidateGenerationStopReason.REVIEW_BLOCKER` + `policy.stop_on_review_blocker`
are defined but never directly enforced in `run_local_candidate_generation` — review-blocker protection
is enforced transitively via the routing gate (review_blocks → builder_routing high risk →
HUMAN_REVIEW_REQUIRED tier ≠ local_candidate_generator → generation blocked). Harmless dead config.
NIT: `_next_action` else-branch `return f"remedy local-candidate status --json"` is an f-string with no
placeholder (cosmetic).

Next id: R-0091.

## Reviewer audit log
- PR #65 merged Expensive Builder Routing v0 (1573-1608) to main → `4d4d7ad`; reviewer verdict PASS
  @ `50ecb9d` (R-0088/R-0089/R-0090 resolved). New branch
  `feature/steps-1609-1644-automated-local-candidate-generator-v0` off `4d4d7ad` (clean merged main).
  `git log 4d4d7ad..HEAD` empty → no drift, no block code yet. Check 1 PASS. Awaiting builder commits.
- WATCH (this block layers a REAL local model generator on the loopback adapter): endpoint must stay
  loopback-only + disabled by default; generation must be routing-gated (local_candidate_generator
  tier) + request-package-required; output MUST enter the existing Trust Gate→Verification→
  Materialization pipeline (no direct parse-to-intent, no pre-trust materialization); no provider/
  cloud SDK / subprocess / external net; no raw prompt/output on public surfaces; idempotent;
  pending intent/approval suppresses new generation; loop guard on repeated failed generation.
