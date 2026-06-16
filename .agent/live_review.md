# Live Review — Steps 1917-1960: Token-Aware Repair Loop v1/v2

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): repair loop metadata/state machine; repair work items from failure artifacts; repair
work items from review findings; token-aware repair context packs; route recommendations; candidate
intake state tracking; review gate tracking; re-test gate tracking; mission contract integration; CLI
visibility; command catalog / run_contract entries; progress ledger / feature planner / review bundle /
cockpit summaries; integrity checks; docs/tests. Existing bounded test execution may be CONSUMED but
must stay bounded/synchronous (no unbounded/background exec).
Must NOT: provider/Claude/Pi/OpenCode/Ollama execution; direct worker execution; ARBITRARY command
execution; auto-apply; auto-approval; autonomous repair mutation; auto-PR/git automation; real rollback
restore; internal MemPalace memory; embeddings/vector DB; UI redesign; MCP activation.
BRIDGE BLOCK — test failure → controlled repair. Hard invariants: failure artifact is EVIDENCE not raw
log dump; repair context minimal + token-aware; candidates UNTRUSTED until reviewed; candidate quality
pass ≠ applied; applied ≠ repaired until re-test passes; `Done:` ≠ reviewer `Resolved`; open review
findings block repair completion; failed/timeout latest relevant test blocks repair completion; max
attempts/retests prevent infinite loops; required blockers vs optional ideas separated; token reduction
must NOT drop safety-critical evidence; NO provider/model/worker exec; NO auto-apply/approval/mutation;
no fake repaired state; no fake autonomy.
Timestamp: 2026-06-16

## Verdict (reviewer-owned)
**PASS WITH RISKS** @ 5c411dd — zero open Blocker/High/Medium; ONE documented Low (R-0105, integrity-
scanner completeness vs Check 12). All 13 checks PASS (Check 12 PASS with the documented Low). Targeted
suite 516 passed (345 + 171), 0 failed. No forbidden execution path (no shell=True / arbitrary cmd /
provider / worker / model / network / git-write / embeddings / MemPalace); no auto-apply/approve/mutate/
PR; no real rollback restore; no fake repaired (review+apply+retest gates with durable evidence). Token
pack bounded (unknown→decision, oversized→compress, no raw). Route reco never executes (unknown/
expensive→human approval; external→package-create ingress; local only if safe+available). English-only;
changed-files table present. Merge-ready (Low documented). Auto-merge applies on reviewer PASS per merge-
autonomy; NO PR opened (user has not asked).
RISKS: (1) R-0105 Low. (2) Builder full-suite self-report "6283 passed" REJECTED — NOT reproduced: a
deterministic, PRE-EXISTING failure `test_project_brain.py::TestFileProvenanceChain::test_full_chain_
order` exists (fails standalone AND at base 43197d9; unrelated to repair-loop scope — commit touched no
file_provenance/project_brain source). Carry-forward repo issue, NOT a 1917-1960 regression; block's own
targeted suite is fully green.

## Check matrix (reviewed @ 5c411dd)
1. Mainline closure — PASS. Real Test Execution v1 (1877-1916) reviewer PASS @ 7230268 merged via PR #73
   → main `43197d9`. Fresh branch `feature/steps-1917-1960-token-aware-repair-loop-v1-v2` off merged
   main `43197d9`; ZERO feature commits before closure; plan.md/context.md reconciled (Current Step
   1917) before code commit.
2. Repair models — PASS. `RepairLoopPolicy` (bounded max_attempts/max_retests/max_estimated_tokens +
   gate flags), `RepairWorkItem`, `RepairAttempt`, `RepairLoopEvaluation`; explicit `RepairLoopStatus`
   set (13 statuses incl BLOCKED/ABANDONED/RETEST_FAILED); `to_dict` scrubs via `_safe` (≤300) +
   `_safe_file_refs` (basenames, bounded ≤12, no `..`); unknown defaults explicit; from_dict safe.
3. Failure artifact integration — PASS. `create_repair_item_from_failure_artifact` idempotent via
   `_stable_repair_id` (sha256); uses artifact SAFE summary + `output_ref` only (never raw); missing/
   non-test artifact → None (safe); `suspected_files` = `_safe_file_refs` only; does NOT start repair.
4. Review finding integration — PASS. `create_repair_item_from_review_finding`: only OPEN finding at
   {blocker,high,medium} floor creates a required item; `status != "open"` (incl Done marker) or below
   floor → None. `_review_gate` re-checks the specific finding still open → "open" blocks; uses
   `parse_review_findings` verdict (pass / pass_with_risks-low-only) — reviewer verdict beats self-report.
5. Token-aware context pack — PASS. `build_repair_context_pack` read-only: safe summaries + `output_ref`
   + ids + token estimate + route hint only; never raw logs/diffs/candidates. band unknown OR budget
   unknown → `needs_decision`/`unknown_context` (never blind cheap). very_high/huge/over_budget/over →
   `needs_compression`. `requires_human_approval` defaults True.
6. Route recommendation — PASS. `recommend_repair_route` read-only, NEVER executes. unknown/requires-
   approval → `human_review` + approval. local_worker only when `prefer_local` AND `local_first` AND a
   worker that is enabled+user_selectable+not placeholder+not hard_safety_requires_approval (no fake
   Ollama readiness). else `external_builder_package` ingress (no exec) + approval. Respects Worker
   Registry / Token Economy hint / Route Policy.
7. Candidate/review/apply/retest gates — PASS. `evaluate_repair_loop`: candidate absent → CONTEXT_NEEDED/
   WAITING_FOR_CANDIDATE; review open → REVIEW_FAILED; review unknown → WAITING_FOR_REVIEW; apply not
   present (policy) → WAITING_FOR_APPLY_APPROVAL; retest failing → RETEST_FAILED; retest none/unknown →
   APPLIED_WAITING_RETEST. received≠repaired, quality≠applied, applied≠repaired until retest green.
8. State machine / loop safety — PASS. `len(attempts) > max_attempts` → BLOCKED + user decision; failing
   retests > max_retests (stop_on_repeated_failure) → BLOCKED + user decision (no infinite loop). Every
   returned state sets `required_next_actions` (catalog-valid) or `blocked_reasons`. REPAIRED only when
   review_ok AND apply_ok AND retest_ok (policy gates) + `satisfied=True`; defensive else → WAITING_FOR_
   REVIEW (never fake repaired).
9. Mission contract integration — PASS. `repair_loop_mission_signal` (open/blocked/repaired counts +
   user_decision); `_gather_mission_evidence` sets `repair_status="needed"` when repair_needed/user_
   decision; satisfaction conjunctive requires `repair_status != "needed"` (overnight_mission L633);
   blocked/abandoned → user_decision_required. Honest (no fake repaired).
10. CLI/catalog/run_contract — PASS. Catalog `repair.*`: item-show/list/context-pack/route-recommend/
    attempts/policy-show/integrity = read_only; item-create-from-failure/review + evaluate + policy-set =
    write_metadata. NO `may_execute`. run_contract `REPAIR_ITEM_CREATE/EVALUATE/POLICY_SET/SHOW` in
    `_DEFAULT_ALLOWED_ACTIONS`, none executable. CLI handlers stdlib-only, JSON-safe, no exec/apply/
    approve/shell.
11. Progress/Feature/Review/Cockpit — PASS. progress_ledger + feature_planner (required vs optional
    separated + Impact/Effort) + review_bundle (33→34 sections) + ui_server cockpit repair_loop READ-
    ONLY; safe summaries (counts/ids/status), no raw/private.
12. Integrity — PASS (with R-0105 Low). `audit_work_item_safety` (raw_or_secret_in_public via
    `_RAW_MARKERS` incl diff/BEGIN/Traceback/secrets, absolute_path_in_public, unknown_status);
    `audit_evaluation_safety` (repaired_with_open_review_finding, repaired_with_failing_retest,
    repaired_without_apply_proof, repaired_but_not_satisfied); `repair_loop_integrity` (repaired_but_not_
    satisfied + non_catalog_next_action). Done≠Resolved manifests as repaired_with_open_review_finding.
    GAP (R-0105, Low): no DEDICATED scanner code for max-attempts/retests-exceeded-without-blocked, nor
    optional-idea-marked-required — both STRUCTURALLY enforced by `evaluate_repair_loop` + tested, so no
    runtime path produces them; defense-in-depth completeness only.
13. Architecture guards — PASS. `repair_loop_v2.py` = stdlib (json/os/re/dataclasses/datetime/pathlib/
    typing/uuid/hashlib) + `provider_trust` scrub only. NO provider SDK / network / browser / subprocess
    / shell=True / arbitrary exec / git-write / apply-approve-PR / Ollama-cloud-model exec / embeddings-
    vector-DB / MemPalace. CLI cmd = stdlib only. Reuses v0/v1 repair_loop + real_test_execution +
    review parser + token_economy (no duplicated apply cycle, no execution).

## Findings — Steps 1917-1960

### R-0105
- **Severity**: Low
- **Status**: Open
- **Area**: `packages/orchestration/repair_loop_v2.py` `repair_loop_integrity` /
  `audit_evaluation_safety`.
- **Problem**: Check 12 enumerates eight integrity detections. Six are present as dedicated codes
  (repaired_with_open_review_finding, repaired_with_failing_retest, repaired_without_apply_proof,
  repaired_but_not_satisfied, raw_or_secret_in_public, absolute_path_in_public/unknown_status,
  non_catalog_next_action; Done-as-Resolved is caught indirectly via repaired_with_open_review_finding).
  TWO have NO dedicated scanner code: (a) max-attempts/max-retests exceeded while status is not
  BLOCKED/ABANDONED, and (b) an optional future idea appearing in `required_next_actions` (optional-
  marked-required-without-evidence). Both invariants ARE enforced at runtime by `evaluate_repair_loop`
  (attempts/retests over bound → BLOCKED + user decision before REPAIRED; `_optional_ideas` returns a
  separate list never merged into `required`) and are covered by unit tests, so no runtime path can
  produce the bad state. Impact is limited to defense-in-depth completeness of the standalone integrity
  scanner vs the Check-12 checklist — hence Low.
- **Fix options**: add two `repair_loop_integrity` codes — `attempts_exceeded_without_blocked`
  (attempts_count > policy.max_attempts OR failing-retests > policy.max_retests while status ∉
  {blocked, abandoned}) and `optional_idea_in_required_actions` (a `required_next_actions` entry that
  matches an `optional_next_ideas` entry / is not evidence-backed). Add regression tests.
- **Done: R-0105** — Added three dedicated integrity codes to `audit_evaluation_safety`:
  `attempts_exceeded_without_blocked` (attempts_count > max_attempts while status ∉ {blocked,
  abandoned}), `retests_exceeded_without_blocked` (failing_retest_count > max_retests while status ∉
  {blocked, abandoned}), `optional_idea_marked_required` (overlap between required_next_actions and
  optional_next_ideas). Wired into `repair_loop_integrity` scanner with attempt-loading for failing
  retest count. Added 9 regression tests (3 positive + 6 negative). Targeted suite 43+107 passed.

Next id: R-0106.

## Reviewer test run (targeted)
- `remedy_pytest.sh test_repair_loop_v2.py + tests/cli/test_repair_loop_v2_cli.py + test_overnight_
  mission.py + test_real_test_execution.py + test_run_contract.py + tests/test_command_catalog.py +
  tests/cli/test_command_catalog.py + test_progress_ledger.py + test_feature_planner.py +
  test_review_bundle.py + test_integrity_gate.py -q` → **345 passed**.
- regression: `test_worker_registry.py + test_builder_routing.py + test_model_route_tournament.py +
  test_model_route_tournament_integration.py + test_token_economy.py + test_token_economy_integration.py
  + test_repair_request_builder.py + test_builder_repair_loop.py -q` → **171 passed**. Targeted total
  **516 passed**, 0 failed. German scan CLEAN.
- FULL-SUITE: builder self-report "6283 passed, 8 skipped, 1 deselected" is REJECTED (not reproduced).
  Reviewer observed a deterministic failure `test_project_brain.py::TestFileProvenanceChain::test_full_
  chain_order` (provenance chain missing `test_run` step) — fails standalone (1 failed/83 passed in file)
  AND at pre-block base `43197d9`. PRE-EXISTING, out of repair-loop scope (commit modified no
  file_provenance/project_brain source). NOT a 1917-1960 regression. Carry-forward repo issue to raise
  separately. Block acceptance rests on the green targeted verification (zero open Medium/High/Blocker
  in scope), not on the rejected full-suite claim.

## Reviewer audit log
- VERDICT PASS WITH RISKS @ 5c411dd — one documented Low R-0105 (integrity-scanner completeness vs
  Check 12: max-attempts/optional-marked-required detections absent but structurally enforced +
  tested). All 13 checks PASS. Repair loop verified: no exec/apply/approve/mutate/PR/git; no fake
  repaired (review+apply+retest gates + satisfied); bounded loop (max_attempts/retests→BLOCKED+user
  decision); token pack bounded (unknown→decision, oversized→compress, no raw); route never executes
  (unknown/expensive→approval, external→package ingress, local only if safe+available); mission gate
  required-repair-blocks-satisfaction; catalog read_only/write_metadata no may_execute; English-only.
  Targeted 516 passed. Builder full-suite "6283 passed" REJECTED (pre-existing unrelated failure
  test_project_brain::test_full_chain_order at base 43197d9; out of scope, not a regression).
- Block opened. Check 1 (mainline closure) PASS @ branch base `43197d9` (PR #73 merged Real Test
  Execution v1 → main). Prior block 1877-1916 PASS @ 7230268 (R-0104 Resolved) merged; fresh branch at
  main tip; no work before closure. Plan.md reconciled to new block (Current Step 1917) before commit.
- WATCH (BRIDGE failure→repair): failure artifact = evidence not raw dump; context minimal+token-aware
  (no full logs/repo/candidate dumps; oversized→compress/human; unknown≠cheap; safety-critical evidence
  kept); candidates UNTRUSTED (received≠repaired, quality≠applied, applied≠repaired until passed
  re-test; failed/timeout re-test blocks); open Blocker/High/Medium findings block completion;
  Done≠Resolved; reviewer verdict beats self-report; max attempts/retests (no infinite loop, user
  decision at limit, no fake repaired); required blockers vs optional ideas separated; route reco
  respects registry/policy/economy/tournament (expensive/unknown→approval, disabled not recommended,
  external→package-create not exec); mission gate (required repair blocks satisfaction); integrity 8
  detections; CLI read_only/write_metadata no may_execute; NO provider/worker/model exec, NO auto-apply/
  approve/mutate/PR/git, NO real rollback restore, NO MemPalace/embeddings/MCP/UI-redesign; all
  project-facing text English.
- Merge-autonomy: PR #73 (prior block) auto-merged on reviewer PASS per merge-autonomy. No PR for THIS
  block; NO PR unless user asks.
