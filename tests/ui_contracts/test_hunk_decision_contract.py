"""F292 T003 — the hunk controls read exactly what the recorded-decision routes serve, and send
exactly the command the door records (DECISION F292 D6).

`readHunkDecisions` in `apps/ui/src/api/hunkDecisions.ts` decodes the answer of
`_hunk_decisions_for_view` in `packages/orchestration/ui_server.py`; a decoder that read a key
the server never writes would start every hunk from pending and the next send would erase the
record. So each key the TypeScript reads is compared with the Python that writes it, the states
with the ledger's, the command id with the door's, and the route names with the server's. The
three modules are pure and are read as source for that too.
"""
from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
API = REPO_ROOT / "apps" / "ui" / "src" / "api"
DECISIONS_TS = API / "hunkDecisions.ts"
VIEW_TS = API / "hunkDecisionView.ts"
SEND_TS = API / "hunkDecisionSend.ts"
UI_SERVER = REPO_ROOT / "packages" / "orchestration" / "ui_server.py"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _served() -> dict:
    from packages.orchestration.hunk_decision_record import HUNK_DECISIONS_METADATA_KEY
    from packages.orchestration.ui_server import _hunk_decisions_for_view

    job = SimpleNamespace(metadata={HUNK_DECISIONS_METADATA_KEY: {"job:workspace.diff": {
        "task_id": "job", "attempt": "workspace.diff", "decided_at": "2026-10-01T09:00:00+00:00",
        "hunks": [{"id": "h1", "state": "rejected", "reason": "r", "landing": "unattempted"}]}}})
    served = _hunk_decisions_for_view(job, {"task_id": None, "source": "workspace.diff"})
    assert served["hunks"], served
    return served


def test_the_envelope_keys_the_decoder_reads_are_the_servers():
    assert set(re.findall(r'payload\["([a-z_]+)"\]', _source(DECISIONS_TS))) == set(_served())


def test_the_row_keys_the_decoder_reads_are_the_servers():
    assert set(re.findall(r'entry\["([a-z_]+)"\]', _source(DECISIONS_TS))) == set(_served()["hunks"][0])


def test_the_states_are_the_ledgers():
    from packages.orchestration.hunk_ledger import HUNK_STATE_APPROVED, HUNK_STATE_PENDING, HUNK_STATE_REJECTED

    [states] = re.findall(r"export const HUNK_STATES = \[([^\]]*)\] as const;", _source(DECISIONS_TS))
    assert re.findall(r'"([a-z]+)"', states) == [HUNK_STATE_APPROVED, HUNK_STATE_REJECTED, HUNK_STATE_PENDING]


def test_the_command_is_the_doors_exposed_hunk_command():
    from apps.cli.command_catalog import UI_EXPOSED_COMMANDS
    from packages.orchestration.ui_server import HUNK_APPROVE_COMMAND_ID

    [command] = re.findall(r'export const HUNK_DECISION_COMMAND_ID = "([a-z.-]+)";', _source(SEND_TS))
    assert command == HUNK_APPROVE_COMMAND_ID
    assert command in UI_EXPOSED_COMMANDS


def test_the_counts_the_send_reads_are_the_doors_accepted_body():
    dispatch = UI_SERVER.read_text(encoding="utf-8")
    body = dispatch[dispatch.index("    def _dispatch_approve_hunks("):]
    body = body[:body.index("\n    def ", 1)]
    read = re.findall(r'count\(body, "([a-z]+)"\)', _source(SEND_TS))
    assert read == ["approved", "rejected", "pending"]
    for key in read:
        assert f'"{key}":' in body, key


def test_the_route_names_are_the_servers():
    server = UI_SERVER.read_text(encoding="utf-8")
    assert '"hunk-decisions": _build_hunk_decisions_json,' in server
    assert 'parts[4] == "task-runs" and parts[6] == "hunk-decisions"' in server
    path = _source(DECISIONS_TS)
    assert "/hunk-decisions${query}" in path and "/task-runs/${encodeURIComponent(taskId)}/hunk-decisions" in path


def test_the_three_modules_open_no_socket_read_no_clock_and_keep_no_storage():
    for module in (DECISIONS_TS, VIEW_TS):
        for forbidden in ("fetch(", "XMLHttpRequest", "Date.now", "new Date", "localStorage"):
            assert forbidden not in _source(module), (module.name, forbidden)
    send = _source(SEND_TS)
    for forbidden in ("fetch(", "XMLHttpRequest", "localStorage"):
        assert forbidden not in send, forbidden
