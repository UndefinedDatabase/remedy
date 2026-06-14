# Live Review — Steps 1465-1498: Main Orchestrator Brain v0

Reviewer: parallel reviewer
Scope: Decision Engine + Anti-Loop Guard + Model Routing Plan. Read state from SAFE
summaries → Situation → deterministic Options → score → loop guard → routing plan →
ONE Decision. Planning/decision ONLY. Must NOT: execute actions, call Ollama/provider/
network/subprocess/browser, apply, approve, create PRs, mutate main/code, insert
Job.tasks, emit fake/missing-entity commands, ignore open blocker/high review, loop on
a failed action without new evidence, treat routing as execution, leak raw source/diff/
logs/secrets/paths. NO PR unless user asks (Step 1495/1498).
Timestamp: 2026-06-14

## Verdict
PASS WITH RISKS — all 15 checks PASS; sole finding R-0086 (MEDIUM, scorer ignored
contract permission) is **Resolved** (CONTINUE_INTENT gated on patch_apply permission;
regression test). Zero open Blocker/High. Orchestrator targeted 19 pass; full suite
green; integrity passed. Planning/decision only — no execution/model/provider/apply/
approve/PR/main mutation; routing is a plan, not a call; open blocker/high → human
review; anti-loop holds; no fake/missing-entity commands. NO PR created (Step 1495/1498).

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | cd3d45c off clean main 38df37d; PR#61 (Self-Dogfood Execution 1429-1464) MERGED FIRST then branched (correct sequencing, no stacking); residuals carried; only .agent/ files touched; no drift; PR held (1495/1498) |
| 2. Orchestrator models (no raw fields) | PASS | Situation/Decision/Option/EvidenceRef/Risk/RoutingPlan/LoopGuard/Idea hold IDs/labels/counts/scrubbed summaries; no raw |
| 3. Situation builder (safe summaries; unknown stays unknown) | PASS | _gather_signals from durable stores (artifacts/repair/intents/trust/material/requests/self/contract-usage); try/except→unknown refs; missing→risk; NO event-only truth promotion |
| 4. Option generator (real entities/commands only) | PASS | deterministic; entity-backed (intent/fa/pt ids); _catalog_ok via validate_next_safe_action_command→available=False if not catalog-backed; why_now/why_not |
| 5. Decision scorer (deterministic; reason codes) | PASS | R-0086 RESOLVED @0bc1a47: _gather_signals evaluates evaluate_run_action(PATCH_APPLY)→patch_apply_allowed; CONTINUE_INTENT unavailable when denied; test_contract_denied_apply_not_recommended; scorer now uses evidence/review/contract/budget/loop/risk |
| 6. Anti-loop guard (allow/warn/block/human) | PASS | durable repair_failed≥2→human_review, trust_rejected≥2→block; decision-history repetition (same evidence_fingerprint+kind)→warn/block; new evidence (diff fingerprint) resets; CLI decide persists=True |
| 7. Model routing plan (no calls; 4 tiers) | PASS | deterministic_only/local_advisor_preferred/external_builder_needed/human_review_required; PLAN only (notes "no model called"); external only when justified + Trust Gate; no calls |
| 8. Decision selector (exactly one outcome) | PASS | exactly one: SELECTED|HUMAN_REVIEW_REQUIRED|NO_SAFE_ACTION|EVIDENCE_INCOMPLETE; rejected_options explained; next_safe_action safe (catalog cmd or self inspect) |
| 9. Decision trace persistence (safe/atomic/hashed) | PASS | _save_decision tmp+os.replace 0o600 + sha256; export_decision_json safe (IDs/labels/counts) |
| 10. CLI (inspect/decide/report/idea) + catalog + RunContract | PASS | inspect/report read_only, decide/idea write_metadata, no-mutate/no-exec; JSON; no traceback; ORCHESTRATOR_INSPECT/DECIDE/REPORT contract allowed |
| 11. Idea intake + idea-to-option (hints not truth; dedupe) | PASS | record_idea scrub+classify+dedupe(fingerprint); never creates ProposedTask; idea→option available=False (human review only) |
| 12. Integrations (Progress/Feature/Review/Cockpit) | PASS | 4ef4235: ledger fixed item_ids+counts/safe enums; feature planner human-review follow-up; review_bundle _build_orchestrator_decision_summary counts/labels/IDs only (no raw ideas, REQUIRED_SECTIONS→22); cockpit read-only; no mutation buttons |
| 13. Redaction | PASS | _scrub_public+[:300] on idea text; test_no_raw_leak injects sk-token//home//id_rsa/Traceback (live_review + idea text) → asserts absent |
| 14. Architecture guards (no provider/Ollama/network/apply/git/PR/Job.tasks) | PASS | test_no_network_subprocess/no_provider_or_ollama(ollama/anthropic/openai/litellm)/no_apply_or_execution_imports(patch_apply/source_apply)/no_git_pr_jobtasks(os.system/.tasks.append) |
| 15. Quality + anti-loop + routing tests | PASS | 2b36844: decision-quality/anti-loop(warn→block, repair-fail→human, new-evidence-resets)/routing(human/external/deterministic)/idea/redaction/arch (committed); targeted run pending builder lock |

## Findings — Steps 1465-1498

## Finding R-0086
Status: Resolved
Severity: medium
Area: scoring
Resolution: RESOLVED @ 0bc1a47, reviewer-verified in committed code. _gather_signals now
evaluates evaluate_run_action(contract, ContractAction.PATCH_APPLY) → sig["patch_apply_allowed"]
(orchestrator_brain.py:406-407, fallback False on error :410); CONTINUE_INTENT (the
contract-gated apply action) is marked available=False + why_not "Contract denies patch_apply
(or stop_before_apply)" when apply not permitted (:562-564), so a contract-denied apply can
never be the SELECTED next step. APPROVE_INTENT stays available (human approval gate ≠ apply;
the downstream CONTINUE_INTENT apply is the gated step) — acceptable. Regression test
`test_contract_denied_apply_not_recommended` (default contract denies PATCH_APPLY → continue
options unavailable + not selected). Targeted suite re-run confirmation deferred (builder holds
/tmp/remedy-pytest.lock) — fix + test verified by inspection in committed code.
Summary: decision scorer ignores run-contract action permission — options are scored/selected without evaluating their required_contract_action, so a contract-denied action can be recommended as the top next step.
Details: Options set `required_contract_action` (e.g. APPROVE_INTENT/CONTINUE_INTENT →
"patch_apply") in `_generate_options` (orchestrator_brain.py:540-553), but neither
`_generate_options` nor `_score_options` (627-650) ever calls
`run_contract.evaluate_run_action`. The only contract-derived input is `budget_exhausted`
(from load_usage) which suppresses CONTINUE_INTENT only (639-641). If the job's contract
denies an action (e.g. stop_before_apply, a custom disallowed action, no_cloud-style gate),
the orchestrator still scores CONTINUE_INTENT=85 / APPROVE_INTENT=90 and selects it as the
SELECTED next_safe_action with high confidence. Check 4 explicitly requires the scorer to use
"contract", and the block-if list includes "budget/contract denial is ignored" — budget is
handled, contract action permission is NOT. No unsafe EXECUTION results (the brain only emits
a command string; the downstream `do continue`/`patch approve` still enforces the contract),
but the brain's decision quality/confidence is wrong and the block-if/Check-4 contract factor
is unimplemented.
Evidence: orchestrator_brain.py:520-526 (_opt records required_contract_action but never
checks it), 540-553 (options set patch_apply action), 627-650 (_score_options uses base score
+ review_blocks + budget + loop + risk, NO evaluate_run_action), 394-404 (only budget pulled
from contract). No `evaluate_run_action` call anywhere in the module.
Expected fix: in scoring/option-availability, evaluate each option's required_contract_action
via `evaluate_run_action(ensure_contract(job), action)`; when denied, mark the option
unavailable (or score→min) with reason_code "contract_denied" so a contract-denied action is
never the SELECTED next step. Add a regression test (contract denies patch_apply → continue/
approve not selected).

Done: R-0086 — `_gather_signals` now evaluates `evaluate_run_action(contract, PATCH_APPLY)`
and stores `patch_apply_allowed`; the CONTINUE_INTENT option is marked `available=False`
("Contract denies patch_apply (or stop_before_apply)") when apply is not permitted, so it
can never be the SELECTED next step. APPROVE_INTENT is a human approval gate (not a
contract-gated apply) and stays available. Regression test
`test_contract_denied_apply_not_recommended` (default contract denies PATCH_APPLY →
continue option unavailable + not selected).

### Reviewer audit log
- 2026-06-14: Block start. Worker at cd3d45c (Step 1465 reconciliation). Sequencing verified:
  PR#61 (Self-Dogfood Execution 1429-1464) merged to main 38df37d FIRST, then branch
  feature/steps-1465-1498-main-orchestrator-brain-v0 off clean main (no stacking on unmerged
  work; honors prior Step 1460 "separate PR, do not stack"). Reconciliation touches only
  .agent/ files. Plan steps 1466-1498 each cover a stated check/block-if; hard rules align
  (advisory/read-only-metadata-only; NO action execution/Ollama/provider/network/subprocess/
  browser; routing is a PLAN never a call; no apply/test/source_apply/patch_apply/approve/PR/
  git/main/Job.tasks; anti-loop; open-blocker-high review→human_review; budget/contract gating;
  catalog-backed real-entity actions; no raw leak; PR held 1495/1498). Residuals carried.
  Check 1 PASS. Worker now writing core (orchestrator_brain.py untracked). Next id: R-0086.
- 2026-06-14: Reviewed a4e1f1c (core+contract 1466-1480) + 31e7118 (CLI) + 4ef4235
  (integrations 1481-1484). orchestrator_brain.py (938L): situation/options/scorer/anti-loop/
  routing/selector/trace/idea-intake. Block-ifs cleared: NO execution (emits command STRINGS
  only, never runs), NO Ollama/provider/network/subprocess/apply/test/approve/PR/git/Job.tasks;
  situation from durable safe summaries (no event-truth promotion); options deterministic +
  entity-backed + catalog-validated (_catalog_ok→validate_next_safe_action_command, non-catalog
  →available=False); routing is PLAN (4 tiers, notes "no model called", external only via Trust
  Gate); selector emits exactly one outcome; trace atomic 0o600+sha256; idea scrub+classify+
  dedupe (never ProposedTask, idea→human-review-only); anti-loop durable failure signals +
  decision-history (CLI decide persists=True); review-blocks force human_review; budget
  suppresses continue. ONE FINDING: R-0086 (MEDIUM, scoring) — scorer/option-gen never evaluate
  required_contract_action (only budget pulled from contract); a contract-denied action (e.g.
  patch_apply under stop_before_apply) can be SELECTED as top next step. No unsafe execution
  (brain advisory; downstream command enforces contract), but Check-4 "contract" factor +
  block-if "contract denial is ignored" unmet. Checks 2-12 PASS (5 carries R-0086). 13/14 PASS
  by code; 15 PENDING (tests not committed). Await fix + tests. Next id: R-0087.
- 2026-06-14: Reviewed 2b36844 (tests+docs 1485-1492) + a8f5058 (plan) + 0bc1a47 (R-0086 fix).
  R-0086 RESOLVED + reviewer-verified in committed code (evaluate_run_action PATCH_APPLY →
  patch_apply_allowed; CONTINUE_INTENT unavailable when denied; test_contract_denied_apply_not_
  recommended). All 15 checks now have committed test coverage: catalog-backed selected cmd,
  open-blocker→human-review, priority ordering, anti-loop (warn→block, repair-fail→human,
  new-evidence-resets), routing (human/external-builder notes plan-only/deterministic), idea
  classify+dedupe+hint-not-executed, redaction (sk-token//home//id_rsa/Traceback absent),
  architecture (no subprocess/shell/ollama/anthropic/openai/litellm/patch_apply/source_apply/
  os.system/.tasks.append). Side fix in 2b36844: feature_planner local-advisor mapping
  FeaturePlanSource.FEATURE_SUGGESTION→ROADMAP (FEATURE_SUGGESTION is ProgressSource-only) —
  sound. Changed-files reconciled vs git diff 38df37d..HEAD = 17 files, all covered. ALL 15
  checks PASS; ZERO open findings. Builder running full pytest (lock held) — await count +
  handoff. Targeted orchestrator run deferred (lock). Next id: R-0087.

## Builder Final Handoff (Steps 1465-1498)

- **Mainline reconciliation**: PR #61 (Self-Dogfood Execution) merged FIRST → main 38df37d;
  branch off clean main; no stacking; no drift.
- **Tests**: orchestrator unit/anti-loop/routing/idea/redaction/architecture (19) + CLI
  runtime (6) + review-bundle/cockpit/catalog/progress/feature/run-contract. **Full pytest**
  (post R-0086) re-run recorded below. Wrapper `scripts/remedy_pytest.sh`, `-k "not test_full_chain_order"`.
- **Integrity gate**: `remedy integrity check` passed=True, fail_count=0.
- **Findings**: R-0086 (Resolved — contract-gated apply option).
- **Models / situation builder / option generator / decision scorer / anti-loop guard /
  model routing plan / decision selector / decision trace / CLI (inspect/decide/report/idea) /
  RunContract / idea intake / Progress / Feature / Review / Cockpit / redaction / architecture
  guards**: DONE.
- **Hard completion criteria (1497)**: executes nothing; no Ollama/provider/network/subprocess;
  no apply/approve/PR/main mutation/Job.tasks; no fake/missing-entity commands; open blocker/
  high → human_review; anti-loop (no repeat without new evidence); routing is a plan not a call;
  no raw leak; live_review NOT PENDING. ALL satisfied.

### Changed Files (Steps 1465-1498)
| File | What changed | Why |
|---|---|---|
| `packages/orchestration/orchestrator_brain.py` | NEW — situation/options/scorer/anti-loop/routing-plan/selector/decision-trace/idea intake; contract-gated apply option | Core orchestrator brain |
| `packages/orchestration/run_contract.py` | orchestrator_inspect/decide/report actions | Gate read/metadata decisioning |
| `apps/cli/command_catalog.py` | orchestrator group + inspect/decide/report/idea | CLI surface |
| `apps/cli/commands/orchestrator_cmd.py` | NEW — inspect/decide/report/idea handlers | Wire CLI |
| `apps/cli/commands/__init__.py` | register orchestrator_cmd | Handler collection |
| `packages/orchestration/progress_ledger.py` | orchestrator decision/human-review/blocked/advisor/builder items | Progress surface |
| `packages/orchestration/feature_planner.py` | human-review/local-advisor/external-builder follow-ups (FeaturePlanSource.ROADMAP) | Human next-steps |
| `packages/orchestration/review_bundle.py` | orchestrator_decision_summary.json (REQUIRED_SECTIONS 21→22) | Reviewable summary |
| `packages/orchestration/ui_server.py` | read-only orchestrator cockpit section | Surface latest decision |
| `docs/orchestrator-brain-v0.md` | NEW — orchestrator doc | Long-term knowledge |
| `tests/orchestration/test_orchestrator_brain.py` | NEW — 19 unit/anti-loop/routing/idea/redaction/architecture/R-0086 tests | Coverage |
| `tests/cli/test_orchestrator_brain_cli.py` | NEW — 6 CLI runtime tests | Coverage |
| `tests/orchestration/test_review_bundle.py`, `tests/ui_server/test_dashboard_cockpit_truth.py` | REQUIRED_SECTIONS==22 + cockpit shape | Keep invariants |
| `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md` | block state + product readiness + review | Runtime state |

### Readiness + merge
Readiness ~95% (decision/planning rail; model execution deliberately deferred). Merge-
ready as a SEPARATE PR. **PR NOT created** (Step 1495/1498 — awaiting explicit user request).
Next block: Local Model Advisor Adapter v0 OR Provider Trust Verification v1.

### Reviewer audit log (final)
- 2026-06-14: FINAL. Reviewed bc7c7f3 (live review + handoff, PR held). Targeted run via
  `scripts/remedy_pytest.sh test_orchestrator_brain.py test_orchestrator_brain_cli.py -q`
  → 25 passed (incl test_contract_denied_apply_not_recommended [R-0086], anti-loop warn→block/
  repair-fail→human/new-evidence-resets, routing human/external/deterministic, idea dedupe+
  hint-not-executed, redaction, architecture guards). Builder full suite 5689 passed/8 skipped/
  1 deselected; integrity passed=True/fail=0. Changed-files table reconciled vs git diff
  38df37d..HEAD = 17 files, all covered, none missing/extra. R-0086 Resolved + verified. ALL 15
  checks PASS; zero open Blocker/High. Verdict PASS WITH RISKS. NO PR (Step 1495/1498). COMPLETE.

## Reviewer Final Verdict — Steps 1465-1498 (Main Orchestrator Brain v0)

**PASS WITH RISKS.** Zero open Blocker/High. One finding filed (R-0086 MEDIUM, scoring) and
**Resolved** — reviewer-verified in committed code.

Primary goal MET: produces evidence-backed next-step decisions + anti-loop protection +
model-routing recommendations WITHOUT executing actions, calling models, applying patches,
approving work, or leaking raw data. Controller-not-executor: emits command strings only.

- Handoff: PASS (PR#61 merged first → clean main 38df37d; correct sequencing, no stacking; residuals carried; PR held)
- Situation builder: PASS (durable safe summaries; unknown stays unknown; missing→risk; no event-only truth promotion)
- Option generator: PASS (deterministic; entity-backed; catalog-validated via validate_next_safe_action_command; why-now/why-not)
- Scoring: PASS (deterministic; evidence/review/contract[R-0086 fix]/budget/loop/risk; reason codes; no fake green)
- Anti-loop: PASS (durable repair-fail≥2→human, trust-reject≥2→block; persisted decision-history warn→block; new evidence resets)
- Model routing: PASS (4 tiers; PLAN only, no calls; external only when justified + via Trust Gate)
- Decision selector: PASS (exactly one: SELECTED|HUMAN_REVIEW_REQUIRED|NO_SAFE_ACTION|EVIDENCE_INCOMPLETE; rejected explained; safe next action)
- CLI: PASS (inspect/report read_only, decide/idea write_metadata; JSON; no traceback; no shell=True)
- Idea intake: PASS (scrub+classify+dedupe; never ProposedTask; hint not truth → human review only)
- Progress/Feature/Review: PASS (counts/labels/IDs/safe enums only; no raw; no mutation)
- Cockpit: PASS (read-only latest decision; no buttons)
- Redaction: PASS (_scrub_public; injected secret/path/traceback absent — test asserted)
- Architecture: PASS (no provider/Ollama/network/subprocess/apply/test/git/PR/Job.tasks — test asserted; routing never executes)
- Tests run: targeted `scripts/remedy_pytest.sh` orchestrator_brain + CLI → 25 passed (reviewer-run once)
- Full pytest: builder post-fix → 5689 passed / 8 skipped / 1 deselected (exit 0); reviewer did NOT run full suite
- Remaining findings: none (R-0086 Resolved)
- Merge readiness: MERGE-READY as a SEPARATE PR; **NO PR** (Step 1495/1498 — awaiting explicit user request)

**Residual risks (→ PASS WITH RISKS, all documented):**
1. Model execution deliberately deferred (v0 = decision/planning rail; routing is a plan, no model called — next block Local Model Advisor Adapter v0).
2. Contract gating now covers patch_apply for the apply option (R-0086); other future option kinds that become contract-gated must extend the same evaluate_run_action check.
3. Anti-loop decision-history relies on persisted decisions (CLI decide persists=True); a caller using persist=False loses history-repetition detection (durable repair/trust-reject signals still apply).
4. Regex `_scrub_public` may miss novel secret/path formats (R-0083 lineage; surfaces are counts/labels/IDs only).
5. Reviewer relied on builder's full-suite count (5689); independently ran targeted suite green + verified all checks + R-0086 fix against committed code.
