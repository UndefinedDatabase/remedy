"""The cockpit's routes below one project, ``/api/projects/<selector>/...`` (DECISION F305 D2).

Step (1) of ``_RemedyHandler.do_GET``'s boundary on ``docs/system/structure-ledger-v1.md``: the
handler hands every path below a project to :func:`project_route_answer`, so a project's routes
grow here and never in the handler. READS ONLY, through ``project_cockpit``; owns no storage.

The routes::

    /api/projects/<selector>/summary — the project's card (DECISION F042 D1)
    /api/projects/<selector>/missions — its missions as cards (DECISION F305 D2)
    /api/projects/<selector>/missions/<mission id>/orders — one mission's orders and chains

Public API::

    project_route_answer(parts) -> (status, body)
"""

from __future__ import annotations

from typing import Any


def _build_project_summary_json(selector: str) -> tuple[int, dict[str, Any]]:
    """Build one project's summary card, or 404 for an unknown selector
    (F042 T001, DECISION F042 D1)."""
    from packages.orchestration.project_cockpit import find_project, project_summary
    project = find_project(selector)
    if project is None:
        return (404, {"error": "project not found"})
    return (200, project_summary(project))


# One door for every path below a project, so the handler's size never follows their number.
def project_route_answer(parts: list[str]) -> tuple[int, dict[str, Any]]:
    """The answer to a path split on ``/`` that reads ``""``, ``api``, ``projects``, a selector and
    more: the project's summary card, its missions, or one mission's orders; 404 ``project not
    found`` for a selector that names no project, and the handler's own 404 for a route that does
    not exist."""
    if len(parts) == 5 and parts[4] == "summary":
        return _build_project_summary_json(parts[3])
    missions = len(parts) == 5 and parts[4] == "missions"
    orders = len(parts) == 7 and parts[4] == "missions" and parts[6] == "orders"
    if not (missions or orders):
        return (404, {"error": "not found"})
    from packages.orchestration.mission_cockpit import mission_orders_view, project_missions_view
    from packages.orchestration.project_cockpit import find_project
    project = find_project(parts[3])
    if project is None:
        return (404, {"error": "project not found"})
    if missions:
        return (200, project_missions_view(project))
    return mission_orders_view(project, parts[5])
