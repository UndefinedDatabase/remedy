# Live Review — Steps 1681-1716: External Builder Sandbox v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: INGRESS sandbox for EXTERNAL builder candidates — safe request-package export, quarantined
external candidate submission, bridge into the EXISTING Trust Gate → Verification → Materialization
seams, candidate quality evaluation for external submissions, READ-ONLY routing feedback, safe
progress/review/cockpit summaries, docs/tests/integrity. Sandbox is INGRESS, NOT execution. Must NOT:
execute external providers, call Claude/Pi/OpenAI/Ollama, use network/browser/subprocess/MCP, auto
apply/approve/test/repair, automate git commit/branch/PR, or build a model/route tournament.
NO PR unless user asks (Step 1716).
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
FAIL (closure review @ `05710d0`) — directed closure audit (Steps 1707-1716) opened 3 findings:
R-0091 (LOW, redaction — raw_storage_ref in public CLI JSON), R-0092 (MEDIUM, idempotency — valid-package
blocked submissions not persisted as safe evidence), R-0094 (MEDIUM, routing-feedback — external route
recommends old `repair request` path, not the new external-builder rail). R-0093 (CLI stability) verified
PASS / refuted. Two open MEDIUM → per closure verdict rules merge-readiness is HELD until R-0091–R-0094
all resolved (zero open Medium/High/Blocker). NO safety-invariant violation: external candidate stays
untrusted, pending≠completed, rejected scores low, no provider/network/subprocess/apply/approve, no raw/
secret/diff/traceback content leak (raw_storage_ref = opaque quarantine_id duplicate, not content),
routing emits strings only. R-0091–R-0094 status table:
| ID | Sev | Status | Note |
|---|---|---|---|
| R-0091 | low | OPEN | raw_storage_ref emitted in public submission JSON (to_dict); remove from public export + test |
| R-0092 | medium | OPEN | valid-package blocked submissions not persisted as safe evidence; persist + test |
| R-0093 | low | RESOLVED | CLI suite 7 passed/2.29s; no hang/traceback/leak — refuted |
| R-0094 | medium | OPEN | external route next_safe_action = `repair request` (old); switch to `external-builder package-create` rail + test |

Targeted tests run: `tests/cli/test_external_builder_cli.py` = 7 passed (R-0093); prior full targeted
(external_builder_sandbox + candidate_quality + builder_routing + review_bundle + cockpit) = 172 passed.
Integrity: external_builder_integrity logic present + arch-guards green. Builder full suite 5969 passed/
8 skipped/1 deselected reported — NOT accepted as merge-evidence while R-0092/R-0094 open. Changed-files
table present in context.md. MERGE-READINESS: HELD (FAIL) pending R-0091/R-0092/R-0094. NO PR unless user asks.

---
(superseded) Prior safety pass — reviewed @ commit `05710d0`; ZERO open findings; all 14 checks PASS; all 10 negative cases
verified. External Builder Sandbox is INGRESS-ONLY ("Worker execute. Remedy governs."): Remedy never
executes an external worker, never calls provider/model/network/browser/subprocess/MCP/git, never
auto-applies/approves/tests. An external candidate FILE enters the EXISTING pipeline verbatim via
`intake_provider_repair(provider_name="external_builder:<label>", source_kind=FILE)` → quarantine →
Trust Gate → Verification → Materialization; the module NEVER reads/renders the raw candidate and
NEVER parses-to-intent — a pending intent (`PENDING_APPROVAL`) appears ONLY when the PTV gate sets
`repair_intent_id`. Intake pre-checks reject path-traversal (`..`), protected substrings (.env/.ssh/
.aws/.git/credentials/id_rsa/secrets/…), symlinks, non-regular files, oversized (>256KiB), unreadable
— all as safe structured errors (never raises). Request-package export carries safe context only
(failure IDs + scrubbed safe_summary labels; scrubbed objective; no raw source/diff/log/secret/path).
Candidate-quality reuse for external submissions adds model_label/route_tier LABELS only — scoring
path (`_classify`/`_score` evidence-only ceilings) is UNCHANGED, so rejected/unverified can't score
high and pending≠completed. Routing feedback (builder_routing step 9) is READ-ONLY — poor external
history → HUMAN_REVIEW_REQUIRED, never starts a worker/generation. Public surfaces = IDs/labels/
counts/states only (raw_storage_ref = quarantine pointer); `external_builder_integrity` actively flags
raw markers (diff --git/-----BEGIN/Traceback/sk-) + abs paths in public. run_contract
EXTERNAL_BUILDER_PACKAGE/SUBMIT/SHOW + all 8 catalog commands are write_metadata/read_only,
`may_execute_commands=False` (non-executable). All emitted next_safe_action catalog-valid (R-0088
lesson). REVIEWER-INDEPENDENT verification: targeted `scripts/remedy_pytest.sh`
(test_external_builder_sandbox + test_external_builder_cli + test_candidate_quality + test_builder_routing
+ test_review_bundle + test_dashboard_cockpit_truth) = **172 passed**; builder-reported full pytest
5969 passed/8 skipped/1 deselected (exit 0) — ACCEPTED per standing rule (targeted green, count clearly
reported, no hidden-failure evidence). Changed-files table present in `.agent/context.md`. Commit
reviewed: `05710d0`. Open findings: 0. MERGE-READY. NO PR unless user asks (Step 1716).
2 NITs (not findings): `save_job` imported but unused in external_builder_sandbox.py; traversal shares
the PROTECTED_PATH stop_reason with protected substrings (cosmetic).

## Check Matrix (1-14)
| Check | Status | Note |
|---|---|---|
| 1. Mainline closure (Candidate Quality v1 PASS respected; no scope before closure) | PASS | branch off 7cec21c (merged main); 0 drift commits |
| 2. Scope boundary (sandbox is ingress, not execution) | PASS | export package + submit file → intake; no worker exec; arch-guard tests |
| 3. Request package safety (safe context only; no raw/protected leaks) | PASS | _gather_safe_context = failure IDs + scrubbed labels; objective scrubbed; idempotent |
| 4. Storage/quarantine (raw/private separated from public summaries) | PASS | pkg/sub 0o600/dir 0o700; raw only via intake quarantine; public = IDs/labels |
| 5. Submission intake (bounded; protected; no traversal/symlink/binary unsafe) | PASS | _validate_candidate_path rejects ../protected/symlink/non-file/oversized/unreadable; binary via intake |
| 6. Trust/verification bridge (external candidate stays untrusted until verified) | PASS | intake_provider_repair FILE; intent only via PTV gate; PENDING_APPROVAL explicit |
| 7. Candidate Quality (evidence-only; ceilings preserved) | PASS | model_label/route_tier = labels only; _classify/_score unchanged |
| 8. Routing feedback (read-only confidence only; no auto generation) | PASS | builder_routing step 9 lower→HUMAN_REVIEW; never starts worker/generation |
| 9. Progress/Feature/Review/Cockpit (safe summaries; no fake live state) | PASS | fixed item_ids; bundle +external_builder_summary; cockpit counts/no buttons |
| 10. CLI/catalog/run contract (catalog-valid; non-executable classifications) | PASS | 8 commands write_metadata/read_only; may_execute_commands=False; non-cloud actions |
| 11. Redaction (no raw/secret/path/log/diff/traceback public) | PASS | public = IDs/labels/states; integrity flags raw markers + abs paths; test_public_surfaces_never_expose |
| 12. Architecture guards (no forbidden imports/calls) | PASS | stdlib + scrub helpers; test_no_forbidden_imports + test_no_execution_or_apply |
| 13. Tests (targeted + full suite reported) | PASS | reviewer targeted = 172 passed; builder full 5969 passed/8 skipped/1 deselected (accepted) |
| 14. Handoff (changed-files table, risks, non-goals, next block) | PASS | changed-files table in context.md; non-goals + risks documented |

## Negative-test checklist (reviewer must verify)
| # | Case | Status |
|---|---|---|
| 1 | Candidate fake "tests passed" claim → no proof promotion | PASS | candidate_quality scoring uses durable test_state/proof_chain, not candidate text (scoring path unchanged); test_external_evaluation + candidate_quality suite |
| 2 | Candidate secret-looking token → not public | PASS | test_secret_candidate_trust_rejected_no_echo + test_public_surfaces_never_expose (sk-/BEGIN) |
| 3 | Candidate absolute path → not public | PASS | test_public_surfaces_never_expose (/home//Users/ forbidden); integrity abs-path check |
| 4 | Candidate `diff --git` → not public | PASS | test_public_surfaces_never_expose payload "diff --git a/x b/x" absent from public |
| 5 | Candidate oversized → rejected safely | PASS | test_oversized_rejected + CLI test_submit_oversized → OVERSIZED, no raise |
| 6 | Candidate symlink / path traversal / protected path → rejected safely | PASS | test_symlink_rejected + test_protected_path_rejected; _validate_candidate_path `..`+protected branch |
| 7 | Rejected candidate → low score / no intent | PASS | trust-rejected → no intent (test_secret_candidate...); candidate_quality rejected→LOW |
| 8 | Pending approval → not completed | PASS | PENDING_APPROVAL state explicit; candidate_quality pending→MEDIUM "not complete" |
| 9 | Routing poor history → human-review recommendation only | PASS | builder_routing step 9 lower→HUMAN_REVIEW (test_builder_routing) |
| 10 | Routing recommendation creates/runs/generates nothing | PASS | route_quality_feedback read-only; test_no_execution_or_apply + test_no_forbidden_imports |

## Findings — Steps 1681-1716

NOTE: initial safety pass @ `05710d0` was clean (10/10 negative cases, 172 passed). A directed CLOSURE
review (Steps 1707-1716) surfaced 3 completeness/hygiene findings below — none are safety-invariant
violations, but R-0092/R-0094 are MEDIUM and gate the closure PASS. Verdict downgraded to FAIL until
resolved.

## Finding R-0091
Status: Open
Severity: low
Area: redaction
Summary: `raw_storage_ref` (a field documented "private; never rendered") is emitted in the public CLI submission JSON.
Details: `ExternalBuilderCandidateSubmission.to_dict()` (external_builder_sandbox.py:177) includes
`"raw_storage_ref"`, and `export_external_submission_json` == `to_dict`, so `remedy external-builder
submit/submission-show --json` (external_builder_cmd.py:80) prints it. The field is annotated
":155 quarantine id — private; never rendered", AND `external_builder_integrity` (:538) DELIBERATELY
excludes `raw_storage_ref` from its raw-marker leak scan — so the code itself treats it as private,
yet `to_dict` exposes it. NOT a raw/secret/content leak: the value is the quarantine_id (an opaque id
already public via the separate `quarantine_id` field), so no NEW sensitive data escapes — hence LOW.
But it violates the field's own contract + the integrity-scanner intent.
Evidence: external_builder_sandbox.py:155 (comment), :177 (to_dict emits it), :538 (integrity excludes
it); external_builder_cmd.py:80 prints export_external_submission_json.
Expected fix: Drop `raw_storage_ref` from `to_dict`/`export_external_submission_json` (keep it as an
in-memory/private field only; `quarantine_id` already carries the public pointer), add a CLI/bundle/
cockpit test asserting `raw_storage_ref` absent from public JSON. Then write `Done: R-0091`.

## Finding R-0092
Status: Open
Severity: medium
Area: idempotency
Summary: Valid-package BLOCKED submissions are not persisted as safe evidence (ephemeral return).
Details: `_blocked_submission` (external_builder_sandbox.py:415) builds a BLOCKED submission but never
`_atomic_write`s it; `submit_external_candidate` returns it directly at :457/:466/:470/:476
(package-not-found, job-not-found, contract-denied, path-validation-failure incl. oversized/symlink/
protected/unreadable). Only the successful path persists (`_atomic_write(_sub_path…)` :507). So a
rejected external candidate against a VALID package leaves NO durable record — `load_external_submissions`
/ progress / review-bundle never see it; an attacker repeatedly submitting protected/oversized files
produces no audit trail. SAFETY is intact (state=BLOCKED, never success/pending), so this is not a
blocker — but the evidence/audit rail is incomplete (this is the block's own ingress-evidence purpose).
Evidence: external_builder_sandbox.py:415 (_blocked_submission, no write), :457/:466/:470/:476 (return
without persist), :507 (only success persists).
Expected fix: Persist BLOCKED submissions as safe evidence when the job+package are valid (oversized/
symlink/protected/contract-denied) under `_sub_path` with state=BLOCKED + safe stop_reason only; keep
invalid-package/job-not-found ephemeral (nowhere to persist) and document that behavior. Add a test:
oversized/symlink submission against a valid package → persisted, state=BLOCKED, public surface shows
only the stop_reason. Then write `Done: R-0092`.

## Finding R-0093
Status: Resolved (verified — not a defect)
Severity: low
Area: cli-runtime
Summary: External-builder CLI suite stability.
Resolution: Reviewer ran `scripts/remedy_pytest.sh tests/cli/test_external_builder_cli.py -q` =
**7 passed in 2.29s** — suite completes, no hang, JSON parses, no tracebacks, no raw candidate content
in output. Stability concern refuted. (Note: the suite does NOT assert `raw_storage_ref` absent — that
hygiene gap is tracked under R-0091, not here.)

## Finding R-0094
Status: Open
Severity: medium
Area: routing-feedback
Summary: Builder Routing's external route recommends the OLD `repair request` path, not the new External Builder rail.
Details: In `select_builder_routing_decision` step 9 (builder_routing.py ~:722), the
EXTERNAL_CANDIDATE_GENERATOR route emits `_prepare_request_cmd(request)` → `remedy repair request
{job_id} --json`. That is a valid catalog command (so NOT a fake-action/R-0088-class defect), but it
points at the older repair-request packaging path rather than this block's new external-builder rail
(`remedy external-builder package-create …`). The local route was updated to `local-candidate generate`
in the prior block; the external route was not updated to the external-builder rail. Result: the user
following the routing recommendation lands on the confusing old path instead of the rail this block
exists to provide. Read-only/no-auto-generation is intact (string only); this is a UX/architecture
correctness gap, not a safety violation.
Evidence: builder_routing.py:722 `_finalize(d, EXTERNAL_CANDIDATE_GENERATOR, …, _prepare_request_cmd(request), …)`;
`_prepare_request_cmd` returns `remedy repair request …`; new rail command `external-builder.package-create`
exists in the catalog but is never recommended by routing.
Expected fix: Emit a catalog-valid external-builder next action (e.g. `remedy external-builder
package-create --job-id {job_id} [--route-id {routing_id}] --json`) for the external route; keep it a
recommendation STRING only (no auto generation). Add a builder_routing test asserting the external
route's next_safe_action targets the external-builder rail and parses via build_parser. Then write
`Done: R-0094`.

Next id: R-0095.

## Reviewer audit log
- PR #67 merged Candidate Quality Evaluation v1 (1645-1680) to main → `7cec21c`; reviewer verdict
  PASS @ `7729b89`. New branch `feature/steps-1681-1716-external-builder-sandbox-v0` off `7cec21c`
  (clean merged main). `git log main..HEAD` empty → no drift, no block code yet. Check 1 PASS.
- WATCH: sandbox is INGRESS only — external candidate text is UNTRUSTED and must flow through the
  EXISTING quarantine → Trust Gate → Verification → Materialization pipeline (no direct parse-to-
  intent, no pre-trust materialization, no trusting external candidate). Quality eval must reuse the
  evidence-only ceilings (no model confidence / self-claim / "tests passed" / raw text). Routing
  feedback read-only (no auto generation / no worker exec). Intake must reject traversal/symlink/
  protected/binary/oversized safely. NO provider/network/subprocess/browser/MCP/git/apply/approve/
  test/PR. Public surfaces = codes/IDs/counts only. Idempotent. next actions catalog-valid (R-0088).

## Builder remediation — audit findings R-0091..R-0094 (awaiting reviewer re-check @ new HEAD)
Done: R-0091 - raw_storage_ref removed from ExternalBuilderCandidateSubmission.to_dict (public export + persisted record); kept in-memory only; equals quarantine_id which stays public. Test: test_public_export_has_no_raw_storage_ref.
Done: R-0092 - blocked submissions (oversized/protected/symlink/traversal/contract-denied) now persisted as evidence-backed BLOCKED records when package+job valid (no raw candidate stored); missing/invalid package stays ephemeral (documented). Tests: test_blocked_submission_persisted, test_protected_blocked_persisted, test_missing_package_block_ephemeral.
Done: R-0093 - external builder CLI suite verified isolated `scripts/remedy_pytest.sh tests/cli/test_external_builder_cli.py -vv -s` = 7 passed in 2.29s; no hang; no traceback in safe error JSON.
Done: R-0094 - builder_routing external route next_safe_action now emits `remedy external-builder package-create <job> --route-id <route> --json` (catalog-valid), not the old repair-request rail; poor history still HUMAN_REVIEW, unknown neutral, pending not success. Test: test_external_route_with_known_cost (parser-validated).

Builder verification: targeted external sandbox/routing/quality = 78 passed; CLI 7 passed; review_bundle/cockpit/catalog/run_contract/progress/feature = 261 passed; integrity passed=True/fail=0. Full pytest pending (one run). NOT claiming merge-ready — reviewer owns verdict at new HEAD.
