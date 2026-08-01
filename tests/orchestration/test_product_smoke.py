"""F062 T001 — the product-smoke standard block: registration, app_starts.

What the order requires proof of:

  * the block registers into the DoD compiler's standard-check seam and
    contributes ordered blocking checks;
  * ``app_starts`` = harness start + readiness probe inside the configured
    window, with teardown ALWAYS run and no process left behind;
  * one retry after a short backoff, and a pass that needed it is recorded as
    "passed on retry";
  * a port already in use is reported as a start failure carrying the
    harness's own reason;
  * no runtime configured → "smoke: not applicable (no runtime configured)",
    reported and NOT gating — never silently green;
  * the broken-start fixture: its unit tests are green, and its job is HELD
    OPEN with a concrete reason.

Both fixture apps are REAL mini-apps under
``tests/orchestration/fixtures/smoke/`` — not mocks of the harness. Every app
is started through the harness verbs and torn down on every outcome. v1 is
HTTP level: nothing here imports a browser driver.
"""
from __future__ import annotations

import json
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest

from packages.orchestration.dod_compiler import (
    StandardCheckContext,
    compile_dod,
    registered_standard_check_providers,
)
from packages.orchestration.dod_gate import evaluate_dod, store_dod
from packages.orchestration.dod_runners import (
    REASON_NONE,
    REASON_SMOKE_NOT_APPLICABLE,
    REASON_SMOKE_START_FAILED,
    RUNNER_REGISTRY,
    STATUS_FAILED,
    STATUS_PASSED,
    run_check,
)
from packages.orchestration.dod_schema import DOD_SCHEMA_V, SMOKE_CHECK_NAMES, DoD, DoDCheck
from packages.orchestration.product_smoke import (
    CHECK_ID_APP_STARTS,
    NOT_APPLICABLE_MESSAGE,
    PASSED_ON_RETRY,
    SMOKE_APP_STARTS,
    SMOKE_PROVIDER_NAME,
    is_registered,
    register,
    resolve_runtime,
    smoke_checks,
    unregister,
)
from packages.orchestration.schemas.models import FlightPlan

FIXTURES = Path(__file__).parent / "fixtures" / "smoke"
GOOD_APP = FIXTURES / "good_app.py"
BROKEN_APP = FIXTURES / "broken_start_app.py"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_runtime_config(root: Path, *, cmd: list[str], health_path: str = "/health",
                         ready_timeout_s: float = 20.0, port: int = 5273) -> None:
    """The F007 runtime configuration the harness reads to start this project."""
    conf = root / ".remedy"
    conf.mkdir(exist_ok=True)
    argv = ", ".join(json.dumps(a) for a in cmd)
    (conf / "config.toml").write_text(
        "\n".join([
            "[runtime]",
            f"cmd = [{argv}]",
            'cwd = "."',
            f"port = {port}",
            f'health_path = "{health_path}"',
            f"ready_timeout_s = {ready_timeout_s}",
        ]) + "\n",
        encoding="utf-8",
    )


def project(root: Path, app: Path, **kw) -> Path:
    """A throwaway project: a copy of a fixture app plus its runtime config."""
    root.mkdir(parents=True, exist_ok=True)
    shutil.copy(app, root / app.name)
    write_runtime_config(root, cmd=[sys.executable, app.name], **kw)
    return root


def smoke_check(*, blocking: bool = True, retry: bool = False) -> DoDCheck:
    spec: dict = {"smoke": SMOKE_APP_STARTS}
    if not retry:
        spec["retry"] = False
    return DoDCheck(id=CHECK_ID_APP_STARTS, kind="product_smoke", spec=spec,
                    blocking=blocking, source="standard")


def simple_plan(*acceptance: str) -> FlightPlan:
    return FlightPlan.model_validate({
        "schema_v": "flight_plan_v1",
        "tasks": [{"id": "T001", "title": "t", "goal": "g",
                   "acceptance": list(acceptance) or ["tests/x.py passes"],
                   "est_tokens_band": "S"}],
    })


@pytest.fixture(autouse=True)
def _clean_seam():
    """The seam is process-global; never leak a registration between tests."""
    before = registered_standard_check_providers()
    yield
    if SMOKE_PROVIDER_NAME not in before:
        unregister()


# ---------------------------------------------------------------------------
# The fixture apps are real, and the broken one's unit tests are GREEN
# ---------------------------------------------------------------------------

class TestFixtureApps:
    def test_both_fixtures_exist_as_real_files(self):
        assert GOOD_APP.is_file() and BROKEN_APP.is_file()

    def test_the_broken_app_unit_tests_are_green(self):
        """The premise of the whole feature: tests pass, the product is broken."""
        sys.path.insert(0, str(FIXTURES))
        try:
            import broken_start_app  # noqa: PLC0415 - fixture app, loaded on purpose
        finally:
            sys.path.pop(0)

        assert broken_start_app.tax_cents(10_000, 19) == 1900
        assert broken_start_app.tax_cents(0, 19) == 0
        with pytest.raises(ValueError):
            broken_start_app.tax_cents(-1, 19)

    def test_the_broken_app_really_fails_to_start(self):
        """Not a mocked failure: the process exits non-zero with its reason."""
        proc = subprocess.run(
            [sys.executable, str(BROKEN_APP)], capture_output=True, text=True,
            timeout=30, env={"PATH": "/usr/bin:/bin"})
        assert proc.returncode == 78
        assert "PAYMENTS_ENDPOINT is not set" in proc.stdout

    def test_no_browser_dependency_is_introduced(self):
        """v1 is HTTP level; a browser driver in this feature is a reject."""
        banned = ("selenium", "playwright", "puppeteer", "webdriver")
        for path in (Path("packages/orchestration/product_smoke.py"),
                     Path(__file__), GOOD_APP, BROKEN_APP):
            text = path.read_text(encoding="utf-8").lower()
            for name in banned:
                assert f"import {name}" not in text and f"from {name}" not in text


# ---------------------------------------------------------------------------
# Registration into the DoD compiler's seam
# ---------------------------------------------------------------------------

class TestRegistration:
    def test_registration_is_explicit_not_an_import_side_effect(self):
        assert not is_registered(), (
            "importing product_smoke must not change what every DoD contains")
        register()
        assert is_registered()

    def test_registering_twice_is_a_no_op(self):
        register()
        register()
        assert registered_standard_check_providers().count(SMOKE_PROVIDER_NAME) == 1

    def test_the_block_reaches_a_compiled_dod_as_a_standard_check(self, tmp_path):
        register()
        root = project(tmp_path / "app", GOOD_APP)
        result = compile_dod({"goal": "g"}, simple_plan(), None,
                             worktree_root=str(root))

        smoke = [c for c in result.dod.checks if c.kind == "product_smoke"]
        # The compiler namespaces standard ids (F061): a provider proposes an
        # id, the compiler owns uniqueness and provenance.
        assert [c.id for c in smoke] == [f"std-{CHECK_ID_APP_STARTS}"]
        assert smoke[0].source == "standard"
        assert smoke[0].blocking is True

    def test_the_schema_knows_the_kind_and_its_runner_exists(self):
        assert SMOKE_APP_STARTS in SMOKE_CHECK_NAMES
        assert "product_smoke" in RUNNER_REGISTRY

    def test_an_unknown_smoke_name_is_refused_at_compile_time(self):
        with pytest.raises(Exception) as exc:
            DoDCheck(id="c1", kind="product_smoke", spec={"smoke": "teleports"},
                     source="standard")
        assert "unknown check" in str(exc.value)

    def test_no_project_context_contributes_nothing(self):
        """The compiler had no worktree: claiming either way would be invented."""
        ctx = StandardCheckContext(intake={}, plan=simple_plan(), worktree_root="")
        assert smoke_checks(ctx) == []


# ---------------------------------------------------------------------------
# The not-applicable path
# ---------------------------------------------------------------------------

class TestNotApplicable:
    def test_a_project_with_no_runtime_is_reported_not_gated(self, tmp_path):
        register()
        bare = tmp_path / "bare"
        bare.mkdir()
        (bare / "notes.md").write_text("no app here\n", encoding="utf-8")

        result = compile_dod({"goal": "g"}, simple_plan(), None,
                             worktree_root=str(bare))
        smoke = [c for c in result.dod.checks if c.kind == "product_smoke"]
        assert len(smoke) == 1
        assert smoke[0].blocking is False, "not-applicable must never gate"
        assert NOT_APPLICABLE_MESSAGE in smoke[0].description

    def test_running_it_reports_not_applicable_and_is_not_green(self, tmp_path):
        bare = tmp_path / "bare"
        bare.mkdir()
        ev = run_check(smoke_check(blocking=False), bare)

        assert ev.status == STATUS_FAILED, "never silently green"
        assert ev.reason == REASON_SMOKE_NOT_APPLICABLE
        assert NOT_APPLICABLE_MESSAGE in ev.output_tail

    def test_it_does_not_hold_a_job(self, tmp_path):
        """Reported, not gating: the gate releases with it in the matrix."""
        bare = tmp_path / "bare"
        bare.mkdir()
        dod = DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
                  checks=[smoke_check(blocking=False)])
        result = evaluate_dod(dod, bare)

        assert result.released is True
        assert result.blocking_red == ()
        assert result.reported_red == (CHECK_ID_APP_STARTS,)

    def test_resolve_runtime_reports_the_harness_reason(self, tmp_path):
        bare = tmp_path / "bare"
        bare.mkdir()
        spec, reason = resolve_runtime(bare)
        assert spec is None and reason, "the harness's own text, not an invented one"


# ---------------------------------------------------------------------------
# app_starts — green
# ---------------------------------------------------------------------------

class TestAppStartsGreen:
    def test_a_clean_app_passes(self, tmp_path):
        root = project(tmp_path / "app", GOOD_APP)
        ev = run_check(smoke_check(), root, timeout_sec=60)

        assert ev.status == STATUS_PASSED, ev.output_tail
        assert ev.reason == REASON_NONE
        assert "ready on /health" in ev.output_tail
        assert "good-app: listening on" in ev.output_tail

    def test_the_app_is_always_stopped(self, tmp_path):
        """Teardown on every outcome — asserted against the real port."""
        root = project(tmp_path / "app", GOOD_APP)
        ev = run_check(smoke_check(), root, timeout_sec=60)
        assert ev.status == STATUS_PASSED, ev.output_tail
        assert "the application family was stopped" in ev.output_tail

        port = int(ev.output_tail.split("port=")[1].split(")")[0])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            assert sock.connect_ex(("127.0.0.1", port)) != 0, "app still listening"

    def test_nothing_is_written_into_the_project(self, tmp_path):
        root = project(tmp_path / "app", GOOD_APP)
        before = sorted(p.name for p in root.iterdir())
        run_check(smoke_check(), root, timeout_sec=60)
        assert sorted(p.name for p in root.iterdir()) == before


# ---------------------------------------------------------------------------
# app_starts — red, and the job it holds open
# ---------------------------------------------------------------------------

class TestBrokenStartHoldsTheJob:
    def _broken(self, tmp_path: Path) -> Path:
        return project(tmp_path / "broken", BROKEN_APP, ready_timeout_s=6.0)

    def test_a_broken_start_is_red_with_a_concrete_reason(self, tmp_path):
        ev = run_check(smoke_check(), self._broken(tmp_path), timeout_sec=90)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_START_FAILED
        assert "start failed: " in ev.output_tail, "the finding must be concrete"
        assert "exited before it answered /health" in ev.output_tail
        # The app's own fatal line is carried through, not paraphrased.
        assert "PAYMENTS_ENDPOINT is not set" in ev.output_tail

    def test_the_job_is_held_open(self, tmp_path):
        """Green unit tests, blocked job — the acceptance criterion itself."""
        dod = DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
                  checks=[smoke_check(blocking=True)])
        result = evaluate_dod(dod, self._broken(tmp_path))

        assert result.released is False, "a red blocking smoke must hold the job"
        assert result.blocking_red == (CHECK_ID_APP_STARTS,)
        assert result.evidence[0].reason == REASON_SMOKE_START_FAILED

    def test_the_held_job_reports_which_check_failed_and_why(self, tmp_path,
                                                             monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path / "data"))
        job_id = "77777777-7777-4777-8777-777777777777"
        store_dod(job_id, DoD(schema_v=DOD_SCHEMA_V, compiled=False,
                              origin="deterministic",
                              checks=[smoke_check(blocking=True)]))

        from packages.orchestration.dod_gate import matrix_rows, run_job_gate
        result = run_job_gate(job_id, self._broken(tmp_path))

        assert result is not None and result.released is False
        row = matrix_rows(result)[0]
        assert row[0] == CHECK_ID_APP_STARTS
        assert row[1] == "product_smoke"
        assert row[2] == "yes"          # blocking
        assert row[3] == "failed"
        assert row[4] == REASON_SMOKE_START_FAILED

    def test_the_app_is_stopped_even_on_the_red_path(self, tmp_path):
        ev = run_check(smoke_check(), self._broken(tmp_path), timeout_sec=90)
        assert ev.status == STATUS_FAILED
        assert "the application family was stopped" in ev.output_tail


# ---------------------------------------------------------------------------
# Retry, and the port-conflict reason
# ---------------------------------------------------------------------------

class TestRetryAndPortConflict:
    def test_a_flaky_start_passes_on_retry_and_says_so(self, tmp_path):
        """First attempt fails, second succeeds — the pass is labeled."""
        root = tmp_path / "flaky"
        root.mkdir()
        marker = root / "attempts.txt"
        app = root / "flaky_app.py"
        app.write_text(
            "import os, sys\n"
            f"m = {str(marker)!r}\n"
            "n = 0\n"
            "if os.path.exists(m):\n"
            "    n = int(open(m).read() or 0)\n"
            "open(m, 'w').write(str(n + 1))\n"
            "if n == 0:\n"
            "    sys.stdout.write('flaky-app: cold start failed\\n')\n"
            "    sys.stdout.flush()\n"
            "    raise SystemExit(1)\n"
            "from http.server import BaseHTTPRequestHandler, HTTPServer\n"
            "class H(BaseHTTPRequestHandler):\n"
            "    def do_GET(self):\n"
            "        self.send_response(200); self.send_header('Content-Length','2')\n"
            "        self.end_headers(); self.wfile.write(b'ok')\n"
            "    def log_message(self, *a): pass\n"
            "s = HTTPServer(('127.0.0.1', int(os.environ.get('PORT','0'))), H)\n"
            "sys.stdout.write('flaky-app: listening\\n'); sys.stdout.flush()\n"
            "s.serve_forever()\n",
            encoding="utf-8")
        write_runtime_config(root, cmd=[sys.executable, "flaky_app.py"],
                             ready_timeout_s=6.0)

        ev = run_check(smoke_check(retry=True), root, timeout_sec=120)

        assert ev.status == STATUS_PASSED, ev.output_tail
        assert PASSED_ON_RETRY in ev.output_tail
        assert "retrying once after" in ev.output_tail
        assert marker.read_text().strip() == "2", "exactly two attempts"

    def test_retry_is_bounded_to_one(self, tmp_path):
        """A permanently broken app is attempted twice, never more."""
        root = tmp_path / "always-broken"
        root.mkdir()
        marker = root / "attempts.txt"
        app = root / "dead_app.py"
        app.write_text(
            "import os, sys\n"
            f"m = {str(marker)!r}\n"
            "n = int(open(m).read()) if os.path.exists(m) else 0\n"
            "open(m, 'w').write(str(n + 1))\n"
            "sys.stdout.write('dead-app: never starts\\n'); sys.stdout.flush()\n"
            "raise SystemExit(3)\n",
            encoding="utf-8")
        write_runtime_config(root, cmd=[sys.executable, "dead_app.py"],
                             ready_timeout_s=4.0)

        ev = run_check(smoke_check(retry=True), root, timeout_sec=120)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_START_FAILED
        assert marker.read_text().strip() == "2", "one retry, not a loop"

    def test_a_port_in_use_is_reported_as_a_start_failure(self, tmp_path):
        """The harness picks a free port; an app that insists on a taken one
        dies, and the smoke reports that as the start failure it is."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as squatter:
            squatter.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            squatter.bind(("127.0.0.1", 0))
            squatter.listen(1)
            taken = squatter.getsockname()[1]

            root = tmp_path / "port-clash"
            root.mkdir()
            app = root / "fixed_port_app.py"
            app.write_text(
                "import sys\n"
                "from http.server import BaseHTTPRequestHandler, HTTPServer\n"
                f"PORT = {taken}\n"
                "try:\n"
                "    HTTPServer(('127.0.0.1', PORT), BaseHTTPRequestHandler)\n"
                "except OSError as exc:\n"
                "    sys.stdout.write('fixed-port-app: bind failed: %s\\n' % exc)\n"
                "    sys.stdout.flush()\n"
                "    raise SystemExit(1)\n",
                encoding="utf-8")
            write_runtime_config(root, cmd=[sys.executable, "fixed_port_app.py"],
                                 ready_timeout_s=5.0)

            ev = run_check(smoke_check(), root, timeout_sec=90)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_START_FAILED
        assert "start failed: " in ev.output_tail
        assert "bind failed" in ev.output_tail, "the harness's own reason survives"


# ---------------------------------------------------------------------------
# Evidence shape
# ---------------------------------------------------------------------------

class TestEvidence:
    def test_the_check_carries_its_command_and_timing(self, tmp_path):
        root = project(tmp_path / "app", GOOD_APP)
        ev = run_check(smoke_check(), root, timeout_sec=60)

        assert ev.check_id == CHECK_ID_APP_STARTS
        assert ev.kind == "product_smoke"
        assert ev.source == "standard"
        assert ev.argv and ev.argv[0] == sys.executable
        assert "good_app.py" in ev.command
        assert ev.duration_ms >= 0

    def test_a_not_applicable_result_ran_nothing(self, tmp_path):
        bare = tmp_path / "bare"
        bare.mkdir()
        ev = run_check(smoke_check(blocking=False), bare)
        assert ev.argv == () and ev.exit_code is None and ev.duration_ms == 0


def test_no_zombie_processes_after_the_suite(tmp_path):
    """A final sweep: run both outcomes, then assert nothing of ours survives."""
    good = project(tmp_path / "good", GOOD_APP)
    broken = project(tmp_path / "broken", BROKEN_APP, ready_timeout_s=6.0)

    ports = []
    for root in (good, broken):
        ev = run_check(smoke_check(), root, timeout_sec=90)
        if "port=" in ev.output_tail:
            ports.append(int(ev.output_tail.split("port=")[1].split(")")[0]))

    time.sleep(0.2)
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            assert sock.connect_ex(("127.0.0.1", port)) != 0, f"port {port} still open"
