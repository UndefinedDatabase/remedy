"""Guard: the client's per-round facts door agrees with the route and envelope the server has.

`apps/ui/src/api/taskRunRounds.ts` builds the path and decodes the envelope that
`packages/orchestration/run_rounds_view.py` builds and `ui_server.py` serves (DECISION F023
D3). vitest proves the decoder against a hand-written envelope and cannot see the server, so
the agreement that spans both languages is checked here: the path the client BUILDS is one
the server ROUTES, and every key the server's envelope really carries is a key the decoder
reads. The client is read AS TEXT with its comments stripped, as
`test_diff_envelope_door.py` reads its door, so a comment naming a key cannot satisfy it.
"""
from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from packages.orchestration.run_rounds_view import build_task_run_rounds
from tests.ui_contracts.test_diff_envelope_door import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOOR = REPO_ROOT / "apps" / "ui" / "src" / "api" / "taskRunRounds.ts"
API = REPO_ROOT / "apps" / "ui" / "src" / "api" / "remedyApi.ts"
SERVER = REPO_ROOT / "packages" / "orchestration" / "ui_server.py"

# A report with every field present, so the envelope built from it carries every key.
_FULL_REPORT = {
    "retries_used": 0,
    "rounds": [{
        "round": 1, "kind": "initial", "started_at": "2026-09-25T10:00:00+00:00",
        "finished_at": "2026-09-25T10:00:01+00:00", "test_passed": True,
        "builder": {"duration_ms": 1, "tokens_used": 1},
        "reviewer": {"verdict": "pass", "duration_ms": 1, "parse_retried": False},
    }],
}


def _envelope() -> dict:
    job = SimpleNamespace(job_id="j", tasks=[SimpleNamespace(task_id="T001", run_id="0123456789abcdef")])
    return build_task_run_rounds(job, "T001", read_report=lambda _run: (_FULL_REPORT, None))


def test_the_client_path_is_the_route_the_server_dispatches():
    door = strip_ts_comments(DOOR.read_text(encoding="utf-8"))
    assert "`${base}/api/jobs/${job}/task-runs/${task}/rounds?token=${encodeURIComponent(request.token)}`" in door
    server = SERVER.read_text(encoding="utf-8")
    route = server[server.index('parts[6] == "rounds"') - 200:server.index('parts[6] == "rounds"')]
    assert 'parts[4] == "task-runs"' in route and "len(parts) == 7" in route


def test_the_decoder_reads_every_key_the_server_envelope_carries():
    door = strip_ts_comments(DOOR.read_text(encoding="utf-8"))
    env = _envelope()
    assert env["available"] is True
    for key in env:
        if key == "job_id":
            continue  # the client already knows its job; nothing renders it
        assert f"env.{key}" in door, f"the decoder never reads the envelope's `{key}`"
    round_ = env["rounds"][0]
    for key in round_:
        assert f"r.{key}" in door, f"the decoder never reads a round's `{key}`"
    for part in ("builder", "reviewer"):
        for key in round_[part]:
            assert f"{part}.{key}" in door, f"the decoder never reads `{part}.{key}`"


def test_the_door_fetches_the_path_and_decodes_what_arrives():
    api = strip_ts_comments(API.read_text(encoding="utf-8"))
    body = api[api.index("export async function loadTaskRunRounds("):]
    body = body[:body.index("\n}\n")]
    assert "decodeTaskRunRounds(await fetchPayload(taskRunRoundsPath(request)), request.taskId)" in body
    assert "catch {" in body and "decodeTaskRunRounds(null, request.taskId)" in body
