"""The public parse entry point.

``parse_record`` returns None on malformed input — deliberately, because
gauntlet order g06 asks for that to become a typed error.
"""
from __future__ import annotations


def parse_record(line: str) -> dict[str, str] | None:
    """One ``name=value`` record, or None when the line is malformed.

    Returning None loses the reason, which is exactly the weakness g06 exists
    to fix; :mod:`sampleproj.errors` already carries the messages a typed
    error would use.
    """
    if line is None:
        return None
    text = line.strip()
    if not text:
        return None
    name, sep, value = text.partition("=")
    if not sep:
        return None
    if not name.strip():
        return None
    return {"name": name.strip(), "value": value.strip()}


def parse_records(lines: list[str]) -> list[dict[str, str]]:
    """Every parsable record; malformed lines are skipped."""
    parsed = []
    for line in lines:
        record = parse_record(line)
        if record is not None:
            parsed.append(record)
    return parsed
