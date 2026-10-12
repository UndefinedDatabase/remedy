"""The cockpit's routes below one project, ``/api/projects/<selector>/...`` (DECISION F305 D2).

Step (1) of ``_RemedyHandler.do_GET``'s boundary on ``docs/system/structure-ledger-v1.md``: the
handler hands every path below a project to :func:`project_route_answer`, so a project's routes
grow here and never in the handler. READS ONLY, through ``project_cockpit``; owns no storage.

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
    more: the project's summary card, else the handler's own 404 for a route that does not exist."""
    if len(parts) == 5 and parts[4] == "summary":
        return _build_project_summary_json(parts[3])
    return (404, {"error": "not found"})
