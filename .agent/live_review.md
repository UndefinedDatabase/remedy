# Live Review — Steps 1499-1536: Local Model Advisor Adapter v0

Reviewer: parallel reviewer
Scope: Optional Ollama-compatible local-model advisory layer for orchestrator decisions.
Loopback-only, DISABLED by default, advisory-only. The deterministic orchestrator MAY ask
a local advisor to critique a SAFE decision summary; the advisor may flag concerns/
alternatives/missing evidence; the orchestrator verifies everything against deterministic
evidence; the final next_safe_action stays deterministic + catalog-backed + entity-backed.
Must NOT: call external network, import provider/cloud SDKs, be enabled by default, break
deterministic orchestration when the model is missing, let model output become commands/
entities/approvals/applies/PRs/jobs, override contract/budget/review blockers, mark evidence
true/complete, leak raw prompt/response/source/diff/logs/secrets/tracebacks/abs paths, or
loop endlessly on repeated advisor failure. NO PR unless user asks (Step 1536).
Timestamp: 2026-06-14

## Verdict
PENDING — implementation in progress.

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation (PR #62 merged; clean branch; residuals carried) | PENDING | |
| 2. Advisor models (no raw prompt/response fields) | PENDING | |
| 3. Config (loopback-only; disabled by default; scrubbed) | PENDING | |
| 4. Safe prompt builder (safe summaries only; no raw) | PENDING | |
| 5. Response schema + parsing (unparseable safe; code/diff → high concern) | PENDING | |
| 6. Private run storage (0o700/0o600; atomic; bounded; no public raw) | PENDING | |
| 7. Ollama client (stdlib; loopback; timeout; bounded; no SDK/subprocess) | PENDING | |
| 8. Availability probe (disabled/non-loopback/timeout → unavailable, no crash) | PENDING | |
| 9. Orchestrator integration (deterministic first; final action deterministic) | PENDING | |
| 10. Advisor impact rules (lower confidence/escalate only; no commands/override) | PENDING | |
| 11. Anti-loop integration (reuse by prompt_hash; failure → loop guard) | PENDING | |
| 12. CLI + catalog + RunContract (status read_only; run write_metadata; no exec) | PENDING | |
| 13. Budget/usage + Progress/Feature/Review(23)/Cockpit integrations | PENDING | |
| 14. Redaction (no raw prompt/response/secrets/paths/tracebacks in public) | PENDING | |
| 15. Architecture guards (no provider SDK/cloud/subprocess/network/apply/git/PR) | PENDING | |

## Findings — Steps 1499-1536
(none yet) — Next id: R-0087.

## Reviewer audit log
- `a079378` reconciliation: touches only `.agent/{context,plan,live_review}.md`; branch off clean main `5d4cdf4` (PR #62 merged). No production drift. Check 1 OK. Prior block zero open findings — nothing to carry.
- `2021606` core `local_model_advisor.py` (916L) reviewed — ZERO findings. Verified: disabled-by-default (`enabled=False`; `effective=enabled and ep_ok and bool(model)`); loopback-only `_validate_endpoint` (host∈{127.0.0.1,localhost,::1}, non-loopback never echoed, redirects rejected via `_NoRedirect`, timeout≤30 enforced, `MAX_RESPONSE_BYTES` bound→OVERSIZED); safe JSON-only prompt (scrub+bound, no code/secrets); stdlib urllib only (no subprocess/SDK/shell/external net); parse never raises (unparseable/oversized safe, code/diff→high concern, `_scrub_public`+`scan_secrets`); anti-loop `_count_unavailable≥2` suppress + `MAX_RETRIES=1`; impact advisory hint-only (orchestrator re-derives binding); raw prompt/response private 0o700/0o600 atomic only, public = hashes+counts+scrubbed.
  - NIT (not a finding): line 317 `endpoint=endpoint if ep_ok else endpoint` dead ternary (identical branches); harmless (raw endpoint in-memory only, non-loopback cannot be effective-enabled).
- PENDING for later commits: Check 9 (orchestrator binding-impact / final action stays deterministic), Check 10 (no command/entity/ProposedTask/PatchIntent from advisor; no contract/budget/review override), Checks 11-13 (CLI local-advisor status/run + decide --use-local-advisor, catalog, run_contract, budget, Progress/Feature/Review/Cockpit), Check 14 tests.
