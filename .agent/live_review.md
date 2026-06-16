# Live Review — Steps 1837-1876: Overnight Mission Contract + Review/Repair Spine v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict;
a builder `Done:` marker is NOT reviewer `Resolved`).
Scope (ALLOWED): Overnight Mission Contract metadata + contract creation from job/prompt + mission
evaluation + review finding detection + metadata-only review/repair state machine + next-safe-action
planning + required-vs-optional idea queue surfacing + progress/feature/review/cockpit safe summaries
+ CLI visibility + catalog/run_contract entries + integrity + docs/tests. METADATA + EVALUATION +
PLANNING ONLY — no execution.
Must NOT: Claude/Pi/OpenCode/Ollama/provider/local-model execution; MemPalace integration/internal
memory; embeddings/vector DB; auto-apply; auto-approval; uncontrolled test execution; auto-repair;
auto-PR/git; UI redesign; MCP activation.
Strategic lens: mission satisfaction must be evidence-backed; open Blocker/High findings block
completion; `Done:`≠`Resolved`; builder self-report cannot override reviewer verdict; missing
required tests/proofs/snapshots block completion; no fake overnight readiness; required blockers vs
optional ideas clearly separated; next actions catalog-valid; no raw/secret/path/traceback leak; no
worker/provider/model execution. BLOCK if this becomes a fake overnight runner.
Timestamp: 2026-06-16

## Verdict (reviewer-owned)
FAIL @ 39bd3cc — one open Medium (R-0102) in the core evaluator. No safety-invariant violation (never
fake-satisfied; no execution; no leak; English-only), but mission evaluation is wrong on the primary
production path. Builder must NOT claim merge-ready while FAIL. Re-review after fix + targeted re-run.

## Check matrix (reviewed @ 39bd3cc)
1. Mainline closure — PASS. Tournament v0 merged via PR #71 → main `4ddd59f` (incl R-0101 closure
   `4dabf5c`). Branch off merged main; no work before closure.
2. Mission Contract model — PASS. Bounded safe fields; `to_dict` scrubs `user_goal`(≤300)/criteria
   (≤200); explicit `required_gates` + `forbidden_actions`; `validate_mission_contract` rejects
   unknown gates / negatives. Acceptance-criteria absence → `needs_user_acceptance_criteria`, never
   done. No raw/private leak.
3. Review finding detection — PASS. Reuses `parse_review_findings`: open counts come ONLY from
   `### R-xxxx` blocks with `**Status**: Open` (a `Done:` marker never flips Status → Done≠Resolved);
   verdict read from `## Verdict` heading (reviewer-owned file). `evaluate` blocks on
   open_blocker+high>0 and on verdict in pending/fail/unknown → reviewer verdict beats self-report;
   PENDING/FAIL blocks completion.
4. Mission evaluation — **FAIL (R-0102, Medium)**. Satisfaction logic is correctly conjunctive
   (criteria ∧ review_clean ∧ open_tasks==0 ∧ failed_tests==0 ∧ no missing_proofs ∧ repair≠needed) and
   never fake-satisfied; BUT first-evaluation self-block via mission progress items counted as
   open_tasks (see R-0102). Safe direction, but wrong on the production path.
5. Next safe action planning — PASS. All emitted commands catalog-valid (`overnight contract-show/
   evaluate/contract-create`, `review list`, `repair status`, `progress checklist`); no provider/
   Ollama/Claude/Pi action; `user_decision_required` flagged; no-action → BLOCKED.
6. Review/repair spine — PASS. Metadata-only state machine; statuses include WAITING_FOR_REVIEW /
   REPAIR_NEEDED; satisfied requires review_clean ∧ repair≠needed → cannot satisfy while review/repair
   incomplete. No worker/test/apply/git.
7. IdeaFactory / Feature Planner — PASS. `required_next_actions` vs `optional_next_ideas` separated;
   optional ideas surfaced ONLY when `evaluation.satisfied` (L688) so blockers never mix with future
   ideas; ideas carry impact+effort, `required=False`, no auto-build.
8. Surfacing — PASS with note. Ledger/bundle/cockpit honest: `live:False`, no mutation buttons, no
   fake done/overnight-run; satisfied/status from durable evaluation; safe summaries only. NOTE: the
   green test suite does not exercise the real-UUID evaluation path (see R-0102 blind spot).
9. CLI/catalog/run_contract — PASS. `overnight contract-create`/`evaluate`=write_metadata;
   `contract-show`/`next-action`/`cycles`/`contract-readiness`/`integrity`=read_only; none
   may_execute; run_contract gates CREATE/EVALUATE/SHOW (default-allowed, non-exec). Invalid ids safe
   (corruption-aware loaders, never raise).
10. Integrity — PASS (core). `audit_evaluation_safety` flags satisfied_with_open_findings /
    _missing_gates / _open_tasks / _failing_tests + raw_or_secret_in_public + absolute_path_in_public;
    `mission_integrity` adds absolute_path_in_contract. (Done≠Resolved, verdict-override, fake-ready
    are enforced structurally in the parser/evaluator/readiness, not as integrity codes — acceptable;
    catalog-validity of next actions is covered by the catalog parser, not integrity.)
11. Architecture guards — PASS. `overnight_mission.py` = stdlib (json/os/dataclass/datetime/pathlib/
    typing/uuid) + provider_trust scrub helpers only. No provider/Claude/Pi/OpenCode/Ollama/cloud/
    network/browser/subprocess/shell/SDK; no embeddings/faiss/chromadb/vector DB; no MemPalace; no
    apply/approve/test/git/PR; no `.tasks.append`. Storage atomic 0o600/0o700.

## Findings — Steps 1837-1876

### R-0102
- **Severity**: Medium
- **Status**: Open
- **Area**: `packages/orchestration/overnight_mission.py` `_gather_mission_evidence` (open-task
  counting) × `packages/orchestration/progress_ledger.py` `build_progress_ledger` (line ~1810
  `merge_mission_items`).
- **Problem**: Circular self-block. `evaluate_mission_contract` → `_gather_mission_evidence` →
  `build_progress_ledger(job, events)` which (line ~1804-1812) merges this contract's OWN mission
  progress items into the same ledger. `_gather` then counts ledger items in
  PLANNED/IN_PROGRESS/BLOCKED as `open_tasks` (overnight_mission.py L480-487), and its exclusion list
  (L482-484) covers only `token-economy-local`/`route-policy-local`/`tournament-winner` — NOT
  `mission-*`. On the FIRST evaluation of a real-UUID job, no persisted evaluation exists yet, so
  `extract_mission_items` emits `mission-not-evaluated` with status PLANNED → counted as an open task →
  `open_tasks>=1` → contract reports **not satisfied** (status `running_metadata_only`) even when
  acceptance criteria are met, review is clean, gates pass, and there are zero real open tasks.
  (`mission-user-decision` BLOCKED can similarly inflate when a stale persisted eval had
  `user_decision_required`.) Direction is SAFE (never fake-satisfied; it errs toward not-done) and it
  self-heals on the 2nd evaluate (once a prior eval is persisted, `mission-not-satisfied` is RISK and
  uncounted) — so NOT a Blocker/High. But the central evaluator (Check 4) returns a wrong result on
  the primary production path.
- **Why tests miss it (Check 8 blind spot)**: `test_satisfied_when_clean` uses `job_id="j"` (not a
  UUID); `_gather_mission_evidence` does `load_job(UUID("j"))` which raises → `job=None` →
  `build_progress_ledger` is skipped entirely → mission items never merged → first-eval satisfied
  passes. With a real UUID job the ledger path runs and the self-block triggers. So the green suite
  does not exercise the production evaluation path.
- **Fix options**: (a) exclude `mission-`-prefixed item_ids from the open-task count in
  `_gather_mission_evidence` (mirror the existing prefix exclusion at L482); or (b) do not merge
  mission items inside `build_progress_ledger` when it is being built for mission evaluation (pass a
  flag / use a leaner builder); or (c) build the ledger used for evaluation without the
  self-referential merge. Add a regression test that drives `evaluate_mission_contract` with a REAL
  persisted job + ledger (valid UUID) and asserts first-eval satisfied for a clean contract.

Next id: R-0103.

## Reviewer test run (targeted)
- `remedy_pytest.sh test_overnight_mission.py + _integration.py + test_overnight_mission_cli.py +
  test_review_bundle.py + test_overnight_executor.py -q` → **135 passed**.
- regression: `test_command_catalog.py + test_dashboard_cockpit_truth.py + test_progress_ledger.py +
  test_feature_planner.py + test_run_contract.py + test_model_route_tournament.py +
  test_worker_registry.py + test_token_economy.py -q` → **295 passed**.
- repair regression: `test_repair_loop_v1.py + test_repair_loop_hardened.py +
  test_builder_repair_loop.py -q` → **39 passed**. Targeted total **469 passed**, 0 failed.
- NOTE: green suite does not cover the real-UUID evaluation path (R-0102 blind spot). Builder
  full-suite self-report NOT accepted while Medium open.
- German scan (module/cmd/2 docs) CLEAN. Danger scan (committed core+cmd) CLEAN.

## Reviewer audit log
- VERDICT FAIL @ 39bd3cc — open Medium R-0102 (first-eval self-block). No safety violation.
- Block opened. Check 1 (mainline closure) PASS @ branch base `4ddd59f`. Pre-existing overnight_*.py
  (executor/readiness/cmd) carried from prior blocks — any modifications will be reviewed against the
  metadata-only / no-execution invariants.
- WATCH: contract cannot be satisfied with open Blocker/High findings or reviewer PENDING/FAIL;
  `Done:`≠`Resolved`; missing required gates/tests/proofs/snapshot block satisfaction; no fake
  overnight-ready; required blockers separated from optional future ideas; next_safe_action
  catalog-valid; CLI read_only/write_metadata only (no may_execute_commands); no provider/Ollama/
  cloud/network/subprocess/embeddings execution; no auto-apply/approve/test/repair/git/PR; all
  project-facing text English.

## Builder remediation — R-0102 (+ handoff truth) (awaiting reviewer re-check @ new HEAD)
Done: R-0102 - _gather_mission_evidence now excludes mission-* prefixed ledger item_ids from open-task counting (mirrors the existing token-economy-local/route-policy-local/tournament-winner prefix skip), so the mission evaluator no longer self-blocks on its own merged ledger items (e.g. mission-not-evaluated/mission-user-decision) on the real-UUID production path. Genuine job/task/repair/test/review blockers still counted; safety gates unchanged (never fake-satisfied). Regression tests: test_real_uuid_job_first_eval_not_self_blocked (real persisted UUID job → first eval open_tasks==0, satisfied==True with clean review + acceptance + gates), test_real_non_mission_open_task_still_blocks (open High review finding still blocks).
Done: R-0103 - .agent/plan.md reconciled: steps 1837-1857 marked [x], Current Step set to 1858-1876 review closure / awaiting reviewer PASS; carried risks preserved; reviewer verdict NOT changed by builder.

Builder verification: targeted overnight/ledger/bundle/cockpit/catalog/run_contract = 274 passed; overnight + central integrity passed. Full pytest = 6200 passed, 8 skipped, 1 deselected (exit 0). NOT claiming merge-ready — reviewer owns verdict at new HEAD.
