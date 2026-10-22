"""F113 T001 — the named local endpoints a side role may run on, their health probe, and their call.

A local endpoint is an Ollama server on this machine or the operator's network, named in the
`local_routing.endpoints` table with exactly a `base_url` and a `model` (DECISION F113 D1). Several
may be named; Remedy balances no load between them. The probe asks the server for its model list the
first time a process uses the endpoint and keeps the answer for `LOCAL_PROBE_MAX_AGE_S`, so a
long-lived process notices an endpoint that went away or came back. An endpoint that does not answer,
or does not serve its model, is classified `provider_unavailable`, the same class model failover and
the failure postmortem already read, and the side role falls back (`side_role_routing.py`).

The call goes through the planner's own Ollama client, `OllamaPlanner.raw_call`, with the endpoint's
host and model: Remedy deliberately does not write a second local adapter. A local endpoint keeps no
conversation between calls, so it never resumes one.
"""

from __future__ import annotations

import time
import warnings
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from packages.orchestration.config_keys_model_routing import LOCAL_ENDPOINTS_CONFIG_KEY

#: The two keys an endpoint table holds; any other key is refused.
LOCAL_ENDPOINT_KEYS: tuple[str, ...] = ("base_url", "model")

#: How long one probe's answer stands before the next use asks the server again.
LOCAL_PROBE_MAX_AGE_S: float = 300.0

#: How long the probe waits for the server's model list.
LOCAL_PROBE_TIMEOUT_S: float = 5.0

#: Every unavailable reason opens with this, so `is_provider_unavailable_error` reads it.
LOCAL_UNAVAILABLE_PREFIX: str = "provider_unavailable: local endpoint"


@dataclass(frozen=True)
class LocalEndpoint:
    """One named local endpoint: the server's base URL and the model it serves."""

    name: str
    base_url: str
    model: str

    @property
    def supports_resume(self) -> bool:
        # Honest capability flag: a chat call keeps no session, so there is nothing to resume.
        return False


class LocalEndpointError(ValueError):
    """A `local_routing.endpoints` table Remedy cannot use. Every message starts the same way."""


def parse_local_endpoints(raw: Mapping[str, Any]) -> dict[str, LocalEndpoint]:
    """Return the endpoints `raw` names, in the table's order, or RAISE :class:`LocalEndpointError`."""
    endpoints: dict[str, LocalEndpoint] = {}
    for name, entry in raw.items():
        if not isinstance(entry, Mapping):
            raise LocalEndpointError(
                f"local_routing.endpoints: {name!r} must be a table, got {type(entry).__name__}")
        for key in entry:
            if key not in LOCAL_ENDPOINT_KEYS:
                raise LocalEndpointError(
                    f"local_routing.endpoints: {name!r} has unknown key {key!r}; an endpoint holds "
                    f"exactly {', '.join(LOCAL_ENDPOINT_KEYS)}")
        base_url = entry.get("base_url")
        if not isinstance(base_url, str) or not base_url.startswith(("http://", "https://")):
            raise LocalEndpointError(
                f"local_routing.endpoints: {name!r} must set base_url to an http:// or https:// URL")
        model = entry.get("model")
        if not isinstance(model, str) or not model:
            raise LocalEndpointError(
                f"local_routing.endpoints: {name!r} must set model to a non-empty string")
        endpoints[name] = LocalEndpoint(name=name, base_url=base_url.rstrip("/"), model=model)
    return endpoints


def resolve_local_endpoints() -> dict[str, LocalEndpoint]:
    """Return the endpoints this project's configuration names, or `{}` when it names none.

    A table that cannot be read gives exactly one `UserWarning` naming the fault and answers `{}`:
    no side role runs locally on an endpoint Remedy could not read.
    """
    from packages.orchestration.config import get_config

    value = get_config().get(LOCAL_ENDPOINTS_CONFIG_KEY)
    if not isinstance(value, Mapping) or not value:
        return {}
    try:
        return parse_local_endpoints(dict(value))
    except LocalEndpointError as exc:
        warnings.warn(f"{exc}; no side role runs locally", stacklevel=2)
        return {}


@dataclass(frozen=True)
class LocalEndpointHealth:
    """What one probe found: whether the endpoint can serve, and why not when it cannot."""

    endpoint: str
    available: bool
    reason: str


def _ollama_model_names(base_url: str) -> list[str]:
    """The model names the Ollama server at `base_url` lists."""
    import ollama

    listing = ollama.Client(host=base_url, timeout=LOCAL_PROBE_TIMEOUT_S).list()
    return [str(entry.model) for entry in listing.models if entry.model]


def _probe_errors() -> tuple[type[BaseException], ...]:
    """The errors a probe turns into an unavailable answer: the client's own, the transport's, a missing package."""
    errors: list[type[BaseException]] = [ImportError, OSError, ValueError]
    try:
        import httpx
        import ollama
    except ImportError:
        return tuple(errors)
    return (*errors, ollama.ResponseError, ollama.RequestError, httpx.HTTPError)


def _serves(names: Iterable[str], model: str) -> bool:
    """Whether `model` is among `names`; a name without a tag matches its `:latest`."""
    wanted = {model, f"{model}:latest"} if ":" not in model else {model}
    return any(name in wanted for name in names)


def probe_local_endpoint(
    endpoint: LocalEndpoint, *, list_models: Callable[[str], Iterable[str]] | None = None,
) -> LocalEndpointHealth:
    """Ask the endpoint's server for its models; never raises."""
    lister = list_models or _ollama_model_names
    where = f"{LOCAL_UNAVAILABLE_PREFIX} {endpoint.name} at {endpoint.base_url}"
    try:
        names = list(lister(endpoint.base_url))
    except _probe_errors() as exc:
        return LocalEndpointHealth(endpoint.name, False, f"{where} did not answer: {type(exc).__name__}: {exc}")
    if not _serves(names, endpoint.model):
        return LocalEndpointHealth(endpoint.name, False, f"{where} does not serve model {endpoint.model}")
    return LocalEndpointHealth(endpoint.name, True, "")


class LocalEndpointProbes:
    """The probe at first use: the first use of an endpoint asks its server, later uses read the answer."""

    def __init__(
        self, *, list_models: Callable[[str], Iterable[str]] | None = None,
        clock: Callable[[], float] = time.monotonic, max_age_s: float = LOCAL_PROBE_MAX_AGE_S,
    ) -> None:
        self._list_models = list_models
        self._clock = clock
        self._max_age_s = max_age_s
        self._answers: dict[LocalEndpoint, tuple[float, LocalEndpointHealth]] = {}

    def health(self, endpoint: LocalEndpoint) -> LocalEndpointHealth:
        now = self._clock()
        held = self._answers.get(endpoint)
        if held is not None and now - held[0] < self._max_age_s:
            return held[1]
        answer = probe_local_endpoint(endpoint, list_models=self._list_models)
        self._answers[endpoint] = (now, answer)
        return answer


#: The probes of this process, which the side-role route reads.
LOCAL_ENDPOINT_PROBES = LocalEndpointProbes()


def make_local_call_fn(endpoint: LocalEndpoint, model_cls: type[BaseModel]) -> Callable[[str, int], str]:
    """A structured call_fn bound to `model_cls` that the endpoint's model serves."""
    from packages.orchestration.schemas import to_json_schema
    from packages.providers.ollama_planner.provider import OllamaPlanner

    planner = OllamaPlanner(model=endpoint.model, host=endpoint.base_url)
    schema = to_json_schema(model_cls)

    def _call(prompt: str, attempt: int) -> str:
        from packages.orchestration.order_cancel import walk_cancel_reader
        from packages.orchestration.planner_cancel import planner_call_scope

        with planner_call_scope(walk_cancel_reader()):
            return planner.raw_call(prompt, schema=schema)

    _call.resolved_model = planner.model  # type: ignore[attr-defined]
    # Inside a `remedy do` walk the call is recorded on the order's ledger, as every planner call is.
    from packages.orchestration.order_ledger import bound_order_ledger, reason_for

    ledger = bound_order_ledger()
    return _call if ledger is None else ledger.wrap(reason_for(model_cls), _call)
