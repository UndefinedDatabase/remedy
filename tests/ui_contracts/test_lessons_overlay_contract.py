"""F265 T002 — the learning overlay reads exactly what the server's lessons route serves.

`apps/ui/src/api/lessons.ts` decodes `GET /api/jobs/<job_id>/lessons` (DECISION F265 D2) and
names the run-log event that announces a stored lesson. A decoder that read a key the server
never writes would refuse every index, and one that missed a key the server renamed would show
an empty lesson as a whole one, so each key the TypeScript reads is compared with the Python
that writes it. The components are read as source too, because no DOM harness exists
(DECISION F031 D5): the overlay reaches the route only through `loadLessonsIndex`, drops a stale
answer, closes on Escape, and is mounted outside the main column (DECISION F265 D3).
"""
from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
LESSONS_TS = UI_SRC / "api" / "lessons.ts"
OVERLAY = UI_SRC / "components" / "lessons" / "LessonsOverlay.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _reads(pattern: str) -> set[str]:
    return set(re.findall(pattern, _source(LESSONS_TS)))


def test_the_envelope_keys_are_the_routes():
    from packages.orchestration.ui_server import _build_lessons_json

    served = _build_lessons_json(SimpleNamespace(job_id="0a1b2c3d4e5f6a7b", tasks=[]))
    assert _reads(r'payload\["([a-z_]+)"\]') == set(served)


def test_every_row_key_the_decoder_reads_is_one_the_server_writes():
    from packages.orchestration.lessons import _OVERVIEW_FIELDS, job_lessons_overview

    bare = job_lessons_overview([SimpleNamespace(task_id="T001", title="t", run_id="")],
                                enabled=False)[0]
    written = set(bare) | set(_OVERVIEW_FIELDS)
    read = _reads(r'row\["([a-z_]+)"\]')
    assert {"task_id", "title", "run_id", "status", "reason"} <= read
    assert read <= written


def test_the_construct_keys_are_the_generators():
    from packages.orchestration.lessons import _CONSTRUCT_FIELDS

    assert _reads(r'construct\["([a-z_]+)"\]') == set(_CONSTRUCT_FIELDS)


def test_the_event_and_the_ready_status_are_the_servers():
    from packages.orchestration.event_names import EVENT_NAMES
    from packages.orchestration.lessons import STATUS_READY

    source = _source(LESSONS_TS)
    [event] = re.findall(r'export const LESSON_WRITTEN_EVENT = "([a-z_]+)";', source)
    [ready] = re.findall(r'export const LESSON_STATUS_READY = "([a-z_]+)";', source)
    assert event in EVENT_NAMES
    assert f'event="{event}"' in (REPO_ROOT / "packages/orchestration/pingpong_job.py").read_text(
        encoding="utf-8")
    assert ready == STATUS_READY


def test_the_pure_module_opens_no_socket_reads_no_clock_and_keeps_no_storage():
    source = _source(LESSONS_TS)
    for forbidden in ("fetch(", "XMLHttpRequest", "Date.now", "new Date", "localStorage"):
        assert forbidden not in source, forbidden


def test_the_overlay_reads_only_through_the_door_and_drops_a_stale_answer():
    source = _source(OVERLAY)
    assert "fetch(" not in source and "XMLHttpRequest" not in source
    assert "loadLessonsIndex(" in source
    assert "let cancelled = false;" in source and "if (!cancelled) setRead(" in source
    assert "}, [jobId, serverToken, refreshKey]);" in source


def test_the_overlay_is_a_dialog_that_escape_closes():
    source = _source(OVERLAY)
    assert 'role="dialog"' in source and 'aria-label="Lessons"' in source
    assert 'if (event.key === "Escape") onClose();' in source


def test_the_shell_mounts_the_overlay_outside_the_main_column():
    source = _source(SHELL)
    assert source.index("</main>") < source.index("<LessonsOverlay")
    assert "refreshKey={lessonsKey}" in source
    assert "const lessonsKey = lessonsRefreshKey(stream.recent ?? []);" in source
