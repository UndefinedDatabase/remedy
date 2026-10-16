"""What a client token may read: the projects its policy lists and nothing else (amend1015c D2).

DECISION F253 D16 gave a client token its projects and held its writes to them (D17); the story
and the logs followed (amendment amend1014-luna-mission-fixes B.3, DECISION amend1015f D14). The
check of operator order amend1015-final-closure found the other read routes still answered a
client about every project: the digest and what changed listed every job with its title and its
repository, and the proof, the run poll and the order poll answered for a job or an order of
another project. This module names the projects a client may read and refuses an order of
another project; `packages/orchestration/public_api.py` applies it, and the server's own token
still reads everything.

Public API::

    client_project_ids(client) -> frozenset[str]
    client_order_read_refusal(client, order) -> str | None
"""

from __future__ import annotations

from typing import Any


def client_project_ids(client: Any) -> frozenset[str]:
    """The ids of the registered projects CLIENT lists, by slug or by id; a job or a mission is
    the client's when its `project_id` is one of them. A listed name no project answers to adds
    nothing, so a client of no registered project reads no job."""
    from packages.orchestration.api_clients import client_lists_project
    from packages.orchestration.project_registry import _list_projects_readonly

    return frozenset(str(project.id) for project in _list_projects_readonly()
                     if client_lists_project(client, (project.slug or "", str(project.id))))


def client_order_read_refusal(client: Any, order: str) -> str | None:
    """One sentence when CLIENT may not read the order ORDER, whose order file names a project the
    client does not list or cannot be read, else None. An order no record names is left to the
    route's own `order_not_found`."""
    from pathlib import Path

    from packages.orchestration.api_clients import client_lists_project
    from packages.orchestration.order_file import OrderFileError, parse_order_file_text
    from packages.orchestration.project_registry import (
        AmbiguousProjectError,
        InvalidProjectSelectorError,
        ProjectNotFoundError,
        select_project,
    )
    from packages.orchestration.serve_paths import serve_paths
    from packages.orchestration.serve_runs import read_order_record

    record = read_order_record(serve_paths(), order)
    if record is None:
        return None
    refusal = (f"the client {client.name!r} may not read order {order!r}, which is not an order "
               "of one of its projects")
    try:
        parsed = parse_order_file_text(Path(record.order_file).read_text(encoding="utf-8"),
                                       "order.md")
    except (OSError, UnicodeDecodeError, OrderFileError):
        return refusal
    if not parsed.projects:
        return refusal
    for selector in parsed.projects:
        try:
            project, _source = select_project(selector, ".")
        except (AmbiguousProjectError, InvalidProjectSelectorError, ProjectNotFoundError):
            return refusal
        if not client_lists_project(client, (project.slug or "", str(project.id))):
            return refusal
    return None
