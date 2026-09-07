"""F272 T002 — the eight administrative fields ``JobPlan`` had no counterpart for.

DECISION F260 D1 names eleven administrative fields for the ONE job record.
Three of them already had a spelling — ``id`` is ``job_id``, ``name`` is
``job_title``, ``state`` collides with ``status`` — and the other eight are
these: ``mission``, ``user_prompt``, ``project_id``, ``intake``,
``flight_plan``, ``artifacts``, ``budget`` and ``fences``.

``_export_job`` and ``_import_job`` are explicit field-by-field functions with
no ``asdict`` and no ``**data`` splat, so a field added to the dataclass and to
neither of them is a Python-only attribute that VANISHES on the first
persist/resume cycle. These tests therefore pin the defaults, the whole round
trip THROUGH ``json.dumps`` (which is what proves the exporter emitted
JSON-serialisable data rather than model objects), the defaulted read that keeps
records written before this round loadable, and the real writer and reader.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.core.models import Artifact, ArtifactKind, Budget, JobFences
from packages.orchestration.pingpong_job import (
    JobPlan,
    _export_job,
    _import_job,
    load_job_plan,
    save_job_plan,
)

# The eight, in the order the dataclass and both writers spell them.
ADMINISTRATIVE_FIELDS = (
    "mission",
    "user_prompt",
    "project_id",
    "intake",
    "flight_plan",
    "artifacts",
    "budget",
    "fences",
)


def _populated_plan() -> tuple[JobPlan, dict]:
    """A JobPlan with all eight set to distinguishable non-default values."""
    values = {
        "mission": "finish the one world record",
        "user_prompt": "make the job carry its own mission",
        "project_id": "proj-f272-t002",
        "intake": {"source": "cli", "answers": ["a", "b"]},
        "flight_plan": {"steps": ["plan", "build", "review"], "version": 3},
        "artifacts": [
            Artifact(
                name="plan.md",
                content="# the plan",
                kind=ArtifactKind.UNKNOWN,
            )
        ],
        "budget": Budget(max_tokens=4242, max_cost_usd=1.5, max_steps=7),
        "fences": JobFences(allow=["packages/**"], deny=["secrets/**"]),
    }
    return JobPlan(**values), values


class TestAdministrativeFieldDefaults:
    """The declared defaults, and the mutable one's factory."""

    def test_the_eight_have_their_documented_defaults(self):
        """A bare JobPlan starts with every administrative field ABSENT.

        Breaks if someone gives one of them a truthy default, which would write
        invented content into every job record ever persisted.
        """
        job = JobPlan()
        assert job.mission == ""
        assert job.user_prompt == ""
        assert job.project_id == ""
        assert job.intake is None
        assert job.flight_plan is None
        assert job.artifacts == []
        assert job.budget is None
        assert job.fences is None

    def test_artifacts_is_a_factory_and_never_shared(self):
        """The one mutable default must come from a ``default_factory``.

        Breaks if ``artifacts`` is ever spelled ``= []``, which would make every
        JobPlan in the process append into ONE shared list.
        """
        first = JobPlan()
        second = JobPlan()
        assert first.artifacts is not second.artifacts
        first.artifacts.append(
            Artifact(name="x.md", content="x", kind=ArtifactKind.UNKNOWN)
        )
        assert second.artifacts == []


class TestAdministrativeFieldRoundTrip:
    """Export, through real JSON, and back — the persist/resume cycle."""

    def test_all_eight_survive_a_json_round_trip(self):
        """Each of the eight survives ``_export_job`` -> json -> ``_import_job``.

        The json.dumps/loads pair is REQUIRED and not decoration: it is what
        proves the exporter emitted JSON-serialisable data rather than Pydantic
        model objects, which ``_persist_job`` could never write. Breaks the
        moment a field is added to the dataclass but to neither writer.
        """
        plan, values = _populated_plan()
        back = _import_job(json.loads(json.dumps(_export_job(plan))))
        assert back.mission == values["mission"]
        assert back.user_prompt == values["user_prompt"]
        assert back.project_id == values["project_id"]
        assert back.intake == values["intake"]
        assert back.flight_plan == values["flight_plan"]
        assert back.artifacts == values["artifacts"]
        assert back.budget == values["budget"]
        assert back.fences == values["fences"]

    def test_the_exporter_emits_plain_json_data_not_model_objects(self):
        """The three model-valued fields leave ``_export_job`` as plain data.

        Breaks if a future edit passes the model object straight through, which
        raises deep inside ``json.dumps`` in ``_persist_job`` rather than here.
        """
        plan, _ = _populated_plan()
        exported = _export_job(plan)
        assert isinstance(exported["artifacts"], list)
        assert all(isinstance(a, dict) for a in exported["artifacts"])
        assert isinstance(exported["budget"], dict)
        assert isinstance(exported["fences"], dict)
        json.dumps(exported)


class TestAdministrativeFieldDefaultedRead:
    """The old-record path: a job record written before these keys existed."""

    def test_a_record_carrying_only_the_required_key_reads_defaults(self):
        """``_import_job`` over the minimal old record defaults all eight.

        Breaks if any import stops reading through a default, which would raise
        a KeyError on every job record written before F272 T002.
        """
        bare = JobPlan()
        imported = _import_job({"job_id": "0123456789abcdef"})
        for name in ADMINISTRATIVE_FIELDS:
            assert getattr(imported, name) == getattr(bare, name), name

    def test_a_full_old_record_without_the_eight_keys_reads_defaults(self):
        """A COMPLETE record with all pre-existing keys and none of the eight.

        The previous test proves the minimal case; this one proves the realistic
        one, where every other key is present and only the new keys are missing.
        """
        bare = JobPlan()
        record = _export_job(JobPlan(job_id="0123456789abcdef", job_title="old"))
        for name in ADMINISTRATIVE_FIELDS:
            record.pop(name)
        imported = _import_job(json.loads(json.dumps(record)))
        for name in ADMINISTRATIVE_FIELDS:
            assert getattr(imported, name) == getattr(bare, name), name

    def test_job_id_stays_the_one_required_key(self):
        """``_import_job({})`` raises KeyError('job_id') — unchanged by F272 T002.

        Pinned because the round's own gate G4(iii) asked for ``_import_job({})``
        to return, and it does not: ``job_id=data["job_id"]`` has been a required
        read since long before this round, measured identically at the base
        commit df955058. This test records the measured truth so the next reader
        does not mistake it for damage this round did. Breaks if ``job_id``
        becomes optional, which is a real design change and wants its own ruling.
        """
        with pytest.raises(KeyError):
            _import_job({})


class TestAdministrativeFieldsThroughTheRealWriter:
    """``save_job_plan`` then ``load_job_plan`` — the actual file on disk."""

    @pytest.fixture
    def isolate_data(self, tmp_path: Path, monkeypatch) -> Path:
        """Persist jobs under tmp_path, never the repo's configured data dir."""
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    def test_the_eight_survive_the_real_job_record_file(self, isolate_data):
        """The eight survive ``save_job_plan`` -> job.json -> ``load_job_plan``.

        The round-trip test above never touches a filesystem; this one proves the
        same eight survive the real writer and the real reader, which is the
        cycle a resumed job actually performs.
        """
        plan, values = _populated_plan()
        path = save_job_plan(plan)
        assert path.exists()
        loaded = load_job_plan(plan.job_id)
        assert loaded is not None
        assert loaded.mission == values["mission"]
        assert loaded.user_prompt == values["user_prompt"]
        assert loaded.project_id == values["project_id"]
        assert loaded.intake == values["intake"]
        assert loaded.flight_plan == values["flight_plan"]
        assert loaded.artifacts == values["artifacts"]
        assert loaded.budget == values["budget"]
        assert loaded.fences == values["fences"]
