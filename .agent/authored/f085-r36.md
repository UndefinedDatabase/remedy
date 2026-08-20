── STEP T002b migration — F085 — R36 ─────────────────────────────────────────

Goal: put the default `runner` closure of `packages/orchestration/mission_state.py`
onto `run_guarded_test_command`, together with the first test that reaches that
closure at all, and record the R35 PASS while registering R-0526.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 record R35
and register R-0526 · C2 the migration and its seam test · C3 plan · C4 handback.

## Why this round exists — read before C2

R35 PASSED; RECORD4 carries the re-run numbers and this section does not repeat them.

R33, R34 and R35 changed no production code. That is three rounds of record-keeping in
a row, and the momentum flag says so plainly this round rather than after a fourth.
This round is a production round, and the meta-work in it is one registration.

THE SITE. At 23b5fcd9 `run_verify_task` in `packages/orchestration/mission_state.py`
builds a default `runner` closure when the caller passes none, and that closure calls
`subprocess.run(argv, cwd=..., capture_output=True, text=True, timeout=900)` behind a
function-local `import subprocess`. It is the capture-and-timeout shape already
migrated at `pingpong_loop.py`, `test_runner.py`, `job_promote.py` and
`integrity_gate.py`. At 23b5fcd9 those two lines are the only occurrences of the
string `subprocess` in that module, so the local import goes with the call it served.

WHY THE TEST IS NOT OPTIONAL. At 23b5fcd9 every test in
`tests/orchestration/test_mission_state.py` that exercises `run_verify_task` passes its
own `runner=`, except the one returning at the empty-command branch before any closure
is built, so the default closure is executed by NO test in the suite. A migration landed
without a new test would be a change no gate can see — the R-0220 class. T1 adds
`test_the_default_runner_goes_through_the_guarded_seam` in the SAME commit as the code.

WHY THE IMPORT IS AT MODULE LEVEL. Every existing seam test intercepts the call with
`monkeypatch.setattr(<module>, "run_guarded_test_command", _fake_guarded)`
(`tests/orchestration/test_integrity_gate.py`, `test_pingpong.py`, `test_job_promote.py`
at 23b5fcd9), and that patch cannot reach a name bound by a function-local import: the
module would carry no such attribute, and `monkeypatch.setattr` raises rather than
patching. A local import would leave the site untestable by the established pattern
while every gate stayed green. G8 proves exactly this and nothing else.

NO CYCLE. The reviewer grepped `packages/orchestration/exec_guard.py` at 23b5fcd9 for
`mission_state` and got no match, so a module-level import adds no import cycle.

BYTES, NOT STR. `run_guarded_test_command` returns `CompletedProcess[bytes]` while this
closure has always returned `str`, so the decode is part of the change and matches
`pingpong_loop.py` at 23b5fcd9. `subprocess.TimeoutExpired` is what a wall trip raises
at the seam and what `timeout=900` raised before it, and the existing `except Exception`
around the call already turns either into a FAILED outcome, so a timing-out verify
command behaves as it did. `builder_bridge.py` still comes LAST and stays BLOCKED until
the seam can SET an environment value rather than only allowlist a key.

## Change

C1 — `.agent/live_review.md`, one commit, RECORD4 appended and nothing else. RECORD4
carries the R35 gate entry and then the R-0526 registration, as one slice.

C2 — one commit holding both files of the migration:
`packages/orchestration/mission_state.py` — the M1 import pair, the M3 docstring pair
and the M2 closure pair — and `tests/orchestration/test_mission_state.py`, the T1
pair. The code and the test that reaches it are not split across commits.

C3 — `.agent/plan.md`, one commit, the PLANF4→PLANT4 pair over the Current Step block
through the first Next Steps item. The pair changes no item's number and adds none.

Change set, named rather than counted: `.agent/authored/f085-r36.md`,
`.agent/last_block.md`, `.agent/live_review.md`, `packages/orchestration/mission_state.py`,
`tests/orchestration/test_mission_state.py`, `.agent/plan.md` and `.agent/handoff.md`.
Nothing else is touched.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r36.md` by its marker pair. Never retype a slice, never apply
   one from the prompt. Marker lines never reach a target file.
2. Pair shapes, each MEASURED by the reviewer with a containment test and recorded as
   the test's OUTPUT, one reading per pair — the form checklist item 15 requires:
   M1F→M1T — TO contains FROM: true — APPEND.
   M3F→M3T — TO contains FROM: true — APPEND.
   M2F→M2T — TO contains FROM: false — REWRITE.
   T1F→T1T — TO contains FROM: true — APPEND.
   PLANF4→PLANT4 — TO contains FROM: false — REWRITE.
   For every APPEND pair the "FROM 0x after" count is unattainable by construction and
   is NOT ordered; §4.9's append obligation is ordered instead. Do not report a
   FROM-zero reading for an APPEND pair under any wording.
3. Re-read `.agent/STOP` from disk before C0a and again before C4. If it exists,
   finish the commit in flight, write the handback and stop.
4. `git status --porcelain` is empty at round start and after every commit. G8 is a
   destructive check and runs ONLY inside a disposable `git worktree`, never in the
   primary checkout; that worktree is removed and pruned before C4, so
   `git worktree list` is one line at round start and one line again after G8.
5. C1 is an APPEND: the pre-commit file stays a byte-exact prefix and exactly one
   blank line separates it from RECORD4. Do not reflow, re-wrap or re-indent it.
6. Nothing outside the declared change set is touched. This round REGISTERS R-0526 and
   resolves no id, so the open count moves from 118 to 119 and no `Done:` line is
   written by anyone this round.
7. If any gate comes out red, or a FROM does not match at exactly one place in the file
   it is applied to, STOP: write the handback naming the exact command, its exit code
   and its output, and do not improvise a repair. This includes G8 coming out GREEN,
   which would mean the proof did not reach what it claims to reach.
8. STALENESS, standing: after C3 re-read every edited file and confirm that no sentence
   this round put on disk was falsified by a later commit of the same round, and that
   no slice quotes another file's current wording as a claim. Name what was re-read.
   RECORD4 states facts about `packages/orchestration/mission_state.py` and
   `tests/orchestration/test_mission_state.py`, both of which C2 of this same round
   edits, and every one of those sentences names the SHA 23b5fcd9 — the state BEFORE
   this round — or names constraint 9 for the change this round itself creates.
9. The commit order C1 before C2 is load-bearing: RECORD4's readings of
   `mission_state.py` and of its test file describe those files at 23b5fcd9, and C1
   lands before C2 changes them. Do not reorder.
10. Do not "repair" any landed text. R-0526's imprecise sentence stays in the commit
    that holds it; the correction is RECORD4's registration, not an edit to
    `.agent/live_review.md` — the R-0521 principle.
11. C2 is ONE commit holding both files. Do not split the code from the test that
    reaches it: a commit with the migration and no test is a state in which no gate
    can see the change.

## Done when

G1 STATE. `.agent/STOP` absent at the two points named in constraint 3;
`git status --porcelain` empty at round start and after every commit;
`git worktree list` one line at round start and again after G8.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r36.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL. Report the sha256, the
byte count, the line count, the number of marker lines, and region digests over the
line ranges 1-100, 101-200 and 201-end, each digest taken over those lines with their
trailing newlines included. Do not compute any of those numbers by hand; measure them.

G3 APPEND SHAPE for C1. The pre-commit blob of `.agent/live_review.md` is a byte-exact
PREFIX of the post-commit file; the remainder is exactly one blank line plus RECORD4;
RECORD4 is an exact suffix of the post-commit file; RECORD4's first line occurs once
among the lines that commit's diff ADDS; 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$`
land in the file — count marker LINES, never the substring, because the quoted regex
already appears in that file's prose. Report `git show --numstat` for that path.

G4 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md`
at base 23b5fcd9 and at HEAD, taking registered from `^- R-\d{4} — `, done from
`^Done: R-\d{4} — ` and landed from `^Landed: R-\d{4}`. The reviewer's base reading is
140 registered / 22 done / 0 landed, 118 open, max registered R-0525 and max resolved
R-0525; at HEAD it must be 141 / 22 / 0 with 119 open, max registered R-0526 and max
resolved STILL R-0525, because this round resolves nothing. Report the registered
symmetric difference (exactly R-0526), the done symmetric difference (empty), the
landed symmetric difference (empty), the count of duplicate ids, the count of
resolutions naming an unregistered id, the maximum id, and the next free id, which
moves from R-0526 to R-0527.

G5 PAIR PROOFS, measured at HEAD after C2, per pair and never generalised:
- M1F, M3F and T1F each still occur exactly once in their target file, because those
  three pairs are APPEND-shaped and their FROMs survive by construction;
- M2F occurs 0 times and M2T occurs exactly once, the rewrite reading, which is
  ordered for this pair and for no other;
- every line M1T, M3T and T1T add that their own FROM does not contain occurs exactly
  once AMONG THE LINES C2'S DIFF ADDS — that is the §4.9 append obligation, ordered
  INSTEAD of a FROM-zero count for those three;
- 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` reached either file;
- the string `subprocess` occurs 0 times in `packages/orchestration/mission_state.py`
  at HEAD, because M2 removed the only two occurrences the module had at 23b5fcd9 and
  no slice in this block writes that string into that file.
Report `git show --numstat` for C2, and the same three readings for PLANF4→PLANT4 in
`.agent/plan.md` after C3: FROM 0x, TO 1x.

G6 LINT AND SUITES, each run in the PRIMARY checkout and never in a worktree (R-0518):
- `python3 -m ruff check packages/orchestration/mission_state.py
  tests/orchestration/test_mission_state.py` exits 0. Base reading at 23b5fcd9:
  `All checks passed!`. This round changes production code, so the lint is ordered.
- `python3 -m pytest tests/orchestration/test_mission_state.py -q` exits 0. Base
  reading `81 passed`; at HEAD it must read `82 passed`, one more because T1 adds
  exactly one test. Report the number, do not predict it a second time.
- `python3 -m pytest tests/orchestration/test_test_runner.py
  tests/regression/test_resource_safety.py tests/orchestration/test_integrity_gate.py
  tests/ui_server/test_dashboard_contract.py -rf -q` exits 0, base reading
  `159 passed`. A red naming `TestVitestFrontendTestFoundation::test_vitest_passes`
  with `apps/ui/node_modules` absent IS finding R-0518 rather than a regression, and
  means the command was run in a worktree; re-run it in the primary checkout. Any
  other red is a STOP under constraint 7.
- CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0, base reading
  `42 passed`.
No `tests/docs/` gate is ordered: this round's change set contains no path under
`docs/`, and that suite is blind to `docs/agents/**` anyway (red-controlled at 7480d880).

G7 COMMIT HYGIENE. `git diff --name-only 23b5fcd9..HEAD` measured BEFORE C4 holds
exactly the paths named in the change set above, minus `.agent/handoff.md` which C4
writes, and nothing else. Report per-commit insertions for every commit BEFORE C4 — C4
cannot measure itself, so report its own insertions in the round report instead — and
confirm none exceeds 500. Confirm every commit has exactly one parent and that
`git reflog -10` holds only `commit:` entries.

G8 RED PROOF that the module-level import is load-bearing. Run this ONLY inside a
disposable worktree created at the C2 commit, never in the primary checkout.
Recipe: delete the module-level line
`from packages.orchestration.exec_guard import run_guarded_test_command` and add that
same import as the first statement INSIDE the `runner` closure, then run
`python3 -m pytest tests/orchestration/test_mission_state.py -q -rf`.
Property: `test_the_default_runner_goes_through_the_guarded_seam` FAILS, and the
reported reason is an `AttributeError` naming `run_guarded_test_command`, raised at the
`monkeypatch.setattr` line — a closure-local name is not a module attribute, so the
established seam-patch pattern cannot reach it. Report the failing test id, the quoted
error line and the passed/failed counts, then remove and prune the worktree and show
`git worktree list` back at one line. The reviewer ran this exact control at 23b5fcd9
with these slices applied and got `1 failed, 81 passed` with that AttributeError; a
GREEN result here is a STOP under constraint 7, because it would mean the test does not
depend on the property this round exists to establish.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round,
branch, base SHA 23b5fcd9, a per-commit changed-files table, the item-status table
covering C0a, C0b, C1, C2, C3 and C4, the real verification results for G1-G8 with
exit codes, the open-findings count, and the next expected action. In the
`## Authored-text proofs` section report each pair under the shape constraint 2 assigns
it, and NEVER report a FROM-zero count for an APPEND pair. Repeat this Fortschritt line
verbatim:
Fortschritt: ~72 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R35
PASS · T002a KOMPLETT · T002b 10 von 12 Sites auf dem Seam, 2 offen · T002c-d, T003
offen) — Schätzung, gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The handback MUST state, in its `## Next` section, that the next session's FIRST action
is Phase 1 rule 1 — re-read `.agent/STOP` from disk — BEFORE rule 2, the Open PR Gate
(`gh pr list --state open --json number,headRefName,baseRefName,isDraft`). It MUST also
state that R36's own verdict is NOT a §4.13 terminator because this branch continues,
and that the next reviewed round records R36's gate entry in `.agent/live_review.md`.

The `## Next` section MUST additionally carry this note verbatim, because the reviewer
measured it at 23b5fcd9 and it would otherwise be re-derived wrongly:

  The next migration site is `packages/orchestration/ci_run.py`. At 23b5fcd9 its only
  spawn is line 79, `subprocess.run(command, check=False, cwd=cwd, env=env).returncode`
  — no capture, no timeout, output streaming straight to the console. Moving it onto
  `run_guarded_test_command` therefore CHANGES observable behaviour rather than
  preserving it: the seam captures, so a console-streaming CI run would go silent
  unless the migration also decides where that output goes. That decision belongs in
  the round that does it and must be recorded as a DECISION, not taken in passing.
  `builder_bridge.py` comes LAST and stays BLOCKED until the seam can SET an
  environment value rather than only allowlist a key.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-M1F
from packages.orchestration.data_paths import missions_dir
END-M1F

BEGIN-M1T
from packages.orchestration.data_paths import missions_dir
from packages.orchestration.exec_guard import run_guarded_test_command
END-M1T

BEGIN-M3F
    ``runner`` exists for tests and for callers that already own a sandboxed
    executor; it takes ``(argv, cwd)`` and returns ``(exit_code, output)``.
    The default runs the recorded command as an argv list — never through a
    shell, so a recorded command cannot become a recorded shell injection.
END-M3F

BEGIN-M3T
    ``runner`` exists for tests and for callers that already own a sandboxed
    executor; it takes ``(argv, cwd)`` and returns ``(exit_code, output)``.
    The default runs the recorded command as an argv list — never through a
    shell, so a recorded command cannot become a recorded shell injection.
    It goes through ``run_guarded_test_command``, so the recorded command runs
    under the `test`-class resource limits, the wall timeout and the environment
    allowlist rather than on prompted discipline alone.
END-M3T

BEGIN-M2F
        def runner(argv: list[str], cwd: Path | None):  # noqa: E306
            import subprocess

            completed = subprocess.run(
                argv, cwd=str(cwd) if cwd else None, capture_output=True,
                text=True, timeout=900,
            )
            return (completed.returncode,
                    (completed.stdout or "") + (completed.stderr or ""))
END-M2F

BEGIN-M2T
        def runner(argv: list[str], cwd: Path | None):  # noqa: E306
            completed = run_guarded_test_command(
                argv, timeout_sec=900, cwd=str(cwd) if cwd else None,
            )
            return (completed.returncode,
                    (completed.stdout or b"").decode("utf-8", "replace")
                    + (completed.stderr or b"").decode("utf-8", "replace"))
END-M2T

BEGIN-T1F
        run_verify_task(self._task("pytest tests/importer -q"), runner=_record)

        assert seen == [["pytest", "tests/importer", "-q"]]
END-T1F

BEGIN-T1T
        run_verify_task(self._task("pytest tests/importer -q"), runner=_record)

        assert seen == [["pytest", "tests/importer", "-q"]]

    def test_the_default_runner_goes_through_the_guarded_seam(self, monkeypatch):
        import subprocess

        from packages.orchestration import mission_state

        seen: dict[str, object] = {}

        def _fake_guarded(cmd, *, timeout_sec, cwd, extra_env_keys=()):
            seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
            return subprocess.CompletedProcess(
                list(cmd), 0, b"ok-\xff-undecodable\n", b"warn\n")

        monkeypatch.setattr(mission_state, "run_guarded_test_command", _fake_guarded)
        outcome = run_verify_task(self._task("pytest tests/importer -q"))

        assert seen == {
            "cmd": ["pytest", "tests/importer", "-q"],
            "timeout_sec": 900,
            "cwd": None,
        }
        assert outcome.result == VERIFY_RESULT_PASSED
        assert outcome.exit_code == 0
        assert "ok-" in outcome.output_tail
        assert "undecodable" in outcome.output_tail
        assert "warn" in outcome.output_tail
END-T1T

BEGIN-RECORD4
Gate: R36 — the R35 entry. R35 PASSED: the interlude that recorded R34 and narrowed
checklist item 20 to the paths this workflow rewrites every round. Every ordered gate
was re-run by the reviewer over 6ca30b16..23b5fcd9 and each reproduces the handback's
reading. TRANSPORT: the committed `.agent/authored/f085-r35.md`, the committed
`.agent/last_block.md` and both working copies are byte-EQUAL at sha256
41a8470f56a9063fb40a82526f0731bb57b2de20f296b075de572848a6f8581d, 21145 B, 331 lines,
10 marker lines, region digests c9271720, 72829987 and 3e006c9f — all four measured by
the reviewer, not read from the handback. THE APPEND COMMIT HELD ITS SHAPE: cde59e8c's
pre-commit blob 381289 B is a byte-exact PREFIX of the 387274 B post-commit file, the
remainder 5985 B is one blank line plus RECORD3, RECORD3 is an exact suffix, its first
line occurs once among the 78 lines that commit adds, numstat 78/0, 0 lines match
`^(BEGIN|END)-[A-Z0-9]+$` while the BEGIN substring occurs 11 times. THE ARITHMETIC
MOVED IN BOTH SETS BY THE SAME ONE ID: 139 registered / 21 done / 0 landed at 6ca30b16
against 140 / 22 / 0 at 23b5fcd9, 118 open at both ends, registered and done symmetric
differences each exactly R-0525, landed symmetric difference empty, no duplicate id, no
resolution naming an unregistered id, and next free R-0526. THE NARROWING LANDED AS AN
APPEND AND WAS PROVED AS ONE: at 23b5fcd9 the I20F text still occurs exactly once, the
item-15, item-20 and closing-paragraph openers each occur exactly once, and the 11
lines C1's diff adds are exactly the 11 lines I20T adds that I20F does not contain,
each once; 0 marker lines reached the file; numstat 11/0. THE SUITES WERE RE-RUN, NOT
READ: the four state readers `159 passed`, the docs suite `295 passed` and the canary
`42 passed`, each as its exact ordered command line in the primary checkout, each exit
0. The ordered push landed: `git ls-remote origin` and the local branch agree at
23b5fcd9. COMMIT HYGIENE IS CLEAN: the path set before C4 is the five declared paths,
per-commit insertions are 331, 215, 11, 78, 3 and the handback's own 58, none over 500,
all six commits are single-parent, and the reflog holds only `commit:` entries.

- R-0526 — Low, A RESOLUTION ASSERTED A UNIVERSAL PROPERTY OF ITS OWN REFERENCES THAT
ITS OWN TEXT DOES NOT MEET. R35's RECORD3, applied at commit cde59e8c, closes its
R-0525 resolution with "This entry obeys the new clause: every reference it makes to
`.agent/handoff.md` names the SHA that holds the text it means." The reviewer counted
the sentences of RECORD3 mentioning that path at 23b5fcd9 and found four: one locates
landed text and names 2342ed97, and the other three — the rule statement, the path list
and the compliance claim itself — name no SHA and locate nothing. Under the clause as it
landed the entry IS compliant, because the clause binds only a slice that LOCATES landed
text; what fails is the sentence's own restatement of it, which quantifies over every
reference rather than over the ones that locate text and is false of three of its own
four. The referent is recoverable, so the cost is the audit it invites: a later reader
checking the claim must re-derive that three of those references locate nothing. This is
the R-0402 and R-0460 family with a quantifier in place of a numeral — item 11 forbids a
hand-counted NUMERAL about a block's own parts, and nothing yet forbids a hand-checked
UNIVERSAL about a slice's own text. Registered here and deliberately NOT resolved in the
same round: the counter-measure is a checklist clause, this is a production round, and a
fix authored in passing is how the last three rounds became record-keeping. The next
record round resolves it by extending item 11 from numerals to any self-referential
claim a slice makes about its own text, stated as the property actually measured.
END-RECORD4

BEGIN-PLANF4
## Current Step
R35, this round: record the R34 PASS, and register and resolve R-0525 by naming the
paths this workflow rewrites every round, so a slice locating landed text in one of
them carries the SHA that holds it. No production code changes.

## Next Steps
1. T002b remainder — the three `test`-class sites still on a bare spawn, in this
   order. `mission_state.py` next: it spawns inside a default `runner` closure and
   is otherwise the capture-and-timeout shape already migrated three times. Then
   `ci_run.py`, which streams to the console instead of capturing and passes no
   timeout, so moving it onto a capturing seam is a behaviour decision and not a
   mechanical swap. `builder_bridge.py` comes LAST and is BLOCKED until the seam
END-PLANF4

BEGIN-PLANT4
## Current Step
R36, this round: record the R35 PASS and register R-0526, then migrate the default
`runner` closure of `mission_state.py` onto `run_guarded_test_command` together with
the first test that reaches that closure at all.

## Next Steps
1. T002b remainder — the two `test`-class sites still on a bare spawn, in this order.
   `ci_run.py` next: at 23b5fcd9 its only spawn streams to the console and passes no
   timeout, so moving it onto the capturing seam changes observable behaviour and the
   round that does it records where the output goes as a DECISION.
   `builder_bridge.py` comes LAST and is BLOCKED until the seam
END-PLANT4
