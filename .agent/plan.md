# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0483. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R17 is closed PASS and R18 recorded it. R18 built the `budgets` stage: `CiStage`
carries `test_paths`, the stage selects the standing guard tests by path, and
`packages/orchestration/ci_budgets.py` holds the documented lint ceiling. DECISION
F083 D4 ruled that determinism does NOT become a stage — the suite already sits
wholly inside `standard`. DECISION F083 D5 ruled R-0468 ratcheted at 26 rather
than fixed, and registered R-0482 for the one genuine runtime defect among them.

## Next Steps
1. R19 rules on R-0480: the `ui` stage is RED on a clean checkout with a cold npx
   cache, so T2_F083's Acceptance line "clean checkout: green" is not met today.
   The options are warming the toolchain inside the stage, moving
   `test_typescript_compiles` behind the documented "UI toolchain absent locally"
   edge case, or amending Acceptance. It is a SPLIT round.
2. T003 then remains: hosted workflow files calling the same entrypoint, the docs,
   and the runtime-budget documentation from the measured data.

## Risks
- The `budgets` stage deliberately RE-RUNS guard tests other stages already
  select. That overlap is intentional and is why the fixture-tree overlap and
  union properties now scope themselves to the marker-selected stages; a later
  round that folds path-bearing stages back into those properties reintroduces a
  false green, because a marker union that contains `not real_ollama` reports
  every uncovered test as covered.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path. It is frozen under the
  ceiling, not fixed, and belongs to a branch of its own.
