"""F036 T003 (DECISION F036 D5) — the browser's tour module reads exactly what `tour_view`
in `packages/orchestration/result_tour.py` answers, the SAME view the command line's `tour`
section shows.

`apps/ui/src/api/resultTour.ts` decodes `GET /api/jobs/<job_id>/tour`. A decoder that read a
key the server never writes would refuse every view, and one that missed a key the server
renamed would show a shorter tour than the job actually offers, so each key the TypeScript
reads is compared with the Python that writes it.
"""
from __future__ import annotations

import re
from pathlib import Path

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
RESULT_TOUR_TS = UI_SRC / "api" / "resultTour.ts"
REMEDY_API_TS = UI_SRC / "api" / "remedyApi.ts"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _reads(pattern: str, text: str) -> set[str]:
    return set(re.findall(pattern, text))


def test_the_payload_keys_are_tour_view_s_own():
    from packages.orchestration.result_tour import TOUR_VIEW_KEYS

    source = _source(RESULT_TOUR_TS)
    assert _reads(r'payload\["([a-z_]+)"\]', source) == set(TOUR_VIEW_KEYS)


def test_the_tour_keys_are_result_tour_py_s_own():
    source = _source(RESULT_TOUR_TS)
    assert _reads(r'tour\["([a-z_]+)"\]', source) == {
        "schema", "job_id", "generator", "stops", "dropped"}


def test_the_stop_keys_are_the_stop_s_own():
    source = _source(RESULT_TOUR_TS)
    assert _reads(r'stop\["([a-z_]+)"\]', source) == {"title", "body", "anchor"}


def test_the_anchor_keys_are_the_anchor_s_own():
    source = _source(RESULT_TOUR_TS)
    assert _reads(r'anchor\["([a-z_]+)"\]', source) == {"kind", "ref"}


def test_the_drop_keys_are_the_dropped_entry_s_own():
    source = _source(RESULT_TOUR_TS)
    assert _reads(r'drop\["([a-z_]+)"\]', source) == {"title", "reason"}


def test_the_anchor_kinds_match_result_tour_py_in_order():
    from packages.orchestration.result_tour import TOUR_ANCHOR_KINDS

    source = _source(RESULT_TOUR_TS)
    [block] = re.findall(r"TOUR_ANCHOR_KINDS = \[(.*?)\] as const", source, re.S)
    kinds = re.findall(r'"([a-z]+)"', block)
    assert tuple(kinds) == TOUR_ANCHOR_KINDS


def test_the_pure_module_opens_no_socket_reads_no_clock_and_keeps_no_storage():
    source = _source(RESULT_TOUR_TS)
    for forbidden in ("fetch(", "Date.now", "new Date", "localStorage"):
        assert forbidden not in source, forbidden


def test_load_tour_view_reads_through_tour_view_path_and_decode_tour_view():
    source = _source(REMEDY_API_TS)
    start = source.index("export async function loadTourView(")
    next_export = source.find("\nexport ", start + 1)
    end = len(source) if next_export == -1 else next_export
    body = source[start:end]
    assert "tourViewPath(request)" in body
    assert "decodeTourView(" in body
