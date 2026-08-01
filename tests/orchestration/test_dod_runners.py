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

import sys
from pathlib import Path

import pytest

from packages.orchestration.dod_runners import (
    CHECK_TIMEOUT_DEFAULT_SEC,
    DEFAULT_ALLOWED_EXECUTABLES,
    MAX_OUTPUT_TAIL_CHARS,
    PYTEST_PYTHON,
    REASON_CWD_MISSING,
    REASON_CWD_OUTSIDE_WORKTREE,
    REASON_EXECUTABLE_NOT_ALLOWED,
    REASON_NONE,
    REASON_NONZERO_EXIT,
    REASON_TIMEOUT,
    REASON_TOOL_UNAVAILABLE,
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
# runtime_flow: schema-valid, but no runner in this round
# ---------------------------------------------------------------------------

class TestRuntimeFlowFailsLoud:
    def test_registry_has_no_runtime_flow_entry(self):
        assert set(RUNNER_REGISTRY) == {"pytest", "lint", "build", "custom_cmd"}
        assert "runtime_flow" not in RUNNER_REGISTRY

    def test_runner_for_raises(self):
        with pytest.raises(UnsupportedCheckKindError) as exc:
            runner_for("runtime_flow")
        assert "runtime_flow" in str(exc.value)

    def test_running_the_check_raises_rather_than_returning_a_result(
            self, worktree: Path):
        flow = check("runtime_flow", {"steps": [{"action": "open /health"}]})
        with pytest.raises(UnsupportedCheckKindError):
            run_check(flow, worktree)

    def test_a_dod_containing_one_fails_loud_too(self, worktree: Path):
        """No partial evidence that could be mistaken for a completed run."""
        dod = DoD(
            schema_v=DOD_SCHEMA_V, compiled=True, origin="provider",
            checks=[
                DoDCheck(id="ok", kind="custom_cmd", spec={"argv": EXIT_OK},
                         source="compiled"),
                DoDCheck(id="flow", kind="runtime_flow",
                         spec={"steps": [{"action": "open /"}]}, source="compiled"),
            ],
        )
        with pytest.raises(UnsupportedCheckKindError):
            run_checks(dod, worktree)


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
