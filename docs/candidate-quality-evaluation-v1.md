# Local Candidate Quality Evaluation v1 (Steps 1645–1680)

Evidence-based quality scoring of candidate-generation OUTCOMES. After a candidate is generated and
run through the pipeline, this layer scores whether it was actually **useful** — not merely safe —
and builds model/route scorecards that feed FUTURE routing. It is **evaluation / reporting /
routing-feedback only**.

## Core principle

> Evidence, not model confidence, determines quality. No score claims success without linked
> proof/test evidence. Candidate quality feeds future routing. No automatic execution.

## The stages are different things

`generated ≠ safe (trust) ≠ relevant (verification) ≠ materialized ≠ approved ≠ applied ≠
proven`. Quality evaluation reads all of these as **separate evidence** and only the full chain
(approved + applied + linked passing test + verified proof) earns a high/excellent score.

## Evidence inputs (read-only, safe summaries)

local candidate run manifests · provider trust reports · provider verification reports · patch
intent approval state · proof chain (`build_proof_chain` → per-intent approval/apply/test/proof
status) · builder routing traces. Unknown stays unknown; **missing evidence becomes risk, never
success**.

## Score dimensions

`request_adherence · safety_trust · verification_quality · materialization_quality ·
human_decision · apply_outcome · test_outcome · proof_outcome · scope_minimality · loop_risk ·
cost_efficiency`. Each is `pass | fail | partial | unknown | n/a`. Cost is **never invented**
(`unknown`).

### Invariant ceilings (enforced in `_score`)

- Score ≤ **medium** when verification did not pass.
- Score not **high** when the human decision is unknown.
- Score not **excellent** without `proof_outcome == pass` (proof_verified).
- Rejected / trust-failed candidates score **low**. Pending approval is **not** completed.

## Outcomes

`generated_unavailable · generated_blocked · trust_rejected · verification_rejected ·
needs_human_review · materialization_failed · pending_approval · human_rejected ·
approved_pending_continue · applied_pending_tests · tests_failed · proof_verified ·
completed_success · completed_with_risks · evidence_incomplete`.

## Idempotency

`evaluate_candidate_quality(...)` is idempotent by an **evidence fingerprint** (trust/verification/
intent ids + run status + intent/proof/test/apply state). Repeated evaluation returns the same
report; when the underlying evidence changes, the fingerprint changes and a fresh evaluation is
produced (no duplicate active scorecards). `--new` forces a fresh evaluation.

## Model / route scorecards

`build_candidate_scorecards()` aggregates by model and route tier: run_count, trust/verification/
materialization/approval/apply/proof rates, rejection_rate, average_score, loop_risk,
unknown_cost_count. Safe counts only — no raw content.

## Routing feedback (read-only; never triggers generation)

`route_quality_feedback(model, route_tier)` returns a confidence signal Builder Routing consults:
repeated rejections / loop risk → `lower` (Builder Routing escalates the local-candidate tier to
human review instead of recommending more generation); proof-verified successes → `raise`; no
evidence → `unknown` / neutral. **Unknown quality never promotes an expensive builder.** Feedback
never causes automatic generation.

## CLI

- `remedy candidate-quality evaluate [--generation-id|--trust-report-id|--verification-id|--intent-id|--job-id] [--new] --json` — metadata-only.
- `remedy candidate-quality show <evaluation_id> --json` — read-only.
- `remedy candidate-quality scorecard [--model|--route-tier|--job-id] --json` — read-only.
- `remedy candidate-quality report [--job-id] [--markdown] --json` — read-only.
- `remedy candidate-quality integrity --json` — read-only invariant check (no success-without-proof,
  no high score for rejected, no duplicate evaluation per fingerprint).

All `may_mutate_repo=false`, `may_execute_commands=false`. Contract actions
`candidate_quality_evaluate` (metadata) / `..._show|scorecard|report` (read-only), allowed by
default; distinct from any model/provider/apply/test action.

## Integrations

Progress Ledger / Feature Planner / Review Bundle (`candidate_quality_summary.json`, 26→27
sections) / Cockpit — safe counts/outcomes/IDs only; no buttons, no raw content. Every
next_safe_action is catalog + entity backed.

## Why this reduces wasted agent work

Instead of treating "verified" or "model said it's good" as done, Remedy learns which routes/models
actually produce **proof-verified** results and which keep failing — so future routing prefers
what works, avoids what doesn't, and escalates repeated failure to a human instead of looping.

## Next

- [Model/Route Tournament Harness v0](model-route-tournament-future.md) — controlled comparison of
  generators on the same request package + trust + verification + quality scoring.
- External Builder Sandbox v0 — bounded external generation, judged by the same pipeline + scorecards.
