"""Property tests for the F033 stable hunk identity.

One test per PROPERTY the feature turns on, named for the property rather than for the
mechanism that happens to implement it, so a later change of mechanism does not leave a
misleading test name behind. The properties, in the order they appear below:

1. re-emitting the same hunk keeps its id;
2. an edit ELSEWHERE in the file leaves other hunks' ids alone — this is the whole point
   of the feature, the one the positional ``"<file_index>:<hunk_index>"`` scheme in
   ``packages/orchestration/diff_parser.py`` cannot satisfy;
3. trailing whitespace is noise, and 4. leading whitespace is not;
5. path is part of the identity; 6. exact duplicates are separated by ``occurrence``;
7. the id survives a PROCESS boundary, which the builtin salted hash would not;
8. no input raises, and every input still yields a well-formed id;
9. the id's shape.

Every input is constructed inline; there is deliberately no fixture file, because the
inputs are three-line lists and a reader should see them beside the expectation.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from packages.orchestration.hunk_identity import (
    HUNK_ID_LENGTH,
    hunk_identity,
    normalise_old_side,
)

#: Repo root, so the subprocess in the cross-process test imports the SAME
#: ``packages.orchestration`` tree this test imported, not one off ``site-packages``.
REPO_ROOT = Path(__file__).resolve().parents[2]

_HEX_DIGITS = frozenset("0123456789abcdef")

#: One small file's old side, used to carve two hunks out of a single file.
FILE_OLD_SIDE = [
    "def render(payload):",
    "    header = payload['header']",
    "    body = payload['body']",
    "",
    "",
    "def footer(payload):",
    "    return payload['footer']",
    "",
]

FIRST_HUNK = FILE_OLD_SIDE[0:3]
SECOND_HUNK = FILE_OLD_SIDE[5:7]

#: Fixed inputs for the cross-process test; the child program is generated from these
#: constants so there is exactly one source of truth for what both sides hash.
CROSS_PROCESS_PATH = "pkg/app.py"
CROSS_PROCESS_LINES = ["    alpha", "beta  ", "\tgamma"]
CROSS_PROCESS_OCCURRENCE = 2

#: Two DIFFERENT fixed seeds, set explicitly rather than left to the interpreter default,
#: so the test really exercises two distinct hash salts instead of hoping for one.
HASH_SEEDS = ("1", "424242")


def assert_well_formed_id(value: object) -> None:
    """A well-formed id, asserted positively — "nothing raised" is not the claim."""
    assert isinstance(value, str), f"expected a str id, got {type(value).__name__}"
    assert len(value) == HUNK_ID_LENGTH, f"expected {HUNK_ID_LENGTH} chars, got {len(value)}: {value!r}"
    assert set(value) <= _HEX_DIGITS, f"expected lowercase hex, got {value!r}"


def test_the_same_hunk_re_emitted_keeps_its_id() -> None:
    """Determinism within one process: identical inputs, identical output."""
    first = hunk_identity("pkg/app.py", FIRST_HUNK)
    second = hunk_identity("pkg/app.py", list(FIRST_HUNK))
    assert first == second
    assert_well_formed_id(first)


def test_an_edit_elsewhere_leaves_other_hunk_ids_unchanged() -> None:
    """THE stability property. Two hunks are carved from one file; the FIRST hunk's lines
    are then rewritten. The second hunk's id must not move — under the positional scheme
    it would, because inserting or removing a hunk renumbers everything after it."""
    first_before = hunk_identity("pkg/app.py", FIRST_HUNK, 0)
    second_before = hunk_identity("pkg/app.py", SECOND_HUNK, 0)

    edited_first = [
        "def render(payload, *, theme):",
        "    header = payload['header']",
        "    body = theme.wrap(payload['body'])",
        "    extra = theme.footnote()",
    ]
    first_after = hunk_identity("pkg/app.py", edited_first, 0)
    second_after = hunk_identity("pkg/app.py", SECOND_HUNK, 0)

    # The discriminator: the edited hunk really did change identity, so the unchanged
    # reading below is evidence about stability and not about a function that ignores
    # its input.
    assert first_after != first_before
    assert second_after == second_before


def test_trailing_whitespace_does_not_change_the_id() -> None:
    """Trailing spaces, a trailing CR and a bare line are one hunk, not three."""
    padded = hunk_identity("pkg/app.py", ["alpha   ", "beta\t"])
    carriage_return = hunk_identity("pkg/app.py", ["alpha\r", "beta\r"])
    bare = hunk_identity("pkg/app.py", ["alpha", "beta"])
    assert padded == carriage_return == bare
    assert normalise_old_side(["alpha   ", "beta\r"]) == "alpha\nbeta"


def test_leading_whitespace_does_change_the_id() -> None:
    """The negative of the test above, and what stops the normalisation being over-broad:
    indentation is meaning, so two bodies differing only in indent are different hunks."""
    flush = hunk_identity("pkg/app.py", ["alpha", "beta"])
    indented = hunk_identity("pkg/app.py", ["    alpha", "    beta"])
    assert flush != indented
    assert normalise_old_side(["    alpha"]) == "    alpha"


def test_the_same_content_at_a_different_path_gets_a_different_id() -> None:
    """The path is part of the identity: the same three lines in two files are two hunks."""
    here = hunk_identity("pkg/app.py", FIRST_HUNK)
    there = hunk_identity("pkg/other.py", FIRST_HUNK)
    assert here != there
    assert_well_formed_id(here)
    assert_well_formed_id(there)


def test_two_identical_hunks_in_one_file_are_separated_by_occurrence() -> None:
    """Byte-identical old sides in ONE file would otherwise collide; ``occurrence`` is the
    minimal disambiguator, and it is a rank rather than a position."""
    duplicated = ["    return None", ""]
    first = hunk_identity("pkg/app.py", duplicated, 0)
    second = hunk_identity("pkg/app.py", duplicated, 1)
    third = hunk_identity("pkg/app.py", duplicated, 2)
    assert len({first, second, third}) == 3
    for value in (first, second, third):
        assert_well_formed_id(value)


def test_the_id_is_stable_across_processes() -> None:
    """The id must survive a process boundary. The builtin hash is salted per process by
    PEP 456, so an id built on it would differ between the two child runs below; the
    ``hashlib.sha256`` the module actually uses does not. Both children are started with
    an EXPLICIT and different ``PYTHONHASHSEED``."""
    in_process = hunk_identity(CROSS_PROCESS_PATH, CROSS_PROCESS_LINES, CROSS_PROCESS_OCCURRENCE)
    assert_well_formed_id(in_process)

    program = (
        "from packages.orchestration.hunk_identity import hunk_identity\n"
        f"print(hunk_identity({CROSS_PROCESS_PATH!r}, {CROSS_PROCESS_LINES!r}, "
        f"{CROSS_PROCESS_OCCURRENCE!r}))\n"
    )

    printed = []
    for seed in HASH_SEEDS:
        env = dict(os.environ)
        env["PYTHONHASHSEED"] = seed
        proc = subprocess.run(
            [sys.executable, "-B", "-c", program],
            cwd=str(REPO_ROOT),
            env=env,
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, f"seed {seed} exited {proc.returncode}: {proc.stderr[-2000:]}"
        printed.append(proc.stdout.strip())

    assert printed[0] == printed[1], f"two hash seeds disagreed: {printed}"
    assert printed[0] == in_process, f"subprocess {printed[0]!r} != in-process {in_process!r}"


def test_a_lone_surrogate_cannot_be_encoded_strictly() -> None:
    """Pins WHY ``errors="replace"`` is in the module rather than decoration: the strict
    encode of a lone surrogate raises, so a hostile line would otherwise take the id
    function down. Measured, not assumed."""
    with pytest.raises(UnicodeEncodeError):
        "\ud800".encode()
    assert "\ud800".encode(errors="replace") == b"?"


def test_hostile_input_never_raises_and_still_returns_an_id() -> None:
    """Totality. Every case below must come back with a WELL-FORMED id — the claim is not
    merely that nothing raised, because a function returning ``None`` would satisfy that."""
    cases = {
        "empty iterable and empty path": ("", []),
        "empty iterable, real path": ("pkg/app.py", []),
        "lone surrogate in the path AND in a line": ("\ud800/app.py", ["\ud800", "ok"]),
        "a non-str line": ("pkg/app.py", [7, None, object()]),
        "a very long line": ("pkg/app.py", ["q" * 200_000]),
    }
    for label, (path, lines) in cases.items():
        value = hunk_identity(path, lines)
        assert_well_formed_id(value), label

    # ``occurrence`` has its own totality guard, because ``int()`` is what would raise.
    negative = hunk_identity("pkg/app.py", ["alpha"], -1)
    not_a_number = hunk_identity("pkg/app.py", ["alpha"], "x")
    missing = hunk_identity("pkg/app.py", ["alpha"], None)
    for value in (negative, not_a_number, missing):
        assert_well_formed_id(value)

    assert normalise_old_side([]) == ""


def test_the_id_shape_is_lowercase_hex_of_the_declared_length() -> None:
    """The shape consumers may rely on, pinned against the declared constant."""
    assert HUNK_ID_LENGTH == 16
    value = hunk_identity("a.py", ["x"])
    assert len(value) == HUNK_ID_LENGTH
    assert value == value.lower()
    assert set(value) <= _HEX_DIGITS
