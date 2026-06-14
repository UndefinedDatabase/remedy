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
| 1. Mainline reconciliation (PR #62 merged; clean branch; residuals carried) | PASS | a079378 .agent-only; off clean main 5d4cdf4 |
| 2. Advisor models (no raw prompt/response fields) | PASS | public = hashes/counts/scrubbed only |
| 3. Config (loopback-only; disabled by default; scrubbed) | PASS | enabled=False; effective gate; no token field |
| 4. Safe prompt builder (safe summaries only; no raw) | PASS | counts/kind/label/score; JSON-only; scrub+bound |
| 5. Response schema + parsing (unparseable safe; code/diff → high concern) | PASS | never raises; oversized/code-diff handled |
| 6. Private run storage (0o700/0o600; atomic; bounded; no public raw) | PASS | raw only in private dir; manifest safe |
| 7. Ollama client (stdlib; loopback; timeout; bounded; no SDK/subprocess) | PASS | urllib only; _NoRedirect; size-bounded |
| 8. Availability probe (disabled/non-loopback/timeout → unavailable, no crash) | PASS | degrades; never raises |
| 9. Orchestrator integration (deterministic first; final action deterministic) | PASS | escalate→report cmd or unchanged; never strengthens |
| 10. Advisor impact rules (lower confidence/escalate only; no commands/override) | PASS | tightens only; contract+budget gated; no entity creation |
| 11. Anti-loop integration (reuse by prompt_hash; failure → loop guard) | PASS | _count_unavailable≥2 suppress |
| 12. CLI + catalog + RunContract (status read_only; run write_metadata; no exec) | PASS | UUID imported; LOCAL_ADVISOR_RUN non-cloud; no shell |
| 13. Budget/usage + Progress/Feature/Review/Cockpit integrations | PASS | fixed item_ids; FeaturePlanSource valid; no raw/buttons |
| 14. Redaction (no raw prompt/response/secrets/paths/tracebacks in public) | PASS | _scrub_public + scan_secrets; hashes only public |
| 15. Architecture guards (no provider SDK/cloud/subprocess/network/apply/git/PR) | PASS | stdlib only; no SDK/subprocess in any new file |
| (tests) Targeted suite + full pytest once | PENDING | steps 1521-1526 not yet committed |

## Findings — Steps 1499-1536
(none yet) — Next id: R-0087.

## Reviewer audit log
- `a079378` reconciliation: touches only `.agent/{context,plan,live_review}.md`; branch off clean main `5d4cdf4` (PR #62 merged). No production drift. Check 1 OK. Prior block zero open findings — nothing to carry.
- `2021606` core `local_model_advisor.py` (916L) reviewed — ZERO findings. Verified: disabled-by-default (`enabled=False`; `effective=enabled and ep_ok and bool(model)`); loopback-only `_validate_endpoint` (host∈{127.0.0.1,localhost,::1}, non-loopback never echoed, redirects rejected via `_NoRedirect`, timeout≤30 enforced, `MAX_RESPONSE_BYTES` bound→OVERSIZED); safe JSON-only prompt (scrub+bound, no code/secrets); stdlib urllib only (no subprocess/SDK/shell/external net); parse never raises (unparseable/oversized safe, code/diff→high concern, `_scrub_public`+`scan_secrets`); anti-loop `_count_unavailable≥2` suppress + `MAX_RETRIES=1`; impact advisory hint-only (orchestrator re-derives binding); raw prompt/response private 0o700/0o600 atomic only, public = hashes+counts+scrubbed.
  - NIT (not a finding): line 317 `endpoint=endpoint if ep_ok else endpoint` dead ternary (identical branches); harmless (raw endpoint in-memory only, non-loopback cannot be effective-enabled).
- `cc7a645` integration (orchestrator advisory mode + CLI + contract + integrations) reviewed — ZERO findings.
  - Check 9 (final action deterministic): `consult_local_advisor_for_decision` only either leaves action unchanged or escalates to `StopReason.HUMAN_REVIEW_REQUIRED` with `next_safe_action="remedy orchestrator report --json"` (deterministic catalog command). Advisor never emits a new command; never strengthens. ✓
  - Check 10 (no creation / no override): advisor can ONLY lower confidence (`_lower_confidence`, monotone-down) or escalate to human review. Escalation gated by `decision.stop_reason==SELECTED and not open_blocker and (loop_risk==high or high_concern) and deterministic _evidence_is_weak` — strictly tightens, can't clear a blocker/enable an action. No ProposedTask/PatchIntent/approval/apply. Contract-gated via `evaluate_run_action(..., ContractAction.LOCAL_ADVISOR_RUN)`; denial → no change. Budget enforced in `run_local_advisor`. ✓
  - Check 11 (anti-loop): `_count_unavailable≥2` (MAX_UNAVAILABLE_REPEAT) suppress until new evidence; unavailable attempts persisted for the count. ✓
  - Check 12 (CLI/catalog/contract): `local-advisor.status` read_only, `local-advisor.run` + `orchestrator.decide --use-local-advisor` write_metadata, all `may_execute_commands=False`/`may_mutate_repo=False`; decide runs deterministic select first then advisory consult then single persist; degrades to disabled msg (no Ollama in CI); `UUID` imported (line 37, no crash); `LOCAL_ADVISOR_STATUS/RUN` in `_DEFAULT_ALLOWED_ACTIONS` only (distinct from cloud — no_cloud doesn't deny local loopback). No shell=True. ✓
  - Check 13 (integrations): progress_ledger `merge_local_advisor_items` fixed item_ids de-duped, safe summaries (status/impact/counts); feature_planner 3 rules map to valid `FeaturePlanSource.ROADMAP/KNOWN_RISK`; review_bundle REQUIRED_SECTIONS += `local_advisor_summary.json` (counts/labels/IDs only); ui_server cockpit section counts/status only, no buttons/mutation/raw. ✓
  - Check 15 (arch): stdlib urllib only; no provider SDK/cloud/subprocess/shell/external net/apply/git/PR/browser in any new file. ✓
  - NIT (not a finding): review_bundle `_build_local_advisor_summary` `sev_counts` is declared but never populated (manifest carries no per-finding list) → `finding_severity_counts` always `{}`. Cosmetic, no leak.
- PENDING: Check 14 (targeted tests — redaction/endpoint/parsing/impact/CLI/arch guards; steps 1521-1526 not yet committed) + full pytest once + final handoff (changed-files table, integrity, verdict).
