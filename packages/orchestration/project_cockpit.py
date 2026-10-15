"""A project's ledger cost on one UTC day (F042 T001, DECISION F042 D1), for the client digest.

PURE COMPOSITION over the token ledger's ``query_cost``: this module owns no storage, writes no
file, starts no subprocess and opens no socket. The multi-project cockpit's project list and
per-project card that once lived here (``projects_view``, ``find_project``, ``job_project_view``,
``project_summary``) were deleted with the old face, because only its routes read them
(operator amendment amend1015-face-migration, DECISION amend1015f D19). The module keeps its name.

Public API::

    project_cost_of_day(project_id, moment) -> dict
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from packages.orchestration.job_digest import (
    COST_BASIS_ABSENT,
    COST_BASIS_ACTUAL,
    COST_BASIS_LOWER_BOUND,
)


# The one reader of a project's cost on one UTC day, which the client digest reads.
def project_cost_of_day(project_id: Any, moment: datetime) -> dict[str, Any]:
    """The project's ledger cost on *moment*'s UTC day, with its exactness basis.

    ``value_usd`` is the ledger's own sum, None when no call of the day reported
    a price; ``basis`` is ``absent`` when there is no ledger, no call or no
    figure, ``lower_bound`` when a call of the day was not measured, and
    ``actual`` otherwise. *moment* must be timezone-aware UTC.
    """
    from packages.orchestration.token_ledger import query_cost

    since = moment.date().isoformat()
    until = (moment.date() + timedelta(days=1)).isoformat()
    report = query_cost(project_id=project_id, since=since, until=until)
    total_row = report.total
    if not report.ledger_exists or not total_row.calls or total_row.cost_usd is None:
        basis = COST_BASIS_ABSENT
    elif total_row.unmeasured_calls > 0:
        basis = COST_BASIS_LOWER_BOUND
    else:
        basis = COST_BASIS_ACTUAL
    return {
        "day": since,
        "value_usd": total_row.cost_usd,
        "basis": basis,
        "harness_invocations": total_row.calls,
    }
