── STEP T002b close — F085 — R45 ─────────────────────────────────────────────

Goal: record the R44 PASS, register the eight findings R43 and R44 left owed, rule DECISION
F085 D6 on the block budget the 500-insertion commit cap actually leaves, migrate
`packages/orchestration/builder_bridge.py` onto `run_guarded_test_command` as the last
`test`-class site DECISION F085 D3 names. The checklist item 16 widening R-0537 asked for is
NOT in this round: the block measured 497 lines against DEC6's 490-line budget with it in, and
under a cap the product ships first. R46 carries it, and PLANT2 says so on disk.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R44, register
R-0539 through R-0546 and rule DECISION F085 D6 · C2 the migration and its two tests · C3 the
plan · C4 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line.

## Change

C1 appends RECORD13 to `.agent/live_review.md` and DEC6 to `.agent/decisions.md`. C2 applies
BBF1→BBT1, BBF2→BBT2, BBF3→BBT3 to `packages/orchestration/builder_bridge.py`, applies
TIMPF→TIMPT to `tests/orchestration/test_builder_bridge.py` and appends TESTS to that same
file — code and tests in ONE commit, because TESTS references a name BBT2 imports and a split
would leave an intermediate commit whose own suite cannot pass. C3 applies PLANF1→PLANT1 and
PLANF2→PLANT2 to `.agent/plan.md`.

Change set, named rather than counted: `.agent/authored/f085-r45.md`, `.agent/last_block.md`,
`.agent/live_review.md`, `.agent/decisions.md`, `packages/orchestration/builder_bridge.py`,
`tests/orchestration/test_builder_bridge.py`, `.agent/plan.md`, `.agent/handoff.md`. Nothing
else; neither `docs/**` nor `docs/roadmap/**` is in that set, so the §3 docs tier does not
trigger.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r45.md` by its marker pair. Never retype one, never apply one from
   the prompt. Marker lines never reach a target file.
2. Pair shape, MEASURED by the reviewer with a containment test and recorded as that test's
   OUTPUT, one reading per pair: BBF2→BBT2 `TO contains FROM: true`, an APPEND owed the §4.9
   obligation and never a FROM-zero count; each of BBF1→BBT1, BBF3→BBT3, TIMPF→TIMPT,
   PLANF1→PLANT1 and PLANF2→PLANT2 `TO contains FROM: false`, a REWRITE owed the FROM 0x /
   TO 1x reading at HEAD. Each FROM was measured to occur exactly 1x in its target at
   981d08d0. NO base reading of a TO is ordered, because BBT2 contains BBF2 and a "TO 0x at
   base" clause is unattainable for it — finding R-0544, which this block registers, and this
   constraint is the first text written under it. RECORD13, DEC6 and TESTS carry no FROM.
3. Re-read `.agent/STOP` from disk before C0a and again before C4; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit; this round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line.
4. Both of C1's slices are APPENDS of PROSE: each target file stays a byte-exact prefix,
   exactly one blank line joins it to its slice, and no slice is reflowed or re-indented.
   TESTS is an APPEND of CODE, carrying the ORDERED-EQUALITY obligation instead of a per-line
   count (R-0531).
5. Nothing outside the declared change set is touched. This round registers R-0539 through
   R-0546 and resolves nothing: the open count goes 126 → 134, next free id R-0547.
6. If a gate comes out red, or any FROM does not match at exactly one place, STOP: write the
   handback naming the exact command, its exit code and its output. Never edit a slice to
   make a gate green.
7. STALENESS, standing: after C3 re-read every file this round edited and confirm no sentence
   this round put on disk was falsified by a later commit of the same round, and that no
   slice quotes another file's current wording as a claim. Report the measurement, not a
   restatement. Give special attention to any clause qualifying one reading with a SHA and
   setting a second beside it — the R-0534 / R-0535 / R-0538 shape, now on its fifth round.
8. C1 lands before C2. RECORD13 states that R44 passed — a reading of f3e9687a..981d08d0 taken
   before C1 — and also what THIS round's C2 changes, a claim about this round's own commits;
   this constraint fixes that claim's commit order per checklist item 20 as R-0524 carves it
   out. DEC6 rides in the same commit because it rules on a measurement of THIS block.
9. THE BLOCK'S OWN SIZE. DEC6, which C1 lands, budgets a block at 490 lines TOTAL and keeps
   D5's 400-line PROSE cap. The reviewer measured both at emission and states them here:
   PROSE 219, TOTAL 477. The worker re-measures both from the committed
   `.agent/authored/f085-r45.md` and reports them; a mismatch is a finding against this block,
   not against the worker.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 3; `git status --porcelain`
empty at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r45.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the
reviewer's `.remedy-wt/f085-r45.md` — disk-to-disk, not a digest fallback. Report sha256, byte
count, line count, marker-line count, and region digests over lines 1-100 and 101-end,
trailing newlines included, each with its own byte count. Measure every one.

G3 APPEND SHAPE for C1, measured SEPARATELY for RECORD13 on `.agent/live_review.md` and DEC6
on `.agent/decisions.md`. For each: the pre-commit blob is a byte-exact PREFIX of its
post-commit file, the remainder is exactly one blank line plus that slice, the slice is an
exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file — count marker
LINES, never the substring, since that regex already appears in `.agent/live_review.md` prose.
Both are PROSE, so §4.9's per-line obligation applies: every line a slice contains occurs
exactly once among the lines C1's diff adds TO THAT PATH, EXCEPT the empty line — report each
slice's empty-line count. Neither slice was measured to hold a duplicate non-empty line, so a
violation is a transport fault. Report `git show --numstat` for both paths.

G4 THE CODE at HEAD after C2, proved by reconstruction. Take
`packages/orchestration/builder_bridge.py` at 981d08d0, replace BBF1 with BBT1, BBF2 with BBT2
and BBF3 with BBT3 in that order, confirm byte-identity with the committed file, report both
sha256 values. Then at HEAD report FROM 0x / TO 1x for the REWRITE pairs only, TO 1x for
BBF2→BBT2, and 0 marker lines. Take `tests/orchestration/test_builder_bridge.py` at 981d08d0,
replace TIMPF with TIMPT and append TESTS, confirm byte-identity, report both sha256 values and
TIMPF 0x / TIMPT 1x at HEAD, and prove the TESTS append by ORDERED EQUALITY: the base blob WITH
TIMPF→TIMPT ALREADY APPLIED is a byte-exact PREFIX of the post-commit file, TESTS is an exact
SUFFIX of it, and the lines C2's diff adds to that path are exactly the lines TIMPT adds plus
the lines of TESTS, in order. The prefix is stated against that intermediate text and NOT
against the pre-commit blob, because C2 rewrites the import block of the same file it appends
to — finding R-0545, which this block registers. Report `git show --numstat` for both paths.

G5 LINT, scoped to the two `.py` paths and run in the primary checkout: `python3 -m ruff check
packages/orchestration/builder_bridge.py tests/orchestration/test_builder_bridge.py` — exit 0.
Both paths resolve at 981d08d0 and the reviewer ran this exact command line there:
`All checks passed!`, exit 0, and again against the applied slice bytes in a disposable
worktree. A repository-wide `ruff check` is RED on main and is NOT a gate (R-0364).

G6 SUITES, each in the PRIMARY checkout and never in a worktree (R-0518), each as its exact
command line, each exit 0. Every base reading was taken by the reviewer at 981d08d0 there.
- `python3 -m pytest tests/orchestration/test_builder_bridge.py
  tests/orchestration/test_builder_bridge_smoke.py tests/orchestration/test_stop_reasons.py
  tests/orchestration/test_repair_loop_hardened.py
  tests/orchestration/test_self_healing_cycles.py -rf -q` — the five files reaching
  `builder_bridge`; base `80 passed, 1 skipped`. REPORT the number this run prints; do not
  assert it. The reviewer measured `82 passed, 1 skipped` against these exact slice bytes in a
  disposable worktree at 981d08d0.
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` — the four files reading `.agent/` state
  live; base `159 passed`. A red naming `TestVitestFrontendTestFoundation` with
  `apps/ui/node_modules` absent IS finding R-0518 and means the command ran in a worktree;
  re-run it in the primary checkout. Any other red is a STOP under constraint 6.
- CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base `42 passed`.

No mutation red-proof is ordered, deliberately: the reviewer ran four against these exact slice
bytes in a disposable worktree at 981d08d0 — the fixture repo demanding the scrubbed token be
PRESENT, the fixture repo demanding the `PYTHONDONTWRITEBYTECODE` overlay be ABSENT, `extra_env`
dropped from the guard call, and `cwd` handed None — and each exited non-zero on the test it was
aimed at, the fourth after 60.27 s, the guard's own wall tripping. The readings go to R46.

G7 THE PLAN at HEAD after C3, proved by reconstruction: take `.agent/plan.md` at 981d08d0,
replace PLANF1 with PLANT1 and PLANF2 with PLANT2, confirm byte-identity with the committed
file, report both sha256 values. Then report PLANF1 0x, PLANT1 1x, PLANF2 0x, PLANT2 1x at HEAD,
that the file still carries `## Goal` and `## Next Steps`, that 0 marker lines reached it,
`git show --numstat` for C3, and the line count against the 50-line AGENTS.md cap.

G8 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
981d08d0 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 153 / 27 / 0, 126 open, max registered R-0538, max resolved
R-0532. At HEAD registered must be 161, the registered symmetric difference exactly R-0539
through R-0546, done and landed symmetric differences EMPTY, 134 open, next free id R-0547.
Report the three symmetric differences, the duplicate-id count and the count of resolutions
naming an unregistered id, at both SHAs.

G9 HYGIENE. `git diff --name-only 981d08d0..HEAD` measured BEFORE C4 holds exactly the change
set above minus `.agent/handoff.md`, which C4 writes, and nothing else. Report per-commit
insertions for every commit BEFORE C4 — C4 cannot measure itself, so its own insertions go in
the round report — and confirm none exceeds 500. This branch already spent the AGENTS.md
declared-oversize allowance at d4473f85, so a second oversize commit is a STOP under constraint
6, never a declaration. Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch,
base SHA 981d08d0, a per-commit changed-files table, the item-status table covering C0a, C0b,
C1, C2, C3 and C4, the real G1-G9 results with exit codes, the open-findings count and the
next expected action. Keep it inside the 60-line cap, or name the DECISION D15 stated cause
and the exact mandated content behind it. Repeat this Fortschritt line verbatim:
Fortschritt: ~85 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R44 PASS ·
T002a KOMPLETT · T002b KOMPLETT, alle Sites der Klasse auf dem Seam · T002c-d, T003 offen) —
Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section states that the next round is R46; that R46 makes the checklist item 16
widening this round cut for size and opens T002c, the two DoD sites in
`packages/orchestration/dod_runners.py`, whose policy differs because their children are the
long-lived harness and take no wall timeout; that T002d, T003, the integration gate and closure
follow; and that R46's first reviewed act is recording R45's gate entry.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-RECORD13
Gate: R45 — the R44 entry. R44 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over f3e9687a..981d08d0, not read, and each reproduces the handback's reading exactly; the full
numbers live in the handback at 981d08d0 and are not restated here. LINE COUNTS ARE
`splitlines` COUNTS. What the re-run establishes: transport proved disk-to-disk against the
reviewer's own `.remedy-wt/f085-r44.md` with no digest fallback, all copies equal at sha256
d8bf11c9…, 30615 B, 516 lines; both C1 appends held their prefix-plus-blank-plus-slice shape
with 0 marker LINES reaching either file; both edited `.py` files reconstruct byte-identically
from their base blobs under the ordered slice application; the suites re-ran in the primary
checkout at exit 0, `190 passed` against a base of 186 with each of the four new test names
collected exactly once and the canary `42 passed` against 42; the arithmetic held still at
153 / 27 / 0 and 126 open at both SHAs, all three symmetric differences EMPTY.

THE ONE RED CLAUSE WAS REPORTED AS RED, WHICH IS WHY THIS IS A PASS. C0a carries 516
insertions against the AGENTS.md 500-line cap, and R44's handback declared it under the
AGENTS.md exception with an inseparability reason rather than reporting the clause green.
Clause (b) reproduces under independent measurement at 981d08d0: walking all 268 commits of
`main..981d08d0` gives exactly one over 500 — d4473f85 at 516 — the next largest at 454 and
four at 400. The allowance is spent for F085, and DEC6, landed by this same commit, is the
counter-measure so that it is never needed again.

EIGHT REGISTRATIONS, ALL OWED BEFORE THIS ROUND AND ALL RE-MEASURED AT 981d08d0. Three were
declared by R43's worker and deferred by RECORD12; five come from R44's handback, four of them
defects in the R44 block, which is the reviewer's own text.

- R-0539 — Low, A RANGE READING WAS QUALIFIED WITH A SINGLE COMMIT. RECORD11, applied at
007f18df, states "the path set at 7c4a2583 is exactly the five ordered paths". Measured at
981d08d0: `git show --name-only 7c4a2583` returns exactly one path, `.agent/plan.md`; the
five-path set is a property of the RANGE 0e2cdacd..4c7bcb3a. The mis-scoped-qualifier class
R-0534 opened and R-0538 recorded recurring, arriving through the RANGE side checklist item 22
governs. Declared by R43's worker and registered here per checklist item 20.

- R-0540 — Low, A COUNT WAS REPORTED WITHOUT THE FILE IT WAS COUNTED IN. RECORD11, applied at
007f18df, states that lines matching a `## DECISION F085 D<n> —` pattern "number 2 at 0e2cdacd
against 3 at 4c7bcb3a", and names no path. Measured at 981d08d0: in `.agent/live_review.md`,
the file that sentence sits in, the count is 0 at both SHAs; in `.agent/decisions.md` it is 2
and 3. The numbers are right and their owner is missing, so a reader who resolves the string to
the file holding it reads a false sentence. Declared by R43's worker.

- R-0541 — Low, A FINDING'S ENUMERATION OF ANOTHER TEXT'S NUMERALS WAS INCOMPLETE. R-0537,
applied at f3e9687a, states that the R41 block's numerals "of that family are the 50-line and
60-line caps it quotes as standing rules and the 45 and 69 that RECORD9 reports as READINGS".
Measured at 981d08d0 against `.agent/authored/f085-r41.md` as committed at 9cc4772c: that file
contains "500-line cap" twice, quoting the AGENTS.md commit cap, and neither occurrence appears
in R-0537's list. The conclusion survives, since neither omitted numeral is a prediction; the
enumeration fails, inside a finding whose subject is a defective enumeration. Declared by R43's
worker.

- R-0542 — Medium, A DECISION DESCRIBED THE BLOCK IT SHIPPED WITH AND THE BLOCK DID OTHERWISE.
DECISION F085 D5, applied at da47ee40, closes "The R44 block is the first measured under this
counting and declares both of its numbers in its own constraints". Measured at 981d08d0 against
`.agent/authored/f085-r44.md` as committed at d4473f85: constraint 10 of that block declines to
state them — "the worker measures them from the committed `.agent/authored/f085-r44.md` rather
than taking them from here" — and neither 239 nor 516 occurs anywhere in the block's prose.
This is checklist item 11's R-0527 shape one level out: item 11 forbids a BLOCK constraint
asserting a property its own slice lacks, and here a SLICE asserts a property its own block
lacks. DEC6 carries the counter-measure; R45's constraint 9 is the first text written under it.
Declared by R44's worker as deviation 2.

- R-0543 — Low, A PLAN SENTENCE COUNTED THE TESTS ITS OWN ROUND SHIPPED AND COUNTED THEM WRONG.
PLANT13, applied at 91ad51ae, says R44 applies DECISION F085 D4 "with five tests". Measured at
981d08d0: `def test_` in `tests/orchestration/test_ci_run.py` goes from 10 at f3e9687a to 14,
so C2 added four, and the R44 block's own goal line says "four tests". The slice was applied
byte-verbatim and correctly left unrepaired. This is the class R-0537 named and asked the
checklist to cover; that widening is R46's, having been cut from this block for size, and this
registration does not claim it has happened. Declared by R44's worker as deviation 3.

- R-0544 — Medium, A BASE READING WAS ORDERED THAT A CONTAINMENT-SHAPED PAIR CANNOT PRODUCE.
Constraint 2 of the R44 block, committed at d4473f85, asserts that each FROM occurred 1x in its
target at f3e9687a "and each TO 0x there". Measured at 981d08d0: CIT1 is the single line
`import subprocess` and CIF1 is that line preceded by `import os`, so CIF1 CONTAINS CIT1 and
CIT1 reads 1x at f3e9687a, not 0x. A deletion-shaped rewrite whose TO is a subset of its FROM
has the unattainable-count property checklist items 4 and 15 establish for an APPEND, and both
are written only about the TO-contains-FROM direction. Nothing broke, since every FROM read
exactly 1x, but the block ordered a number no honest run could produce. The counter-measure is
to order no base reading of a TO at all, which R45's constraint 2 is the first block to do.
Declared by R44's worker as deviation 4.

- R-0545 — Medium, AN ORDERED-EQUALITY GATE ASSUMED A COMMIT DOES ONE THING TO A FILE. Gate G4
of the R44 block, committed at d4473f85, orders the R-0531 code-append proof as "the pre-commit
blob is a byte-exact PREFIX of the post-commit file". Measured at 981d08d0: for
`tests/orchestration/test_ci_run.py` that clause is FALSE and cannot be true, since the same
commit both REWRITES the file's import block and APPENDS to its end. The meetable form holds
and was measured by worker and reviewer alike: the base blob with TIMPF→TIMPT applied, 4206 B,
IS a byte-exact prefix of the 6317 B post-commit file, the remainder being exactly TESTS. §4.9
carries the same assumption; this finding does not amend it, it records that the PREFIX half
must name the intermediate text whenever a commit edits above its own append, which G4 of this
round is the first gate to do. Declared by R44's worker as deviation 5.

- R-0546 — Medium, LIFTING ONE CAP LEFT THE ROUND STANDING ON ANOTHER. DECISION F085 D5,
applied at da47ee40, rules that the 400-line block cap counts a block's PROSE and that slices
are counted but not capped, its CHOSEN paragraph naming "a commit under 500 insertions" among
the caps that stand untouched. Measured at 981d08d0: the very block D5 was written for measures
516 lines, and C0a saves it as a NEW file where insertions equal lines, so D5's first
application forced the branch to spend its single AGENTS.md declared-oversize allowance. Both
rules were correctly stated and never measured against each other. What earns it an id is that
the collision was derivable at emission from numbers already in the block. DEC6, landed by this
same commit, is the counter-measure. Found by the reviewer at this gate.
END-RECORD13

BEGIN-DEC6
## DECISION F085 D6 — a block is budgeted at 480 lines TOTAL, because the commit that saves it is capped at 500 insertions (2026-08-17)

Ruled by the reviewer at the R45 gate under docs/agents/planner_reviewer_prompt.md §4 item 7.
Reverse it by deleting this section; D5's 400-line PROSE cap then stands alone and the total
is again unbudgeted. This decision AMENDS nothing in AGENTS.md and weakens nothing there: the
500-insertion commit cap is untouched and remains the higher authority.

THE PROBLEM IS MEASURED, and it is finding R-0546. DECISION F085 D5 lifted the 400-line cap off
a block's authored SLICES so a round could carry code again, and its CHOSEN paragraph left "a
commit under 500 insertions" standing; the two sentences are individually correct and were
never read against each other. A block is saved by C0a as a NEW file under `.agent/authored/`,
where insertions EQUAL lines, and DECISION F105 D5 rules that path counts normally rather than
claiming the `.agent/**` single-artifact exemption. The commit cap has therefore always been a
hard ceiling on a block's TOTAL size, and D5's first application produced a 516-line block that
spent the branch's one AGENTS.md declared-oversize allowance — measured at 981d08d0, exactly
one of the 268 commits on this branch exceeds 500.

CHOSEN: a block is budgeted at 490 lines TOTAL and its PROSE stays capped at 400 by D5. The ten
lines of margin are not an estimate of anything — C0b's insertions are bounded above by the
block's own line count, so the mirror needs no allowance — they exist because a reviewer's
hand-shaped artifact must not sit within a rounding error of a hard repository cap that no
downstream actor can relax. Both numbers are MEASURED at emission and stated in the block's
constraints, and the worker re-measures both from the committed file and reports them; the
disagreement between those two readings is what makes drift visible, and stating only one of
them is what produced R-0542. A RECORD SLICE IS BUDGETED AT 140 LINES — the counter-measure D5
named as owed and did not supply. The record is the slice class that actually grew and the one
whose growth is least visible, a gate entry having no natural stopping point. A round whose
record would exceed 140 lines splits the registrations into their own round rather than
deferring them, which is what R43 and R44 each did under pressure from the wrong cap.

ALTERNATIVES CONSIDERED AND REJECTED: splitting C0a across two commits, for the reason R44's
handback gave — it puts a truncated block on disk at an intermediate commit while constraint 1
makes those exact bytes the source every slice is extracted from; claiming the `.agent/**`
single-artifact exemption for `.agent/authored/`, because DECISION F105 D5 rules that path
counts normally and this decision may not reverse another feature's ruling; raising the
AGENTS.md 500-insertion cap, because AGENTS.md is the highest authority and §4 item 7 routes a
wrong FEATURE spec to planning, never a repository rule to the reviewer.

CONSEQUENCE. 490 against 400 leaves at most 90 lines of slice in a block whose prose runs to
the cap, which is not enough for a migration; that is intentional, since it prices prose
against product at emission, where the reviewer can still shorten the prose, rather than at
commit time, where nobody can. The R45 block ran over this budget in draft and was cut to fit
before emission, dropping a checklist edit to R46, which is the rule working as intended.
END-DEC6

BEGIN-BBF1
import os
from dataclasses import dataclass, field
END-BBF1

BEGIN-BBT1
from dataclasses import dataclass, field
END-BBT1

BEGIN-BBF2
from packages.orchestration.diff_repair_response import (
    diff_repair_response_to_patch,
    parse_diff_repair_response,
)
END-BBF2

BEGIN-BBT2
from packages.orchestration.diff_repair_response import (
    diff_repair_response_to_patch,
    parse_diff_repair_response,
)
from packages.orchestration.exec_guard import run_guarded_test_command
END-BBT2

BEGIN-BBF3
                env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
                proc = subprocess.run(
                    test_cmd,
                    capture_output=True, text=True, timeout=60,
                    cwd=str(repo_path),
                    env=env,
                )
END-BBF3

BEGIN-BBT3
                # Stage-1 guard, per DECISION F085 D3. `extra_env` SETS the one
                # variable this site used to overlay onto a copy of `os.environ`,
                # which the guard's allowlist scrub would otherwise drop. The 60 s
                # was already this call's wall and stays its wall: the guard's own
                # deadline replaces `subprocess.run`'s and still surfaces as
                # `TimeoutExpired`, so the handler below is unchanged. Streams come
                # back as BYTES rather than text, and only `returncode` is read here.
                proc = run_guarded_test_command(
                    test_cmd,
                    timeout_sec=60,
                    cwd=str(repo_path),
                    extra_env={"PYTHONDONTWRITEBYTECODE": "1"},
                )
END-BBT3

BEGIN-TIMPF
import json

from packages.core.models import Job
from packages.orchestration.builder_models import BuilderOutput
END-TIMPF

BEGIN-TIMPT
import json
import subprocess

from packages.core.models import Job
from packages.orchestration import builder_bridge
from packages.orchestration.builder_models import BuilderOutput
END-TIMPT

BEGIN-TESTS


def _run_bridge_test_stage(tmp_path):
    """Drive the bridge to stage 4 against a one-file fixture repo."""
    patch_text = json.dumps({
        "file_ops": [{"path": "calc.py", "action": "create", "content": "x = 1\n"}]
    })
    output = BuilderOutput(
        summary="Fix calc", proposed_changes=["Fix add"],
        structured_patch_text=patch_text,
    )
    return builder_bridge.run_builder_bridge(
        output, tmp_path, job=Job(name="test"), data_dir=tmp_path, autonomy_level=4
    )


class TestBuilderBridgeGuardSeam:
    """T002b's last `test`-class site, migrated onto the stage-1 guard."""

    def test_the_guard_receives_the_wall_the_cwd_and_the_bytecode_overlay(
        self, tmp_path, monkeypatch
    ):
        """Read off the call the seam receives, which the result cannot show."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        seen = {}

        def capture(cmd, **kwargs):
            seen.update(kwargs)
            return subprocess.CompletedProcess(list(cmd), 0, b"", b"")

        monkeypatch.setattr(builder_bridge, "run_guarded_test_command", capture)
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_calc.py").write_text("def test_ok():\n    pass\n")
        assert _run_bridge_test_stage(tmp_path).test_passed is True
        assert seen["timeout_sec"] == 60
        assert seen["cwd"] == str(tmp_path)
        assert seen["extra_env"] == {"PYTHONDONTWRITEBYTECODE": "1"}

    def test_a_secret_like_parent_variable_does_not_reach_the_test_child(
        self, tmp_path, monkeypatch
    ):
        """The overlay must still arrive while the parent's secret does not.

        Both halves are asserted inside the fixture repo's own test body, so the
        green `test_passed` below IS the assertion rather than a proxy for it.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        monkeypatch.setenv("REMEDY_BRIDGE_FAKE_TOKEN", "sk-not-a-real-secret")
        (tmp_path / "tests").mkdir()
        (tmp_path / "tests" / "test_env.py").write_text(
            "import os\n"
            "\n"
            "def test_env():\n"
            "    assert 'REMEDY_BRIDGE_FAKE_TOKEN' not in os.environ\n"
            "    assert os.environ.get('PYTHONDONTWRITEBYTECODE') == '1'\n"
        )
        assert _run_bridge_test_stage(tmp_path).test_passed is True
END-TESTS

BEGIN-PLANF1
## Current Step
R44, this round: record the R43 PASS and apply DECISION F085 D4 to
`packages/orchestration/ci_run.py` with five tests. The three findings R43's worker declared
are stated in the record and take ids at R45; the block cap took the half already safe on
disk rather than deferring the code a third time.
END-PLANF1

BEGIN-PLANT1
## Current Step
R45, this round: record the R44 PASS, register R-0539 through R-0546, rule DECISION F085 D6 on
the block budget, and migrate `packages/orchestration/builder_bridge.py` onto the stage-1 guard
as the last `test`-class site. T002b closes with this round.
END-PLANT1

BEGIN-PLANF2
1. R45 — register the three findings RECORD12 states as owed, then migrate
   `packages/orchestration/builder_bridge.py`, the last `test`-class site on a bare spawn,
   which at c3201976 overlays `PYTHONDONTWRITEBYTECODE` onto a copy of `os.environ` and is
   unblocked by the same `extra_env` overlay `ci_run.py` needed (DECISION F085 D3). R45 also
   owes two checklist promotions this branch has measured and not made: widening item 16 to
   any sentence that counts what follows it, and a stated budget for a record slice.
END-PLANF2

BEGIN-PLANT2
1. R46 — the checklist item 16 widening R-0537 and R-0543 both name, cut from R45 for size,
   then T002c: the two DoD sites in `packages/orchestration/dod_runners.py`, whose policy
   differs from the `test` class in taking no wall timeout, because their children are the
   long-lived harness rather than a bounded suite run.
END-PLANT2
