"""
Domain tests: ui_server/test_diff_endpoint.py

F037 T001, the read endpoint: the two GET routes that hand `build_diff_view`'s
envelope to a client. The server is a REAL one on a free port — the routes are
the thing under test, so a direct call to the builder would prove nothing about
dispatch.
"""

from __future__ import annotations

import json
import statistics
import threading
import time
from http.client import HTTPConnection
from pathlib import Path

import pytest

from packages.core.models import Job, Task
from packages.orchestration.diff_parser import DIFF_VIEW_MAX_BODY_LINES

# WHY the two diffs name DIFFERENT files: serving the job diff where the task
# run's was asked for — or the reverse — is then a red rather than a shrug.
JOB_DIFF_PATH = "packages/orchestration/job_scope_only.py"
TASK_DIFF_PATH = "packages/orchestration/task_scope_only.py"

JOB_DIFF = f"""diff --git a/{JOB_DIFF_PATH} b/{JOB_DIFF_PATH}
--- a/{JOB_DIFF_PATH}
+++ b/{JOB_DIFF_PATH}
@@ -1,2 +1,2 @@
 a line that did not move
-the old job line
+the new job line
"""

TASK_DIFF = f"""diff --git a/{TASK_DIFF_PATH} b/{TASK_DIFF_PATH}
--- a/{TASK_DIFF_PATH}
+++ b/{TASK_DIFF_PATH}
@@ -1,2 +1,2 @@
 a line that did not move
-the old task line
+the new task line
"""


def _make_job() -> Job:
    return Job(
        name="test-diff-endpoint-job",
        user_prompt="Test prompt for the diff endpoint",
        tasks=[Task(type="write_readme", description="Write a README")],
    )


class TestDiffEndpoint:
    """The job-scope and task-run-scope diff routes, over real HTTP."""

    @pytest.fixture(autouse=True)
    def _setup_job(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        from packages.orchestration.storage import save_job
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

    def _write_evidence(self) -> Path:
        """Build an evidence dir and point the server's resolver at it.

        The index file is the FIRST branch `_resolve_evidence_dir` reads, so
        writing it keeps this test independent of the working directory — the
        fallback branch is a path relative to the CWD.
        """
        evidence = self.tmp_path / "evidence"
        (evidence / "task_runs" / "T001").mkdir(parents=True)
        (evidence / "workspace.diff").write_text(JOB_DIFF, encoding="utf-8")
        (evidence / "task_runs" / "T001" / "safe.diff").write_text(
            TASK_DIFF, encoding="utf-8")

        index_dir = self.tmp_path / "job_evidence_index"
        index_dir.mkdir(parents=True, exist_ok=True)
        (index_dir / f"{self.job_id}.json").write_text(
            json.dumps({"evidence_dir_local": str(evidence)}), encoding="utf-8")
        return evidence

    def _start_server(self):
        """Start the real server in a daemon thread, return (port, token)."""
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()

        for _ in range(50):
            if Path(info_file).exists():
                info = json.loads(Path(info_file).read_text())
                return info["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    @staticmethod
    def _get(port, path):
        conn = HTTPConnection("127.0.0.1", port, timeout=5)
        try:
            conn.request("GET", path)
            resp = conn.getresponse()
            raw = resp.read()
            return resp.status, json.loads(raw)
        finally:
            conn.close()

    def test_job_route_serves_the_workspace_diff(self):
        self._write_evidence()
        port, token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/diff?token={token}")
        assert status == 200, body
        assert body["scope"] == "job", body
        assert body["available"] is True, body
        assert body["source"] == "workspace.diff", body
        assert [f["path"] for f in body["files"]] == [JOB_DIFF_PATH], body

    def test_task_run_route_serves_only_that_runs_diff(self):
        self._write_evidence()
        port, token = self._start_server()
        status, body = self._get(
            port, f"/api/jobs/{self.job_id}/task-runs/T001/diff?token={token}")
        assert status == 200, body
        assert body["scope"] == "task_run", body
        assert body["task_id"] == "T001", body
        assert body["available"] is True, body
        # ONLY the task run's file: the job diff names a different path, so a
        # route that ignored the task id would show up right here.
        assert [f["path"] for f in body["files"]] == [TASK_DIFF_PATH], body

    def test_unknown_task_run_is_a_named_absence_at_status_200(self):
        """An unknown run is DATA, not an HTTP error.

        The status is asserted explicitly because 200-with-a-reason is the
        design decision the route carries: a 404 would make a job with no diff
        indistinguishable from a bad URL, so a later change to 404 must be red.
        """
        self._write_evidence()
        port, token = self._start_server()
        status, body = self._get(
            port, f"/api/jobs/{self.job_id}/task-runs/T404/diff?token={token}")
        assert status == 200, body
        assert body["available"] is False, body
        assert body["reason"] == "unknown_task_run", body
        assert body["task_run_ids"] == ["T001"], body

    def test_job_route_refuses_a_bad_token(self):
        self._write_evidence()
        port, _token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/diff?token=wrong")
        assert status == 403, body
        assert body["error"] == "invalid token", body

    def test_task_run_route_refuses_a_bad_token(self):
        self._write_evidence()
        port, _token = self._start_server()
        status, body = self._get(
            port, f"/api/jobs/{self.job_id}/task-runs/T001/diff?token=wrong")
        assert status == 403, body
        assert body["error"] == "invalid token", body

    def test_job_without_evidence_names_the_absence_at_status_200(self):
        # No `_write_evidence()` call: the index is absent and the CWD-relative
        # fallback directory does not exist for this job's id either.
        port, token = self._start_server()
        status, body = self._get(port, f"/api/jobs/{self.job_id}/diff?token={token}")
        assert status == 200, body
        assert body["available"] is False, body
        assert body["reason"] == "evidence_dir_unavailable", body


# --------------------------------------------------------------------------- #
# F256 T002 — the Acceptance fixture measured END TO END, over the real route.
# --------------------------------------------------------------------------- #

#: The Acceptance fixture's BODY-line count. F037's Acceptance names a "10k-line
#: fixture within the perf budget (recorded)" and F256 T002 is the work that
#: measures it. It must be EVEN: the body below is alternating deletion/addition
#: PAIRS.
DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT = 10_000

#: The LINEAR REFERENCE size, served through the SAME route in the SAME run, so
#: the two medians differ only in the number of body lines. Even for the same
#: reason as the count above.
DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT = 1_000

#: The SCALE RATIO CEILING: the measured `t(10_000) / t(1_000)` must stay under
#: it. Authority: DECISION F256 D4, which measured both the linear and the
#: quadratic case before fixing the number. A ratio taken on one machine in one
#: run divides every constant factor out, so this guard — unlike a second
#: absolute second-count — never becomes a report on machine speed.
DIFF_ENDPOINT_SCALE_RATIO_CEILING = 20

#: The HANG NET, in seconds, over a SINGLE Acceptance-size request. Authority:
#: DECISION F256 D4. Coarse by design and NOT a budget: it catches a pipeline
#: that stopped answering at all, not one that merely got slower.
DIFF_ENDPOINT_HANG_NET_SECONDS = 5.0


def _generated_huge_endpoint_diff(
    body_line_count: int, path: str = "pkg/huge_module.py"
) -> str:
    """One file with `body_line_count` body lines, as alternating `-`/`+` pairs.

    A TWIN of `_generated_huge_single_file_diff` in
    `tests/orchestration/test_diff_parser.py`, and deliberately a copy rather than
    an import: that helper is private to another test package, so importing it
    would let a change made for the parser suite's own reasons move the numbers
    THIS module records, and the two suites measure different things — the parser
    alone there, the whole server path here. Generated rather than typed out for
    the reason that module gives: ten thousand literal body lines show a reader
    nothing the fourth line does not already show.
    """
    pair_count = body_line_count // 2
    lines = [
        f"diff --git a/{path} b/{path}",
        f"--- a/{path}",
        f"+++ b/{path}",
        f"@@ -1,{pair_count} +1,{pair_count} @@",
    ]
    for index in range(pair_count):
        lines.append(f"-old body line {index}")
        lines.append(f"+new body line {index}")
    return "\n".join(lines) + "\n"


class TestDiffEndpointPerfBudget:
    """F256 T002: the 10k-line fixture through the REAL route, timed.

    NOT a direct call to `build_diff_view`. What is under measurement is the route
    and everything behind it — artifact read, parse, envelope assembly, JSON
    serialisation, HTTP — and the parser half of that is already measured by
    `test_the_huge_diff_parses_inside_the_recorded_perf_budget` in
    `tests/orchestration/test_diff_parser.py`. Calling the builder here would
    re-measure that half and leave the composition around it unguarded, which is
    the gap DECISION F256 D4 exists to close.
    """

    #: Requests per size. Enough for a median to be a median rather than one
    #: sample, few enough that the whole class stays about a second of wall clock.
    _SAMPLE_COUNT = 5

    @pytest.fixture(autouse=True)
    def _setup_perf_job(self, tmp_path, monkeypatch):
        """This class's own fixture, not `TestDiffEndpoint._setup_job`.

        The evidence body here is a GENERATED fixture whose size each test
        chooses, so the evidence directory and the resolver index are built once
        here and the diff artifact is written per size by `_serve_body_lines`.
        `_start_perf_server` below reads `tmp_path` and `job_id` off the instance
        exactly as `TestDiffEndpoint._start_server` reads its own, which is why
        that helper cannot be borrowed across the two classes.
        """
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        self.job = _make_job()
        from packages.orchestration.storage import save_job
        save_job(self.job)
        self.job_id = str(self.job.id)
        self.tmp_path = tmp_path

        self.evidence_dir = tmp_path / "evidence"
        self.evidence_dir.mkdir(parents=True)
        index_dir = tmp_path / "job_evidence_index"
        index_dir.mkdir(parents=True, exist_ok=True)
        (index_dir / f"{self.job_id}.json").write_text(
            json.dumps({"evidence_dir_local": str(self.evidence_dir)}),
            encoding="utf-8")

    def _serve_body_lines(self, body_line_count: int) -> None:
        """Put a fixture of exactly `body_line_count` body lines behind the route.

        Rewriting the artifact rather than restarting the server is what lets one
        test measure two sizes in one run: nothing between the route and the file
        caches, so the next request reads what was just written.
        """
        (self.evidence_dir / "workspace.diff").write_text(
            _generated_huge_endpoint_diff(body_line_count), encoding="utf-8")

    def _start_perf_server(self):
        """Start the real server in a daemon thread, return (port, token).

        The same shape as `TestDiffEndpoint._start_server` and as the harness each
        of the other modules under `tests/ui_server/` carries; re-declared here
        because that one is bound to its own class's instance attributes.
        """
        import secrets as _s

        from packages.orchestration.ui_server import start_ui_server

        info_file = str(self.tmp_path / "server_info.json")
        token = _s.token_urlsafe(16)

        def run():
            try:
                start_ui_server(
                    self.job_id,
                    host="127.0.0.1",
                    port=0,
                    token=token,
                    open_browser=False,
                    info_file=info_file,
                )
            except (SystemExit, KeyboardInterrupt):
                pass

        threading.Thread(target=run, daemon=True).start()

        for _ in range(50):
            if Path(info_file).exists():
                info = json.loads(Path(info_file).read_text())
                return info["port"], token
            time.sleep(0.1)
        pytest.fail("Server did not start in time")

    def _timed_diff_requests(self, port, token):
        """`_SAMPLE_COUNT` GETs of this job's diff route; (times, status, body).

        The response is decoded on every request, not only the last, because the
        decode is part of what a client pays: timing a pipeline that stops at the
        socket would time a pipeline no client has.
        """
        path = f"/api/jobs/{self.job_id}/diff?token={token}"
        times: list[float] = []
        status, body = None, None
        for _ in range(self._SAMPLE_COUNT):
            started = time.perf_counter()
            # Reused unchanged from `TestDiffEndpoint`: it is a @staticmethod and
            # carries no instance state, so the two classes share one client.
            status, body = TestDiffEndpoint._get(port, path)
            times.append(time.perf_counter() - started)
        return times, status, body

    @staticmethod
    def _pin_the_served_work(status, body, expected_body_lines):
        """A budget met by serving nothing is not a budget: pin the WORK first."""
        assert status == 200, body
        assert body["available"] is True, body
        assert body["truncated"] is False, body
        assert len(body["files"]) == 1, [entry["path"] for entry in body["files"]]
        served = sum(len(hunk["lines"]) for hunk in body["files"][0]["hunks"])
        assert served == expected_body_lines, (
            f"the route served {served} body lines against a fixture of "
            f"{expected_body_lines}")

    def test_the_acceptance_fixture_is_served_inside_the_hang_net(self):
        """The end-to-end figure F037's Acceptance asks to have RECORDED.

        MEASURED 2026-08-28 on the machine this feature is being built on — a Linux
        x86-64 development workstation, CPython 3, unloaded — as the median of five
        GETs of this job's diff route with a 10,000 body-line `workspace.diff` on
        disk: MEDIAN 0.1331 s, minimum 0.1282 s, maximum 0.1489 s, for a serialised
        JSON response of 1,045,960 bytes. That is the WHOLE server path — artifact
        read, parse, envelope, `json.dumps`, HTTP — against the 0.105 s
        `test_the_huge_diff_parses_inside_the_recorded_perf_budget` records for the
        parser alone, so the parse is most of the cost and everything composed
        around it is the remainder.

        THE ASSERTION IS NOT THAT FIGURE. `DIFF_ENDPOINT_HANG_NET_SECONDS` is a
        coarse net at 5.0 s, ruled by DECISION F256 D4: at nearly forty times the
        measured median it is not a budget and is not described as one — it catches a
        pipeline that stopped answering at all. The property that the pipeline
        stayed LINEAR is guarded by the ratio in the test below, because a second
        absolute second-count here would re-guard the parser's own cost more
        loosely than the parser test already does, and would go red on a slower
        runner, which teaches a future session to raise it.
        """
        # Both counts are pair counts doubled, and the Acceptance fixture must
        # reach the parser WHOLE. The ceiling comparison is asserted DIRECTLY
        # rather than left to `truncated`, so a re-decided ceiling that cut the
        # very fixture Acceptance names says so here instead of quietly turning
        # the recorded number into a measurement of a truncated parse.
        assert DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT % 2 == 0
        assert DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT % 2 == 0
        assert DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT < DIFF_VIEW_MAX_BODY_LINES, (
            f"the Acceptance fixture is {DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT} "
            f"body lines and DIFF_VIEW_MAX_BODY_LINES is "
            f"{DIFF_VIEW_MAX_BODY_LINES}: the fixture would be truncated")

        self._serve_body_lines(DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT)
        port, token = self._start_perf_server()
        times, status, body = self._timed_diff_requests(port, token)
        self._pin_the_served_work(
            status, body, DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT)

        median_seconds = statistics.median(times)
        # `_send_json` writes `json.dumps(data, default=str).encode()`, so this is
        # the response's own byte length rather than an estimate of it.
        response_bytes = len(json.dumps(body, default=str).encode())
        # PRINTED because "recorded" is half of what Acceptance asks for: a run of
        # this class reports the figures its docstrings carry, so re-recording them
        # after a change needs no edit here. pytest captures it, so a green suite
        # run shows nothing; `-s` or `-rP` surfaces it.
        print(
            f"F256 T002 endpoint@{DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT}: "
            f"median {median_seconds:.4f}s min {min(times):.4f}s "
            f"max {max(times):.4f}s bytes {response_bytes}")

        assert median_seconds < DIFF_ENDPOINT_HANG_NET_SECONDS, (
            f"the median of {len(times)} requests at "
            f"{DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT} body lines was "
            f"{median_seconds:.4f}s (min {min(times):.4f}s, max {max(times):.4f}s, "
            f"{response_bytes} response bytes), hang net "
            f"{DIFF_ENDPOINT_HANG_NET_SECONDS}s")

    def test_the_route_stays_linear_in_body_lines(self):
        """The property a recorded second-count cannot carry: the pipeline's SHAPE.

        The same route is measured at 1,000 and at 10,000 body lines, in this test,
        in this run, on this machine, and the assertion is on their RATIO. A
        pipeline linear in body lines answers near 10 — the size ratio itself; a
        pipeline quadratic in body lines answers near 100, that ratio squared.
        Because both medians come off ONE machine in ONE run, every constant factor
        the machine contributes — clock speed, load, interpreter version — divides
        out, so this assertion cannot become a report on machine speed however slow
        the runner is. `DIFF_ENDPOINT_SCALE_RATIO_CEILING` is 20 by DECISION F256
        D4, which measured both directions before fixing it.

        THE FIXED PER-REQUEST OVERHEAD MOVES THE MEASURED RATIO DOWN, and down is
        the safe direction. Server dispatch, socket setup and JSON decoding cost
        the same at both sizes, so they inflate the SMALLER median proportionally
        more than the larger one and the measured ratio lands BELOW the true
        algorithmic one. The error therefore makes this guard more permissive: it
        can miss a mild regression, it cannot manufacture one, which is the only
        direction a bound in a suite that must stay green may err in.

        MEASURED 2026-08-28 on the same machine and in the same run as the test
        above: a median of 0.0269 s at 1,000 body lines against 0.1339 s at 10,000,
        a ratio of 4.97 — below the algorithmic 10 exactly as the paragraph above
        predicts, and 4.0 times inside the ceiling.
        """
        self._serve_body_lines(DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT)
        port, token = self._start_perf_server()
        reference_times, reference_status, reference_body = (
            self._timed_diff_requests(port, token))

        # Same server, same route, same process — only the artifact changes size.
        self._serve_body_lines(DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT)
        acceptance_times, acceptance_status, acceptance_body = (
            self._timed_diff_requests(port, token))

        self._pin_the_served_work(
            reference_status, reference_body,
            DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT)
        self._pin_the_served_work(
            acceptance_status, acceptance_body,
            DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT)

        reference_median = statistics.median(reference_times)
        acceptance_median = statistics.median(acceptance_times)
        measured_ratio = acceptance_median / reference_median
        size_ratio = (DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT
                      / DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT)
        print(
            f"F256 T002 endpoint ratio: "
            f"{reference_median:.4f}s@{DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT} "
            f"{acceptance_median:.4f}s@{DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT} "
            f"ratio {measured_ratio:.2f}")

        assert measured_ratio < DIFF_ENDPOINT_SCALE_RATIO_CEILING, (
            f"{DIFF_ENDPOINT_ACCEPTANCE_BODY_LINE_COUNT} body lines answered in "
            f"{acceptance_median:.4f}s against {reference_median:.4f}s at "
            f"{DIFF_ENDPOINT_LINEAR_REFERENCE_BODY_LINE_COUNT}, a ratio of "
            f"{measured_ratio:.2f} against ceiling "
            f"{DIFF_ENDPOINT_SCALE_RATIO_CEILING} for a size ratio of "
            f"{size_ratio:.0f}")
