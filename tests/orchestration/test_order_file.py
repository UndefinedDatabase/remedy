"""Unit tests for `packages/orchestration/order_file.py` (F295 T001, DECISION F295 D2)."""
from __future__ import annotations

import hashlib

import pytest

from packages.orchestration.order_file import (
    OrderFileError,
    order_argument_names_file,
    parse_order_file_text,
    read_order_file,
)

# ── order_argument_names_file (D2 (1)) ────────────────────────────────────────


@pytest.mark.parametrize("argument", [
    "order.md", "ORDER.MD", "docs/next-order.md", "  order.md  ",
])
def test_a_single_dot_md_path_in_any_case_with_outer_whitespace_names_a_file(argument):
    assert order_argument_names_file(argument) is True


@pytest.mark.parametrize("argument", [
    "fix the heading in README.md", "notes.txt", "", "   ",
])
def test_text_holding_whitespace_or_no_dot_md_suffix_is_not_a_file(argument):
    assert order_argument_names_file(argument) is False


# ── parse_order_file_text: the header/order split (D2 (2), (3)) ──────────────


def test_a_file_with_no_header_is_entirely_order_text():
    order = parse_order_file_text("Write a CONTRIBUTING.md.\n", "order.md")
    assert order.text == "Write a CONTRIBUTING.md."
    assert (order.project, order.contract, order.max_cost_usd) == (None, None, None)
    assert order.constraints == ()


def test_every_header_key_is_read():
    raw = (
        "---\n"
        "project: demo\n"
        "contract: website\n"
        "max-cost-usd: 5\n"
        "max-total-tokens: 20000\n"
        "max-provider-calls: 12\n"
        "max-wall-clock-minutes: 30\n"
        "constraint: never edit README.md\n"
        "---\n"
        "Write a CONTRIBUTING.md.\n"
    )
    order = parse_order_file_text(raw, "order.md")
    assert order.project == "demo"
    assert order.contract == "website"
    assert order.max_cost_usd == "5"
    # DECISION F304 D14: the other three job budgets are caps an order file may carry.
    assert (order.max_total_tokens, order.max_provider_calls,
            order.max_wall_clock_minutes) == ("20000", "12", "30")
    assert order.constraints == ("never edit README.md",)
    assert order.text.startswith("Write a CONTRIBUTING.md.")


def test_a_file_without_the_other_caps_reads_none_for_each():
    order = parse_order_file_text("---\nmax-cost-usd: 1\n---\nOrder text.\n", "order.md")
    assert (order.max_total_tokens, order.max_provider_calls,
            order.max_wall_clock_minutes) == (None, None, None)


@pytest.mark.parametrize("key", ["max-total-tokens", "max-provider-calls",
                                 "max-wall-clock-minutes"])
def test_a_repeated_cap_key_names_its_line_number(key):
    raw = f"---\n{key}: 1\n{key}: 2\n---\nOrder text.\n"
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text(raw, "order.md")
    exc = exc_info.value
    assert exc.error == "order_file_invalid_header"
    assert "line 3" in str(exc)


def test_a_repeated_constraint_keeps_order_and_builds_the_d2_3_text_exactly():
    raw = (
        "---\n"
        "constraint: never edit README.md\n"
        "constraint: keep the CLI backward compatible\n"
        "---\n"
        "Write a CONTRIBUTING.md.\n"
    )
    order = parse_order_file_text(raw, "order.md")
    assert order.constraints == (
        "never edit README.md", "keep the CLI backward compatible")
    assert order.text == (
        "Write a CONTRIBUTING.md.\n\n"
        "Constraints the plan must honour:\n"
        "- never edit README.md\n"
        "- keep the CLI backward compatible"
    )


def test_a_blank_header_line_is_ignored():
    raw = "---\nproject: demo\n\ncontract: website\n---\nOrder text.\n"
    order = parse_order_file_text(raw, "order.md")
    assert (order.project, order.contract) == ("demo", "website")


# ── order_file_invalid_header, each cause naming its 1-based line (D2 (5)) ───


def test_an_unclosed_header_gives_order_file_invalid_header_naming_line_1():
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text("---\nproject: demo\nOrder text.\n", "order.md")
    exc = exc_info.value
    assert exc.error == "order_file_invalid_header"
    assert "line 1" in str(exc)
    assert "order.md" in str(exc)
    assert not str(exc).endswith("Nothing was run.")


def test_a_header_line_without_a_colon_names_its_line_number():
    raw = "---\nbudget 3\n---\nOrder text.\n"
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text(raw, "order.md")
    exc = exc_info.value
    assert exc.error == "order_file_invalid_header"
    assert "line 2" in str(exc)


def test_an_unknown_header_key_names_its_line_number():
    raw = "---\nbudget: 3\n---\nOrder text.\n"
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text(raw, "order.md")
    exc = exc_info.value
    assert exc.error == "order_file_invalid_header"
    assert "line 2" in str(exc)


def test_an_empty_header_value_names_its_line_number():
    raw = "---\nproject: \n---\nOrder text.\n"
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text(raw, "order.md")
    exc = exc_info.value
    assert exc.error == "order_file_invalid_header"
    assert "line 2" in str(exc)


def test_the_same_project_named_twice_names_its_line_number():
    raw = "---\nproject: demo\nproject: demo\n---\nOrder text.\n"
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text(raw, "order.md")
    exc = exc_info.value
    assert exc.error == "order_file_invalid_header"
    assert "line 3" in str(exc)


def test_several_projects_are_read_in_their_order():
    """DECISION F205 D4: each `project` line names one more project; the first is `project`."""
    several = parse_order_file_text("---\nproject: demo\nproject: other\n---\nOrder text.\n",
                                    "order.md")
    assert (several.project, several.projects) == ("demo", ("demo", "other"))
    assert several.project_selector == ("demo", "other")
    one = parse_order_file_text("---\nproject: demo\n---\nOrder text.\n", "order.md")
    assert (one.projects, one.project_selector) == (("demo",), "demo")
    none = parse_order_file_text("Order text.\n", "order.md")
    assert (none.project, none.projects, none.project_selector) == (None, (), None)


# ── order_file_empty (D2 (5)) ─────────────────────────────────────────────────


def test_an_empty_order_after_the_header_gives_order_file_empty():
    raw = "---\nproject: demo\n---\n   \n"
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text(raw, "order.md")
    assert exc_info.value.error == "order_file_empty"


def test_a_zero_byte_file_gives_order_file_empty():
    with pytest.raises(OrderFileError) as exc_info:
        parse_order_file_text("", "order.md")
    assert exc_info.value.error == "order_file_empty"


# ── read_order_file: the byte-order mark and the I/O refusals (D2 (5)) ───────


def test_a_byte_order_mark_is_allowed(tmp_path):
    path = tmp_path / "order.md"
    path.write_bytes(b"\xef\xbb\xbfWrite a CONTRIBUTING.md.\n")
    order = read_order_file(str(path))
    assert order.text == "Write a CONTRIBUTING.md."


def test_a_missing_path_gives_order_file_not_found(tmp_path):
    path = tmp_path / "missing.md"
    with pytest.raises(OrderFileError) as exc_info:
        read_order_file(str(path))
    exc = exc_info.value
    assert exc.error == "order_file_not_found"
    assert str(path) in str(exc)


def test_a_directory_gives_order_file_unreadable(tmp_path):
    path = tmp_path / "order.md"
    path.mkdir()
    with pytest.raises(OrderFileError) as exc_info:
        read_order_file(str(path))
    assert exc_info.value.error == "order_file_unreadable"


def test_invalid_utf8_gives_order_file_unreadable(tmp_path):
    path = tmp_path / "order.md"
    path.write_bytes(b"\xff\xfe\x00\x81")
    with pytest.raises(OrderFileError) as exc_info:
        read_order_file(str(path))
    assert exc_info.value.error == "order_file_unreadable"


# ── source_path and source_sha256 (DECISION F295 D3) ─────────────────────────


def test_read_order_file_returns_the_resolved_path_and_digest_of_the_bytes_read(tmp_path):
    path = tmp_path / "order.md"
    raw = b"\xef\xbb\xbfWrite a CONTRIBUTING.md.\n"
    path.write_bytes(raw)
    order = read_order_file(str(path))
    assert order.source_path == str(path.resolve())
    assert order.source_sha256 == hashlib.sha256(raw).hexdigest()


def test_parse_order_file_text_leaves_source_path_and_digest_empty():
    order = parse_order_file_text("Write a CONTRIBUTING.md.\n", "order.md")
    assert order.source_path == ""
    assert order.source_sha256 == ""
