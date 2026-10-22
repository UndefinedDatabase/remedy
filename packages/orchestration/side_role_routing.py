"""F113 T002 — which side role runs on a local endpoint, the hard rule that keeps every other role off
one, and the fallback to the role's own provider.

`local_routing.side_roles` maps a role to an endpoint `local_routing.endpoints` names
(`packages/orchestration/local_endpoints.py`). Only a SIDE ROLE may be mapped: a role whose task class
the routing table sends to the cheap tier, `FAILOVER_LOCAL_ROLES` of `model_failover.py`, today
summary, teacher and study. Mapping any other role is refused with the hard rule F058 already names,
`core_role_on_local_provider` ("core never local"), and the whole table is refused with it, so no role
runs locally on a table Remedy could not accept (DECISION F113 D1).

A mapped role runs on its endpoint while no failed spot check stands against it
(`side_role_quality.py`) and the endpoint answers its probe. When either fails, the role falls back
to the path it takes unmapped, its own configured model, and the route says why. A route
travels on the call_fn as `side_role_route`, which is how the summary records what served it.
"""

from __future__ import annotations

import warnings
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from packages.orchestration.config_keys_model_routing import SIDE_ROLES_CONFIG_KEY
from packages.orchestration.local_endpoints import (
    LOCAL_ENDPOINT_PROBES,
    LocalEndpoint,
    LocalEndpointProbes,
    make_local_call_fn,
    resolve_local_endpoints,
)
from packages.orchestration.model_failover import FAILOVER_LOCAL_ROLES, RULE_CORE_ROLE_ON_LOCAL_PROVIDER
from packages.orchestration.role_config import KNOWN_ROLES
from packages.orchestration.side_role_quality import flip_reason
from packages.orchestration.token_ledger import COST_BASIS_UNKNOWN

#: The role ran on its local endpoint.
ROUTE_LOCAL = "local"
#: The role is mapped, but its endpoint could not serve, so its own provider did.
ROUTE_FALLBACK = "fallback"

#: The cost basis of a call a local endpoint served: no API tokens were bought, though the machine
#: still did the work, so the label keeps cost comparisons truthful rather than claiming a price.
#: A fallback call's basis is the ledger's `unknown`: its provider reports no cost on this path.
COST_BASIS_LOCAL_ZERO = "local_zero"


@dataclass(frozen=True)
class SideRoleRoute:
    """Where one side-role call went, the model it ran on when that is known, and why it went there."""

    role: str
    route: str
    endpoint: str
    routed_model: str
    reason: str

    @property
    def cost_basis(self) -> str:
        return COST_BASIS_LOCAL_ZERO if self.route == ROUTE_LOCAL else COST_BASIS_UNKNOWN

    def evidence(self) -> dict[str, str]:
        """The route as a record writes it."""
        return {"role": self.role, "route": self.route, "endpoint": self.endpoint,
                "routed_model": self.routed_model, "reason": self.reason, "cost_basis": self.cost_basis}


class SideRoleRoutingError(ValueError):
    """A `local_routing.side_roles` table Remedy cannot use. Every message starts the same way."""


class SideRoleRouteRefused(SideRoleRoutingError):
    """A table that maps one or more roles that are not side roles to a local endpoint."""

    def __init__(self, roles: tuple[str, ...]) -> None:
        self.roles = roles
        super().__init__("local_routing.side_roles: refused — " + "; ".join(
            f"{role}: {RULE_CORE_ROLE_ON_LOCAL_PROVIDER}" for role in roles))


def parse_side_role_routes(raw: Mapping[str, Any], endpoints: Mapping[str, LocalEndpoint]) -> dict[str, LocalEndpoint]:
    """Return each mapped role's endpoint, or RAISE: a shape fault first, then every refused role at once."""
    routes: dict[str, LocalEndpoint] = {}
    refused: list[str] = []
    for role, name in raw.items():
        if role not in KNOWN_ROLES:
            raise SideRoleRoutingError(
                f"local_routing.side_roles: {role!r} is not a known role; known roles: "
                f"{', '.join(sorted(KNOWN_ROLES))}")
        if not isinstance(name, str) or name not in endpoints:
            raise SideRoleRoutingError(
                f"local_routing.side_roles: {role!r} names endpoint {name!r}, which local_routing.endpoints "
                f"does not name; named: {', '.join(endpoints) or 'none'}")
        if role not in FAILOVER_LOCAL_ROLES:
            refused.append(role)
            continue
        routes[role] = endpoints[name]
    if refused:
        raise SideRoleRouteRefused(tuple(refused))
    return routes


def resolve_side_role_routes() -> dict[str, LocalEndpoint]:
    """Return the side roles this project maps to a local endpoint, or `{}`.

    A table that cannot be read, or that maps a core role, gives exactly one `UserWarning` naming the
    fault or the rule and answers `{}`: no role runs locally on a table Remedy refused.
    """
    from packages.orchestration.config import get_config

    value = get_config().get(SIDE_ROLES_CONFIG_KEY)
    if not isinstance(value, Mapping) or not value:
        return {}
    try:
        return parse_side_role_routes(dict(value), resolve_local_endpoints())
    except SideRoleRoutingError as exc:
        warnings.warn(f"{exc}; no side role runs locally", stacklevel=2)
        return {}


def route_side_role(role: str, endpoint: LocalEndpoint, probes: LocalEndpointProbes) -> SideRoleRoute:
    """The route of one call of a mapped role: the fallback while a failed spot check stands, else its
    endpoint while the probe says it serves, else the fallback."""
    flipped = flip_reason(role, endpoint)
    if flipped:
        return SideRoleRoute(role, ROUTE_FALLBACK, endpoint.name, "", flipped)
    health = probes.health(endpoint)
    if health.available:
        return SideRoleRoute(role, ROUTE_LOCAL, endpoint.name, endpoint.model, "")
    return SideRoleRoute(role, ROUTE_FALLBACK, endpoint.name, "", health.reason)


def side_role_call_fn(
    role: str, model_cls: type[BaseModel], fallback: Callable[[], Callable[[str, int], str] | None], *,
    routes: Mapping[str, LocalEndpoint] | None = None, probes: LocalEndpointProbes | None = None,
) -> Callable[[str, int], str] | None:
    """The call_fn a side role's call runs on: its local endpoint, or `fallback()`, the role's own path.

    An unmapped role gets `fallback()` untouched. A mapped role's call_fn carries its route as
    `side_role_route`, also when the fallback served it; when the fallback has nothing to serve with,
    the answer is None, as the role's own path answers.
    """
    endpoint = (resolve_side_role_routes() if routes is None else routes).get(role)
    if endpoint is None:
        return fallback()
    route = route_side_role(role, endpoint, LOCAL_ENDPOINT_PROBES if probes is None else probes)
    call_fn = make_local_call_fn(endpoint, model_cls) if route.route == ROUTE_LOCAL else fallback()
    if call_fn is not None:
        call_fn.side_role_route = route  # type: ignore[attr-defined]
    return call_fn
