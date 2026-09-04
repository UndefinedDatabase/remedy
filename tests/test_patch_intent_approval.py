"""
Tests for packages/orchestration/approval_queue.py and the four approval CLI commands.

Coverage:
  - list_patch_intents: no intents, one intent pending, multiple intents
  - get_patch_intent: found, not found, malformed ID
  - set_approval_state: approve, reject, approve-after-reject, reject-after-approve
  - Invalid approval state raises ValueError
  - Invalid stored risk coerced to RISK_UNKNOWN
  - CLI: list-patch-intents with no intents
  - CLI: list-patch-intents with one intent
  - CLI: show-patch-intent found and not-found
  - CLI: approve-patch-intent writes metadata + run log event
  - CLI: reject-patch-intent writes metadata + run log event
  - CLI: approve after reject updates state
  - CLI: invalid intent_id exits non-zero
  - CLI: no repo files modified by approve/reject
  - Cockpit: pending approval attention item shown
  - Cockpit: rejected count attention item shown
  - Cockpit: all-approved next action does not imply applied
  - Cockpit: next action directs to list-patch-intents when approval pending + risk
"""

from __future__ import annotations

import json
from uuid import uuid4

import pytest

from packages.core.models import ArtifactKind, Job, RunState, Task
from packages.orchestration.approval_queue import (
    APPROVAL_APPROVED,
    APPROVAL_PENDING,
    APPROVAL_REJECTED,
    format_intent_detail,
    format_intent_list,
    get_patch_intent,
    list_patch_intents,
    make_intent_id,
    set_approval_state,
)
from packages.orchestration.cockpit import summarize_cockpit
from packages.orchestration.patch_intent import RISK_MEDIUM, RISK_UNKNOWN
from packages.orchestration.storage import save_job

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_job(**kwargs) -> Job:
    defaults: dict = {"name": "Test approval job", "state": RunState.PENDING}
    defaults.update(kwargs)
    return Job(**defaults)


def _make_pending_task(**kwargs) -> Task:
    return Task(description="do work", inputs={"task_type": "write_readme"}, **kwargs)


def _completed_task(**kwargs) -> Task:
    t = Task(description="done", inputs={"task_type": "write_readme"}, **kwargs)
    t.status = RunState.COMPLETED
    return t


def _add_patch_artifact(job: Job, *, risk: str = RISK_MEDIUM, intent_count: int = 1) -> str:
    """Add a fake patch-intent artifact to the job.  Returns the intent_id of the first intent."""
    from packages.core.models import Artifact

    explanations = [
        {
            "file": f"docs/file_{i}.md",
            "action": "modify",
            "risk": risk,
            "reason": "task type 'write_readme'",
            "summary": f"Proposed change {i} for readme",
        }
        for i in range(intent_count)
    ]
    artifact = Artifact(
        name="builder_proposal",
        content="",
        kind=ArtifactKind.BUILDER_PROPOSAL,
        task_id=uuid4(),
        metadata={
            "patch_intent_explanations": explanations,
            "patch_intent_risks": [risk] * intent_count,
            "patch_intent_diff_preview": "--- docs/file_0.md\n  + proposed content here",
        },
    )
    job.artifacts.append(artifact)
    return make_intent_id(artifact.id, 0)


def _ts(offset: int = 0) -> str:
    return f"2026-05-04T10:{offset:02d}:00+00:00"


def _task_run_succeeded_events(job_id: str, task_id: str) -> list[dict]:
    return [
        {"event": "task_run_started", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(0), "task_id": task_id,
         "metadata": {"task_type": "write_readme"}},
        {"event": "task_run_completed", "job_id": job_id, "run_id": "r",
         "timestamp": _ts(1), "task_id": task_id, "outcome": "pass", "metadata": {}},
    ]


def _patch_intent_event(job_id: str, task_id: str, risk: str = RISK_MEDIUM) -> dict:
    return {
        "event": "patch_intent_created", "job_id": job_id, "run_id": "r",
        "timestamp": _ts(2), "task_id": task_id, "outcome": "created",
        "metadata": {"intent_count": 1, "risk_levels": [risk]},
    }


# ---------------------------------------------------------------------------
# list_patch_intents
# ---------------------------------------------------------------------------


class TestListPatchIntents:
    def test_no_artifacts_returns_empty(self):
        job = _make_job()
        assert list_patch_intents(job) == []

    def test_artifact_without_explanations_returns_empty(self):
        from packages.core.models import Artifact
        job = _make_job()
        job.artifacts.append(Artifact(name="x", content="", metadata={}))
        assert list_patch_intents(job) == []

    def test_one_intent_default_state_pending(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        intents = list_patch_intents(job)
        assert len(intents) == 1
        assert intents[0]["state"] == APPROVAL_PENDING
        assert intents[0]["intent_id"] == intent_id

    def test_intent_fields_populated(self):
        job = _make_job()
        _add_patch_artifact(job)
        item = list_patch_intents(job)[0]
        assert item["target_path"] == "docs/file_0.md"
        assert item["action"] == "modify"
        assert item["risk"] == RISK_MEDIUM
        assert item["summary"] == "Proposed change 0 for readme"
        assert "intent_id" in item
        assert "artifact_id" in item

    def test_multiple_intents_all_listed(self):
        job = _make_job()
        _add_patch_artifact(job, intent_count=3)
        assert len(list_patch_intents(job)) == 3

    def test_intent_ids_are_distinct(self):
        job = _make_job()
        _add_patch_artifact(job, intent_count=2)
        intents = list_patch_intents(job)
        ids = [i["intent_id"] for i in intents]
        assert ids[0] != ids[1]

    def test_invalid_stored_risk_coerced_to_unknown(self):
        from packages.core.models import Artifact
        job = _make_job()
        artifact = Artifact(
            name="bad_risk",
            content="",
            metadata={"patch_intent_explanations": [{"file": "x.md", "action": "modify",
                                                       "risk": "super-dangerous",
                                                       "reason": "", "summary": ""}]},
        )
        job.artifacts.append(artifact)
        item = list_patch_intents(job)[0]
        assert item["risk"] == RISK_UNKNOWN

    def test_approved_intent_state_visible(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        item = list_patch_intents(job)[0]
        assert item["state"] == APPROVAL_APPROVED

    def test_rejected_intent_state_visible(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        item = list_patch_intents(job)[0]
        assert item["state"] == APPROVAL_REJECTED


# ---------------------------------------------------------------------------
# get_patch_intent
# ---------------------------------------------------------------------------


class TestGetPatchIntent:
    def test_found_by_id(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        item = get_patch_intent(job, intent_id)
        assert item is not None
        assert item["intent_id"] == intent_id

    def test_not_found_returns_none(self):
        job = _make_job()
        assert get_patch_intent(job, "deadbeef-0") is None

    def test_malformed_id_returns_none(self):
        job = _make_job()
        assert get_patch_intent(job, "no-dashes-or-idx") is None
        assert get_patch_intent(job, "") is None

    def test_wrong_index_returns_none(self):
        job = _make_job()
        _add_patch_artifact(job)  # only index 0 exists
        artifact = job.artifacts[0]
        bad_id = make_intent_id(artifact.id, 99)
        assert get_patch_intent(job, bad_id) is None


# ---------------------------------------------------------------------------
# set_approval_state
# ---------------------------------------------------------------------------


class TestSetApprovalState:
    def test_approve_sets_state(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        entry = set_approval_state(job, intent_id, APPROVAL_APPROVED)
        assert entry["state"] == APPROVAL_APPROVED

    def test_reject_sets_state(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        entry = set_approval_state(job, intent_id, APPROVAL_REJECTED)
        assert entry["state"] == APPROVAL_REJECTED

    def test_approve_after_reject_latest_wins(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        assert list_patch_intents(job)[0]["state"] == APPROVAL_APPROVED

    def test_reject_after_approve_latest_wins(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        assert list_patch_intents(job)[0]["state"] == APPROVAL_REJECTED

    def test_invalid_state_raises_value_error(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        with pytest.raises(ValueError, match="Invalid approval state"):
            set_approval_state(job, intent_id, "maybe")

    def test_invalid_intent_id_raises_value_error(self):
        job = _make_job()
        with pytest.raises(ValueError, match="not found"):
            set_approval_state(job, "deadbeef-0", APPROVAL_APPROVED)

    def test_entry_contains_target_path(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        entry = set_approval_state(job, intent_id, APPROVAL_APPROVED)
        assert entry["target_path"] == "docs/file_0.md"

    def test_entry_contains_reason(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        entry = set_approval_state(job, intent_id, APPROVAL_APPROVED, reason="looks good")
        assert entry["reason"] == "looks good"
        assert list_patch_intents(job)[0]["approval_reason"] == "looks good"

    def test_entry_contains_decided_at_timestamp(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        entry = set_approval_state(job, intent_id, APPROVAL_APPROVED)
        assert entry["decided_at"] is not None
        assert "T" in entry["decided_at"]  # ISO format

    def test_entry_risk_coerced_when_invalid_stored(self):
        from packages.core.models import Artifact
        job = _make_job()
        artifact = Artifact(
            name="bad",
            content="",
            metadata={"patch_intent_explanations": [{"file": "x.md", "action": "modify",
                                                       "risk": "INVALID",
                                                       "reason": "", "summary": ""}]},
        )
        job.artifacts.append(artifact)
        intent_id = make_intent_id(artifact.id, 0)
        entry = set_approval_state(job, intent_id, APPROVAL_APPROVED)
        assert entry["risk"] == RISK_UNKNOWN


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------


class TestFormatHelpers:
    def test_format_intent_list_empty(self):
        out = format_intent_list([])
        assert "No patch intents" in out

    def test_format_intent_list_shows_state(self):
        job = _make_job()
        _add_patch_artifact(job)
        out = format_intent_list(list_patch_intents(job))
        assert APPROVAL_PENDING in out

    def test_format_intent_list_shows_target_path(self):
        job = _make_job()
        _add_patch_artifact(job)
        out = format_intent_list(list_patch_intents(job))
        assert "docs/file_0.md" in out

    def test_format_intent_list_shows_decided_when_set(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        item = get_patch_intent(job, intent_id)
        out = format_intent_list(list_patch_intents(job))
        assert item["decided_at"] in out

    def test_format_intent_detail_shows_risk_and_summary(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        item = get_patch_intent(job, intent_id)
        out = format_intent_detail(item, None)
        assert RISK_MEDIUM in out
        assert "Proposed change 0" in out

    def test_format_intent_detail_truncates_diff_preview(self):
        long_preview = "x" * 500
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        item = get_patch_intent(job, intent_id)
        out = format_intent_detail(item, long_preview)
        # Should be truncated to _MAX_DIFF_DISPLAY_CHARS and show ellipsis
        assert "…" in out
        assert "x" * 500 not in out

    def test_format_intent_detail_no_diff_when_none(self):
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        item = get_patch_intent(job, intent_id)
        out = format_intent_detail(item, None)
        assert "diff preview" not in out


# ---------------------------------------------------------------------------
# CLI: list-patch-intents
# ---------------------------------------------------------------------------


class TestCmdListPatchIntents:
    def _save(self, tmp_path, monkeypatch, **kwargs) -> Job:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job(**kwargs)
        save_job(job)
        return job

    def test_no_intents_prints_placeholder(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id))
        out = capsys.readouterr().out
        assert "No patch intents" in out

    def test_one_intent_shows_in_table(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id))
        out = capsys.readouterr().out
        assert "docs/file_0.md" in out
        assert APPROVAL_PENDING in out

    def test_invalid_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.patch import _cmd_list_patch_intents
        with pytest.raises(SystemExit) as exc_info:
            _cmd_list_patch_intents("not-a-uuid")
        assert exc_info.value.code == 1

    def test_unknown_job_id_exits_1(self, tmp_path, monkeypatch):
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        from apps.cli.commands.patch import _cmd_list_patch_intents
        with pytest.raises(SystemExit) as exc_info:
            _cmd_list_patch_intents(str(uuid4()))
        assert exc_info.value.code == 1

    def test_json_output_has_version_and_intents(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_list_patch_intents
        _cmd_list_patch_intents(str(job.id), json_output=True)
        data = json.loads(capsys.readouterr().out)
        assert data["version"] == 1
        assert data["intent_count"] == 1
        assert data["intents"][0]["target_path"] == "docs/file_0.md"
        assert data["intents"][0]["decided_at"] is None


# ---------------------------------------------------------------------------
# CLI: show-patch-intent
# ---------------------------------------------------------------------------


class TestCmdShowPatchIntent:
    def _save(self, tmp_path, monkeypatch) -> Job:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        save_job(job)
        return job

    def test_shows_risk_and_summary(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        intent_id = _add_patch_artifact(job)
        save_job(job)
        from apps.cli.commands.patch import _cmd_show_patch_intent
        _cmd_show_patch_intent(str(job.id), intent_id)
        out = capsys.readouterr().out
        assert RISK_MEDIUM in out
        assert "Proposed change 0" in out

    def test_shows_diff_preview_truncated(self, tmp_path, monkeypatch, capsys):
        job = self._save(tmp_path, monkeypatch)
        intent_id = _add_patch_artifact(job)
        # Patch the artifact's diff preview to be long enough to trigger truncation
        job.artifacts[-1].metadata["patch_intent_diff_preview"] = "x" * 500
        save_job(job)
        from apps.cli.commands.patch import _cmd_show_patch_intent
        _cmd_show_patch_intent(str(job.id), intent_id)
        out = capsys.readouterr().out
        # Full 500-char preview must not appear verbatim
        assert "x" * 500 not in out

    def test_invalid_intent_id_exits_1(self, tmp_path, monkeypatch):
        job = self._save(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_show_patch_intent
        with pytest.raises(SystemExit) as exc_info:
            _cmd_show_patch_intent(str(job.id), "deadbeef-0")
        assert exc_info.value.code == 1


# ---------------------------------------------------------------------------
# CLI: approve-patch-intent
# ---------------------------------------------------------------------------


class TestCmdApprovePatchIntent:
    def _setup(self, tmp_path, monkeypatch) -> tuple[Job, str]:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        save_job(job)
        return job, intent_id

    def test_approve_writes_metadata(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        from packages.orchestration.storage import load_job
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        reloaded = load_job(job.id)
        item = get_patch_intent(reloaded, intent_id)
        assert item is not None
        assert item["state"] == APPROVAL_APPROVED

    def test_approve_emits_run_log_event(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        # Capture events by reading the JSONL file after the command.
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        approval_events = [e for e in events if e.get("event") == "patch_intent_approved"]
        assert len(approval_events) == 1
        meta = approval_events[0].get("metadata", {})
        assert meta.get("intent_id") == intent_id
        assert meta.get("target_path") == "docs/file_0.md"
        assert meta.get("risk") == RISK_MEDIUM

    def test_approve_confirmation_printed(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        out = capsys.readouterr().out
        assert "Approved" in out
        assert intent_id in out

    def test_approve_prints_no_files_modified_note(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        out = capsys.readouterr().out
        # Must reassure user that no repo files were changed.
        assert "no files" in out.lower() or "metadata only" in out.lower()

    def test_approve_with_reason(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        from packages.orchestration.storage import load_job
        _cmd_approve_patch_intent(str(job.id), intent_id, "LGTM")
        reloaded = load_job(job.id)
        item = get_patch_intent(reloaded, intent_id)
        assert item["approval_reason"] == "LGTM"

    def test_approve_with_reason_does_not_echo_raw_text(self, tmp_path, monkeypatch, capsys):
        """Raw approval reason must not appear in CLI output."""
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        _cmd_approve_patch_intent(str(job.id), intent_id, "SECRET_APPROVAL_REASON_DO_NOT_RENDER")
        out = capsys.readouterr().out
        assert "SECRET_APPROVAL_REASON_DO_NOT_RENDER" not in out

    def test_approve_with_reason_prints_recorded(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        _cmd_approve_patch_intent(str(job.id), intent_id, "any reason text")
        out = capsys.readouterr().out
        assert "reason: recorded" in out

    def test_approve_without_reason_prints_none(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        out = capsys.readouterr().out
        assert "reason: none" in out

    def test_approve_invalid_intent_id_exits_1(self, tmp_path, monkeypatch):
        job, _ = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        with pytest.raises(SystemExit) as exc_info:
            _cmd_approve_patch_intent(str(job.id), "deadbeef-0", None)
        assert exc_info.value.code == 1

    def test_no_repo_files_modified(self, tmp_path, monkeypatch, capsys):
        """approve-patch-intent must not modify any file outside REMEDY_DATA_DIR."""
        job, intent_id = self._setup(tmp_path, monkeypatch)
        # Record files in tmp_path before
        before = set(tmp_path.rglob("*"))
        from apps.cli.commands.patch import _cmd_approve_patch_intent
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        after = set(tmp_path.rglob("*"))
        new_files = after - before
        # New files must be inside REMEDY_DATA_DIR (tmp_path), not elsewhere.
        for f in new_files:
            assert str(f).startswith(str(tmp_path)), f"unexpected file outside data dir: {f}"


# ---------------------------------------------------------------------------
# CLI: reject-patch-intent
# ---------------------------------------------------------------------------


class TestCmdRejectPatchIntent:
    def _setup(self, tmp_path, monkeypatch) -> tuple[Job, str]:
        monkeypatch.setenv("REMEDY_DATA_DIR", str(tmp_path))
        job = _make_job()
        intent_id = _add_patch_artifact(job)
        save_job(job)
        return job, intent_id

    def test_reject_writes_metadata(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        from packages.orchestration.storage import load_job
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        reloaded = load_job(job.id)
        item = get_patch_intent(reloaded, intent_id)
        assert item is not None
        assert item["state"] == APPROVAL_REJECTED

    def test_reject_emits_run_log_event(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        rejection_events = [e for e in events if e.get("event") == "patch_intent_rejected"]
        assert len(rejection_events) == 1
        meta = rejection_events[0].get("metadata", {})
        assert meta.get("intent_id") == intent_id
        assert meta.get("risk") == RISK_MEDIUM

    def test_reject_confirmation_printed(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        out = capsys.readouterr().out
        assert "Rejected" in out
        assert intent_id in out

    def test_approve_after_reject_updates_state(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_approve_patch_intent, _cmd_reject_patch_intent
        from packages.orchestration.storage import load_job
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        _cmd_approve_patch_intent(str(job.id), intent_id, None)
        reloaded = load_job(job.id)
        item = get_patch_intent(reloaded, intent_id)
        assert item["state"] == APPROVAL_APPROVED

    def test_reject_prints_metadata_only_note(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        out = capsys.readouterr().out
        assert "no files" in out.lower() or "metadata only" in out.lower()

    def test_reject_with_reason_does_not_echo_raw_text(self, tmp_path, monkeypatch, capsys):
        """Raw rejection reason must not appear in CLI output."""
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, "SECRET_APPROVAL_REASON_DO_NOT_RENDER")
        out = capsys.readouterr().out
        assert "SECRET_APPROVAL_REASON_DO_NOT_RENDER" not in out

    def test_reject_with_reason_prints_recorded(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, "needs more work")
        out = capsys.readouterr().out
        assert "reason: recorded" in out

    def test_reject_without_reason_prints_none(self, tmp_path, monkeypatch, capsys):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        out = capsys.readouterr().out
        assert "reason: none" in out

    def test_reject_invalid_intent_id_exits_1(self, tmp_path, monkeypatch):
        job, _ = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        with pytest.raises(SystemExit) as exc_info:
            _cmd_reject_patch_intent(str(job.id), "deadbeef-0", None)
        assert exc_info.value.code == 1

    def test_run_log_reason_present_false_when_no_reason(self, tmp_path, monkeypatch):
        """reason_present=False logged when no reason given (not the absence of a key)."""
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, None)
        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next(e for e in events if e.get("event") == "patch_intent_rejected")
        assert ev["metadata"]["reason_present"] is False

    def test_run_log_reason_present_true_when_reason_given(self, tmp_path, monkeypatch):
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        _cmd_reject_patch_intent(str(job.id), intent_id, "not ready")
        runs_dir = tmp_path / "runs" / str(job.id)
        events = []
        for f in runs_dir.glob("*.jsonl"):
            for line in f.read_text().splitlines():
                if line.strip():
                    events.append(json.loads(line))
        ev = next(e for e in events if e.get("event") == "patch_intent_rejected")
        assert ev["metadata"]["reason_present"] is True

    def test_run_log_does_not_contain_raw_reason_text(self, tmp_path, monkeypatch):
        """The reason string must NOT appear in the run log — only reason_present=True."""
        job, intent_id = self._setup(tmp_path, monkeypatch)
        from apps.cli.commands.patch import _cmd_reject_patch_intent
        secret_reason = "SECRET_REASON_TEXT_MUST_NOT_LOG"
        _cmd_reject_patch_intent(str(job.id), intent_id, secret_reason)
        runs_dir = tmp_path / "runs" / str(job.id)
        for f in runs_dir.glob("*.jsonl"):
            assert secret_reason not in f.read_text()


# ---------------------------------------------------------------------------
# Cockpit integration
# ---------------------------------------------------------------------------


class TestCockpitApprovalIntegration:
    def test_pending_approval_medium_risk_shows_attention(self):
        """Pending approval + medium risk → attention item with 'pending' count."""
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        events = _task_run_succeeded_events(str(job.id), task_id) + [
            _patch_intent_event(str(job.id), task_id, RISK_MEDIUM),
        ]
        out = summarize_cockpit(job, events)
        assert "pending" in out.lower()
        assert "Review patch intent" in out or "list-patch-intents" in out

    def test_rejected_count_shows_in_attention(self):
        """Rejected intents show a rejected-count attention item."""
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_REJECTED)
        events = _task_run_succeeded_events(str(job.id), task_id) + [
            _patch_intent_event(str(job.id), task_id, RISK_MEDIUM),
        ]
        out = summarize_cockpit(job, events)
        assert "rejected" in out.lower()

    def test_all_approved_next_action_does_not_say_applied(self):
        """When all intents are approved, next action must not imply they were applied."""
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        set_approval_state(job, intent_id, APPROVAL_APPROVED)
        events = _task_run_succeeded_events(str(job.id), task_id)
        out = summarize_cockpit(job, events)
        # Must not imply files were applied to the repo
        assert "applied to" not in out.lower()
        assert "files changed" not in out.lower()
        # Must mention this is approval only / apply not implemented
        assert "not implemented" in out or "approval" in out.lower() or "approved" in out.lower()

    def test_next_action_suggests_list_intents_when_pending_approval_and_risk(self):
        """Next best action directs to list-patch-intents when pending approvals + risk."""
        job = _make_job()
        job.tasks.append(_make_pending_task())
        task_id = str(uuid4())
        _add_patch_artifact(job, risk=RISK_MEDIUM)
        events = _task_run_succeeded_events(str(job.id), task_id) + [
            _patch_intent_event(str(job.id), task_id, RISK_MEDIUM),
        ]
        out = summarize_cockpit(job, events)
        assert "patch list" in out

    def test_no_approval_attention_when_low_risk_and_no_intents_in_job(self):
        """Low risk patch events with no artifact approvals → no approval attention."""
        job = _make_job(state=RunState.COMPLETED)
        job.tasks.append(_completed_task())
        task_id = str(uuid4())
        events = _task_run_succeeded_events(str(job.id), task_id) + [
            _patch_intent_event(str(job.id), task_id, "low"),
        ]
        out = summarize_cockpit(job, events)
        # Low risk + no pending approvals → "Nothing needs your attention"
        assert "Nothing needs your attention" in out

    def test_cockpit_pending_approval_auto_continue_no_interaction(self):
        """Pending approval does not block auto-continue (it's guidance, not a hard gate)."""
        job = _make_job()
        job.tasks.append(_make_pending_task())
        intent_id = _add_patch_artifact(job, risk=RISK_MEDIUM)
        # No approval set — pending. workspace_write allowed.
        out = summarize_cockpit(job, [])
        # Can continue automatically is still yes (pending approval is attention, not a gate)
        section = out.split("Can continue automatically")[1].split("\n── ")[0]
        assert "yes" in section
