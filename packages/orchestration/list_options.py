"""
Shared sort/filter/limit behaviour for list commands (F262 T003).

One implementation, called by a list handler's own already-built row
list, instead of N hand-rolled copies. The same call produces the rows
for BOTH --json and text rendering, so behaviour and the newest-first
default stay identical between the two.

Public API::

    apply_list_options(rows, sort=, desc=, since=, until=, limit=,
                        sort_fields=, default_sort_field=,
                        date_getter=) -> list
    parse_time_bound(value) -> datetime
    ListOptionError
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from typing import Any, TypeVar

T = TypeVar("T")

_RELATIVE_UNITS = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds"}


class ListOptionError(ValueError):
    """--sort/--since/--until/--limit could not be honoured; the CLI layer
    turns this into a clean stderr message and a non-zero exit, never a
    traceback."""


def parse_time_bound(value: str) -> datetime:
    """Parse an ISO-8601 timestamp or a relative form (2d, 12h, 30m, 45s)
    into an absolute, timezone-aware UTC datetime. A relative form always
    means "this far back from now"."""
    value = value.strip()
    if len(value) >= 2 and value[-1] in _RELATIVE_UNITS and value[:-1].isdigit():
        amount = int(value[:-1])
        unit = _RELATIVE_UNITS[value[-1]]
        return datetime.now(timezone.utc) - timedelta(**{unit: amount})
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ListOptionError(
            f"invalid time value {value!r}: expected ISO-8601 or a relative form like 2d/12h"
        ) from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def apply_list_options(
    rows: list[T],
    *,
    sort: str | None,
    desc: bool,
    since: str | None,
    until: str | None,
    limit: str | None,
    sort_fields: dict[str, Callable[[T], Any]],
    default_sort_field: str,
    date_getter: Callable[[T], str | None] | None = None,
) -> list[T]:
    """Filter by --since/--until, order by --sort/--desc (newest-first is
    the DEFAULT with no flags at all), then cap by --limit — in that
    order. `sort_fields` maps a valid --sort NAME to a key function over a
    row; an unknown name raises ListOptionError naming the valid set.
    `date_getter` extracts a row's own date string for --since/--until; a
    store with no timestamp concept passes None and --since/--until are
    accepted but filter nothing."""
    out = list(rows)

    if (since or until) and date_getter is not None:
        lo = parse_time_bound(since) if since else None
        hi = parse_time_bound(until) if until else None
        filtered = []
        for row in out:
            raw = date_getter(row)
            if raw is None:
                continue
            try:
                dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            except ValueError:
                continue
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            if lo is not None and dt < lo:
                continue
            if hi is not None and dt > hi:
                continue
            filtered.append(row)
        out = filtered

    field = sort or default_sort_field
    if field not in sort_fields:
        valid = ", ".join(sorted(sort_fields))
        raise ListOptionError(f"unknown --sort field {field!r}; valid fields: {valid}")
    is_default_reverse = field == default_sort_field
    reverse = (not desc) if is_default_reverse else desc
    out = sorted(out, key=sort_fields[field], reverse=reverse)

    if limit:
        try:
            n = int(limit)
        except ValueError as exc:
            raise ListOptionError(f"invalid --limit value {limit!r}: must be an integer") from exc
        out = out[:n]

    return out
