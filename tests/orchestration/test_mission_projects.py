"""F205, DECISION F205 D2 — a mission over several repositories names the projects it spans.

The record names the projects a mission spans, its own project first, and each job link the
project of its job; both are written only on such a mission, so the record of every other mission
keeps its bytes. A job is linked to such a mission only when its own record names a project the
mission spans. Every test writes under ``tmp_path``, passed as ``root=``.
"""
from __future__ import annotations

import json

import pytest

from packages.orchestration.mission_record import Mission, MissionJobLink
from packages.orchestration.mission_state import (
    MISSION_ROLE_FOLLOW_UP,
    MISSION_ROLE_INITIAL,
    MissionError,
    MissionProjectError,
    continue_mission,
    create_mission,
    link_job_to_mission,
    load_mission,
    mission_for_job,
    mission_record_path,
)
from packages.orchestration.pingpong_job import JobPlan, list_job_plans, save_job_plan

_LEAD = "proj-toolbox"
_OTHER = "proj-brain"
_STRANGER = "proj-app"


def _job(tmp_path, project_id: str) -> str:
    job = JobPlan(job_title=f"a job in {project_id}", project_id=project_id)
    save_job_plan(job, root=tmp_path)
    return str(job.job_id)


def _record(tmp_path, mission) -> dict:
    return json.loads(mission_record_path(mission.project_id, mission.id, tmp_path).read_text())


class TestTheRecordOfOneProjectKeepsItsBytes:
    def test_a_mission_of_one_project_writes_no_project_list_and_no_link_project(self, tmp_path):
        mission = create_mission(_LEAD, "one repository", root=tmp_path)
        link_job_to_mission(_LEAD, mission.id, _job(tmp_path, _OTHER), MISSION_ROLE_INITIAL,
                            root=tmp_path)
        record = _record(tmp_path, mission)
        assert "project_ids" not in record
        assert [sorted(link) for link in record["job_links"]] == [["created_at", "job_id", "role"]]

    def test_naming_only_its_own_project_is_a_mission_of_one_project(self, tmp_path):
        mission = create_mission(_LEAD, "one repository", project_ids=[_LEAD], root=tmp_path)
        assert mission.project_ids == ()
        assert "project_ids" not in _record(tmp_path, mission)
        assert mission.spanned_project_ids() == (_LEAD,)


class TestAMissionOverSeveralProjects:
    def test_the_record_names_the_projects_its_own_first_and_reads_back(self, tmp_path):
        mission = create_mission(_LEAD, "two repositories", project_ids=(_LEAD, _OTHER),
                                 root=tmp_path)
        assert _record(tmp_path, mission)["project_ids"] == [_LEAD, _OTHER]
        loaded = load_mission(_LEAD, mission.id, tmp_path)
        assert loaded.project_ids == (_LEAD, _OTHER)
        assert loaded.spanned_project_ids() == (_LEAD, _OTHER)

    def test_each_link_records_the_project_its_job_works_in(self, tmp_path):
        mission = create_mission(_LEAD, "two repositories", project_ids=(_LEAD, _OTHER),
                                 root=tmp_path)
        first, second = _job(tmp_path, _LEAD), _job(tmp_path, _OTHER)
        link_job_to_mission(_LEAD, mission.id, first, MISSION_ROLE_INITIAL, root=tmp_path)
        link_job_to_mission(_LEAD, mission.id, second, MISSION_ROLE_FOLLOW_UP, root=tmp_path)
        record = _record(tmp_path, mission)
        assert [(link["job_id"], link["project_id"]) for link in record["job_links"]] == [
            (first, _LEAD), (second, _OTHER)]
        assert [link.project_id for link in load_mission(_LEAD, mission.id, tmp_path).job_links] == [
            _LEAD, _OTHER]
        assert mission_for_job(second, tmp_path).id == mission.id

    def test_a_job_of_a_project_the_mission_does_not_span_is_refused(self, tmp_path):
        mission = create_mission(_LEAD, "two repositories", project_ids=(_LEAD, _OTHER),
                                 root=tmp_path)
        before = mission_record_path(_LEAD, mission.id, tmp_path).read_bytes()
        with pytest.raises(MissionProjectError, match=_STRANGER):
            link_job_to_mission(_LEAD, mission.id, _job(tmp_path, _STRANGER), MISSION_ROLE_INITIAL,
                                root=tmp_path)
        assert mission_record_path(_LEAD, mission.id, tmp_path).read_bytes() == before

    def test_a_job_without_a_record_is_refused(self, tmp_path):
        mission = create_mission(_LEAD, "two repositories", project_ids=(_LEAD, _OTHER),
                                 root=tmp_path)
        with pytest.raises(MissionProjectError, match="no readable record"):
            link_job_to_mission(_LEAD, mission.id, "0123456789abcdef", MISSION_ROLE_INITIAL,
                                root=tmp_path)
        assert load_mission(_LEAD, mission.id, tmp_path).job_links == ()


class TestTheProjectsMustFit:
    @pytest.mark.parametrize("project_ids", [
        (_OTHER, _LEAD),            # its own project is not first
        (_LEAD, _OTHER, _LEAD),     # a project twice
        (_OTHER,),                  # one project that is not its own
    ])
    def test_create_refuses_projects_that_do_not_fit(self, tmp_path, project_ids):
        with pytest.raises(MissionProjectError):
            create_mission(_LEAD, "two repositories", project_ids=project_ids, root=tmp_path)
        assert not (tmp_path / "missions").exists()

    def test_create_refuses_a_project_id_that_cannot_be_a_path(self, tmp_path):
        with pytest.raises(MissionError):
            create_mission(_LEAD, "two repositories", project_ids=(_LEAD, "../x"), root=tmp_path)

    @pytest.mark.parametrize("project_ids", [
        "proj-toolbox", [_LEAD], [_OTHER, _LEAD], [_LEAD, _OTHER, _OTHER]])
    def test_a_record_whose_projects_do_not_fit_will_not_read(self, project_ids):
        body = Mission(id="m1", project_id=_LEAD, goal="g").to_json()
        body["project_ids"] = project_ids
        with pytest.raises(ValueError):
            Mission.from_json(body)

    def test_a_link_reads_and_writes_its_project(self):
        link = MissionJobLink(job_id="j", role=MISSION_ROLE_INITIAL, created_at="t",
                              project_id=_OTHER)
        assert link.to_json()["project_id"] == _OTHER
        assert MissionJobLink.from_json(link.to_json()) == link
        assert "project_id" not in MissionJobLink(job_id="j", role=MISSION_ROLE_INITIAL,
                                                  created_at="t").to_json()


class TestTheNextJobContinuesWhereTheChainIs:
    """DECISION F205 D5: the next job works in the project and repository of the chain's last job."""

    @pytest.fixture(autouse=True)
    def _data_root(self, tmp_path, monkeypatch):
        """continue_mission reads and saves jobs through the default data root."""
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))

    def _chain(self, tmp_path, last_repo: str = "/repos/brain"):
        mission = create_mission(_LEAD, "two repositories", project_ids=(_LEAD, _OTHER),
                                 root=tmp_path)
        first = JobPlan(job_title="the toolbox part", project_id=_LEAD, repo_path="/repos/toolbox")
        last = JobPlan(job_title="the brain part", project_id=_OTHER, repo_path=last_repo)
        for job, role in ((first, MISSION_ROLE_INITIAL), (last, MISSION_ROLE_FOLLOW_UP)):
            save_job_plan(job, root=tmp_path)
            link_job_to_mission(_LEAD, mission.id, str(job.job_id), role, root=tmp_path)
        return mission, last

    def test_the_next_job_works_in_the_project_and_repository_of_the_last(self, tmp_path):
        mission, last = self._chain(tmp_path)

        following = continue_mission(_LEAD, mission.id, "Wire the brain to the app", root=tmp_path)

        assert (following.project_id, following.repo_path) == (_OTHER, "/repos/brain")
        assert following.tasks[0].inputs["previous_job_id"] == str(last.job_id)
        assert load_mission(_LEAD, mission.id, tmp_path).job_links[-1].project_id == _OTHER

    def test_a_last_job_without_a_repository_refuses_the_next_and_saves_nothing(self, tmp_path):
        mission, _last = self._chain(tmp_path, last_repo="")
        saved = len(list_job_plans())

        with pytest.raises(MissionProjectError, match="cannot tell where its next job works"):
            continue_mission(_LEAD, mission.id, "Wire the brain to the app", root=tmp_path)

        assert len(load_mission(_LEAD, mission.id, tmp_path).job_links) == 2
        assert len(list_job_plans()) == saved

    def test_a_mission_of_one_project_plans_its_next_job_as_before(self, tmp_path):
        mission = create_mission(_LEAD, "one repository", root=tmp_path)
        first = JobPlan(job_title="first", project_id=_LEAD, repo_path="/repos/toolbox")
        save_job_plan(first, root=tmp_path)
        link_job_to_mission(_LEAD, mission.id, str(first.job_id), MISSION_ROLE_INITIAL,
                            root=tmp_path)

        following = continue_mission(_LEAD, mission.id, "next", root=tmp_path)

        assert (following.project_id, following.repo_path) == (_LEAD, "")
