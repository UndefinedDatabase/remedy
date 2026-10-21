"""F313 T003 — record the answers the universe's kit tests the Orb against (DECISION F313 D2).

`python3 scripts/record_client_answers.py` seeds a scratch data root of its own with two running
Pi jobs, serves a stub of the local model server on a free local port for the time of the
recording, runs the real client commands, `remedy client now --json` and its siblings, as child
processes with no model, and writes each one's standard output byte for byte to
`docs/system/client-answers-v1/<case>.json`.
Nothing of this machine's own data or configuration is read: the children see only the scratch
data root, a scratch home folder and the stub's address.

`python3 scripts/record_client_answers.py --check` records the cases again and compares them with
the folder: the same keys at every level and the same values, except at the keys of
`ANSWER_KEYS_READ_BY_TYPE`, whose values come from the clock or from the stub's port and are
compared by their JSON type alone. It exits 0 when every case matches and 1 naming every differing
path, so a change of any recorded answer fails until the folder is recorded again.

Remedy deliberately writes no file of another repository: the universe's kit copies this folder.
"""
from __future__ import annotations

import argparse
import http.server
import json
import os
import site
import subprocess
import sys
import tempfile
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

#: Where the recorded answers live, one `<case>.json` per case (DECISION F313 D2).
CLIENT_ANSWERS_DIR = REPO_ROOT / "docs" / "system" / "client-answers-v1"
#: The running job whose worker wrote five seconds ago, and the one silent for ten minutes.
WORKING_JOB_ID = "f313000000000001"
SILENT_JOB_ID = "f313000000000002"
#: The project both jobs belong to.
KIT_PROJECT_ID = "p-kit"
#: The one model the stub of the local model server reports, installed and loaded.
STUB_MODEL = "qwen3:8b"
#: Each case: its name, the `remedy` arguments, and whether the two jobs are seeded before it.
RECORDED_CASES: tuple[tuple[str, tuple[str, ...], bool], ...] = (
    ("client-now-idle", ("client", "now", "--json"), False),
    ("client-now-running", ("client", "now", "--json"), True),
    ("client-insight-working", ("client", "insight", WORKING_JOB_ID, "--json", "--lines", "40"), True),
    ("client-insight-silent", ("client", "insight", SILENT_JOB_ID, "--json", "--lines", "40"), True),
    ("client-story-working", ("client", "story", WORKING_JOB_ID, "--json"), True),
)
#: The keys whose values come from the clock or from the stub's port; `--check` compares their type.
ANSWER_KEYS_READ_BY_TYPE = frozenset({
    "age_seconds", "at", "created_at", "duration_s", "ended_at", "host", "last_output_s", "minutes",
    "started_at", "updated_at",
})
_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
_CHILD_TIMEOUT_S = 120


class _StubModelServer(http.server.BaseHTTPRequestHandler):
    """Answers the two reads the insight makes of the local model server, and nothing else."""

    def do_GET(self) -> None:
        if self.path == "/api/tags":
            body: dict[str, Any] = {"models": [{"name": STUB_MODEL}]}
        elif self.path == "/api/ps":
            body = {"models": [{"name": STUB_MODEL}]}
        else:
            self.send_error(404)
            return
        data = json.dumps(body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, *args: Any) -> None:
        """Silent: the recording's output is the answers alone."""


def _moment(now: datetime, seconds_ago: int) -> str:
    return (now - timedelta(seconds=seconds_ago)).strftime(_TIME_FORMAT)


def _seed_running_jobs(now: datetime) -> None:
    """The two running Pi jobs of `KIT_PROJECT_ID`, each with its worker pulse, on the data root
    `REMEDY_DATA_DIR` names."""
    from packages.common.secure_fs import durable_write_json
    from packages.core.models import RunState
    from packages.orchestration import data_paths
    from packages.orchestration.execution_config import ExecutionConfig
    from packages.orchestration.pingpong_job import TASK_RUNNING, JobPlan, TaskEntry, save_job_plan
    from packages.orchestration.worker_pulse import WORKER_PULSE_VERSION

    seeds = (
        (WORKING_JOB_ID, "Make the showcase page responsive", "style.css", 5, [
            {"at": _moment(now, 30), "role": "builder", "kind": "model_text",
             "text": "I will add one media query for narrow screens."},
            {"at": _moment(now, 20), "role": "builder", "kind": "tool_call", "tool": "edit",
             "text": "{\"path\":\"style.css\"}"},
            {"at": _moment(now, 5), "role": "builder", "kind": "tool_result", "tool": "edit", "length": 512},
        ]),
        (SILENT_JOB_ID, "Add a contact form", "contact.html", 600, [
            {"at": _moment(now, 640), "role": "builder", "kind": "model_text",
             "text": "I will write the form first."},
            {"at": _moment(now, 600), "role": "builder", "kind": "tool_call", "tool": "write",
             "text": "{\"path\":\"contact.html\"}"},
        ]),
    )
    for created_s, (job_id, title, task_title, silent_s, stream) in zip((900, 840), seeds):
        job = JobPlan(job_id=job_id, job_title=title, project_id=KIT_PROJECT_ID, state=RunState.RUNNING,
                      tasks=[TaskEntry(task_id="T001", title=task_title, status=TASK_RUNNING)],
                      execution_config=ExecutionConfig(builder="pi", reviewer="pi", builder_model=STUB_MODEL,
                                                       reviewer_model=STUB_MODEL))
        # Fixed creation times keep `now`'s newest-first order the same in every recording.
        job.created_at = (now - timedelta(seconds=created_s)).isoformat()
        job.first_running_at = (now - timedelta(seconds=720)).isoformat()
        job.budget_actuals = {
            "schema_version": "2.0.0", "started_at": job.first_running_at, "provider_call_count": 4,
            "actual_call_count": 4, "unmeasured_call_count": 0, "total_tokens": 48_211,
            "actual_sources": ["pingpong_live"], "measured_cost_usd": None, "priced_call_count": 0,
            "unpriced_call_count": 4}
        save_job_plan(job)
        path = data_paths.worker_pulse_path(job_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        durable_write_json(path, {
            "version": WORKER_PULSE_VERSION, "job_id": job_id, "bound_at": _moment(now, 720),
            "role": "builder", "provider": "pi", "model": STUB_MODEL, "round": 1, "call_kind": "attempt",
            "call_started_at": _moment(now, silent_s + 40), "call_ended_at": None,
            "last_output_at": _moment(now, silent_s), "stream": stream,
        })


def record_client_answers() -> dict[str, str]:
    """Every case of `RECORDED_CASES` as the real command printed it, by case name."""
    answers: dict[str, str] = {}
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _StubModelServer)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with tempfile.TemporaryDirectory(prefix="rca-") as scratch_name:
            scratch = Path(scratch_name)
            data_root, home = scratch / "data", scratch / "home"
            data_root.mkdir()
            home.mkdir()
            # A scratch HOME hides the operator's configuration; PYTHONUSERBASE keeps the packages
            # installed for this user, which Python otherwise looks for under HOME.
            env = {"PATH": os.environ.get("PATH", ""), "HOME": str(home), "LANG": "C.UTF-8",
                   "PYTHONUSERBASE": site.getuserbase(), "PYTHONPATH": str(REPO_ROOT),
                   "REMEDY_DATA_DIR": str(data_root),
                   "REMEDY_OLLAMA_HOST": f"http://127.0.0.1:{server.server_address[1]}"}
            seeded = False
            for name, args, needs_jobs in RECORDED_CASES:
                if needs_jobs and not seeded:
                    previous = os.environ.get("REMEDY_DATA_DIR")
                    os.environ["REMEDY_DATA_DIR"] = str(data_root)
                    try:
                        _seed_running_jobs(datetime.now(timezone.utc))
                    finally:
                        if previous is None:
                            os.environ.pop("REMEDY_DATA_DIR", None)
                        else:
                            os.environ["REMEDY_DATA_DIR"] = previous
                    seeded = True
                result = subprocess.run([sys.executable, "-m", "apps.cli.main", *args], cwd=str(scratch),
                                        env=env, capture_output=True, text=True, timeout=_CHILD_TIMEOUT_S)
                if result.returncode != 0:
                    raise SystemExit(f"{name}: `remedy {' '.join(args)}` exited {result.returncode}: "
                                     f"{result.stdout[-400:]}{result.stderr[-400:]}")
                if scratch_name in result.stdout:
                    raise SystemExit(f"{name}: the answer names the scratch folder; nothing is written")
                answers[name] = result.stdout
    finally:
        server.shutdown()
        server.server_close()
    return answers


def _differences(recorded: Any, fresh: Any, path: str, key: str = "") -> list[str]:
    """The paths at which FRESH differs from RECORDED, by value or, under a key read by type, by type."""
    if key in ANSWER_KEYS_READ_BY_TYPE:
        return [] if type(recorded) is type(fresh) else [f"{path}: type {type(recorded).__name__} "
                                                          f"became {type(fresh).__name__}"]
    if isinstance(recorded, dict) and isinstance(fresh, dict):
        found = [f"{path}.{k}: missing" for k in sorted(set(recorded) - set(fresh))]
        found += [f"{path}.{k}: new" for k in sorted(set(fresh) - set(recorded))]
        for k in sorted(set(recorded) & set(fresh)):
            found += _differences(recorded[k], fresh[k], f"{path}.{k}", k)
        return found
    if isinstance(recorded, list) and isinstance(fresh, list):
        if len(recorded) != len(fresh):
            return [f"{path}: {len(recorded)} items became {len(fresh)}"]
        found = []
        for index, (a, b) in enumerate(zip(recorded, fresh)):
            found += _differences(a, b, f"{path}[{index}]", key)
        return found
    return [] if recorded == fresh else [f"{path}: {recorded!r} became {fresh!r}"]


def check_client_answers() -> list[str]:
    """Every difference between the folder and a fresh recording; empty when they match."""
    fresh = record_client_answers()
    found: list[str] = []
    expected = {f"{name}.json" for name, _args, _jobs in RECORDED_CASES}
    present = {p.name for p in CLIENT_ANSWERS_DIR.glob("*.json")} if CLIENT_ANSWERS_DIR.is_dir() else set()
    found += [f"{name}: not recorded" for name in sorted(expected - present)]
    found += [f"{name}: no such case" for name in sorted(present - expected)]
    for name, text in fresh.items():
        target = CLIENT_ANSWERS_DIR / f"{name}.json"
        if target.is_file():
            found += _differences(json.loads(target.read_text(encoding="utf-8")), json.loads(text), name)
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record the answers the universe's kit tests against.")
    parser.add_argument("--check", action="store_true",
                        help="record again and compare with the folder; write nothing")
    args = parser.parse_args(argv)
    if args.check:
        found = check_client_answers()
        for line in found:
            print(line)
        print("client answers: match" if not found else f"client answers: {len(found)} difference(s)")
        return 0 if not found else 1
    from packages.common.secure_fs import durable_write

    CLIENT_ANSWERS_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in record_client_answers().items():
        durable_write(CLIENT_ANSWERS_DIR / f"{name}.json", text.encode("utf-8"), mode=0o644)
        print(f"recorded {name}.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
