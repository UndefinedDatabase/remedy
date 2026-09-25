"""F024 T001 — the phase mapping table maps measured writers onto the bar's own stops.

`apps/ui/src/components/timeline/phaseMapping.ts` is the timeline's pure reading of the
event ledger (T5_F024.md T001, DECISION F024 D1). Its two tables are contracts: every
kind they name must be an event some code path really writes, which
`packages/orchestration/event_names.py` declares and `tests/orchestration/test_event_names.py`
measures, and the six phases must be the ones the bar and the dashboard already speak.
The vitest goldens in `phaseMapping.test.ts` cannot read Python, so this guard holds the
binding.
"""
from __future__ import annotations

import re
from pathlib import Path

from packages.orchestration.event_names import EVENT_NAMES

ROOT = Path(__file__).resolve().parent.parent.parent
TIMELINE = ROOT / "apps" / "ui" / "src" / "components" / "timeline"
MAPPING = TIMELINE / "phaseMapping.ts"
BAR = TIMELINE / "PhaseTimeline.tsx"
UI_SERVER = ROOT / "packages" / "orchestration" / "ui_server.py"


def _table(src: str, name: str) -> dict[str, str]:
    match = re.search(rf"^export const {name}: [^=]+= \{{\n(.*?)^\}};$", src, re.MULTILINE | re.DOTALL)
    assert match, f"phaseMapping.ts declares no `export const {name}` table"
    entries = re.findall(r'^  ([a-z_.]+): "([a-z]+)",$', match.group(1), re.MULTILINE)
    assert len(entries) == len(match.group(1).strip().splitlines()), f"{name} has a line of another shape"
    return dict(entries)


def _phases(src: str, name: str) -> list[str]:
    match = re.search(rf"{name}[^=]*= \[(.*?)\];", src, re.DOTALL)
    assert match, f"no `{name}` list"
    return re.findall(r'"([a-z]+)"', match.group(1))


def test_every_kind_either_table_names_is_a_measured_writer():
    src = MAPPING.read_text(encoding="utf-8")
    for name in ("PHASE_MARKER_TABLE", "SUB_GLYPH_TABLE"):
        unwritten = sorted(set(_table(src, name)) - EVENT_NAMES)
        assert not unwritten, f"{name} names kinds nothing writes: {unwritten}"


def test_job_and_finalized_are_derived_and_never_marked_by_a_kind():
    src = MAPPING.read_text(encoding="utf-8")
    values = set(_table(src, "PHASE_MARKER_TABLE").values())
    assert values == {"planning", "build", "test", "review"}
    assert set(_table(src, "SUB_GLYPH_TABLE").values()) <= {"decision", "failure", "heal", "stop"}


def test_the_six_phases_are_the_bar_s_and_the_dashboard_s_in_order():
    mapping = _phases(MAPPING.read_text(encoding="utf-8"), "export const TIMELINE_PHASES")
    assert mapping == ["job", "planning", "build", "test", "review", "finalized"]
    assert _phases(BAR.read_text(encoding="utf-8"), "const CANONICAL_PHASES") == mapping
    server = UI_SERVER.read_text(encoding="utf-8")
    block = server[server.index("    phases = [\n"):]
    block = block[:block.index("\n    ]\n")]
    assert re.findall(r'\{"id": "([a-z]+)"', block) == mapping


def test_the_mapping_is_pure_and_reuses_the_reducer_and_the_catalog():
    # Comments are stripped first: the file's own WHY comment names what it avoids
    # (finding R-0584's quoted-token trap).
    src = re.sub(r"//[^\n]*|/\*.*?\*/", "", MAPPING.read_text(encoding="utf-8"), flags=re.DOTALL)
    imports = re.findall(r'^import [^;]*from "([^"]+)";$', src, re.MULTILINE)
    assert sorted(set(imports)) == ["../../api/humanize", "../graph/brainOntology", "../graph/brainReducer"]
    for word in ("window.", "document.", "Date", "Math.random", "useState", "useEffect", "fetch("):
        assert word not in src, f"phaseMapping.ts reaches for {word}"
