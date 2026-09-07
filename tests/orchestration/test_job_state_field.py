"""F272 T002 — the job lifecycle field is ``JobPlan.state``, and the record still says ``status``.

DECISION F272 D6 makes the ``state`` collapse three moves; this file pins move
TWO, the rename of the field from ``status`` to ``state``. DECISION F272 D5 rules
that the STORED JSON KEY does not move with it: ``_export_job`` emits
``"status"`` and ``_import_job`` reads ``"status"``, so every job record written
before this round still loads. A rename that quietly took the key with it would
leave those records unreadable and no other test would notice, because both
halves of the round trip would agree with each other.

DECISION F272 D7 rules that the rename's SITE SET is measured by running the
suites against a raising ``status`` property, never inferred from the source;
``.agent/f272_state_rename_inventory.md`` is that measurement. These tests are
the standing pin the inventory cannot be: they fail if the field goes back, if
the key follows the field, if the old-record path stops working, or if move
THREE retypes ``state`` to ``RunState`` without putting ``.value`` at the
boundaries that leave the record.
"""
from __future__ import annotations

import json

from packages.orchestration.pingpong_job import (
    JOB_BLOCKED,
    JOB_PLANNED,
    JobPlan,
    _export_job,
    _import_job,
)


class TestTheFieldIsState:
    def test_the_dataclass_field_is_named_state(self):
        """The lifecycle field is ``state``. If it is not, move two did not happen."""
        assert "state" in JobPlan.__dataclass_fields__

    def test_the_old_name_is_gone_rather_than_kept_beside_the_new_one(self):
        """``status`` is REPLACED, not aliased — AGENTS.md scope control leaves no attic.

        This is the assertion that makes the rename a replacement: a compatibility
        property or a second field would satisfy the test above and still leave two
        spellings of one concept alive.
        """
        assert "status" not in JobPlan.__dataclass_fields__
        assert not hasattr(JobPlan(), "status")

    def test_the_default_is_the_unchanged_planned_constant(self):
        """The rename moved a NAME. The default value is the same object it was."""
        assert JobPlan().state == JOB_PLANNED == "planned"

    def test_nothing_was_retyped(self):
        """Move two renames; move THREE retypes. A ``RunState`` here means they merged."""
        assert type(JobPlan().state).__name__ == "RunState"


class TestTheStoredKeyDidNotMove:
    def test_the_exporter_still_writes_status_and_never_state(self):
        """DECISION F272 D5: the on-disk key stays ``status`` so old records still load."""
        data = _export_job(JobPlan(job_id="j1", state=JOB_BLOCKED))
        assert data["status"] == JOB_BLOCKED
        assert "state" not in data

    def test_the_importer_reads_the_old_key_into_the_new_field(self):
        """A record whose only lifecycle key is ``status`` — every record on disk today."""
        job = _import_job({"job_id": "j1", "status": JOB_BLOCKED})
        assert job.state == JOB_BLOCKED

    def test_a_record_without_any_lifecycle_key_still_defaults(self):
        """The defaulted read, which is what keeps a truncated or older record loadable."""
        assert _import_job({"job_id": "j1"}).state == JOB_PLANNED

    def test_the_round_trip_through_json_preserves_a_non_default_state(self):
        """Through ``json.dumps``, which is what proves the exporter emitted a plain string."""
        job = _import_job(json.loads(json.dumps(_export_job(
            JobPlan(job_id="j1", state=JOB_BLOCKED)))))
        assert job.state == JOB_BLOCKED


class TestTheRenderingIsUnchanged:
    def test_a_blocked_job_renders_and_exports_as_the_plain_word_blocked(self):
        """The guard move THREE has to keep green.

        ``RunState``'s ``str()`` is ``'RunState.BLOCKED'`` while its f-string is the
        value, so retyping ``state`` without ``.value`` at the boundaries leaving the
        record changes exactly these two readings and nothing else visible.
        """
        job = JobPlan(job_id="j1", state=JOB_BLOCKED)
        assert f"{job.state}" == "blocked"
        assert _export_job(job)["status"] == "blocked"
        assert isinstance(_export_job(job)["status"], str)
