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
PENDING — block just started. New branch `feature/steps-1609-1644-automated-local-candidate-generator-v0`
off clean merged main `4d4d7ad` (PR #65 merged Expensive Builder Routing v0; reviewer verdict PASS
@ 50ecb9d). Zero block commits (`git log 4d4d7ad..HEAD` empty). No code to verdict yet. Merge-ready
CANNOT be claimed while this verdict is PENDING.

## Check Matrix (1-14)
| Check | Status | Note |
|---|---|---|
| 1. Handoff/mainline (clean main after routing merge; residuals preserved; no drift) | PASS | branch off 4d4d7ad (merged main); 0 drift commits |
| 2. Config/endpoint (disabled default; opt-in; loopback-only; timeout/size bound; unavailable safe) | PENDING | |
| 3. Prompt (request-package based; one candidate; relative paths; no secrets/claims/raw) | PENDING | |
| 4. Storage (private prompt/output; 0o700/0o600; atomic/hash/bounded; no raw public) | PENDING | |
| 5. Intake bridge (enters provider intake/quarantine; deterministic label; linked generation_id; no direct parse-to-intent) | PENDING | |
| 6. Trust/verification/materialization (reject stops; intent only after passed verif + supported material) | PENDING | |
| 7. Routing gate (routing selected local_candidate_generator; no pending; budget/attempt/loop; live_review/contract) | PENDING | |
| 8. CLI runtime (status/generate; JSON; no traceback; no shell; no real Ollama in CI) | PENDING | |
| 9. RunContract/budget (local distinct from cloud; usage counted; exhausted blocks generation only) | PENDING | |
| 10. Integrations (orchestrator/progress/feature/review/cockpit safe; no buttons/mutations) | PENDING | |
| 11. Idempotency (no dup quarantine/trust/verif/intent; pending blocks new gen; failed not retried endlessly) | PENDING | |
| 12. Redaction (no secrets/paths/tracebacks/source/diff/log in public) | PENDING | |
| 13. Architecture (no SDK/net/subprocess/apply/test/git/PR; no raw prompt/output in public dataclasses) | PENDING | |
| 14. Tests (targeted local-candidate/routing/trust/verif/material/catalog/redaction; full pytest ≤1×) | PENDING | |
| (handoff) Changed-files table present | PENDING | |

## Findings — Steps 1609-1644
(none yet)

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
