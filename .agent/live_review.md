# Live Review — Steps 1429-1464: Self-Dogfood Execution v0

Reviewer: parallel reviewer
Scope: After human approval of a self-dogfood ProposedTask, create+track a bounded
SelfImprovementAttempt routed through EXISTING gates (request → Provider Trust Gate →
materialization → approval → do continue → snapshot/apply/test/proof). Orchestrator/
tracking rail. Must NOT: edit code, apply outside do continue, approve, create PRs,
mutate main/master, do git ops, insert Job.tasks, call provider/network/subprocess/
browser, bypass the Trust Gate, mark pending intent completed, overclaim test/proof,
duplicate attempts/intents, leak raw source/diff/logs/secrets/paths. NO PR unless user asks.
Timestamp: 2026-06-14

## Verdict
PENDING — block in progress. Builder constructing self_dogfood_execution.py + CLI on
top of main fa8ebe2 (PR #60 merged). Hard completion criteria (Step 1459) gate verdict.

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | 3bd6eac off clean main fa8ebe2; PR#60 recorded; residuals carried; only .agent/ files touched; no drift; PR held (Step 1457/1464) |
| 2. Self-execution models (no raw fields) | PASS | Attempt/Linkage/Checkpoint/Result hold IDs/states/scrubbed title only; no raw |
| 3. Attempt storage (atomic, safe-transition, hashed) | PASS | _atomic_write 0o600 tmp+os.replace; attempt.json; fingerprint dedup; _transition legality-checked |
| 4. Eligibility (approved self ProposedTask; no dup; review ok) | PASS | task_type==self_dogfood + status==APPROVED_FOR_BUILD; non-self/unapproved blocked; _review_blocks (PENDING/FAIL/blocker-high); contract SELF_EXECUTE_PREPARE; target_repo + branch gate; dup active→resume |
| 5. Branch/main safety gate | PASS | current_branch reads .git/HEAD only (NO subprocess/git); refuses main/master/detached(unknown); no branch creation/git mutation |
| 6. Attempt state machine (legal; pending≠completed) | PASS w/ R-0085 | legal forward transitions; reconcile reaches COMPLETED only via PROOF_VERIFIED after proof==verified; integrity flags completed_without_proof. R-0085 (LOW): table latently permits COMPLETED from INTENT_APPROVED/TESTED_PASSED/EVIDENCE_INCOMPLETE |
| 7. Self request package (no FailureArtifact) | PASS | no fa; scrubbed title/detail; one-candidate+.md-only+no-secrets+no-apply/test-claim constraints; required schema; stored 0o600 |
| 8. CLI self execute → awaiting_external_candidate (real intake cmd) | PASS | start_self_execution stops at awaiting; next_safe_action = real provider intake-repair (no fa; generic intake tolerant, no fake fa); write_metadata no-mutate/no-exec |
| 9. Generic candidate intake compat + intent linkage | CONCERN R-0084 | intake compat OK (validate_failure_link handles empty fa; arg required=False; no bypass of Trust Gate). BUT reconcile intent-linkage uncorrelated → R-0084 (MEDIUM) mislink/false-completion |
| 10. do continue compatibility (snapshot/test/proof; no overclaim) | PASS w/ R-0084 | approved self intent → existing `do continue` (next_action); proof from authoritative build_proof_chain per intent_id; completed only if proof==verified. Overclaim possible only via mislink (R-0084) |
| 11. CLI self status / reconcile (read/metadata-only) + RunContract | PASS | status/integrity read_only, reconcile write_metadata (no apply/provider); SELF_RECONCILE/STATUS/EXECUTE_PREPARE allowed not cloud; all next-actions catalog-backed (incl job.attach-repo) |
| 12. Integrations (Progress/Feature/Review/Cockpit/self report) | PENDING | feature_planner/progress_ledger/review_bundle/ui_server uncommitted |
| 13. Redaction | PASS (code) | _scrub_public+[:300] on title/detail; attempts hold IDs/states only; await committed redaction test |
| 14. Architecture guards (no apply/provider/git/PR/Job.tasks/main-mutation) | PASS (code) | imports stdlib+internal only; NO source_apply/patch_apply/subprocess/network/provider/git/Job.tasks; reconcile no apply/approve; await committed guard test |
| 15. Idempotency + E2E simulated self-improvement | PARTIAL | idempotency PASS (fingerprint dedup→resume; reconcile excludes other-attempt intents); E2E test not yet committed |

## Findings — Steps 1429-1464

## Finding R-0084
Status: Open
Severity: medium
Area: intent-linkage
Summary: reconcile attaches the newest unlinked accepted provider intent to a self attempt with NO correlation to that attempt — risk of mislink + false completion (proof overclaim).
Details: `reconcile_self_attempt` (self_dogfood_execution.py:664-677), when `a.patch_intent_id`
is empty, iterates ALL job trust reports newest-first and links the first `repair_intent_id`
not already linked to another self attempt. There is no correlation to THIS attempt's
request: TrustReport carries no `provider` label (verified: provider_trust.py TrustReport /
export_trust_report_json have repair_intent_id/report_id/material_id/received_at but NO
provider field) and the attempt records no intake/report id at candidate-import time
(start_self_execution stops at awaiting_external_candidate; patch_intent_id is ONLY ever set
by this heuristic). If the same job also has a regular provider repair (e.g.
`intake-repair --failure-artifact-id ... --provider claude`) producing an accepted
materialized intent, reconcile can attach THAT unrelated intent to the self attempt; once it
is approved + `do continue`d to verified proof, reconcile marks the self attempt COMPLETED
(lines 689-692). That is an unrelated change marking the self attempt complete — a
proof/completion overclaim and a cross-flow linkage error.
Evidence: self_dogfood_execution.py:664-677 (heuristic link), 679-692 (proof→completed);
provider_trust.py:195-206 TrustReport has no provider field; export_trust_report_json
(770-786) emits no provider/attempt correlation key.
Expected fix: correlate the linked intent to the self attempt instead of guessing. Preferred:
record the trust report id / intent id on the attempt at an explicit candidate-import step
(metadata-only) rather than newest-unlinked heuristic; OR add a `provider`/origin label to the
trust report and filter to the self-dogfood provider label AND match the attempt's
request/material. At minimum, gate linkage so an intent that cannot be correlated to this
attempt is NOT auto-adopted.

## Finding R-0085
Status: Open
Severity: low
Area: state-machine
Summary: state transition table permits COMPLETED without verified proof (latent; reconcile + integrity-check currently gate it, but the table is over-permissive).
Details: `_TRANSITIONS` (self_dogfood_execution.py:81-113) allows COMPLETED directly from
INTENT_APPROVED (95-98), TESTED_PASSED (105-106) and EVIDENCE_INCOMPLETE (110). Current code
only ever reaches COMPLETED via PROOF_VERIFIED after `proof == "verified"` (689-692), and
`self_integrity_check` flags `completed_without_proof` (746-747), so there is no LIVE
violation. But the table itself does not enforce the block-if invariant "no completed state
without linked proof" — a future caller using `_transition(a, COMPLETED)` from those states
would silently bypass proof. EVIDENCE_INCOMPLETE→COMPLETED is also semantically wrong.
Evidence: self_dogfood_execution.py:95-98, 105-106, 110; completion only gated in reconcile
(689-692) + integrity (746-747), not in the table.
Expected fix: restrict COMPLETED predecessors to {PROOF_VERIFIED} only; drop COMPLETED from
INTENT_APPROVED/TESTED_PASSED/EVIDENCE_INCOMPLETE edges so the state machine itself enforces
proof-before-completed.

Done: R-0084 — candidate intake for a self attempt is now correlated via provider label
`self_dogfood:<attempt_id>` (`_self_provider_label`): `self execute` / `_next_action_for`
emit the intake command with that label, and `reconcile_self_attempt` links ONLY a trust
report whose `provider_name == self_dogfood:<attempt_id>` (provider_name IS exported on the
trust report). A foreign/regular provider intent can no longer be adopted → no mislink, no
false completion. Regression test `test_reconcile_does_not_mislink_foreign_intent`.
Done: R-0085 — `_TRANSITIONS` now makes COMPLETED reachable ONLY from PROOF_VERIFIED;
dropped COMPLETED edges from INTENT_APPROVED/TESTED_PASSED/EVIDENCE_INCOMPLETE. Test
`test_transition_rejects_illegal` covers the illegal PROPOSED→COMPLETED jump.

### Reviewer audit log
- 2026-06-14: Block start. Worker at 3bd6eac (Step 1429 reconciliation). Branch
  feature/steps-1429-1464-self-dogfood-execution-v0 off clean main fa8ebe2 (PR#60 merged
  Self-Dogfood Planner v0). Reconciliation touches only .agent/ files. Plan steps 1430-1464
  each cover a stated check/block-if; hard rules align (orchestrator/tracking rail bypasses
  NO gate; no direct apply/approve/PR/merge/main-mutation/git/Job.tasks; candidate via
  existing Provider Trust Gate + materialization; approved intent via existing do continue;
  pending≠completed; idempotent by fingerprint+candidate-hash; branch/main safety; no raw
  leak; PR held Step 1457/1464). Residuals carried. Check 1 PASS. Worker now writing core.
  Next finding id: R-0084.
- 2026-06-14: Reviewed f06ebea (core+contract 1430-1441/1462) + b244e90 (CLI). self_dogfood_
  execution.py (769L): models, branch-safety (.git/HEAD read only), storage (0o600 atomic),
  eligibility, state machine, self request package, start/reconcile, integrity. CLI self
  execute/status/reconcile/integrity + report. Verified deps: ProposedTaskStatus.APPROVED_FOR_
  BUILD, get_proposed_task; contract SELF_EXECUTE_PREPARE/RECONCILE/EXECUTION_STATUS (allowed,
  not cloud); APPROVAL_APPROVED; build_proof_chain ProofChange.intent_id/.proof_status
  (authoritative, per-intent); all next-actions catalog-backed (incl job.attach-repo); intake
  tolerates empty fa (no fake fa). Block-ifs mostly cleared: no source_apply/patch_apply/
  subprocess/network/provider/git/PR/Job.tasks; candidate via existing Trust Gate (no bypass);
  approved intent via existing do continue; pending≠completed (reconcile gates COMPLETED on
  proof==verified); branch gate refuses main/master/detached; idempotent by fingerprint→resume.
  TWO FINDINGS: R-0084 (MEDIUM, intent-linkage) reconcile attaches newest unlinked accepted
  intent with NO correlation to the attempt (TrustReport has no provider field; attempt records
  no intake id) → mislink + false-completion overclaim if a regular provider repair intent
  exists in the same job. R-0085 (LOW, state-machine) transition table latently permits
  COMPLETED without proof (reconcile+integrity gate it, but tighten table). Checks 2-11 PASS
  (9/10 carry R-0084 concern, 6 carries R-0085). Check 12 PENDING (integrations uncommitted).
  13/14 PASS by code; 15 idempotency PASS, E2E pending. Await fixes + tests. Next id: R-0086.
