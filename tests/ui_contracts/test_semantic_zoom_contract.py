"""F023 T001 — the semantic-zoom machine is pure and its thresholds are the spec's.

`apps/ui/src/components/graph/semanticZoom.ts` is the state machine {level, focusId}
and `zoomWheel.ts` its wheel adapter, where the hysteresis lives (T5_F023 Design,
DECISION F023 D1). graph_spec.md §10 fixes the thresholds in prose and asks for a
renderer-agnostic machine; the vitest environment reads no Markdown, so the binding
between the spec's numbers and the adapter's constants is pinned here, beside the
goldens in `semanticZoom.test.ts` and `zoomWheel.test.ts`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH = ROOT / "apps" / "ui" / "src" / "components" / "graph"
MACHINE = GRAPH / "semanticZoom.ts"
WHEEL = GRAPH / "zoomWheel.ts"
SPEC = ROOT / "docs" / "ui" / "design_reference" / "graph_spec.md"


def _spec_section_10() -> str:
    text = SPEC.read_text(encoding="utf-8")
    start = text.index("## 10. Semantic zoom")
    return text[start:text.index("\n## 11.", start)]


def _constant(src: str, name: str) -> float:
    match = re.search(rf"^export const {name} = ([0-9.]+);$", src, re.MULTILINE)
    assert match, f"zoomWheel.ts declares no `export const {name} = <number>;`"
    return float(match.group(1))


def test_the_wheel_thresholds_are_the_ones_graph_spec_section_10_states():
    spec = re.search(r"in >([0-9.]+) on node, out <([0-9.]+)", _spec_section_10())
    assert spec, "graph_spec.md §10 no longer states `in >N on node, out <M`"
    src = WHEEL.read_text(encoding="utf-8")
    assert _constant(src, "ZOOM_IN_ABOVE") == float(spec.group(1))
    assert _constant(src, "ZOOM_OUT_BELOW") == float(spec.group(2))


def test_the_crossing_is_strict_on_both_sides():
    src = WHEEL.read_text(encoding="utf-8")
    assert "previous <= ZOOM_IN_ABOVE && next > ZOOM_IN_ABOVE" in src
    assert "previous >= ZOOM_OUT_BELOW && next < ZOOM_OUT_BELOW" in src


def test_the_machine_and_its_adapter_are_renderer_agnostic():
    for path in (MACHINE, WHEEL):
        src = path.read_text(encoding="utf-8")
        imports = re.findall(r'^import [^;]*from "([^"]+)";$', src, re.MULTILINE)
        assert all(spec.startswith("./") for spec in imports), f"{path.name} imports {imports}"
        for word in ("window.", "document.", "useState", "useReducer", "Path2D", "ForceGraph"):
            assert word not in src, f"{path.name} reaches for {word}"


def test_the_levels_are_the_four_graph_spec_names():
    section = _spec_section_10()
    for label in ("**L0 organism**", "**L1 task focus**", "**L2 run detail**", "**L3 evidence**"):
        assert label in section
    src = MACHINE.read_text(encoding="utf-8")
    assert "export type ZoomLevel = 0 | 1 | 2 | 3;" in src
