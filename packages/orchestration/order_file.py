"""F295 T001 — an order file: `remedy do <order.md>` reads its order from disk.

DECISION F295 D2 rules the shape. An argument names an order file when,
stripped of outer whitespace, it is not empty, holds no whitespace and ends
in `.md` in any letter case; every other argument is order text. The file is
UTF-8, a leading byte-order mark allowed. When its first line is exactly
`---`, the lines up to the next line that is exactly `---` are its header;
otherwise the whole file is the order. A header line is `key: value`, a
blank line is ignored, the keys are `project`, `contract`, `max-cost-usd`
(each at most once) and `constraint` (as often as needed). The constraints
reach the planner appended to the order text. This module knows nothing of
the command line; `apps/cli/commands/do_cmd.py` calls it first. DECISION
F295 D3: `read_order_file` also returns the file's resolved absolute path
and the sha256 of the exact bytes it read, as `OrderFile.source_path` and
`.source_sha256`.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from pathlib import Path

#: The header's recognised keys, each meaning what the flag of the same name
#: means; `constraint` is the one key a header may repeat.
ORDER_FILE_HEADER_KEYS = ("project", "contract", "max-cost-usd", "constraint")

#: The single-valued keys — repeating one of these is `order_file_invalid_header`.
_SINGLE_VALUED_KEYS = ("project", "contract", "max-cost-usd")

#: The header's opening and closing delimiter, matched by exact line equality.
_HEADER_DELIMITER = "---"


# WHY: a refusal needs a stable machine token distinct from its human sentence,
# so a caller can branch on `.error` without parsing prose (DECISION F295 D2 (5)).
class OrderFileError(Exception):
    """An order file refuses to be read or parsed; `.error` is the machine token.

    The message names the path and does not end "Nothing was run." — the
    caller (`_cmd_do`) owns that closing clause.
    """

    def __init__(self, error: str, message: str) -> None:
        self.error = error
        super().__init__(message)


# WHY: the parsed order file in one immutable value, carried from read_order_file
# straight into _cmd_do's merge with the command line (DECISION F295 D2 (4)).
@dataclass(frozen=True)
class OrderFile:
    """The parsed contents of one order file."""

    path: str
    text: str
    project: str | None
    contract: str | None
    max_cost_usd: str | None
    constraints: tuple[str, ...]
    #: The file's resolved absolute path (DECISION F295 D3); "" for text `parse_order_file_text` parsed directly.
    source_path: str = ""
    #: sha256 (hex) of the exact bytes `read_order_file` read (DECISION F295 D3); "" likewise.
    source_sha256: str = ""


# WHY: the one predicate that decides text-vs-file, read by both `_cmd_do` and
# this module's own tests, so the rule is defined exactly once (DECISION F295 D2 (1)).
def order_argument_names_file(argument: str) -> bool:
    """True when `argument` names an order file rather than order text."""
    stripped = argument.strip()
    if not stripped:
        return False
    if any(ch.isspace() for ch in stripped):
        return False
    return stripped.lower().endswith(".md")


# WHY: the header/order split and every refusal it can raise, isolated from
# file I/O so a test can drive it on a plain string (DECISION F295 D2 (2), (3)).
def parse_order_file_text(raw: str, path: str) -> OrderFile:
    """Parse `raw` (the order file's decoded text) into an `OrderFile`.

    Raises `OrderFileError` with `order_file_invalid_header` for a broken
    header and `order_file_empty` for an order text that is empty once
    stripped.
    """
    lines = raw.splitlines()
    project: str | None = None
    contract: str | None = None
    max_cost_usd: str | None = None
    constraints: list[str] = []
    order_lines = lines

    if lines and lines[0] == _HEADER_DELIMITER:
        close_index = None
        for index in range(1, len(lines)):
            if lines[index] == _HEADER_DELIMITER:
                close_index = index
                break
        if close_index is None:
            raise OrderFileError(
                "order_file_invalid_header",
                f"{path}: line 1 ({_HEADER_DELIMITER!r}) opens a header that no "
                f"second {_HEADER_DELIMITER!r} line closes.",
            )
        seen_single: dict[str, bool] = {key: False for key in _SINGLE_VALUED_KEYS}
        for offset, line in enumerate(lines[1:close_index]):
            line_no = offset + 2  # 1-based; line 1 is the opening delimiter.
            if not line.strip():
                continue
            if ":" not in line:
                raise OrderFileError(
                    "order_file_invalid_header",
                    f"{path}: line {line_no} ({line!r}) is not `key: value`.",
                )
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            if key not in ORDER_FILE_HEADER_KEYS:
                raise OrderFileError(
                    "order_file_invalid_header",
                    f"{path}: line {line_no} ({line!r}) names the unknown header "
                    f"key {key!r}.",
                )
            if not value:
                raise OrderFileError(
                    "order_file_invalid_header",
                    f"{path}: line {line_no} ({line!r}) has an empty value.",
                )
            if key in seen_single:
                if seen_single[key]:
                    raise OrderFileError(
                        "order_file_invalid_header",
                        f"{path}: line {line_no} ({line!r}) repeats the header "
                        f"key {key!r}.",
                    )
                seen_single[key] = True
                if key == "project":
                    project = value
                elif key == "contract":
                    contract = value
                else:
                    max_cost_usd = value
            else:
                constraints.append(value)
        order_lines = lines[close_index + 1:]

    order_text = "\n".join(order_lines).strip()
    if not order_text:
        raise OrderFileError("order_file_empty", f"{path} carries no order text.")

    if constraints:
        text = (order_text + "\n\nConstraints the plan must honour:\n"
                + "\n".join(f"- {constraint}" for constraint in constraints))
    else:
        text = order_text

    return OrderFile(
        path=path, text=text, project=project, contract=contract,
        max_cost_usd=max_cost_usd, constraints=tuple(constraints),
    )


# WHY: the one function `_cmd_do` calls — reads the bytes, maps every I/O
# failure to its refusal code, then hands off to parse_order_file_text
# (DECISION F295 D2 (5)); it alone sees the bytes on disk, so it alone sets
# `source_path` and `source_sha256` (DECISION F295 D3).
def read_order_file(path: str) -> OrderFile:
    """Read and parse the order file at `path`, or raise `OrderFileError`."""
    try:
        raw_bytes = Path(path).read_bytes()
    except FileNotFoundError as exc:
        raise OrderFileError(
            "order_file_not_found", f"{path} does not exist.") from exc
    except OSError as exc:
        raise OrderFileError(
            "order_file_unreadable", f"{path} cannot be read: {exc}.") from exc
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise OrderFileError(
            "order_file_unreadable", f"{path} cannot be read: {exc}.") from exc
    order = parse_order_file_text(text, path)
    return replace(
        order,
        source_path=str(Path(path).resolve()),
        source_sha256=hashlib.sha256(raw_bytes).hexdigest(),
    )
