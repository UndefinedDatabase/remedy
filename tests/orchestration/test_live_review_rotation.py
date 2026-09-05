"""amend0905-throughput 2c — tests for ``scripts/rotate_live_review.py``.

Every test drives the script through ``main`` against synthetic ledger and
STATUS files under ``tmp_path`` and asserts on the BYTES read back from disk,
never on a return value alone. The load-bearing tests are
:func:`test_moved_records_reappear_byte_identical_and_leave_the_ledger` (the
byte-identity contract) and the two refusal tests, which pin that a corrupted
archive write or a lying digest leaves both files untouched.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import pytest

from scripts import rotate_live_review as rot

PREAMBLE = (
    "# Live Review — F900 Synthetic feature\n"
    "\n"
    "> Round-by-round review record for the synthetic branch, reset at the claim.\n"
    "> Second blockquote line of the preamble.\n"
    "\n"
    "## Steps\n"
    "\n"
    "R1 claim the feature → R2 build it → R3 close it.\n"
    "\n"
    "## Findings\n"
)

OPEN_FINDING = (
    "- R-0001 — Low, AN OPEN FINDING THAT STAYS. Raised at R1 by the reviewer.\n"
    "wrapped continuation line of the open finding at column 0."
)
OPEN_FINDING_2 = "- R-0004 — Medium, A SECOND OPEN FINDING THAT STAYS. Raised at R2."
RESOLVED_REG = (
    "- R-0002 — Medium, A RESOLVED FINDING WHOSE PAIR MOVES. Raised at R1.\n"
    "\n"
    "  FIX: the indented fix paragraph belongs to the registration record."
)
RESOLVED_DONE = "Done: R-0002 — RESOLVED at R3 by commit abc1234; the fix paragraph above describes it."
TWICE_REG = "- R-0003 — Low, AN ID WITH TWO DONE RECORDS STAYS IN PLACE."
TWICE_DONE_1 = "Done: R-0003 — first resolution, recorded at R2."
TWICE_DONE_2 = "Done: R-0003 — second resolution, recorded again at R3."
LANDED = "Landed: R-0001 — the fix landed at def5678 (unreviewed), stays."
RECURRENCE = (
    "Recurrence: R-0001 — the defect reappeared at R4.\n"
    "Second line of the recurrence paragraph, also stays."
)
GATE_FORM_ONE = (
    "Gate: F900 R1 — THE CLAIM ROUND. VERDICT PASS. Header form one.\n"
    "wrapped continuation line of the gate record."
)
GATE_FORM_TWO = "Gate: R2 — the F900 R2 entry — VERDICT PASS. Header form two."
GATE_OPEN_FEATURE = "Gate: F901 R1 — A GATE OF A FEATURE STILL OPEN. VERDICT PASS. Stays."
DECISION = "DECISION F900 D1 — a decision paragraph that stays where it is."

STATUS_F900_CLOSED = (
    "# Roadmap status\n"
    "\n"
    "- [x] F900 — Synthetic feature (accepted 2026-09-05)\n"
    "- [ ] F901 — Still open\n"
)
STATUS_BOTH_CLOSED = STATUS_F900_CLOSED.replace("- [ ] F901 — Still open", "- [x] F901 — Still open")

DEFAULT_RECORDS = [
    OPEN_FINDING,
    RESOLVED_REG,
    RESOLVED_DONE,
    TWICE_REG,
    TWICE_DONE_1,
    TWICE_DONE_2,
    OPEN_FINDING_2,
    LANDED,
    RECURRENCE,
    GATE_FORM_ONE,
    GATE_FORM_TWO,
    GATE_OPEN_FEATURE,
    DECISION,
]


def _ledger_text(records: list[str] | None = None) -> str:
    return PREAMBLE + "\n" + "\n\n".join(DEFAULT_RECORDS if records is None else records)


def _write(tmp_path: Path, ledger: str, status: str = STATUS_F900_CLOSED) -> tuple[Path, Path, Path]:
    ledger_path = tmp_path / "live_review.md"
    status_path = tmp_path / "STATUS.md"
    archive_path = tmp_path / "live_review_archive.md"
    ledger_path.write_bytes(ledger.encode("utf-8"))
    status_path.write_bytes(status.encode("utf-8"))
    return ledger_path, status_path, archive_path


def _run(ledger: Path, status: Path, archive: Path, *extra: str) -> int:
    return rot.main(["--ledger", str(ledger), "--status", str(status), "--archive", str(archive), *extra])


def _open_count(data: bytes) -> int:
    text = data.decode("utf-8")
    return len(re.findall(r"^- R-\d{4} — ", text, re.M)) - len(re.findall(r"^Done: R-\d{4} — ", text, re.M))


def test_moved_records_reappear_byte_identical_and_leave_the_ledger(tmp_path: Path) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())

    assert _run(ledger, status, archive) == 0

    ledger_bytes = ledger.read_bytes()
    archive_bytes = archive.read_bytes()
    for moved in (GATE_FORM_ONE, GATE_FORM_TWO, RESOLVED_REG, RESOLVED_DONE):
        encoded = moved.encode("utf-8")
        assert archive_bytes.count(encoded) == 1
        assert encoded not in ledger_bytes
        # byte-identical: the archive slice at the record's position hashes like the fixture
        start = archive_bytes.index(encoded)
        assert hashlib.sha256(archive_bytes[start:start + len(encoded)]).hexdigest() == hashlib.sha256(encoded).hexdigest()
    # archive records are separated by exactly one blank line, in ledger order
    expected_tail = "\n" + "\n\n".join([RESOLVED_REG, RESOLVED_DONE, GATE_FORM_ONE, GATE_FORM_TWO]) + "\n"
    assert archive_bytes.endswith(expected_tail.encode("utf-8"))
    assert archive_bytes.startswith(rot.ARCHIVE_HEADER.encode("utf-8"))


def test_non_movable_records_stay_in_place(tmp_path: Path) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())

    assert _run(ledger, status, archive) == 0

    ledger_bytes = ledger.read_bytes()
    archive_bytes = archive.read_bytes()
    for stays in (
        GATE_OPEN_FEATURE,
        OPEN_FINDING,
        OPEN_FINDING_2,
        LANDED,
        RECURRENCE,
        TWICE_REG,
        TWICE_DONE_1,
        TWICE_DONE_2,
        DECISION,
        PREAMBLE,
    ):
        assert stays.encode("utf-8") in ledger_bytes
        assert stays.encode("utf-8") not in archive_bytes
    remaining = [
        OPEN_FINDING,
        TWICE_REG,
        TWICE_DONE_1,
        TWICE_DONE_2,
        OPEN_FINDING_2,
        LANDED,
        RECURRENCE,
        GATE_OPEN_FEATURE,
        DECISION,
    ]
    assert ledger_bytes == _ledger_text(remaining).encode("utf-8")


def test_open_findings_count_is_identical_before_and_after(tmp_path: Path) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())
    before = _open_count(ledger.read_bytes())
    assert before == 4 - 3  # four registrations, three Done lines

    assert _run(ledger, status, archive) == 0

    assert _open_count(ledger.read_bytes()) == before
    assert _open_count(ledger.read_bytes() + b"\n" + archive.read_bytes()) == before


def test_archive_is_append_only_across_a_second_rotation(tmp_path: Path) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())
    assert _run(ledger, status, archive) == 0
    first_archive = archive.read_bytes()
    first_ledger = ledger.read_bytes()

    status.write_bytes(STATUS_BOTH_CLOSED.encode("utf-8"))
    assert _run(ledger, status, archive) == 0

    second_archive = archive.read_bytes()
    assert second_archive.startswith(first_archive)
    assert second_archive == first_archive + ("\n" + GATE_OPEN_FEATURE + "\n").encode("utf-8")
    assert GATE_OPEN_FEATURE.encode("utf-8") not in ledger.read_bytes()
    assert ledger.read_bytes() == first_ledger.replace(("\n\n" + GATE_OPEN_FEATURE).encode("utf-8"), b"")


def test_second_run_with_nothing_new_moves_nothing_and_changes_no_byte(tmp_path: Path, capsys) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())
    assert _run(ledger, status, archive) == 0
    ledger_before = ledger.read_bytes()
    archive_before = archive.read_bytes()
    ledger_mtime = ledger.stat().st_mtime_ns
    archive_mtime = archive.stat().st_mtime_ns
    capsys.readouterr()

    assert _run(ledger, status, archive) == 0

    out = capsys.readouterr().out
    assert "gate records moved: 0" in out
    assert "finding pairs moved: 0 (0 records)" in out
    assert "nothing to move; no byte changed" in out
    assert ledger.read_bytes() == ledger_before
    assert archive.read_bytes() == archive_before
    assert ledger.stat().st_mtime_ns == ledger_mtime
    assert archive.stat().st_mtime_ns == archive_mtime


def test_refuses_and_writes_nothing_when_the_archive_writer_drops_a_byte(tmp_path: Path, monkeypatch, capsys) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())
    original_ledger = ledger.read_bytes()
    real_append = rot.append_to_archive

    def lossy_append(old_archive: str, bodies: list[str]) -> str:
        out = real_append(old_archive, bodies)
        return out[:-2] + out[-1:]  # drop the last byte of the last appended record

    monkeypatch.setattr(rot, "append_to_archive", lossy_append)

    assert _run(ledger, status, archive) == 2

    assert "REFUSED, nothing written" in capsys.readouterr().err
    assert ledger.read_bytes() == original_ledger
    assert not archive.exists()
    with pytest.raises(rot.RotationError):
        rot.rotate(original_ledger.decode("utf-8"), STATUS_F900_CLOSED, None)


def test_refuses_and_writes_nothing_when_the_ledger_digest_lies(tmp_path: Path, monkeypatch, capsys) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())
    original_ledger = ledger.read_bytes()

    def lying_digest(body: str) -> str:
        return hashlib.sha256((body + "x").encode("utf-8")).hexdigest()

    monkeypatch.setattr(rot, "record_digest", lying_digest)

    assert _run(ledger, status, archive) == 2

    assert "sha256 mismatch" in capsys.readouterr().err
    assert ledger.read_bytes() == original_ledger
    assert not archive.exists()
    with pytest.raises(rot.RotationError, match="sha256"):
        rot.rotate(original_ledger.decode("utf-8"), STATUS_F900_CLOSED, None)


def test_dry_run_prints_the_sizes_and_writes_nothing(tmp_path: Path, capsys) -> None:
    ledger, status, archive = _write(tmp_path, _ledger_text())
    original_ledger = ledger.read_bytes()
    ledger_mtime = ledger.stat().st_mtime_ns

    assert _run(ledger, status, archive, "--dry-run") == 0

    out = capsys.readouterr().out
    assert f"old ledger size: {len(original_ledger)} bytes" in out
    assert re.search(r"^new ledger size: \d+ bytes$", out, re.M)
    assert "old archive size: 0 bytes" in out
    assert re.search(r"^new archive size: \d+ bytes$", out, re.M)
    assert "gate records moved: 2" in out
    assert "finding pairs moved: 1 (2 records)" in out
    assert "open findings before: 1" in out and "open findings after: 1" in out
    assert "dry run; nothing written" in out
    assert ledger.read_bytes() == original_ledger
    assert ledger.stat().st_mtime_ns == ledger_mtime
    assert not archive.exists()


def test_a_gate_glued_to_the_previous_record_with_one_newline_moves_cleanly(tmp_path: Path) -> None:
    glued_gate = "Gate: F900 R7 — A GATE GLUED TO THE RECORD ABOVE WITH ONE NEWLINE. VERDICT PASS."
    ledger_text = (
        PREAMBLE
        + "\n"
        + OPEN_FINDING
        + "\n\n"
        + RESOLVED_REG
        + "\n\n"
        + RESOLVED_DONE
        + "\n"
        + glued_gate
        + "\n\n"
        + DECISION
        + "\n"
        + GATE_FORM_TWO
        + "\n\n"
        + OPEN_FINDING_2
    )
    ledger, status, archive = _write(tmp_path, ledger_text)

    assert _run(ledger, status, archive) == 0

    ledger_bytes = ledger.read_bytes()
    assert ledger_bytes == (PREAMBLE + "\n" + OPEN_FINDING + "\n\n" + DECISION + "\n\n" + OPEN_FINDING_2).encode("utf-8")
    assert b"\n\n\n" not in ledger_bytes
    archive_tail = "\n" + "\n\n".join([RESOLVED_REG, RESOLVED_DONE, glued_gate, GATE_FORM_TWO]) + "\n"
    assert archive.read_bytes() == (rot.ARCHIVE_HEADER + archive_tail).encode("utf-8")


def test_a_wrapped_line_matching_a_preamble_pattern_does_not_split_its_record(tmp_path: Path) -> None:
    wrapped_reg = (
        "- R-0005 — Medium, A RESOLVED FINDING WHOSE WRAPPED LINE STARTS LIKE A STEPS LINE.\n"
        "R13 migration, against pre-existing code and not against any round; and the next line is marked\n"
        "LANDED. But a Landed line is an unreviewed fix, so the paragraph continues here."
    )
    wrapped_done = "Done: R-0005 — RESOLVED at R3; the whole registration above moves with this line."
    ledger, status, archive = _write(tmp_path, _ledger_text([OPEN_FINDING, wrapped_reg, wrapped_done, DECISION]))

    assert _run(ledger, status, archive) == 0

    assert ledger.read_bytes() == _ledger_text([OPEN_FINDING, DECISION]).encode("utf-8")
    assert archive.read_bytes() == (rot.ARCHIVE_HEADER + "\n" + wrapped_reg + "\n\n" + wrapped_done + "\n").encode("utf-8")
