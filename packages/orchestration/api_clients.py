"""The client tokens and the policy the operator writes for them (F253, DECISION F253 D16).

The operator writes the file `clients.json` into the `api` folder of the data root, beside the
call ledger `calls.jsonl`. It holds one JSON object whose only key `clients` is a list; each entry
holds exactly the keys `name`, `token`, `projects`, `max_total_tokens`, `max_provider_calls` and
`may_apply`, and no two entries share a name or a token. Fail-closed rule (D16 (2)): the file is
read again at every call, and a file that is missing, that group or others may read or write, that
cannot be read, that is not JSON, or that holds any part outside this shape, holds no client at
all, so a mistake in it never grants more than the operator wrote. A client token answers a
decision, declines a result and applies a job only for a job of its projects, and may not raise a
budget limit above its ceilings (DECISION F253 D17).
"""

from __future__ import annotations

import json
import secrets
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: The file's name under the data root's `api` folder (DECISION F253 D16 (1)).
API_CLIENTS_FILE_NAME = "clients.json"

#: The fewest characters a client token may have (DECISION F253 D16 (1)).
API_CLIENT_TOKEN_MIN_LENGTH = 32

_ENTRY_KEYS = frozenset(
    {"name", "token", "projects", "max_total_tokens", "max_provider_calls", "may_apply"})


@dataclass(frozen=True)
class ApiClient:
    """One client the operator wrote: its token and the policy that token carries."""

    name: str
    #: Kept out of every `repr`, so that a log line or a traceback never shows it.
    token: str = field(repr=False)
    projects: tuple[str, ...]
    max_total_tokens: int | None
    max_provider_calls: int | None
    may_apply: bool


def api_clients_path(root: Path | None = None) -> Path:
    """The file the operator writes the clients into, under the data root's `api` folder."""
    from packages.orchestration.data_paths import data_class_dir

    return data_class_dir("api", root) / API_CLIENTS_FILE_NAME


def _ceiling_valid(value: Any) -> bool:
    """True for no ceiling (None) or a whole number above zero that is not a `bool`."""
    return value is None or (isinstance(value, int) and not isinstance(value, bool) and value > 0)


def _entry_client(entry: Any) -> ApiClient | None:
    """The client one entry of the file holds, or None when the entry is outside the shape."""
    if not isinstance(entry, dict) or set(entry) != _ENTRY_KEYS:
        return None
    name, token, projects = entry["name"], entry["token"], entry["projects"]
    if not isinstance(name, str) or not name:
        return None
    if not isinstance(token, str) or len(token) < API_CLIENT_TOKEN_MIN_LENGTH:
        return None
    if not isinstance(projects, list) or not all(
            isinstance(item, str) and item for item in projects):
        return None
    if not _ceiling_valid(entry["max_total_tokens"]):
        return None
    if not _ceiling_valid(entry["max_provider_calls"]):
        return None
    if not isinstance(entry["may_apply"], bool):
        return None
    return ApiClient(
        name=name, token=token, projects=tuple(projects),
        max_total_tokens=entry["max_total_tokens"],
        max_provider_calls=entry["max_provider_calls"], may_apply=entry["may_apply"])


def load_api_clients(root: Path | None = None) -> tuple[ApiClient, ...]:
    """The clients the operator's file holds, in its order, or `()` (DECISION F253 D16 (2)).

    Never raises for the file's content or for an `OSError`: every way the file can be wrong
    answers `()`, which holds no client.
    """
    path = api_clients_path(root)
    try:
        if path.stat().st_mode & 0o077:
            return ()
        parsed = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, ValueError, RecursionError):
        return ()
    if not isinstance(parsed, dict) or set(parsed) != {"clients"}:
        return ()
    entries = parsed["clients"]
    if not isinstance(entries, list):
        return ()
    clients: list[ApiClient] = []
    for entry in entries:
        client = _entry_client(entry)
        if client is None:
            return ()
        clients.append(client)
    if len({c.name for c in clients}) != len(clients):
        return ()
    if len({c.token for c in clients}) != len(clients):
        return ()
    return tuple(clients)


def match_api_client(supplied: str, clients: Sequence[ApiClient]) -> ApiClient | None:
    """The client whose token equals SUPPLIED, or None.

    Compared as UTF-8 bytes in constant time against every client, so neither the position of
    a match nor non-ASCII bytes change how long or whether the comparison runs.
    """
    if not supplied:
        return None
    supplied_bytes = supplied.encode("utf-8")
    found: ApiClient | None = None
    for client in clients:
        if secrets.compare_digest(supplied_bytes, client.token.encode("utf-8")):
            found = client
    return found


def _cap_refusal(client: ApiClient, key: str, ceiling: int | None, cap: str | None) -> str | None:
    """One sentence when CAP, the order header's value under KEY, is outside CEILING, else None."""
    from packages.orchestration.budget_resolution import BudgetConfigError, _pos_int

    if ceiling is None:
        return None
    name = key.replace("-", "_")
    head = f"the client {client.name!r} may set '{key}:' to at most {ceiling}"
    try:
        parsed = _pos_int(name, cap)
    except BudgetConfigError:
        return f"{head}, and the order's '{key}:' is not a whole number above zero; nothing was run"
    if parsed is None:
        return f"{head}, and the order's header names no '{key}:'; nothing was run"
    if parsed > ceiling:
        return f"{head}, and the order's '{key}:' is {parsed}; nothing was run"
    return None


def client_lists_project(client: ApiClient, project_keys: Iterable[str]) -> bool:
    """True when any key of PROJECT_KEYS (a project's slug or id) is in the client's projects."""
    return any(key in client.projects for key in project_keys)


def client_order_refusal(
    client: ApiClient, project_keys: Iterable[str],
    max_total_tokens: str | None, max_provider_calls: str | None,
) -> str | None:
    """None when the order is inside CLIENT's policy, else one sentence ending "; nothing was run".

    Outside means: no key of PROJECT_KEYS (the project's slug and id) is in the client's
    projects; or, for a ceiling that is not None, the matching cap is absent, is not a whole
    number above zero, or is above the ceiling (DECISION F253 D16 (5)).
    """
    if not client_lists_project(client, project_keys):
        return (f"the client {client.name!r} may not order work on this project; "
                "nothing was run")
    return (_cap_refusal(client, "max-total-tokens", client.max_total_tokens, max_total_tokens)
            or _cap_refusal(client, "max-provider-calls", client.max_provider_calls,
                            max_provider_calls))


def client_budget_answer_refusal(client: ApiClient, answers: Sequence[str]) -> str | None:
    """One sentence ending "; nothing was run" when an item of ANSWERS raises a limit above CLIENT's
    ceiling, else None (DECISION F253 D17 (2)).

    Only an item `<limit>=<value>` whose limit, stripped, is `max_total_tokens` or
    `max_provider_calls`, and for which the client's ceiling is not None, can be refused: its value,
    read as a cap is read, must not be above the ceiling. A value that cannot be read, an item
    without `=` and every other limit are passed on, and the command refuses what it refuses.
    """
    from packages.orchestration.budget_resolution import BudgetConfigError, _pos_int

    for item in answers:
        limit, equals, value = item.partition("=")
        limit = limit.strip()
        if not equals or limit not in ("max_total_tokens", "max_provider_calls"):
            continue
        ceiling = getattr(client, limit)
        if ceiling is None:
            continue
        try:
            parsed = _pos_int(limit, value)
        except BudgetConfigError:
            continue
        if parsed is not None and parsed > ceiling:
            return (f"the client {client.name!r} may raise '{limit}' to at most {ceiling}, "
                    f"and the answer gives {parsed}; nothing was run")
    return None
