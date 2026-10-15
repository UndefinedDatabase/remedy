"""amend1015 Part 4.4: which brain-graph nodes each zoom level shows, the default zoom included.

Before this module the default zoom showed exactly one node, the job orb, so a one-task job
opened on an orb with its only task hidden under it. The default zoom now shows the orb and
its task dots, up to ``MAX_INITIAL_NODES_CAP`` nodes; past that, the per-level caps apply as
before. The cap loop moved here unchanged from ``ui_view_model.build_brain_view_model``, which
keeps that function under its structure pin.

Public API::

    MAX_INITIAL_NODES_CAP — the most nodes the default zoom shows
    apply_brain_zoom_caps(raw_nodes, caps) -> int
"""

from __future__ import annotations

from typing import Any

MAX_INITIAL_NODES_CAP = 12


def apply_brain_zoom_caps(raw_nodes: list[dict[str, Any]], caps: list[int]) -> int:
    """Open the default zoom to the job and its first tasks, enforce *caps* per level, and
    return ``max_initial_nodes`` — the task count plus one, capped at MAX_INITIAL_NODES_CAP.

    Tasks are opened in plan order (the order of *raw_nodes*). A level's cap is never below the
    initial count, so a node the default zoom shows is never pushed out of a deeper level.
    """
    tasks = [n for n in raw_nodes if n["type"] == "task"]
    initial = min(len(tasks) + 1, MAX_INITIAL_NODES_CAP)
    for task in tasks[:initial - 1]:
        task["visible_from_zoom"] = 0
    # Sort by importance descending, then push the excess of each level to the next one.
    sorted_by_importance = sorted(raw_nodes, key=lambda n: -n["importance"])
    for level in range(7):
        max_at_level = max(caps[level], initial)
        visible_at_level = [n for n in sorted_by_importance if n["visible_from_zoom"] <= level]
        if len(visible_at_level) > max_at_level:
            for excess in visible_at_level[max_at_level:]:
                if excess["visible_from_zoom"] == level:
                    excess["visible_from_zoom"] = min(level + 1, 6)
    return initial
