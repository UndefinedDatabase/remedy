"""F038 T003, DECISION F038 D12 — the evidence panel's Chat tab, pinned as source.

`EvidenceChatTab.tsx` and `chatTurn.ts` are read as source, exactly as `TourOverlay.tsx` is
pinned by `test_tour_overlay_contract.py` (DECISION F031 D5: no DOM harness exists for a
mounted component in this repository's vitest config). The DOM audit of `ChatTurnBlock` itself
— the one surface `renderToStaticMarkup` can reach — lives in `evidenceChatAudit.test.ts`.
"""
from __future__ import annotations

from pathlib import Path

from packages.orchestration.chat_answer import CHAT_NOT_IN_EVIDENCE
from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
TAB = UI_SRC / "components" / "graph" / "EvidenceChatTab.tsx"
PANEL = UI_SRC / "components" / "graph" / "EvidencePanel.tsx"
CHAT_TURN = UI_SRC / "api" / "chatTurn.ts"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def test_the_panel_mounts_the_tab():
    source = _source(PANEL)
    assert (
        '{tab === "chat" && <EvidenceChatTab jobId={jobId} token={token} '
        'taskId={detail.taskId} onTab={onTab} />}'
    ) in source
    assert 'import { EvidenceChatTab } from "./EvidenceChatTab";' in source


def test_the_tab_holds_no_fetch_and_reads_and_sends_only_through_its_two_doors():
    source = _source(TAB)
    assert "fetch(" not in source
    assert "loadChatTurn(" in source
    assert "sendChatCard(" in source


def test_the_ts_chat_not_in_evidence_equals_the_python_one():
    source = _source(CHAT_TURN)
    assert f'export const CHAT_NOT_IN_EVIDENCE = "{CHAT_NOT_IN_EVIDENCE}";' in source


def test_the_decoder_reads_every_key_of_the_view_and_available_and_reason_by_name():
    source = _source(CHAT_TURN)
    keys = (
        "available", "reason", "kind", "scope", "subject", "question", "generator",
        "sentences", "evidence", "omitted", "text", "citations", "supported", "problem",
        "number", "ref", "verb", "title", "lines", "args", "missing", "confirmable",
    )
    for key in keys:
        assert f'["{key}"]' in source, f"the decoder does not read {key!r} by name"
