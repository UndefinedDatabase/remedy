"""
Domain tests: orchestration/test_list_options.py
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from packages.orchestration.list_options import ListOptionError, apply_list_options, parse_time_bound


def test_parse_time_bound_relative_form():
    now = datetime.now(timezone.utc)
    bound = parse_time_bound("2d")
    assert abs((now - timedelta(days=2) - bound).total_seconds()) < 5


def test_parse_time_bound_iso():
    bound = parse_time_bound("2026-01-01T00:00:00+00:00")
    assert bound == datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_parse_time_bound_invalid_raises():
    with pytest.raises(ListOptionError):
        parse_time_bound("not-a-time")


def test_default_sort_is_newest_first():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "b", "created_at": "2026-01-03T00:00:00+00:00"},
            {"id": "c", "created_at": "2026-01-02T00:00:00+00:00"}]
    out = apply_list_options(
        rows, sort=None, desc=False, since=None, until=None, limit=None,
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert [r["id"] for r in out] == ["b", "c", "a"]


def test_desc_flag_reverses_the_default():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "b", "created_at": "2026-01-03T00:00:00+00:00"}]
    out = apply_list_options(
        rows, sort=None, desc=True, since=None, until=None, limit=None,
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert [r["id"] for r in out] == ["a", "b"]


def test_unknown_sort_field_raises_naming_valid_set():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(ListOptionError, match="created_at"):
        apply_list_options(
            rows, sort="bogus", desc=False, since=None, until=None, limit=None,
            sort_fields={"created_at": lambda r: r["created_at"]},
            default_sort_field="created_at",
            date_getter=lambda r: r["created_at"],
        )


def test_since_until_filter_by_date():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"},
            {"id": "b", "created_at": "2026-01-05T00:00:00+00:00"},
            {"id": "c", "created_at": "2026-01-10T00:00:00+00:00"}]
    out = apply_list_options(
        rows, sort=None, desc=False, since="2026-01-02T00:00:00+00:00",
        until="2026-01-09T00:00:00+00:00", limit=None,
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert [r["id"] for r in out] == ["b"]


def test_limit_caps_rows():
    rows = [{"id": str(i), "created_at": f"2026-01-{i:02d}T00:00:00+00:00"} for i in range(1, 6)]
    out = apply_list_options(
        rows, sort=None, desc=False, since=None, until=None, limit="2",
        sort_fields={"created_at": lambda r: r["created_at"]},
        default_sort_field="created_at",
        date_getter=lambda r: r["created_at"],
    )
    assert len(out) == 2


def test_invalid_limit_raises():
    rows = [{"id": "a", "created_at": "2026-01-01T00:00:00+00:00"}]
    with pytest.raises(ListOptionError):
        apply_list_options(
            rows, sort=None, desc=False, since=None, until=None, limit="not-a-number",
            sort_fields={"created_at": lambda r: r["created_at"]},
            default_sort_field="created_at",
            date_getter=lambda r: r["created_at"],
        )


def test_no_default_sort_field_keeps_original_order_when_sort_not_given():
    rows = [{"id": "c"}, {"id": "a"}, {"id": "b"}]
    out = apply_list_options(
        rows, sort=None, desc=False, since=None, until=None, limit=None,
        sort_fields={"id": lambda r: r["id"]},
        default_sort_field=None,
    )
    assert [r["id"] for r in out] == ["c", "a", "b"]


def test_no_default_sort_field_still_honours_explicit_sort():
    rows = [{"id": "c"}, {"id": "a"}, {"id": "b"}]
    out = apply_list_options(
        rows, sort="id", desc=False, since=None, until=None, limit=None,
        sort_fields={"id": lambda r: r["id"]},
        default_sort_field=None,
    )
    assert [r["id"] for r in out] == ["a", "b", "c"]
