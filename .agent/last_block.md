── STEP R15 — T2_F083 CI self-check — SPLIT ROUND, PRODUCTION CODE ───────────
Goal:        Give every CI stage its own measured wall-clock budget, so `remedy
             ci` stops killing `standard` at the runner's 600-second default.
             First round since fb9ddf12 to touch production code: you execute,
             the reviewer gates, nothing here is self-certified.

Bundle:      SIX commits, in this order, with these exact subjects:
  C0a `docs(f083): save the R15 block verbatim` — THIS ENTIRE BLOCK, byte-
      verbatim, to `.agent/authored/f083-r15.md`.
  C0b `docs(f083): mirror the R15 block into last_block` — `.agent/last_block.md`
      becomes a byte-identical copy of that file.
  C1  `docs(f083): record the R14-REC PASS and rule DECISION F083 D3` — the
      RECORD-R14REC append at EOF of `.agent/live_review.md`, nothing else.
  C2  `fix(f083): budget each CI stage and stop standard being killed at 600s` —
      the S-slices below, all four code files in THIS ONE commit. Guard and
      change land together: the injected runner's signature widens, so a commit
      carrying one side leaves the other red.
  C3  `docs(f083): point the plan at the R16 budget stage` — `.agent/plan.md`
      replaced as a WHOLE FILE by the PLAN slice.
  C4  `docs(f083): write the R15 handback` — `.agent/handoff.md` alone.
Change:      Exactly these files, nothing else: under `.agent/`, `authored/
             f083-r15.md`, `last_block.md`, `live_review.md`, `plan.md` and
             `handoff.md`; `packages/orchestration/ci_stages.py` and `ci_run.py`;
             `tests/orchestration/test_ci_stages.py` and `test_ci_run.py`.

Constraints:
  1. Apply every slice BYTE-VERBATIM. If a FROM string is not found exactly
     once, STOP, commit nothing further, write the handoff naming the slice and
     what you found instead (G8). Never repair a slice yourself.
  2. Do NOT touch `.agent/f083_inventory.md` — a round that edits its own
     evidence has none.
  3. Do NOT change `scripts/remedy_pytest_runner.py`. Its 600-second default
     stays exactly as it is: every OTHER caller depends on it, which is the
     whole reason the budget is carried per stage instead.
  4. Do NOT add, remove or reorder a stage, and do not touch any
     `marker_expression`. The selections are DECISION F083 D2 and are settled.
  5. No `git commit --amend`, `git rebase`, `git reset`, force push or PR
     (R-0477, G2). The subjects above are given so you never choose one.
  6. `docs/` is deliberately NOT touched: no ist-doc describes `remedy ci` yet
     (measured: `grep -rln "remedy ci" docs/` returns only roadmap files), and
     writing that doc is T003's job, not this round's.
Slice convention: every slice is delimited by its own `--- BEGIN SLICE <NAME>
---` and `--- END SLICE <NAME> ---` markers, which are transport only and NEVER
reach a target file. EACH MARKER IS EXACTLY ONE LINE: a slice's content starts
on the line AFTER its BEGIN marker and ends on the line BEFORE its END marker,
and every blank line between those two — leading, inner or trailing — is part
of the content. The named units are RECORD-R14REC, S1 through S20, and PLAN. A
FROM:/TO: slice is a PAIR and states its shape: REWRITE means FROM is gone
afterwards; APPEND means the TO literally CONTAINS the FROM, so FROM stays and
only the TO-ONLY lines are new. A slice with no FROM: line is an EOF-APPEND:
concatenate its content to the target's bytes EXACTLY as given — its leading
blank lines are part of it — and change nothing already in the file.
--- BEGIN SLICE RECORD-R14REC --- (EOF-APPEND to .agent/live_review.md, C1)

Gate: R14-REC — PASS. The reviewer re-ran all fourteen gates itself at 54d83919 from the repository root and all fourteen reproduce. TRANSPORT: `.agent/authored/f083-r14-rec.md` and `.agent/last_block.md` are byte-equal at sha256 bb8bd83dbe465e62 over 19665 bytes and 214 lines, and 214 is under the 400-line cap. C1's prefix property holds with the tail byte-equal to `b"\n" + RECORD-R14` extracted from the COMMITTED authored file by its markers, numstat `4 0`. C2's `.agent/plan.md` byte-equals its PLAN slice, 43 lines, `## Goal` and `## Next Steps` present, 0 `- [ ]` lines. `.agent/f083_inventory.md` is untouched across the range and its `^## Q\d` headings still read Q1 through Q11, each once. The scoped range diff over `packages/`, `apps/`, `tests/`, `scripts/` and `docs/` printed NOTHING, so a record round that promised no code delivered none, and the measured change set is exactly the five `.agent/` paths. Every gate ran as its own process with the exit code read from that process: the four CI suites at 7, 9, 6 and 8 passed and the verification quartet at 70, 21, 15 and 42 passed, all exit 0; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set recomputes to 105 registered, 6 `Done:`, 0 `Landed:`, 99 open, max R-0477, next free R-0478, no duplicate id. Insertions 214, 122, 4, 12 and 101, none over 500. THE ROUND'S OWN CLAIM WAS CHECKED AGAINST ITS SUBJECT RATHER THAN READ: R-0477 is the amend disclosure the R14 handback could not carry, so the record now holds what the handoff did not, and both of its standing rules are obeyed by the block below — every C-item subject is NAMED there, so no worker has to choose one and none has to repair one. The worker's conduct was correct throughout: both slices applied byte-verbatim, no `Done:` paragraph of its own, the change set exactly the ordered paths, and the declared cap overage names the mandated content as its cause. No defect was found in this round and no finding is registered against it.

DECISION F083 D3 — R15 CARRIES THE TIMEOUT ALONE; THE BUDGET STAGE, THE DETERMINISM SHAPE AND THE R-0468 RULING MOVE TO R16. `.agent/plan.md` at 54d83919 names four things for R15: a per-stage timeout, a budget stage written from the `## Q11` spread, a ruling on R-0468, and the determinism stage's shape. CHOSEN: R15 does the FIRST only. Reason: the timeout is the one item that is BROKEN rather than merely absent — `## Q10` records `standard` killed at exit 124 three times out of three — and it is the item the others rest on, because a budget stage asserting a ceiling on a stage the runner truncates would be asserting it against a kill and not against the stage. ALTERNATIVES CONSIDERED: all four in one round, rejected because the block ordering them cannot fit under the 400-line cap of docs/agents/planner_reviewer_prompt.md §3 item 1 and the change set would mix a production fix with three rulings, which AGENTS.md Commit Discipline forbids; and the budget stage first, rejected for the reason just given. REVERSE by ordering the remaining three in any later round — nothing here forecloses them and `.agent/plan.md` now points at R16 for exactly those three. Said plainly so it cannot be misread later: the `budgets` STAGE that T2_F083's Design section names remains UNBUILT, and this decision does not build it. A per-stage `timeout_sec` is a kill threshold the runner enforces on one stage; the budgets stage is a stage that CHECKS documented ceilings and runs the guard tests. The two are not the same thing and F083 is not done when only the first exists.
--- END SLICE RECORD-R14REC ---
--- BEGIN SLICE S1 --- (APPEND pair, packages/orchestration/ci_stages.py, C2)
FROM:
    runs_in_ci: bool
    manual_command: str
TO:
    runs_in_ci: bool
    manual_command: str
    #: Wall-clock budget for this stage in seconds; 0 for a stage CI never runs.
    timeout_sec: int
--- END SLICE S1 ---
--- BEGIN SLICE S2 --- (APPEND pair, packages/orchestration/ci_stages.py, C2)
FROM:
        marker_expression="not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow",
        runs_in_ci=True,
        manual_command="",
TO:
        marker_expression="not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=900,
--- END SLICE S2 ---
--- BEGIN SLICE S3 --- (APPEND pair, packages/orchestration/ci_stages.py, C2)
FROM:
        marker_expression="(integration or subprocess) and not real_ollama",
        runs_in_ci=True,
        manual_command="",
TO:
        marker_expression="(integration or subprocess) and not real_ollama",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=2100,
--- END SLICE S3 ---
--- BEGIN SLICE S4 --- (APPEND pair, packages/orchestration/ci_stages.py, C2)
FROM:
        marker_expression="ui_contract and not real_ollama",
        runs_in_ci=True,
        manual_command="",
TO:
        marker_expression="ui_contract and not real_ollama",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=300,
--- END SLICE S4 ---
--- BEGIN SLICE S5 --- (APPEND pair, packages/orchestration/ci_stages.py, C2)
FROM:
        marker_expression="smoke and not real_ollama",
        runs_in_ci=True,
        manual_command="",
TO:
        marker_expression="smoke and not real_ollama",
        runs_in_ci=True,
        manual_command="",
        timeout_sec=300,
--- END SLICE S5 ---
--- BEGIN SLICE S6 --- (APPEND pair, packages/orchestration/ci_stages.py, C2)
FROM:
        manual_command="python3 -m pytest -m real_ollama -q  # needs a running Ollama server",
TO:
        manual_command="python3 -m pytest -m real_ollama -q  # needs a running Ollama server",
        timeout_sec=0,
--- END SLICE S6 ---
--- BEGIN SLICE S7 --- (APPEND pair, packages/orchestration/ci_run.py, C2)
FROM:
import subprocess
import sys
TO:
import os
import subprocess
import sys
--- END SLICE S7 ---
--- BEGIN SLICE S8 --- (APPEND pair, packages/orchestration/ci_run.py, C2)
FROM:
PYTEST_TIMEOUT_EXIT_CODE = 124
TO:
PYTEST_TIMEOUT_EXIT_CODE = 124

#: The env var `scripts/remedy_pytest_runner.py` reads its budget from.
PYTEST_TIMEOUT_ENV_VAR = "REMEDY_PYTEST_TIMEOUT_SEC"
--- END SLICE S8 ---
--- BEGIN SLICE S9 --- (REWRITE pair, packages/orchestration/ci_run.py, C2)
FROM:
def _run_via_subprocess(command: list[str], cwd: Path) -> int:
    """Run `command` ANCHORED at `cwd`, never at wherever the caller stands.
TO:
def _run_via_subprocess(command: list[str], cwd: Path, timeout_sec: int) -> int:
    """Run `command` ANCHORED at `cwd` and BUDGETED at `timeout_sec` seconds.
--- END SLICE S9 ---
--- BEGIN SLICE S10 --- (REWRITE pair, packages/orchestration/ci_run.py, C2)
FROM:
    anchor the caller's cwd decides what a stage means (finding R-0456).
    """
    return subprocess.run(command, check=False, cwd=cwd).returncode
TO:
    anchor the caller's cwd decides what a stage means (finding R-0456).

    The budget travels as an environment variable because that is the runner's
    only input for it, and it is set on THIS call rather than left to the ambient
    environment: the runner's own default is 600 s, and `standard` was killed at
    it three times out of three (`.agent/f083_inventory.md` `## Q10`) while
    needing 935.14 s at its slowest uncapped sample (`## Q11`). Budgeting per
    stage leaves every OTHER caller of the runner on the 600-second default,
    which raising that default would not.
    """
    env = {**os.environ, PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)}
    return subprocess.run(command, check=False, cwd=cwd, env=env).returncode
--- END SLICE S10 ---
--- BEGIN SLICE S11 --- (REWRITE pair, packages/orchestration/ci_run.py, C2)
FROM:
    run_command: Callable[[list[str], Path], int] = _run_via_subprocess,
TO:
    run_command: Callable[[list[str], Path, int], int] = _run_via_subprocess,
--- END SLICE S11 ---
--- BEGIN SLICE S12 --- (REWRITE pair, packages/orchestration/ci_run.py, C2)
FROM:
    exit_code = run_command(stage_command(stage, repo_root), repo_root)
TO:
    exit_code = run_command(stage_command(stage, repo_root), repo_root, stage.timeout_sec)
--- END SLICE S12 ---
--- BEGIN SLICE S13 --- (REWRITE pair, tests/orchestration/test_ci_run.py, C2)
FROM:
from pathlib import Path

from packages.orchestration.ci_run import (
    PYTEST_RUNNER_SCRIPT,
    StageResult,
TO:
import sys
from pathlib import Path

from packages.orchestration.ci_run import (
    PYTEST_RUNNER_SCRIPT,
    PYTEST_TIMEOUT_ENV_VAR,
    StageResult,
    _run_via_subprocess,
--- END SLICE S13 ---
--- BEGIN SLICE S14 --- (REWRITE pair, tests/orchestration/test_ci_run.py, C2)
FROM:
        run_command=lambda command, cwd: 0,
TO:
        run_command=lambda command, cwd, timeout_sec: 0,
--- END SLICE S14 ---
--- BEGIN SLICE S15 --- (REWRITE pair, tests/orchestration/test_ci_run.py, C2)
FROM:
        run_command=lambda command, cwd: 124,
TO:
        run_command=lambda command, cwd, timeout_sec: 124,
--- END SLICE S15 ---
--- BEGIN SLICE S16 --- (REWRITE pair, tests/orchestration/test_ci_run.py, C2)
FROM:
        run_command=lambda command, cwd: calls.append(command) or 0,
TO:
        run_command=lambda command, cwd, timeout_sec: calls.append(command) or 0,
--- END SLICE S16 ---
--- BEGIN SLICE S17 --- (REWRITE pair, tests/orchestration/test_ci_run.py, C2)
FROM:
    def record(command, cwd):
TO:
    def record(command, cwd, timeout_sec):
--- END SLICE S17 ---
--- BEGIN SLICE S18 --- (EOF-APPEND to tests/orchestration/test_ci_run.py, C2)


def test_run_ci_stage_hands_the_stage_its_own_budget():
    seen = []
    stage = ci_stage_by_name("standard")
    run_ci_stage(
        stage,
        REPO_ROOT,
        run_command=lambda command, cwd, timeout_sec: seen.append(timeout_sec) or 0,
        monotonic=lambda: 0.0,
    )
    assert seen == [stage.timeout_sec]


def test_the_budget_reaches_the_runner_process_as_its_environment_variable():
    """The real `_run_via_subprocess`, not an injected stand-in.

    The child exits 0 only when it READS the budget this call passed, so no
    unset variable and no ambient 600 can produce a green here.
    """
    probe = (
        "import os,sys;"
        f"sys.exit(0 if os.environ.get({PYTEST_TIMEOUT_ENV_VAR!r}) == '4242' else 3)"
    )
    assert _run_via_subprocess([sys.executable, "-c", probe], REPO_ROOT, 4242) == 0
    assert _run_via_subprocess([sys.executable, "-c", probe], REPO_ROOT, 600) == 3
--- END SLICE S18 ---
--- BEGIN SLICE S19 --- (APPEND pair, tests/orchestration/test_ci_stages.py, C2)
FROM:
import re
from pathlib import Path
TO:
import math
import re
from pathlib import Path
--- END SLICE S19 ---
--- BEGIN SLICE S20 --- (EOF-APPEND to tests/orchestration/test_ci_stages.py, C2)


#: The slowest wall second each stage was MEASURED at, three samples per stage:
#: `.agent/f083_inventory.md` `## Q10` for `fast`, `ui` and `smoke`, and `## Q11`
#: for `standard`, whose three uncapped samples span 916.36 s to 935.14 s.
MEASURED_MAX_WALL_S = {"fast": 397.45, "standard": 935.14, "ui": 8.09, "smoke": 11.07}

#: The budget rule: twice the measured maximum, rounded UP to a whole multiple of
#: this many seconds. Doubling absorbs a slow machine; the rounding keeps the
#: table readable. Changing a budget means re-measuring, not re-guessing.
BUDGET_HEADROOM_FACTOR = 2
BUDGET_ROUNDING_S = 300


def test_every_stage_ci_runs_carries_a_budget_and_excluded_carries_none():
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            assert stage.timeout_sec > 0, stage.name
        else:
            assert stage.timeout_sec == 0, stage.name


def test_each_budget_is_the_documented_multiple_of_the_measured_maximum():
    for stage in CI_STAGES:
        if not stage.runs_in_ci:
            continue
        measured = MEASURED_MAX_WALL_S[stage.name]
        expected = math.ceil(
            BUDGET_HEADROOM_FACTOR * measured / BUDGET_ROUNDING_S
        ) * BUDGET_ROUNDING_S
        assert stage.timeout_sec == expected, stage.name


def test_the_standard_budget_clears_the_runners_default_that_killed_it():
    assert ci_stage_by_name("standard").timeout_sec > 600
    assert ci_stage_by_name("standard").timeout_sec > MEASURED_MAX_WALL_S["standard"]
--- END SLICE S20 ---
--- BEGIN SLICE PLAN --- (WHOLE FILE, replaces .agent/plan.md, C3)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0478. `.agent/live_review.md` is the source of
truth for the open set; this file repeats no count of it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
None in flight. R15 is committed: every stage carries a measured `timeout_sec`,
the runner is handed that budget per call, and `standard` is no longer killed at
the runner's 600-second default. R15 did the timeout ONLY — DECISION F083 D3 in
`.agent/live_review.md` moved the other three items to R16 and gives the reason.

## Next Steps
1. R16 takes the three items D3 deferred: the `budgets` STAGE T2_F083's Design
   asks for, which is a stage that checks documented ceilings and runs the guard
   tests and does not yet exist; a ruling on R-0468 from the 26-error ruff
   baseline `## Q10` records; and the determinism stage's shape settled as a
   DECISION. It is a SPLIT round: the budgets stage is production code.

## Risks
- A per-stage `timeout_sec` is a kill threshold, NOT the budgets stage; reading
  R15 as the stage would close F083 with a Design item unbuilt.
- The determinism suite is already wholly inside `standard` (850 ids, 0 outside,
  measured at R11), so a determinism stage duplicates work unless `standard`'s
  expression is narrowed in the same change.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is
reported as not run, never as green (G4):

 1. `pwd` printed FIRST and equal to the repository root. `git status
    --porcelain` EMPTY before C0a and before C4. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before C0a; report it and whether it equals
    54d83919.
 3. TRANSPORT AND SIZE, bytes read in Python: sha256, byte count and line count
    of `.agent/authored/f083-r15.md` and `.agent/last_block.md`, and whether the
    two are EQUAL. This block declares no count of its own, so report the
    measured line count as a value — yours is the only measurement.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` EQUALS the RECORD-R14REC slice extracted from the
    COMMITTED authored file by its markers. Report numstat; deletions 0.
 5. `.agent/f083_inventory.md` UNTOUCHED: `git diff --name-only 54d83919..HEAD
    -- .agent/f083_inventory.md` prints NOTHING, and its `^## Q\d` count is 11.
 6. C2 CHANGE SET: `git diff --name-only <C2>^..<C2>` is EXACTLY the four code
    paths; `scripts/remedy_pytest_runner.py` is NOT among them (constraint 3).
 7. LINT, the repository's own config, from the repository root:
    `python3 -m ruff check .` — report its final `Found N errors.` line and exit
    code. N must be 26, the `## Q10` baseline: this round adds no lint error.
 8. GATE — the four CI suites, each its own process, REAL exit code from that
    process, each `python3 -m pytest <path> -q`, expectations in brackets:
    `tests/orchestration/test_ci_stages.py` [10, 0];
    `tests/orchestration/test_ci_stage_selection.py` [9, 0];
    `tests/cli/test_ci_cmd.py` [6, 0]; `tests/orchestration/test_ci_run.py`
    [10, 0]. Report the counts you MEASURE.
 9. GATE — VERIFICATION, each separately: `test_dashboard_contract.py` [70, 0];
    `test_resource_safety.py` [21, 0]; `test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0]. Paths as gate 8 names them; on any
    red, report the FAILED ids VERBATIM (R-0205 class) before you stop.
10. RED CONTROL, in a DISPOSABLE `git worktree` at HEAD under `.remedy-wt/`,
    NEVER in the primary checkout (G5): set `timeout_sec=2100` to `600` there,
    run `python3 -m pytest tests/orchestration/test_ci_stages.py -q`, report the
    exit code and which test ids FAILED — the colour and the ids, not a count.
    Then remove and prune the worktree and re-report `git worktree list`.
11. C3 PLAN byte-equals the PLAN slice as a whole file — sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line.
12. GATE — INTEGRITY, in Python because the `remedy` CLI is denied here
    (R-0408): `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, each check's status and the
    `handler_import` message [BASE: handlers=338; no handler is added here].
13. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. [BASE: 105 / 6 / 0, open 99, max R-0477.] This
    block registers NO finding, so the set is expected unchanged.
14. Insertions (`+` column only) for C0a through C3 — report each; none over
    500. C0b is a verbatim single-`.agent/`-file rewrite and AGENTS.md-exempt;
    report it anyway. C4's own count cannot exist inside C4 (R-0149).
15. NO COMMIT WAS AMENDED (R-0477): confirm in one sentence that you ran no
    `git commit --amend`, no `git rebase` and no `git reset` this round.

The push, the post-C4 clean-tree reading and the open-PR list postdate C3, so
per R-0449 they are NOT ordered into the handoff: run `git push -u origin
feature/f083-ci-self-check` after C4, create no PR, and report all three in your
final message with C4's own SHA and insertion count.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md —
feature and round, branch, per-commit changed-files tables, an item-status table
covering C0a through C4 and every gate above, the real verification values, the
open-findings count, the next expected action. Declare any cap overage with its
mandated cause (DECISION D15). End it with this line verbatim:

Fortschritt: 52 % (F083 beansprucht · R1 bis R7 und R9 bis R15 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner, die `remedy ci` CLI-Naht und die Selektionstests als Code gelandet · seit R15 trägt jede Stage ihr gemessenes Wall-Clock-Budget und `standard` wird nicht mehr nach 600 Sekunden abgeschnitten · noch keine budgets-Stage, keine Determinismus-Stage, kein Lint-Ceiling, keine hosted workflows) — Rundenzahl gemessen, Prozentwert geschätzt

If a GATE is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).
──────────────────────────────────────────────────────────────────────────────
