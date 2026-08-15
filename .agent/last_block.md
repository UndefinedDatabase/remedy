── STEP R10/15 — F083 CI self-check — RECORD R9 PASS, LAND THE PER-STAGE SELECTION TESTS, PROMOTE CHECKLIST ITEM 12 ──

Goal:
  Answer the question `test_ci_stages.py` defers: whether each stage's marker
  expression SELECTS what its description claims. The subject is a fixture tree
  whose markers are known by construction, never the live suite. One live test is
  added and it asserts a PROPERTY — that no test here escapes all five stages —
  the coverage claim `ci_stages` makes in prose and has kept only by luck. Then
  pay R-0463's debt: the dry-run rule becomes §3 checklist item 12.

Bundle, in commit order:
  C0a  copy the reviewer's scratchpad original to `.agent/authored/f083-r10.md`
  C0b  mirror it byte-identically into `.agent/last_block.md`
  C1   `.agent/live_review.md` — RECORD-R9 appended at EOF, ONE commit, one body:
       gate line, blank line, the three findings and the one `Done:` line.
  C2   `tests/orchestration/test_ci_stage_selection.py` (TESTFILE, a NEW file
       written whole) plus the DOCSTRING pair in
       `tests/orchestration/test_ci_stages.py`, ONE commit — the tests land and
       the file that deferred them stops pointing at "a later round".
  C3   `docs/agents/planner_reviewer_prompt.md` — OPENER and ITEM12, ONE commit.
  C4   `.agent/plan.md` (PLAN, whole file), ONE commit.
  C5   `.agent/handoff.md`, the handback, alone.

BASE: 98900254. Re-derive `git rev-parse HEAD` before the first commit and report
whether it equals 98900254. If it does NOT, stop and hand off.

TRANSPORT: the scratchpad original of THIS block is at
`.remedy-wt/.cache/f083-r10/f083-r10.md`, which `.gitignore` drops. C0a is a byte
COPY of it — do not retype, reflow or strip anything. `cp` is denied in this
session class: copy with `python3 -c "import shutil; shutil.copyfile(a, b)"`.

SLICE CONVENTION (R-0437, §3 item 11): every slice body below is the lines
between its markers INCLUDING the trailing newline of its last line, and every
shape is declared UNDER THAT CONVENTION. The authored units are, listed and NOT
counted: RECORD-R9, TESTFILE, DOCSTRING-FROM, DOCSTRING-TO, OPENER-FROM,
OPENER-TO, ITEM12-FROM, ITEM12-TO, PLAN.

PAIR SHAPES, stated at authoring time (§4.9) and verified on these bytes:
  · DOCSTRING and OPENER are REWRITEs — FROM and TO are disjoint — each proved by
    FROM 0x and TO 1x over the whole file.
  · ITEM12 is APPEND-shaped: its TO literally CONTAINS its FROM as the LAST line,
    so "FROM 0x" is UNSATISFIABLE and is NOT ordered. Its property is FROM 1x
    before AND after, TO 0x before and 1x after.
  · TESTFILE and PLAN are WHOLE FILES, each proved by byte equality.

DRY RUN ALREADY PERFORMED, reported because §3 item 12 — which C3 lands — asks it
of me, not of you. In a disposable worktree at 98900254, from the repository root,
with the repo's own `pyproject.toml` and no substituted flag: ruff gave `All checks
passed!` exit 0 and pytest gave `9 passed` exit 0. The RED CONTROL ran too: with one
extra `tests/cli/test_redproof_slow_only.py` marked only `slow` the union test
FAILED, naming that path. Gate 8 makes you reproduce that colour.

Constraints:
  1. Change set, exactly: `.agent/authored/f083-r10.md`, `.agent/last_block.md`,
     `.agent/live_review.md`, `.agent/plan.md`, `.agent/handoff.md`,
     `tests/orchestration/test_ci_stage_selection.py`,
     `tests/orchestration/test_ci_stages.py`,
     `docs/agents/planner_reviewer_prompt.md`. Nothing else. `packages/`, `apps/`
     and `docs/roadmap/` stay EMPTY in the range diff.
  2. Apply every slice BYTE-VERBATIM. A defect in my text is a declared deviation
     in the handback, never a silent repair. Do NOT run `ruff --fix` or any
     formatter: TESTFILE already passes ruff, so reformatting is unordered change.
  3. Commit strictly in the C-order above. Push after C5. Create NO pull request.
  4. Gate 8 is the ONLY step that adds a worktree, removes it inside that same
     gate, and leaves `git worktree list` at ONE line. The red-control file is
     created INSIDE that worktree and nowhere else; the primary checkout is never
     mutated.
  5. Env-var assignment (all three forms), `cp`, `$?` inside `$(...)` and process
     substitution are denied in this session class. Capture real exit codes as
     `bash -c '<cmd>; echo "REAL_EXIT=$?"'` and use `python3` scripts under
     `.remedy-wt/.cache/f083-r10/` for all counting, hashing and byte comparison.
     A `cd` PERSISTS into later commands here; if you use one, `cd` back and print
     `pwd` before the next gate. A gate measured from the wrong directory is the
     R-0337 class — that is why gate 1 asks for `pwd`.

--- BEGIN SLICE RECORD-R9 --- (APPEND to .agent/live_review.md, C1, with exactly one blank line between the file's current last line and the first line of this slice. The blank line INSIDE this slice, between the gate line and the first finding, is part of it.)
Gate: R9 — PASS. All seventeen gates were re-run by the reviewer at the round's head, from the repository root, and every value the handback reported was reproduced exactly: TRANSPORT three-way byte-equal at sha256 322dedf6b5ca6f5f2dde8c45dc939d24088d61920fa12012c67faa76695c58d2, 23438 bytes, 250 lines, equal to the block's declared footer; the C1 prefix property holds with the tail byte-equal to `b"\n" + RECORD-R8`; every one of the ten authored slices re-extracted by marker to the digest the handback printed; the STEPS, BLANK and OPENER rewrites each read FROM 0x and TO 1x at their own commits and the ITEM11 append read FROM 1x before and after with TO 0x before and 1x after; the change set is exactly the seven declared paths with `packages/`, `tests/` and `apps/cli/command_catalog.py` empty in the range diff; the integrity gate reports passed true, fail_count 0, check_count 5, handlers=338; the open set is 92 registered, 4 `Done:`, 0 `Landed:`, open 88, max R-0464, no duplicate; `.agent/plan.md` byte-equals its PLAN slice at 30 lines; and the verification quartet is 70, 21, 15 and 42 passed, each at exit 0 from the process itself. Gate 7, the red one this round existed to clear, is GREEN — and the reviewer did not accept green on its own word: the R8 command was re-run UNCHANGED inside a disposable worktree checked out at BASE 4406f1c1, where it exited 1 with `I001 Import block is un-sorted or un-formatted` at `apps/cli/commands/ci_cmd.py:15:1`, against exit 0 and `All checks passed!` at HEAD. A gate that cannot be shown to fail is not evidence, and this one was shown to fail. The `.agent/STOP` sentinel that ended R9 was cleared by the operator before this session and is ABSENT on disk; it was never deleted by an agent. The worker's conduct was correct throughout: it applied every slice byte-verbatim, declared three deviations rather than silently repairing reviewer text, and refused to invent its own commit SHA. All three deviations are defects in MY block, not in its work, and the two findings below are charged to the reviewer accordingly. One process note belongs in this record because it nearly cost the verdict: the reviewer's first pass at gates 10 to 13 ran in a shell whose working directory had silently persisted into the BASE worktree from the red control, so a 601, an empty `git diff` and an integrity reading were all produced against 4406f1c1 while being read as HEAD. The `git diff` gate was vacuous by construction there — the range is empty at its own base. It was caught before any verdict, every affected gate was re-run at the root with `pwd` confirmed first, and the re-run values are the ones recorded above. Nothing was reported from the stale directory. This is the R-0337 family in a third medium — not import path, not configuration, but working directory — and item 12, which R10 lands, names the working directory explicitly for that reason.

- R-0465 — Medium, GATES THAT ORDER A PROPERTY AT A COMMIT WHICH CANNOT CARRY IT. The R9 block spent two of its three deviations on gates that were unsatisfiable as written, both in the same way. Gate 8 ordered the item-11 numerals to agree "over the file at C3", but four of its five anchors are created by C4 itself, so at C3 they necessarily read 0 / 1 / 0 / 0 / 1; gate 16 ordered a change set "measured BEFORE the handoff is written into C6, so it lists seven paths with `.agent/handoff.md` the seventh and last", and both clauses cannot hold at once because the seventh path is created by the very commit the measurement must precede. The worker did the right thing twice — measured what was measurable, reported both readings, declared the deviation — but each cost a round-slot of reviewer arithmetic to adjudicate, and a worker with less nerve would have fabricated the agreeing numbers instead. This is the R-0371 family, whose rule is that a block may never order a value which cannot exist at the moment the ordered text is written; the earlier instances were commit SHAs, and these two are properties pinned to the wrong commit boundary, which is the same defect wearing different clothes. Standing rule, binding the reviewer from here and already covered in spirit by §3 item 8: every done-when that names a commit states the commit at which the property FIRST holds, and when a property spans a pair of commits the gate names both readings it expects instead of one that only one of them can satisfy. OPEN.
- R-0466 — Low, A FINDING NAMED THE WRONG COMMIT FOR THE EDIT IT WAS DEFERRING. Inside RECORD-R8, finding R-0463 reads "This block does NOT place that rule in §3: C3 lands item 11 and nothing else". The R9 bundle assigns item 11 to C4 and the ruff repair to C3, so the sentence is wrong about its own block on disk: item 11 landed in bb5b8836 (C4) and 196b8f4f (C3) is the one-line ruff repair. The substance was right — the finding correctly declined to claim a promotion its change set did not order, and correctly named R10 as the round that would own it, which is precisely what §3 item 11 demands — and only the commit letter is false. The worker applied the slice byte-verbatim as constraint 2 required and declared the contradiction rather than editing reviewer text, which is the conduct this repository wants. Low because nothing downstream depended on the letter and no verdict turned on it. Refinement, binding the reviewer: when finding text names a commit inside its own block, that letter is re-read against the bundle at emission, in the same pass as §3 item 9 re-greps citations — a C-letter is a pointer, and pointers are checked, not remembered. OPEN.
- R-0467 — Low, THE STAGE TABLE'S UNION CLAIM WAS TRUE BY LUCK AND GUARDED BY NOTHING. `packages/orchestration/ci_stages.py` states in prose that the five selections' "union was the whole suite with nothing uncovered", measured once in `.agent/f083_inventory.md` Q4 at claim time. Nothing on disk kept that true afterwards. A test marked ONLY `slow` is selected by no stage at all — `fast` excludes `slow` explicitly and no other stage claims it — so a single such test would silently be run by no CI stage while the docstring went on promising full coverage. Measured at 98900254 the hole is empty: the complement of all five expressions collects 0 of 17036 tests, so the claim is TRUE today, which is exactly why this is Low rather than a defect in the table. It is registered because a claim kept by luck is indistinguishable from one kept by design right up to the commit that breaks it, and because the fix is one test rather than a redesign. RESOLVED by this round's C2: `test_a_slow_only_module_is_selected_by_no_ci_stage` pins the blind spot against the fixture tree so it is documented rather than rediscovered, and `test_no_test_in_this_repository_escapes_all_five_stages` asserts the complement collects nothing, as a property and never as a count, so it stays green as the suite grows and goes red only when a test appears that no stage would run.
Done: R-0467 — the union claim is now a live guard; see C2 of R10.
--- END SLICE RECORD-R9 ---

--- BEGIN SLICE TESTFILE --- (WHOLE FILE, a NEW file at tests/orchestration/test_ci_stage_selection.py, C2)
"""Selection tests for the F083 CI stage table, measured against a fixture tree.

`test_ci_stages.py` reads the table structurally and defers the question this
file answers: whether each stage's marker expression SELECTS what its
description claims. The subject is a FIXTURE tree whose markers are known by
construction, so every assertion pins an EXPRESSION rather than the live suite —
pinning live collected counts would go red whenever an unrelated commit added a
test, the carried finding R-0205 this feature owns. The one live-suite test
asserts a PROPERTY and never a count: that no test here escapes all five stages.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.ci_stages import CI_STAGES, ci_stage_by_name

REPO_ROOT = Path(__file__).resolve().parents[2]
LIVE_MODULES = {"test_live_only.py", "test_live_integration.py"}

#: One fixture module per marker combination the stage set distinguishes.
FIXTURE_MODULES: dict[str, tuple[str, ...]] = {
    "test_plain.py": (),
    "test_slow_only.py": ("slow",),
    "test_integration_only.py": ("integration",),
    "test_subprocess_only.py": ("subprocess",),
    "test_ui_only.py": ("ui_contract",),
    "test_smoke_only.py": ("smoke",),
    "test_live_only.py": ("real_ollama",),
    "test_subprocess_and_smoke.py": ("subprocess", "smoke"),
    "test_live_integration.py": ("integration", "real_ollama"),
}
FIXTURE_MARKERS = ("slow", "integration", "subprocess", "ui_contract", "smoke", "real_ollama")


@pytest.fixture(scope="module")
def fixture_tree(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A tiny pytest tree whose markers are known by construction, not measured."""
    tree = tmp_path_factory.mktemp("ci_stage_selection")
    ini = ["[pytest]", "markers ="] + [f"    {name}: fixture marker" for name in FIXTURE_MARKERS]
    (tree / "pytest.ini").write_text("\n".join(ini) + "\n")
    for filename, markers in FIXTURE_MODULES.items():
        lines = ["import pytest", ""] + [f"@pytest.mark.{m}" for m in markers]
        (tree / filename).write_text("\n".join([*lines, "def test_case():", "    pass", ""]))
    return tree


def collect_in_tree(tree: Path, marker_expression: str) -> set[str]:
    """The fixture modules `marker_expression` selects, by filename.

    Collection runs in a CHILD process against the tree's own config, so the
    repository's `pyproject.toml` and conftest cannot colour the result.
    """
    argv = [sys.executable, "-m", "pytest", str(tree), "-c", str(tree / "pytest.ini"),
            "--collect-only", "-q", "-p", "no:cacheprovider", "-m", marker_expression]
    done = subprocess.run(argv, cwd=tree, capture_output=True, text=True, timeout=120, check=False)
    assert done.returncode in (0, 5), done.stdout[-2000:] + done.stderr[-2000:]
    return {line.split("::")[0] for line in done.stdout.splitlines() if "::" in line}


def selection_for(tree: Path, stage_name: str) -> set[str]:
    """What the named stage's own expression selects out of the fixture tree."""
    return collect_in_tree(tree, ci_stage_by_name(stage_name).marker_expression)


def test_fast_selects_only_the_module_carrying_no_marker_at_all(fixture_tree: Path):
    assert selection_for(fixture_tree, "fast") == {"test_plain.py"}


def test_standard_selects_integration_and_subprocess_but_never_live(fixture_tree: Path):
    assert selection_for(fixture_tree, "standard") == {
        "test_integration_only.py", "test_subprocess_only.py", "test_subprocess_and_smoke.py"}


def test_ui_selects_the_ui_contract_module_alone(fixture_tree: Path):
    assert selection_for(fixture_tree, "ui") == {"test_ui_only.py"}


def test_smoke_selects_both_smoke_modules_including_the_overlapping_one(fixture_tree: Path):
    assert selection_for(fixture_tree, "smoke") == {"test_smoke_only.py", "test_subprocess_and_smoke.py"}


def test_excluded_selects_every_live_provider_module_and_only_those(fixture_tree: Path):
    assert selection_for(fixture_tree, "excluded") == LIVE_MODULES


def test_no_ci_stage_ever_selects_a_live_provider_module(fixture_tree: Path):
    """The exclusion is the honesty claim of the whole table (DECISION F083 D2)."""
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            assert selection_for(fixture_tree, stage.name) & LIVE_MODULES == set(), stage.name


def test_exactly_one_fixture_module_lands_in_two_ci_stages(fixture_tree: Path):
    """The inventory measured exactly one overlapping pair; this names it."""
    counts: dict[str, int] = {}
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            for filename in selection_for(fixture_tree, stage.name):
                counts[filename] = counts.get(filename, 0) + 1
    assert [name for name, seen in counts.items() if seen > 1] == ["test_subprocess_and_smoke.py"]


def test_a_slow_only_module_is_selected_by_no_ci_stage(fixture_tree: Path):
    """The table's one blind spot, pinned rather than rediscovered later.

    `fast` excludes `slow` and no other stage claims it, so a test marked ONLY
    `slow` would be run by nothing. The live guard below is what keeps that
    hypothetical: no such test exists today.
    """
    for stage in CI_STAGES:
        if stage.runs_in_ci:
            assert "test_slow_only.py" not in selection_for(fixture_tree, stage.name), stage.name


@pytest.mark.subprocess
def test_no_test_in_this_repository_escapes_all_five_stages():
    """The union claim in the `ci_stages` docstring, measured as a property.

    Asserts the COMPLEMENT of the five expressions collects nothing, so it stays
    green as the suite grows and reddens only when a test no stage runs appears.
    """
    union = " or ".join(f"({stage.marker_expression})" for stage in CI_STAGES)
    argv = [sys.executable, "-m", "pytest", "--collect-only", "-q",
            "-p", "no:cacheprovider", "-m", f"not ({union})"]
    done = subprocess.run(argv, cwd=REPO_ROOT, capture_output=True, text=True, timeout=600, check=False)
    assert done.returncode == 5, done.stdout[-3000:] + done.stderr[-2000:]
    assert "no tests collected" in done.stdout
--- END SLICE TESTFILE ---

--- BEGIN SLICE DOCSTRING-FROM --- (the REWRITE pair's FROM, C2; one whole line occurring exactly once in tests/orchestration/test_ci_stages.py)
different question, measured against a fixture tree in a later round — a test
--- END SLICE DOCSTRING-FROM ---

--- BEGIN SLICE DOCSTRING-TO --- (the REWRITE pair's TO, C2; replaces DOCSTRING-FROM in place, one whole line. The line that follows it in the file, beginning `pinning live collected counts`, is NOT part of this pair and is not touched.)
different question, measured against a fixture tree in test_ci_stage_selection.py — a test
--- END SLICE DOCSTRING-TO ---

--- BEGIN SLICE OPENER-FROM --- (the REWRITE pair's FROM, C3; one whole line occurring exactly once in docs/agents/planner_reviewer_prompt.md)
  eleven checks mechanically, on the FINAL bytes, after the last edit, before any
--- END SLICE OPENER-FROM ---

--- BEGIN SLICE OPENER-TO --- (the REWRITE pair's TO, C3; replaces OPENER-FROM in place, one whole line. The list gains item 12 in the same commit, so the numeral and the enumeration agree at every commit boundary.)
  twelve checks mechanically, on the FINAL bytes, after the last edit, before any
--- END SLICE OPENER-TO ---

--- BEGIN SLICE ITEM12-FROM --- (the APPEND-shaped pair's FROM, C3; one whole line occurring exactly once in docs/agents/planner_reviewer_prompt.md — the "Why this is on disk" line that closes the checklist)
  Why this is on disk and not a habit: item 2 has recurred six times across
--- END SLICE ITEM12-FROM ---

--- BEGIN SLICE ITEM12-TO --- (the APPEND-shaped pair's TO, C3; replaces ITEM12-FROM in place. It CONTAINS the FROM line unchanged as its LAST line, so item 12 is inserted immediately after item 11 and before the closing paragraph.)
  12. **A dry run executes the gate's EXACT command line.** Finding R-0463. When
      the reviewer lints, collects or runs anything to convince itself an
      authored slice is sound, it runs the command the BLOCK will order — same
      binary, same flags, same working directory, and the repository's OWN
      configuration — or the result is not evidence and may not be reported as
      if it were. The R8 instance: the authored CI slice was checked under
      `ruff check --isolated --line-length 120`, and `--isolated` discards
      `pyproject.toml` and with it the `select = ["E", "F", "W", "I", "UP"]`
      line that enables the isort rules at all, so the `I001` the worker hit was
      never EVALUATED rather than merely unreported. The probe was green because
      it was blind. Two neighbours differ from it: item 5 orders a PROBE when a
      colour is unreachable, and item 8 checks a gate's expected VALUE against
      the code, while this one governs the reviewer's own PRE-EMISSION runs,
      which no worker ever sees and no gate ever re-checks. Working directory is
      named in that list because it has since failed the same way: gates re-run
      from a shell that had silently persisted into a BASE worktree produced
      readings that were true of the wrong commit. Pair every dry run with a RED
      CONTROL — break the property on purpose inside a disposable worktree and
      confirm the command really goes red — because a command that cannot fail
      proves nothing at all when it passes.
  Why this is on disk and not a habit: item 2 has recurred six times across
--- END SLICE ITEM12-TO ---

--- BEGIN SLICE PLAN --- (WHOLE FILE replacement of .agent/plan.md, C4)
# Plan — F083 CI self-check

Branch: feature/f083-ci-self-check, cut from main after the F082 closure PR #201
merged. Next free finding id: R-0468. Open findings: the seventy-five carried out
of the F082 record plus R-0448 to R-0467 registered on this branch, of which
R-0456 to R-0459 and R-0467 are resolved. `.agent/live_review.md` is the source
of truth.

## Goal
Remedy's own repository gets an honest CI: one local command (`remedy ci`) and
matching hosted workflows run the unit and integration suites on the fake
provider, the determinism suite, the UI build plus its smoke, and budget checks,
with live-provider tests excluded by marker and said so. DONE when `remedy ci`
reproduces the hosted result locally on a clean checkout, a seeded failure fails
the right stage with a readable summary, and runtime stays within a budget.

## Current Step
R10 records the R9 PASS, registers R-0465 to R-0467, lands the per-stage
selection tests over a fixture tree with a live union guard that resolves
R-0467, and promotes R-0463's dry-run rule into §3 as checklist item 12.

## Next Steps
1. R11 adds the determinism and budget stages plus the guard-test wiring, and
   measures `fast` under `-n auto` so a runtime budget can rest on data.

## Risks
- `fast` still rests on a single 391.8 s reading, and the inventory showed it is
  inverted with respect to cost. Until that is measured under `-n auto`, no
  runtime budget can be written from measured data.
--- END SLICE PLAN ---

Done when — run every gate, record its REAL value; a gate you cannot run is reported as not run, never as green:

 1. `pwd` printed FIRST and equal to the repository root. `git status --porcelain`
    EMPTY before the first commit and before C5. `git worktree list` ONE line at
    round start and at handback. `.agent/STOP` ABSENT at both (R-0347).
 2. BASE: `git rev-parse HEAD` before the first commit; report it and whether it
    equals 98900254.
 3. TRANSPORT, bytes read in Python: sha256, bytes and lines of
    `.remedy-wt/.cache/f083-r10/f083-r10.md`, `.agent/authored/f083-r10.md` and
    `.agent/last_block.md`; whether all three are EQUAL; whether the measured line
    count equals this block's declared footer.
 4. C1 PREFIX PROPERTY over `<C1>^..<C1>`: `pre` prefixes `post`, and
    `post[len(pre):]` equals `b"\n" + RECORD-R9`, that slice extracted from the
    COMMITTED `.agent/authored/f083-r10.md` by its markers. Report the numstat;
    its deletion column must be 0.
 5. C2, both halves. `tests/orchestration/test_ci_stage_selection.py` byte-equals
    the TESTFILE slice as a whole file — report sha256, bytes, lines, and whether
    the digest is fbffda72e407c1a0ed12d99ee5a473beaccb64f9bd4fc000e556a987e7d9ce7e.
    Then over the whole `tests/orchestration/test_ci_stages.py` at C2:
    DOCSTRING-FROM 0x, DOCSTRING-TO 1x. Report the numstat.
 6. RUFF over the new file, from the repository root, NO `--isolated` and no
    substituted flag so it reads `pyproject.toml` (R-0463, §3 item 12):
    `python3 -m ruff check tests/orchestration/test_ci_stage_selection.py` —
    report REAL exit code and full output.
 7. THE NEW SUITE:
    `python3 -m pytest tests/orchestration/test_ci_stage_selection.py -q` —
    report collected count and REAL exit code. My dry run read 9 passed, exit 0.
 8. THE UNION GUARD REALLY GOES RED — a guard that cannot fail is not a guard. In
    a DISPOSABLE worktree and nowhere else:
    `git worktree add .remedy-wt/redproof-r10 HEAD --detach`; inside it create
    `tests/cli/test_redproof_slow_only.py` holding exactly `import pytest`, two
    blank lines, `@pytest.mark.slow`, `def test_case():`, `    pass`; from INSIDE
    it run `python3 -m pytest "tests/orchestration/test_ci_stage_selection.py::test_no_test_in_this_repository_escapes_all_five_stages" -q`
    and report the COLOUR and REAL exit code; then
    `git worktree remove .remedy-wt/redproof-r10 --force` and report
    `git worktree list` is ONE line again. The probe must be marked `slow` and sit
    under `tests/cli/`: `tests/conftest.py` auto-marks any `orchestration` or
    `storage` path as `integration`, which would put it in `standard` and make
    the control silently useless.
 9. C3 PAIRS over the whole `docs/agents/planner_reviewer_prompt.md` at C3; the
    two shapes DIFFER: OPENER-FROM 0x and OPENER-TO 1x (REWRITE), ITEM12-FROM 1x
    BEFORE and 1x AFTER with ITEM12-TO 0x before and 1x after (APPEND). Report all
    six. Then over the file AT C3 — the commit landing both, so every anchor
    exists there — numerals and enumeration must agree: `  12. **A dry run` 1,
    `  11. **A convention paragraph` 1, `  13. **` 0, `twelve checks mechanically`
    1, `eleven checks mechanically` 0. Report the numstat.
10. THE STRUCTURAL SUITE IS UNDISTURBED:
    `python3 -m pytest tests/orchestration/test_ci_stages.py -q` — report
    collected count and REAL exit code [BASE: 7 collected, 7 passed, exit 0].
11. THE SEAM STILL WORKS: `python3 -m pytest tests/cli/test_ci_cmd.py -q` —
    report collected count and REAL exit code [BASE: 6 collected, 6 passed, 0].
12. THE CATALOG STILL AGREES WITH ITSELF, all four paths confirmed on disk first
    (R-0438), in ONE run: `python3 -m pytest tests/test_command_catalog.py
    tests/cli/test_command_catalog.py tests/test_grouped_cli.py tests/cli/test_cli_ux.py
    -q` — report collected count and REAL exit code. These suites are parametrised
    per GROUP and this round adds none, so the count should not move from the 601
    measured at BASE (R-0464); report what you MEASURE either way.
13. VERIFICATION, each run separately, REAL exit code from the process (R-0438),
    each via `python3 -m pytest <path> -q`:
    `tests/ui_server/test_dashboard_contract.py` [70, 0];
    `tests/regression/test_resource_safety.py` [21, 0];
    `tests/orchestration/test_integrity_gate.py` [15, 0]; canary
    `tests/cli/test_golden_path.py` [42, 0].
14. NOTHING ELSE MOVED: `git diff --name-only 98900254..HEAD -- packages/ apps/
    docs/roadmap/` must print NOTHING. Report it as a measured list, and confirm
    you ran it from the repository root — at the wrong root this gate is vacuous.
15. INTEGRITY GATE, in Python because the `remedy` CLI is denied here (R-0408):
    `python3 -c "from packages.orchestration.integrity_gate import
    run_integrity_checks, export_integrity_json; import json;
    print(json.dumps(export_integrity_json(run_integrity_checks())))"` — report
    `passed`, `fail_count`, `check_count`, every check's status, and the
    `handler_import` message [BASE: handlers=338; this round adds no handler].
16. OPEN SET at HEAD: count `^- R-\d+ — ` paragraphs, `^Done: R-\d+ — ` and
    `^Landed: R-\d+ — ` lines; report all three, registered-minus-done, max id,
    next free id, any duplicate. Reviewer measured 92 / 4 / 0, max R-0464, at BASE
    and expects 95 / 5 / 0, max R-0467, open 90. Report what you MEASURE.
17. C4 PLAN byte-equals the PLAN slice as a whole file — report sha256, line count
    (under 50), `## Goal` and `## Next Steps` present, no `- [ ]` line, and the
    count of numbered items under `## Next Steps`.
18. CHANGE SET at C4 — SEVEN paths, `.agent/handoff.md` being written by C5 and so
    absent from any measurement preceding it: `git diff --name-only
    98900254..HEAD`. Report the list and count; name `.agent/handoff.md` the
    eighth path C5 adds.
19. Insertions (`+` column only) for C0a through C4 — report each; none over 500.
    C0b is a verbatim single-`.agent/`-file rewrite, AGENTS.md-exempt; report it
    anyway. C5's own count cannot exist inside C5 (R-0149): final message.

The push result, post-C5 clean-tree reading and open-PR list postdate C4, so per
R-0449 and R-0452 they are NOT ordered into that file: run `git push -u origin
feature/f083-ci-self-check` after C5, create no PR, report all three in the final message.

Handback: rewrite `.agent/handoff.md` per docs/agents/handback_template.md, as C5
— feature and round, branch, per-commit changed-files tables, every gate value
above, the item-status table covering every C-item and gate, open findings with
max and next free id, and next action R11 as the plan states it. C5 cannot table
its own SHA (R-0371, R-0149); say so. Over a cap, name BOTH caps (R-0462). Fortschritt, verbatim:

Fortschritt: 38 % (F083 beansprucht · R1 bis R7 und R9 PASS, R8 FAIL auf einem roten ruff-Gate und in R9 repariert · Stage-Tabelle, Stage-Runner und die `remedy ci` CLI-Naht als Code gelandet, dazu die Selektionstests, die jede Marker-Expression gegen einen Fixture-Baum festnageln, plus ein Live-Wächter gegen Tests, die keine Stage erfasst · noch keine hosted workflows, keine Determinismus- oder Budget-Stage) — gemessen, nicht geschätzt

If any gate is RED, or anything here contradicts what you find on disk: finish the
commit you are in, write the handoff naming the exact blocker, end. Do not widen
scope to route around it (G8).

BLOCK SIZE, measured on these final bytes: 399 lines (cap 400, DECISION F105 D5).
──────────────────────────────────────────────────────────────────────────────
