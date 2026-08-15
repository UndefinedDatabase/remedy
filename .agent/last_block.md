── STEP R6/13 — F083 CI self-check — RECORD R5, REGISTER FOUR FINDINGS, REPAIR THE RUNNER ──

Goal:
  Record the R5 PASS, register the four findings its review produced — three of
  them defects in code the reviewer itself authored — and repair all three in the
  stage runner: anchor the run at the repository root, make a run in which no
  stage ran RED, and replace a guard assertion that cannot fail with one that
  can. The CLI seam moves one round later; the map is repaired in this same block
  because this round's scope is not the one the map describes (R-0455).

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r6.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R5-BLOCK appended at EOF, ONE commit.
  C2   `.agent/live_review.md` — FINDINGS appended at EOF, ONE commit.
  C3   `.agent/live_review.md` — the STEPS pair, ONE commit.
  C4   `packages/orchestration/ci_run.py` and `tests/orchestration/test_ci_run.py`,
       all six repair pairs plus the test append, ONE commit.
  C5   `.agent/live_review.md` — LANDED appended at EOF, ONE commit.
  C6   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C7   `.agent/handoff.md`, the handback, alone.

BASE: 81af8a98. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 81af8a98. If it does NOT, stop and hand off.

TRANSPORT: the scratchpad original of THIS block is at
`.remedy-wt/.cache/f083-r6/f083-r6.md`, which `.gitignore` drops. C0a is a byte
COPY of it — do not retype, reflow or strip anything. `cp` is denied in this
session class: copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The authored units are, listed: two EOF appends
(GATE-R5-BLOCK, FINDINGS), one further EOF append (LANDED), one REWRITE pair in
`.agent/live_review.md` (STEPS-FROM → STEPS-TO), five REWRITE pairs and one
end-of-file append in the two code files, and one whole-file replacement (PLAN).
No numeral is stated for that list — the list IS the statement (R-0402).

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r6.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `packages/orchestration/ci_run.py`,
     `tests/orchestration/test_ci_run.py`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `apps/`, `scripts/`, `docs/` and
     `packages/orchestration/ci_stages.py` stay EMPTY in the range diff — this
     round repairs the runner and touches neither the stage table nor its tests.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice contains an instruction
     addressed to you about the file it lands in (R-0450).
  3. C1 before C2, C2 before C3, C3 before C4, C4 before C5. Push after C7.
     Create NO pull request. This round adds NO worktree; `git worktree list` is
     one line throughout. No red-proof is ordered: the reviewer measured both
     repaired behaviours directly against the pre-repair code at 81af8a98 and the
     measurements are recorded in R-0456 and R-0457, so ordering a mutation would
     re-prove what the findings already carry (R-0327).
  4. Nothing registers the runner elsewhere: no catalog entry, no
     `COMMAND_HANDLERS` table, no import from another module. That seam is R7's.
  5. Env-var assignment (`VAR=x cmd`, `env VAR=x cmd`, `export VAR=x; cmd`) is
     denied in this session class, as is `cp`, `$?` inside `$(...)`, and process
     substitution. Capture real exit codes as `bash -c '<cmd>; echo "REAL_EXIT=$?"'`
     and use `python3 -` heredocs for counting, hashing and byte comparison.

--- BEGIN SLICE GATE-R5-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R5 — PASS on execution, with FOUR findings registered below. Verification tier: the live-state contract reader, the two live-state readers and the canary, all re-run by the reviewer at the round's head, plus ruff and both orchestration test files, and an independent re-derivation of every authored-text proof out of the committed git objects; no full-suite claim is made. The worker's execution was exact and its declaration discipline held for the ninth consecutive round: every slice was applied byte-verbatim, every ordered gate was run and reported with a real value, and the one defect it found in the reviewer's own text — the plan naming two future rounds where the map allows one — was declared before the reviewer read the diff rather than silently repaired. TRANSPORT held: the scratchpad `.remedy-wt/.cache/f083-r5/f083-r5.md`, `.agent/authored/f083-r5.md` and `.agent/last_block.md` are all sha256 54bd00a70d792420fe7ff66966dd284be2ddeb6a36848729bf29031aef4c8f04, 22102 bytes, 382 lines, three-way byte-equal, and the measured 382 equals the block's declared footer. C1's prefix property holds from the git blobs, 155450 B to 158478 B, with a tail byte-equal to `b"\n" + GATE-R4-BLOCK` extracted by marker from the COMMITTED authored file, and a `2 0` numstat. C2's REWRITE pair holds in both directions, with the three ordered section literals counting 1, 1 and 0 exactly as ordered, and the substring the dashboard contract reads still present — that contract is green at 70 collected, 70 passed, exit 0. C3's two new files were read back OUT of 8ab928aa and byte-equal their slices: `packages/orchestration/ci_run.py` sha256 1eab0b140529e05c…, 3257 bytes, 94 lines, and `tests/orchestration/test_ci_run.py` sha256 cbe857b3afa99954…, 2517 bytes, 81 lines, both added with a 0 deletion column. Both run green in the PRIMARY checkout: ruff over the two paths exits 0 with "All checks passed!", the two orchestration test files collect 13 and pass 13 at exit 0, and `packages.orchestration.ci_run` imports from the primary checkout path, so the green is the committed code's (R-0337). C4's plan byte-equals PLAN at sha256 8937d73f5badbdc1…, 35 lines, `## Goal` and `## Next Steps` present, no `- [ ]` line. The change set is the seven ordered paths and nothing else. Insertions 382 · 291 · 2 · 6 · 175 · 17, with the handback's own 164 measured after the fact, none over 500. The open set at HEAD is 83 registered, 0 resolved, max R-0455, next free R-0456, no duplicate id — unchanged from BASE, as ordered. The integrity gate reports passed true, fail_count 0, check_count 5, every named check pass; resource safety and the integrity-gate tests together are 36 passed exit 0, and the canary is 42 passed exit 0. What the ordered gates could not catch is what the findings below carry: every gate this block wrote was a gate about TRANSPORT and SHAPE, and none of them asked whether the runner is correct. It is not, in three ways, and all three are the reviewer's own authored text landing unexamined — which is the R-0220 class, a green gate that is not a working feature, arriving in the round that first gave this feature executable code.
--- END SLICE GATE-R5-BLOCK ---

--- BEGIN SLICE FINDINGS --- (APPEND to .agent/live_review.md, C2, with exactly one blank line between the file's current last line and the first line of this slice)
- R-0456 — Medium, THE STAGE RUNNER TAKES A REPOSITORY ROOT AND THEN RUNS PYTEST WHEREVER THE CALLER HAPPENS TO STAND. Found by the REVIEWER while reviewing R5. `run_ci_stage` accepts `repo_root` and hands it to `stage_command`, which uses it for exactly one thing: building the absolute path of `scripts/remedy_pytest_runner.py`. The run itself is `subprocess.run(command, check=False)` in `_run_via_subprocess`, with no `cwd`, and `pytest_argv_for_stage` returns `["-m", <expression>, "-q"]` — a MARKER selection carrying no path. `pyproject.toml` `[tool.pytest.ini_options]` sets `pythonpath` and `markers` and no `testpaths`, so pytest with no path argument collects from the process's working directory. Measured by the reviewer at 81af8a98, the same marker expression run twice with only the cwd differing: from the repository root, `-m "smoke and not real_ollama" --collect-only -q` reports `23/17020 tests collected (16997 deselected)` at exit 0; from `tests/orchestration`, the identical command reports `4/10729 tests collected (10725 deselected), 10 errors` at exit 2. So what a stage MEANS is decided by the caller's working directory — in the one feature whose stated purpose is that there is a single source of truth for what CI means (T2_F083). Medium, because the failure is silent in the direction that matters: a working directory whose smaller collected subset happens to pass returns exit 0, and the summary the CLI will print calls that stage green. The stage table is not implicated; `ci_stages.py` is correct and this is entirely the runner's. Fix: `_run_via_subprocess` takes the root and passes `cwd=`, the injected `run_command` signature widens to carry it so a test can pin the anchor, and `run_ci_stage` passes the same `repo_root` it already uses to find the script. OPEN.

- R-0457 — Medium, THE AGGREGATE EXIT CODE REPORTS GREEN FOR A RUN IN WHICH NO STAGE RAN AT ALL. Found by the REVIEWER while reviewing R5. `ci_exit_code` is `0 if all(r.exit_code == 0 for r in results if r.ran) else 1`. The generator is EMPTY whenever no result has `ran` True, `all()` over an empty iterable is True, and the function therefore returns 0. Measured by the reviewer at 81af8a98 against the committed code: `ci_exit_code(())` returns 0, and `ci_exit_code((StageResult("excluded", False, None, 0.0, "not run by CI"),))` returns 0. The function's own docstring states "0 only when every stage that RAN ended green. A skipped stage is not a pass" — and the second sentence is false in exactly the case where no stage ran. This is reachable, not theoretical: the plan's next round adds `remedy ci --stage NAME`, and `excluded` is a stage name, so `remedy ci --stage excluded` is a spelled-out invocation that executes no test and exits 0. Medium, and not Low, because the entire feature is a claim about honest CI and an exit code of 0 that means "nothing ran" is indistinguishable — to a shell, to a hosted workflow, to the operator — from one that means "everything passed"; a hosted workflow gating a merge on that code would gate on nothing. Fix: green requires that at least one stage RAN, `ci_exit_code` returns 1 for a results tuple with no `ran` member, and a test pins both the empty tuple and the all-skipped tuple. OPEN.

- R-0458 — Low, A GUARD ASSERTION THAT CANNOT FAIL, WRITTEN TO FORBID A STRING THAT IS IN FACT PRESENT. Found by the REVIEWER while reviewing R5. The last line of `test_stage_command_goes_through_the_runner_and_carries_the_selection` in `tests/orchestration/test_ci_run.py` is `assert "pytest" not in command[1:2]`. `command[1:2]` is a one-element LIST, so `in` is element equality and not a substring test: the assertion asks whether that list contains the exact string `"pytest"`, which it cannot, because the line directly above already asserts that its single element equals `str(REPO_ROOT / PYTEST_RUNNER_SCRIPT)`. Measured by the reviewer at 81af8a98: `command[1]` is `/home/decodeux/Repos/remedy/scripts/remedy_pytest_runner.py`, `"pytest" in command[1]` is True — the path contains the very substring the line reads as forbidding — and the assertion as written evaluates True. The line therefore reads to a human as "we do not exec bare pytest" while proving nothing, and it is the exact shape R-0327's family names: a check whose colour is decided before it runs. Low: no production behaviour depends on it and the two assertions above it do the real work. Fix: assert the proposition that was meant and that a regression can actually violate — that the argv is not the `[python, "-m", "pytest", …]` shape the module docstring says shelling out would lose. OPEN.

- R-0459 — Low, THE PLAN NAMES TWO FUTURE ROUNDS WHERE THE MAP ALLOWS ONE. Declared by the WORKER in the R5 handback as its second deviation, with the disk evidence, before the reviewer read the diff — the declaration discipline working exactly as intended, and the reviewer rules on it here as asked. The condition at 81af8a98: the Steps section of `.agent/live_review.md` says "Another file may name at most the NEXT round — `.agent/plan.md` must, because AGENTS.md mandates its Next Steps section — and naming one round is not restating the map", while the `## Next Steps` section of `.agent/plan.md` carries two numbered items. AGENTS.md's plan.md contract requires a Next Steps section and sets no count, so the two texts do not contradict AGENTS.md — they contradict each other, which is the R-0447 class, a map stated in two places drifting, arriving in reviewer-authored text one round after R-0455 registered the same class for the same file pair. The reviewer rules for the tighter reading: the map is stated once, and any other file names the NEXT round only. Low, because no code, gate or claim depends on it, and because the plan carried this shape at BASE too, so R5 neither introduced nor widened it. Fix: the plan's Next Steps carries one item. OPEN.
--- END SLICE FINDINGS ---

--- BEGIN SLICE STEPS-FROM --- (the REWRITE pair's FROM, C3; six whole lines INSIDE the existing Steps paragraph, occurring exactly once in .agent/live_review.md. The line that follows it in the file — the one beginning `closure. Each round marks` — is NOT part of this pair and is not touched.)
stage runner over the existing pytest subprocess runner → R6 T001 the `remedy
ci` CLI seam and the summary table it prints → R7 T001 the per-stage selection
tests over a fixture tree and the parallelism measurement D2.5 defers → R8 T002
the determinism and budget stages plus the guard-test wiring → R9 T002 the
seeded-failure test per stage → R10 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R11 the integration gate → R12
--- END SLICE STEPS-FROM ---

--- BEGIN SLICE STEPS-TO --- (the REWRITE pair's TO, C3; replaces STEPS-FROM in place, seven whole lines, the rest of the paragraph untouched)
stage runner over the existing pytest subprocess runner → R6 T001 the runner
repairs R-0456 to R-0458 and the cwd anchor → R7 T001 the `remedy ci` CLI seam
and the summary table it prints → R8 T001 the per-stage selection tests over a
fixture tree and the parallelism measurement D2.5 defers → R9 T002 the
determinism and budget stages plus the guard-test wiring → R10 T002 the
seeded-failure test per stage → R11 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R12 the integration gate → R13
--- END SLICE STEPS-TO ---

--- BEGIN SLICE RUNNER-FROM --- (REWRITE pair FROM, C4, packages/orchestration/ci_run.py, two whole lines occurring exactly once)
def _run_via_subprocess(command: list[str]) -> int:
    return subprocess.run(command, check=False).returncode
--- END SLICE RUNNER-FROM ---

--- BEGIN SLICE RUNNER-TO --- (REWRITE pair TO, C4, replaces RUNNER-FROM in place)
def _run_via_subprocess(command: list[str], cwd: Path) -> int:
    """Run `command` ANCHORED at `cwd`, never at wherever the caller stands.

    A stage selects by MARKER and carries no path, and this repository sets no
    `testpaths`, so pytest collects from the working directory — without this
    anchor the caller's cwd decides what a stage means (finding R-0456).
    """
    return subprocess.run(command, check=False, cwd=cwd).returncode
--- END SLICE RUNNER-TO ---

--- BEGIN SLICE INJECT-FROM --- (REWRITE pair FROM, C4, one whole line occurring exactly once)
    run_command: Callable[[list[str]], int] = _run_via_subprocess,
--- END SLICE INJECT-FROM ---

--- BEGIN SLICE INJECT-TO --- (REWRITE pair TO, C4, replaces INJECT-FROM in place)
    run_command: Callable[[list[str], Path], int] = _run_via_subprocess,
--- END SLICE INJECT-TO ---

--- BEGIN SLICE CALL-FROM --- (REWRITE pair FROM, C4, one whole line occurring exactly once)
    exit_code = run_command(stage_command(stage, repo_root))
--- END SLICE CALL-FROM ---

--- BEGIN SLICE CALL-TO --- (REWRITE pair TO, C4, replaces CALL-FROM in place)
    exit_code = run_command(stage_command(stage, repo_root), repo_root)
--- END SLICE CALL-TO ---

--- BEGIN SLICE EXIT-FROM --- (REWRITE pair FROM, C4, three whole lines occurring exactly once)
def ci_exit_code(results: tuple[StageResult, ...]) -> int:
    """0 only when every stage that RAN ended green. A skipped stage is not a pass."""
    return 0 if all(r.exit_code == 0 for r in results if r.ran) else 1
--- END SLICE EXIT-FROM ---

--- BEGIN SLICE EXIT-TO --- (REWRITE pair TO, C4, replaces EXIT-FROM in place)
def ci_exit_code(results: tuple[StageResult, ...]) -> int:
    """0 only when a stage actually RAN and every stage that ran ended green.

    A run in which NOTHING ran is red: `all()` over the empty selection is True,
    so the plain reading reports an invocation that executed no test — every
    stage skipped, or no stage at all — as a passing CI (finding R-0457).
    """
    ran = [result for result in results if result.ran]
    return 0 if ran and all(result.exit_code == 0 for result in ran) else 1
--- END SLICE EXIT-TO ---

--- BEGIN SLICE ASSERT-FROM --- (REWRITE pair FROM, C4, tests/orchestration/test_ci_run.py, one whole line occurring exactly once)
    assert "pytest" not in command[1:2]
--- END SLICE ASSERT-FROM ---

--- BEGIN SLICE ASSERT-TO --- (REWRITE pair TO, C4, replaces ASSERT-FROM in place)
    assert command[1:3] != ["-m", "pytest"]
--- END SLICE ASSERT-TO ---

--- BEGIN SLICE LAMBDAS-FROM --- (REWRITE pair FROM, C4, tests/orchestration/test_ci_run.py; three SEPARATE whole lines, each occurring exactly once, listed here in file order and replaced one for one by the three lines of LAMBDAS-TO)
        run_command=lambda command: 0,
        run_command=lambda command: 124,
        run_command=lambda command: calls.append(command) or 0,
--- END SLICE LAMBDAS-FROM ---

--- BEGIN SLICE LAMBDAS-TO --- (REWRITE pair TO, C4; the three replacement lines in the same order — line 1 replaces line 1 of LAMBDAS-FROM, and so on. These three lines are NOT contiguous in the target file.)
        run_command=lambda command, cwd: 0,
        run_command=lambda command, cwd: 124,
        run_command=lambda command, cwd: calls.append(command) or 0,
--- END SLICE LAMBDAS-TO ---

--- BEGIN SLICE TESTS-APPEND --- (APPEND to tests/orchestration/test_ci_run.py, C4, as post = pre + b"\n\n" + this slice, so exactly two blank lines separate it from the file's current last line)
def test_the_stage_run_is_anchored_at_the_repository_root():
    seen = []

    def record(command, cwd):
        seen.append(cwd)
        return 0

    run_ci_stage(
        ci_stage_by_name("fast"),
        REPO_ROOT,
        run_command=record,
        monotonic=lambda: 0.0,
    )
    assert seen == [REPO_ROOT]


def test_a_run_in_which_nothing_ran_is_not_green():
    skipped = StageResult("excluded", False, None, 0.0, "not run by CI")
    assert ci_exit_code(()) == 1
    assert ci_exit_code((skipped,)) == 1
--- END SLICE TESTS-APPEND ---

--- BEGIN SLICE LANDED --- (APPEND to .agent/live_review.md, C5, with exactly one blank line between the file's current last line and the first line of this slice)
Landed: R-0456 — the stage run is anchored at `repo_root` via `cwd=`, the injected runner signature carries it, and a test pins that the runner receives the root; C4.
Landed: R-0457 — `ci_exit_code` returns 1 when no stage ran, with the empty and all-skipped tuples both pinned by a test; C4.
Landed: R-0458 — the assertion that could not fail is replaced by one on the argv shape a regression can actually produce; C4.
Landed: R-0459 — `.agent/plan.md` names one future round; C6.
--- END SLICE LANDED ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C6)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0460. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0459 registered on this branch.
`.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R6 records the R5 PASS, registers R-0456 to R-0459 and repairs the three runner
defects the R5 review found: the run is anchored at the repository root, because
a marker selection carries no path and pytest otherwise collects from wherever
the caller stands; a run in which no stage ran is red rather than green; and a
guard assertion that could not fail is replaced by one that can.

## Next Steps
1. R7 adds the `remedy ci [--stage NAME] [--json]` CLI seam Q8 names — the
   catalog group, the entry and a `COMMAND_HANDLERS` module — and the summary
   table it prints, which states the accepted `standard`/`smoke` double-run.

## Risks
- No test yet runs a stage for real: the injected runner buys speed at the cost
  of never proving the subprocess seam end to end, and this round narrows that
  gap only as far as the cwd anchor. R7 must land one real stage invocation.
  `fast` still rests on a single 391.8 s reading.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C7.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 81af8a98.
 3. TRANSPORT, bytes read in Python: sha256, byte count and line count of
    `.remedy-wt/.cache/f083-r6/f083-r6.md`, `.agent/authored/f083-r6.md` and
    `.agent/last_block.md`; whether all three byte strings are EQUAL; whether the
    measured line count equals this block's declared footer count.
 4. C1 and C2 PREFIX PROPERTY, each over `<commit>^..<commit>`: `pre` is a prefix
    of `post`, and `post[len(pre):]` equals `b"\n" + <slice>` byte-for-byte, each
    slice extracted from the COMMITTED `.agent/authored/f083-r6.md` by its
    markers. Report both numstats; each deletion column must be 0.
 5. C3 REWRITE PAIR, both slices extracted from that same committed file: over
    the WHOLE `.agent/live_review.md` at C3, STEPS-FROM occurs 0x and STEPS-TO
    occurs 1x. Then count these three literals over the whole file, each wholly
    on ONE line of the TO so no count is defeated by a line break:
    `repairs R-0456 to R-0458 and the cwd anchor` must be 1,
    `R11 T003 the hosted workflow files` must be 1, and
    `R10 T003 the hosted workflow files` must be 0. Confirm the substring `Steps`
    still occurs. Report the C3 numstat.
 6. C4 CODE, each file read back OUT of the commit: report the sha256, byte count
    and line count of `packages/orchestration/ci_run.py` and
    `tests/orchestration/test_ci_run.py`, and the numstat of each. Then count
    these literals as SUBSTRINGS over the committed bytes of each file and report
    every measured number. Per-line counting is NOT ordered here, because the
    `def ci_exit_code(...)` signature line is deliberately common to EXIT-FROM and
    EXIT-TO and a whole-line zero-gate over it would be unsatisfiable by
    construction. In `packages/orchestration/ci_run.py`, these must be 0:
    `check=False).returncode` · `Callable[[list[str]], int]` ·
    `stage, repo_root))` · `A skipped stage is not a pass` ·
    `for r in results if r.ran`. In the same file, these must be 1:
    `check=False, cwd=cwd).returncode` · `Callable[[list[str], Path], int]` ·
    `stage_command(stage, repo_root), repo_root)` ·
    `ran = [result for result in results if result.ran]` · `cwd: Path) -> int:`.
    In `tests/orchestration/test_ci_run.py`, these must be 0:
    `"pytest" not in command[1:2]` · `lambda command:` — note the colon, which is
    what distinguishes it from the repaired `lambda command, cwd:`. These must be
    1: `command[1:3] != ["-m", "pytest"]` ·
    `def test_the_stage_run_is_anchored_at_the_repository_root` ·
    `def test_a_run_in_which_nothing_ran_is_not_green`. And `lambda command, cwd:`
    must be 3.
 7. C4 TESTS-APPEND, from the committed `tests/orchestration/test_ci_run.py`:
    report whether the file's bytes END with the TESTS-APPEND slice extracted from
    the committed authored file (True/False), and whether the two lines
    immediately before that slice are both empty (True/False).
 8. C4 RUNS GREEN, each command separately, exit code from the process object,
    never a pipe (R-0438), both paths resolved on disk first.
    `python3 -m ruff check packages/orchestration/ci_run.py
    tests/orchestration/test_ci_run.py` — report the exit code [reviewer measured
    0 at 81af8a98 before the repair]. `python3 -m pytest
    tests/orchestration/test_ci_run.py -q` — report collected count and exit code
    [the reviewer expects 8: the 6 that exist at BASE plus the 2 TESTS-APPEND
    adds; report what you MEASURE]. `python3 -c "import
    packages.orchestration.ci_run as m; print(m.__file__)"` — must resolve inside
    the PRIMARY checkout (R-0337). Repo-wide `ruff check` is RED on main and is
    NOT a gate here (R-0364).
 9. THE STAGE TABLE STILL RUNS, untouched by this round: `python3 -m pytest
    tests/orchestration/test_ci_stages.py -q`, report collected count and exit
    code [reviewer measured 7 collected, 7 passed, exit 0 at BASE].
10. C6 PLAN byte-equals the PLAN slice as a whole file — report sha256 and line
    count, under 50, `## Goal` and `## Next Steps` present, no `- [ ]` line, and
    the count of numbered items under `## Next Steps`.
11. CHANGE SET, measured BEFORE the handoff is written into C7, so it lists six
    paths and `.agent/handoff.md` is the seventh and last:
    `git diff --name-only 81af8a98..HEAD`. Report the full list and its count.
    Restricted to `apps/`, `scripts/` and `docs/` it must be EMPTY, and
    `packages/orchestration/ci_stages.py`, `tests/orchestration/test_ci_stages.py`
    and `.agent/f083_inventory.md` must not appear. Report both as measured lists.
12. VERIFICATION, each command run separately, exit code from the process
    (R-0438), every path resolved on disk first. Report collected count and real
    exit code for EACH, with the reviewer's BASE reading in brackets: `python3 -m
    pytest tests/ui_server/test_dashboard_contract.py -q` [70/70, exit 0] — the
    reader of both files C3 and C6 rewrite; `python3 -m pytest
    tests/regression/test_resource_safety.py -q` [21, exit 0]; `python3 -m pytest
    tests/orchestration/test_integrity_gate.py -q` [15, exit 0]; and the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q` [42/42, exit 0].
    `tests/docs/` is NOT a gate here: no `docs/roadmap/**` path is in the change
    set, which is what triggers it.
13. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` lines and
    `^Landed: R-\d+ — ` lines; report all three, the registered-minus-done
    difference, max id, next free id, any duplicate id. The reviewer measured 83 /
    0 / 0 with max R-0455 at BASE and expects 87 / 0 / 4 with max R-0459 here.
    Report what you MEASURE.
14. INTEGRITY GATE, in Python because the `remedy` CLI is denied in this session
    class (R-0408): `python3 -c "from packages.orchestration.integrity_gate
    import run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every named check's status.
15. Insertions (`+` column only) for C0a, C0b, C1, C2, C3, C4, C5, C6 — report
    each; none over 500. C0b is a verbatim single-`.agent/`-file rewrite, exempt
    by the AGENTS.md counting rule; report its number anyway. C7's own count
    cannot exist inside C7 (R-0149): report it in your final message.

The push result, the post-C7 clean-tree reading and the open-PR list come into
existence AFTER C7, so per R-0449 and R-0452 they are NOT ordered into that file:
run `git push -u origin feature/f083-ci-self-check` after C7, create no pull
request, and report all three in your final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as
C7 — feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next action, R7's CLI seam and summary table.
C7 cannot table its own SHA (R-0371, R-0149); say so rather than inventing one.
Repeat this line verbatim as the Fortschritt line:

Fortschritt: 22 % (F083 beansprucht · R1 bis R5 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · Stage-Tabelle und Stage-Runner als Code gelandet · Runner-Defekte R-0456 bis R-0458 repariert · noch keine CLI, kein Summary, keine hosted workflows) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, end. Do not
widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 346 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
