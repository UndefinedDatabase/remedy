"""F020 T002 — the graph legend is generated from the glyph and state modules.

`apps/ui/src/components/graph/GraphLegend.tsx` renders the rows
`renderers/legendModel.ts` enumerates from `glyphPaths.ts` and `nodeStates.ts`,
the sources the canvas paints from, so the legend can never drift from the graph
(T5_F020.md, Goal and Acceptance; assets_spec.md §8 check 9). The vitest
environment reads `.test.ts` files only, so the component is pinned from source
here, as `test_brain_stage_mount.py` pins the stage; the row model itself is
pinned by `legendModel.test.ts`.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH = ROOT / "apps" / "ui" / "src" / "components" / "graph"
LEGEND = GRAPH / "GraphLegend.tsx"
STAGE = GRAPH / "BrainGraphStage.tsx"
GLYPH_PATHS = GRAPH / "renderers" / "glyphPaths.ts"
NODE_STATES = GRAPH / "renderers" / "nodeStates.ts"


def _names(path: Path) -> list[str]:
    names = re.findall(r'^    name: "([^"]+)",$', path.read_text(encoding="utf-8"), flags=re.M)
    assert names, f"{path.name} declares no names"
    return names


def test_the_legend_renders_the_rows_the_model_enumerates():
    src = LEGEND.read_text(encoding="utf-8")
    assert 'from "./renderers/legendModel"' in src
    assert "KIND_ROWS.map(" in src and "STATE_ROWS.map(" in src
    assert "const KIND_ROWS = legendKindRows();" in src
    assert "const STATE_ROWS = legendStateRows();" in src


def test_the_legend_writes_no_kind_or_state_name_of_its_own():
    src = LEGEND.read_text(encoding="utf-8")
    written = [n for n in _names(GLYPH_PATHS) + _names(NODE_STATES) if f'"{n}"' in src or f">{n}<" in src]
    assert not written, f"GraphLegend.tsx writes names the modules own: {written}"


def test_the_legend_draws_no_path_of_its_own():
    src = LEGEND.read_text(encoding="utf-8")
    assert 'd="' not in src, "GraphLegend.tsx draws a path literal; paths come from the row model"
    assert re.findall(r"\bd=\{([^}]+)\}", src), "GraphLegend.tsx draws no path at all"
    for expr in re.findall(r"\bd=\{([^}]+)\}", src):
        assert re.fullmatch(r"(row|m)\.(strokePath|fillPath)( \|\| m\.fillPath)?", expr.strip()), expr


def test_every_inline_colour_in_the_legend_is_a_token():
    src = LEGEND.read_text(encoding="utf-8")
    styles = re.findall(r"style=\{\{([^}]*)\}\}", src)
    assert styles, "GraphLegend.tsx paints no swatch"
    for style in styles:
        values = [v.strip() for v in re.findall(r":\s*([^,]+)", style)]
        assert values and all(v.startswith("tokenVar(") for v in values), style


def test_the_legend_opens_from_the_graph_chrome_and_closes_on_escape():
    src = LEGEND.read_text(encoding="utf-8")
    assert "aria-expanded={open}" in src
    assert 'role="dialog"' in src and 'aria-label="Graph legend"' in src
    assert 'e.key === "Escape"' in src
    stage = STAGE.read_text(encoding="utf-8")
    dock = stage[stage.index("<div className={styles.viewDock}>"):]
    assert dock.index("<GraphLegend />") < dock.index("</div>")
