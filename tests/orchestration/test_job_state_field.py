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

import pytest

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


class TestTheRetypeIsComplete:
    """F272 move three — the guards round 13 measured as MISSING.

    Round 10's rendering guard cannot see a missing ``.value`` at the record
    boundary: a ``RunState`` member equals, formats and JSON-serialises exactly
    like its value, so that guard's three assertions are all TRUE for a bare
    member. Only its TYPE tells them apart, which is what the first test reads.
    """

    def test_the_exported_status_is_a_plain_str_and_not_a_run_state(self):
        """The discriminator. A bare ``RunState`` passes every other guard."""
        job = JobPlan(job_id="j1", state=JOB_BLOCKED)
        assert type(_export_job(job)["status"]) is str

    def test_every_construction_path_settles_as_a_run_state(self):
        """One spelling per concept: a raw literal, a JOB_* constant and an
        imported record reach the same type, or the annotation is a lie."""
        assert type(JobPlan(state="completed").state).__name__ == "RunState"
        assert type(JobPlan(state=JOB_BLOCKED).state).__name__ == "RunState"
        assert type(_import_job({"job_id": "j1", "status": "blocked"}).state).__name__ == "RunState"

    def test_a_record_whose_status_is_not_a_run_state_value_still_loads(self):
        """DECISION F272 D5. ``complete``, ``dry_run`` and ``promoted`` occur in
        records on disk; an unrecognised value is KEPT, never raised on."""
        job = _import_job({"job_id": "j1", "status": "complete"})
        assert job.state == "complete"
        assert _export_job(job)["status"] == "complete"


class TestTheRenameLeftNoSilentReaderBehind:
    """The two production guards a ``getattr(job, "status", <default>)`` broke.

    DECISION F272 D7's raising-property probe cannot see these: a string-named
    read with a default answers with the default instead of raising, so the
    probe stayed green while both guards stopped working. The class-wide scan
    lives in ``test_job_plan_state_reads.py``; these two pin the BEHAVIOUR,
    because a scan proves a spelling is absent and never that a guard fires.
    """

    def _isolated_data_root(self, tmp_path, monkeypatch):
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    def test_budget_flags_are_refused_on_a_stopped_job(self, tmp_path, monkeypatch, capsys):
        """F018: raw budget flags must not silently override a stopped job's
        limits. With the retired read the test was ``"" == "stopped"``, so the
        refusal never fired and the job re-ran under the new limits."""
        from apps.cli.commands.do_cmd import _cmd_do_job_run
        from packages.orchestration.pingpong_job import save_job_plan

        self._isolated_data_root(tmp_path, monkeypatch)
        save_job_plan(JobPlan(job_id="0123456789abcdef", state="stopped"))

        with pytest.raises(SystemExit) as exc:
            _cmd_do_job_run("0123456789abcdef", max_cost_usd="5.0")

        assert exc.value.code == 2
        assert "budget limits cannot be changed" in capsys.readouterr().err

    def test_a_linked_job_that_loads_reports_its_real_state(self, tmp_path, monkeypatch):
        """``_linked_job_summary`` reserves ``unknown`` for a job it could not
        load. With the retired read every linked job read ``unknown`` while the
        same summary reported that the job WAS available."""
        from packages.orchestration.job_evidence import _linked_job_summary
        from packages.orchestration.pingpong_job import save_job_plan

        self._isolated_data_root(tmp_path, monkeypatch)
        save_job_plan(JobPlan(job_id="0123456789abcdee", state="completed"))

        summary = _linked_job_summary("0123456789abcdee")

        assert summary["status"] == "completed", summary
        assert summary["source"] != "unavailable", summary
