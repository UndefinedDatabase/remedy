── STEP R8/14 — F083 CI self-check — RECORD R7, REGISTER TWO, LAND THE `remedy ci` CLI SEAM ──

Goal:
  Make the runner reachable. Record the R7 PASS, register the two findings review
  produced, then land the T001 CLI seam: a `ci` group and `ci.run` entry in the
  catalog, `apps/cli/commands/ci_cmd.py` carrying `COMMAND_HANDLERS` and the
  summary table, its wiring into `collect_all_handlers`, and
  `tests/cli/test_ci_cmd.py` — whose last test really launches a stage argv
  through `scripts/remedy_pytest_runner.py` as a subprocess.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r8.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R7 appended at EOF, ONE commit, one body:
       gate line, blank line, the two findings.
  C2   `apps/cli/commands/ci_cmd.py` — NEW FILE, whole file, ONE commit.
  C3   `apps/cli/command_catalog.py` — the GROUP and ENTRY pairs, ONE commit.
  C4   `apps/cli/commands/__init__.py` — the IMPORT and TUPLE pairs, ONE commit.
  C5   `tests/cli/test_ci_cmd.py` — NEW FILE, whole file, ONE commit.
  C6   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C7   `.agent/handoff.md`, the handback, alone.

BASE: 2d1c6d8d. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 2d1c6d8d. If it does NOT, stop and hand off.

TRANSPORT: the scratchpad original of THIS block is at
`.remedy-wt/.cache/f083-r8/f083-r8.md`, which `.gitignore` drops. C0a is a byte
COPY of it — do not retype, reflow or strip anything. `cp` is denied in this
session class: copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.

SLICE CONVENTION (R-0437): every slice body below is the lines between its markers
INCLUDING the trailing newline of its last line, and every shape is declared UNDER
THAT CONVENTION. The authored units are, listed and NOT counted (R-0402, R-0460):
RECORD-R7, CI-CMD, GROUP, ENTRY, IMPORT, TUPLE, TEST-CI-CMD, PLAN.

PAIR SHAPES, stated at authoring time (§4.9), verified on these bytes rather than
asserted, and DIFFERENT for the two files C3 and C4 touch — read this before
choosing a proof. GROUP and ENTRY are APPEND-shaped: each TO literally CONTAINS its
FROM, so "FROM 0x" is UNSATISFIABLE for them and is NOT ordered; their property is
FROM 1x before AND after, TO 0x before and 1x after. IMPORT and TUPLE are REWRITEs
— FROM and TO are disjoint — so each is proved by FROM 0x and TO 1x over the whole
file. CI-CMD, TEST-CI-CMD and PLAN are WHOLE FILES, proved by byte equality.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r8.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
     `apps/cli/commands/ci_cmd.py`, `apps/cli/command_catalog.py`,
     `apps/cli/commands/__init__.py`, `tests/cli/test_ci_cmd.py`. Nothing else.
     `packages/` stays EMPTY in the range diff — this round wires the existing
     runner and changes no orchestration code.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice carries an instruction
     addressed to you about the file it lands in (R-0450).
  3. Commit strictly in the C-order above: C2 before C3, C3 before C4, C4 before
     C5. Push after C7. Create NO pull request. This round adds NO worktree;
     `git worktree list` is one line throughout.
  4. Env-var assignment (all three forms), `cp`, `$?` inside `$(...)` and process
     substitution are denied in this session class. Capture real exit codes as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and use `python3` scripts written to
     `.remedy-wt/.cache/f083-r8/` for all counting, hashing and byte comparison —
     a quoted heredoc is also fine where the shell accepts it.

--- BEGIN SLICE RECORD-R7 --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice. The blank line INSIDE this slice, between the gate line and the first finding, is part of it.)
Gate: R7 — PASS. Verification tier: all fourteen ordered gates re-run by the reviewer itself at the round's head, plus an independent re-derivation of every authored-text proof out of the committed git objects; no full-suite claim is made. Every value the handback declares was re-measured and every one MATCHED. TRANSPORT held in its strongest form: `.remedy-wt/.cache/f083-r7/f083-r7.md`, the committed `.agent/authored/f083-r7.md` and `.agent/last_block.md` are three-way byte-equal at sha256 55d13bea17d21bc337a66abdb580297d1806d557e9cf23a6dfecb9d5e28be7b7, 19042 bytes, 207 lines, and the measured 207 equals the block's declared footer — so no applied byte was retyped anywhere on the path. The two EOF appends each hold the prefix property, re-derived from the git blobs with the slices extracted BY MARKER from the committed authored file: C1 and C2 both prefix True with tails byte-equal to `b"\n" + GATE-R6-BLOCK` and `b"\n" + FINDING-R460`, numstats `2 0` and `2 0`, deletion column 0 in both. The C3 REWRITE pair holds in both directions at 0cef203c — LANDED-FROM 0x, DONE-TO 1x, line-anchored `^Landed: R-` 0 and `^Done: R-` 4, numstat `4 4` — and the C4 pair likewise at 0f854f82, STEPS-FROM 0x and STEPS-TO 1x with the three ordered literals at their ordered 1, 1 and 0, `Steps` still occurring 26 times, numstat `7 6`. The round's defining constraint held: `git diff --name-only e166b640..HEAD -- apps/ packages/ tests/ scripts/ docs/` printed NOTHING, so no code was written. The code R6 landed still runs — the two orchestration files give 15 passed at exit 0, collecting 8 and 7 per file, equal to the reviewer's BASE reading. All four verification paths were confirmed on disk before use (R-0438) and each ran separately: dashboard contract 70 passed, resource safety 21 passed, integrity-gate tests 15 passed, canary 42 passed, every one exit 0. The open set at HEAD is 88 registered, 4 `Done:`, 0 `Landed:`, open 84, max R-0460, no duplicate id, and the four resolved ids are exactly R-0456 to R-0459 — matching the block's expectation on every value. The integrity gate reports passed true, fail_count 0, check_count 5, every named check pass. `.agent/plan.md` byte-equals the PLAN slice at sha256 dad347470a35fc42ae82bb6d877002049350ddcef9ec31a88f230b035111c213, 32 lines, one numbered Next Step, no `- [ ]` line. Insertions 207 · 146 · 2 · 2 · 4 · 7 · 15, with the handback's own 112 measured after the fact, none over 500. The worker's conduct was exact: every slice applied byte-verbatim, no slice altered or reflowed, no scope widened, and no claim made that the reviewer could not re-derive. Both findings registered below are defects of the REVIEWER's own authored text, found by re-reading it against disk, and neither is chargeable to the round that applied it.

- R-0461 — Medium, A FINDING DECLARED ITS OWN RULE ALREADY PLACED IN THE CHECKLIST WHILE THE SAME BLOCK FORBADE TOUCHING THE FILE THAT CARRIES IT. R-0460's closing sentence reads "Standing rule from here, binding the reviewer, and placed in the pre-emission checklist rather than left as finding prose (R-0452)". It is not placed there. The pre-emission checklist in `docs/agents/planner_reviewer_prompt.md` §3 opens "Run all ten checks mechanically" and its items run 1 to 10, none of which is the convention-paragraph rule; a repo-wide grep of every `*.md` for "convention paragraph", "NO count of them", "denies enumerating" and "both enumerates" returns the rule ONLY in `.agent/live_review.md` and in the two mirrors of the block that authored it, so the absence is measured across every writer rather than inferred from one file (R-0419). The claim was moreover unsatisfiable by construction: constraint 1 of the same block fixed the change set at five `.agent/**` paths and ordered `docs/` to stay EMPTY in the range diff, so the block asserted a placement its own constraints forbade any commit in that round from making. This is exactly the class R-0452 exists to name — a standing rule written as finding prose binds nothing — and the sentence defeats it in a new way, by ASSERTING the promotion instead of performing it, which is strictly worse than leaving it as prose because a later reader greps the checklist, does not find it, and cannot tell whether the rule was retired or never landed. It is also the R-0416 class in its purest form: an authored finding stating an outcome about bytes the same block has not written and cannot write. Low would understate it — R-0416 already ruled that completeness claims are forbidden and this is a stronger claim than completeness — so Medium. The reviewer's defect entirely; the R7 worker applied the text byte-verbatim as ordered, which is the correct conduct. Fix, owed and NOT ordered here: the promotion R-0460 claimed still has to happen — the rule becomes checklist item 11 in §3, and the "Run all ten checks" opener is updated in the same pair so the count and the enumeration agree. R8 does NOT do it: this block's change set contains no `docs/` path, and ordering the edit in the finding text while excluding the file is the very defect being registered. R9 owns it as its first item. From here, a finding may state that a rule IS in the checklist only when the same block ORDERS the edit that puts it there; otherwise it names the round that will, as this one does. OPEN.
- R-0462 — Low, THE HANDBACK TOKEN CAP IS BINDING, EXCEEDED EVERY ROUND, AND MEASURED BY NOTHING. `docs/agents/handback_template.md` sets two independent limits: a LINE cap of ≤60, ≤100 for a >5-commit bundle and ≤160 for the >10-commit LARGE case, and below it a "Hard cap: this file stays ≤800 tokens — ≤1600 in the >10-commit LARGE case". The R7 handback declares a DECISION D15 stated-cause overage naming its 178 lines against the ≤100 cap, which is the correct and honest treatment of the LINE cap — and says nothing about the token cap, which it also exceeds. `.agent/handoff.md` at 2d1c6d8d is 8839 bytes; the file is English prose with tables, so no defensible bytes-per-token ratio brings it under 800, and even a deliberately generous five-bytes-per-token reading leaves it above the 1600 the LARGE case allows, which this 8-commit bundle cannot claim anyway. The property is what is registered here, not a token count the reviewer cannot measure exactly: the file is over the hard cap by a multiple, under every ratio worth arguing about. It is chronic rather than new — R5 was 164 lines, R6 152, R7 178 — and it is structural rather than careless: the mandated sections compose a per-commit table for every commit, a value for every ordered gate, and an item-status row for every C-item and every gate, which for a bundle of this shape cannot fit 800 tokens however tersely written. Low, because nothing downstream consumed a wrong number and the honesty of the record is unharmed. The cause is a gap in the counter-measure rather than in any round: pre-emission checklist item 3 names the LINE caps of `.agent/plan.md` and `.agent/handoff.md` and is silent on the token cap, so no reviewer pass has ever measured it. Fix, deferred to a paydown round and NOT to R8, because it changes a rule document that R8's change set does not include and the right repair is a ruling rather than an edit: the operator decides whether the 800-token cap is raised to match the mandated content, or the mandated content is reduced, and whichever way it goes, item 3 gains the token cap so the number is measured instead of assumed. Until that ruling, a handback that declares a D15 stated-cause overage names BOTH caps it exceeds rather than only the line cap. OPEN.
--- END SLICE RECORD-R7 ---

--- BEGIN SLICE CI-CMD --- (WHOLE FILE, the NEW file apps/cli/commands/ci_cmd.py, C2)
"""CLI handlers for the ``ci`` command group — Remedy's own CI, run locally.

The stage TABLE is :mod:`packages.orchestration.ci_stages` and the RUNNER is
:mod:`packages.orchestration.ci_run`; this module owns only the seam between them
and the terminal — stage selection, the summary table, and the process exit code.
Rendering lives HERE rather than in the runner because a summary is a property of
the command that prints it, not of the run (T2_F083). `remedy ci` runs every stage
in table order; `--stage NAME` runs exactly one. A stage marked `runs_in_ci=False`
is REPORTED as skipped with the command that runs it by hand — never silently
dropped, because the coverage claim is honest only while the exclusions stay
visible. Remedy deliberately does NOT give this command a "stop at the first red"
switch: `run_ci_stage` never raises on a red stage, so every selected stage always
runs and the summary is always complete.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

def repo_root_for_ci() -> Path:
    """The repository root every stage is anchored at (finding R-0456).

    This file is `apps/cli/commands/ci_cmd.py`, so the root is three levels up.
    """
    return Path(__file__).resolve().parents[3]


def summarize_ci_results(results: tuple[Any, ...]) -> str:
    """The per-stage table a human reads: one line per stage, in run order."""
    lines = ["STAGE        RESULT      TIME  NOTE"]
    for result in results:
        if not result.ran:
            verdict = "skipped"
        elif result.exit_code == 0:
            verdict = "passed"
        else:
            verdict = f"failed({result.exit_code})"
        lines.append(f"{result.stage:<12} {verdict:<11} {result.duration_s:5.1f}  {result.note}".rstrip())
    return "\n".join(lines)


def ci_results_as_json(results: tuple[Any, ...]) -> str:
    """The same table as JSON, for a caller that parses instead of reads."""
    rows = [
        {
            "stage": result.stage, "ran": result.ran, "exit_code": result.exit_code,
            "duration_s": round(result.duration_s, 3), "note": result.note,
        }
        for result in results
    ]
    return json.dumps(rows, indent=2)


def _cmd_ci_run(args: Any) -> None:
    """Run the selected CI stages and exit with the run's honest verdict."""
    from packages.orchestration.ci_run import ci_exit_code, run_ci_stage
    from packages.orchestration.ci_stages import CI_STAGES, ci_stage_by_name

    selected = getattr(args, "stage", None)
    stages = (ci_stage_by_name(selected),) if selected else CI_STAGES
    root = repo_root_for_ci()
    results = tuple(run_ci_stage(stage, root) for stage in stages)

    if getattr(args, "json", False):
        print(ci_results_as_json(results))
    else:
        print(summarize_ci_results(results))

    sys.exit(ci_exit_code(results))


COMMAND_HANDLERS = {
    "ci.run": lambda args: _cmd_ci_run(args),
}
--- END SLICE CI-CMD ---

--- BEGIN SLICE GROUP-FROM --- (the APPEND-shaped pair's FROM, C3; one whole line occurring exactly once in apps/cli/command_catalog.py)
    "integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks.", user_facing=False),
--- END SLICE GROUP-FROM ---

--- BEGIN SLICE GROUP-TO --- (the APPEND-shaped pair's TO, C3; replaces GROUP-FROM in place. It CONTAINS the FROM line unchanged as its second line.)
    "ci": GroupDef("ci", "CI", "Remedy's own CI stages, run locally.", user_facing=False),
    "integrity": GroupDef("integrity", "Integrity", "Pre-handoff integrity checks.", user_facing=False),
--- END SLICE GROUP-TO ---

--- BEGIN SLICE ENTRY-FROM --- (the APPEND-shaped pair's FROM, C3; ONE whole line occurring exactly once in apps/cli/command_catalog.py — the section comment above the integrity entry)
    # ── integrity ───────────────────────────────────────────────────────
--- END SLICE ENTRY-FROM ---

--- BEGIN SLICE ENTRY-TO --- (the APPEND-shaped pair's TO, C3; replaces ENTRY-FROM in place. It CONTAINS the FROM line unchanged as its LAST line. `action_class` is `test_execution` and `may_execute_commands` is True because this command spawns pytest — `read_only` would fail the catalog's own mutating-commands guard.)
    # ── ci ─────────────────────────────────────────────────────────────
    CommandEntry(
        command_id="ci.run",
        group_id="ci",
        subcommand="run",
        description="Run Remedy's own CI stages locally and print the summary.",
        action_class="test_execution",
        args=(
            ArgDef("--stage", "Run one stage by name instead of all of them", required=False, is_option=True),
            ArgDef("--json", "Output as JSON", required=False, is_option=True),
        ),
        supports_json=True,
        may_execute_commands=True,
    ),

    # ── integrity ───────────────────────────────────────────────────────
--- END SLICE ENTRY-TO ---

--- BEGIN SLICE IMPORT-FROM --- (the REWRITE pair's FROM, C4; two whole contiguous lines occurring exactly once in apps/cli/commands/__init__.py)
        change,
        config_cmd,
--- END SLICE IMPORT-FROM ---

--- BEGIN SLICE IMPORT-TO --- (the REWRITE pair's TO, C4; replaces IMPORT-FROM in place, three whole lines, keeping the import list alphabetical)
        change,
        ci_cmd,
        config_cmd,
--- END SLICE IMPORT-TO ---

--- BEGIN SLICE TUPLE-FROM --- (the REWRITE pair's FROM, C4; a fragment at the end of the `for mod in (...)` line, occurring exactly once in apps/cli/commands/__init__.py)
, bench_cmd):
--- END SLICE TUPLE-FROM ---

--- BEGIN SLICE TUPLE-TO --- (the REWRITE pair's TO, C4; replaces TUPLE-FROM in place. This tuple is ordered by when a module was added, not alphabetically, so the new module goes last.)
, bench_cmd, ci_cmd):
--- END SLICE TUPLE-TO ---

--- BEGIN SLICE TEST-CI-CMD --- (WHOLE FILE, the NEW file tests/cli/test_ci_cmd.py, C5)
"""Contract tests for the `remedy ci` CLI seam.

The seam is thin by design, so these pin the three things that can rot: the
catalog entry and its handler agree, the summary reports every stage including
the ones CI never runs, and the argv a stage builds really reaches
`scripts/remedy_pytest_runner.py` as a subprocess.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from apps.cli.command_catalog import GROUPS, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands.ci_cmd import repo_root_for_ci, summarize_ci_results
from packages.orchestration.ci_run import StageResult, stage_command
from packages.orchestration.ci_stages import ci_stage_by_name

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_ci_group_and_entry_declare_that_the_command_executes():
    assert "ci" in GROUPS
    assert GROUPS["ci"].user_facing is False
    cmd = get_command("ci.run")
    assert cmd.group_id == "ci"
    assert cmd.subcommand == "run"
    assert cmd.action_class == "test_execution"
    assert cmd.may_execute_commands is True


def test_ci_run_handler_is_reachable_from_the_cli():
    assert "ci.run" in collect_all_handlers()


def test_repo_root_is_the_repository_root():
    assert repo_root_for_ci() == REPO_ROOT
    assert (repo_root_for_ci() / "scripts" / "remedy_pytest_runner.py").is_file()


def test_summary_reports_a_skipped_stage_instead_of_dropping_it():
    note = "not run by CI — run it manually with: pytest -m real_ollama"
    results = (
        StageResult(stage="fast", ran=True, exit_code=0, duration_s=1.0, note=""),
        StageResult(stage="excluded", ran=False, exit_code=None, duration_s=0.0, note=note),
    )
    table = summarize_ci_results(results)
    assert "excluded" in table
    assert "skipped" in table
    assert "passed" in table
    assert "run it manually" in table


def test_summary_names_the_failing_exit_code():
    results = (StageResult(stage="fast", ran=True, exit_code=2, duration_s=0.5, note=""),)
    assert "failed(2)" in summarize_ci_results(results)


@pytest.mark.subprocess
def test_a_stage_argv_really_reaches_the_pytest_runner():
    """Launch a real stage argv through the runner script, not a stub.

    The tests above prove the wiring without spawning anything; this one proves
    the seam a user actually hits.
    """
    command = stage_command(ci_stage_by_name("fast"), REPO_ROOT)
    assert command[1].endswith("scripts/remedy_pytest_runner.py")
    assert command[2] == "--"
    probe = [*command[:3], "--collect-only", "-q", "tests/cli/test_ci_cmd.py"]
    completed = subprocess.run(
        probe, cwd=REPO_ROOT, capture_output=True, text=True, timeout=300, check=False
    )
    assert completed.returncode == 0, completed.stdout[-2000:] + completed.stderr[-2000:]
--- END SLICE TEST-CI-CMD ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C6)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0463. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0462 registered on this branch, of which
R-0456 to R-0459 are resolved. `.agent/live_review.md` is the source of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R8 records the R7 PASS, registers R-0461 and R-0462, and lands the T001 CLI seam:
the `ci` catalog group and `ci.run` entry, `apps/cli/commands/ci_cmd.py` with its
summary table, the wiring into `collect_all_handlers`, and `tests/cli/test_ci_cmd.py`
— whose last test really launches a stage argv through the pytest runner script.

## Next Steps
1. R9 promotes R-0460's rule into the §3 pre-emission checklist as item 11
   (finding R-0461, its first item), then adds the per-stage selection tests over
   a fixture tree that pin each stage's marker expression against known markers.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C7.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 2d1c6d8d.
 3. TRANSPORT, bytes read in Python: sha256, bytes and lines of
    `.remedy-wt/.cache/f083-r8/f083-r8.md`, `.agent/authored/f083-r8.md` and
    `.agent/last_block.md`; whether all three are EQUAL; whether the measured line
    count equals this block's declared footer.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R7`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r8.md` by its markers. Report the numstat;
    its deletion column must be 0.
 5. THE TWO NEW FILES, each byte-equal to its slice as a whole file — sha256 and
    line count for both: `apps/cli/commands/ci_cmd.py` against CI-CMD and
    `tests/cli/test_ci_cmd.py` against TEST-CI-CMD. Also report
    `git diff --name-only <C2>^..<C2>`, which must list `ci_cmd.py` ALONE.
 6. C3 APPEND-SHAPED PAIRS over the whole `apps/cli/command_catalog.py` at C3 —
    each FROM is CONTAINED in its TO, so GROUP-FROM and ENTRY-FROM must each be 1x
    BEFORE and 1x AFTER, while GROUP-TO and ENTRY-TO must each be 0x before and 1x
    after. Report all eight. Then over the file at C3: `"ci": GroupDef` 1,
    `command_id="ci.run"` 1, `command_id="integrity.check"` 1. Report the numstat.
 7. C4 REWRITE PAIRS over the whole `apps/cli/commands/__init__.py` at C4:
    IMPORT-FROM 0x, IMPORT-TO 1x, TUPLE-FROM 0x, TUPLE-TO 1x. Then `ci_cmd`
    occurs exactly 2 in that file and `bench_cmd` exactly 2. Report the numstat.
 8. RUFF over the four Python files this round writes or edits, in ONE run:
    `python3 -m ruff check apps/cli/commands/ci_cmd.py apps/cli/command_catalog.py
    apps/cli/commands/__init__.py tests/cli/test_ci_cmd.py` — report the real exit
    code [reviewer measured exit 0 over the two edited files at BASE].
 9. THE NEW TESTS RUN: `python3 -m pytest tests/cli/test_ci_cmd.py -q` — report
    collected count and exit code. Its last test spawns a real subprocess and is
    the slowest; if it exceeds the runner's budget, report that rather than
    trimming the test.
10. THE CATALOG STILL AGREES WITH ITSELF, all four paths confirmed on disk first
    (R-0438), in ONE run: `python3 -m pytest tests/test_command_catalog.py
    tests/cli/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_cli_ux.py
    -q` — collected count and exit code [BASE: 593 passed, exit 0 — a red here is
    this round's doing]. NOTE the two same-named files; both are gates.
11. VERIFICATION, each run separately, exit code from the process (R-0438), each
    via `python3 -m pytest <path> -q`: `tests/ui_server/test_dashboard_contract.py`
    [70, 0] — it reads the handler table this round extends;
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0]. `tests/docs/` is NOT a gate — no
    `docs/roadmap/**` path is in the change set.
12. THE STAGE TABLE AND RUNNER ARE UNTOUCHED: `git diff --name-only 2d1c6d8d..HEAD
    -- packages/` must print NOTHING. Report it as a measured list.
13. INTEGRITY GATE, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message, whose count rises by exactly 1 [BASE: handlers=337].
14. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. Reviewer measured 88 / 4 / 0, max R-0460, at BASE
    and expects 90 / 4 / 0, max R-0462, open 86. Report what you MEASURE.
15. C6 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    number of numbered items under `## Next Steps`.
16. CHANGE SET, measured BEFORE the handoff is written into C7, so it lists eight
    paths with `.agent/handoff.md` the ninth and last: `git diff --name-only
    2d1c6d8d..HEAD`. Report the list and its count.
17. Insertions (`+` column only) for C0a through C6 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt; report it
    anyway. C7's own count cannot exist inside C7 (R-0149): final message.

The push result, the post-C7 clean-tree reading and the open-PR list postdate C7,
so per R-0449 and R-0452 they are NOT ordered into that file: run `git push -u
origin feature/f083-ci-self-check` after C7, create no PR, report all three in your
final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as C7
— feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and gate, open findings with
max and next free id, and the next action, R9 as the plan states it. C7
cannot table its own SHA (R-0371, R-0149); say so rather than inventing one. If it
exceeds a cap, name BOTH the line and token caps — R-0462 registers that gap in
C1. Fortschritt, verbatim:

Fortschritt: 32 % (F083 beansprucht · R1 bis R7 PASS · Stage-Tabelle, Stage-Runner und jetzt die `remedy ci` CLI-Naht als Code gelandet, mit einem Test der wirklich einen Stage-Argv durch den Runner startet · noch kein Summary in den hosted workflows, keine Determinismus- oder Budget-Stage) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 400 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
