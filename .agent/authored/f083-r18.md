# F083 R18 — the budgets stage, the R-0468 ruling, the determinism shape

SPLIT round. This round writes PRODUCTION CODE, so it is executed by the worker
and gated by the reviewer; nothing in it is self-certified.

Base: `git rev-parse HEAD` MUST print ab1d2344 before the first commit. If it
does not, stop and report — every gate below is measured against that base.

Round type and numbering, per R-0481: R16 was the record round, R17 the repair
round, and this is R18, the next engineering round.

## What this round is for

`.agent/plan.md` names three items and this round does all three.

1. The `budgets` STAGE that T2_F083's Design section asks for and that
   `CI_STAGES` does not have. Its ceilings are DOCUMENTED and its check is a
   test, so a ceiling that only holds when someone remembers to look is not
   what lands.
2. A ruling on R-0468, the twenty-six ruff errors the repository stands at while
   no CI stage runs a linter.
3. The determinism stage's shape, settled as a DECISION rather than left open.

## The two DECISIONS this block rules, both reversible by any later relay

**DECISION F083 D4 — determinism does NOT become a stage of its own.**
Measured at R11 and recorded in `.agent/f083_inventory.md` `## Q9`: the glob
`tests/orchestration/test_run_manifest_*.py` matches forty-five files collecting
850 tests, and a Python set operation over collected node ids puts all 850 inside
the 12579 ids `standard` selects, with 0 ids outside. A `determinism` stage would
therefore either re-run 850 tests `standard` has already run, or require
`standard`'s expression to be narrowed — and narrowing it is a marker-semantics
change, which T2_F083's Do-not-touch list forbids. Chosen: the determinism suite
stays inside `standard`, and the absence is DOCUMENTED where a reader would
search for it, in the `ci_stages` module docstring, in the repository's own
"Remedy deliberately does not X because Y" idiom (AGENTS.md, Code
Discoverability Conventions). Alternatives considered and rejected: a new
`determinism` marker (marker-semantics change, forbidden); a path-selected
determinism stage (buys nothing `standard` does not already do, and doubles 850
tests' wall cost). Reverse by narrowing `standard` and adding the stage in the
same commit. T2_F083's Design section is amended by this block to say so, per
docs/agents/planner_reviewer_prompt.md §4 item 7.

**DECISION F083 D5 — the twenty-six ruff errors are RATCHETED, not fixed here.**
R-0468 measured 26 errors at the repository root under the repo's own
`pyproject.toml`, none of them from this branch. Fixing them is a mass edit
across files this feature is not otherwise touching, which AGENTS.md Scope
Control forbids as its own activity. Chosen: `budgets` carries a documented lint
CEILING of 26 that fails when the count RISES, so the debt is frozen and visible
instead of silently growing, and the ceiling is a ratchet — the number may only
be lowered, never raised. Alternatives considered and rejected: fix all 26 now
(scope drift, and 25 are auto-fixable import hygiene that would churn the suite
that was just stabilised); leave lint out of CI entirely (leaves the feature's
own Acceptance line green while `ruff check .` is red). Reverse by lowering the
ceiling to 0 and fixing the errors in a branch of their own. One of the 26 is not
import hygiene at all but a genuine runtime defect, and it is registered below as
its own finding rather than frozen without comment.

## Slice convention

Every slice is delimited by its own `--- BEGIN SLICE <NAME> ---` and
`--- END SLICE <NAME> ---` markers, which are TRANSPORT ONLY and NEVER reach a
target file. A slice's content begins on the line AFTER its BEGIN marker and
ends on the line BEFORE its END marker, newline included. The slices carried
here are named RECORD-R17 and PLAN. A slice with no FROM: line is an EOF-APPEND:
its bytes are appended to the end of the named file and nothing already in that
file is edited. Extract both slices programmatically from the COMMITTED
`.agent/authored/f083-r18.md` by their markers — never by retyping.

--- BEGIN SLICE RECORD-R17 --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R17-REPAIR — PASS. The reviewer re-ran the round's gates itself at ab1d2344 from the repository root and every one reproduces. TRANSPORT: `.agent/authored/f083-r17-repair.md` and `.agent/last_block.md` are byte-equal at sha256 7e27fc530221b2302ee225f4bc65a761f5f2d510ae6f3015a1e51e7ab2dfc3a9 over 17638 bytes and 176 lines, matching the handback's declared digest exactly. C1's prefix property holds: `.agent/live_review.md` at 8c9290dd is 243969 bytes, at 0cbeae03 is 249551 bytes, the former prefixes the latter, and the 5582-byte tail is byte-EQUAL to the RECORD-R16REC slice extracted from the COMMITTED authored file by its own markers — with numstat `4 0`, so nothing already in the file was edited. No marker line leaked: `.agent/plan.md` contains zero `--- BEGIN SLICE` occurrences and the one occurrence in `.agent/live_review.md` is present at 8c9290dd, before C1 ran, so it is quoted finding text and not transport residue. C2's `.agent/plan.md` byte-equals its PLAN slice at 2424 bytes and sha256 8a06dd76b2fc2be0c6b65a9e971dc5470110f012c5bc1100d28d562a89b27c5d, 41 lines under the 50-line cap, `## Goal` and `## Next Steps` both present, 0 `- [ ]` lines; all four of the plan's text gates hold at HEAD — `R18 has not started` PRESENT, `R-0478, R-0479 and R-0480` PRESENT, `the two findings it produced` ABSENT, `R16 has not started` ABSENT — which is precisely the R-0481 repair the round existed to perform. The range gate holds: `git diff --name-only 0d9c72e0..HEAD -- packages/ apps/ tests/ scripts/ docs/` prints NOTHING, so the round wrote no production code, exactly as declared. Per-commit numstat read from `git log --numstat` reproduces the handback's table to the line: 176/0, 70/65, 4/0, 9/7 and 65/83, one path each, no insertion count near 500. Gates taken BEFORE any pytest command, honouring R-0479: `python3 -m ruff check .` ends `Found 26 errors.` at exit 1, EQUAL to the `## Q10` baseline, and the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338, with all five checks pass. Then the suites, each unpiped with its exit read from its own process: the four CI suites at 35 passed, exit 0, and the verification quartet with the canary at 148 passed, exit 0 — 70 + 21 + 15 + 42, matching the handback's per-suite claims in their sum. The open set recomputes mechanically from the record to 109 registered, 6 `Done:`, 0 `Landed:`, 103 open, max R-0481, no duplicate id — exactly what the handback declared. Both declared deviations are honest and neither is a finding: the discarded gate-10 invocation produced no reading and none was reported from it, and the 97-line handoff carries its DECISION D15 stated cause naming the mandated content that overran. REVIEWER CONDUCT, recorded because it is the lesson of this gate: the reviewer's own first re-run of the quartet named `tests/ui_contracts/test_dashboard_contract.py`, which does not exist — pytest exited 4 with `file or directory not found` and ran nothing. The block under review had ordered `tests/ui_server/test_dashboard_contract.py`, correctly; the wrong path was the reviewer's, it was caught because exit 4 is not exit 0, and the quartet was re-run at the ordered paths. It is written down because a reviewer who had read that exit code as a pass would have certified a gate that never ran, which is the R-0438 class exactly. One new finding is registered below; it is a pre-existing repository defect this round's lint reading surfaced, not a defect of R17.

- R-0482 — Medium, A GUARD THAT REFUSES AN UNSUPPORTED INJECTION RAISES `NameError` INSTEAD OF THE ERROR IT NAMES, BECAUSE THE MESSAGE INTERPOLATES AN UNDEFINED NAME. Measured at ab1d2344 by the reviewer: `python3 -m ruff check .` reports `F821 Undefined name MISSING_SEAM` at `packages/orchestration/gauntlet_injection.py:286:20`, and `grep -rn "MISSING_SEAM" packages/ tests/` returns exactly one line — that same use site. The name is referenced and defined nowhere, in the repository or in the test tree. The site is `check_injections_supported`, whose whole purpose is to "refuse an order whose declared injections cannot be driven honestly": for a name in `BLOCKED_INJECTIONS` it builds `f"{name} cannot be injected at {BLOCKED_INJECTIONS[name]}: {MISSING_SEAM}"` and hands it to `MissingSeamError`. The f-string is evaluated BEFORE the exception is constructed, so that branch raises `NameError: name 'MISSING_SEAM' is not defined` and the `MissingSeamError` the caller is written to catch is never constructed at all. The unknown-injection branch immediately below it is unaffected and does raise correctly, which is why the defect is invisible from the outside: the guard appears to work, and fails only on the one input class it was written for. Medium and not High: no false GREEN exists on disk, the branch is not reached by any current test — no test in the tree names `MISSING_SEAM` — and the failure is loud rather than silent when it does fire. Not Low, because a guard whose refusal path is itself broken is worse than no guard, and because a caller catching `MissingSeamError` around this call gets an uncaught `NameError` through it. This finding belongs to F083 only in the sense that F083's lint reading is what surfaced it: it is ONE of the twenty-six errors DECISION F083 D5 freezes at the ceiling, and D5 freezes it deliberately rather than fixing it here, because the fix is a production change in an unrelated module and AGENTS.md Scope Control forbids it as a "while I'm here" edit. The fix — define the constant or drop the interpolation — belongs to a branch of its own and is not ordered by this round. OPEN.
--- END SLICE RECORD-R17 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C6)
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
--- END SLICE PLAN ---

## Change — exactly these paths, nothing beyond them

**C2 — the ceilings module and its tests.** New
`packages/orchestration/ci_budgets.py`: a frozen `BudgetCheck` dataclass carrying
`name`, `ok`, `observed`, `ceiling` and `detail`; a module constant
`LINT_ERROR_CEILING = 26` whose one-line WHY comment sits directly above it and
names DECISION F083 D5, finding R-0468 and the ratchet rule; a
`parse_ruff_error_count(output: str) -> int` that returns the integer from ruff's
own final `Found N errors.` line, returns 0 when the output carries
`All checks passed!`, and raises `ValueError` naming what it could not parse
otherwise; and a `check_lint_ceiling(observed: int) -> BudgetCheck` that is `ok`
when `observed <= LINT_ERROR_CEILING`. The module RUNS NOTHING at import — same
rule the `ci_stages` docstring already states for the stage table. New
`tests/orchestration/test_ci_budgets.py`: parse cases for `Found 26 errors.`, for
`All checks passed!`, and for unparseable output; ceiling cases at 25, 26 and 27;
and ONE live check, marked `@pytest.mark.subprocess`, that runs
`[sys.executable, "-m", "ruff", "check", "."]` from the repository root with
`capture_output=True`, parses its own output and asserts the count is at or below
the ceiling — the repository's own `pyproject.toml`, no substituted flag, no
`--isolated` (finding R-0463).

**C3 — the measurement.** Append `## Q12` to `.agent/f083_inventory.md`, in the
shape `## Q10` and `## Q11` already use: three samples of the budgets selection's
wall time, each its own process, each with the exit code read from that process,
the driver command recorded verbatim, and the slowest sample named as the
measured maximum. Measure the SELECTION, which needs no stage to exist yet:
`[sys.executable, "-m", "pytest", "-m", "not real_ollama", "-q", <the paths
listed in C4>]` run from the repository root. Record real numbers only; a sample
that fails is recorded with its failure, not dropped.

**C4 — the stage table.** `packages/orchestration/ci_stages.py`: add
`test_paths: tuple[str, ...] = ()` as the LAST field of `CiStage`, with a `#:`
comment saying a stage carrying paths selects BY PATH and its marker expression
only excludes the live provider; add the `budgets` entry between `smoke` and
`excluded` with `marker_expression="not real_ollama"`, `runs_in_ci=True`,
`manual_command=""`, `test_paths` =
`tests/orchestration/test_scratch_file_guard.py`,
`tests/test_no_interactive_guard.py`, `tests/test_test_categories.py` and
`tests/orchestration/test_ci_budgets.py` — the guard suites that assert
REPOSITORY ceilings, which is why `tests/orchestration/test_budget_guard.py` is
NOT among them: it covers F018 job budgets, a runtime concept that shares the
word and nothing else — and `timeout_sec` computed by the
SAME rule the other budgets use — `ceil(2 * measured_max / 300) * 300` over the
C3 measurement; make `pytest_argv_for_stage` append `*stage.test_paths` after
`-q`; and add the DECISION F083 D4 deliberate-absence paragraph to the module
docstring, in the "Remedy deliberately does NOT ..." idiom already there.
`tests/orchestration/test_ci_stages.py`: add `"budgets"` to the expected name
tuple in run order; add the C3 measured maximum to `MEASURED_MAX_WALL_S`; amend
`test_pytest_argv_selects_the_expression_and_nothing_else` so it pins BOTH shapes
— a path-less stage's argv ends at `-q`, and `budgets`' argv is `-m`, its
expression, `-q`, then exactly its `test_paths` in order; and add one test
asserting every path in every stage's `test_paths` RESOLVES ON DISK relative to
the repository root, because a stage whose path has moved runs nothing and exits
4 (finding R-0438). `tests/orchestration/test_ci_stage_selection.py`: scope
`test_exactly_one_fixture_module_lands_in_two_ci_stages`,
`test_a_slow_only_module_is_selected_by_no_ci_stage`,
`test_no_ci_stage_ever_selects_a_live_provider_module` and
`test_no_test_in_this_repository_escapes_all_five_stages` to stages with
`runs_in_ci and not stage.test_paths`, and rename that last one so its name no
longer says "five stages"; its docstring states WHY a path-bearing
stage is excluded from the union — `not real_ollama` in a marker union would
report every uncovered test as covered, which is a false green of exactly the
kind this feature exists to detect.

**C5 — the rulings on disk.** Append DECISION F083 D4 and DECISION F083 D5 to
`.agent/decisions.md` in the file's existing entry shape. Amend
`docs/roadmap/features/T2_F083.md`: the Design bullet listing the stages loses
`determinism` from the stage list and gains a sentence recording D4 with its
measured evidence, and the Task slicing `T002` line is amended to say the
determinism stage was ruled out rather than built. Change nothing else in that
file; ROADMAP.md is not touched.

**C6** applies the PLAN slice. **C7** rewrites `.agent/handoff.md`.

## Constraints

1. Never work on `main`; never force-push; never amend, rebase or reset. No PR is
   created or merged by this round.
2. `.agent/live_review.md` is APPENDED to only. No committed text in it is edited.
3. No marker line reaches a target file. Both slices are extracted from the
   COMMITTED `.agent/authored/f083-r18.md` by their markers.
4. Marker SEMANTICS are not touched: no marker is added, removed or redefined in
   `pyproject.toml`, and no existing stage's `marker_expression` changes.
5. The twenty-six ruff errors are NOT fixed. Every file this round writes is
   ruff-clean under the repository's own config, so the count stays at 26.
6. The lint ceiling is not raised. If the live ceiling test goes red, that is the
   finding — report it and stop; do not edit the constant.
7. Gate ordering (R-0479): the lint reading and the integrity gate are taken
   BEFORE any pytest command runs in this round, and no reading is taken while a
   suite is running.
8. Any destructive or red-control check runs ONLY inside a disposable
   `git worktree`, which is removed before the handback (G5).
9. If any gate is red, stop at that gate, record its real output, and hand back.
   Do not widen the change set to route around it.

## Done when — every command run from /home/decodeux/Repos/remedy, each its own
## unpiped process, each exit code read from that process

1. `pwd` printed FIRST. `git status --porcelain` EMPTY before the first commit
   and before C7. `git worktree list` ONE line at round start and at handback.
   `.agent/STOP` ABSENT at both.
2. `git rev-parse HEAD` at round start EQUALS ab1d2344.
3. `.agent/authored/f083-r18.md` and `.agent/last_block.md` byte-equal, with
   their sha256 and byte count reported.
4. `.agent/live_review.md`: the pre-C1 content PREFIXES the post-C1 content, the
   tail byte-EQUALS the RECORD-R17 slice extracted from the committed authored
   file by its markers, and `git show --numstat` for that commit has deletion
   column 0.
5. `.agent/plan.md` byte-equals the PLAN slice; report its sha256, its line
   count (under 50), that `## Goal` and `## Next Steps` are present, and its
   count of `- [ ]` lines.
6. `python3 -m ruff check .` — report its final line and exit code. Expected
   `Found 26 errors.` at exit 1. Run BEFORE any pytest command.
7. The integrity gate, run BEFORE any pytest command (R-0408 — the property, not
   the tool): `python3 -c "from packages.orchestration.integrity_gate import
   run_integrity_checks, export_integrity_json; import json;
   print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
   `passed`, `fail_count` and `check_count`.
8. `python3 -m pytest tests/orchestration/test_ci_budgets.py -q` — report the
   passed count and exit code.
9. `python3 -m pytest tests/orchestration/test_ci_stages.py
   tests/orchestration/test_ci_stage_selection.py tests/cli/test_ci_cmd.py
   tests/orchestration/test_ci_run.py -q` — report the passed count and exit
   code. All four paths exist today; report any that does not rather than
   accepting exit 4 as a pass.
10. RED CONTROL for the ceiling, inside a disposable worktree at HEAD and nowhere
    else: lower `LINT_ERROR_CEILING` to 0 there and report whether
    `python3 -m pytest tests/orchestration/test_ci_budgets.py -q` goes RED, and
    which test id fails. Report the COLOUR, not a count. Remove the worktree and
    report `git worktree list` afterwards.
11. RED CONTROL for the path gate, in that same disposable worktree: point one
    entry of the `budgets` stage's `test_paths` at a path that does not exist and
    report whether the new resolves-on-disk test goes RED.
12. `python3 -m pytest tests/docs/ -q` — the docs-round gate, because C5 changes
    `docs/roadmap/**`. Report the passed count and exit code.
13. `python3 -m pytest tests/ui_server/test_dashboard_contract.py
    tests/regression/test_resource_safety.py
    tests/orchestration/test_integrity_gate.py tests/cli/test_golden_path.py -q`
    — the verification quartet and the canary. Report the passed count and exit
    code. If `test_typescript_compiles` fails on its FIRST run in a cold-cache
    worktree, that is R-0480 and it is reported, not repaired.
14. The open set, recomputed from `.agent/live_review.md` at HEAD: count every
    `^- R-\d+ — ` paragraph, every `^Done: R-\d+ — ` line, every
    `^Landed: R-\d+ — ` line; report registered, done, landed, open, the maximum
    id, the next free id, and whether any id repeats. Expected after C1: 110
    registered, 6 done, 0 landed, 104 open, max R-0482, next free R-0483.
15. `git diff --name-only ab1d2344..HEAD` — report the full path list. Nothing
    outside the paths this block names may appear.
16. `git log --numstat` over the round — report the insertion count of every
    commit. None may exceed 500.
17. `## Q\d` headings in `.agent/f083_inventory.md` at HEAD — report the count
    and the range. Expected Q1 through Q12.
18. Confirm in one sentence that no `git commit --amend`, `git rebase` or
    `git reset` was run this round (R-0477).

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and
round, branch, every commit SHA, a changed-files table per commit, the real
measured value of every gate above in an item-status table where each ordered
item appears exactly once with `done`, `skipped` or `deviated`, the open-findings
count, declared deviations with their causes, and the next expected action. If
the file exceeds 60 lines, carry a "Deviations, declared" line naming its line
count and the mandated content that caused the overage (DECISION D15). Repeat
this Fortschritt line verbatim as the handoff's last line:

Fortschritt: 58 % (F083 beansprucht · R1 bis R7 und R9 bis R17 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht, die Selektionstests und die gemessenen Stage-Budgets als Code gelandet · neu in R18: die budgets-Stage mit dokumentierter Lint-Decke, D4 schliesst eine eigene Determinismus-Stage aus, D5 friert die 26 ruff-Fehler auf einer Ratsche ein · noch offen: R-0480 (ui-Stage rot auf frischem Checkout mit kaltem npx-Cache) und T003 mit den hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt

Then `git push -u origin feature/f083-ci-self-check` and report its result, the
post-push `git status --porcelain` and the open-PR list in the round report.
