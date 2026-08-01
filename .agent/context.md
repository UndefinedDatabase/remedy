# Context — F062 Product smoke as the closing gate (Tier 1)

## Active Branch
`feature/f062-product-smoke`
Base commit: main after PR #173 merge (paydown-0801), `b836d364`

## Steps (round map)
R1 (SPLIT): claim `[~]` + state reset → T001 product-smoke standard
block registered into the DoD compiler's seam, app_starts check, the
not-applicable path, and two real fixture mini-apps (clean start /
green tests with broken startup).
R2: T002 core_paths_respond + path extraction hand-off + fixtures.
R3: T003 clean_console + pattern list + teardown-always; then the
integration gate. R4: closure — its own round.

## Scope
`packages/orchestration/**` (the product-smoke block and its
registration into the F061 standard-check seam),
`tests/orchestration/test_product_smoke.py` plus the fixture apps
under `tests/`, `docs/roadmap/STATUS.md` (claim line only), and
`.agent/` state. Nothing beyond.

## Gates (round verification, pytest)
python3 -m pytest tests/orchestration/test_product_smoke.py -q  T001 gate
python3 -m pytest tests/docs/ -q                                docs gate
python3 -m pytest tests/cli/test_golden_path.py -q              canary
Resource safety: everything runs through these pytest wrappers; no
unbounded subprocess fan-out from smoke or fixture tooling — every
fixture app is started through the harness verbs and torn down on
every outcome.

## Constraints
- The smoke ORCHESTRATES the F007 harness verbs (start, probe,
  log capture, stop). Harness process semantics are not touched.
- NO browser dependency in v1 — HTTP level only; a diff adding one is
  rejected at self-review (feature file, Orchestrator brief).
- Teardown ALWAYS runs; no zombie process on any outcome, including
  failure and the retry path.
- One retry of app_starts after a short backoff, recorded as
  "passed on retry" (visible risk, A9).
- Port conflict = start failure reported with the harness's own
  reason; never re-implemented here.
- No runtime configured/detected → "smoke: not applicable (no runtime
  configured)", non-gating and never silently green (P6).
- Fixtures are REAL mini-apps in the test tree, not harness mocks.
- Reviewer-authored texts under .agent/authored/ are applied by copy
  and sha256-verified before use; never hand-edited.
- Commits stay under 500-line diffs (AGENTS.md).
- context.md satisfies its FULL test reader list: a "Steps" section,
  "## Active Branch" with a feature/ slug, a roadmap F-id, and this
  pytest/resource line (R-0162; reader rule in
  planner_reviewer_prompt.md §4 item 11).

## Do not touch
Browser automation, visual comparison, the harness's process
semantics. docs/roadmap/ROADMAP.md; STATUS entries other than the
F062 claim line. Tier-11 verification depth.
