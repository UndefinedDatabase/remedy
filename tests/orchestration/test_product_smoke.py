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
    REASON_SMOKE_DIRTY_CONSOLE,
    REASON_SMOKE_DISABLED,
    REASON_SMOKE_NOT_APPLICABLE,
    REASON_SMOKE_PATH_FAILED,
    REASON_SMOKE_START_FAILED,
    RUNNER_REGISTRY,
    STATUS_FAILED,
    STATUS_PASSED,
    run_check,
)
from packages.orchestration.dod_schema import DOD_SCHEMA_V, SMOKE_CHECK_NAMES, DoD, DoDCheck
from packages.orchestration.product_smoke import (
    CHECK_ID_APP_STARTS,
    CHECK_ID_CLEAN_CONSOLE,
    CHECK_ID_CORE_PATHS,
    CONSOLE_ERROR_PATTERNS,
    DISABLED_MESSAGE,
    MAX_EXTRACTED_PATHS,
    NOT_APPLICABLE_MESSAGE,
    PASSED_ON_RETRY,
    SMOKE_APP_STARTS,
    SMOKE_CHECKS,
    SMOKE_CLEAN_CONSOLE,
    SMOKE_CORE_PATHS,
    SMOKE_PROVIDER_NAME,
    error_patterns,
    extract_paths,
    is_registered,
    register,
    resolve_runtime,
    scan_console,
    smoke_checks,
    smoke_config,
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
                         ready_timeout_s: float = 20.0, port: int = 5273,
                         env: dict[str, str] | None = None) -> None:
    """The F007 runtime configuration the harness reads to start this project."""
    conf = root / ".remedy"
    conf.mkdir(exist_ok=True)
    argv = ", ".join(json.dumps(a) for a in cmd)
    lines = [
        "[runtime]",
        f"cmd = [{argv}]",
        'cwd = "."',
        f"port = {port}",
        f'health_path = "{health_path}"',
        f"ready_timeout_s = {ready_timeout_s}",
    ]
    if env:
        lines.append("[runtime.env]")
        lines += [f"{k} = {json.dumps(v)}" for k, v in env.items()]
    (conf / "config.toml").write_text("\n".join(lines) + "\n", encoding="utf-8")


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
        # id, the compiler owns uniqueness and provenance. Order is the block's:
        # the app must start before probing it means anything.
        assert [c.id for c in smoke] == [f"std-{CHECK_ID_APP_STARTS}",
                                         f"std-{CHECK_ID_CORE_PATHS}",
                                         f"std-{CHECK_ID_CLEAN_CONSOLE}"]
        assert all(c.source == "standard" for c in smoke)
        assert all(c.blocking is True for c in smoke)

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


# ---------------------------------------------------------------------------
# T002 — core_paths_respond
# ---------------------------------------------------------------------------

PATHS_APP = FIXTURES / "paths_app.py"


def paths_check(*paths: dict, blocking: bool = True) -> DoDCheck:
    return DoDCheck(
        id=CHECK_ID_CORE_PATHS, kind="product_smoke",
        spec={"smoke": SMOKE_CORE_PATHS, "paths": list(paths), "retry": False},
        blocking=blocking, source="standard")


class TestCorePathsVocabulary:
    def test_the_name_is_in_both_closed_vocabularies(self):
        assert SMOKE_CORE_PATHS in SMOKE_CHECKS
        assert SMOKE_CORE_PATHS in SMOKE_CHECK_NAMES

    def test_a_probe_set_is_required(self):
        with pytest.raises(Exception) as exc:
            DoDCheck(id="c1", kind="product_smoke",
                     spec={"smoke": SMOKE_CORE_PATHS}, source="standard")
        assert "non-empty 'paths'" in str(exc.value)

    @pytest.mark.parametrize("entry,needle", [
        ({"path": "orders"}, "must start with '/'"),
        ({"path": ""}, "needs a non-empty 'path'"),
        ({}, "needs a non-empty 'path'"),
        ({"path": "/x", "expect_status": "200"}, "must be an integer"),
        ({"path": "/x", "expect_status": True}, "must be an integer"),
        ({"path": "/x", "expect_text": 1}, "must be a string"),
        ({"path": "/x", "expect": "200"}, "unknown key(s): expect"),
    ])
    def test_a_nonsense_probe_is_refused_at_compile_time(self, entry, needle):
        with pytest.raises(Exception) as exc:
            paths_check(entry)
        assert needle in str(exc.value)

    def test_the_failing_entry_index_is_named(self):
        with pytest.raises(Exception) as exc:
            paths_check({"path": "/a"}, {"path": "/b"}, {"path": "nope"})
        assert "paths[2]" in str(exc.value)

    def test_paths_do_not_apply_to_app_starts(self):
        with pytest.raises(Exception) as exc:
            DoDCheck(id="c1", kind="product_smoke",
                     spec={"smoke": SMOKE_APP_STARTS, "paths": [{"path": "/"}]},
                     source="standard")
        assert "does not apply" in str(exc.value)


class TestPathExtraction:
    def _ctx(self, *, goal: str = "", hints=(), acceptance=("done",)):
        plan = FlightPlan.model_validate({
            "schema_v": "flight_plan_v1",
            "tasks": [{"id": "T001", "title": "t", "goal": "g",
                       "acceptance": list(acceptance), "est_tokens_band": "S"}],
        })
        return StandardCheckContext(
            intake={"goal": goal, "acceptance_hints": list(hints)},
            plan=plan, worktree_root="/nonexistent")

    def test_routes_are_taken_from_intent_and_plan(self):
        found = extract_paths(self._ctx(
            goal="serve /orders and /orders/new",
            hints=["the dashboard at / must render"],
            acceptance=["GET /reports returns the table"]))
        assert found[:2] == ["/orders", "/orders/new"]
        assert "/reports" in found and "/" in found

    def test_filesystem_paths_and_source_files_are_not_routes(self):
        found = extract_paths(self._ctx(
            goal="edit /home/user/app.py and tests/x.py",
            hints=["see /etc/hosts", "docs/guide.md"],
            acceptance=["update /srv/data/config.toml"]))
        assert found == [], f"probing these would be nonsense: {found}"

    def test_extraction_is_deduped_ordered_and_capped(self):
        found = extract_paths(self._ctx(
            goal=" ".join(f"/r{i}" for i in range(12)) + " /r0"))
        assert found == [f"/r{i}" for i in range(MAX_EXTRACTED_PATHS)]

    def test_the_block_probes_the_health_path_plus_extracted_routes(self, tmp_path):
        register()
        root = project(tmp_path / "app", PATHS_APP)
        ctx = StandardCheckContext(
            intake={"goal": "the /orders page must load"},
            plan=simple_plan(), worktree_root=str(root))
        checks = smoke_checks(ctx)

        assert [c.spec["smoke"] for c in checks] == [
            SMOKE_APP_STARTS, SMOKE_CORE_PATHS, SMOKE_CLEAN_CONSOLE]
        assert [p["path"] for p in checks[1].spec["paths"]] == ["/health", "/orders"]
        assert checks[1].blocking is True

    def test_not_applicable_contributes_no_probe_set(self, tmp_path):
        """No app means no paths — a filler probe would be an invented value."""
        bare = tmp_path / "bare"
        bare.mkdir()
        checks = smoke_checks(StandardCheckContext(
            intake={"goal": "/orders"}, plan=simple_plan(),
            worktree_root=str(bare)))
        assert [c.spec["smoke"] for c in checks] == [SMOKE_APP_STARTS]
        assert checks[0].blocking is False


class TestCorePathsRun:
    def test_ok_paths_pass(self, tmp_path):
        root = project(tmp_path / "app", PATHS_APP)
        ev = run_check(
            paths_check({"path": "/health"},
                        {"path": "/orders", "expect_text": "orders: 2 open"}),
            root, timeout_sec=60)

        assert ev.status == STATUS_PASSED, ev.output_tail
        assert "path /health -> 200 OK" in ev.output_tail
        assert "path /orders -> 200 OK" in ev.output_tail

    def test_a_wrong_status_is_red(self, tmp_path):
        root = project(tmp_path / "app", PATHS_APP)
        ev = run_check(paths_check({"path": "/broken"}), root, timeout_sec=60)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_PATH_FAILED
        assert "path /broken -> 500, expected an OK status" in ev.output_tail

    def test_a_declared_status_that_does_not_match_is_red(self, tmp_path):
        root = project(tmp_path / "app", PATHS_APP)
        ev = run_check(paths_check({"path": "/health", "expect_status": 204}),
                       root, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert "-> 200, expected 204" in ev.output_tail

    def test_a_missing_marker_is_red(self, tmp_path):
        root = project(tmp_path / "app", PATHS_APP)
        ev = run_check(
            paths_check({"path": "/empty", "expect_text": "orders"}),
            root, timeout_sec=60)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_PATH_FAILED
        assert "does not contain 'orders'" in ev.output_tail

    def test_an_unknown_path_is_red_not_a_pass(self, tmp_path):
        root = project(tmp_path / "app", PATHS_APP)
        ev = run_check(paths_check({"path": "/nope"}), root, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert "-> 404, expected an OK status" in ev.output_tail

    def test_a_path_failure_is_not_retried(self, tmp_path):
        """The app came up; retrying the START would hide a product failure."""
        root = project(tmp_path / "app", PATHS_APP)
        check = DoDCheck(
            id=CHECK_ID_CORE_PATHS, kind="product_smoke",
            spec={"smoke": SMOKE_CORE_PATHS, "paths": [{"path": "/broken"}],
                  "retry": True},
            blocking=True, source="standard")
        ev = run_check(check, root, timeout_sec=90)

        assert ev.reason == REASON_SMOKE_PATH_FAILED
        assert "retrying once after" not in ev.output_tail

    def test_the_app_is_stopped_after_a_path_failure(self, tmp_path):
        root = project(tmp_path / "app", PATHS_APP)
        ev = run_check(paths_check({"path": "/broken"}), root, timeout_sec=60)
        assert "the application family was stopped" in ev.output_tail

        port = int(ev.output_tail.split("port=")[1].split(")")[0])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            assert sock.connect_ex(("127.0.0.1", port)) != 0

    def test_a_project_without_a_runtime_is_not_applicable(self, tmp_path):
        bare = tmp_path / "bare"
        bare.mkdir()
        ev = run_check(paths_check({"path": "/health"}, blocking=False), bare)
        assert ev.reason == REASON_SMOKE_NOT_APPLICABLE
        assert NOT_APPLICABLE_MESSAGE in ev.output_tail


# ---------------------------------------------------------------------------
# T003 — clean_console + the smoke config table
# ---------------------------------------------------------------------------

NOISY_APP = FIXTURES / "noisy_app.py"


def console_check(*, blocking: bool = True) -> DoDCheck:
    return DoDCheck(
        id=CHECK_ID_CLEAN_CONSOLE, kind="product_smoke",
        spec={"smoke": SMOKE_CLEAN_CONSOLE, "retry": False},
        blocking=blocking, source="standard")


class TestConsolePatterns:
    def test_the_base_list_is_small_and_documented(self):
        assert 0 < len(CONSOLE_ERROR_PATTERNS) <= 10
        assert "Traceback (most recent call last)" in CONSOLE_ERROR_PATTERNS
        assert "ERROR" in CONSOLE_ERROR_PATTERNS
        # Documented in the module, so extending it is a reviewable decision.
        doc = Path("packages/orchestration/product_smoke.py").read_text("utf-8")
        for pattern in CONSOLE_ERROR_PATTERNS:
            assert pattern in doc

    def test_matching_is_case_sensitive(self):
        assert scan_console("ERROR boom", CONSOLE_ERROR_PATTERNS)
        assert not scan_console("error in prose is not a fatal",
                                CONSOLE_ERROR_PATTERNS)
        assert not scan_console("Errors are handled gracefully",
                                CONSOLE_ERROR_PATTERNS)

    def test_the_matched_lines_come_back_for_quoting(self):
        hits = scan_console("fine\nERROR could not warm the cache\nfine",
                            CONSOLE_ERROR_PATTERNS)
        assert hits == [("ERROR", "ERROR could not warm the cache")]

    def test_a_clean_stream_has_no_hits(self):
        assert scan_console("app: listening on 127.0.0.1:8080\napp: GET / 200",
                            CONSOLE_ERROR_PATTERNS) == []


class TestSmokeConfig:
    def test_defaults_are_the_documented_ones(self, monkeypatch):
        for var in ("REMEDY_SMOKE_ENABLED", "REMEDY_SMOKE_PATHS",
                    "REMEDY_SMOKE_ERROR_PATTERNS", "REMEDY_SMOKE_READY_TIMEOUT_S"):
            monkeypatch.delenv(var, raising=False)
        cfg = smoke_config()
        assert cfg["enabled"] is True
        assert cfg["paths"] == [] and cfg["error_patterns"] == []
        assert cfg["ready_timeout_s"] is None

    def test_config_EXTENDS_the_pattern_list_never_replaces_it(self, monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_ERROR_PATTERNS", "ORA-00942,my-fatal")
        patterns = error_patterns()
        assert patterns[:len(CONSOLE_ERROR_PATTERNS)] == CONSOLE_ERROR_PATTERNS
        assert "ORA-00942" in patterns and "my-fatal" in patterns

    def test_the_base_guarantees_cannot_be_configured_away(self, monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_ERROR_PATTERNS", "only-this")
        assert "ERROR" in error_patterns()

    def test_a_path_override_replaces_the_extracted_routes(self, tmp_path,
                                                           monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_PATHS", "/orders,/empty")
        register()
        root = project(tmp_path / "app", PATHS_APP)
        checks = smoke_checks(StandardCheckContext(
            intake={"goal": "the /ignored-by-override page"},
            plan=simple_plan(), worktree_root=str(root)))
        paths = [p["path"] for p in checks[1].spec["paths"]]
        assert paths == ["/health", "/orders", "/empty"]

    def test_disabled_reports_itself_and_does_not_gate(self, tmp_path, monkeypatch):
        """A switched-off smoke is a reported fact, not an absent row."""
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        root = project(tmp_path / "app", GOOD_APP)
        checks = smoke_checks(StandardCheckContext(
            intake={}, plan=simple_plan(), worktree_root=str(root)))
        assert len(checks) == 1
        assert checks[0].blocking is False
        assert "disabled by config" in checks[0].description


class TestCleanConsoleRun:
    def test_a_quiet_app_passes(self, tmp_path):
        root = project(tmp_path / "quiet", NOISY_APP,
                       env={"REMEDY_NOISY_APP_QUIET": "1"})
        ev = run_check(console_check(), root, timeout_sec=60)

        assert ev.status == STATUS_PASSED, ev.output_tail
        assert ev.reason == REASON_NONE

    def test_a_noisy_app_is_red_with_the_lines_QUOTED(self, tmp_path):
        root = project(tmp_path / "noisy", NOISY_APP)
        ev = run_check(console_check(), root, timeout_sec=60)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_DIRTY_CONSOLE
        assert "error marker(s) in the app console" in ev.output_tail
        # The real lines, quoted with the pattern that matched them.
        assert "[Traceback (most recent call last)] Traceback (most recent call last):" \
            in ev.output_tail
        assert "[ERROR] ERROR could not warm the cache; serving cold" in ev.output_tail

    def test_a_configured_pattern_makes_an_otherwise_clean_app_red(
            self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_ERROR_PATTERNS", "listening on")
        root = project(tmp_path / "quiet", NOISY_APP,
                       env={"REMEDY_NOISY_APP_QUIET": "1"})
        ev = run_check(console_check(), root, timeout_sec=60)

        assert ev.status == STATUS_FAILED
        assert ev.reason == REASON_SMOKE_DIRTY_CONSOLE
        assert "[listening on]" in ev.output_tail

    def test_the_app_is_stopped_even_when_the_console_is_dirty(self, tmp_path):
        root = project(tmp_path / "noisy", NOISY_APP)
        ev = run_check(console_check(), root, timeout_sec=60)
        assert ev.status == STATUS_FAILED
        assert "the application family was stopped" in ev.output_tail

        port = int(ev.output_tail.split("port=")[1].split(")")[0])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            assert sock.connect_ex(("127.0.0.1", port)) != 0

    def test_it_holds_a_job_open_when_blocking(self, tmp_path):
        dod = DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
                  checks=[console_check(blocking=True)])
        result = evaluate_dod(dod, project(tmp_path / "noisy", NOISY_APP))
        assert result.released is False
        assert result.blocking_red == (CHECK_ID_CLEAN_CONSOLE,)

    def test_a_project_without_a_runtime_is_not_applicable(self, tmp_path):
        bare = tmp_path / "bare"
        bare.mkdir()
        ev = run_check(console_check(blocking=False), bare)
        assert ev.reason == REASON_SMOKE_NOT_APPLICABLE


class TestThreeOrderedChecks:
    def test_the_block_contributes_all_three_in_order(self, tmp_path):
        register()
        root = project(tmp_path / "app", PATHS_APP)
        result = compile_dod({"goal": "the /orders page"}, simple_plan(), None,
                             worktree_root=str(root))
        smoke = [c for c in result.dod.checks if c.kind == "product_smoke"]

        assert [c.spec["smoke"] for c in smoke] == [
            SMOKE_APP_STARTS, SMOKE_CORE_PATHS, SMOKE_CLEAN_CONSOLE]
        assert [c.id for c in smoke] == [
            f"std-{CHECK_ID_APP_STARTS}", f"std-{CHECK_ID_CORE_PATHS}",
            f"std-{CHECK_ID_CLEAN_CONSOLE}"]
        assert all(c.blocking for c in smoke)

    def test_all_three_rows_are_green_for_a_healthy_app(self, tmp_path):
        root = project(tmp_path / "quiet", NOISY_APP,
                       env={"REMEDY_NOISY_APP_QUIET": "1"})
        dod = DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
                  checks=[smoke_check(), paths_check({"path": "/health"}),
                          console_check()])
        result = evaluate_dod(dod, root, timeout_sec=90)

        assert result.released is True, [e.output_tail for e in result.evidence
                                         if not e.green]
        assert [e.status for e in result.evidence] == [STATUS_PASSED] * 3


def test_no_zombie_processes_after_every_outcome(tmp_path):
    """Teardown always — across green, path-red and console-red alike."""
    cases = [
        (project(tmp_path / "ok", PATHS_APP), paths_check({"path": "/health"})),
        (project(tmp_path / "pathred", PATHS_APP), paths_check({"path": "/broken"})),
        (project(tmp_path / "noisered", NOISY_APP), console_check()),
    ]
    ports = []
    for root, check in cases:
        ev = run_check(check, root, timeout_sec=90)
        if "port=" in ev.output_tail:
            ports.append(int(ev.output_tail.split("port=")[1].split(")")[0]))

    assert len(ports) == 3
    time.sleep(0.2)
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2.0)
            assert sock.connect_ex(("127.0.0.1", port)) != 0, f"port {port} open"


# ---------------------------------------------------------------------------
# R-0167 — a disabled smoke must not start the app
# ---------------------------------------------------------------------------

class TestDisabledStartsNothing:
    """The off switch has to switch things OFF, not just report that it did."""

    def _marker_project(self, tmp_path: Path) -> tuple[Path, Path]:
        """A project whose app TOUCHES a marker file the moment it starts.

        The marker is the proof: asserting on it is a real process fact, not a
        claim about the runner's own bookkeeping.
        """
        root = tmp_path / "marker"
        root.mkdir()
        marker = root / "started.txt"
        (root / "marker_app.py").write_text(
            "import os, sys\n"
            f"open({str(marker)!r}, 'w').write('started')\n"
            "from http.server import BaseHTTPRequestHandler, HTTPServer\n"
            "class H(BaseHTTPRequestHandler):\n"
            "    def do_GET(self):\n"
            "        self.send_response(200); self.send_header('Content-Length','2')\n"
            "        self.end_headers(); self.wfile.write(b'ok')\n"
            "    def log_message(self, *a): pass\n"
            "s = HTTPServer(('127.0.0.1', int(os.environ.get('PORT','0'))), H)\n"
            "sys.stdout.write('marker-app: listening\\n'); sys.stdout.flush()\n"
            "s.serve_forever()\n",
            encoding="utf-8")
        write_runtime_config(root, cmd=[sys.executable, "marker_app.py"],
                             ready_timeout_s=8.0)
        return root, marker

    def test_disabled_starts_no_process_at_all(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        root, marker = self._marker_project(tmp_path)

        ev = run_check(smoke_check(), root, timeout_sec=60)

        assert not marker.exists(), "the app was started despite smoke.enabled=false"
        assert ev.argv == ()
        assert ev.command == ""
        assert ev.exit_code is None
        assert ev.duration_ms == 0

    def test_disabled_is_not_green_and_quotes_the_reason(self, tmp_path,
                                                         monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        root, _ = self._marker_project(tmp_path)

        ev = run_check(smoke_check(), root, timeout_sec=60)

        assert ev.status == STATUS_FAILED and ev.green is False
        assert ev.reason == REASON_SMOKE_DISABLED
        assert "disabled by config" in ev.output_tail
        assert ev.reason != REASON_SMOKE_NOT_APPLICABLE, (
            "a switched-off smoke is not the same fact as a project with no app")

    def test_the_enabled_default_still_runs_the_app(self, tmp_path, monkeypatch):
        monkeypatch.delenv("REMEDY_SMOKE_ENABLED", raising=False)
        root, marker = self._marker_project(tmp_path)

        ev = run_check(smoke_check(), root, timeout_sec=60)

        assert ev.status == STATUS_PASSED, ev.output_tail
        assert marker.exists(), "the default must still start the app"
        assert ev.argv and ev.duration_ms > 0

    def test_no_runtime_still_reports_not_applicable_even_when_disabled(
            self, tmp_path, monkeypatch):
        """Ordering: 'no app here' outranks 'we chose not to look'."""
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        bare = tmp_path / "bare"
        bare.mkdir()

        ev = run_check(smoke_check(blocking=False), bare)

        assert ev.reason == REASON_SMOKE_NOT_APPLICABLE
        assert NOT_APPLICABLE_MESSAGE in ev.output_tail

    def test_every_smoke_kind_refuses_early_when_disabled(self, tmp_path,
                                                          monkeypatch):
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        root, marker = self._marker_project(tmp_path)

        for check in (smoke_check(), paths_check({"path": "/health"}),
                      console_check()):
            ev = run_check(check, root, timeout_sec=60)
            assert ev.reason == REASON_SMOKE_DISABLED, check.spec["smoke"]
            assert ev.argv == ()
        assert not marker.exists()

    def test_a_stored_blocking_check_still_gates_by_its_own_flag(
            self, tmp_path, monkeypatch):
        """No gating-machinery change: the row's blocking flag decides, as ever.

        A DoD stored while the smoke was enabled carries blocking=True. Turning
        the smoke off does not silently release it — the refusal is red, and a
        red BLOCKING row holds the job exactly as before.
        """
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        root, _ = self._marker_project(tmp_path)

        held = evaluate_dod(
            DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
                checks=[smoke_check(blocking=True)]), root)
        assert held.released is False
        assert held.blocking_red == (CHECK_ID_APP_STARTS,)

        # The row the block itself contributes while disabled is non-blocking,
        # so that one reports without holding anything.
        reported = evaluate_dod(
            DoD(schema_v=DOD_SCHEMA_V, compiled=False, origin="deterministic",
                checks=[smoke_check(blocking=False)]), root)
        assert reported.released is True
        assert reported.reported_red == (CHECK_ID_APP_STARTS,)

    def test_the_disabled_text_is_one_shared_constant(self, tmp_path,
                                                      monkeypatch):
        """The compile-time row and the run-time refusal cannot drift apart."""
        monkeypatch.setenv("REMEDY_SMOKE_ENABLED", "false")
        root, _ = self._marker_project(tmp_path)

        contributed = smoke_checks(StandardCheckContext(
            intake={}, plan=simple_plan(), worktree_root=str(root)))
        ev = run_check(smoke_check(), root, timeout_sec=60)

        assert contributed[0].description == DISABLED_MESSAGE
        assert DISABLED_MESSAGE in ev.output_tail
