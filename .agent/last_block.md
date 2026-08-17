── STEP T002d first half, the seam and the extraction — F085 — R54 ───────────

Goal: add the `runtime-build` seam to `packages/orchestration/exec_guard.py` under Amendment F085
D8 — a BOUNDED class, so it KEEPS a wall timeout — and, at that third use, extract the guard-result
translation `run_guarded_test_command` and `run_guarded_dod_process_command` each carry today,
which `run_guarded_dod_process_command`'s own docstring scheduled for this round while there were
only two callers. No call site migrates here; the two `runtime-build` sites in
`packages/orchestration/ui_server.py` move at R55. The R53 PASS is recorded too, with R-0557.

Bundle, in order: C0a save this block · C0b mirror it into last_block · C1 advance
`.agent/plan.md` · C2 record R53 and register R-0557 · C3 append the shared translation and the
`runtime-build` seam · C4 move the two existing wrappers onto the shared translation · C5 append
the tests · C6 handback. That is EIGHT ordered commits, which is more than five, so the handback's
≤100-line allowance applies.

CONVENTION, binding on every count here, carried verbatim in force from the R53 block because it
is the R-0556 counter-measure. A line count is the `splitlines` reading — a trailing newline is NOT
an extra line. A SLICE IS THE BYTES STRICTLY BETWEEN ITS MARKER LINES AND THEREFORE INCLUDES THE
NEWLINE THAT TERMINATES ITS LAST CONTENT LINE: extract it as everything after the `BEGIN-` line's
own newline up to and including the newline immediately before the `END-` line, so that
`pre + slice` is already a newline-terminated file and NO joiner and NO terminator byte is ever
added. SEAM3 and TESTSRB are CODE slices CARRYING their own leading blank lines, so for each the
post-commit file is `pre + slice` exactly; RECORD22 is PROSE joined by one blank line.

## Change

C1 applies PLAN8F→PLAN8T to `.agent/plan.md` and C2 appends RECORD22 to `.agent/live_review.md`.
C3 appends SEAM3 to `packages/orchestration/exec_guard.py`: the `_completed_process_from_guarded`
helper and the `runtime-build` policy and wrapper, in one section at the end of that module. C4
applies XLAT1F→XLAT1T, XLAT2F→XLAT2T and DOCXF→DOCXT to the SAME module — the two existing wrappers
lose their copied translation bodies and call the helper C3 added, and the docstring paragraph
explaining why the translation was NOT yet shared is rewritten because C3 makes it false. C3 and C4
are separate commits because AGENTS.md forbids mixing a refactor with a new feature in one commit,
and C3 precedes C4 so no commit leaves a call to a helper that does not yet exist. C5 appends
TESTSRB to `tests/orchestration/test_exec_guard.py`.

Change set, named rather than counted: `.agent/authored/f085-r54.md`, `.agent/last_block.md`,
`.agent/plan.md`, `.agent/live_review.md`, `packages/orchestration/exec_guard.py`,
`tests/orchestration/test_exec_guard.py`, `.agent/handoff.md`. Nothing else — in particular
`packages/orchestration/ui_server.py` is NOT in it, because no call site migrates here. No
`docs/roadmap/**` path is in that set, so the §3 docs tier does NOT trigger and no `tests/docs/`
gate is ordered; `.py` files ARE in it, so a lint gate is, and G4 carries it.

## Constraints

1. Every slice is applied byte-verbatim, extracted PROGRAMMATICALLY from the committed
   `.agent/authored/f085-r54.md` by its marker pair under the CONVENTION above. Never retype one,
   never apply one from the prompt, never reflow one to a different wrap, and never add, rename or
   reorder a test the slices define. Marker lines never reach a target file.
2. Re-read `.agent/STOP` from disk before C0a and again before C6; if it exists, finish the commit
   in flight, write the handback and stop. `git status --porcelain` is empty at round start and
   after every commit. This round orders no destructive check, so it creates no worktree and
   `git worktree list` stays one line throughout.
3. PAIR SHAPES. The reviewer ran the containment test on each pair separately at emission against
   that file's blob at 8ba3ad45, and prints each pair's own output here per checklist item 15, none
   generalised to another: PLAN8F→PLAN8T `TO contains FROM: false`; XLAT1F→XLAT1T
   `TO contains FROM: false`; XLAT2F→XLAT2T `TO contains FROM: false`; DOCXF→DOCXT
   `TO contains FROM: false`. All four are REWRITES and each owes the FROM 0x / TO 1x reading over
   its whole post-commit file. PLAN8F spans the `## Current Step` section AND the
   WHOLE `## Next Steps` list rather than a prefix of either, because its TO drops the completed
   item and so changes that list's arity (checklist item 17). SEAM3 and TESTSRB are APPENDS
   carrying no FROM, so no containment reading is owed for either. Each of the four FROM texts
   occurs EXACTLY 1x in its target at 8ba3ad45 — the reviewer measured all four. XLAT1F and XLAT2F
   each CARRY their own distinguishing first line on purpose: the eleven-line translation body they
   share occurs 2x in that module at 8ba3ad45, so neither may be shortened to that body alone.
4. C1 IS THE FIRST SUBSTANTIVE COMMIT, ahead of the record and every code commit; only C0a and C0b
   may precede it. This round writes to the finding ledger, so §3 checklist item 23 binds it.
5. Every sentence in RECORD22 that states a reading of a file THIS BLOCK also edits names the SHA
   it was read at in the same clause, per checklist item 20 as R-0521 and R-0534 narrow it — the
   qualifier attaches to EVERY reading in the clause, not only the first. C0b overwrites the
   working `.agent/last_block.md` before RECORD22 lands, which is why a SHA carries those readings.
6. NO SLICE REPRODUCES A RETIRED FROM TEXT. The reviewer tested each of the four FROM texts against
   every later-applied text at emission and got NO hits — including against SEAM3, which re-adds
   the shared body XLAT1F and XLAT2F retire — so each FROM-0x reading stays attainable (item 2).
7. Nothing outside the declared change set is touched. This round REGISTERS R-0557 and resolves
   nothing, so the registered count rises by one, the done count is unchanged and the open count
   rises from 144 to 145; the next free id becomes R-0558. `.agent/plan.md` after C1 is 41 lines,
   which the reviewer projected mechanically by applying the pair to that file's blob at 8ba3ad45.
8. If a gate comes out red, STOP: write the handback naming the exact command, its exit code and
   its output, and push what is committed. Never edit a slice to make a gate green, and never widen
   the change set to route around a red.
9. THE BLOCK'S OWN SIZE, under DECISION F085 D6 as DEC6C fixes the ruled figure: 490 lines TOTAL,
   PROSE capped at 400 by D5, a RECORD slice capped at 140. The reviewer measured all three on the
   final bytes at emission and states them here: TOTAL 490, PROSE 225, RECORD22 52. The worker
   re-measures all three from the committed `.agent/authored/f085-r54.md` and reports them; a
   mismatch is a finding against this block, not against the worker.
10. THE REVIEWER ALREADY DRY-RAN THIS ROUND, at 8ba3ad45, in a disposable worktree it removed
   afterwards, with these exact slice bytes applied by the extraction ordered above: the lint gate
   and the code suite both came out GREEN on the applied tree, and a red control confirmed the
   suite can fail — dropping the wall-trip raise from the helper SEAM3 adds turned
   `test_a_wall_trip_raises_timeout_expired_carrying_the_partial_output` RED. DO NOT repeat it:
   this round needs no worktree, and G4 and G5 carry that reading onto the worker's own commits.
11. BEHAVIOURAL EQUALITY IS THE REFACTOR'S PROOF. C4 changes no observable behaviour, and the
   existing `test_exec_guard.py` tests for both migrated wrappers are what say so — no slice here
   rewrites, renames or moves one. G5 is therefore the equality golden this round owes, and a
   failure in it is a STOP under constraint 8 rather than a slice to edit.

## Done when

G1 STATE. `.agent/STOP` absent at the two points in constraint 2; `git status --porcelain` empty at
round start and after every commit; `git worktree list` one line throughout.

G2 TRANSPORT. After C0b the committed `.agent/authored/f085-r54.md`, the committed
`.agent/last_block.md` and BOTH working copies are byte-EQUAL, and all four equal the reviewer's
`.remedy-wt/f085-r54.md` — disk-to-disk, not a digest fallback. Report sha256, byte count, line
count and marker-line count. Measure every one on every copy.

G3 SHAPES, measured SEPARATELY per pair and per path.
 - The four REWRITES of constraint 3: in each post-commit file the FROM occurs 0x and the TO
   exactly 1x. Report both counts and `git show --numstat` per path per commit.
 - C2 / RECORD22 / `.agent/live_review.md`, a PROSE APPEND: the pre-commit blob is a byte-exact
   PREFIX of the post-commit file, the remainder is exactly one blank line plus the slice, the
   slice is an exact suffix, and 0 lines matching `^(BEGIN|END)-[A-Z0-9]+$` land in the file —
   count marker LINES, never the substring, since that regex already appears in that file's prose.
   §4.9's per-line PROSE obligation also applies: every non-empty line the slice contains occurs
   exactly once among the lines C2's diff adds TO THAT PATH.
 - C3 / SEAM3 and C5 / TESTSRB are CODE APPENDS, so §4.9 as R-0531 narrows it orders ORDERED
   EQUALITY rather than a per-line count, measured separately for each: the pre-commit blob is a
   byte-exact PREFIX of the post-commit file, the slice is an exact SUFFIX, the post-commit file
   equals `pre + slice` with NO byte between them and none appended after — the CONVENTION above
   makes each slice newline-terminated already — the lines that commit's diff adds TO THAT PATH are
   exactly that slice's lines IN ORDER, and 0 marker LINES reach either file. Report
   `git show --numstat` for each path.

G4 LINT, the repository's own configuration and never `--isolated`, exit 0:
`python3 -m ruff check packages/orchestration/exec_guard.py
tests/orchestration/test_exec_guard.py` — base reading at 8ba3ad45, taken by the reviewer with this
exact command line: `All checks passed!`, exit 0. `pyproject.toml` enables the `I` rules, so this
gate and not the eye is what checks import order.

G5 CODE SUITE, in the PRIMARY checkout and never in a worktree (R-0518), exit 0:
`python3 -m pytest tests/orchestration/test_exec_guard.py
tests/orchestration/test_dod_runners.py tests/orchestration/test_product_smoke.py -q -rf` — the
file this round edits plus the two modules whose behaviour the extraction must leave untouched.
Base at 8ba3ad45, taken by the reviewer in the primary checkout: `152 passed`. TESTSRB adds four
tests, so a green run reads `156 passed`; REPORT the number this run prints. Under constraint 11
it is also the refactor's equality golden.

G6 STATE READERS, primary checkout, exit 0: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -rf -q` —
ordered because C1 rewrites `.agent/plan.md`, which two of them assert on. Base at 8ba3ad45:
`159 passed`. CANARY `python3 -m pytest tests/cli/test_golden_path.py -q`, base `42 passed`. REPORT
both numbers.

G7 PLAN CONTRACT, on `.agent/plan.md` after C1, the union of every assertion the reviewer collected
by grepping `tests/` plus the AGENTS.md cap: the file contains `## Goal`, contains `## Next Steps`,
matches `\bF\d{3}\b`, and is at most 50 lines. Report the line count and the three booleans. G6
covers the first three through their tests; this gate covers the cap.

G8 ARITHMETIC. Count the registered, done and landed id sets in `.agent/live_review.md` at base
8ba3ad45 and at HEAD, from the line-start patterns for a registration, a resolution and a landed
line. The reviewer's base reading is 171 / 27 / 0, 144 open, max registered R-0556, max resolved
R-0532. At HEAD the registered count must read 172, the done count must be UNCHANGED at 27 and the
landed count UNCHANGED at 0; the registered symmetric difference must be exactly R-0557 while the
done and landed symmetric differences are EMPTY, because this round registers that one id and
resolves nothing; 145 open, next free id R-0558. Report the three symmetric differences, the
duplicate-id count and the count of resolutions naming an unregistered id, at both SHAs.

G9 HYGIENE. `git diff --name-only 8ba3ad45..HEAD` measured BEFORE C6 holds exactly the change set
above minus `.agent/handoff.md`, which C6 writes, and nothing else — and in particular does NOT
hold `packages/orchestration/ui_server.py`. Report per-commit insertions for every commit BEFORE C6
— C6 cannot measure itself, so its own insertions go in the round report — and confirm none exceeds
500. This branch spent the AGENTS.md declared-oversize allowance at d4473f85, so a second oversize
commit is a STOP under constraint 8, never a declaration. Confirm every commit is single-parent.

## Handback

Rewrite `.agent/handoff.md` per docs/agents/handback_template.md: feature and round, branch, base
SHA 8ba3ad45, a per-commit changed-files table, the item-status table covering C0a, C0b, C1, C2,
C3, C4, C5 and C6, the real G1-G9 results with exit codes, the open-findings count and the next
expected action. The Bundle above names more than five commits, so the ≤100-line allowance applies;
beyond it, name the DECISION D15 stated cause and the mandated content behind the overage.
Repeat this Fortschritt line verbatim:
Fortschritt: ~93 % (T001 gebaut · R13-R32 PASS · R33 FAIL, an R34 repariert · R34-R53 PASS ·
T002a KOMPLETT · T002b KOMPLETT · T002c KOMPLETT · T002d zur Hälfte — Naht und Extraktion in
dieser Runde, Call-Sites offen · T003 offen) — Schätzung, gegen die Klassentabelle aus
Amendment F085 D1 gemessen.

The `## Next` section carries the statements labelled ONE through FOUR below. ONE: the next round
is R55, which migrates the two `runtime-build` call sites in `_auto_build_frontend`
(`packages/orchestration/ui_server.py`) onto `run_guarded_runtime_build_command` with `check=True`,
and rewrites the `exec_guard` PARTIAL COVERAGE note in that same round if and only if the migration
makes it false. Then the three `runtime-server` sites, then T003, the integration gate and closure.
TWO: R54's own verdict is NOT on disk as a gate entry, because the round that records a verdict
cannot record one on itself (docs/agents/planner_reviewer_prompt.md §4.13) — that absence is the
terminator, and R55 must not open a repair round to close it; R54's verdict is recorded by R55's
OWN record slice. THREE: a standalone closing line stating the open findings count and the next
free id as its own sentence. FOUR: `Phase 1 rule 1 first: re-read `.agent/STOP` from disk`, which
the self-drive protocol requires every handoff naming a next action to put ahead of the PR Gate.

Then `git push -u origin feature/f085-sandbox-hardening`. No PR, no merge.

BEGIN-PLAN8F
## Current Step
R53, this round: T002c's migration, which COMPLETES T002c. `_run_app_once` in
`packages/orchestration/dod_runners.py` takes the CHILD half alone through `plan_child_spawn`
under the `dod-app` seam R52 landed, so the whole-parent-environment copy it passed becomes an
allowlist. The `exec_guard` PARTIAL COVERAGE note is rewritten in the same round, because only
this call site's move makes it false. One test ships with it. The R52 PASS is recorded in the same
round, with findings R-0555 and R-0556.

## Next Steps
1. T002d — the runtime sites under DECISION F085 D8: `runtime-server` takes no wall timeout and
   `runtime-build` keeps the one it already has. That round also extracts the guard-result
   translation the `test` and `dod-process` seams each carry, now that three uses show its shape.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.
END-PLAN8F

BEGIN-PLAN8T
## Current Step
R54, this round: T002d's first half. `packages/orchestration/exec_guard.py` gains the
`runtime-build` seam under Amendment F085 D8 — a BOUNDED class, so it KEEPS a wall timeout — and
that third caller is what makes the guard-result translation worth extracting, so the `test` and
`dod-process` wrappers move onto the shared helper in the same round. No call site migrates here.
Four tests ship with it. The R53 PASS is recorded in the same round, with finding R-0557.

## Next Steps
1. T002d's second half — migrate the two `runtime-build` sites in `_auto_build_frontend`
   (`packages/orchestration/ui_server.py`) onto the new seam with `check=True`, then the three
   `runtime-server` sites, which take no wall timeout because a clock would kill them mid-service.
2. T003 — network posture, the limitations document, its README link. That document states what
   the CHILD-half migrations do NOT bound: an app log written to a file takes no guard output cap.
   Then the integration gate, then closure.
END-PLAN8T

BEGIN-XLAT1F
    guarded = run_guarded(cmd, test_command_exec_policy(
        timeout_sec, cwd, extra_env_keys=extra_env_keys, extra_env=extra_env))
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
END-XLAT1F

BEGIN-XLAT1T
    guarded = run_guarded(cmd, test_command_exec_policy(
        timeout_sec, cwd, extra_env_keys=extra_env_keys, extra_env=extra_env))
    return _completed_process_from_guarded(cmd, timeout_sec, guarded)
END-XLAT1T

BEGIN-XLAT2F
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
END-XLAT2F

BEGIN-XLAT2T
    guarded = run_guarded(cmd, dod_process_exec_policy(timeout_sec, cwd))
    return _completed_process_from_guarded(cmd, timeout_sec, guarded)
END-XLAT2T

BEGIN-DOCXF
    WHY the translation is duplicated here rather than shared: two callers are not
    yet a pattern, and the third is known — `runtime-build` at T002d, whose sites
    are `subprocess.run` calls carrying a `timeout=` of their own. That round
    extracts this, with three uses to show which parts are really common.
END-DOCXF

BEGIN-DOCXT
    WHY the translation is shared rather than repeated here: T002d added the third
    caller, `run_guarded_runtime_build_command`, and three uses showed which parts
    are really common. `_completed_process_from_guarded` holds all three
    translations; what stays per-seam is the policy each wrapper builds, and the
    `check` knob `runtime-build` alone asks for.
END-DOCXT

BEGIN-SEAM3


# ---------------------------------------------------------------------------
# The `runtime-build` seam (F085 T002d) — the UI auto-build's npm commands, which
# KEEP their wall timeout: a build runs to completion, and `runtime-server` is the
# row Amendment F085 D8 rules must not hold a clock. The translation the three
# seams share is extracted HERE, at its third use, for the reason
# `run_guarded_dod_process_command` recorded while there were only two.
# ---------------------------------------------------------------------------


def _completed_process_from_guarded(
    cmd: Sequence[str],
    timeout_sec: float,
    guarded: ExecGuardResult,
) -> subprocess.CompletedProcess[bytes]:
    """Translate one `ExecGuardResult` into what `subprocess.run` would have returned.

    The three translations every seam-shaped wrapper performs, in one place: a wall
    trip is raised as `subprocess.TimeoutExpired` CARRYING the partial streams the
    guard is holding, a signal death comes back as a NEGATIVE returncode in the
    -SIGNUM form, and anything else becomes a `CompletedProcess` with BYTES streams.
    `FileNotFoundError` never reaches here: `Popen` raises it inside `run_guarded`
    before any supervision starts, so no wrapper ever holds a result to translate.

    Remedy deliberately does not fold `check=True` in here: only `runtime-build`
    asks for it, and one caller is not a pattern — the same reason this function
    itself waited for a third use.
    """
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


#: WHY: the environment a `runtime-build` command may inherit, and its per-stream cap.
#: The MEMBERS are the `test`-class values and the NAMES are deliberately separate, for
#: the reason `DOD_PROCESS_ENV_ALLOWLIST` states: T2_F085's policy table rules
#: `runtime-build` as its own row, so widening one row stays a one-line edit here.
RUNTIME_BUILD_ENV_ALLOWLIST: tuple[str, ...] = TEST_COMMAND_ENV_ALLOWLIST
RUNTIME_BUILD_OUTPUT_CAP_BYTES: int = TEST_COMMAND_OUTPUT_CAP_BYTES


def runtime_build_exec_policy(timeout_sec: float, cwd: str | None) -> ExecGuardPolicy:
    """The stage-1 policy every `runtime-build` command runs under.

    A build is BOUNDED — `npm install` and `npm run build` each run to completion —
    so it KEEPS a wall timeout, which is what Amendment F085 D8 separates this class
    from `runtime-server` by. Its network stays ALLOWED: the class fetches from a
    package registry, and a default-deny posture would break the command it guards.

    `cpu_seconds`, `address_space_bytes` and `open_files` are None for the reasons
    `managed_builder_execution._builder_exec_policy` already settled for the builder
    class, not restated here so the two cannot drift apart.

    `env=None` is deliberate and is the gap this seam closes: the call sites it is
    built for inherit the whole parent environment, so a secret-like variable reaches
    an npm lifecycle script a project's own `package.json` may author.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout_sec),
        output_cap_bytes=RUNTIME_BUILD_OUTPUT_CAP_BYTES,
        cwd=cwd,
        core_file_bytes=0,
        env=None,
        env_allowlist=RUNTIME_BUILD_ENV_ALLOWLIST,
    )


def run_guarded_runtime_build_command(
    cmd: Sequence[str],
    *,
    timeout_sec: float,
    cwd: str | None,
    check: bool = False,
) -> subprocess.CompletedProcess[bytes]:
    """Run one `runtime-build` command under the guard, shaped like `subprocess.run`.

    `_completed_process_from_guarded` performs the three translations this seam
    shares with `test` and `dod-process`. `check` is the part it does NOT share:
    both call sites this seam is built for pass `check=True` and catch
    `subprocess.CalledProcessError`, so the seam raises exactly that rather than
    making each site re-derive it from a returncode.
    """
    completed = _completed_process_from_guarded(
        cmd, timeout_sec, run_guarded(cmd, runtime_build_exec_policy(timeout_sec, cwd)))
    if check and completed.returncode != 0:
        raise subprocess.CalledProcessError(
            completed.returncode, list(cmd),
            output=completed.stdout, stderr=completed.stderr,
        )
    return completed
END-SEAM3

BEGIN-TESTSRB


def test_the_runtime_build_policy_keeps_the_wall_timeout_its_class_is_defined_by():
    policy = exec_guard.runtime_build_exec_policy(90.0, "/tmp")
    assert policy.wall_timeout_seconds == 90.0
    assert policy.output_cap_bytes == exec_guard.RUNTIME_BUILD_OUTPUT_CAP_BYTES
    assert policy.cwd == "/tmp"
    assert policy.core_file_bytes == 0
    assert policy.env is None
    assert policy.env_allowlist == exec_guard.RUNTIME_BUILD_ENV_ALLOWLIST
    assert policy.cpu_seconds is None
    assert policy.address_space_bytes is None


@pytest.mark.subprocess
def test_the_runtime_build_seam_hands_a_child_the_allowlist_and_not_the_secret(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-should-never-appear")
    monkeypatch.setenv("MY_PROJECT_SECRET", "should-never-appear-either")
    completed = exec_guard.run_guarded_runtime_build_command(
        _child(_ENV_DUMP), timeout_sec=30, cwd=None)
    dumped = _dumped(completed)
    assert completed.returncode == 0
    assert "PATH" in dumped
    assert "ANTHROPIC_API_KEY" not in dumped
    assert "MY_PROJECT_SECRET" not in dumped


@pytest.mark.subprocess
def test_the_runtime_build_seam_raises_called_process_error_only_when_check_is_asked():
    cmd = _child("raise SystemExit(3)")
    completed = exec_guard.run_guarded_runtime_build_command(cmd, timeout_sec=30, cwd=None)
    assert completed.returncode == 3
    with pytest.raises(subprocess.CalledProcessError) as caught:
        exec_guard.run_guarded_runtime_build_command(
            cmd, timeout_sec=30, cwd=None, check=True)
    assert caught.value.returncode == 3
    assert caught.value.cmd == cmd


@pytest.mark.subprocess
def test_the_runtime_build_seam_raises_timeout_expired_on_a_wall_trip():
    with pytest.raises(subprocess.TimeoutExpired) as caught:
        exec_guard.run_guarded_runtime_build_command(
            _child("import time; print('before', flush=True); time.sleep(30)"),
            timeout_sec=1.0, cwd=None, check=True)
    assert b"before" in (caught.value.output or b"")
END-TESTSRB

BEGIN-RECORD22
Gate: R54 — the R53 entry. R53 PASSED. Every ordered gate G1-G9 was re-executed by the reviewer
over 3bafcc1e..8ba3ad45, not read, and each reproduces the handback's reading. LINE COUNTS ARE
`splitlines` COUNTS. TRANSPORT HELD AGAINST THE REVIEWER'S OWN ORIGINAL, disk-to-disk with no
digest fallback: `.remedy-wt/f085-r53.md`, the committed `.agent/authored/f085-r53.md` at 94e4da84,
the committed `.agent/last_block.md` at 8267fde9, both of those paths at 8ba3ad45 and both working
copies as they stand at 8ba3ad45 are all seven byte-EQUAL at sha256
58a4c90c25772d8c0083afd808474e69bf96cb3c27033eb652dca7cba28f1825, 28869 B, 429 lines, 24 marker
lines — every figure measured on every copy. THE SHAPES HELD. Each of the five REWRITES gives
`TO contains FROM: false`, its FROM 1x in the pre-commit blob and 0x after with its TO exactly 1x:
PLAN7F→PLAN7T at 2e136a4e numstat `9 11`, HDRF2→HDRT2 at de4f2057 numstat `6 5`, and DOCF2→DOCT2,
IMPF2→IMPT2 and SITEF2→SITET2 all at bbd35e23, that path's numstat `27 7`. THE PROSE APPEND
RECORD21 on `.agent/live_review.md` at d5fe684c: byte-exact prefix, a remainder of exactly one
blank line plus the slice, an exact suffix, 0 marker LINES, and each of its 60 non-empty slice
lines occurring exactly once among the 63 lines that commit adds, numstat `63 0`. THE CODE APPEND
TESTSDOD2 at 85f5da00 held under ORDERED EQUALITY: the post-commit file equals `pre + slice` with
NO byte between them, that commit's added lines are exactly the slice's 41 lines IN ORDER, and 0
marker LINES reached it, numstat `41 0`. THE SUITES AND THE LINT GATE WERE RE-RUN, NOT READ, in the
primary checkout with the block's exact command lines, each exit 0: the code suite `152 passed`
against a base of 151, the four state readers `159 passed` against 159, the canary `42 passed`
against 42, and ruff `All checks passed!`. THE PLAN CONTRACT HELD at 2e136a4e: 42 lines against the
50-line cap, with `## Goal`, `## Next Steps` and a roadmap F-id present — 42 is the figure that
block projected. THE ARITHMETIC MOVED AS ORDERED: 171 / 27 / 0 at 8ba3ad45 against 169 / 27 / 0 at
3bafcc1e, 144 open against 142, the registered symmetric difference exactly R-0555 and R-0556, done
and landed symmetric differences EMPTY, no duplicate id and no resolution naming an unregistered id
at either SHA. HYGIENE IS CLEAN: walking 3bafcc1e..8ba3ad45 commit by commit the INSERTION counts,
the column AGENTS.md DECISION F104 D1 fixes for the cap, are 429, 340, 9, 63, 6, 27, 41 and 45 for
the handback commit; none over 500; that range's path set measured before the handback is exactly
the seven ordered paths and does NOT hold `tests/orchestration/test_exec_guard.py`, which that
round's change set excluded; all eight commits are single-parent; the tree is clean and
`git worktree list` is one line. THE BLOCK'S OWN SIZE re-measured from the committed file gives
TOTAL 429, PROSE 231 and RECORD21 62, agreeing with that block. THE HANDBACK'S OWN SELF-CLAIM was
checked and holds: `.agent/handoff.md` at 8ba3ad45 states 92 lines and measures 92, inside the
≤100 allowance an eight-commit round carries. THE REVIEWER ALSO RAN ITS OWN RED CONTROL on the
LANDED code rather than accepting the one that block recorded at its base: in a disposable worktree
at 8ba3ad45, removed afterwards, the new `TestTheDodAppSeam` test passed unmutated and went RED when
SITET2 was reverted to SITEF2, failing on `AWS_SECRET_ACCESS_KEY` present in the child environment
— so the migration is genuinely covered at its call site and the test is not vacuous.

- R-0557 — the R53 block's Handback section said "seven commits" over a Bundle naming eight. Low.
That block's Bundle at 8ba3ad45 names C0a, C0b, C1, C2, C3, C4, C5 and C6, and its Handback section
then wrote "This round's Bundle names seven commits, which is more than five". This is checklist
item 16's class as R-0537 and R-0543 widened it — a sentence that quantifies what follows it,
drifting because the numeral is the half nobody re-reads — and it is the SECOND instance in two
rounds: R-0555 registered exactly this shape against the R52 block, in the very record slice the
R53 block carried. Registering the class twice without changing the practice is what makes it worth
naming a counter-measure: the R54 block states its commit count ONCE, in its Bundle sentence, in
the same words the item-status list beneath it uses, so a later revision cannot move one without
visibly contradicting the other. It is LOW for the reason R-0555 was: the allowance it computes is
identical either way, since the threshold is more than five commits and both readings clear it, so
no gate and no cap moved, and the worker again read the Bundle rather than the sentence and wrote
"Eight commits" in the handback while flagging the contradiction. Found by the worker, registered
by the reviewer while gating R53.
END-RECORD22
