── STEP R5/12 — F083 CI self-check — RECORD R4, SPLIT THE MAP, BUILD THE STAGE RUNNER ──

Goal:
  Record the R4 PASS — a clean round, no finding — split the map's R5 clause,
  which bundles the runner with a CLI seam that does not fit one round, and build
  the runner: one stage in, one honest verdict out, every stage through
  `scripts/remedy_pytest_runner.py` so its process-group cleanup, output caps and
  timeout survive. CLI seam and summary rendering move to R6.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r5.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R4 appended at EOF, ONE commit.
  C2   `.agent/live_review.md` — the STEPS pair, ONE commit.
  C3   `packages/orchestration/ci_run.py` and `tests/orchestration/test_ci_run.py`,
       both NEW, ONE commit.
  C4   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C5   `.agent/handoff.md`, the handback, alone.

BASE: 0e4526b0. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 0e4526b0 (R-0428). If it does NOT, stop and hand off.

TRANSPORT: the scratchpad original of THIS block is at
`.remedy-wt/.cache/f083-r5/f083-r5.md`, which `.gitignore` drops. C0a is a byte
COPY of it — do not retype, reflow or strip anything.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The authored units are, listed: one EOF append
(GATE-R4-BLOCK), one REWRITE pair (STEPS-FROM → STEPS-TO, same file, later
commit), two whole NEW files (CI-RUN, TEST-CI-RUN), one whole-file replacement
(PLAN). No numeral is stated for that list — the list IS the statement (R-0402).

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r5.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `packages/orchestration/ci_run.py`,
     `tests/orchestration/test_ci_run.py`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `apps/`, `scripts/` and `docs/` stay
     EMPTY in the range diff; R4's two files and `.agent/f083_inventory.md` are
     NOT edited — this round builds ON them.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice contains an instruction
     addressed to you about the file it lands in (R-0450).
  3. C1 lands BEFORE C2, C2 before C3. Push after C5. Create NO pull request.
     This round adds NO worktree; `git worktree list` is one line throughout.
  4. Nothing registers the new module elsewhere: no catalog entry, no
     `COMMAND_HANDLERS` table, no import from another module. That seam is R6's.

--- BEGIN SLICE GATE-R4-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R4 — PASS, with NO finding registered: the round was clean and the reviewer looked for one. Verification tier: the live-state contract reader, the two live-state readers and the canary, all re-run by the reviewer at the round's head, plus ruff and the new test file, and an independent re-derivation of every authored-text proof out of the committed objects; no full-suite claim is made. TRANSPORT held: the scratchpad `.remedy-wt/.cache/f083-r4/f083-r4.md`, `.agent/authored/f083-r4.md` and `.agent/last_block.md` are all sha256 3ae4f3b405cf1f65080217f69f73fdc93392ebc893874a7db2d8d03292790ab9, 25711 bytes, 396 lines, three-way byte-equal, and the measured 396 equals the block's declared footer. C1's prefix property holds from the git blobs, 150497 B to 154993 B, with a tail byte-equal to `b"\n" + GATE-R3-BLOCK` and a `4 0` numstat. C2's REWRITE pair holds in both directions: over the whole file STEPS-FROM is 0x and STEPS-TO is 1x, and inside the `## Steps`-to-`## Findings` section the literal `R3 T001` is 0x while `R4 T001 the stage definitions` is 1x — the map now describes the rounds that actually remain. The substring `Steps` survives in the file, so the dashboard contract that reads it stays green, and it does: 70 collected, 70 passed, exit 0, equal to the BASE reading. C3's two new files were read back OUT of the commit and byte-equal their slices — `packages/orchestration/ci_stages.py` sha256 6fb04d77bc4aae2e…, 3838 bytes, 98 lines, and `tests/orchestration/test_ci_stages.py` sha256 d61b189366699ea6…, 2355 bytes, 67 lines, both absent at BASE, both added with a 0 deletion column. Both run green in the PRIMARY checkout, not only in the reviewer's probe worktree: `ruff check` over the two paths exits 0, `pytest tests/orchestration/test_ci_stages.py -q` collects 7 and passes 7 at exit 0, and `packages.orchestration.ci_stages` imports from the primary checkout path — so the green is the committed code's, not a stale copy's (R-0337). C4's plan byte-equals PLAN at sha256 cdaa06847f2b7005…, 41 lines, `## Goal` and `## Next Steps` present, no `- [ ]` line. The change set is the seven ordered paths and nothing else, with `apps/`, `scripts/` and `docs/` empty and `.agent/f083_inventory.md` absent. Insertions 396 · 324 · 4 · 12 · 165 · 17 · 122, none over 500. The open set at HEAD is 83 registered, 0 resolved, max R-0455, next free R-0456, no duplicate id, and R-0455 is the only id added since BASE. The integrity gate reports passed true, fail_count 0, check_count 5, every named check pass; resource safety 21 passed exit 0, the integrity-gate tests 15 passed exit 0, and the canary 42 passed exit 0. The handback carries every mandated section, a 25-row item-status table and the Fortschritt line verbatim, and its stated-cause overage names the real measured 172 lines — the worker measured its own first draft's claim of 145, found it wrong and corrected it before committing, which is the declaration discipline working before the reviewer ever read the file.
--- END SLICE GATE-R4-BLOCK ---

--- BEGIN SLICE STEPS-FROM --- (the REWRITE pair's FROM, C2; six whole lines INSIDE the existing Steps paragraph, occurring exactly once in .agent/live_review.md)
stage runner over the existing pytest subprocess runner, the `remedy ci` CLI
seam and the summary table → R6 T001 the per-stage selection tests over a
fixture tree and the parallelism measurement D2.5 defers → R7 T002 the
determinism and budget stages plus the guard-test wiring → R8 T002 the
seeded-failure test per stage → R9 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R10 the integration gate → R11
--- END SLICE STEPS-FROM ---

--- BEGIN SLICE STEPS-TO --- (the REWRITE pair's TO, C2; replaces STEPS-FROM in place, six whole lines, the rest of the paragraph untouched)
stage runner over the existing pytest subprocess runner → R6 T001 the `remedy
ci` CLI seam and the summary table it prints → R7 T001 the per-stage selection
tests over a fixture tree and the parallelism measurement D2.5 defers → R8 T002
the determinism and budget stages plus the guard-test wiring → R9 T002 the
seeded-failure test per stage → R10 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R11 the integration gate → R12
--- END SLICE STEPS-TO ---

--- BEGIN SLICE CI-RUN --- (the WHOLE content of the NEW file packages/orchestration/ci_run.py, C3)
"""Running Remedy's own CI stages — one stage in, one honest verdict out.

The stage TABLE lives in :mod:`packages.orchestration.ci_stages`; this module
runs it. The split is deliberate: importing the table must never be able to
start a test run.

EVERY STAGE GOES THROUGH `scripts/remedy_pytest_runner.py`, AS A SUBPROCESS —
that script owns the process-group isolation, the 512 KiB output caps, the
`REMEDY_PYTEST_TIMEOUT_SEC` budget and exit code 124 for a timeout, and shelling
out to bare `pytest` would lose all four. It is invoked rather than imported
because `scripts/` carries no `__init__.py`, which is how
`tests/cli/test_pytest_runner.py` reaches it too.

Remedy deliberately does NOT retry a failing stage — a flaky test is quarantined
only by an explicit marker change in a reviewed diff (T2_F083: "retries hide
rot"). The command runner is INJECTED so a test can prove the wiring without
spawning pytest; the default really does spawn it. Rendering the summary belongs
with the command that prints it and is not here.
"""
from __future__ import annotations

import subprocess
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.ci_stages import CiStage, pytest_argv_for_stage

#: Exit code `scripts/remedy_pytest_runner.py` returns when it kills a timeout.
PYTEST_TIMEOUT_EXIT_CODE = 124

#: The runner every stage goes through, relative to the repository root.
PYTEST_RUNNER_SCRIPT = "scripts/remedy_pytest_runner.py"


@dataclass(frozen=True)
class StageResult:
    """What one stage did: whether it ran, how it ended, how long it took."""

    stage: str
    ran: bool
    exit_code: int | None
    duration_s: float
    note: str


def stage_command(stage: CiStage, repo_root: Path) -> list[str]:
    """The exact argv that runs `stage`. Builds it; runs nothing."""
    return [
        sys.executable,
        str(repo_root / PYTEST_RUNNER_SCRIPT),
        "--",
        *pytest_argv_for_stage(stage),
    ]


def _run_via_subprocess(command: list[str]) -> int:
    return subprocess.run(command, check=False).returncode


def run_ci_stage(
    stage: CiStage,
    repo_root: Path,
    *,
    run_command: Callable[[list[str]], int] = _run_via_subprocess,
    monotonic: Callable[[], float] = time.monotonic,
) -> StageResult:
    """Run one stage, or record why it was not run. Never raises on a red stage."""
    if not stage.runs_in_ci:
        return StageResult(
            stage=stage.name,
            ran=False,
            exit_code=None,
            duration_s=0.0,
            note=f"not run by CI — run it manually with: {stage.manual_command}",
        )
    started = monotonic()
    exit_code = run_command(stage_command(stage, repo_root))
    elapsed = monotonic() - started
    note = "timed out" if exit_code == PYTEST_TIMEOUT_EXIT_CODE else ""
    return StageResult(
        stage=stage.name,
        ran=True,
        exit_code=exit_code,
        duration_s=elapsed,
        note=note,
    )


def ci_exit_code(results: tuple[StageResult, ...]) -> int:
    """0 only when every stage that RAN ended green. A skipped stage is not a pass."""
    return 0 if all(r.exit_code == 0 for r in results if r.ran) else 1
--- END SLICE CI-RUN ---

--- BEGIN SLICE TEST-CI-RUN --- (the WHOLE content of the NEW file tests/orchestration/test_ci_run.py, C3)
"""Guards for the F083 CI stage runner.

No test here spawns pytest: the command runner is injected, so these prove the
WIRING — which argv a stage produces, what a red stage does to the aggregate,
what an excluded stage reports — without paying a suite run to learn it.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.ci_run import (
    PYTEST_RUNNER_SCRIPT,
    StageResult,
    ci_exit_code,
    run_ci_stage,
    stage_command,
)
from packages.orchestration.ci_stages import ci_stage_by_name, pytest_argv_for_stage

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_the_runner_script_this_module_targets_exists():
    assert (REPO_ROOT / PYTEST_RUNNER_SCRIPT).is_file()


def test_stage_command_goes_through_the_runner_and_carries_the_selection():
    stage = ci_stage_by_name("smoke")
    command = stage_command(stage, REPO_ROOT)
    assert command[1] == str(REPO_ROOT / PYTEST_RUNNER_SCRIPT)
    assert command[2] == "--"
    assert command[3:] == pytest_argv_for_stage(stage)
    assert "pytest" not in command[1:2]


def test_running_a_stage_records_the_exit_code_and_a_duration():
    ticks = iter([10.0, 12.5])
    result = run_ci_stage(
        ci_stage_by_name("fast"),
        REPO_ROOT,
        run_command=lambda command: 0,
        monotonic=lambda: next(ticks),
    )
    assert result.ran is True
    assert result.exit_code == 0
    assert result.duration_s == 2.5
    assert result.note == ""


def test_a_timeout_exit_code_is_named_in_the_note():
    result = run_ci_stage(
        ci_stage_by_name("fast"),
        REPO_ROOT,
        run_command=lambda command: 124,
        monotonic=lambda: 0.0,
    )
    assert result.exit_code == 124
    assert "timed out" in result.note


def test_an_excluded_stage_is_not_run_and_names_its_manual_command():
    calls = []
    stage = ci_stage_by_name("excluded")
    result = run_ci_stage(
        stage,
        REPO_ROOT,
        run_command=lambda command: calls.append(command) or 0,
        monotonic=lambda: 0.0,
    )
    assert calls == []
    assert result.ran is False
    assert result.exit_code is None
    assert stage.manual_command in result.note


def test_ci_exit_code_is_red_when_any_stage_that_ran_is_red():
    green = StageResult("fast", True, 0, 1.0, "")
    red = StageResult("standard", True, 1, 1.0, "")
    skipped = StageResult("excluded", False, None, 0.0, "not run by CI")
    assert ci_exit_code((green, skipped)) == 0
    assert ci_exit_code((green, red)) == 1
--- END SLICE TEST-CI-RUN ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C4)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0456. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0455 registered on this branch.
`.agent/live_review.md` is the source of truth; this file mirrors it.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R5 records the R4 PASS — a clean round, no finding — splits the map's R5 clause
so the runner and the CLI seam stop sharing one round, and builds
`packages/orchestration/ci_run.py`: one stage in, one `StageResult` out, every
stage going through `scripts/remedy_pytest_runner.py` so the process-group
cleanup, the output caps and the timeout survive. The command runner is injected,
so `tests/orchestration/test_ci_run.py` proves the wiring without spawning pytest.

## Next Steps
1. R6 adds the `remedy ci [--stage NAME] [--json]` CLI seam Q8 names — the
   catalog group, the entry and a `COMMAND_HANDLERS` module — and the summary
   table it prints, which states the accepted `standard`/`smoke` double-run.
2. R7 measures each stage with and without `-n auto`, pins the per-stage setting
   from that reading (DECISION F083 D2.5), and adds the per-stage selection
   tests over a fixture tree rather than live collected counts.

## Risks
- No test yet runs a stage for real, by design: the injected runner buys speed
  at the cost of never proving the subprocess seam end to end. R6 must land one
  real stage invocation. `fast` still rests on a single 391.8 s reading.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C5.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 0e4526b0.
 3. TRANSPORT, bytes read in Python: sha256, byte count and line count of
    `.remedy-wt/.cache/f083-r5/f083-r5.md`, `.agent/authored/f083-r5.md` and
    `.agent/last_block.md`; whether all three byte strings are EQUAL; whether the
    measured line count equals this block's declared footer count.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` is a prefix of `post`, and
    `post[len(pre):]` equals `b"\n" + GATE-R4-BLOCK` byte-for-byte, that slice
    extracted from the COMMITTED `.agent/authored/f083-r5.md` by its markers.
    Report the numstat; its deletion column must be 0.
 5. C2 REWRITE PAIR, both slices extracted from that same committed file: over
    the WHOLE `.agent/live_review.md` at C2, STEPS-FROM occurs 0x and STEPS-TO
    occurs 1x. Inside the STEPS SECTION ONLY — the bytes between the line
    `## Steps` and the line `## Findings` — count these three literals, each
    wholly on one line of the TO: `R6 T001 the` must be 1, `R11 the integration
    gate` must be 1, `R10 the integration gate` must be 0. Confirm the substring
    `Steps` still occurs in the file. Report the C2 numstat.
 6. C3 NEW FILES, read back from the commit and compared with the slices
    extracted from the committed authored file: `packages/orchestration/ci_run.py`
    byte-equals CI-RUN, `tests/orchestration/test_ci_run.py` byte-equals
    TEST-CI-RUN. Report each file's sha256, bytes, lines, and that both were
    ADDED (deletion column 0).
 7. C3 RUNS GREEN, each command separately, exit code from the process object,
    never a pipe (R-0438), both paths resolved on disk first. `python3 -m ruff
    check packages/orchestration/ci_run.py tests/orchestration/test_ci_run.py` —
    report the exit code [reviewer measured 0 at 0e4526b0 in a disposable
    worktree]. `python3 -m pytest tests/orchestration/test_ci_run.py -q` — report
    collected count and exit code [6 collected, 6 passed, exit 0, same worktree].
    `python3 -c "import packages.orchestration.ci_run as m; print(m.__file__)"` —
    must resolve inside the PRIMARY checkout, so the green belongs to the
    committed code, not a stale copy (R-0337). Repo-wide `ruff check` is RED on
    main and is NOT a gate here (R-0364).
 8. R4'S CODE STILL RUNS — this round imports it: `python3 -m pytest
    tests/orchestration/test_ci_stages.py -q`, report collected count and exit
    code [reviewer measured 7 collected, 7 passed, exit 0 at BASE].
 9. C4 PLAN byte-equals the PLAN slice as a whole file — report sha256 and line
    count, under 50, `## Goal` and `## Next Steps` present, no `- [ ]` line.
10. CHANGE SET, measured BEFORE the handoff is written into C5, so it lists six
    paths and `.agent/handoff.md` is the seventh and last:
    `git diff --name-only 0e4526b0..HEAD`. Report the full list and its count.
    Restricted to `apps/`, `scripts/` and `docs/` it must be EMPTY, and R4's two
    files and `.agent/f083_inventory.md` must not appear. Report both as measured
    lists.
11. VERIFICATION, each command run separately, exit code from the process
    (R-0438), every path resolved on disk first. Report collected count and real
    exit code for EACH, with the reviewer's BASE reading in brackets: `python3 -m
    pytest tests/ui_server/test_dashboard_contract.py -q` [70/70, exit 0] — the
    reader of BOTH files C2 and C4 rewrite; `python3 -m pytest
    tests/regression/test_resource_safety.py -q` [21, exit 0]; `python3 -m pytest
    tests/orchestration/test_integrity_gate.py -q` [15, exit 0]; and the canary
    `python3 -m pytest tests/cli/test_golden_path.py -q` [42/42, exit 0].
    `tests/docs/` is NOT a gate here: no `docs/roadmap/**` path is in the change
    set, which is what triggers it.
12. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs and `^Done: R-\d+ — `
    lines; report both, their difference, max id, next free id, any duplicate id.
    No new finding is registered here, so the reviewer expects the same 83 / 0 /
    R-0455 it measured at BASE. Report what you MEASURE.
13. INTEGRITY GATE, in Python because the `remedy` CLI is denied in this session
    class (R-0408): `python3 -c "from packages.orchestration.integrity_gate
    import run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every named check's status.
14. Insertions (`+` column only) for C0a, C0b, C1, C2, C3, C4 — report each;
    none over 500. C0b is a verbatim single-`.agent/`-file rewrite, exempt by the
    AGENTS.md counting rule; report its number anyway. C5's own count cannot
    exist inside C5 (R-0149): report it in your final message.

The push result, the post-C5 clean-tree reading and the open-PR list come into
existence AFTER C5, so per R-0449 and R-0452 they are NOT ordered into that file:
run `git push -u origin feature/f083-ci-self-check` after C5, create no pull
request, and report all three in your final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as
C5 — feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next action, R6's CLI seam and summary table.
C5 cannot table its own SHA (R-0371, R-0149); say so rather than inventing one.
Repeat this line verbatim as the Fortschritt line:

Fortschritt: 20 % (F083 beansprucht · R1 bis R4 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · Stage-Tabelle und Stage-Runner als Code gelandet · noch keine CLI, kein Summary, keine hosted workflows) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, end. Do not
widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 382 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
