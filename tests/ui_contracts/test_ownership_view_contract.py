"""F035 T003 (DECISION F035 D5) — the task detail's "Who did what" section reads exactly what
the server's ownership route serves.

`apps/ui/src/api/ownership.ts` decodes `GET /api/jobs/<job_id>/ownership` (the same view
`ownership_view` in `packages/orchestration/ownership_phrases.py` answers) and names the
run-log events that make the view worth reading again. A decoder that read a key the server
never writes would refuse every view, and one that missed a key the server renamed would show a
whole action as though it never happened, so each key the TypeScript reads is compared with the
Python that writes it. `DetailPopover.tsx` and `RemedyShell.tsx` are read as source too: the
section reaches the route only through `loadOwnershipView`, the shell's effect carries the
`cancelled` guard and the refresh key, and the popover shows the one honest line for a view it
cannot read rather than the server's own words.
"""
from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

from tests.ui_contracts.test_brain_stream_ring import strip_ts_comments

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
UI_SRC = REPO_ROOT / "apps" / "ui" / "src"
OWNERSHIP_TS = UI_SRC / "api" / "ownership.ts"
POPOVER = UI_SRC / "components" / "detail" / "DetailPopover.tsx"
SHELL = UI_SRC / "components" / "shell" / "RemedyShell.tsx"
EVIDENCE_PANEL = UI_SRC / "components" / "graph" / "EvidencePanel.tsx"
PHRASES_PY = REPO_ROOT / "packages" / "orchestration" / "ownership_phrases.py"


def _source(path: Path) -> str:
    return strip_ts_comments(path.read_text(encoding="utf-8"))


def _reads(pattern: str, text: str) -> set[str]:
    return set(re.findall(pattern, text))


def test_the_view_keys_are_ownership_view_s_own(monkeypatch):
    from packages.orchestration.ownership import OwnershipError
    from packages.orchestration.ownership_phrases import ownership_view

    def _raise(_job):
        raise OwnershipError("boom")

    monkeypatch.setattr("packages.orchestration.ownership.build_ownership_ledger", _raise)
    served = ownership_view(SimpleNamespace(job_id="job-1", tasks=[]))

    source = _source(OWNERSHIP_TS)
    assert _reads(r'payload\["([a-z_]+)"\]', source) == set(served)


def test_the_entry_keys_are_ownership_view_s_own_minus_detail_plus_sentence():
    from packages.orchestration.ownership import _ENTRY_KEYS

    expected = (set(_ENTRY_KEYS) - {"detail"}) | {"sentence"}
    source = _source(OWNERSHIP_TS)
    assert _reads(r'entry\["([a-z_]+)"\]', source) == expected


def test_the_actor_keys_are_ownership_actor_s_own():
    from packages.orchestration.ownership import ownership_actor

    served = ownership_actor("alice")
    source = _source(OWNERSHIP_TS)
    assert _reads(r'actor\["([a-z_]+)"\]', source) == set(served)


def test_the_consequence_keys_are__consequence_keys():
    from packages.orchestration.ownership import _CONSEQUENCE_KEYS

    source = _source(OWNERSHIP_TS)
    assert _reads(r'consequence\["([a-z_]+)"\]', source) == set(_CONSEQUENCE_KEYS)


def test_the_pure_module_opens_no_socket_reads_no_clock_and_keeps_no_storage():
    source = _source(OWNERSHIP_TS)
    for forbidden in ("fetch(", "Date.now", "new Date", "localStorage"):
        assert forbidden not in source, forbidden


def test_every_refresh_event_is_a_real_event_name():
    from packages.orchestration.event_names import EVENT_NAMES

    source = _source(OWNERSHIP_TS)
    [block] = re.findall(r"OWNERSHIP_REFRESH_EVENTS = \[(.*?)\] as const", source, re.S)
    names = set(re.findall(r'"([a-z_]+)"', block))
    assert len(names) == 13
    assert names <= EVENT_NAMES


def test_the_chip_words_key_every_catalog_action():
    source_py = PHRASES_PY.read_text(encoding="utf-8")
    actions = set(re.findall(r'action == "([a-z_]+)"', source_py))

    source_ts = _source(OWNERSHIP_TS)
    [block] = re.findall(
        r"OWNERSHIP_CHIP_WORDS: Record<string, string> = \{(.*?)\n\};", source_ts, re.S)
    keys = set(re.findall(r"\n\s*([a-z_]+):", block))
    assert keys == actions


def test_the_popover_places_the_section_after_unreachable_and_never_shows_the_raw_error():
    source = _source(POPOVER)
    assert source.index('data-ui="unreachable-section"') < source.index('data-ui="ownership-section"')
    assert "OWNERSHIP_UNREADABLE_LINE" in source
    assert "{ownership.error}" not in source


def test_the_shell_s_effect_carries_the_guard_and_the_refresh_key():
    source = _source(SHELL)
    assert "const ownershipKey = ownershipRefreshKey(stream.recent ?? []);" in source
    assert "let cancelled = false;" in source
    assert "if (!cancelled) setOwnership(loaded);" in source
    assert "}, [dashboard.jobId, serverToken, ownershipKey, focusedTaskId]);" in source


def test_the_evidence_panel_s_ownership_tab_never_renders_the_raw_error_and_carries_the_cancelled_guard():
    """DECISION F035 D6 — the tab reads its state through `ownershipPanelState`, never `.error`
    directly, so the unreadable line is always the fixed one and the server's own words never
    reach the page; its effect carries the same `cancelled` guard the diff tab beside it does."""
    source = _source(EVIDENCE_PANEL)
    tab_source = source[source.index("function OwnershipTab"):source.index("export function EvidencePanel")]
    assert "let cancelled = false;" in tab_source
    assert "if (!cancelled) setLoaded({ view });" in tab_source
    assert "ownershipPanelState(" in tab_source
    assert ".error" not in tab_source
