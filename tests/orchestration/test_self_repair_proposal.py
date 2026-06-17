"""Tests for self_repair_proposal module (Steps 2446-2505)."""

from __future__ import annotations

import json

from packages.orchestration.self_repair_proposal import (
    _ALL_STATUSES,
    _APPROVABLE_STATUSES,
    _TERMINAL_STATUSES,
    SelfRepairProposal,
    SelfRepairProposalStatus,
    _redact_abs_paths,
    _sanitize_prompt,
    approve_self_repair_proposal,
    convert_self_repair_proposal_to_worker_prompt,
    create_self_repair_proposal_from_replay,
    deny_self_repair_proposal,
    edit_self_repair_proposal,
    export_self_repair_proposal_json,
    list_self_repair_proposals,
    load_self_repair_proposal,
    save_self_repair_proposal,
    self_repair_progress_summary,
    self_repair_proposal_integrity,
    self_repair_proposal_summary_for_bundle,
)

# ---------------------------------------------------------------------------
# Status constants
# ---------------------------------------------------------------------------


class TestStatuses:

    def test_all_statuses_count(self):
        assert len(_ALL_STATUSES) == 7

    def test_terminal_statuses(self):
        assert SelfRepairProposalStatus.DENIED in _TERMINAL_STATUSES
        assert SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT in _TERMINAL_STATUSES
        assert SelfRepairProposalStatus.APPROVED not in _TERMINAL_STATUSES

    def test_draft_not_terminal(self):
        assert SelfRepairProposalStatus.DRAFT not in _TERMINAL_STATUSES


# ---------------------------------------------------------------------------
# Model serialization
# ---------------------------------------------------------------------------


class TestSerialization:

    def test_roundtrip(self):
        p = SelfRepairProposal(
            proposal_id="srp-test123",
            run_id="dfr-abc",
            status=SelfRepairProposalStatus.DRAFT,
            title="Test proposal",
            problem_summary="Something broke",
            evidence_refs=["replay:dfr-abc"],
            suspected_files=["packages/orchestration/dogfood_run.py"],
            suggested_worker_prompt="Fix it",
            acceptance_criteria=["Tests pass"],
            required_tests=["test_foo.py"],
            forbidden_actions=["auto-apply"],
            risk_summary="Low risk",
            created_at="2026-01-01T00:00:00Z",
        )
        d = p.to_dict()
        assert d["proposal_id"] == "srp-test123"
        assert d["status"] == "draft"
        assert d["schema_version"] == "self-repair-proposal-v0"

    def test_to_dict_redacts_abs_paths(self):
        p = SelfRepairProposal(
            proposal_id="srp-pathtest",
            suggested_worker_prompt="Fix /home/user/secret/file.py",
        )
        d = p.to_dict()
        assert "/home/user/" not in d["suggested_worker_prompt"]

    def test_to_dict_bounds_evidence_refs(self):
        p = SelfRepairProposal(
            proposal_id="srp-bound",
            evidence_refs=[f"ref:{i}" for i in range(50)],
        )
        d = p.to_dict()
        assert len(d["evidence_refs"]) <= 30

    def test_to_dict_bounds_suspected_files(self):
        p = SelfRepairProposal(
            proposal_id="srp-files",
            suspected_files=[f"file{i}.py" for i in range(30)],
        )
        d = p.to_dict()
        assert len(d["suspected_files"]) <= 20

    def test_to_dict_bounds_prompt_length(self):
        p = SelfRepairProposal(
            proposal_id="srp-longprompt",
            suggested_worker_prompt="x" * 10000,
        )
        d = p.to_dict()
        assert len(d["suggested_worker_prompt"]) <= 8000


# ---------------------------------------------------------------------------
# Redaction
# ---------------------------------------------------------------------------


class TestRedaction:

    def test_redact_home_path(self):
        result = _redact_abs_paths("file at /home/user/secret/foo.py")
        assert "/home/user/" not in result

    def test_redact_users_path(self):
        result = _redact_abs_paths("file at /Users/dev/project/bar.py")
        assert "/Users/dev/" not in result

    def test_redact_tmp_path(self):
        result = _redact_abs_paths("file at /tmp/abc123/test.toml")
        assert "/tmp/" not in result

    def test_no_redaction_for_relative(self):
        result = _redact_abs_paths("file at packages/foo.py")
        assert result == "file at packages/foo.py"

    def test_url_not_redacted(self):
        result = _redact_abs_paths("url http://localhost:11434")
        assert "http://localhost:11434" in result


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------


class TestStorage:

    def test_save_load_roundtrip(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-store1",
            run_id="dfr-abc",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            title="Test save",
            created_at="2026-01-01T00:00:00Z",
        )
        assert save_self_repair_proposal(p, data_dir=tmp_path)
        loaded = load_self_repair_proposal("srp-store1", data_dir=tmp_path)
        assert loaded is not None
        assert loaded.proposal_id == "srp-store1"
        assert loaded.title == "Test save"

    def test_load_missing(self, tmp_path):
        assert load_self_repair_proposal("nonexistent", data_dir=tmp_path) is None

    def test_list_proposals(self, tmp_path):
        for i in range(3):
            p = SelfRepairProposal(
                proposal_id=f"srp-list{i}",
                run_id="dfr-abc",
                status=SelfRepairProposalStatus.DRAFT,
                created_at=f"2026-01-0{i+1}T00:00:00Z",
            )
            save_self_repair_proposal(p, data_dir=tmp_path)
        result = list_self_repair_proposals(data_dir=tmp_path)
        assert len(result) == 3

    def test_list_filter_by_run_id(self, tmp_path):
        for i, rid in enumerate(["dfr-a", "dfr-b", "dfr-a"]):
            p = SelfRepairProposal(
                proposal_id=f"srp-filter{i}",
                run_id=rid,
                created_at=f"2026-01-0{i+1}T00:00:00Z",
            )
            save_self_repair_proposal(p, data_dir=tmp_path)
        result = list_self_repair_proposals(run_id="dfr-a", data_dir=tmp_path)
        assert len(result) == 2

    def test_list_filter_by_status(self, tmp_path):
        for i, st in enumerate([SelfRepairProposalStatus.DRAFT,
                                 SelfRepairProposalStatus.APPROVED,
                                 SelfRepairProposalStatus.DRAFT]):
            p = SelfRepairProposal(
                proposal_id=f"srp-statf{i}",
                status=st,
                created_at=f"2026-01-0{i+1}T00:00:00Z",
            )
            save_self_repair_proposal(p, data_dir=tmp_path)
        result = list_self_repair_proposals(
            status=SelfRepairProposalStatus.DRAFT, data_dir=tmp_path,
        )
        assert len(result) == 2

    def test_list_empty_dir(self, tmp_path):
        assert list_self_repair_proposals(data_dir=tmp_path) == []

    def test_corrupt_file_skipped(self, tmp_path):
        pdir = tmp_path / "self_repair_proposals"
        pdir.mkdir(parents=True)
        (pdir / "bad.json").write_text("not json{{{")
        p = SelfRepairProposal(
            proposal_id="srp-good",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = list_self_repair_proposals(data_dir=tmp_path)
        assert len(result) == 1
        assert result[0]["proposal_id"] == "srp-good"


# ---------------------------------------------------------------------------
# Proposal generation from replay
# ---------------------------------------------------------------------------


class TestProposalGeneration:

    def test_no_issues_produces_blocked(self, tmp_path):
        p = create_self_repair_proposal_from_replay("nonexistent-run", data_dir=tmp_path)
        assert p.status == SelfRepairProposalStatus.BLOCKED
        assert "No suspected" in p.title
        assert p.proposal_id.startswith("srp-")

    def test_proposal_saved_after_creation(self, tmp_path):
        p = create_self_repair_proposal_from_replay("test-run", data_dir=tmp_path)
        loaded = load_self_repair_proposal(p.proposal_id, data_dir=tmp_path)
        assert loaded is not None
        assert loaded.proposal_id == p.proposal_id

    def test_proposal_has_forbidden_actions(self, tmp_path):
        p = create_self_repair_proposal_from_replay("test-run", data_dir=tmp_path)
        if p.status != SelfRepairProposalStatus.BLOCKED:
            assert len(p.forbidden_actions) > 0
            assert "auto-apply" in p.forbidden_actions


# ---------------------------------------------------------------------------
# Operator decision flow
# ---------------------------------------------------------------------------


class TestApproval:

    @staticmethod
    def _approvable_proposal(**overrides):
        defaults = dict(
            proposal_id="srp-appr1",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            evidence_refs=["replay:test"],
            suggested_worker_prompt="Fix the bug",
            acceptance_criteria=["Tests pass"],
            required_tests=["test_foo.py"],
            created_at="2026-01-01T00:00:00Z",
        )
        defaults.update(overrides)
        return SelfRepairProposal(**defaults)

    def test_approve(self, tmp_path):
        p = self._approvable_proposal()
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = approve_self_repair_proposal("srp-appr1", "op-1", data_dir=tmp_path)
        assert result is not None
        assert result.status == SelfRepairProposalStatus.APPROVED
        assert "approved" in result.operator_decision

    def test_approve_with_notes(self, tmp_path):
        p = self._approvable_proposal(proposal_id="srp-appr2")
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = approve_self_repair_proposal(
            "srp-appr2", "op-1", notes="Looks good", data_dir=tmp_path,
        )
        assert result is not None
        assert result.operator_notes == "Looks good"

    def test_approve_nonexistent(self, tmp_path):
        assert approve_self_repair_proposal("nope", "op-1", data_dir=tmp_path) is None

    def test_approve_denied_fails(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-denied1",
            status=SelfRepairProposalStatus.DENIED,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-denied1", "op-1", data_dir=tmp_path) is None

    def test_approve_blocked_fails(self, tmp_path):
        p = self._approvable_proposal(
            proposal_id="srp-blocked1",
            status=SelfRepairProposalStatus.BLOCKED,
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-blocked1", "op-1", data_dir=tmp_path) is None

    def test_approve_draft_fails(self, tmp_path):
        p = self._approvable_proposal(
            proposal_id="srp-draft1",
            status=SelfRepairProposalStatus.DRAFT,
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-draft1", "op-1", data_dir=tmp_path) is None

    def test_approve_missing_evidence_fails(self, tmp_path):
        p = self._approvable_proposal(
            proposal_id="srp-noev2",
            evidence_refs=[],
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-noev2", "op-1", data_dir=tmp_path) is None

    def test_approve_missing_prompt_fails(self, tmp_path):
        p = self._approvable_proposal(
            proposal_id="srp-noprompt",
            suggested_worker_prompt="",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-noprompt", "op-1", data_dir=tmp_path) is None

    def test_approve_missing_criteria_fails(self, tmp_path):
        p = self._approvable_proposal(
            proposal_id="srp-nocrit",
            acceptance_criteria=[],
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-nocrit", "op-1", data_dir=tmp_path) is None

    def test_approve_missing_tests_fails(self, tmp_path):
        p = self._approvable_proposal(
            proposal_id="srp-notests",
            required_tests=[],
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert approve_self_repair_proposal("srp-notests", "op-1", data_dir=tmp_path) is None


class TestDeny:

    def test_deny(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-deny1",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = deny_self_repair_proposal("srp-deny1", "op-1", data_dir=tmp_path)
        assert result is not None
        assert result.status == SelfRepairProposalStatus.DENIED

    def test_deny_nonexistent(self, tmp_path):
        assert deny_self_repair_proposal("nope", "op-1", data_dir=tmp_path) is None

    def test_deny_already_converted(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-conv1",
            status=SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert deny_self_repair_proposal("srp-conv1", "op-1", data_dir=tmp_path) is None


class TestEdit:

    def test_edit_returns_to_awaiting(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-edit1",
            status=SelfRepairProposalStatus.APPROVED,
            suggested_worker_prompt="Original",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = edit_self_repair_proposal(
            "srp-edit1", "op-1", "Updated prompt", data_dir=tmp_path,
        )
        assert result is not None
        assert result.status == SelfRepairProposalStatus.AWAITING_OPERATOR
        assert result.suggested_worker_prompt == "Updated prompt"

    def test_edit_denied_fails(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-editdeny",
            status=SelfRepairProposalStatus.DENIED,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert edit_self_repair_proposal(
            "srp-editdeny", "op-1", "text", data_dir=tmp_path,
        ) is None


class TestConversion:

    def test_convert_approved(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-cnv1",
            status=SelfRepairProposalStatus.APPROVED,
            suggested_worker_prompt="Do the fix",
            evidence_refs=["replay:test"],
            operator_decision="approved by op-1",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        prompt = convert_self_repair_proposal_to_worker_prompt("srp-cnv1", data_dir=tmp_path)
        assert prompt == "Do the fix"
        loaded = load_self_repair_proposal("srp-cnv1", data_dir=tmp_path)
        assert loaded is not None
        assert loaded.status == SelfRepairProposalStatus.CONVERTED_TO_WORKER_PROMPT

    def test_convert_no_evidence_fails(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-cnvnoev",
            status=SelfRepairProposalStatus.APPROVED,
            suggested_worker_prompt="Do the fix",
            evidence_refs=[],
            operator_decision="approved by op-1",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert convert_self_repair_proposal_to_worker_prompt(
            "srp-cnvnoev", data_dir=tmp_path,
        ) is None

    def test_convert_denied_blocked(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-cnvdeny",
            status=SelfRepairProposalStatus.DENIED,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert convert_self_repair_proposal_to_worker_prompt(
            "srp-cnvdeny", data_dir=tmp_path,
        ) is None

    def test_convert_draft_blocked(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-cnvdraft",
            status=SelfRepairProposalStatus.DRAFT,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        assert convert_self_repair_proposal_to_worker_prompt(
            "srp-cnvdraft", data_dir=tmp_path,
        ) is None

    def test_convert_nonexistent(self, tmp_path):
        assert convert_self_repair_proposal_to_worker_prompt(
            "nope", data_dir=tmp_path,
        ) is None

    def test_edit_requires_reapproval(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-reappr",
            status=SelfRepairProposalStatus.APPROVED,
            suggested_worker_prompt="Original",
            evidence_refs=["replay:test"],
            acceptance_criteria=["Tests pass"],
            required_tests=["test_foo.py"],
            operator_decision="approved by op-1",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        edit_self_repair_proposal("srp-reappr", "op-1", "Edited", data_dir=tmp_path)
        assert convert_self_repair_proposal_to_worker_prompt(
            "srp-reappr", data_dir=tmp_path,
        ) is None
        approve_self_repair_proposal("srp-reappr", "op-1", data_dir=tmp_path)
        prompt = convert_self_repair_proposal_to_worker_prompt(
            "srp-reappr", data_dir=tmp_path,
        )
        assert prompt == "Edited"


# ---------------------------------------------------------------------------
# Integrity checks
# ---------------------------------------------------------------------------


class TestIntegrity:

    def test_clean_integrity(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-int1",
            status=SelfRepairProposalStatus.DRAFT,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = self_repair_proposal_integrity(data_dir=tmp_path)
        assert result["passed"] is True

    def test_unknown_status_fails(self, tmp_path):
        pdir = tmp_path / "self_repair_proposals"
        pdir.mkdir(parents=True)
        (pdir / "bad_status.json").write_text(json.dumps({
            "proposal_id": "srp-bad", "status": "fake_status",
        }))
        result = self_repair_proposal_integrity(data_dir=tmp_path)
        assert result["passed"] is False
        assert any(c["code"] == "unknown_status" for c in result["checks"])

    def test_approved_without_evidence(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-noev",
            status=SelfRepairProposalStatus.APPROVED,
            evidence_refs=[],
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = self_repair_proposal_integrity(data_dir=tmp_path)
        assert result["passed"] is False
        assert any(c["code"] == "approved_without_evidence" for c in result["checks"])

    def test_raw_data_leak_detected(self, tmp_path):
        pdir = tmp_path / "self_repair_proposals"
        pdir.mkdir(parents=True)
        (pdir / "leak.json").write_text(json.dumps({
            "proposal_id": "srp-leak",
            "status": "draft",
            "suggested_worker_prompt": "Fix the sk-ant-api03-secret key",
        }))
        result = self_repair_proposal_integrity(data_dir=tmp_path)
        assert result["passed"] is False
        assert any(c["code"] == "raw_data_leak" for c in result["checks"])

    def test_empty_dir_passes(self, tmp_path):
        result = self_repair_proposal_integrity(data_dir=tmp_path)
        assert result["passed"] is True
        assert result["checks"] == []


# ---------------------------------------------------------------------------
# Bundle / progress summaries
# ---------------------------------------------------------------------------


class TestBundleSummary:

    def test_summary_counts(self, tmp_path):
        for i, st in enumerate([
            SelfRepairProposalStatus.AWAITING_OPERATOR,
            SelfRepairProposalStatus.APPROVED,
            SelfRepairProposalStatus.DENIED,
        ]):
            p = SelfRepairProposal(
                proposal_id=f"srp-sum{i}",
                status=st,
                created_at=f"2026-01-0{i+1}T00:00:00Z",
            )
            save_self_repair_proposal(p, data_dir=tmp_path)
        result = self_repair_proposal_summary_for_bundle(data_dir=tmp_path)
        assert result["total_proposals"] == 3
        assert result["awaiting_operator"] == 1
        assert result["approved"] == 1
        assert result["denied"] == 1

    def test_summary_empty(self, tmp_path):
        result = self_repair_proposal_summary_for_bundle(data_dir=tmp_path)
        assert result["total_proposals"] == 0


class TestProgressSummary:

    def test_progress_with_awaiting(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-prog1",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = self_repair_progress_summary(data_dir=tmp_path)
        assert result["awaiting_operator_count"] == 1
        assert "proposal-list" in result["next_safe_action"]

    def test_progress_with_approved(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-prog2",
            status=SelfRepairProposalStatus.APPROVED,
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = self_repair_progress_summary(data_dir=tmp_path)
        assert result["approved_count"] == 1
        assert "worker-prompt" in result["next_safe_action"]

    def test_progress_empty(self, tmp_path):
        result = self_repair_progress_summary(data_dir=tmp_path)
        assert result["latest_proposal_id"] == ""
        assert result["next_safe_action"] == ""


# ---------------------------------------------------------------------------
# No-raw-leak closure
# ---------------------------------------------------------------------------


class TestNoRawLeak:

    def test_to_dict_no_raw_markers(self):
        p = SelfRepairProposal(
            proposal_id="srp-noleak",
            title="Test",
            problem_summary="Safe text",
            suggested_worker_prompt="Fix the bug",
            risk_summary="Low",
        )
        d = p.to_dict()
        as_str = json.dumps(d)
        for marker in ("diff --git", "-----BEGIN", "sk-ant", "sk-proj"):
            assert marker not in as_str

    def test_export_matches_to_dict(self):
        p = SelfRepairProposal(proposal_id="srp-exp1")
        assert export_self_repair_proposal_json(p) == p.to_dict()


# ---------------------------------------------------------------------------
# R-0135: Approvable status gate
# ---------------------------------------------------------------------------


class TestApprovableStatuses:

    def test_approvable_statuses_defined(self):
        assert SelfRepairProposalStatus.AWAITING_OPERATOR in _APPROVABLE_STATUSES
        assert SelfRepairProposalStatus.EDITED in _APPROVABLE_STATUSES
        assert SelfRepairProposalStatus.DRAFT not in _APPROVABLE_STATUSES
        assert SelfRepairProposalStatus.BLOCKED not in _APPROVABLE_STATUSES
        assert SelfRepairProposalStatus.APPROVED not in _APPROVABLE_STATUSES

    def test_edited_can_be_approved(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-edited-appr",
            status=SelfRepairProposalStatus.EDITED,
            evidence_refs=["replay:test"],
            suggested_worker_prompt="Fix bug",
            acceptance_criteria=["Tests pass"],
            required_tests=["test_foo.py"],
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = approve_self_repair_proposal("srp-edited-appr", "op-1", data_dir=tmp_path)
        assert result is not None
        assert result.status == SelfRepairProposalStatus.APPROVED


# ---------------------------------------------------------------------------
# R-0136: Secret marker scrubbing
# ---------------------------------------------------------------------------


class TestSecretScrubbing:

    def test_sanitize_prompt_scrubs_sk_ant(self):
        result = _sanitize_prompt("key is sk-ant-api03-1234567890abcdef")
        assert "sk-ant" not in result
        assert "<secret-redacted>" in result

    def test_sanitize_prompt_scrubs_sk_proj(self):
        result = _sanitize_prompt("sk-proj-abcdef12345")
        assert "sk-proj" not in result

    def test_sanitize_prompt_scrubs_api_key(self):
        result = _sanitize_prompt("api_key = abc123secret")
        assert "abc123secret" not in result

    def test_sanitize_prompt_scrubs_password(self):
        result = _sanitize_prompt("password=mysecret123")
        assert "mysecret123" not in result

    def test_sanitize_prompt_scrubs_pem(self):
        pem = "-----BEGIN RSA PRIVATE KEY-----\ndata\n-----END RSA PRIVATE KEY-----"
        result = _sanitize_prompt(pem)
        assert "-----BEGIN" not in result

    def test_to_dict_scrubs_secrets_in_prompt(self):
        p = SelfRepairProposal(
            proposal_id="srp-secprompt",
            suggested_worker_prompt="Use sk-ant-api03-secret-value here",
        )
        d = p.to_dict()
        assert "sk-ant" not in d["suggested_worker_prompt"]

    def test_to_dict_scrubs_secrets_in_risk_summary(self):
        p = SelfRepairProposal(
            proposal_id="srp-secrisk",
            risk_summary="Leaked password=admin123",
        )
        d = p.to_dict()
        assert "admin123" not in d["risk_summary"]

    def test_to_dict_scrubs_secrets_in_notes(self):
        p = SelfRepairProposal(
            proposal_id="srp-secnotes",
            operator_notes="api_key=my_secret_key_here",
        )
        d = p.to_dict()
        assert "my_secret_key_here" not in d["operator_notes"]

    def test_edit_sanitizes_input(self, tmp_path):
        p = SelfRepairProposal(
            proposal_id="srp-editsec",
            status=SelfRepairProposalStatus.AWAITING_OPERATOR,
            suggested_worker_prompt="Original",
            created_at="2026-01-01T00:00:00Z",
        )
        save_self_repair_proposal(p, data_dir=tmp_path)
        result = edit_self_repair_proposal(
            "srp-editsec", "op-1", "Fix with sk-ant-api03-leak", data_dir=tmp_path,
        )
        assert result is not None
        assert "sk-ant" not in result.suggested_worker_prompt


# ---------------------------------------------------------------------------
# R-0137: Signal collection diagnostics
# ---------------------------------------------------------------------------


class TestSignalCollectionDiagnostics:

    def test_no_issues_with_warnings_produces_blocked(self, tmp_path):
        p = create_self_repair_proposal_from_replay("nonexistent-run", data_dir=tmp_path)
        assert p.status == SelfRepairProposalStatus.BLOCKED
        assert p.proposal_id.startswith("srp-")
