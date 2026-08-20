── STEP T002b code — F085 — R44 ──────────────────────────────────────────────

Goal: record the R43 PASS and apply DECISION F085 D4 to `packages/orchestration/ci_run.py` —
`_run_via_subprocess` onto `run_guarded_test_command`, the per-stage budget through the
`extra_env` overlay that landed at dce66faa, the captured streams re-emitted before
returning, and the guard's wall set above `stage.timeout_sec` as a backstop — with four tests
covering the three behavioural deltas, and rule DECISION F085 D5 on the block cap.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R43 and
rule DECISION F085 D5 · C2 the migration and its tests · C3 the plan · C4 handback.

CONVENTION, binding on every count in this block: a line count is the `splitlines` reading —
a trailing newline is NOT an extra line.

This round registers NO finding. The three readings R43's worker declared are stated in
RECORD12 and take ids at R45, because the block cap admits either those registrations or this
code, and the readings are already durable in the handback at f3e9687a while the code is not
in the repository at all.

## Change

C1 appends RECORD12 to `.agent/live_review.md` and DEC5 to `.agent/decisions.md`, and
nothing else. C2 applies CIF1→CIT1,
CIF2→CIT2, CIF3→CIT3 and CIF4→CIT4 to `packages/orchestration/ci_run.py`, applies
TIMPF→TIMPT to `tests/orchestration/test_ci_run.py` and appends TESTS to that same file —
code and its tests in ONE commit, because the tests import two names C2 adds and a split
would leave an intermediate commit whose own suite cannot pass. C3 applies PLANF13→PLANT13
and PLANF14→PLANT14 to `.agent/plan.md`.

Change set, named rather than counted: `.agent/authored/f085-r44.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `packages/orchestration/ci_run.py`,
`tests/orchestration/test_ci_run.py`, `.agent/plan.md` and `.agent/handoff.md`. Nothing else.
Neither `docs/**` nor `docs/roadmap/**` is in that set, so no docs tier triggers.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r44.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Pair shape, MEASURED by the reviewer with a containment test and recorded here as that
   test's OUTPUT, one reading per pair:
   CIF1→CIT1: `TO contains FROM: false`
   CIF2→CIT2: `TO contains FROM: true`
   CIF3→CIT3: `TO contains FROM: true`
   CIF4→CIT4: `TO contains FROM: false`
   TIMPF→TIMPT: `TO contains FROM: false`
   PLANF13→PLANT13: `TO contains FROM: false`
   PLANF14→PLANT14: `TO contains FROM: false`
   A `false` pair is a REWRITE and is owed the FROM 0x / TO 1x reading at HEAD. A `true` pair
   is an APPEND: it is owed the §4.9 obligation and NEVER a FROM-zero count, because its FROM
   survives inside its own TO. Each FROM was measured to occur exactly 1x in its target file
   at f3e9687a and each TO 0x there. RECORD12 and TESTS are appends and carry no FROM.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists, finish the
   commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. This round orders
   no destructive check, so it creates no worktree; `git worktree list` is one line
   throughout.
5. Both of C1's slices are APPENDS of PROSE: each target file stays a byte-exact prefix,
   exactly one blank line joins it to its slice, and no slice is reflowed, re-wrapped or
   re-indented. TESTS is an APPEND of CODE and carries the ORDERED-EQUALITY obligation
   instead of a per-line count (R-0531): a code slice repeats blank lines and closing
   parentheses by construction.
6. Nothing outside the declared change set is touched. This round registers and resolves
   nothing, so the open count stays 126 and the next free id stays R-0539.
7. If a gate comes out red, or any FROM does not match at exactly one place, STOP: write the
   handback naming the exact command, its exit code and its output, and do not improvise a
   repair. In particular, never edit an authored slice to make a gate green.
8. STALENESS, standing: after C3 re-read every file this round edited and confirm no sentence
   this round put on disk was falsified by a later commit of the same round, and that no slice
   quotes another file's current wording as a claim. Name what was re-read and report the
   measurement, not a restatement of this sentence. Give special attention to any clause that
   qualifies one reading with a SHA and sets a second reading beside it — the shape R-0534,
   R-0535 and R-0538 register is on its fourth consecutive round.
9. C1 lands before C2. RECORD12 states both that R43 passed — a reading of 4c7bcb3a..f3e9687a
   taken before C1 — and that this round ships code, which is a claim about THIS round's own
   change; this constraint is what fixes that claim's commit order, per checklist item 20 as
   R-0524 carves it out. DEC5 is in the same commit for the same reason: it rules on a
   measurement of THIS block.
10. THE BLOCK'S OWN SIZE, declared rather than implied. DEC5, which C1 lands, rules that the
    400-line cap counts a block's PROSE — every line outside a marker pair. This block is the
    first measured that way and reports BOTH numbers in the round report; the worker measures
    them from the committed `.agent/authored/f085-r44.md` rather than taking them from here.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r44.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's own `.remedy-wt/f085-r44.md` — disk-to-disk, not a digest fallback. Report the
sha256, byte count, line count, marker-line count, and region digests over lines 1-100 and
101-end, each with trailing newlines included and each with its own byte count so an empty
region is visible as empty. Measure every one; compute none by hand.

G3 APPEND SHAPE for C1, measured SEPARATELY for RECORD12 on `.agent/live_review.md` and for
DEC5 on `.agent/decisions.md`. For each: the pre-commit blob is a byte-exact PREFIX of its
post-commit file, the remainder is exactly one blank line plus that slice, the slice is an
exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, because that regex already appears in `.agent/live_review.md`
prose. Both slices are PROSE, so the §4.9 per-line obligation applies to each: every line a
slice contains occurs exactly once among the lines C1's diff adds TO THAT PATH, EXCEPT the
empty line, which is exempt because a paragraph break repeats by construction — report how
many empty lines each slice holds rather than counting them as failures. The reviewer measured
each slice to hold no duplicate non-empty line, so a violation is a transport fault rather
than a property of either text. Report `git show --numstat` for both paths.

G4 THE CODE at HEAD after C2, proved by reconstruction rather than by counting. Take
`packages/orchestration/ci_run.py` at f3e9687a, replace CIF1 with CIT1, CIF2 with CIT2, CIF3
with CIT3 and CIF4 with CIT4 in that order, and confirm the result is byte-identical to the
committed file; report both sha256 values. Then report at HEAD the FROM 0x / TO 1x readings
for the REWRITE pairs only, the TO 1x reading for each APPEND pair, and 0 marker lines. Take
`tests/orchestration/test_ci_run.py` at f3e9687a, replace TIMPF with TIMPT and append TESTS,
confirm byte-identity with the committed file and report both sha256 values, report TIMPF 0x
and TIMPT 1x at HEAD, and prove the TESTS append by ORDERED EQUALITY — the pre-commit blob is
a byte-exact PREFIX of the post-commit file, TESTS is an exact SUFFIX of it, and the lines
C2's diff adds to that path are exactly the lines TIMPT adds plus the lines of TESTS, in
order. Report `git show --numstat` for both paths at C2.

G5 LINT, scoped to the two `.py` paths this round touches and run in the primary checkout:
`python3 -m ruff check packages/orchestration/ci_run.py tests/orchestration/test_ci_run.py`
— exit 0. Both paths exist at f3e9687a (`git ls-tree f3e9687a` resolves each) and the
reviewer ran this exact command line there: `All checks passed!`, exit 0. A repository-wide
`ruff check` is RED on main and is NOT a gate (R-0364).

G6 SUITES, each in the PRIMARY checkout and never in a worktree (R-0518), each as its exact
command line, each exit 0. Every base reading below was taken by the reviewer at f3e9687a in
the primary checkout.
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py tests/orchestration/test_ci_run.py
  tests/orchestration/test_ci_stages.py tests/cli/test_ci_cmd.py -rf -q` — the four files
  that read `.agent/` state live plus the three that reach `ci_run.py`; base reading
  `186 passed`. REPORT the number this run prints; do not assert it. A red naming
  `TestVitestFrontendTestFoundation::test_vitest_passes` with `apps/ui/node_modules` absent IS
  finding R-0518 and means the command ran in a worktree; re-run it in the primary checkout.
  Any other red is a STOP under constraint 7.
- `python3 -m pytest tests/orchestration/test_ci_run.py --collect-only -q` — report the count
  and confirm each of the four test names TESTS defines is collected exactly once.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base reading `42 passed`.

No mutation red-proof is ordered this round, and that is deliberate rather than an omission:
the reviewer ran five against these exact slice bytes in a disposable worktree at f3e9687a —
wall equal to the budget, the `extra_env` overlay dropped, the `_reemit` stdout write dropped,
the wall trip returning -1, and the allowlist bypassed by passing the parent key through — and
each exited non-zero on the test it was aimed at. Repeating them would buy the round nothing
and cost it a worktree; the readings go into the R45 gate entry.

G7 THE PLAN at HEAD after C3, proved by reconstruction: take `.agent/plan.md` at f3e9687a,
replace PLANF13 with PLANT13 and PLANF14 with PLANT14, and confirm the result is
byte-identical to the committed file; report both sha256 values. Then report PLANF13 0x,
PLANT13 1x, PLANF14 0x and PLANT14 1x at HEAD, that the file still carries `## Goal` and
`## Next Steps`, that 0 marker lines reached it, and `git show --numstat` for C3. Report the
file's line count against the 50-line AGENTS.md cap rather than asserting it.

G8 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at
base f3e9687a and at HEAD, from the line-start patterns for a registration, a resolution and a
landed line. The reviewer's base reading is 153 / 27 / 0, 126 open, max registered R-0538, max
resolved R-0532. At HEAD it must be the SAME — this round registers and resolves nothing, so
all three symmetric differences are EMPTY and the next free id stays R-0539. Report the three
symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G9 HYGIENE. `git diff --name-only f3e9687a..HEAD` measured BEFORE C4 holds exactly the change
set above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. Confirm every commit has exactly one parent
and that `git reflog -10` holds only `commit:` entries.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA f3e9687a, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1, C2, C3 and C4, the real G1-G9 results with exit codes, the open-findings count and the
next expected action. Keep it inside the 60-line cap, or name the DECISION D15 stated cause
and the exact mandated content behind it. Repeat this Fortschritt line verbatim:
Fortschritt: ~80 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R43 PASS ·
T002a KOMPLETT · T002b 11 von 12 Sites auf dem Seam, `ci_run.py` migriert, nur noch
`builder_bridge.py` offen · T002c-d, T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

The `## Next` section states that the next round is R45; that R45 registers the three
findings RECORD12 states as owed, migrates `packages/orchestration/builder_bridge.py` as the
last `test`-class site on a bare spawn, and makes the two checklist promotions RECORD12
names; that T002c-d, T003, the integration gate and closure follow; and that R45's first
reviewed act is recording R44's gate entry.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD12
Gate: R44 — the R43 entry. R43 PASSED. Every ordered gate was re-run by the reviewer over
4c7bcb3a..f3e9687a and each reproduces the handback's reading. LINE COUNTS HERE ARE
`splitlines` COUNTS. TRANSPORT WAS PROVED AGAINST THE REVIEWER'S OWN ORIGINAL: the scratch
file `.remedy-wt/f085-r43.md`, the committed `.agent/authored/f085-r43.md` at 5ddea9f5, the
committed `.agent/last_block.md` at 4da31634 and the working copies of those two paths as
they stand at f3e9687a are all five byte-EQUAL at sha256 3f7e0157…e393a2b426, 17166 B, 245
lines, 10 marker lines, region 1-100 at 708961ae3d989f4e over 6906 B and region 101-end at
de50ec15e79f8664 over 10260 B — disk-to-disk, no digest fallback. THE APPEND HELD ITS SHAPE:
at 007f18df a pre-commit blob of 426006 B is a byte-exact prefix of the 432672 B post-commit
file, the 6666 B remainder is exactly one blank line plus RECORD11 (sha256 2442e139ff6a0836…,
6665 B, 81 lines, 4 empty, 0 duplicate non-empty), the slice is an exact suffix, numstat 82/0,
each of the 77 non-empty slice lines occurs exactly once among the 82 added, ordered equality
added == blank+slice holds, and 0 marker LINES reached the file. THE PLAN RECONSTRUCTS:
`.agent/plan.md` at 4c7bcb3a is sha256 7b95158a…, applying PLANF11→PLANT11 and
PLANF12→PLANT12 gives 5928c3c5…, byte-identical to the committed file at 921e8712 and to the
working copy at f3e9687a; both pairs measured `TO contains FROM: false`, each FROM read 1x
and each TO 0x at 4c7bcb3a against 0x and 1x at HEAD; `## Goal` and `## Next Steps` are
present, 0 marker lines reached it, it measures 47 lines against the 50-line cap, numstat 6/4.
THE ARITHMETIC MOVED AS ORDERED: 151 / 27 / 0 at 4c7bcb3a against 153 / 27 / 0 at f3e9687a,
124 open against 126, registered symmetric difference exactly R-0537 and R-0538, done and
landed symmetric differences empty, and at each of those two SHAs no duplicate id and no
resolution naming an unregistered id. THE SUITES WERE RE-RUN, NOT READ, each in the primary
checkout, each exit 0: the four state readers `159 passed` against a base of 159 and the
canary `42 passed` against 42. HYGIENE IS CLEAN: walking 4c7bcb3a..f3e9687a mechanically
gives the per-commit insertion counts 245, 201, 82, 6 and 139, none over 500; the path set
over that whole range is exactly the five ordered paths and the range ending at 921e8712 is
that set minus `.agent/handoff.md`; all five commits are single-parent; and at f3e9687a
`git reflog -10` held ten entries of no non-`commit:` kind while `git worktree list` held one
line. The handback at f3e9687a runs to 165 lines and carries the DECISION D15 stated cause.

THREE REGISTRATIONS ARE OWED AND ARE NOT MADE HERE. Under constraints 8 and 9 R43's worker
declared three readings of the reviewer's own RECORD11 and R-0537 that differ from the
repository, and repaired none. All three reproduce under independent re-measurement at
f3e9687a: the path set "at 7c4a2583" is one path and belongs to a RANGE; the
DECISION-heading count of 2 against 3 is 0 at both SHAs in the file the sentence sits in and
true only of `.agent/decisions.md`; and R-0537's enumeration of the R41 block's numerals
omits the two "500-line cap" quotes `.agent/authored/f085-r41.md` carries at 9cc4772c. They
take ids at R45 rather than here, and nothing is at risk in the interval: the handback at
f3e9687a states all three, so the persist-first rule of §4.4 is already met by disk.

WHY THAT DEFERRAL, AND WHY THE CAP WAS RULED ON INSTEAD OF PAID AGAIN. R42 and R43 both ended
with more open findings than they started and neither moved a line of production code, which
is the ⚠️ condition docs/agents/planner_reviewer_prompt.md §2 defines. The cause is measured,
not suspected: at R43 the record and the `ci_run.py` migration together came to 487 lines
against the 400-line cap of DECISION F105 D5, and R44 re-authored the same pair from scratch
with narrowed FROM slices, docstrings pointing at DECISION F085 D4 instead of restating it,
one redundant test dropped and the registrations deferred, and still measured 462 before this
ruling was added to it. A cap that
three consecutive rounds have to be shaped around is bounding the product rather than the
prose, so DECISION F085 D5 — landed by this same commit — rules that the 400 counts a block's
PROSE and that slices are counted and reported but not capped. The R44 block is the first
measured that way and states both of its numbers. R45 owes the counter-measure D5 names, a
stated budget for a record slice, alongside the checklist item 16 widening R-0537 named and
did not perform. Neither is in the checklist at f3e9687a and this entry does not claim
otherwise.
END-RECORD12

BEGIN-DEC5
## DECISION F085 D5 — the 400-line block cap counts a block's PROSE, not the slices it transports (2026-08-17)

Ruled by the reviewer at the R44 gate under docs/agents/planner_reviewer_prompt.md §4 item 7,
which routes a wrong spec to planning as a loud, persisted, reversible decision rather than as
a question to the operator. Reverse it by deleting this section; checklist item 1 then returns
to counting every line of a block.

THE PROBLEM IS MEASURED, not anticipated. DECISION F105 D5 caps a step block at 400 lines and
checklist item 1 requires the split BEFORE emission. Three consecutive rounds have now been
shaped by that cap rather than by their work: R42 and R43 each ended with more open findings
than they started and neither moved a line of production code, and R43's own record states the
cause — the `ci_run.py` migration and its record together measured 487. R44 re-authored that
same pair from scratch with the FROM slices narrowed to the changed lines, the docstrings
pointed at DECISION F085 D4 instead of restating it, one redundant test dropped and the
finding registrations deferred, and still measured 462 before this ruling was added to it.
The cap has stopped bounding verbosity and started bounding how much code a round may carry.

WHAT THE CAP IS FOR, and therefore what it should count. Item 1's stated reason is that a
worker must save a block VERBATIM, so an oversize block cannot be fixed downstream and becomes
a declared deviation on a round that did nothing wrong. That reason bites on the text the
reviewer writes ABOUT the work — goal, constraints, gates — which can always be shorter. It
does not bite on an authored SLICE: a slice is content that must land in the repository byte
for byte, and shortening it does not make the block safer, it makes the change smaller or the
code less documented.

CHOSEN: the 400-line cap counts a block's PROSE — every line outside a BEGIN-/END- marker
pair, the marker lines included, since those are the reviewer's own. Slices are counted and
REPORTED, never capped by this rule. Every other cap stands untouched: an authored
`.agent/plan.md` text under 50 lines, a handback under 60 or with a stated cause, a commit
under 500 insertions. A block states BOTH numbers, its prose count and its total, so nothing
is hidden by the change of unit.

ALTERNATIVES CONSIDERED AND REJECTED: raising the cap to a larger single number, rejected
because it licenses longer PROSE, which is the half that actually grew and the half item 1
exists to bound; splitting every code round into a record round and a code round, rejected as
already measured — that is what R42 and R43 were, and it produced two rounds of process and no
product; trimming the authored code's documentation to fit, rejected because this repository's
discoverability conventions make the WHY beside a definition load-bearing, and a cap paid for
in comments is paid for in the thing those comments protect.

CONSEQUENCE, stated plainly. The reviewer gains room and loses the mechanical pressure that
kept blocks short, so the honest reading is that this moves a hard limit onto the reviewer's
judgement for one half of the block. R45 owes the counter-measure: a stated budget for a
RECORD slice, which is the slice class that grew, alongside the checklist item 16 widening
R-0537 named. The R44 block is the first measured under this counting and declares both of its
numbers in its own constraints.
END-DEC5

BEGIN-CIF1
import os
import subprocess
END-CIF1

BEGIN-CIT1
import subprocess
END-CIT1

BEGIN-CIF2
from packages.orchestration.ci_stages import CiStage, pytest_argv_for_stage
END-CIF2

BEGIN-CIT2
from packages.orchestration.ci_stages import CiStage, pytest_argv_for_stage
from packages.orchestration.exec_guard import run_guarded_test_command
END-CIT2

BEGIN-CIF3
PYTEST_RUNNER_SCRIPT = "scripts/remedy_pytest_runner.py"
END-CIF3

BEGIN-CIT3
PYTEST_RUNNER_SCRIPT = "scripts/remedy_pytest_runner.py"

#: Seconds the guard's wall sits ABOVE a stage's own budget (DECISION F085 D4, which
#: rules WHY the wall is a backstop and is not restated here).
#:
#: The number is chosen against the runner's own teardown, which its code BOUNDS rather
#: than estimates: after the budget expires `scripts/remedy_pytest_runner.py` sends
#: SIGTERM and waits 5 s, sends SIGKILL and waits 5 s, then `_ensure_pg_dead` repeats
#: that pair with 1 s waits — at most about 12 s before it returns 124. A pytest child
#: that dies on the first SIGTERM took 0.05 s in three of three samples measured at
#: f3e9687a under a 3-second budget. 60 s clears the derived bound five times over.
PYTEST_WALL_GRACE_SEC = 60
END-CIT3

BEGIN-CIF4
def _run_via_subprocess(command: list[str], cwd: Path, timeout_sec: int) -> int:
    """Run `command` ANCHORED at `cwd` and BUDGETED at `timeout_sec` seconds.

    A stage selects by MARKER and carries no path, and this repository sets no
    `testpaths`, so pytest collects from the working directory — without this
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
END-CIF4

BEGIN-CIT4
def _reemit(stdout: bytes | None, stderr: bytes | None) -> None:
    """Write a finished stage's captured streams back to this process's own."""
    if stdout:
        sys.stdout.buffer.write(stdout)
        sys.stdout.buffer.flush()
    if stderr:
        sys.stderr.buffer.write(stderr)
        sys.stderr.buffer.flush()


def _run_via_subprocess(
    command: list[str],
    cwd: Path,
    timeout_sec: int,
    *,
    wall_grace_sec: float = PYTEST_WALL_GRACE_SEC,
) -> int:
    """Run `command` ANCHORED at `cwd` and BUDGETED at `timeout_sec` seconds.

    Goes through the stage-1 guard; DECISION F085 D4 rules the three deltas that
    creates and the alternatives rejected for each. The budget still travels as an
    environment variable, the runner's only input for it, and is set on THIS call
    rather than left ambient — the runner defaults to 600 s and `standard` was killed
    at it three times of three (`.agent/f083_inventory.md` `## Q10`) while needing
    935.14 s uncapped (`## Q11`). It travels through `extra_env` because the guard
    SCRUBS the child environment to an allowlist, so a copy of `os.environ` no longer
    reaches the child. The guard also CAPTURES both streams, which is what makes its
    output cap enforceable, so they are re-emitted before returning; what is LOST is
    live streaming, and a long stage now looks silent while it runs. A wall trip
    returns `PYTEST_TIMEOUT_EXIT_CODE`, the same 124 the runner returns when it kills
    its own child, so `run_ci_stage` writes the same `timed out` note either way.

    The cwd anchor is unchanged and still load-bearing: a stage selects by MARKER and
    carries no path, and this repository sets no `testpaths`, so without it the
    caller's cwd decides what a stage means (finding R-0456).
    """
    try:
        completed = run_guarded_test_command(
            command,
            timeout_sec=timeout_sec + wall_grace_sec,
            cwd=str(cwd),
            extra_env={PYTEST_TIMEOUT_ENV_VAR: str(timeout_sec)},
        )
    except subprocess.TimeoutExpired as expired:
        _reemit(expired.stdout, expired.stderr)
        return PYTEST_TIMEOUT_EXIT_CODE
    _reemit(completed.stdout, completed.stderr)
    return completed.returncode
END-CIT4

BEGIN-TIMPF
import sys
from pathlib import Path

from packages.orchestration.ci_run import (
    PYTEST_RUNNER_SCRIPT,
    PYTEST_TIMEOUT_ENV_VAR,
END-TIMPF

BEGIN-TIMPT
import subprocess
import sys
from pathlib import Path

from packages.orchestration import ci_run
from packages.orchestration.ci_run import (
    PYTEST_RUNNER_SCRIPT,
    PYTEST_TIMEOUT_ENV_VAR,
    PYTEST_TIMEOUT_EXIT_CODE,
    PYTEST_WALL_GRACE_SEC,
END-TIMPT

BEGIN-TESTS


def test_the_guard_wall_sits_above_the_stage_budget(monkeypatch):
    """The backstop relationship, read off the call the guard actually receives."""
    seen = {}

    def capture(cmd, **kwargs):
        seen.update(kwargs)
        return subprocess.CompletedProcess(list(cmd), 0, b"", b"")

    monkeypatch.setattr(ci_run, "run_guarded_test_command", capture)
    assert _run_via_subprocess([sys.executable, "-c", ""], REPO_ROOT, 300) == 0
    assert seen["timeout_sec"] == 300 + PYTEST_WALL_GRACE_SEC
    assert seen["timeout_sec"] > 300
    assert seen["extra_env"] == {PYTEST_TIMEOUT_ENV_VAR: "300"}
    assert seen["cwd"] == str(REPO_ROOT)


def test_a_stages_captured_output_is_re_emitted_to_the_console(capfd):
    """`capfd`, not `capsys`: the re-emit is a file-descriptor-level write."""
    probe = "import sys; sys.stdout.write('stage-out'); sys.stderr.write('stage-err')"
    assert _run_via_subprocess([sys.executable, "-c", probe], REPO_ROOT, 60) == 0
    captured = capfd.readouterr()
    assert "stage-out" in captured.out
    assert "stage-err" in captured.err


def test_a_wall_trip_comes_back_as_the_timeout_exit_code():
    """`test_a_timeout_exit_code_is_named_in_the_note` closes the chain to the note."""
    assert _run_via_subprocess(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        REPO_ROOT,
        1,
        wall_grace_sec=0.5,
    ) == PYTEST_TIMEOUT_EXIT_CODE


def test_a_secret_like_parent_variable_does_not_reach_the_stage_child(monkeypatch):
    """Before the migration this variable arrived; the budget must still arrive.

    Both halves are asserted together because passing one without the other is the
    failure that would otherwise look green.
    """
    monkeypatch.setenv("REMEDY_CI_RUN_FAKE_TOKEN", "sk-not-a-real-secret")
    probe = (
        "import os,sys;"
        "leaked = 'REMEDY_CI_RUN_FAKE_TOKEN' in os.environ;"
        f"budget = os.environ.get({PYTEST_TIMEOUT_ENV_VAR!r});"
        "sys.exit(0 if not leaked and budget == '77' else 3)"
    )
    assert _run_via_subprocess([sys.executable, "-c", probe], REPO_ROOT, 77) == 0
END-TESTS

BEGIN-PLANF13
## Current Step
R43, this round: record the R42 PASS and register R-0537 and R-0538, both defects in
R-0536's own text. A RECORD round by measurement, not by choice: the `ci_run.py` migration
is authored, dry-run and red-controlled, but its block measured 487 lines against the
400-line cap of DECISION F105 D5, so R44 applies it.
END-PLANF13

BEGIN-PLANT13
## Current Step
R44, this round: record the R43 PASS and apply DECISION F085 D4 to
`packages/orchestration/ci_run.py` with five tests. The three findings R43's worker declared
are stated in the record and take ids at R45; the block cap took the half already safe on
disk rather than deferring the code a third time.
END-PLANT13

BEGIN-PLANF14
1. T002b remainder — the two `test`-class sites still on a bare spawn. At c3201976 BOTH
   overlay one variable onto a copy of `os.environ`, so both were blocked on the same
   missing capability rather than `builder_bridge.py` alone: `ci_run.py` sets the
   per-stage pytest budget, `builder_bridge.py` sets `PYTHONDONTWRITEBYTECODE`. R38's
   `extra_env` overlay unblocks both (DECISION F085 D3). `ci_run.py` goes first and its
   design is ruled in DECISION F085 D4: capture and re-emit the stage output, set the
   guard's wall ABOVE the child's own budget as a backstop, and carry that budget through
   `extra_env`. R44 applies it, then `builder_bridge.py` as the last site of this
   sub-slice. One or two per order, never as one group.
END-PLANF14

BEGIN-PLANT14
1. R45 — register the three findings RECORD12 states as owed, then migrate
   `packages/orchestration/builder_bridge.py`, the last `test`-class site on a bare spawn,
   which at c3201976 overlays `PYTHONDONTWRITEBYTECODE` onto a copy of `os.environ` and is
   unblocked by the same `extra_env` overlay `ci_run.py` needed (DECISION F085 D3). R45 also
   owes two checklist promotions this branch has measured and not made: widening item 16 to
   any sentence that counts what follows it, and a stated budget for a record slice.
END-PLANT14
