# Live Review — Steps 1645-1680: Candidate Quality Evaluation v1

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: Evaluate generated/external candidate USEFULNESS from DURABLE evidence (trust report,
verification report, materialization/intent state, proof chain, linked test runs) and feed SAFE
scorecards back into Builder Routing as confidence/recommendation signals. Read/metadata-only. Must
NOT: execute models/providers, call network/subprocess, apply patches, approve work, run tests,
create PRs/git; claim success without linked proof/test evidence; let rejected/unverified candidates
score high/excellent; treat pending approval as completed; treat model confidence/text as truth;
trigger automatic generation via routing feedback; leak raw prompt/output/candidate/diff/source/log/
secrets/abs paths; emit fake next actions. NO PR unless user asks (Step 1680).
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PASS — reviewed @ commit `600304e`; ZERO open findings. All 12 checks PASS. Quality evaluation is
evidence-only: `_classify` is durable-evidence-driven (local_candidate run manifest + trust report +
verification report + intent state via get_patch_intent + apply/test/proof via authoritative
`build_proof_chain`) — NEVER model confidence/text, NEVER event-only proof promotion. `_score`
enforces the no-success-without-proof CEILINGS: verification≠pass → cap MEDIUM (rejected/unverified
cannot score high), human_decision unknown → cap MEDIUM, proof_outcome≠pass → cap HIGH (EXCELLENT
requires proof_status==verified + test passed). PENDING_APPROVAL scored MEDIUM and explicitly "not
complete"; rejected/trust-failed → LOW; cost always "unknown" (never invented). `route_quality_feedback`
is a READ-ONLY confidence signal (raise/lower/neutral) that NEVER triggers generation — wired into
builder_routing step 8 so poor history (reject_rate≥0.5 / loop≥2) escalates to HUMAN_REVIEW_REQUIRED
instead of recommending more generation (routing still emits a string only). Evaluator does NO
model/provider/network/subprocess/apply/approve/test/git/PR; reports carry codes/IDs/counts/bands/
dimensions only (no raw prompt/output/candidate/diff/source/secret/path); idempotent by evidence
fingerprint; `candidate_quality_integrity` flags success_without_proof / high_score_for_rejected /
duplicate_fingerprint. All emitted next_safe_action are catalog-valid (R-0088 lesson applied:
`candidate-quality show <evaluation_id>` positional matches catalog; `patch approve`, `do continue
--intent-id`, `provider verification-show`/`trust-show`). REVIEWER-INDEPENDENT verification: targeted
`scripts/remedy_pytest.sh` (test_candidate_quality + test_candidate_quality_cli + test_review_bundle +
test_dashboard_cockpit_truth + test_builder_routing) = **145 passed**; builder-reported full pytest
5927 passed/8 skipped/1 deselected (exit 0) — relied on per standing rule. Changed-files table present
in `.agent/context.md`. Merge-ready. NO PR (Step 1680).

## Check Matrix (1-12)
| Check | Status | Note |
|---|---|---|
| 1. Handoff/mainline (clean main after local-candidate merge; residuals preserved; no drift) | PASS | branch off 3641618 (merged main); 0 drift commits |
| 2. Models/taxonomy (safe fields; clear outcome states; no raw content fields) | PASS | 16 outcomes + finding codes + bands; export = codes/IDs/counts/dims only |
| 3. Inputs/evidence (safe summaries; unknown stays unknown; no event-only proof promotion) | PASS | _gather_evidence durable summaries; build_proof_chain authoritative; try/except→unknown |
| 4. Scoring/outcome (proof/test gates; rejected/unverified can't score high; pending≠completed; no invented costs) | PASS | _score ceilings (verif/human/proof); rejected→LOW; pending=MEDIUM not complete; cost=unknown |
| 5. Idempotency/scorecards (stable fingerprints; no dup active evals; scorecards safe+bounded) | PASS | _fingerprint stable; _find_existing reuse; scorecards counts/rates only |
| 6. Routing feedback (confidence/recommend only; no auto gen; pending suppresses gen; poor→human review) | PASS | route_quality_feedback read-only; builder_routing step 8 lower→HUMAN_REVIEW; never generates |
| 7. CLI runtime (evaluate/show/scorecard/report; JSON; markdown safe; no traceback; no shell) | PASS | evaluate write_metadata / show+scorecard+report+integrity read_only; JSON; errors→stderr |
| 8. RunContract/catalog (metadata/read-only; catalog-backed; no may_execute_commands) | PASS | 4 actions default-allowed non-cloud; may_execute_commands=False |
| 9. Progress/Feature/Review/Cockpit (safe counts/status; no raw; no mutation buttons) | PASS | fixed item_ids; bundle +candidate_quality_summary; cockpit counts/no buttons |
| 10. Redaction (no secrets/paths/tracebacks/source/diff/log in public) | PASS | _scrub_public on summaries; public = codes/IDs/counts/bands/dims only |
| 11. Architecture (no provider/model/net/subprocess/apply/test/git/PR; no source_apply/patch_apply import; no auto approval) | PASS | stdlib + _scrub_public; lazy durable-reader imports; reads intent state never sets it |
| 12. Tests (targeted candidate-quality/local-candidate/routing/verification/catalog/redaction; full pytest ≤1×) | PASS | reviewer targeted = 145 passed; builder full 5927 passed/8 skipped/1 deselected (exit 0) |
| (handoff) Changed-files table present | PASS | table in context.md; reconciled vs git diff 3641618..600304e |

## Findings — Steps 1645-1680
(none) — ZERO open Blocker/High/Medium/Low. Reviewed committed diff `3641618..600304e` line-level +
targeted 145 passed. Builder committed reviewer PENDING ledger (no pre-written verdict).

Next id: R-0091.

## Reviewer audit log
- PR #66 merged Local Candidate Generator v0 (1609-1644) to main → `3641618`; reviewer verdict PASS
  @ `c7ea7ff`. New branch `feature/steps-1645-1680-local-candidate-quality-evaluation-v1` off
  `3641618` (clean merged main). `git log main..HEAD` empty → no drift, no block code yet. Check 1 PASS.
- WATCH: quality score MUST derive from DURABLE truth (build_proof_chain / build_snapshot_truth /
  linked test_run_id / verification decision), NEVER from event presence or model confidence/text;
  rejected/unverified/pending candidates must NOT score high; pending approval ≠ completed; scorecard
  public = safe counts/labels/IDs only (no raw prompt/output/candidate/diff/source/log); routing
  feedback influences confidence/recommendation ONLY (no auto generation); pure read/metadata — no
  model/provider/network/subprocess/apply/approve/test/git/PR; idempotent; emitted next actions
  catalog-valid (R-0088 lesson).
