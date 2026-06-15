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
PENDING — block just started. New branch `feature/steps-1645-1680-local-candidate-quality-evaluation-v1`
off clean merged main `3641618` (PR #66 merged Local Candidate Generator v0; reviewer verdict PASS
@ c7ea7ff). Zero block commits (`git log main..HEAD` empty). No code to verdict yet. Merge-ready
CANNOT be claimed while this verdict is PENDING.

## Check Matrix (1-12)
| Check | Status | Note |
|---|---|---|
| 1. Handoff/mainline (clean main after local-candidate merge; residuals preserved; no drift) | PASS | branch off 3641618 (merged main); 0 drift commits |
| 2. Models/taxonomy (safe fields; clear outcome states; no raw content fields) | PENDING | |
| 3. Inputs/evidence (safe summaries; unknown stays unknown; no event-only proof promotion) | PENDING | |
| 4. Scoring/outcome (proof/test gates; rejected/unverified can't score high; pending≠completed; no invented costs) | PENDING | |
| 5. Idempotency/scorecards (stable fingerprints; no dup active evals; scorecards safe+bounded) | PENDING | |
| 6. Routing feedback (confidence/recommend only; no auto gen; pending suppresses gen; poor→human review) | PENDING | |
| 7. CLI runtime (evaluate/show/scorecard/report; JSON; markdown safe; no traceback; no shell) | PENDING | |
| 8. RunContract/catalog (metadata/read-only; catalog-backed; no may_execute_commands) | PENDING | |
| 9. Progress/Feature/Review/Cockpit (safe counts/status; no raw; no mutation buttons) | PENDING | |
| 10. Redaction (no secrets/paths/tracebacks/source/diff/log in public) | PENDING | |
| 11. Architecture (no provider/model/net/subprocess/apply/test/git/PR; no source_apply/patch_apply import; no auto approval) | PENDING | |
| 12. Tests (targeted candidate-quality/local-candidate/routing/verification/catalog/redaction; full pytest ≤1×) | PENDING | |
| (handoff) Changed-files table present | PENDING | |

## Findings — Steps 1645-1680
(none yet)

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
