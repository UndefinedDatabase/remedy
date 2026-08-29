"""Property tests for F033's hunk-decision RECORDER — the write door's effect.

One test per PROPERTY the recorder turns on, named for the property rather than for the
function that happens to implement it. The properties, in the order they appear below: a clean
decision writes exactly one record under the composed attempt key with every landing
``unattempted``, which is DECISION F033 D4 itself — recording a decision is not applying it; the
recorded rows carry the ledger's own four keys in the DIFF's order; a rejection reason survives
VERBATIM into the record; a second decision on the SAME attempt REPLACES the first; a decision on
a DIFFERENT attempt leaves the first record standing; a truncated view refuses and writes
NOTHING; a refusal from the decision core comes back UNCHANGED and writes NOTHING; unrelated
metadata keys survive; and the whole document round-trips through ``json.dumps`` with no custom
encoder.

THE VIEW DOOR'S OWN PROPERTIES, added when the recorder learned the viewer's envelope: an
envelope whose ``available`` is False refuses with ``HUNK_RECORD_REFUSAL_NO_DIFF``, QUOTES the
envelope's own ``reason`` so the operator learns which absence it was, and writes NOTHING; an
envelope that is BOTH unavailable and truncated answers the NO_DIFF code rather than the
untrustworthy one, because availability is decided first and an absent artifact was never cut
short; a view carrying NO ``available`` key at all is treated as available and records normally,
which is the RAW PARSER case and the discriminator that stops the ``True`` default being flipped;
a truncated but available envelope still refuses as untrustworthy; the two doors record the same
document for the same diff, built on two jobs and compared whole; and a nine-key envelope of the
shape ``diff_view_source.build_diff_view`` really returns records normally.

WHY the two write-nothing tests compare the metadata BEFORE and AFTER rather than merely
checking the return: the claim is that a refused decision leaves the operator's record untouched,
and only a before/after comparison witnesses that. They are also the discriminators for the
refusal tests — without them a recorder that refuses and writes anyway passes.

Diffs are built with ``difflib.unified_diff`` and the job the way
``tests/orchestration/test_hunk_apply.py`` builds them. Both recipes are RESTATED here rather
than imported: a test file that reaches into another test file's helpers couples two suites that
have no reason to move together."""

from __future__ import annotations

import copy
import difflib
import json
from datetime import datetime
from uuid import uuid4

from packages.core.models import Job, RunState
from packages.orchestration.diff_parser import (
    DIFF_VIEW_MAX_FILES,
    parse_unified_diff_to_view,
)
from packages.orchestration.hunk_approval import (
    REFUSAL_MISSING_REASON,
    REFUSAL_UNKNOWN_HUNK,
    HunkApprovalRefusal,
)
from packages.orchestration.hunk_decision_record import (
    HUNK_DECISIONS_METADATA_KEY,
    HUNK_RECORD_REFUSAL_NO_DIFF,
    HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW,
    HunkDecisionRecord,
    record_hunk_decision,
    record_hunk_decision_from_view,
)
from packages.orchestration.hunk_ledger import (
    HUNK_LANDING_UNATTEMPTED,
    HUNK_STATE_APPROVED,
    HUNK_STATE_REJECTED,
    export_hunk_ledger,
)

ORIGINAL = "\n".join(f"line {number:02d}" for number in range(1, 21)) + "\n"

#: An operator's reason with surrounding whitespace, so "verbatim" is a testable claim rather
#: than a description. T003 quotes this text into the next repair prompt.
REASON = "  the second edit is out of scope  "

#: A fixed clock, so ``decided_at`` is an assertable value rather than "some timestamp".
DECIDED_AT = datetime(2026, 8, 29, 12, 30, 45)


def _edited(*replacements: tuple[str, str]) -> str:
    """``ORIGINAL`` with each ``(old, new)`` whole line replaced."""
    text = ORIGINAL
    for old, new in replacements:
        text = text.replace(old + "\n", new + "\n")
    return text


def _diff_of(new_text: str, path: str) -> str:
    """A ``difflib`` unified diff carrying ``---``/``+++`` headers. Two well-separated edits
    give two hunks."""
    return "".join(
        difflib.unified_diff(
            ORIGINAL.splitlines(True), new_text.splitlines(True),
            fromfile=f"a/{path}", tofile=f"b/{path}",
        )
    )


TWO_HUNK_DIFF = _diff_of(
    _edited(("line 03", "line 03 CHANGED"), ("line 15", "line 15 CHANGED")), "f.txt"
)

#: The same real diff repeated past the parser's file ceiling, so the view really comes back
#: truncated. It is a REPEATED REAL DIFF rather than a hand-rolled string: the fixture must be
#: something the parser genuinely refuses to promise it showed in full.
TRUNCATED_DIFF = TWO_HUNK_DIFF * (DIFF_VIEW_MAX_FILES + 1)


def _ids(diff_text: str, file_index: int = 0) -> list[str]:
    """The hunk ids of one file of ``diff_text``, in the diff's own order."""
    return [h["id"] for h in parse_unified_diff_to_view(diff_text)["files"][file_index]["hunks"]]


HUNK_IDS = _ids(TWO_HUNK_DIFF)


def _job(**metadata: object) -> Job:
    """A job carrying ``metadata`` and nothing else. The recorder needs no capability and no
    intent — it writes no repository — so this is deliberately barer than the apply seam's."""
    return Job(
        id=uuid4(),
        name="hunk decision job",
        user_prompt="record the operator's hunk decision",
        state=RunState.RUNNING,
        tasks=[],
        artifacts=[],
        metadata=dict(metadata),
    )


def _record(job: Job, *, task_id: object = "t-1", attempt: object = 2,
            diff_text: str = TWO_HUNK_DIFF, approved=(), rejected=(),
            now: datetime = DECIDED_AT):
    """One call to the shipped TEXT entry point, with this suite's defaults."""
    return record_hunk_decision(
        job,
        task_id=task_id,
        attempt=attempt,
        attempt_diff_text=diff_text,
        approved=approved,
        rejected=rejected,
        now=now,
    )


def _record_from_view(job: Job, *, view, task_id: object = "t-1", attempt: object = 2,
                      approved=(), rejected=(), now: datetime = DECIDED_AT):
    """One call to the shipped VIEW entry point, with this suite's defaults."""
    return record_hunk_decision_from_view(
        job,
        task_id=task_id,
        attempt=attempt,
        attempt_view=view,
        approved=approved,
        rejected=rejected,
        now=now,
    )


#: The nine keys ``diff_view_source.build_diff_view`` really returns, measured at `624818e6`.
#: RESTATED here rather than imported for the same reason the diff and job recipes are: this
#: suite tests what the recorder accepts, and importing the producer would make the fixture move
#: whenever that module does, hiding exactly the drift this test exists to catch.
ENVELOPE_KEYS = [
    "available", "files", "reason", "scope", "source",
    "task_id", "task_run_ids", "truncated", "version",
]

#: Two of the three ``DIFF_REASON_*`` values, spelled out so the "quotes the envelope's own
#: reason" claim is checked against a real absence name rather than a placeholder.
REASON_NO_EVIDENCE_DIR = "evidence_dir_unavailable"
REASON_ARTIFACT_MISSING = "diff_artifact_missing"


def _envelope(diff_text: str = TWO_HUNK_DIFF, **overrides: object) -> dict:
    """A viewer envelope of ``build_diff_view``'s shape, built BY HAND over a real parse."""
    parsed = parse_unified_diff_to_view(diff_text)
    envelope = {
        "available": True,
        "files": parsed["files"],
        "reason": None,
        "scope": "job",
        "source": "workspace.diff",
        "task_id": None,
        "task_run_ids": [],
        "truncated": parsed["truncated"],
        "version": parsed["version"],
    }
    envelope.update(overrides)
    return envelope


def test_a_clean_decision_writes_one_record_under_the_composed_attempt_key_unattempted() -> None:
    # DECISION F033 D4 in one assertion: the door RECORDS and never applies, so every landing
    # is ``unattempted`` and not ``not_landed`` — no apply has run, which is a different fact
    # from one that ran and failed.
    job = _job()
    result = _record(job, approved=[HUNK_IDS[0]],
                     rejected=[{"id": HUNK_IDS[1], "reason": REASON}])
    assert isinstance(result, HunkDecisionRecord), result
    assert result.attempt_key == "t-1:2"
    records = job.metadata[HUNK_DECISIONS_METADATA_KEY]
    assert list(records) == ["t-1:2"]
    entry = records["t-1:2"]
    assert entry["task_id"] == "t-1"
    assert entry["attempt"] == "2"
    assert entry["decided_at"] == DECIDED_AT.isoformat()
    assert [row["landing"] for row in entry["hunks"]] == [HUNK_LANDING_UNATTEMPTED] * 2
    assert [row["state"] for row in entry["hunks"]] == [HUNK_STATE_APPROVED, HUNK_STATE_REJECTED]


def test_the_recorded_rows_carry_the_ledgers_four_keys_in_the_diffs_order() -> None:
    job = _job()
    # The operator names the SECOND hunk first, so a record echoing the decision's order rather
    # than the diff's would come out reversed.
    result = _record(job, approved=[HUNK_IDS[1], HUNK_IDS[0]])
    entry = job.metadata[HUNK_DECISIONS_METADATA_KEY][result.attempt_key]
    assert [row["id"] for row in entry["hunks"]] == HUNK_IDS
    for row in entry["hunks"]:
        assert list(row) == ["id", "state", "reason", "landing"]
    # The rows are the LEDGER's own, unwrapped — the shape is not doubled.
    assert entry["hunks"] == export_hunk_ledger(result.ledger)["hunks"]
    assert list(entry) == ["task_id", "attempt", "decided_at", "hunks"]


def test_a_rejection_reason_survives_verbatim_into_the_record() -> None:
    job = _job()
    result = _record(job, approved=[HUNK_IDS[0]],
                     rejected=[{"id": HUNK_IDS[1], "reason": REASON}])
    entry = job.metadata[HUNK_DECISIONS_METADATA_KEY][result.attempt_key]
    assert [row["reason"] for row in entry["hunks"]] == ["", REASON]


def test_a_second_decision_on_the_same_attempt_replaces_the_first() -> None:
    # An operator may revise a decision while the landing is still ``unattempted``, and two
    # records for one attempt would leave the viewer choosing between them.
    job = _job()
    _record(job, approved=[HUNK_IDS[0]])
    second = _record(job, approved=[HUNK_IDS[1]])
    records = job.metadata[HUNK_DECISIONS_METADATA_KEY]
    assert list(records) == ["t-1:2"]
    assert len(records) == 1
    assert [row["state"] for row in records[second.attempt_key]["hunks"]] == [
        "pending",
        HUNK_STATE_APPROVED,
    ]


def test_a_decision_on_a_different_attempt_leaves_the_first_record_standing() -> None:
    job = _job()
    first = _record(job, attempt=1, approved=[HUNK_IDS[0]])
    second = _record(job, attempt=2, approved=[HUNK_IDS[1]])
    records = job.metadata[HUNK_DECISIONS_METADATA_KEY]
    assert sorted(records) == ["t-1:1", "t-1:2"]
    assert first.attempt_key != second.attempt_key
    assert [row["state"] for row in records[first.attempt_key]["hunks"]] == [
        HUNK_STATE_APPROVED,
        "pending",
    ]


def test_a_truncated_view_refuses_and_writes_nothing() -> None:
    assert parse_unified_diff_to_view(TRUNCATED_DIFF)["truncated"] is True
    job = _job(existing="value")
    before = copy.deepcopy(job.metadata)
    result = _record(job, diff_text=TRUNCATED_DIFF, approved=[HUNK_IDS[0]])
    assert isinstance(result, HunkApprovalRefusal), result
    assert result.code == HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW
    assert result.hunk_ids == ()
    assert result.message
    assert job.metadata == before
    assert HUNK_DECISIONS_METADATA_KEY not in job.metadata


def test_a_decision_refusal_is_returned_unchanged_and_writes_nothing() -> None:
    job = _job()
    before = copy.deepcopy(job.metadata)
    unknown = _record(job, approved=["not-a-hunk-of-this-attempt"])
    assert isinstance(unknown, HunkApprovalRefusal), unknown
    # The decision core's OWN code, message and offending ids, intact — this module mints no
    # second vocabulary for a fault that already has one.
    assert unknown.code == REFUSAL_UNKNOWN_HUNK
    assert unknown.hunk_ids == ("not-a-hunk-of-this-attempt",)
    assert "not-a-hunk-of-this-attempt" in unknown.message
    unreasoned = _record(job, rejected=[{"id": HUNK_IDS[0], "reason": "   "}])
    assert isinstance(unreasoned, HunkApprovalRefusal), unreasoned
    assert unreasoned.code == REFUSAL_MISSING_REASON
    assert unreasoned.hunk_ids == (HUNK_IDS[0],)
    assert job.metadata == before


def test_unrelated_metadata_keys_survive_the_recording() -> None:
    job = _job(permissions={"repo_generated_write": "allow"}, note="untouched")
    _record(job, approved=[HUNK_IDS[0]])
    assert job.metadata["permissions"] == {"repo_generated_write": "allow"}
    assert job.metadata["note"] == "untouched"
    assert HUNK_DECISIONS_METADATA_KEY in job.metadata


def test_the_whole_recorded_document_survives_json_dumps_without_a_custom_encoder() -> None:
    job = _job()
    # A ``UUID`` task id is the realistic case and the one that would need an encoder if the
    # record kept the object instead of its text.
    task_id = uuid4()
    result = _record(job, task_id=task_id, approved=[HUNK_IDS[0]],
                     rejected=[{"id": HUNK_IDS[1], "reason": REASON}])
    assert result.attempt_key == f"{task_id}:2"
    document = job.metadata[HUNK_DECISIONS_METADATA_KEY]
    assert json.loads(json.dumps(document)) == document
    assert result.exported is document[result.attempt_key]


def test_an_unavailable_envelope_refuses_with_no_diff_quoting_its_reason_and_writes_nothing(
) -> None:
    # An unavailable envelope has an EMPTY ``files`` list, so without this refusal every approved
    # id would be unknown and the operator would be told their IDS are wrong when the truth is
    # that the ARTIFACT is missing.
    job = _job(existing="value")
    before = copy.deepcopy(job.metadata)
    view = _envelope(available=False, reason=REASON_NO_EVIDENCE_DIR, files=[], source=None)
    result = _record_from_view(job, view=view, approved=[HUNK_IDS[0]])
    assert isinstance(result, HunkApprovalRefusal), result
    assert result.code == HUNK_RECORD_REFUSAL_NO_DIFF
    assert result.hunk_ids == ()
    # The envelope's OWN reason, so the operator learns WHICH absence it was.
    assert REASON_NO_EVIDENCE_DIR in result.message
    assert job.metadata == before
    assert HUNK_DECISIONS_METADATA_KEY not in job.metadata


def test_an_unavailable_and_truncated_envelope_answers_no_diff_not_untrustworthy() -> None:
    # Availability is decided FIRST: an absent artifact was never cut short, so "there is no
    # diff" is the true answer and "the diff we showed you was incomplete" is not.
    view = _envelope(TRUNCATED_DIFF, available=False, reason=REASON_ARTIFACT_MISSING, files=[])
    assert view["available"] is False
    assert view["truncated"] is True
    job = _job()
    result = _record_from_view(job, view=view, approved=[HUNK_IDS[0]])
    assert isinstance(result, HunkApprovalRefusal), result
    assert result.code == HUNK_RECORD_REFUSAL_NO_DIFF
    assert result.code != HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW
    assert REASON_ARTIFACT_MISSING in result.message
    assert HUNK_DECISIONS_METADATA_KEY not in job.metadata


def test_a_view_with_no_available_key_is_treated_as_available_and_records_normally() -> None:
    # THE RAW PARSER CASE, and the discriminator that stops the ``True`` default being flipped:
    # ``parse_unified_diff_to_view`` emits no ``available`` key at all, because text that exists
    # IS available, so a caller handing over a bare parse must not be refused for a key that
    # parser never emits.
    view = parse_unified_diff_to_view(TWO_HUNK_DIFF)
    assert "available" not in view
    job = _job()
    result = _record_from_view(job, view=view, approved=[HUNK_IDS[0]])
    assert isinstance(result, HunkDecisionRecord), result
    entry = job.metadata[HUNK_DECISIONS_METADATA_KEY][result.attempt_key]
    assert [row["id"] for row in entry["hunks"]] == HUNK_IDS
    assert [row["state"] for row in entry["hunks"]] == [HUNK_STATE_APPROVED, "pending"]


def test_a_truncated_but_available_envelope_still_refuses_as_untrustworthy() -> None:
    view = _envelope(TRUNCATED_DIFF)
    assert view["available"] is True
    assert view["truncated"] is True
    job = _job(existing="value")
    before = copy.deepcopy(job.metadata)
    result = _record_from_view(job, view=view, approved=[HUNK_IDS[0]])
    assert isinstance(result, HunkApprovalRefusal), result
    assert result.code == HUNK_RECORD_REFUSAL_UNTRUSTWORTHY_VIEW
    assert result.hunk_ids == ()
    assert job.metadata == before


def test_both_doors_record_the_same_document_for_the_same_diff() -> None:
    # ONE implementation, two doors — which is the whole reason the view entry point exists. Two
    # jobs so neither call can see the other's record.
    text_job, view_job = _job(), _job()
    via_text = _record(text_job, approved=[HUNK_IDS[0]],
                       rejected=[{"id": HUNK_IDS[1], "reason": REASON}])
    via_view = _record_from_view(view_job, view=parse_unified_diff_to_view(TWO_HUNK_DIFF),
                                 approved=[HUNK_IDS[0]],
                                 rejected=[{"id": HUNK_IDS[1], "reason": REASON}])
    assert isinstance(via_text, HunkDecisionRecord), via_text
    assert isinstance(via_view, HunkDecisionRecord), via_view
    assert via_text.attempt_key == via_view.attempt_key
    assert via_text.exported == via_view.exported
    assert (text_job.metadata[HUNK_DECISIONS_METADATA_KEY]
            == view_job.metadata[HUNK_DECISIONS_METADATA_KEY])


def test_a_nine_key_viewer_envelope_records_normally() -> None:
    view = _envelope()
    assert sorted(view) == ENVELOPE_KEYS
    job = _job()
    result = _record_from_view(job, view=view, approved=[HUNK_IDS[0]],
                               rejected=[{"id": HUNK_IDS[1], "reason": REASON}])
    assert isinstance(result, HunkDecisionRecord), result
    entry = job.metadata[HUNK_DECISIONS_METADATA_KEY][result.attempt_key]
    assert [row["id"] for row in entry["hunks"]] == HUNK_IDS
    assert [row["state"] for row in entry["hunks"]] == [HUNK_STATE_APPROVED, HUNK_STATE_REJECTED]
    assert [row["landing"] for row in entry["hunks"]] == [HUNK_LANDING_UNATTEMPTED] * 2
    assert [row["reason"] for row in entry["hunks"]] == ["", REASON]
