# Live Review — Steps 1573-1608: Expensive Builder Routing v0

Reviewer: parallel reviewer (independent; owns verdict — builder self-report does not set verdict, protocol §5)
Scope: Local-first, budgeted, anti-loop ROUTING/POLICY for when Remedy should use deterministic
logic, local advisory, local candidate generation, or expensive external builder generation.
Routing/policy/planning ONLY. Must NOT: execute any builder/model/provider, call network/
subprocess/cloud/SDK, generate candidates, apply/approve, create Patch Intents/ProposedTasks
directly, create PRs/git, leak raw prompt/response/source/diff/log/secrets/tracebacks/abs paths,
treat model output as truth, recommend external builder without request package + Trust Gate +
Verification + budget + low loop risk + no pending approval/intent, loop on repeated failed
generation, or emit fake next actions. NO PR unless user asks (Step 1608).
Timestamp: 2026-06-15

## Verdict (reviewer-owned)
PASS — R-0088 (HIGH) + R-0089 (MEDIUM) RESOLVED @ d2a1ee4 + R-0090 (LOW, handoff) RESOLVED @ 8579774,
all reviewer-verified; ZERO open findings. Changed-files table now present in BOTH .agent/context.md
(committed earlier) AND .agent/live_review.md (@ 8579774), reconciled vs `git diff --name-only
d22e1dd..HEAD` = all 20 changed prod/test/doc files covered (incl. orchestrator_brain.py from the fix).
Merge-ready (NO PR — Step 1608, held for explicit user request). All SAFETY properties PASS: routing is planning-only
(no builder/model/provider execution, no network/subprocess/SDK, no candidate generation, no Repair
Artifact/Patch Intent/ProposedTask creation, no apply/approve/PR/git, no Job.tasks); external generator
DISABLED by default + gated behind request-package + trust + verification + budget + low-loop-risk +
no-pending (user_requested justifies, never bypasses); unknown external cost blocks external; loop
governor blocks repeat-same-evidence / escalates repeated failure; pending intent/approval &
unverified-trust suppress generation; redaction clean (no raw/secret/path/diff; trace 0o600). The
selector next_safe_action defect (R-0088/R-0089) is fixed: all emitters now produce catalog-valid
commands, and a new regression class validates every emitted next_safe_action through the real
`apps.cli.grouped.build_parser()` + static shape guard (closes the prior testing gap). REVIEWER-
INDEPENDENT verification: targeted `scripts/remedy_pytest.sh` (test_builder_routing +
test_builder_routing_cli + test_review_bundle) = **90 passed** post-fix (was 113 pre-fix on a wider
set); builder-reported full pytest 5852 passed/8 skipped/1 deselected (exit 0) — relied on per
standing rule. NO PR (Step 1608).

## Check Matrix (1-15)
| Check | Status | Note |
|---|---|---|
| 1. Mainline reconciliation (verification PR #64 merged; clean branch; residuals carried) | PASS | off clean main d22e1dd; prior NIT resolved c29a6bf |
| 2. Routing models + tiers + policy (no raw content fields) | PASS | 6 tiers distinct; defaults safe; external+local-gen disabled by default; no hidden exec |
| 3. Routing inputs (safe summaries only; unknown stays unknown) | PASS | reuses _gather_signals (durable, try/except→unknown); advisor CONFIG only, never calls model |
| 4. Candidate-generation need detector (suppress on pending/blocker/budget/loop/missing) | PASS | hard suppressors: pending_intent/approval, review_blocks, unverified-trust, needs-review |
| 5. Local-first decision rules (deterministic→advisor→local-gen→external) | PASS | strict priority ladder; deterministic action dominates new generation |
| 6. Expensive builder justification codes + hard preconditions | PASS | _external_allowed requires ALL (pkg/trust/verif/budget/low-loop); user_requested justifies not bypasses |
| 7. Budget model (unknown cost blocks external; local≠external) | PASS | estimated_external_cost never invented; unknown→block external; per-failure/daily from traces |
| 8. Loop governor (no repeated expensive route without new evidence) | PASS | same-fp external→BLOCK; repeated failure→HUMAN_REVIEW; 1 rejection→WARN; new fp resets |
| 9. Routing selector (exactly one tier / no_safe_route / human_review) | PASS | R-0088/R-0089 RESOLVED @ d2a1ee4; all emitted next_safe_action now parse via build_parser (regression-tested) |
| 10. Trace persistence (atomic; safe; idempotent by fingerprint) | PASS | _save_trace 0o600/dir 0o700 + content_sha256; idempotent by fingerprint unless --new |
| 11. CLI decide/report + catalog + run_contract | PASS | decide write_metadata, report read_only, no exec/mutate; BUILDER_ROUTING_DECIDE/REPORT default-allowed non-cloud |
| 12. Orchestrator / local-advisor / verification / self-dogfood integration | PASS | reuses signals/advisor-config/verification/self via durable summaries; no exec |
| 13. Progress/Feature/Review-bundle/Cockpit | PASS | fixed item_ids; bundle +builder_routing_summary; cockpit counts/no buttons; next_action now valid (R-0088 fixed upstream) |
| 14. Redaction (no raw in any surface) | PASS | _scrub_public; trace/export = codes/counts/IDs/fingerprint only; no raw/secret/path/diff |
| 15. Architecture guards (no exec/SDK/net/subprocess/apply/approval/PR/intent) | PASS | stdlib+_scrub_public; lazy internal imports only; no save_job; no source_apply/patch_apply/materialize |
| (tests) Targeted + full pytest once | PASS | reviewer targeted post-fix = 90 passed; new regression validates emitted next_safe_action via build_parser; builder full 5852 passed/8 skipped/1 deselected |
| (handoff) Changed-files table present | PASS | R-0090 RESOLVED @ 8579774 — table in context.md + live_review.md; 20 files reconciled vs git diff |

## Findings — Steps 1573-1608

## Finding R-0088
Status: Resolved
Resolution: RESOLVED @ d2a1ee4 (reviewer-verified). `_report_cmd` now emits `remedy builder-routing
report --job-id {job_id} --json` (matches catalog --job-id option); feature_planner 3 templates
switched to `--job-id <job_id>`. New regression class runs every emitted next_safe_action through
the real `apps.cli.grouped.build_parser()` + a static guard rejecting `builder-routing report
{job_id}` / `<job_id>` positional shapes. Reviewer re-ran targeted scripts/remedy_pytest.sh = 90
passed. Emitted command now parses.
Severity: high
Area: selector
Summary: `_report_cmd` emits an unrunnable `builder-routing report` next_safe_action (positional job vs `--job-id` option) — block-if "selected next action is fake".
Details: `builder_routing._report_cmd` (builder_routing.py L753-754) returns
`f"remedy builder-routing report {job_id} --json"` — passing job_id as a POSITIONAL arg. But the
catalog entry `builder-routing.report` defines `--job-id` as `is_option=True` (no positional), and
`apps/cli/grouped.py::_add_command_args` builds the real argparse purely from those catalog args.
So the emitted command parses as an unexpected positional → argparse "unrecognized arguments"
error; it cannot run. `_report_cmd` is the next_safe_action for the MAJORITY of routing outcomes
(human_review_required, loop block, no-trust/verification, no-need, all-generators-disabled),
so the module's headline output is broken in the common path. Nothing validates the emitted
next_safe_action against the catalog (unlike orchestrator_brain's `validate_next_safe_action_command`).
Not a safety hole (argparse fails closed; no exec/leak) but defeats Check 9 "next action
catalog/entity-backed" and hits the block-if "selected next action is fake or lacks required entity".
Evidence: builder_routing.py:753 `return f"remedy builder-routing report {job_id} --json" ...`;
command_catalog.py builder-routing.report args = `ArgDef("--job-id", ..., is_option=True)` (no
positional job); grouped.py:_add_command_args adds options from catalog → `remedy builder-routing
report <jobid>` → error. `builder-routing.decide` likewise uses `--job-id` option, confirming the
intended form is `--job-id <id>`.
Scope note: the same wrong shape recurs in `feature_planner.py` (`remedy builder-routing report
<job_id> --json` templates) and propagates into `progress_ledger` items (`next_action=latest
next_safe_action`) and the cockpit/report surfaces — all downstream of the same root. ROOT CAUSE:
the catalog defines `builder-routing.decide/report` with `--job-id` as an OPTION, but every sibling
command (`repair.request`, `patch.approve`, `provider.verify`, `provider.verification-show`) uses a
POSITIONAL `_JOB_ID`, and all emitters (builder_routing + feature_planner) assume positional.
Cleanest fix: make `builder-routing.decide/report` use positional `_JOB_ID` (matches siblings +
every emitted string) — that single change corrects `_report_cmd` and the feature_planner templates.
Expected fix: Either (a) switch builder-routing.decide/report to positional `_JOB_ID` (recommended,
matches all emitters + siblings), or (b) emit `--job-id {job_id}` everywhere it is referenced; then
audit all emitted next actions for arg-shape correctness (ideally add a catalog-validation pass on
next_safe_action). Then write `Done: R-0088`.

## Finding R-0089
Status: Resolved
Resolution: RESOLVED @ d2a1ee4 (reviewer-verified). `_deterministic_action` now emits
`remedy self status --attempt-id {aid} --json` when a pending attempt id exists, else the scope-less
`remedy self status --json` — never the invalid `--job-id`. The attempt id comes from a real durable
signal (`self_pending_attempt_id` populated in orchestrator_brain `_gather_signals` from
`list_attempts`), not invented. Regression tests assert both forms parse via build_parser and that
`--job-id` is absent. Reviewer targeted run green (90 passed).
Severity: medium
Area: selector
Summary: `_deterministic_action` emits `self status --job-id …` but `self.status` has no `--job-id` flag → unrunnable next action.
Details: `builder_routing._deterministic_action` (builder_routing.py L359-360) returns
`f"remedy self status --job-id {job_id} --json"` for the `self_attempts_pending > 0` branch. The
catalog `self.status` entry defines only `--attempt-id` + `--json` (no `--job-id`), and the real
argparse is built from those args, so `--job-id` → "unrecognized arguments" error. Reachable when
self attempts are pending and no pending/approved intent, unverified-trust, or needs-review exists.
Fails closed (read-only command, no unsafe effect) but is a fake/unrunnable next_safe_action
(Check 9 + block-if "selected next action is fake").
Evidence: builder_routing.py:360; command_catalog.py self.status args = (`--attempt-id`, `--json`)
only.
Expected fix: Emit a valid form (e.g. `remedy self status --json`, or `--attempt-id <id>` if an
attempt id is available), then write `Done: R-0089`.

## Finding R-0090
Status: Resolved
Resolution: RESOLVED @ 8579774 (reviewer-verified). NOTE: this was a weak finding — when filing I
grepped only `.agent/live_review.md`, but protocol §53/§82 also accepts the table in the handoff
`.agent/context.md`, which already carried a committed changed-files table. Builder additionally added
a `| File | What changed | Why |` table to live_review.md @ 8579774 (incl. the orchestrator_brain.py
row from the R-0089 fix). Reviewer reconciled the table vs `git diff --name-only d22e1dd..HEAD` = all
20 changed prod/test/doc files covered. Block-if "final handoff lacks changed files table" satisfied.
Severity: low
Area: handoff
Summary: Final handoff lacks the protocol-required changed-files table (explicit block-if).
Details: (original) Protocol §53/§82 + block-if require a `| File | What changed | Why |` table; my
filing checked only live_review.md and missed the table already present in context.md.
Evidence: table now in context.md + live_review.md; reconciled vs `git diff --name-only d22e1dd..HEAD`
(20 files).
Expected fix: (done) table added to final handoff; `Done: R-0090` written @ 8579774.

Next id: R-0091.

## Builder remediation (awaiting reviewer re-check)
Done: R-0088 - fixed builder-routing report next_safe_action shape and added parser validation
Done: R-0089 - fixed self status next_safe_action shape and added regression coverage
Done: R-0090 - added protocol-required changed-files table to final handoff

## Changed files (Steps 1573-1608) — final handoff
| File | What changed | Why |
| ---- | ------------ | --- |
| packages/orchestration/builder_routing.py | NEW core: tiers/policy/inputs/need-detector/local-first selector/justification codes/budget/loop governor/safe trace persistence; R-0088/R-0089 emitter fixes (`_report_cmd` --job-id; `_deterministic_action` self status --attempt-id/scope-less) | the routing rail + runnable next actions |
| apps/cli/commands/builder_routing_cmd.py | NEW `builder-routing decide/report` handlers | CLI surface (planning only) |
| apps/cli/command_catalog.py | NEW builder-routing group + decide(write_metadata)/report(read_only) entries | catalog-backed commands |
| apps/cli/grouped.py | `--user-requested` store_true flag | CLI arg plumb |
| apps/cli/commands/__init__.py | register builder_routing_cmd in imports + handler loop | wire handlers |
| packages/orchestration/run_contract.py | BUILDER_ROUTING_DECIDE/REPORT actions in _DEFAULT_ALLOWED (non-cloud, non-exec) | contract gate |
| packages/orchestration/feature_planner.py | 4 builder-routing repair rules (R-0088 fix: report `--job-id <job_id>`) | suggestions, no auto-exec; runnable next actions |
| packages/orchestration/progress_ledger.py | extract/merge_builder_routing_items (fixed item_ids) | surface routing state, no raw |
| packages/orchestration/review_bundle.py | REQUIRED_SECTIONS 24→25 + _build_builder_routing_summary | bundle safe routing summary |
| packages/orchestration/ui_server.py | _build_builder_routing_section cockpit (counts/tier/flag) | read-only surface, no buttons |
| packages/orchestration/orchestrator_brain.py | _gather_signals exposes self_pending_attempt_id (R-0089 enables `self status --attempt-id`) | runnable self-status next action |
| tests/orchestration/test_builder_routing.py | NEW 24 tests (quality/budget/loop/redaction/arch) incl. TestEmittedCommandsRunnable parser validation (R-0088/R-0089 regression) | coverage + emitted-command runnability |
| tests/cli/test_builder_routing_cli.py | NEW 7 subprocess tests | CLI runtime coverage |
| tests/orchestration/test_review_bundle.py | REQUIRED_SECTIONS==25 + builder_routing_summary assert | bundle test update |
| tests/ui_server/test_dashboard_cockpit_truth.py | test_builder_routing_section_present | cockpit test update |
| docs/expensive-builder-routing-v0.md | NEW design doc | document the routing rail |
| docs/{orchestrator-brain-v0,local-model-advisor-v0,provider-trust-verification-v1,repair-request-builder-v0}.md | cross-ref updates | document the new stage |

Fix detail:
- `builder_routing.py::_report_cmd` now emits `remedy builder-routing report --job-id <id> --json`
  (was positional). All human-review / no-safe-route / generation-next branches route through it.
- `feature_planner.py` 3 builder-routing rules now emit `remedy builder-routing report --job-id
  <job_id> --json` (was positional `<job_id>`).
- `builder_routing.py::_deterministic_action` self-pending branch now emits
  `remedy self status --attempt-id <id> --json` when an attempt id is available, else
  `remedy self status --json` (was unsupported `--json --job-id`). `orchestrator_brain._gather_signals`
  now exposes `self_pending_attempt_id` (first intent_pending_approval attempt) to enable the
  --attempt-id form.
- Regression: `tests/orchestration/test_builder_routing.py::TestEmittedCommandsRunnable` parses every
  emitted next_safe_action through the real `build_parser()` (human-review report, no-safe-route,
  self-pending ±id, feature-planner builder-routing rules) + a static guard rejecting the broken
  shapes. These fail on the pre-fix branch, pass after.
- Tests: targeted builder_routing(24)/CLI(7)/feature_planner/orchestrator_brain/review_bundle/
  cockpit/command_catalog = 182 passed; full pytest 5852 passed/8 skipped/1 deselected (exit 0).
  Builder-run counts; reviewer to re-verify independently.

## Reviewer audit log
- Branch off clean main d22e1dd (PR #64 merged Provider Trust Verification v1; prior block NIT
  _INTENT_OK_RE resolved pre-merge). Prior block zero open findings — nothing to carry.
- Verified: PTV v1 merged to main via PR #64 → main `d22e1dd`; prior-block NIT `_INTENT_OK_RE`
  resolved @ `c29a6bf` (pre-merge). New branch `feature/steps-1573-1608-expensive-builder-routing-v0`
  off `d22e1dd`. `git log d22e1dd..HEAD` empty → no drift, no block code yet. Check 1 PASS.
- Reviewer runs targeted `scripts/remedy_pytest.sh` independently once tests land; relies on
  builder full-suite count for the full run. Reviewer findings beat builder self-report (§5).
