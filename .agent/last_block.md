── STEP R4/11 — F083 CI self-check — RECORD R3, REPAIR THE ROUND MAP, BUILD THE STAGE TABLE ──

Goal:
  Record the R3 PASS, register R-0455 — the round map in `.agent/live_review.md`
  and the two files that name the next round disagree about what R4 is — repair
  that map, and land this feature's first code: the five stage selections
  DECISION F083 D2 ruled, as DATA with no execution in it, plus the structural
  guards that keep the table honest. The stage runner, the CLI seam and the
  summary table are R5; the per-stage selection tests and the D2.5 parallelism
  measurement are R6.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r4.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — GATE-R3 + R-0455, appended at EOF in ONE
       commit. Findings persist FIRST (planner_reviewer_prompt §4.4).
  C2   `.agent/live_review.md` — the STEPS pair, R-0455's repair, ONE commit.
  C3   `packages/orchestration/ci_stages.py` (NEW) and
       `tests/orchestration/test_ci_stages.py` (NEW), ONE commit.
  C4   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C5   `.agent/handoff.md`, the handback, alone.

BASE: 83d4a649. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 83d4a649 (R-0428). If it does NOT, stop and hand off.

TRANSPORT: the reviewer's scratchpad original of THIS block is on disk at
`.remedy-wt/.cache/f083-r4/f083-r4.md`, which `.gitignore` drops. C0a is a byte
COPY of that file — do not retype it, do not reflow it, do not strip anything.

SLICE CONVENTION (R-0437): every slice body below is the lines between its
markers INCLUDING the trailing newline of its last line, and every shape is
declared UNDER THAT CONVENTION. The block's authored units are, listed: one EOF
append (GATE-R3-BLOCK into `.agent/live_review.md`), one REWRITE pair
(STEPS-FROM → STEPS-TO in the same file, in a later commit), two whole NEW files
(CI-STAGES, TEST-CI-STAGES) and one whole-file replacement (PLAN). No numeral is
stated for that list — the list IS the statement (R-0402, R-0441).

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r4.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `packages/orchestration/ci_stages.py`,
     `tests/orchestration/test_ci_stages.py`, `.agent/plan.md`,
     `.agent/handoff.md`. Nothing else. `apps/`, `scripts/` and `docs/` stay
     EMPTY in the range diff, and `.agent/f083_inventory.md` is NOT edited —
     it is R2's measured record and D2 rules over it without rewriting it.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. No slice contains an instruction
     addressed to you about the file it lands in (R-0450).
  3. C1 lands BEFORE C2, and C2 before C3. Push after C5. Create NO pull request.
  4. This round adds NO worktree. `git worktree list` is one line throughout.
  5. Neither new file is registered anywhere else this round: no CLI catalog
     entry, no `COMMAND_HANDLERS` table, no import from another module. The seam
     is R5's, and wiring it early would put a half-built command in the catalog.

--- BEGIN SLICE GATE-R3-BLOCK --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice)
Gate: R3 — PASS. Verification tier: the docs gate, the two live-state readers and the canary, all four re-run by the reviewer at the round's head; no full-suite claim is made, because this round changed no code and no test. Every ordered gate reproduces against the committed tree, each one re-measured by the reviewer rather than read out of the handback. TRANSPORT held: the scratchpad `.remedy-wt/.cache/f083-r3/f083-r3.md`, `.agent/authored/f083-r3.md` and `.agent/last_block.md` are all sha256 16f8c9f5328cd309694229502181e3f7a9511096fb2c3b2732865222399f2d6f, 20235 bytes, 230 lines, and all three byte strings are equal. C1's prefix property holds with a `6 0` numstat and a tail byte-equal to `b"\n" + GATE-R2-BLOCK` extracted by marker from the COMMITTED authored file, not from the reviewer's own copy. C2's two applied units hold the same way: `.agent/decisions.md` is a pure append equal to `b"\n" + DEC-D2`, and `.agent/plan.md` byte-equals PLAN at sha256 de1a88703ff03bc246f1d5dd8451922eabe5af67ddd53f657da19efd26d4ce0e, 43 lines, with `## Goal` and `## Next Steps` present and no `- [ ]` line. R-0453's repair is on disk, counted as literals at HEAD: `six findings` 0x, `Five of the six` 0x, `R-0448 to R-0454` 1x. The change set is six paths, every one under `.agent/`, with `packages/`, `apps/`, `scripts/`, `tests/` and `docs/` all empty and `.agent/f083_inventory.md` untouched as Constraint 5 required. Insertions 230 · 139 · 6 · 78 · 72, none over 500. The open set at HEAD is 82 registered, 0 resolved, max R-0454, next free R-0455, no duplicate id, against 80 and max R-0452 at BASE — exactly the two ordered ids and nothing else. The integrity gate reports passed true, fail_count 0, check_count 5, every named check pass. The four verification targets reproduce the BASE readings exactly: `tests/docs/` 295 passed exit 0, `tests/regression/test_resource_safety.py` 21 passed exit 0, `tests/orchestration/test_integrity_gate.py` 15 passed exit 0, and the canary `tests/cli/test_golden_path.py` 42 passed exit 0. The worker declared no deviation and repaired nothing silently, and its first declared deviation in the previous rounds is what R-0454's standing rule now prevents — the rule held on the first block written after it. ONE finding is registered below and it is again a defect of the reviewer's own block text rather than of the work delivered.

- R-0455 — Medium, THE ROUND MAP AND THE TWO FILES THAT NAME THE NEXT ROUND DISAGREE ABOUT WHAT R4 IS. Found by the REVIEWER while reviewing R3. `.agent/live_review.md` carries the round map in its `## Steps` section, and R-0447's own remedy made that section the single place the map is stated. At 83d4a649 that section reads "R3 T001 the stage runner, the marker selections and the summary table → R4 T002 the determinism and budget stages plus the guard-test wiring", while `.agent/plan.md` and `.agent/handoff.md` at the same commit each carry the string "R4 builds T001" exactly once, counted as a literal in both files. R3 did not build T001: it recorded R2, registered R-0453 and R-0454 and ruled DECISION F083 D2, and its own block says "It builds no stage runner and writes no code". So the single source says R4 is T002 while the two files derived from it say R4 is T001, and a session resuming from the map alone would build the wrong round. The arithmetic is broken with it: the map ends "R7 the integration gate → R8 closure" and the R3 handback opens "R3 of 8", but with T001 pushed to R4 every later item shifts and eight slots can no longer hold the work. The cause is precise and it is the reviewer's own: the R3 block gave its round a scope the map does not describe and ordered no repair of the map, which is the R-0447 class landing in the very file R-0447's remedy designated as the one that cannot go stale. The worker is not at fault — it applied every slice byte-verbatim as ordered and nothing in its change set reached the map. Repaired in this round's STEPS pair, which restates the map over the rounds that actually remain and narrows the "no other file restates it" clause to what it can mean, since AGENTS.md mandates a Next Steps section in `.agent/plan.md` and naming one round is not restating a map. Standing rule from here, binding the reviewer, and placed where it binds rather than left as prose (R-0452): a block that gives its round a scope the map does not describe repairs the map in that same block, or it is not emitted. OPEN until the repair is reviewed.
--- END SLICE GATE-R3-BLOCK ---

--- BEGIN SLICE STEPS-FROM --- (the REWRITE pair's FROM, C2; it occurs exactly once in .agent/live_review.md)
R1 merge the F082 closure PR at the Open PR Gate, claim F083, reset this record
carrying the F082 open set forward, and register the three F082 closure-review
candidates as R-0448, R-0449 and R-0450 → R2 the T001 marker inventory: the
collected count and the wall time per marker, which markers already exist, and
which stage each belongs to, every answer carrying a file-and-symbol citation →
R3 T001 the stage runner, the marker selections and the summary table → R4 T002
the determinism and budget stages plus the guard-test wiring → R5 T002 the
seeded-failure test per stage → R6 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R7 the integration gate → R8
closure. Each round marks the PREVIOUS one done and never itself; the map is
stated here ONLY, and no other file restates it (R-0447).
--- END SLICE STEPS-FROM ---

--- BEGIN SLICE STEPS-TO --- (the REWRITE pair's TO, C2; replaces STEPS-FROM in place)
R1 merge the F082 closure PR at the Open PR Gate, claim F083, reset this record
carrying the F082 open set forward, and register the three F082 closure-review
candidates as R-0448, R-0449 and R-0450 → R2 the T001 marker inventory: the
collected count and the wall time per marker, which markers already exist, and
which stage each belongs to, every answer carrying a file-and-symbol citation →
R3 record R2, register R-0453 and R-0454, and rule DECISION F083 D2, the stage
set → R4 T001 the stage definitions and their structural tests → R5 T001 the
stage runner over the existing pytest subprocess runner, the `remedy ci` CLI
seam and the summary table → R6 T001 the per-stage selection tests over a
fixture tree and the parallelism measurement D2.5 defers → R7 T002 the
determinism and budget stages plus the guard-test wiring → R8 T002 the
seeded-failure test per stage → R9 T003 the hosted workflow files, the docs and
the runtime budget written from measured data → R10 the integration gate → R11
closure. Each round marks the PREVIOUS one done and never itself; the FULL map
is stated here ONLY. Another file may name at most the NEXT round —
`.agent/plan.md` must, because AGENTS.md mandates its Next Steps section — and
naming one round is not restating the map (R-0447, R-0455).
--- END SLICE STEPS-TO ---

--- BEGIN SLICE CI-STAGES --- (the WHOLE content of the NEW file packages/orchestration/ci_stages.py, C3)
"""Remedy's own CI stages — the five marker selections DECISION F083 D2 ruled.

The stage set is DATA and it lives in exactly one place, so the local `remedy
ci` entrypoint and the hosted workflow files cannot drift into two opinions
about what CI means (T2_F083: "one source of truth for what CI means"). This
module RUNS NOTHING: it holds the selections, the reason each exists, and the
pytest argv a caller hands to the existing subprocess runner
(`scripts/remedy_pytest_runner.py`, which owns the process-group cleanup, the
output caps and the timeout). Wiring that runner, the summary table and the CLI
seam are later rounds; putting them here would make importing the stage table
able to start a test run.

The selections are MEASURED, not guessed: `.agent/f083_inventory.md` Q4
collected all five against the whole suite, their union was the whole suite with
nothing uncovered, and exactly one pair overlapped.

Remedy deliberately does NOT make `safety` and `architecture` stages of their
own (DECISION F083 D2.2) — measured, both are subsets of the selections below
and `safety` straddles two of them, so promoting either would introduce overlaps
this set does not have. They stay markers for ad-hoc selection.

Remedy deliberately does NOT store a collected COUNT per stage: a count is true
for one commit and wrong for the next, and a table carrying stale numbers is
worse than one carrying none.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CiStage:
    """One CI stage: what it selects, why it exists, and whether CI runs it."""

    name: str
    description: str
    marker_expression: str
    runs_in_ci: bool
    manual_command: str


#: The stage set DECISION F083 D2.1 ruled, in the order CI runs them.
CI_STAGES: tuple[CiStage, ...] = (
    CiStage(
        name="fast",
        description="Pure unit work: no integration state, no subprocess, no UI contract, no live provider.",
        marker_expression="not integration and not subprocess and not real_ollama and not ui_contract and not smoke and not slow",
        runs_in_ci=True,
        manual_command="",
    ),
    CiStage(
        name="standard",
        description="Integration and subprocess tests on the fake provider.",
        marker_expression="(integration or subprocess) and not real_ollama",
        runs_in_ci=True,
        manual_command="",
    ),
    CiStage(
        name="ui",
        description="Python-verifiable frontend and UI contracts.",
        marker_expression="ui_contract and not real_ollama",
        runs_in_ci=True,
        manual_command="",
    ),
    CiStage(
        name="smoke",
        description="Smoke contracts for the scripts and the infrastructure.",
        marker_expression="smoke and not real_ollama",
        runs_in_ci=True,
        manual_command="",
    ),
    CiStage(
        name="excluded",
        description="Live-provider tests. CI never runs them; they are listed so the coverage claim stays honest.",
        marker_expression="real_ollama",
        runs_in_ci=False,
        manual_command="python3 -m pytest -m real_ollama -q  # needs a running Ollama server",
    ),
)


def ci_stage_names() -> tuple[str, ...]:
    """The stage names, in the order CI runs them."""
    return tuple(stage.name for stage in CI_STAGES)


def ci_stage_by_name(name: str) -> CiStage:
    """The stage called `name`; KeyError naming every known stage otherwise."""
    for stage in CI_STAGES:
        if stage.name == name:
            return stage
    known = ", ".join(ci_stage_names())
    raise KeyError(f"unknown CI stage {name!r}; known stages: {known}")


def pytest_argv_for_stage(stage: CiStage) -> list[str]:
    """The pytest arguments that select `stage`. Builds argv; runs nothing."""
    return ["-m", stage.marker_expression, "-q"]
--- END SLICE CI-STAGES ---

--- BEGIN SLICE TEST-CI-STAGES --- (the WHOLE content of the NEW file tests/orchestration/test_ci_stages.py, C3)
"""Structural guards for the F083 CI stage table.

These tests read the table and nothing else: nothing is collected and no count
of the live suite is asserted. Whether each stage SELECTS the right subset is a
different question, measured against a fixture tree in a later round — a test
pinning live collected counts would go red whenever an unrelated commit added a
test, which is the carried finding R-0205 this feature owns.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from packages.orchestration.ci_stages import (
    CI_STAGES,
    ci_stage_by_name,
    ci_stage_names,
    pytest_argv_for_stage,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
BOOLEAN_WORDS = {"not", "and", "or"}


def test_stage_names_are_decision_d2_in_run_order():
    assert ci_stage_names() == ("fast", "standard", "ui", "smoke", "excluded")
    assert len(set(ci_stage_names())) == len(CI_STAGES)


def test_every_stage_carries_a_description_and_an_expression():
    for stage in CI_STAGES:
        assert stage.description.strip(), stage.name
        assert stage.marker_expression.strip(), stage.name


def test_only_excluded_stays_out_of_ci_and_names_its_manual_command():
    out_of_ci = [stage for stage in CI_STAGES if not stage.runs_in_ci]
    assert [stage.name for stage in out_of_ci] == ["excluded"]
    assert out_of_ci[0].manual_command.strip()


def test_stages_ci_runs_carry_no_manual_command():
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            assert stage.manual_command == "", stage.name


def test_every_marker_named_in_an_expression_is_declared_in_pyproject():
    pyproject = (REPO_ROOT / "pyproject.toml").read_text()
    declared = set(re.findall(r'^\s*"([a-z_]+):', pyproject, re.M))
    for stage in CI_STAGES:
        used = set(re.findall(r"[a-z_]+", stage.marker_expression)) - BOOLEAN_WORDS
        assert used <= declared, (stage.name, sorted(used - declared))


def test_pytest_argv_selects_the_expression_and_nothing_else():
    stage = ci_stage_by_name("smoke")
    assert pytest_argv_for_stage(stage) == ["-m", stage.marker_expression, "-q"]


def test_unknown_stage_name_raises_naming_every_known_stage():
    with pytest.raises(KeyError) as excinfo:
        ci_stage_by_name("determinism")
    for name in ci_stage_names():
        assert name in str(excinfo.value)
--- END SLICE TEST-CI-STAGES ---

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
reproduces the hosted result locally on a clean checkout, a seeded failure in
each stage fails the right stage with a readable summary, and total runtime
stays within a documented budget.

## Current Step
R4 records the R3 PASS, registers R-0455 — the round map and the two files that
name the next round disagreed about what R4 is — repairs that map, and lands
this feature's first code: `packages/orchestration/ci_stages.py`, the five stage
selections DECISION F083 D2 ruled, as data with no execution in it, plus the
structural guards in `tests/orchestration/test_ci_stages.py`.

## Next Steps
1. R5 wires the stage runner over `scripts/remedy_pytest_runner.py`, adds the
   `remedy ci` CLI seam Q8 names, and renders the summary table, which states
   the accepted `standard`/`smoke` double-run.
2. R6 measures each stage with and without `-n auto` and pins the per-stage
   setting from that reading (DECISION F083 D2.5), and adds the per-stage
   selection tests over a fixture tree rather than live collected counts.

## Risks
- Every finding registered on this branch so far is a defect in the reviewer's
  own block text, and R-0452 records that a counter-measure written as finding
  prose does not bind the next block. R-0455 is more of that same evidence.
- `fast` costs 391.8 s, measured once on one machine with an unrelated stale
  process present. The documented runtime budget the Goal requires cannot rest
  on a single reading, and no hosted runner exists yet to give a second one.
- The stage table carries no collected count on purpose. That keeps it from
  going stale, but it also means nothing yet proves a stage selects what R2
  measured; R6's fixture-tree tests are what close that gap.
--- END SLICE PLAN ---

Done when — run every gate and record its REAL value; a gate you cannot run is
reported as not run, never as green:

 1. `git status --porcelain` EMPTY before the first commit and before C5.
    `git worktree list` ONE line throughout. `.agent/STOP` ABSENT at round start
    and again at handback (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 83d4a649.
 3. TRANSPORT, bytes read in Python: report sha256, byte count and line count of
    `.remedy-wt/.cache/f083-r4/f083-r4.md`, `.agent/authored/f083-r4.md` and
    `.agent/last_block.md`, whether all three byte strings are EQUAL, and whether
    the measured line count equals this block's declared footer count.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` is a prefix of `post`, and
    `post[len(pre):]` equals `b"\n" + GATE-R3-BLOCK` byte-for-byte, the slice
    extracted from the COMMITTED `.agent/authored/f083-r4.md` by its markers.
    Report the numstat and confirm its deletion column is 0.
 5. C2 REWRITE PAIR, both slices extracted from the same committed authored file:
    over the WHOLE `.agent/live_review.md` at C2, STEPS-FROM occurs 0x and
    STEPS-TO occurs 1x. Additionally, inside the STEPS SECTION ONLY — the bytes
    between the line `## Steps` and the line `## Findings` — report the count of
    the literal `R3 T001`, which must be 0, and of the literal
    `R4 T001 the stage definitions`, which must be 1. Report the C2 numstat.
 6. C3 NEW FILES, each read back from the commit and compared with the slice
    extracted from the committed authored file: `packages/orchestration/ci_stages.py`
    byte-equals CI-STAGES and `tests/orchestration/test_ci_stages.py` byte-equals
    TEST-CI-STAGES. Report each file's sha256, byte count and line count, and
    that both were ADDED (numstat deletion column 0 on both).
 7. C3 RUNS GREEN, each command separately, exit code read from the process
    object and never from a pipe (R-0438), both paths resolved on disk first:
    `python3 -m ruff check packages/orchestration/ci_stages.py tests/orchestration/test_ci_stages.py`
    — report the exit code, which the reviewer measured as 0 at 83d4a649 in a
    disposable worktree; and `python3 -m pytest tests/orchestration/test_ci_stages.py -q`
    — report the collected count and the exit code, which the reviewer measured
    as 7 collected, 7 passed, exit 0 in that same worktree. Repository-wide
    `ruff check` is RED on main and is NOT a gate here (R-0364).
 8. C4 PLAN byte-equals the PLAN slice as a whole file — report sha256 and line
    count, under 50, with `## Goal` and `## Next Steps` present and no `- [ ]`
    line.
 9. CHANGE SET, measured BEFORE the handoff is written into C5, so it lists six
    paths and `.agent/handoff.md` is the seventh and last:
    `git diff --name-only 83d4a649..HEAD`. Report the full list and its count.
    Restricted to `apps/`, `scripts/` and `docs/` it must be EMPTY, and
    `.agent/f083_inventory.md` must not appear. Report both as measured lists.
10. VERIFICATION, each command run separately with its exit code read from the
    process (R-0438); all four paths resolved on disk before running. Report the
    collected count and the real exit code for EACH: `python3 -m pytest
    tests/ui_server/test_dashboard_contract.py -q`, the reader of BOTH files C2
    and C4 rewrite, which the reviewer measured at 70 collected, 70 passed, exit
    0 at BASE; `python3 -m pytest tests/regression/test_resource_safety.py -q`,
    21 passed, exit 0 at BASE; `python3 -m pytest
    tests/orchestration/test_integrity_gate.py -q`, 15 passed, exit 0 at BASE;
    and the canary `python3 -m pytest tests/cli/test_golden_path.py -q`, 42
    collected, 42 passed, exit 0 at BASE. `tests/docs/` is NOT a gate this round:
    the change set holds no `docs/roadmap/**` path, which is what triggers it.
11. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, count `^Done: R-\d+ — `
    lines, report both, their difference, the max id, the next free id and any
    duplicate id. Report what you MEASURE.
12. INTEGRITY GATE, in Python because the `remedy` CLI is denied in this session
    class (R-0408): `python3 -c "from packages.orchestration.integrity_gate
    import run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count` and every named check's status.
13. Insertions (`+` column only) for C0a, C0b, C1, C2, C3 and C4 — report each;
    none over 500. C0b is a verbatim single-`.agent/`-file rewrite and is exempt
    by the AGENTS.md counting rule; report its number anyway. C5's own insertion
    count cannot exist inside C5 (R-0149): report it in your final message.

The push and its result, the post-C5 clean-tree reading and the open-PR list all
come into existence AFTER C5 writes the handback, so per R-0449 and R-0452 they
are NOT ordered into that file: run `git push -u origin feature/f083-ci-self-check`
after C5, create no pull request, and report all three in your final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as
C5 — feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and every gate, open findings
with max and next free id, and the next expected action, which is R5 wiring the
stage runner and the `remedy ci` CLI seam. C5 cannot table its own SHA (R-0371,
R-0149); say so rather than inventing one. Repeat this line verbatim as the
Fortschritt line:

Fortschritt: 14 % (F083 beansprucht · R1 bis R3 PASS · Marker-Inventar gemessen · Stage-Set per DECISION F083 D2 entschieden · Stage-Tabelle als Code gelandet mit Struktur-Guards · noch kein Stage-Runner, keine CLI, keine hosted workflows) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish
the commit you are in, write the handoff naming the exact blocker, and end. Do
not widen scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 396 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
