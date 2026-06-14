# Live Review — Steps 1399-1428: Self-Dogfood Readiness + Self-Improvement Planner v0

Reviewer: parallel reviewer
Scope: Remedy inspects its OWN evidence (reports/findings/risks/failed tests/stale
handoff/missing evidence) → SelfImprovementItems → Plan → ProposedTasks via the
EXISTING approval flow. Must NOT: edit code, apply, approve, insert Job.tasks directly,
create PRs, do git ops, mutate main, run scheduled/background; call provider/network/
subprocess/browser; read raw source/logs/diffs; leak findings/secrets/paths; ignore
PENDING/FAIL/open blocker-high; duplicate ProposedTasks for same item.
Timestamp: 2026-06-14

## Verdict
PASS WITH RISKS — all 15 checks reviewed PASS in the audit log; ZERO findings, zero
open Blocker/High. Full suite green (5662 passed, 8 skipped, 1 deselected); integrity
passed (0 fail). Read-only inspect/plan/report + metadata-only propose (ProposedTask
via existing flow); no self-apply/approve/PR/git/Job.tasks/provider/network; idempotent
by fingerprint; PENDING/FAIL/open-blocker-high → self-improvement blocker.

## Check Matrix (1-15) — to fill
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation | PASS | f1495c3 off clean main ce18aeb; PR#59 recorded; residuals carried; only .agent/ files touched; no drift |
| 2. Self-dogfood models (no raw fields) | PASS | dataclasses hold IDs/types/priority/scrubbed title+detail; evidence ref=IDs/module names; no raw fields |
| 3. Evidence source registry (available/missing/malformed/stale) | PASS | _read_agent_file → available/missing/malformed; job available/missing; sources_checked names+status only |
| 4. Live review parser reuse (PENDING/FAIL/blocker→blocker) | PASS | reuses overnight_executor.parse_review_findings; verdict pending/fail→blocker+SAFETY_GAP blocker item; open_blocker_or_high>0→blocker; unavailable/malformed→evidence_gap |
| 5. Stale handoff detector | PASS | deterministic regex on plan.md Current Step + open [ ] count + live_review changed-files/test-count presence |
| 6. Evidence gap detector | PASS | deterministic from job repair attempts (failure w/o repair, attempt w/o intent) + provider trust accepted-not-materialized; try/except guarded |
| 7. Quality debt detector (registries only; no code scan) | PASS | docs existence only; NO arbitrary source scan |
| 8. Roadmap detector (deterministic; cites evidence) | PASS | module-existence rules only; cites module file; LOW roadmap items (names scope-blocker topics only as future suggestions, does NOT add them) |
| 9. Item classification + plan builder (dedupe fingerprint; top 3) | PASS | fingerprint sha256(type:key)[:12]; dedup by fingerprint; sort by priority; plan groups by type, recommended[:3] |
| 10. CLI (inspect/plan/propose/report) + catalog + RunContract | PASS | inspect/plan/report read_only, propose write_metadata; JSON via export; errs→stderr no traceback; SELF_INSPECT/PLAN/PROPOSE_TASK allowed (not cloud); denial→contract_blocked; 7 referenced cmds all in catalog |
| 11. ProposedTask integration (origin self_dogfood; existing flow; idempotent) | PASS | add_proposed_task (NOT Job.tasks); task_type=self_dogfood; origin_recommendation_id=self_dogfood:<fp>; dedup vs existing_recs; ambiguous(>1 high)→require --item-id/--top; no approval/exec |
| 12. Integrations (Progress/Feature/Review/Cockpit) | PASS | e589959+9fc5b0c: ledger fixed item_ids+de-dup (status .value normalized); feature planner decision-list (no auto exec); review_bundle counts/IDs only (19→20, no .agent re-scan); cockpit read-only counts, no buttons |
| 13. Redaction | PASS (code) | _scrub_public+[:300] on title/detail; bundle/cockpit emit counts+IDs only; await committed redaction test |
| 14. Architecture guards (no apply/test/provider/git/Job.tasks/PR) | PASS (code) | imports stdlib+internal only; no subprocess/network/provider/git/apply/test/Job.tasks; await committed guard test |
| 15. Idempotency | PASS (code) | deterministic fingerprints + propose dedup by origin_recommendation_id; await committed idempotency test |

## Findings — Steps 1399-1428
(none yet)

### Reviewer audit log
- 2026-06-14: Block start. Worker at f1495c3 (Step 1399 reconciliation). Branch off clean
  main ce18aeb (PR#59 merged Repair Request Builder v0). Reconciliation touches only .agent/
  files (context/plan/live_review). Plan steps 1400-1428 each cover a stated check/block-if;
  hard rules align (read-only/metadata-only, ProposedTask flow not Job.tasks, no self-apply/
  approve/PR/git, fingerprint dedup, PENDING/FAIL/open-blocker-high→BLOCKER, no raw scan).
  Residuals carried. Check 1 PASS. Worker now writing core (self_dogfood.py untracked;
  command_catalog.py + run_contract.py modified, uncommitted) — await commit to review.
  Next finding id: R-0084.
- 2026-06-14: Reviewed 7a07335 (core+CLI+contract 1400-1419) + e589959 (integrations
  1415-1418) + 9fc5b0c (enum .value status fix). self_dogfood.py (683L): models, source
  registry, detectors (review/stale-handoff/evidence-gap/roadmap/quality-debt — all
  deterministic), fingerprint dedup, plan(top3), metadata-only propose. ZERO findings.
  Verified deps exist: ProposedTask.task_type+origin_recommendation_id fields, ORCHESTRATOR
  enum, add_proposed_task/load_proposed_tasks_safe signatures; ReviewFindings.verdict/source/
  open_blocker_or_high (reuses trusted executor parser); contract SELF_INSPECT/PLAN/
  PROPOSE_TASK default-allowed not cloud; all 7 referenced next-actions in catalog
  (self.inspect/plan/propose, decision.list, contract.inspect, job.list, repair.propose).
  Block-ifs cleared: propose uses add_proposed_task NOT Job.tasks; no approval/apply/exec/git/
  PR/subprocess/network/provider; idempotent by origin_recommendation_id=self_dogfood:<fp>;
  PENDING/FAIL/open-blocker-high→BLOCKER; deterministic detectors (no arbitrary code scan);
  roadmap names scope-blocker topics only as LOW future suggestions (does not add them);
  all free-text scrubbed via _scrub_public; bundle/cockpit counts+IDs only (no raw, no .agent
  re-scan, no mutation buttons). Enum-fix 9fc5b0c corrects ledger/cockpit pending count
  (str(enum) → .value lowercased). Checks 2-12 PASS in committed code. Checks 13/14/15 PASS
  by code inspection; await committed redaction/architecture/idempotency tests (untracked:
  test_self_dogfood.py, docs/self-dogfood-v0.md). Await full pytest + handoff before verdict.

## Builder Final Handoff (Steps 1399-1428)

- **Mainline reconciliation**: PR #59 merged; branch off clean main ce18aeb; no drift.
- **Tests**: targeted self_dogfood unit/idempotency/redaction/architecture (19) + CLI
  runtime (7) + review-bundle/cockpit/catalog/progress/feature/run-contract/proposed-tasks.
  **Full pytest** → **5662 passed, 8 skipped, 1 deselected** (exit 0). Wrapper
  `scripts/remedy_pytest.sh`, `-k "not test_full_chain_order"`.
- **Integrity gate**: `remedy integrity check` passed=True, fail_count=0.
- **Findings**: none.
- **Models / source registry / live-review reuse / stale-handoff / evidence-gap /
  quality-debt / roadmap / classification / plan builder / CLI (inspect/plan/propose/
  report) / catalog / RunContract / ProposedTask integration / Progress / Feature /
  Review / Cockpit / report / redaction / architecture guards / idempotency**: DONE.
- **Hard completion criteria (1428)**: does not edit code/apply/approve; no direct
  Job.tasks insertion (uses add_proposed_task); no PR/git; reads only .agent summaries
  + durable registries (no raw source/logs/diffs); no findings/secrets/paths leak;
  next actions catalog-backed; PENDING/FAIL/open-blocker-high → blocker; no duplicate
  ProposedTasks (fingerprint dedupe); live_review NOT PENDING. ALL satisfied.

### Changed Files (Steps 1399-1428)
| File | What changed | Why |
|---|---|---|
| `packages/orchestration/self_dogfood.py` | NEW — models, evidence source registry, live-review/stale-handoff/evidence-gap/quality-debt/roadmap detectors, classification, plan builder, propose (ProposedTask), report, exports | Core self-dogfood planner |
| `packages/orchestration/run_contract.py` | self_inspect / self_plan / self_propose_task actions (allowed default; no apply/test/provider) | Gate planning vs execution |
| `apps/cli/command_catalog.py` | self group + inspect/plan/report (read_only) + propose (write_metadata) | CLI surface |
| `apps/cli/grouped.py` | parse --job-id / --item-id / --top | Self flags |
| `apps/cli/commands/self_cmd.py` | NEW — inspect/plan/propose/report handlers | Wire CLI |
| `apps/cli/commands/__init__.py` | register self_cmd | Handler collection |
| `packages/orchestration/progress_ledger.py` | self-improvement proposed/pending/approved/deferred items (durable ProposedTasks; status .value normalized) | Progress surface |
| `packages/orchestration/feature_planner.py` | self-improvement-pending-evaluation → decision list (no auto exec) | Human next-step |
| `packages/orchestration/review_bundle.py` | self_dogfood_summary.json (REQUIRED_SECTIONS 19→20) | Reviewable summary |
| `packages/orchestration/ui_server.py` | read-only self_dogfood cockpit section | Surface counts |
| `docs/self-dogfood-v0.md` | NEW — planner doc | Long-term knowledge |
| `tests/orchestration/test_self_dogfood.py` | NEW — 19 unit/idempotency/redaction/architecture tests | Coverage |
| `tests/cli/test_self_dogfood_cli.py` | NEW — 7 CLI runtime tests | Coverage |
| `tests/orchestration/test_review_bundle.py`, `tests/ui_server/test_dashboard_cockpit_truth.py` | REQUIRED_SECTIONS==20 + cockpit shape | Keep invariants |
| `.agent/plan.md`, `.agent/context.md`, `.agent/live_review.md` | block state + product readiness + review | Runtime state |

### Readiness + merge
Readiness ~95% (planning rail only; guarded self-execution deliberately deferred).
Merge-ready. Next block: Self-Dogfood Execution v0 OR Provider Trust Verification v1.
