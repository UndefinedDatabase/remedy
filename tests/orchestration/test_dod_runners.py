"""F061 T002 — running DoD checks, and what the evidence has to say.

What the order requires proof of:

  * each of the four runnable kinds — pytest, lint, build, custom_cmd —
    proven RED and GREEN against real processes;
  * a missing tool is red with reason ``tool_unavailable``, never a pass;
  * the per-check evidence shape carries command, exit code and output tail;
  * ``runtime_flow`` has no runner in this round and fails LOUD.

Every command here is a tiny local process (this interpreter, or a two-file
throwaway repo under ``tmp_path``). No network, no repository state, and
nothing runs outside the temporary worktree the test built.
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

from packages.orchestration.dod_runners import (
    ARGV_BUILDERS,
    CHECK_TIMEOUT_DEFAULT_SEC,
    DEFAULT_ALLOWED_EXECUTABLES,
    FLOW_ACTION_OPEN,
    MAX_OUTPUT_TAIL_CHARS,
    PYTEST_PYTHON,
    REASON_APP_NOT_READY,
    REASON_APP_START_FAILED,
    REASON_CWD_MISSING,
    REASON_CWD_OUTSIDE_WORKTREE,
    REASON_EXECUTABLE_NOT_ALLOWED,
    REASON_FLOW_STEP_FAILED,
    REASON_NONE,
    REASON_NONZERO_EXIT,
    REASON_RUNTIME_NOT_CONFIGURED,
    REASON_TIMEOUT,
    REASON_TOOL_UNAVAILABLE,
    REASON_UNKNOWN_FLOW_ACTION,
    RUNNER_REGISTRY,
    STATUS_FAILED,
    STATUS_PASSED,
    CheckEvidence,
    UnsupportedCheckKindError,
    build_argv,
    run_check,
    run_checks,
    runner_for,
)
from packages.orchestration.dod_schema import DOD_SCHEMA_V, DoD, DoDCheck

#: A process that exits 0 / non-zero without touching anything.
EXIT_OK = ["python3", "-c", "print('f061 ok')"]
EXIT_BAD = ["python3", "-c", "import sys; print('f061 boom'); sys.exit(7)"]


def check(kind: str, spec: dict, **kw) -> DoDCheck:
    kw.setdefault("source", "compiled")
    return DoDCheck(id=kw.pop("id", "c1"), kind=kind, spec=spec, **kw)


@pytest.fixture
def worktree(tmp_path: Path) -> Path:
    """A throwaway worktree with one passing and one failing test file."""
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_green.py").write_text("def test_green():\n    assert True\n")
    (tests / "test_red.py").write_text(
        "def test_red():\n    assert 1 == 2, 'f061 deliberate failure'\n")
    return tmp_path


# ---------------------------------------------------------------------------
# The four runnable kinds, red and green
# ---------------------------------------------------------------------------

class TestPytestKind:
    def test_green(self, worktree: Path):
        ev = run_check(check("pytest", {"selector": "tests/test_green.py"}), worktree)
        assert ev.status == STATUS_PASSED
        assert ev.green is True
        assert ev.reason == REASON_NONE
        assert ev.exit_code == 0

    def test_red(self, worktree: Path):
        ev = run_check(check("pytest", {"selector": "tests/test_red.py"}), worktree)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_NONZERO_EXIT
        assert ev.exit_code not in (0, None)
        assert "f061 deliberate failure" in ev.output_tail

    def test_argv_uses_this_interpreter_and_the_selector(self):
        argv = build_argv(check("pytest", {"selector": "tests/x.py::test_y"}))
        assert argv[:3] == [PYTEST_PYTHON, "-m", "pytest"]
        assert "tests/x.py::test_y" in argv
        assert PYTEST_PYTHON == (sys.executable or "python3")

    def test_spec_args_are_forwarded(self):
        argv = build_argv(
            check("pytest", {"selector": "tests", "args": ["-x", "--no-header"]}))
        assert argv[argv.index("tests") + 1:] == ["-x", "--no-header", "-q"]


class TestLintKind:
    def test_green(self, worktree: Path):
        ev = run_check(
            check("lint", {"tool": "python3", "args": ["-c", "print('lint ok')"]}),
            worktree)
        assert ev.status == STATUS_PASSED
        assert ev.exit_code == 0
        assert "lint ok" in ev.output_tail

    def test_red(self, worktree: Path):
        ev = run_check(
            check("lint", {"tool": "python3",
                           "args": ["-c", "import sys; sys.exit(2)"]}),
            worktree)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_NONZERO_EXIT
        assert ev.exit_code == 2

    def test_paths_follow_the_args(self):
        argv = build_argv(check("lint", {
            "tool": "ruff", "args": ["check"], "paths": ["packages", "apps"]}))
        assert argv == ["ruff", "check", "packages", "apps"]


class TestBuildKind:
    def test_green(self, worktree: Path):
        ev = run_check(
            check("build", {"tool": "python3", "args": ["-c", "print('built')"]}),
            worktree)
        assert ev.status == STATUS_PASSED
        assert "built" in ev.output_tail

    def test_red(self, worktree: Path):
        ev = run_check(
            check("build", {"tool": "python3",
                            "args": ["-c", "raise SystemExit(1)"]}),
            worktree)
        assert ev.status == STATUS_FAILED
        assert ev.exit_code == 1


class TestCustomCmdKind:
    def test_green(self, worktree: Path):
        ev = run_check(check("custom_cmd", {"argv": EXIT_OK}), worktree)
        assert ev.status == STATUS_PASSED
        assert "f061 ok" in ev.output_tail

    def test_red(self, worktree: Path):
        ev = run_check(check("custom_cmd", {"argv": EXIT_BAD}), worktree)
        assert ev.status == STATUS_FAILED
        assert ev.exit_code == 7
        assert "f061 boom" in ev.output_tail

    def test_runs_inside_the_worktree(self, worktree: Path):
        """The process's cwd is the worktree, not the test runner's cwd."""
        ev = run_check(check("custom_cmd", {
            "argv": ["python3", "-c", "import os; print(os.getcwd())"]}), worktree)
        assert ev.output_tail.strip() == str(worktree.resolve())

    def test_a_declared_subdirectory_is_honored(self, worktree: Path):
        (worktree / "sub").mkdir()
        ev = run_check(check("custom_cmd", {
            "argv": ["python3", "-c", "import os; print(os.getcwd())"],
            "cwd": "sub"}), worktree)
        assert ev.status == STATUS_PASSED
        assert ev.output_tail.strip() == str((worktree / "sub").resolve())
        assert ev.cwd == "sub"


# ---------------------------------------------------------------------------
# Never a silent pass
# ---------------------------------------------------------------------------

class TestNeverASilentPass:
    def test_missing_tool_is_red_with_tool_unavailable(self, worktree: Path):
        """A linter that is not installed must not look like a clean linter."""
        missing = "remedy-f061-linter-that-does-not-exist"
        ev = run_check(
            check("lint", {"tool": missing}), worktree,
            allowed_executables={missing},
        )
        assert ev.status == STATUS_FAILED
        assert ev.green is False
        assert ev.reason == REASON_TOOL_UNAVAILABLE
        assert ev.exit_code is None
        assert missing in ev.output_tail

    def test_executable_outside_the_allowlist_is_refused_unrun(self, worktree: Path):
        ev = run_check(check("custom_cmd", {"argv": ["rm", "-rf", "/"]}), worktree)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_EXECUTABLE_NOT_ALLOWED
        assert ev.exit_code is None
        assert "nothing was run" in ev.output_tail

    def test_pytest_is_exempt_from_the_allowlist(self, worktree: Path):
        """Its argv is a fixed template — only the selector comes from the check."""
        ev = run_check(
            check("pytest", {"selector": "tests/test_green.py"}), worktree,
            allowed_executables=set())
        assert ev.status == STATUS_PASSED

    def test_a_missing_working_directory_is_red(self, worktree: Path):
        ev = run_check(
            check("custom_cmd", {"argv": EXIT_OK, "cwd": "not-there"}), worktree)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_CWD_MISSING
        assert ev.exit_code is None

    def test_a_working_directory_outside_the_worktree_is_red(
            self, worktree: Path, tmp_path: Path):
        """Second line of defence: the schema refuses this at compile time too."""
        outside = tmp_path.parent / "f061-outside"
        outside.mkdir(exist_ok=True)
        evil = DoDCheck.model_construct(
            id="evil", kind="custom_cmd", spec={"argv": EXIT_OK, "cwd": str(outside)},
            blocking=True, acceptance_refs=[], description="", source="compiled")
        ev = run_check(evil, worktree)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_CWD_OUTSIDE_WORKTREE
        assert ev.exit_code is None

    def test_a_timeout_is_red_not_a_hang(self, worktree: Path):
        ev = run_check(
            check("custom_cmd", {"argv": ["python3", "-c",
                                          "import time; time.sleep(30)"]}),
            worktree, timeout_sec=1)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_TIMEOUT
        assert ev.exit_code is None
        assert "[timeout expired]" in ev.output_tail

    def test_the_default_allowlist_is_the_shared_closed_list(self):
        from packages.orchestration.test_runner import _EXECUTION_SAFE_EXECUTABLES
        assert DEFAULT_ALLOWED_EXECUTABLES is _EXECUTION_SAFE_EXECUTABLES
        assert "rm" not in DEFAULT_ALLOWED_EXECUTABLES
        assert "python3" in DEFAULT_ALLOWED_EXECUTABLES


# ---------------------------------------------------------------------------
# A kind with no runner still fails LOUD (the guarantee outlives T003)
# ---------------------------------------------------------------------------

def unsupported_check(kind: str = "telepathy") -> DoDCheck:
    """A check whose kind the schema would refuse — built past validation.

    The point is the REGISTRY's behaviour, not the schema's: if a kind is ever
    added to CheckKind without a runner, this is what must happen to it.
    """
    return DoDCheck.model_construct(
        id="unsupported", kind=kind, spec={}, blocking=True,
        acceptance_refs=[], description="", source="compiled")


class TestUnsupportedKindFailsLoud:
    def test_registry_covers_exactly_the_schema_kinds(self):
        # F062 added `product_smoke`; the invariant is unchanged — every kind
        # the schema accepts has a runner, and only those.
        assert set(RUNNER_REGISTRY) == {
            "pytest", "lint", "build", "custom_cmd", "runtime_flow",
            "product_smoke"}
        assert set(ARGV_BUILDERS) == {"pytest", "lint", "build", "custom_cmd"}

    def test_runner_for_raises_on_a_kind_with_no_runner(self):
        with pytest.raises(UnsupportedCheckKindError) as exc:
            runner_for("telepathy")
        assert "telepathy" in str(exc.value)

    def test_running_such_a_check_raises_rather_than_returning_a_result(
            self, worktree: Path):
        with pytest.raises(UnsupportedCheckKindError):
            run_check(unsupported_check(), worktree)

    def test_a_dod_containing_one_fails_loud_too(self, worktree: Path):
        """No partial evidence that could be mistaken for a completed run."""
        dod = DoD.model_construct(
            schema_v=DOD_SCHEMA_V, compiled=True, origin="provider",
            checks=[
                DoDCheck(id="ok", kind="custom_cmd", spec={"argv": EXIT_OK},
                         source="compiled"),
                unsupported_check(),
            ],
        )
        with pytest.raises(UnsupportedCheckKindError):
            run_checks(dod, worktree)

    def test_runtime_flow_has_no_argv_form(self):
        """It starts an application; there is no single command to name."""
        with pytest.raises(UnsupportedCheckKindError) as exc:
            build_argv(check("runtime_flow",
                             {"steps": [{"action": "open", "path": "/"}]}))
        assert "argv" in str(exc.value)


# ---------------------------------------------------------------------------
# runtime_flow (T003) — against the fixture app, red and green
# ---------------------------------------------------------------------------

FLOW_APP = Path(__file__).parent / "fixtures" / "dod" / "flow_app.py"


def write_runtime_config(root: Path, *, cmd: list[str], health_path: str = "/health",
                         ready_timeout_s: float = 20.0,
                         env: dict[str, str] | None = None) -> None:
    """The F007 runtime configuration the harness reads to start this project."""
    conf = root / ".remedy"
    conf.mkdir(exist_ok=True)
    argv = ", ".join(json.dumps(a) for a in cmd)
    lines = [
        "[runtime]",
        f"cmd = [{argv}]",
        'cwd = "."',
        "port = 5173",
        f'health_path = "{health_path}"',
        f"ready_timeout_s = {ready_timeout_s}",
    ]
    if env:
        lines.append("[runtime.env]")
        lines += [f"{k} = {json.dumps(v)}" for k, v in env.items()]
    (conf / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def tmp_worktree(root: Path) -> Path:
    """A directory holding a copy of the fixture app, ready for a config."""
    root.mkdir(parents=True, exist_ok=True)
    shutil.copy(FLOW_APP, root / "flow_app.py")
    return root


@pytest.fixture
def flow_worktree(tmp_path: Path) -> Path:
    """A project the runtime harness can start: the fixture app + its config."""
    root = tmp_worktree(tmp_path / "app")
    write_runtime_config(root, cmd=[sys.executable, "flow_app.py"])
    return root


def flow(*steps: dict, **kw) -> DoDCheck:
    return check("runtime_flow", {"steps": list(steps)}, **kw)


def legacy_flow(*steps: dict) -> DoDCheck:
    """A flow check as it could arrive from a DoD STORED before R-0165.

    Since R-0165 the schema refuses these steps at compile time, so a valid
    construction cannot produce one. The runner's own guard is precisely the
    defence for definitions written before that rule existed — proving it
    therefore requires building the check past validation, which is what a
    stored payload effectively does when it is loaded.
    """
    return DoDCheck.model_construct(
        id="c1", kind="runtime_flow", spec={"steps": list(steps)},
        blocking=True, acceptance_refs=[], description="", source="compiled")


class TestRuntimeFlowRunner:
    def test_green_flow_against_the_fixture_app(self, flow_worktree: Path):
        ev = run_check(
            flow({"action": "open", "path": "/health", "expect_status": 200},
                 {"action": "open", "path": "/status", "expect_text": "ready: yes"}),
            flow_worktree, timeout_sec=60)
        assert ev.status == STATUS_PASSED, ev.output_tail
        assert ev.reason == REASON_NONE
        assert ev.exit_code == 0
        assert "step 1: open /health -> 200 OK" in ev.output_tail
        assert "step 2: open /status -> 200 OK" in ev.output_tail

    def test_red_when_a_step_expectation_fails(self, flow_worktree: Path):
        """The api-smoke shape: the app runs, but the flow's assertion does not hold."""
        ev = run_check(
            flow({"action": "open", "path": "/broken", "expect_status": 200}),
            flow_worktree, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_FLOW_STEP_FAILED
        assert "-> 500, expected 200" in ev.output_tail

    def test_red_when_expected_text_is_absent(self, flow_worktree: Path):
        ev = run_check(
            flow({"action": "open", "path": "/health",
                  "expect_text": "this text is not there"}),
            flow_worktree, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_FLOW_STEP_FAILED
        assert "does not contain" in ev.output_tail

    def test_the_api_service_fixture_flow_runs_red_and_green(
            self, flow_worktree: Path):
        """The golden fixture's own api-smoke spec, executed for real."""
        fixture = json.loads(
            (Path(__file__).parent / "fixtures" / "dod" / "api_service.json")
            .read_text(encoding="utf-8"))
        smoke = next(c for c in fixture["golden_dod"]["checks"]
                     if c["id"] == "api-smoke")
        smoke_check = DoDCheck.model_validate(smoke)

        green = run_check(smoke_check, flow_worktree, timeout_sec=60)
        assert green.status == STATUS_PASSED, green.output_tail

        # The SAME flow against an app that starts and is ready, but whose
        # /health now answers 500: the flow's own assertion fails. Readiness is
        # moved to /status so this is a red STEP, not a red startup.
        broken = tmp_worktree(flow_worktree.parent / "broken-app")
        write_runtime_config(
            broken, cmd=[sys.executable, "flow_app.py"], health_path="/status",
            env={"REMEDY_FLOW_APP_BREAK_HEALTH": "1"})
        red = run_check(smoke_check, broken, timeout_sec=60)
        assert red.status == STATUS_FAILED, red.output_tail
        assert red.reason == REASON_FLOW_STEP_FAILED
        assert "-> 500, expected 200" in red.output_tail

    def test_app_that_never_becomes_ready_is_red(self, tmp_path: Path):
        shutil.copy(FLOW_APP, tmp_path / "flow_app.py")
        write_runtime_config(
            tmp_path, cmd=[sys.executable, "flow_app.py"],
            health_path="/never-served", ready_timeout_s=2.0)
        ev = run_check(flow({"action": "open", "path": "/health"}),
                       tmp_path, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_APP_NOT_READY
        assert "never became ready" in ev.output_tail

    def test_app_that_exits_immediately_is_red(self, tmp_path: Path):
        write_runtime_config(
            tmp_path, cmd=[sys.executable, "-c", "raise SystemExit(9)"],
            ready_timeout_s=5.0)
        ev = run_check(flow({"action": "open", "path": "/health"}),
                       tmp_path, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_APP_START_FAILED
        assert "exited before it answered" in ev.output_tail

    def test_a_project_with_no_runtime_configuration_is_red_not_a_pass(
            self, tmp_path: Path):
        ev = run_check(flow({"action": "open", "path": "/health"}), tmp_path)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_RUNTIME_NOT_CONFIGURED
        assert ev.exit_code is None
        assert "cannot start this project" in ev.output_tail

    def test_an_unknown_action_is_red_never_satisfied(self, flow_worktree: Path):
        """A pre-R-0165 stored DoD reaching the runner: red, never satisfied."""
        ev = run_check(legacy_flow({"action": "click the button"}),
                       flow_worktree, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_UNKNOWN_FLOW_ACTION
        assert FLOW_ACTION_OPEN in ev.output_tail

    def test_an_open_step_without_a_path_is_red(self, flow_worktree: Path):
        ev = run_check(legacy_flow({"action": "open"}), flow_worktree,
                       timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_UNKNOWN_FLOW_ACTION
        assert "needs a 'path'" in ev.output_tail

    def test_the_app_is_always_stopped_afterwards(self, flow_worktree: Path):
        """Green or red, no process is left behind and no port stays bound."""
        import socket

        ev = run_check(flow({"action": "open", "path": "/health"}),
                       flow_worktree, timeout_sec=60)
        assert ev.status == STATUS_PASSED, ev.output_tail
        assert "the application family was stopped" in ev.output_tail

        port = int(ev.output_tail.split("port=")[1].split(")")[0])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            assert sock.connect_ex(("127.0.0.1", port)) != 0, (
                "the fixture app is still accepting connections")

    def test_evidence_names_the_app_command_and_the_step_log(
            self, flow_worktree: Path):
        ev = run_check(flow({"action": "open", "path": "/health"}),
                       flow_worktree, timeout_sec=60)
        assert ev.kind == "runtime_flow"
        assert ev.argv[0] == sys.executable
        assert "flow_app.py" in ev.command
        assert ev.duration_ms >= 0
        assert "--- application log ---" in ev.output_tail
        assert "flow-app: listening on" in ev.output_tail

    def test_nothing_is_written_into_the_worktree(self, flow_worktree: Path):
        """The flow log is private and temporary — never the user's repo."""
        before = sorted(p.name for p in flow_worktree.iterdir())
        run_check(flow({"action": "open", "path": "/health"}),
                  flow_worktree, timeout_sec=60)
        assert sorted(p.name for p in flow_worktree.iterdir()) == before


# ---------------------------------------------------------------------------
# Evidence shape
# ---------------------------------------------------------------------------

class TestEvidenceShape:
    def test_every_field_is_populated_for_a_real_run(self, worktree: Path):
        ev = run_check(
            check("custom_cmd", {"argv": EXIT_OK}, id="ev-1", blocking=False,
                  source="standard"),
            worktree)
        assert isinstance(ev, CheckEvidence)
        assert ev.check_id == "ev-1"
        assert ev.kind == "custom_cmd"
        assert ev.source == "standard"
        assert ev.blocking is False
        assert ev.command == " ".join(EXIT_OK)
        assert ev.argv == tuple(EXIT_OK)
        assert ev.exit_code == 0
        assert ev.duration_ms >= 0
        assert ev.output_tail
        assert ev.output_truncated is False

    def test_evidence_is_frozen(self, worktree: Path):
        ev = run_check(check("custom_cmd", {"argv": EXIT_OK}), worktree)
        with pytest.raises(Exception):
            ev.status = STATUS_FAILED  # type: ignore[misc]

    def test_long_output_is_kept_as_a_tail(self, worktree: Path):
        ev = run_check(check("custom_cmd", {"argv": [
            "python3", "-c",
            "print('x' * 200); print('LAST-LINE-F061')"]}), worktree)
        assert ev.status == STATUS_PASSED
        assert "LAST-LINE-F061" in ev.output_tail

        big = run_check(check("custom_cmd", {"argv": [
            "python3", "-c",
            f"print('y' * {MAX_OUTPUT_TAIL_CHARS * 2}); print('TAIL-F061')"]}),
            worktree)
        assert big.output_truncated is True
        assert len(big.output_tail) == MAX_OUTPUT_TAIL_CHARS
        assert "TAIL-F061" in big.output_tail

    def test_stderr_is_captured_alongside_stdout(self, worktree: Path):
        ev = run_check(check("custom_cmd", {"argv": [
            "python3", "-c",
            "import sys; print('out'); print('err', file=sys.stderr)"]}), worktree)
        assert "out" in ev.output_tail
        assert "err" in ev.output_tail

    def test_default_timeout_is_bounded(self):
        assert 0 < CHECK_TIMEOUT_DEFAULT_SEC <= 600


# ---------------------------------------------------------------------------
# Running a whole DoD
# ---------------------------------------------------------------------------

class TestRunChecks:
    def test_one_evidence_per_check_in_order(self, worktree: Path):
        dod = DoD(
            schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
            checks=[
                DoDCheck(id="green", kind="pytest",
                         spec={"selector": "tests/test_green.py"},
                         source="plan_acceptance"),
                DoDCheck(id="red", kind="custom_cmd", spec={"argv": EXIT_BAD},
                         blocking=False, source="plan_acceptance"),
            ],
        )
        evidence = run_checks(dod, worktree)
        assert [e.check_id for e in evidence] == ["green", "red"]
        assert [e.status for e in evidence] == [STATUS_PASSED, STATUS_FAILED]
        assert [e.blocking for e in evidence] == [True, False]

    def test_a_red_check_does_not_stop_the_rest(self, worktree: Path):
        dod = DoD(
            schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
            checks=[
                DoDCheck(id="red", kind="custom_cmd", spec={"argv": EXIT_BAD},
                         source="plan_acceptance"),
                DoDCheck(id="green", kind="custom_cmd", spec={"argv": EXIT_OK},
                         source="plan_acceptance"),
            ],
        )
        evidence = run_checks(dod, worktree)
        assert [e.green for e in evidence] == [False, True]


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


class TestTheDodAppSeam:
    """The harness spawn takes the CHILD half of the `dod-app` policy.

    `Popen` is captured and made to fail before exec, so no application starts
    and no process survives this test: `_run_app_once` documents that path as
    `REASON_APP_START_FAILED`, and what is judged here is the spawn the function
    was given rather than the red evidence that path then produces.
    """

    def test_the_harness_spawn_takes_the_child_half_of_the_dod_app_policy(
            self, tmp_path: Path, monkeypatch):
        from packages.orchestration import dod_runners

        monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "f085-must-not-leak")
        monkeypatch.setenv("F085_NOT_ALLOWLISTED", "f085-must-not-leak")
        root = tmp_worktree(tmp_path / "app")
        write_runtime_config(root, cmd=[sys.executable, "flow_app.py"],
                             env={"F085_DECLARED": "kept"})
        seen: dict = {}

        def _capture(argv, **kwargs):
            seen.update(argv=list(argv), kwargs=kwargs)
            raise OSError("captured before exec")

        monkeypatch.setattr(dod_runners.subprocess, "Popen", _capture)
        ev = run_check(
            flow({"action": "open", "path": "/health", "expect_status": 200}),
            root, timeout_sec=60)

        child_env = seen["kwargs"]["env"]
        assert "AWS_SECRET_ACCESS_KEY" not in child_env
        assert "F085_NOT_ALLOWLISTED" not in child_env
        assert "PATH" in child_env
        assert child_env["F085_DECLARED"] == "kept"
        assert child_env["PORT"].isdigit()
        assert Path(seen["kwargs"]["cwd"]).resolve() == root.resolve()
        assert callable(seen["kwargs"]["preexec_fn"])
        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_APP_START_FAILED
