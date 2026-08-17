── STEP T002c first half — F085 — R51 ────────────────────────────────────────

Goal: move `_run_process_check` in `packages/orchestration/dod_runners.py` onto a new
`dod-process` seam in `packages/orchestration/exec_guard.py`, and record the R50 PASS. The seam
KEEPS the check's wall timeout and its cwd pin — bounded is the column separating `dod-process`
from `dod-app` in the T2_F085 table — and closes the gap that row exists for: the site passes
`env=os.environ.copy()`, handing a project-authored command the whole parent environment.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R50 · C3 rewrite the exec_guard coverage note · C4 append the seam ·
C5 migrate the call site · C6 append the tests · C7 handback.

CONVENTION, binding on every count here: a line count is the `splitlines` reading — a trailing
newline is NOT an extra line. A slice is the bytes strictly between its marker lines. Two append
shapes appear below and they differ: RECORD19 is PROSE joined to its target by exactly one blank
line, while SEAM, TESTSDOD and TESTSGUARD are CODE slices CARRYING their own leading blank lines,
so for those three the post-commit file is `pre + slice` with NO joiner byte.

## Change

C1 applies PLAN5F→PLAN5T to `.agent/plan.md` and C2 appends RECORD19 to
`.agent/live_review.md`. C3 applies HDRF→HDRT to `packages/orchestration/exec_guard.py`, which is
that module's own PARTIAL COVERAGE note: it currently says the DoD class still spawns
unsupervised, and C5 makes that false. C4 appends SEAM to the same file — two commits, because an
append proof needs a pre-commit blob the same commit did not also rewrite. C5 applies DOCF→DOCT,
IMPF→IMPT and SITEF→SITET to `packages/orchestration/dod_runners.py`: the module docstring's
subprocess-discipline bullets, the import, and the call site. All three are rewrites, so one
commit carries them with no append proof. C6 appends TESTSDOD to
`tests/orchestration/test_dod_runners.py` and TESTSGUARD to
`tests/orchestration/test_exec_guard.py` — two paths in one commit, each with its own untouched
pre-commit blob.

Change set, named rather than counted: `.agent/authored/f085-r51.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`packages/orchestration/dod_runners.py`, `tests/orchestration/test_dod_runners.py`,
`tests/orchestration/test_exec_guard.py`, `.agent/handoff.md`. Nothing else. No
`docs/roadmap/**` path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/`
gate is ordered; `.py` files ARE in it, so a lint gate is, and G4 carries it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r51.md` by its marker pair. Never retype one, never apply one from the
   prompt, never reflow one to a different wrap, and never add, rename or reorder a test the
   slices define. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C7; if it exists, finish the
   commit in flight, write the handback and stop. `git status --porcelain` is empty at round
   start and after every commit. This round orders no destructive check, so it creates no
   worktree and `git worktree list` stays one line throughout.
3. PAIR SHAPES. The reviewer ran the containment test on each pair separately at emission against
   that file's blob at 3a64b65e, and prints each pair's own output here per checklist item 15,
   none generalised to another: PLAN5F→PLAN5T `TO contains FROM: false`; HDRF→HDRT
   `TO contains FROM: false`; DOCF→DOCT `TO contains FROM: false`; IMPF→IMPT
   `TO contains FROM: false`; SITEF→SITET `TO contains FROM: false`. All five are therefore
   REWRITES and each owes the FROM 0x / TO 1x reading over its whole post-commit file. DOCF spans
   the WHOLE bullet list rather than a prefix, because its TO drops one bullet and so changes the
   list's arity (checklist item 17). RECORD19, SEAM, TESTSDOD and TESTSGUARD are APPENDS carrying
   no FROM, so no containment reading is owed for any of them. Each of the five FROM texts occurs
   EXACTLY 1x in its target at 3a64b65e — the reviewer measured all five — so none is ambiguous.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and ahead of every code commit. Only
   C0a and C0b may precede it. This round writes to the finding ledger, so §3 checklist item 23
   binds it.
5. Every sentence in RECORD19 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. C0b overwrites the
   working `.agent/last_block.md` before RECORD19 lands, which is why the SHA and never the
   present tense carries those readings.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested each of the five FROM texts
   against every later-applied text at emission and got NO hits, so each G3 FROM-0x reading stays
   attainable (checklist item 2, whose failure mode is a TO that quotes retired text on purpose).
7. Nothing outside the declared change set is touched. This round registers NO finding and
   resolves none: the open count stays 141 and the next free id stays R-0554. `.agent/plan.md`
   after C1 is 43 lines, which the reviewer projected mechanically from the pair.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never
   widen the change set to route around a red.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 489, PROSE 226, RECORD19 37. The worker
   re-measures all three from the committed `.agent/authored/f085-r51.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
10. THE REVIEWER ALREADY RAN THIS ROUND'S RED CONTROLS, at 3a64b65e, in a disposable worktree it
   removed afterwards, with these exact slice bytes applied by the extraction ordered above.
   Reverting SITET to SITEF failed both new `dod_runners` tests, and the secret-leak test's own
   failure message printed `AWS_SECRET_ACCESS_KEY` as the child had received it. Replacing
   `wall_timeout_seconds=float(timeout_sec)` with `None` in the seam failed the new policy test
   AND the pre-existing `test_a_timeout_is_red_not_a_hang`, this slice's behaviour-equality
   golden. DO NOT repeat either control: they are recorded here so this round needs no worktree,
   and G2 plus G3 are what carry those readings onto the worker's own commits.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty
at round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r51.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r51.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The five REWRITES of constraint 3: in each post-commit file the FROM occurs 0x and the TO
   exactly 1x. Report both counts and `git show --numstat` per path per commit.
 - C2 / RECORD19 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's
   prose. §4.9's per-line obligation applies in its PROSE form: every non-empty line the slice
   contains occurs exactly once among the lines C2's diff adds TO THAT PATH.
 - C4 / SEAM, C6 / TESTSDOD and C6 / TESTSGUARD are CODE APPENDS, so §4.9 as R-0531 narrows it
   orders ORDERED EQUALITY rather than a per-line count: for each, the pre-commit blob is a
   byte-exact PREFIX of the post-commit file, the slice is an exact SUFFIX, the post-commit file
   equals `pre + slice` with no joiner byte, the lines that commit's diff adds TO THAT PATH are
   exactly the slice's lines IN ORDER, and 0 marker LINES reach the file. Report `git show
   --numstat` for each path.

G4 LINT, the repository's own configuration and never `--isolated`, exit 0:
`python3 -m ruff check packages/orchestration/exec_guard.py
packages/orchestration/dod_runners.py tests/orchestration/test_dod_runners.py
tests/orchestration/test_exec_guard.py` — base reading at 3a64b65e, taken by the reviewer with
this exact command line: `All checks passed!`, exit 0. `pyproject.toml` enables the `I` rules, so
IMPT's placement between `dod_schema` and `test_runner` is checked by this gate, not by eye.

G5 CODE SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_dod_runners.py
tests/orchestration/test_exec_guard.py tests/orchestration/test_product_smoke.py -q -rf` — the
two files this round edits plus the third module that imports `dod_runners`. Base at 3a64b65e,
taken by the reviewer in the primary checkout: `147 passed`. TESTSDOD adds two tests and
TESTSGUARD adds one, so a green run reads `150 passed`; REPORT the number this run prints.

G6 STATE READERS, primary checkout, exit 0: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
ordered because C1 rewrites `.agent/plan.md`, which two of them assert on. Base at 3a64b65e:
`159 passed`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q` — base at 3a64b65e
`42 passed`. REPORT both numbers.

G7 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer
collected by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains
`## Next Steps`, matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and each of
the three booleans. G6 covers the first three through their tests; this gate covers the cap.

G8 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
3a64b65e and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 168 / 27 / 0, 141 open, max registered R-0553, max resolved
R-0532. At HEAD all three counts must be UNCHANGED and all three symmetric differences EMPTY,
because this round registers and resolves nothing; 141 open, next free id R-0554. Report the
three symmetric differences, the duplicate-id count and the count of resolutions naming an
unregistered id, at both SHAs.

G9 HYGIENE. `git diff --name-only 3a64b65e..HEAD` measured BEFORE C7 holds exactly the change set
above minus `.agent/handoff.md`, which C7 writes, and nothing else. Report per-commit insertions
for every commit BEFORE C7 — C7 cannot measure itself, so its own insertions go in the round
report — and confirm none exceeds 500. This branch spent the AGENTS.md declared-oversize allowance
at d4473f85, so a second oversize commit is a STOP under constraint 8, never a declaration.
Confirm every commit has exactly one parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 3a64b65e, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3, C4, C5, C6 and C7, the real G1-G9 results with exit codes, the open-findings count and the
next expected action. More than five commits, so the ≤100-line allowance applies; beyond it, name
the DECISION D15 stated cause and the mandated content behind the overage.
Repeat this Fortschritt line verbatim:
Fortschritt: ~87 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R50 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c erste Hälfte in dieser Runde gebaut, `_run_app_once`
offen · T002d entsperrt durch Amendment F085 D8, noch nicht gebaut · T003 offen) — Schätzung,
gegen die Klassentabelle aus Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round
is R52, and it implements T002c's second half — `_run_app_once` under the dod-app policy, taking
the CHILD half alone through `plan_child_spawn`; T002d then follows under the D8 split, then T003,
the integration gate and closure. TWO: R51's own verdict is NOT on
disk as a gate entry, because the round that records a verdict cannot record one on itself
(docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the terminator, not a missing
gate, and R52 must not open a repair round to close it; R51's verdict, when the reviewer issues
it, is recorded by R52's OWN record slice. THREE: a standalone closing line stating the open
findings count and the next free id as its own sentence, not only inside a gate transcript.
FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, because the self-drive protocol
requires every handoff that names the next session's first action to name that rule ahead of the
Open PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN5F
## Current Step
R50, this round: record the R49 PASS, register R-0552 and R-0553, and amend the F085 feature
file so the `runtime` class carries the two policies its sites actually need — the same
correction D7 made for `dod`, applied to the row D7 left standing. A planning correction; no
source file changes this round, and T002c is built at R51.

## Next Steps
1. T002c — `_run_process_check` in `packages/orchestration/dod_runners.py` onto the guard seam
   under the dod-process policy: it is a bounded check and KEEPS a wall timeout; the gap it
   closes is `env=os.environ.copy()`, which hands the child the whole parent environment.
2. T002c — `_run_app_once` in that same module under the dod-app policy: no wall timeout and
   network allowed, because it starts the app harness and probes it over HTTP.
3. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout,
   `runtime-build` keeps the one it already has. Then T003, the integration gate, then closure.
END-PLAN5F

BEGIN-PLAN5T
## Current Step
R51, this round: T002c's first half. `_run_process_check` moves onto a new `dod-process` seam in
`packages/orchestration/exec_guard.py` that keeps the check's wall timeout and its cwd pin and
replaces the `env=os.environ.copy()` copy with an allowlist; four tests ship with it. The R50
PASS is recorded in the same round.

## Next Steps
1. T002c — `_run_app_once` in `packages/orchestration/dod_runners.py` under the dod-app policy:
   no wall timeout and network allowed, because it starts the app harness and probes it over
   HTTP. It takes the CHILD half alone through `plan_child_spawn`, since it owns its own
   parent-side deadline and writes the app's output to a file rather than to a pipe.
2. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, once three uses show its shape.
3. T003 — network posture, the limitations document, its README link. Then the integration gate,
   then closure.
END-PLAN5T

BEGIN-HDRF
  through `plan_child_spawn`; since T002b the test class is PARTIALLY migrated
  through `run_guarded_test_command`, while the DoD, runtime, git and packaging
  classes still spawn unsupervised. No count is written here on purpose: it
  changes with every migration round, and the caller grep is the honest answer.
END-HDRF

BEGIN-HDRT
  through `plan_child_spawn`; since T002b the test class is PARTIALLY migrated
  through `run_guarded_test_command`; and since T002c the DoD's bounded process
  checks run through `run_guarded_dod_process_command`, while the DoD app
  harness and the runtime, git and packaging classes still spawn unsupervised.
  No count is written here on purpose: it changes with every migration round,
  and the caller grep is the honest answer.
END-HDRT

BEGIN-DOCF
  * never ``shell=True``; ``subprocess.run`` receives an argv LIST;
  * ``cwd`` is the resolved worktree (or a validated subdirectory of it);
  * the environment is inherited as-is — no extra vars, no ``.env`` reading;
  * a timeout always applies;
  * output is captured, decoded leniently, and truncated to a tail.
END-DOCF

BEGIN-DOCT
  * never ``shell=True``; the spawn receives an argv LIST;
  * ``cwd`` is the resolved worktree (or a validated subdirectory of it);
  * a timeout always applies;
  * output is captured, decoded leniently, and truncated to a tail.

Since F085 T002c the single-process kinds spawn through
``exec_guard.run_guarded_dod_process_command``, so the environment is no longer
inherited as-is: a child receives only allowlisted keys, never a secret-like
variable. The harness spawn in ``_run_app_once`` is still bare — it is the
second half of T002c, under the ``dod-app`` policy.
END-DOCT

BEGIN-IMPF
from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
END-IMPF

BEGIN-IMPT
from packages.orchestration.dod_schema import DoD, DoDCheck
from packages.orchestration.exec_guard import run_guarded_dod_process_command
from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
END-IMPT

BEGIN-SITEF
        proc = subprocess.run(
            argv,
            cwd=str(cwd),
            capture_output=True,
            timeout=ctx.timeout_sec,
            env=os.environ.copy(),
        )
END-SITEF

BEGIN-SITET
        # The guard owns the spawn since F085 T002c: it keeps this check's wall
        # timeout and its cwd pin, and replaces the whole-parent-environment copy
        # this call used to pass with the `dod-process` allowlist.
        proc = run_guarded_dod_process_command(
            argv,
            timeout_sec=ctx.timeout_sec,
            cwd=str(cwd),
        )
END-SITET

BEGIN-SEAM


# ---------------------------------------------------------------------------
# The `dod-process` seam (F085 T002c) — the DoD's own bounded checks, which
# KEEP their wall timeout: a DoD check is a check, never a service.
# ---------------------------------------------------------------------------


#: WHY: the environment a `dod-process` command may inherit, and its per-stream cap.
#: The MEMBERS are the `test`-class values and the NAMES are deliberately separate:
#: T2_F085's policy table rules `test` and `dod-process` as two rows, so widening one
#: row stays a one-line edit here instead of silently widening the other. The cap MUST
#: stay strictly ABOVE `dod_runners.MAX_OUTPUT_TAIL_CHARS` for the reason
#: `TEST_COMMAND_OUTPUT_CAP_BYTES` states about `test_runner`: the caller tails the
#: output itself and publishes `output_truncated` from that measurement.
DOD_PROCESS_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST
DOD_PROCESS_OUTPUT_CAP_BYTES: int = TEST_COMMAND_OUTPUT_CAP_BYTES


def dod_process_exec_policy(timeout_sec: float, cwd: str | None) -> ExecGuardPolicy:
    """The stage-1 policy every `dod-process` check runs under.

    A DoD check is BOUNDED — pytest, a linter, a build, a project's own command —
    so it KEEPS a wall timeout, which is what separates this class from `dod-app`
    in T2_F085's policy table. `cpu_seconds`, `address_space_bytes` and
    `open_files` are None for the reasons
    `managed_builder_execution._builder_exec_policy` already settled for the
    builder class, not restated here so the two cannot drift apart.

    `env=None` is deliberate and is the gap this seam closes: the call site it
    replaces passed `os.environ.copy()`, which handed a project-authored command
    the WHOLE parent environment. With `env=None` and an allowlist,
    `plan_child_spawn` builds the child environment from `os.environ` keeping only
    allowlisted keys, and `FORBIDDEN_ENV_KEYS` remains the floor beneath it.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec),
        output_cap_bytes=DOD_PROCESS_OUTPUT_CAP_BYTES,
        cwd=cwd,
        core_file_bytes=0,
        env=None,
        env_allowlist=DOD_PROCESS_ENV_ALLOWLIST,
    )


def run_guarded_dod_process_command(
    cmd: Sequence[str],
    *,
    timeout_sec: float,
    cwd: str | None,
) -> subprocess.CompletedProcess[bytes]:
    """Run one `dod-process` check under the guard, shaped like `subprocess.run`.

    The same three translations `run_guarded_test_command` performs, and for the
    same reason — a migrated call site keeps the result and exception shapes it
    already handled: a wall trip is raised as `subprocess.TimeoutExpired` CARRYING
    the partial streams the guard is holding, a signal death comes back as a
    NEGATIVE returncode, and `FileNotFoundError` is left to propagate, because it
    means the executable does not exist rather than that a run misbehaved.

    WHY the translation is duplicated here rather than shared: two callers are not
    yet a pattern, and the third is known — `runtime-build` at T002d, whose sites
    are `subprocess.run` calls carrying a `timeout=` of their own. That round
    extracts this, with three uses to show which parts are really common.
    """
    guarded = run_guarded(cmd, dod_process_exec_policy(timeout_sec, cwd))
    if guarded.tripped_limit == "wall_timeout":
        raise subprocess.TimeoutExpired(
            list(cmd), timeout_sec, output=guarded.stdout, stderr=guarded.stderr
        )
    returncode = guarded.returncode
    if returncode is None:
        try:
            returncode = -int(signal.Signals[guarded.term_signal].value)
        except (KeyError, ValueError, TypeError):
            returncode = -1
    return subprocess.CompletedProcess(list(cmd), returncode, guarded.stdout, guarded.stderr)
END-SEAM

BEGIN-TESTSDOD


# ---------------------------------------------------------------------------
# The `dod-process` seam (F085 T002c)
# ---------------------------------------------------------------------------

class TestTheDodProcessSeam:
    """The single-process kinds spawn through the guard, not through a bare run.

    The equality half of this slice is every other test in this file: they drive
    the real path, so a behaviour change under the guard shows up there rather
    than in a golden written for the occasion.
    """

    def test_a_check_spawns_through_the_seam_with_its_timeout_and_cwd(
            self, worktree: Path, monkeypatch):
        import subprocess as sp

        from packages.orchestration import dod_runners

        seen: dict = {}

        def _capture(cmd, *, timeout_sec, cwd):
            seen.update(cmd=list(cmd), timeout_sec=timeout_sec, cwd=cwd)
            return sp.CompletedProcess(list(cmd), 0, b"seam stdout", b"")

        monkeypatch.setattr(
            dod_runners, "run_guarded_dod_process_command", _capture)
        ev = run_check(check("custom_cmd", {"argv": EXIT_OK}),
                       worktree, timeout_sec=7)

        assert seen["cmd"] == EXIT_OK
        assert seen["timeout_sec"] == 7
        assert seen["cwd"] == str(worktree.resolve())
        assert ev.status == STATUS_PASSED
        assert "seam stdout" in ev.output_tail

    def test_a_secret_like_parent_variable_never_reaches_a_check(
            self, worktree: Path, monkeypatch):
        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "f085-must-not-leak")
        monkeypatch.setenv("F085_NOT_ALLOWLISTED", "f085-must-not-leak")
        ev = run_check(
            check("custom_cmd", {"argv": [
                "python3", "-c",
                "import json, os; print(json.dumps(dict(os.environ)))"]}),
            worktree)

        assert ev.status == STATUS_PASSED
        child_env = json.loads(ev.output_tail)
        assert "AWS_SECRET_ACCESS_KEY" not in child_env
        assert "F085_NOT_ALLOWLISTED" not in child_env
        assert "PATH" in child_env
END-TESTSDOD

BEGIN-TESTSGUARD


def test_the_dod_process_policy_keeps_the_wall_timeout_its_class_is_defined_by():
    """The one column separating `dod-process` from `dod-app` in T2_F085's table.

    Everything is reached through the `exec_guard` module handle, for the reason
    the import block states: a bare name here would meet pytest's collection
    pattern or drift from the module's own spelling. The allowlist is asserted by
    IDENTITY rather than by re-listing its members, so widening the shared set
    cannot silently make this test the second place to edit.
    """
    policy = exec_guard.dod_process_exec_policy(45, "/tmp/dod-cwd")
    assert policy.wall_timeout_seconds == 45.0
    assert policy.cwd == "/tmp/dod-cwd"
    assert policy.core_file_bytes == 0
    assert policy.output_cap_bytes == exec_guard.DOD_PROCESS_OUTPUT_CAP_BYTES
    assert policy.env is None
    assert policy.env_allowlist == exec_guard.DOD_PROCESS_ENV_ALLOWLIST
    assert not exec_guard.FORBIDDEN_ENV_KEYS & set(policy.env_allowlist)
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None
    assert policy.open_files is None
END-TESTSGUARD

BEGIN-RECORD19
Gate: R51 — the R50 entry. R50 PASSED. Every ordered gate G1-G8 was re-executed by the reviewer
over 25a5b42e..3a64b65e, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r50.md`, the committed `.agent/authored/f085-r50.md` at
c22cb9dd, the committed `.agent/last_block.md` at 634447bc and both working copies as they stand
at 3a64b65e are all five byte-EQUAL at sha256
061fa19d22524bd91e69697f28285376e82f45005d7894f833ab991adb390cd7, 24335 B, 334 lines, 12 marker
lines — every figure measured on every copy. THE SHAPES HELD, each measured separately from slices
the reviewer extracted programmatically from the committed block by marker pair rather than
retyping them. THE TWO REWRITES: PLAN4F occurs 0x and PLAN4T exactly 1x in `.agent/plan.md` at
2241cb69 at numstat `6 4`, and AMEND8F occurs 0x and AMEND8T exactly 1x in
`docs/roadmap/features/T2_F085.md` at 8bb7a287 at numstat `10 7`; both pairs give
`TO contains FROM: false`, as that block declared. THE TWO PROSE APPENDS: for RECORD18 on
`.agent/live_review.md` at 56722bd7 and for DEC8 on the feature file at 9b9cd0b4 the pre-commit
blob is a byte-exact prefix, the remainder is exactly one blank line plus the slice, the slice is
an exact suffix, 0 marker LINES reached either file, and every non-empty slice line occurs exactly
once among that path's added lines — 72 slice lines of which 2 empty against 73 added at numstat
`73 0`, and 29 slice lines of which 3 empty against 30 added at numstat `30 0`. THE SUITES WERE
RE-RUN, NOT READ, each in the primary checkout, each exit 0: the four state readers `159 passed`
against a base of 159, the canary `42 passed` against 42, the docs tier `295 passed` against 295.
THE PLAN CONTRACT HELD at 2241cb69: 41 lines against the 50-line cap, with `## Goal`,
`## Next Steps` and a roadmap F-id all present. THE ARITHMETIC MOVED AS ORDERED: 168 / 27 / 0 at
3a64b65e against 166 / 27 / 0 at 25a5b42e, 141 open against 139, the registered symmetric
difference exactly R-0552 and R-0553, done and landed symmetric differences EMPTY, no duplicate id
and no resolution naming an unregistered id at either SHA, and R-0554 free. HYGIENE IS CLEAN: over
the six commits of 25a5b42e..3a64b65e that precede the handback the per-commit INSERTION counts,
the column AGENTS.md DECISION F104 D1 fixes for the cap, are 334, 239, 6, 73, 10 and 30, and the
handback commit adds 79; none over 500; the path set of that range is exactly the six ordered paths
and nothing else; all seven commits are single-parent; the tree is clean and `git worktree list` is
one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives TOTAL 334, PROSE 182 and
RECORD18 72, agreeing with that block. THE AMENDMENT'S OWN MEASUREMENT WAS
SPOT-CHECKED rather than accepted: read at 3a64b65e, `.agent/f085_inventory.md` assigns exactly the
five sites DEC8 names to `runtime`, and `packages/orchestration/ui_server.py` really does call
`subprocess.run` with `timeout=120` twice inside `_auto_build_frontend`, for `npm install` and
`npm run build` — the pair whose working guard a no-wall-timeout policy would have removed. NO NEW
FINDING WAS REGISTERED: no gate came out red, no claim in the handback failed to reproduce, and
the open set stays at 141 with R-0554 free.
END-RECORD19
