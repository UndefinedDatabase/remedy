# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0485. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R18 is closed PASS: the `budgets` stage, path-based stage selection, the
ratcheted lint ceiling, DECISION F083 D4 (no determinism stage) and DECISION
F083 D5 (the 26 ruff errors frozen, not fixed) are all on disk. R19 recorded
that verdict, registered R-0483 and R-0484 — both reviewer defects the worker
caught — and MEASURED the R-0480 question as `## Q13` of the inventory. R19
rules nothing.

## Next Steps
1. R20 rules on R-0480 from the `## Q13` data. If the cold-cache cause is
   confirmed, the options are warming the toolchain inside the stage, moving
   `test_typescript_compiles` behind the "UI toolchain absent locally" edge case
   the feature file already documents, or amending Acceptance. If Q13 shows the
   cause is something else, or is not reproducible, R-0480 is amended to say so
   before any fix is ordered. SPLIT round — the fix is production code.
2. T003 then remains: hosted workflow files calling the same entrypoint, the
   docs, and the runtime-budget documentation from the measured data.

## Risks
- R-0480's cause is a HYPOTHESIS, not a measurement. The npx cache is a per-user
  directory, so a fresh `git worktree` alone should not produce a cold one.
  Ordering a fix before Q13 answers this would spend a round proving the
  reviewer wrong.
- The lint ceiling is a RATCHET. Raising it to make a round green converts the
  one honest lint signal in this repository into decoration.
- R-0482 is a live `NameError` on a guard's refusal path, frozen under that
  ceiling rather than fixed, and belongs to a branch of its own.
