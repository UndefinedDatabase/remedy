# Handback — F252 R2 (R-0152 + every remaining class)

## Range
Review of cc247fa..e90ac41 + the handoff commit · feature/f252-standing-red-paydown ·
R-0152, D9, D7, D5, D13, D6, D4-rest, D1, D14, F-A pair done · D3 (10) + D12 (1)
quarantined by decision · delta done · no STOP.

## Commits
### 5b5fad4 chore(f252): persist R1 verdict + R-0152
| Path | +/- | Reason |
|---|---|---|
| .agent/authored/f252-r2-1/2.md · live_review.md · plan.md · last_block.md | +258/-132 | authored texts (sha256-verified) applied by copy; R2 block |
### a0c4717 fix(f252): drop the intake-bound fallback in do planning (R-0152)
| Path | +/- | Reason |
|---|---|---|
| apps/cli/commands/do_cmd.py · .agent/live_review.md | +13/-7 | no fallback to the intake-bound call_fn; without a FlightPlan-bound provider `do` takes the deterministic skeleton, as the no-provider path does. `Done: R-0152` |
### 92a69d9 fix(f252): repair command-catalog action-class drift
| Path | +/- | Reason |
|---|---|---|
| apps/cli/command_catalog.py · tests/test_command_catalog.py · tests/orchestration/test_job_evidence.py | +52/-15 | D9: `read_metadata` typo → read_only; job-evidence executes → test_execution; ActionClass Literal completed; `sk-` matched at a token boundary |
### ac13029 fix(f252): reach path redaction through its owning module
| Path | +/- | Reason |
|---|---|---|
| tests/runtimes/test_supervisor_portability.py · tests/orchestration/test_failure_postmortem.py | +27/-3 | D7: `ABS_PATH_RE` from packages.common.path_redaction; the anti-drift pin gains a third identity + a behavioural check |
### 2666568 fix(f252): align project-guard tests with the F148 contract
| Path | +/- | Reason |
|---|---|---|
| tests/test_cli_main.py · tests/orchestration/test_test_runner.py | +87/-20 | D5 (11): documented creation guard (exit 3); fixtures register a project; two ids renamed to the guard they now assert |
### 031cd97 fix(f252): repair evidence-packaging producers and retire root auto-select tests
| Path | +/- | Reason |
|---|---|---|
| packages/orchestration/manual_attestation.py · job_evidence.py · 2 test files | +180/-49 | D13 product: v1.1 run fields filled, head_sha threaded, commit-gate verdict read back from the artifact, runtime gate scans Remedy's own tree, `_scrub_paths` stops eating the first line. Tests: root auto-selection is retired (01e2018/bd93397), so they assert warn-and-ignore |
### e714200 feat(f252): allow a per-process runtime port override
| Path | +/- | Reason |
|---|---|---|
| packages/runtimes/runtime_config.py · tests/runtimes/test_apps_ui_probe.py | +101/-21 | F-A pair: `REMEDY_RUNTIME_PORT` moves one process off the product default; the real-runtime tests also serialize on a temp-dir lock |
### dd33032 test(f252): build real jobs where the product reads model fields
| Path | +/- | Reason |
|---|---|---|
| tests/orchestration/test_test_execution_service.py · test_test_runner.py | +33/-24 | D6 (9): real `Job` models instead of half-specced MagicMocks; no assertion changed |
### 5d7c591 chore(f252): make context.md current and pin the live state-file contract
| Path | +/- | Reason |
|---|---|---|
| .agent/context.md · tests/orchestration/test_test_runner.py | +68/-25 | D4 remainder: context.md rewritten to F252 reality; the two `Steps \d+-\d+` pins move to the feature/round convention |
### 4bf6340 test(f252): read docs at their restructured paths
| Path | +/- | Reason |
|---|---|---|
| 9 test files under tests/ | +65/-40 | D1 (36): ten docs read from docs/system|guides; `_read_doc` raises instead of returning "" |
### a696547 docs(f252): sync README with the ledger and repin the F012 contracts
| Path | +/- | Reason |
|---|---|---|
| README.md · tests/docs/test_docs_consistency.py | +87/-63 | D14 pins (13): README status → 24 of 252; the F012 pins move to the doc that owns them; the honesty pin cross-checks STATUS |
### 117ff32 fix(f252): pay down the misc drift class
| Path | +/- | Reason |
|---|---|---|
| pingpong_loop.py · project_registry.py · 8 test files | +167/-43 | D14 product: provider_backed evidence must carry its three counts (token_truth refused → artifact gate BLOCKED); `resolve_project` catches named failures only. Tests: retired contracts repinned (read-only project context, v2 UI-spec delegation, linked test evidence, RunInvocation, bare-assert rule, invalid-id stderr contract) |
### e90ac41 test(f252): quarantine the two decision classes with reasons
| Path | +/- | Reason |
|---|---|---|
| tests/regression/test_named_bugs.py · ui_contracts/×2 · test_agent_tooling.py | +44 | D3 (10) + D12 (1): per-test skip + reason + backlog ref; nothing deleted |
### handoff commit (self-reference exception)
| Path | +/- | Reason |
|---|---|---|
| .agent/handoff.md · .agent/last_block.md | rewrite · +1/-1 | this handback; OUTCOME → executed |

## External actions
13 pushes to origin/feature/f252-standing-red-paydown (one per slice), all OK; handoff
commit pushed last. No PR, no merge, no worktree.

## Verification
- R-0152 `pytest tests/cli/test_scoped_listings.py -q` → 0, "18 passed". D9
  `pytest tests/test_command_catalog.py -q` → 0, "18 passed". D7
  `pytest …test_failure_postmortem.py …test_supervisor_portability.py -q` → 0, "211 passed".
- D5 `pytest tests/test_cli_main.py -q` → 0, "48 passed" (test_test_runner residue = baseline).
  D13 `…test_review_zip_hygiene.py -q` → 0, "44 passed"; `…_manual_completion_shapes.py` 23 passed.
- F-A `pytest tests/runtimes/ -q -n 4` → 0, "251 passed"; the 4 ids green 3× in a row; nothing on port 5173.
- D6 `pytest …test_test_execution_service.py -q` → 0, "64 passed". D4/D1/D14 `pytest tests/docs/ -q` → 0, "292 passed"; `tests/cli/ tests/orchestration/ tests/regression/ tests/ui_contracts/ -n 4` NEW vs baseline = EMPTY.
- D3/D12 `pytest … -q -rs` → "276 passed, 11 skipped", each skip printing reason + backlog ref.
  Canary `pytest tests/cli/test_golden_path.py -q` → 0, "42 passed", after every slice.
- CLOSING `pytest -n auto -q --junitxml=…/f252-r2.xml` → exit 0, **"14295 passed, 19
  skipped in 132.31s"**; junitxml failing set = 0 ids. LC_ALL=C comm vs
  churn_gate2_run1.txt: NEW = EMPTY, GONE = 154 (all). 19 skipped = 8 pre-existing + 11
  quarantines.

## Authored-text proofs
f252-r2-1 (11d53808…) and f252-r2-2 (9b806d94…): on-disk `sha256sum` matched the BEGIN
markers exactly BEFORE any commit; applied by copy, `cmp` exit 0 for live_review.md and
plan.md. live_review.md was then edited in one place only, as ordered: `Done: R-0152`.

## Deviations & assumptions
- Three ids were RENAMED where the behaviour they assert changed (`…_warns` → `…_exits_3`,
  `…_does_not_set_metadata` → `…_writes_no_job`, `…_still_readable_but_deprecated` →
  `…_is_ignored_with_a_warning`): same coverage, honest names, no deletion.
- Two test edits sit outside their class's list because a product fix compelled them:
  `test_job_evidence.py` (catalog) and `test_provider_evidence_integration.py` (an
  absent-field assertion the closed schema forbids). Both in .agent/decisions.md.
- D3/D12 are quarantines, not fixes: 11 skips, each with a reason + backlog ref. plan.md
  is reviewer-authored and cmp-verified, so it stays exactly as dictated.

## Next
Reviewer verdict on R2; then the integration-gate round.
