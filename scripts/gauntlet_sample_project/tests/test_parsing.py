"""The parse entry point, including what it does with malformed input."""
from sampleproj.parsing import parse_record, parse_records


def test_a_well_formed_record_parses():
    assert parse_record("name = value") == {"name": "name", "value": "value"}


def test_surrounding_whitespace_is_stripped():
    assert parse_record("  a=b  ") == {"name": "a", "value": "b"}


def test_a_line_without_a_separator_is_malformed():
    assert parse_record("no separator here") is None


def test_a_blank_field_name_is_malformed():
    assert parse_record(" = value") is None


def test_an_empty_line_is_malformed():
    assert parse_record("   ") is None


def test_malformed_lines_are_skipped_by_the_bulk_parser():
    assert parse_records(["a=1", "junk", "b=2"]) == [
        {"name": "a", "value": "1"}, {"name": "b", "value": "2"}]
