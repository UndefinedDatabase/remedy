# F085 R13 — record the R12 PASS, register R-0504, give `exec_guard` its first caller

Feature T2_F085 Sandbox hardening (stage 1) · Round R13 · Branch feature/f085-sandbox-hardening
Base of this round: the R12 handback commit, `git rev-parse HEAD` at start = 91f85510.
Fortschritt: ~45 % (Amendment F085 D1 angewandt · T001 gebaut · R12 PASS · T002a Scrubbing-Hälfte
gebaut · diese Runde migriert die ERSTE der fünf Builder-Sites · vier Sites, T002b-d, T003 offen).

## Goal

First the record: R12 passed the reviewer's gate and that verdict is written by THIS round's C1,
with one finding the reviewer measured while preparing this block. Then the work:
`managed_builder_execution.py`:1160 — the first of amendment F085 D1's five builder sites — stops
calling `subprocess.run` and runs through `exec_guard.run_guarded` under a stage-1 builder policy,
so the guard gains a real caller and one live seam becomes supervised.

## Bundle — six commits in this order, none added, dropped or reordered

- C0a `docs(f085): save the R13 step block verbatim` — `.agent/authored/f085-r13.md`
- C0b `docs(f085): mirror the R13 block into last_block` — `.agent/last_block.md`
- C1 `docs(review): record the R12 PASS and register a vacuous-test finding` — `.agent/live_review.md`
- C2 `feat(f085): route the managed builder spawn through the exec guard` — both source files
  together, since a commit moving the spawn without its tests would be red at that commit
- C3 `docs(f085): advance the plan to the R13 migration round` — `.agent/plan.md`
- C4 `docs(f085): rewrite the handback for R13` — `.agent/handoff.md`

## Change set — exactly these SEVEN paths, nothing else

`.agent/authored/f085-r13.md`, `.agent/last_block.md`, `.agent/live_review.md`, `.agent/plan.md`,
`.agent/handoff.md`, `packages/orchestration/managed_builder_execution.py`,
`tests/orchestration/test_managed_builder_execution.py`. Nothing under `docs/`, `apps/` or
`scripts/`, no other file under `packages/` or `tests/`; `.agent/context.md` and
`.agent/decisions.md` are deliberately NOT touched — scope and constraints are unchanged.

## Constraints

1. `cp` and the `remedy` CLI are denied here: copy with `shutil.copyfile` and prove the BYTE
   property, never the tool. Gate scratch lives under the gitignored `.remedy-wt/`.
2. Extract every slice programmatically by its one-line marker pair and apply it byte-verbatim,
   never retyped, split by substring, reformatted or reworded: the review slices' regex-looking
   text and backticks are prose and land as prose.
3. Apply each FROM/TO pair by locating the FROM exactly once and replacing it with the TO; if it
   does not occur exactly once, STOP and report. No worktree is added, removed or pruned.
4. Re-read `.agent/STOP` from disk before the FIRST commit and again before the LAST. If it exists
   at either point, finish the commit in flight, write the handback and end.

<<<SLICE REVIEW1>>>
Gate: R12 — PASS, the record round that carried the R11 verdict, one resolution and two
reviewer-gate findings onto disk. All eleven ordered gates were re-run by the reviewer and every
one reproduces the handback's reading. TRANSPORT, disk-to-disk and not by digest fallback: the
reviewer's `.remedy-wt/f085-r12.md`, the committed `.agent/authored/f085-r12.md` and
`.agent/last_block.md` are byte-EQUAL at sha256
0f66ffe7b9a96bdb9bf8f9cb130a21d7ec2b8a8102f9f02cf85fa1ff74e78678, 18334 B, 264 lines. C1 IS A
PURE APPEND, proven by shape: the pre-C1 blob is a byte-exact PREFIX of the post-C1 file, HEAD
equals it, and the 9775-byte remainder is exactly the four ordered slices, each occurring ONCE and
in order. THE ARITHMETIC: 116 / 2 / 0 at base against 118 / 3 / 0 at HEAD, so the open set rose
114 to 115 by exactly two registrations against one resolution; the registered difference is
R-0502 and R-0503 with nothing lost, the resolved difference R-0501, no duplicate ids, no
resolution naming an unregistered id. `.agent/plan.md` is 41 lines under its 50-line cap with
`## Goal`, `## Next Steps` and `## Risks` byte-IDENTICAL to base. THE HONESTY GATE HOLDS:
`exec_guard.py` and its test are byte-unchanged, so no containment claim follows from this round.
Canary 42 passed, state readers 157 passed, both matching base; insertions 264, 200, 123, 3, none
over 500; five single-parent commits, no amend or force-push; the change set is exactly the five
declared `.agent/` paths; `.agent/handoff.md` measures 85 lines against its declaration of 85; the
five declared deviations are accurate. LAST_REVIEWED_SHA advances to the R12 handback commit.
<<<END REVIEW1>>>

<<<SLICE REVIEW2>>>
- R-0504 — Medium, A SOURCE-TEXT TEST ASSERTED A KEYWORD ITS TARGET'S OWN DOCSTRING ALSO CARRIED,
SO THE TEST WAS VACUOUS FROM THE DAY IT WAS WRITTEN. Raised by the reviewer while measuring the
R13 migration, against pre-existing code and not against any round.
`tests/orchestration/test_managed_builder_execution.py::TestManagedRunner::test_shell_false_always`
read `inspect.getsource(run_managed_builder)` and asserted that `shell=False` appears in it and
`shell=True` does not. That function's DOCSTRING opens with "shell=False ALWAYS. Sanitized env.
Hard timeout. Output byte cap.", so the positive half was satisfied by prose. The reviewer PROVED
the vacuity rather than arguing it: in a disposable worktree at the round's base commit, deleting
the `shell=False` keyword from the real `subprocess.run` call and touching nothing else left the
test GREEN, exit 0, one passed. A test that stays green when the property it names is deleted was
never testing that property. The negative half fails in the mirror image: the module docstring also
carries "NO shell=True" among its hard rules, so a substring search for the dangerous form matches
prose too. The property was never at risk — `test_no_shell_true_in_orchestration` walks the AST of
every `packages/orchestration/*.py` and fails on a real `shell=True` keyword; what was at risk was
the belief that this second test added anything. This is the R-0438 and R-0502 family, a gate that
cannot fail honestly, and the third instance in three rounds, which is why severity is Medium
rather than Low: the first two were the reviewer's own gate text, this one sat in the committed
suite. Counter-measure, applied in the round that registers it: a test asserting the SHAPE of code
parses that code and inspects the AST, never searches its text, because a docstring, a comment and
a call site are indistinguishable to a substring search. C2 replaces it with an AST assertion that
`run_managed_builder` holds no `subprocess` spawn node, that `run_guarded` holds exactly one
`Popen` node passing no `shell` keyword, and that no `shell=True` keyword node exists here. OPEN.
<<<END REVIEW2>>>

<<<SLICE MBE1F>>>
import re
import subprocess
<<<END MBE1F>>>

<<<SLICE MBE1T>>>
import re
import signal
import subprocess
<<<END MBE1T>>>

<<<SLICE MBE2F>>>
from packages.orchestration.provider_trust import _safe_path_label, _scrub_public
<<<END MBE2F>>>

<<<SLICE MBE2T>>>
from packages.orchestration.exec_guard import ExecGuardPolicy, run_guarded
from packages.orchestration.provider_trust import _safe_path_label, _scrub_public
<<<END MBE2T>>>

<<<SLICE MBE3F>>>
# ---------------------------------------------------------------------------
# Managed runner (the ONLY subprocess execution point for builders)
# ---------------------------------------------------------------------------
<<<END MBE3F>>>

<<<SLICE MBE3T>>>
def _builder_exec_policy(timeout: int, max_bytes: int, cwd: str | None,
                         env: dict[str, str]) -> ExecGuardPolicy:
    """Stage-1 builder policy (F085 T002a) — only the limits this seam can prove.

    `cpu_seconds`, `address_space_bytes` and `open_files` are deliberately None: a
    value picked without measuring real builder workloads would kill legitimate builds
    (a multi-threaded build burns CPU-seconds far faster than wall-clock), and T2_F085
    makes the per-class rlimit VALUES config with per-project overrides. RLIMIT_AS also
    cannot be classified from what `wait4` reports, so a build it killed would surface
    as a plain failure. What IS enforced is real: the guard's own wall deadline, a
    per-stream output cap applied WHILE reading, the cwd pin, a zero core dump, and
    `FORBIDDEN_ENV_KEYS` as a floor beneath the template's allowlist. `env` is already
    the product of `_build_sanitized_env`, so allowlisting its keys reproduces it.
    """
    return ExecGuardPolicy(
        wall_timeout_seconds=float(timeout),
        output_cap_bytes=max_bytes,
        cwd=cwd,
        env=env,
        env_allowlist=tuple(sorted(env)),
        core_file_bytes=0,
    )


def _guarded_exit_code(guarded) -> int:
    """Translate a guard result into the integer `exit_code` this module publishes.

    `subprocess.run` reported a signal death as -SIGNUM; the guard reports
    `returncode=None` plus the signal NAME, so the negative form is rebuilt here.
    """
    if guarded.returncode is not None:
        return guarded.returncode
    try:
        return -int(signal.Signals[guarded.term_signal].value)
    except (KeyError, ValueError, TypeError):
        return -1


# ---------------------------------------------------------------------------
# Managed runner (the ONLY subprocess execution point for builders)
# ---------------------------------------------------------------------------
<<<END MBE3T>>>

<<<SLICE MBE4F>>>
    # 6. Execute subprocess — shell=False ALWAYS.
    start_time = time.monotonic()
    try:
        proc = subprocess.run(
            argv,
            shell=False,  # HARD: never True
            capture_output=True,
            timeout=timeout,
            env=env,
            cwd=repo_path or None,
        )
<<<END MBE4F>>>

<<<SLICE MBE4T>>>
    # 6. Execute subprocess — through the F085 exec guard; argv list, never a shell.
    start_time = time.monotonic()
    try:
        guarded = run_guarded(argv, _builder_exec_policy(timeout, max_bytes,
                                                         repo_path or None, env))
        if guarded.tripped_limit == "wall_timeout":
            # The guard CLASSIFIES a wall trip where subprocess.run RAISED one. Re-raise
            # so the timeout path below stays the one this module already had: the
            # migration changes the mechanism, never the observable outcome.
            raise subprocess.TimeoutExpired(argv, timeout)
        # A CompletedProcess keeps every downstream reader — returncode, stdout, stderr
        # — identical to the pre-migration shape; the slice below is then a no-op,
        # because the guard capped each stream WHILE reading it.
        proc = subprocess.CompletedProcess(argv, _guarded_exit_code(guarded),
                                           guarded.stdout, guarded.stderr)
<<<END MBE4T>>>

<<<SLICE TESTF>>>
    def test_shell_false_always(self):
        """Verify shell=False in subprocess call by checking the source."""
        import inspect
        src = inspect.getsource(run_managed_builder)
        # Must contain shell=False
        assert "shell=False" in src
        # Must NOT contain shell=True
        assert "shell=True" not in src
<<<END TESTF>>>

<<<SLICE TESTT>>>
    def test_spawn_goes_through_the_guard_and_never_through_a_shell(self):
        """Assert the no-shell property by AST, because the text form was vacuous.

        The old assertion searched this function's source for `shell=False` and was
        satisfied by its DOCSTRING (R-0504). Since F085 T002a the spawn lives in
        `exec_guard.run_guarded`, so the property is asserted where it is enforced.
        """
        import ast
        import inspect

        from packages.orchestration import exec_guard
        from packages.orchestration import managed_builder_execution as mbe

        def spawn_calls(func):
            tree = ast.parse(inspect.getsource(func))
            return [n for n in ast.walk(tree)
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                    and n.func.attr in {"run", "Popen", "call", "check_output"}
                    and isinstance(n.func.value, ast.Name)
                    and n.func.value.id == "subprocess"]

        assert spawn_calls(run_managed_builder) == []
        popens = spawn_calls(exec_guard.run_guarded)
        assert len(popens) == 1
        assert "shell" not in {kw.arg for kw in popens[0].keywords}
        # By AST, not by text: this module's own docstring carries the words
        # "NO shell=True", so a substring search fails on prose either way.
        module_tree = ast.parse(inspect.getsource(mbe))
        assert not [n for n in ast.walk(module_tree)
                    if isinstance(n, ast.keyword) and n.arg == "shell"
                    and isinstance(n.value, ast.Constant) and n.value.value is True]

    def test_wall_timeout_is_translated_into_the_timeout_status(self):
        """The guard CLASSIFIES a wall trip; this seam must still REPORT a timeout."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-to")
            t = CommandTemplate(template_id="to-test", argv_template=["sleep", "5"],
                                enabled=True, requires_approval=False, timeout_seconds=1)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-to", template_id="to-test",
                                          job_id="job-to", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.TIMEOUT
            assert result.safe_summary == "Timeout after 1s"

    def test_a_signal_death_keeps_the_negative_exit_code_contract(self):
        """subprocess.run reported -SIGNUM; the guard reports a NAME. -9 either way."""
        import tempfile
        with tempfile.TemporaryDirectory() as td:
            _create_test_session(td, "ses-sig9")
            script = Path(td) / "selfkill.py"
            script.write_text("import os, signal\nos.kill(os.getpid(), signal.SIGKILL)\n")
            t = CommandTemplate(template_id="sig9-test",
                                argv_template=["python3", str(script)],
                                enabled=True, requires_approval=False)
            save_command_template(t, data_dir=Path(td))
            result = run_managed_builder("ses-sig9", template_id="sig9-test",
                                          job_id="job-sig9", data_dir=Path(td))
            assert result.status == ManagedExecutionStatus.FAILED
            assert result.exit_code == -9

    def test_builder_policy_reproduces_the_sanitized_env_and_floors_it(self):
        """The allowlist is an identity on an already-sanitized env, and still a floor."""
        from packages.orchestration.exec_guard import scrub_child_env
        from packages.orchestration.managed_builder_execution import _builder_exec_policy
        env = _build_sanitized_env({})
        policy = _builder_exec_policy(30, 4096, None, env)
        assert scrub_child_env(env, policy.env_allowlist) == env
        assert policy.wall_timeout_seconds == 30.0 and policy.cpu_seconds is None
        smuggled = dict(env, GITHUB_TOKEN="ghp_never")
        floored = _builder_exec_policy(30, 4096, None, smuggled)
        assert "GITHUB_TOKEN" not in scrub_child_env(smuggled, floored.env_allowlist)
<<<END TESTT>>>

<<<SLICE PLANF>>>
## Current Step
R12, this round: record the R11 PASS, resolve R-0501 and register R-0502 and
R-0503 — two gate defects the reviewer wrote into its own R11 block. Pure record
round: no code, no tests, no behaviour, `.agent/` state only.

## Next Steps
1. T002a's migration half: the five builder sites of amendment F085 D1 —
   `managed_builder_execution.py`:1160, `pingpong_provider.py`:952, 1075, 1208
   and `stream_evidence.py`:595 — move to `run_guarded` with a builder policy
   and behaviour-equality goldens.
<<<END PLANF>>>

<<<SLICE PLANT>>>
## Current Step
R13, this round: record the R12 PASS, register R-0504, and migrate the FIRST of
T002a's five builder sites — `managed_builder_execution.py`:1160 — onto
`run_guarded` under a stage-1 builder policy, with behaviour-equality tests.
`exec_guard` gains its first caller in the running system.

## Next Steps
1. T002a's four REMAINING builder sites of amendment F085 D1 —
   `pingpong_provider.py`:952, 1075, 1208 and `stream_evidence.py`:595 — move to
   `run_guarded` the same way `managed_builder_execution.py` did at R13, each with
   its own behaviour-equality goldens.
<<<END PLANT>>>

## Application order

C1 appends REVIEW1 then REVIEW2 to `.agent/live_review.md`, each preceded by exactly one blank
line, appending only. C2 applies MBE1F→MBE1T, MBE2F→MBE2T, MBE3F→MBE3T and MBE4F→MBE4T to
`packages/orchestration/managed_builder_execution.py` and TESTF→TESTT to its test file. C3 applies
PLANF→PLANT to `.agent/plan.md`.

## Gates — every one is RUN and its real exit code recorded; "green" as a word is a finding

The reviewer ran each gate at the base commit before ordering it. This session's Bash tool rejects
`$?`, loops and command substitution BY FORM: read every exit code as a real
`subprocess.returncode` from `python3`.

G1 HYGIENE. `git status --porcelain` EMPTY before each of the six commits; `.agent/STOP` re-read
from disk before the first and last; `git worktree list` prints ONE line.

G2 TRANSPORT. `.agent/authored/f085-r13.md` after C0a, `.agent/last_block.md` after C0b and the
reviewer's original are byte-EQUAL: report one sha256, the byte length and the line count for all
three. C0b copies the COMMITTED C0a blob, never the scratch file.

G3 C1 SHAPE. The pre-C1 blob is a byte-exact PREFIX of the post-C1 file; HEAD equals it; the
remainder is byte-equal to one blank line + REVIEW1 + one blank line + REVIEW2; each slice occurs
exactly ONCE in the whole file at HEAD. Report C1's numstat pair as a READING, not a prediction.

G4 ARITHMETIC over `.agent/live_review.md`, regexes `^- R-\d+ — `, `^Done: R-\d+ — `,
`^Landed: R-\d+`. Base 118 / 3 / 0, 115 open; expected at HEAD 119 / 3 / 0 → 116 open, a rise of
exactly one. Report both symmetric differences, duplicate ids, any resolution naming an
unregistered id, and the max and next-free id.

G5 PAIR SHAPES over the WHOLE of each target file, counted AFTER the commit. MBE1, MBE4, TEST and
PLAN are REWRITES: FROM 0, TO 1. MBE2 and MBE3 are APPENDS whose TO contains its own FROM: FROM 1,
TO 1 — the reviewer measured both shapes in a dry run. Applying the R-0503 counter-measure: when
checking that each line added to a SOURCE file occurs once among the added lines, EXCLUDE blank
lines and bare docstring delimiters, which repeat by construction. Report the tally per pair. For
`.agent/plan.md` also report sha256, bytes and a line count under 50, with `## Goal` and
`## Risks` byte-IDENTICAL to base and `## Current Step` and `## Next Steps` not.

G6 CALLER GATE, applying the R-0502 counter-measure — name the IMPORT over TRACKED files, never a
bare filename grep, and SCOPE it to `-- packages tests` so the block files that quote this pattern
cannot match themselves. At base it names ONE path, `tests/orchestration/test_exec_guard.py`; at
HEAD it names THREE, adding the module and its test. Report the list.

G7 BEHAVIOUR EQUALITY, the round's real proof, and its IMPORT PATH. `python3 -m pytest
tests/orchestration/test_managed_builder_execution.py -q` exits 0 with 132 passed at HEAD and 0
with 129 passed at base; `python3 -m pytest tests/orchestration/test_exec_guard.py -q` exits 0
with 12 passed, unchanged. Before trusting any of it, report `managed_builder_execution.__file__`
and `exec_guard.__file__` from the primary checkout and confirm `_builder_exec_policy` and
`_guarded_exit_code` are present: a green from the wrong `sys.path` is worthless.

G8 RED CONTROLS, in a DISPOSABLE worktree under `.remedy-wt/`, never the primary checkout,
restoring the file between each. Order the COLOUR and the NAME, never a count. Each mutation of
`packages/orchestration/managed_builder_execution.py` must redden EXACTLY the named test and leave
every other test green: (a) insert a direct `subprocess.run` call into `run_managed_builder` →
`test_spawn_goes_through_the_guard_and_never_through_a_shell`; (b) disable the `wall_timeout`
re-raise → `test_wall_timeout_is_translated_into_the_timeout_status`; (c) make `_guarded_exit_code`
return `guarded.returncode` unconditionally → `test_a_signal_death_keeps_the_negative_exit_code_contract`;
(d) delete the `env_allowlist` field → `test_builder_policy_reproduces_the_sanitized_env_and_floors_it`.
Restore, confirm the suite green again, and keep the PRIMARY checkout clean throughout.

G9 RUFF, scoped to the two files this round touches, under the repository's own configuration,
measured at BASE first so a pre-existing error is never read as new: `python3 -m ruff check
packages/orchestration/managed_builder_execution.py
tests/orchestration/test_managed_builder_execution.py` — exit 0 at base and exit 0 at HEAD.

G10 STATE READERS, because this round rewrites `.agent/` state: `python3 -m pytest
tests/orchestration/test_test_runner.py tests/regression/test_resource_safety.py
tests/orchestration/test_integrity_gate.py tests/ui_server/test_dashboard_contract.py -q` exits 0
with 157 passed. CANARY: `python3 -m pytest tests/cli/test_golden_path.py -q` exits 0 with 42
passed. `test_test_runner.py` carries `test_no_shell_true_in_orchestration`, the AST guard
R-0504's replacement leans on, so this also proves that guard still runs.

G11 COMMIT HYGIENE, three readings. `git diff --name-only <base>..HEAD` measured BEFORE C4 equals
the seven declared paths minus `.agent/handoff.md` — report the list; 0 paths outside it. The `+`
column of `git show --numstat` per commit: none exceeds 500, and C4's own count is ordered nowhere
because a handback cannot measure the commit that writes it. `git log --format=%h %p <base>..HEAD`
shows ONE parent per commit and a linear chain, and `git reflog` shows every entry prefixed
`commit:` with no amend, rebase, reset, branch switch or force-push.

G12 STALENESS, reported and deliberately NOT fixed here. `exec_guard.py`'s "Deliberate absences"
says NOTHING imports it, and this module's docstring calls itself the only place that may invoke
subprocess for builder execution and promises "shell=False ALWAYS". This round falsifies the first
and outdates the second, editing neither: both belong with the four remaining sites in R14. Report
both as MEASURED findings.

## Done when

All six commits exist in order, the branch is pushed, every gate has been RUN with its real exit
code recorded, `git status --porcelain` is empty, and `.agent/handoff.md` is rewritten per
docs/agents/handback_template.md with an item-status table covering C0a through C4. Run `gh pr
list --state open --json number,headRefName,baseRefName,isDraft` after the final push and report
its output; create NO pull request and merge nothing. Report what the commands PRINTED — a gate
whose result you did not read is a finding. If a gate contradicts this block, report the
contradiction and STOP: never repair text to make a number come out, never widen the change set.
Declare every deviation with its reason.
