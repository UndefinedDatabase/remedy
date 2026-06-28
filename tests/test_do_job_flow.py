"""
Focused tests for the ``remedy do job-flow`` command.

Coverage:
  - The command is registered in the command catalog (do.job-flow)
  - Argument parsing wires --job-file, --repo, --timeout-sec, --json and the
    optional provider flags through the grouped argparse tree
  - The handler is wired into do_cmd.COMMAND_HANDLERS and the aggregate table
  - The handler validates required/illegal arguments without touching the repo
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, get_command
from apps.cli.commands import collect_all_handlers
from apps.cli.commands.do_cmd import COMMAND_HANDLERS
from apps.cli.grouped import build_parser
from apps.cli.grouped import main as grouped_main

COMMAND_ID = "do.job-flow"


# ---------------------------------------------------------------------------
# Catalog registration
# ---------------------------------------------------------------------------


class TestJobFlowCatalogEntry:
    def test_command_is_registered(self) -> None:
        cmd = get_command(COMMAND_ID)
        assert cmd.command_id == COMMAND_ID
        assert cmd.group_id == "do"
        assert cmd.subcommand == "job-flow"

    def test_command_appears_in_catalog_tuple(self) -> None:
        ids = {c.command_id for c in CATALOG}
        assert COMMAND_ID in ids

    def test_command_supports_json(self) -> None:
        cmd = get_command(COMMAND_ID)
        assert cmd.supports_json is True
        arg_names = {a.name for a in cmd.args}
        assert "--json" in arg_names

    def test_job_file_is_required_option(self) -> None:
        cmd = get_command(COMMAND_ID)
        job_file = next(a for a in cmd.args if a.name == "--job-file")
        assert job_file.is_option is True
        assert job_file.required is True

    def test_expected_options_present(self) -> None:
        cmd = get_command(COMMAND_ID)
        arg_names = {a.name for a in cmd.args}
        for expected in (
            "--job-file",
            "--repo",
            "--builder",
            "--reviewer",
            "--max-rounds",
            "--repair-rounds",
            "--test-command",
            "--claude-cli-write-mode",
            "--timeout-sec",
            "--out",
            "--json",
        ):
            assert expected in arg_names, f"missing option {expected}"

    def test_does_not_mutate_repo(self) -> None:
        cmd = get_command(COMMAND_ID)
        assert cmd.may_mutate_repo is False

    def test_description_explains_safe_stop(self) -> None:
        """Help text must make the safe-stop guarantees discoverable."""
        cmd = get_command(COMMAND_ID)
        desc = cmd.description.lower()
        assert "dry-run" in desc
        assert "evidence" in desc
        assert "approve" in desc
        assert "target repo" in desc


# ---------------------------------------------------------------------------
# Argument parsing (grouped argparse tree)
# ---------------------------------------------------------------------------


class TestJobFlowArgumentParsing:
    def _parse(self, argv: list[str]):
        return build_parser().parse_args(argv)

    def test_minimal_parse(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns._command_id == COMMAND_ID
        assert ns.job_file == "job.md"

    def test_repo_default_is_dot(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns.repo == "."

    def test_timeout_sec_default(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns.timeout_sec == "120"

    def test_json_flag(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md", "--json"])
        assert ns.json is True

    def test_json_defaults_false(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "job.md"])
        assert ns.json is False

    def test_full_parse(self) -> None:
        ns = self._parse([
            "do", "job-flow",
            "--job-file", "x.md",
            "--repo", "/repo",
            "--timeout-sec", "30",
            "--builder", "fake",
            "--reviewer", "fake",
            "--max-rounds", "5",
            "--repair-rounds", "2",
            "--test-command", "pytest -q",
            "--claude-cli-write-mode", "none",
            "--out", "bundle",
            "--json",
        ])
        assert ns._command_id == COMMAND_ID
        assert ns.job_file == "x.md"
        assert ns.repo == "/repo"
        assert ns.timeout_sec == "30"
        assert ns.builder == "fake"
        assert ns.reviewer == "fake"
        assert ns.max_rounds == "5"
        assert ns.repair_rounds == 2
        assert ns.test_command == "pytest -q"
        assert ns.claude_cli_write_mode == "none"
        assert ns.out == "bundle"
        assert ns.json is True


# ---------------------------------------------------------------------------
# Handler wiring
# ---------------------------------------------------------------------------


class TestJobFlowHandlerWiring:
    def test_handler_in_module_table(self) -> None:
        assert COMMAND_ID in COMMAND_HANDLERS
        assert callable(COMMAND_HANDLERS[COMMAND_ID])

    def test_handler_in_aggregate_table(self) -> None:
        table = collect_all_handlers()
        assert COMMAND_ID in table
        assert callable(table[COMMAND_ID])

    def test_every_catalog_arg_name_is_parseable(self) -> None:
        """The catalog options for the command must all be accepted by the parser."""
        cmd = get_command(COMMAND_ID)
        # Build an argv that supplies a value for every option.
        argv = ["do", "job-flow"]
        for a in cmd.args:
            if not a.is_option:
                continue
            if a.name == "--json":
                argv.append("--json")
            elif a.name == "--repair-rounds":
                argv.extend([a.name, "2"])
            else:
                argv.extend([a.name, "v"])
        ns = build_parser().parse_args(argv)
        assert ns._command_id == COMMAND_ID


# ---------------------------------------------------------------------------
# Handler argument validation (no repo mutation, fast-exit paths)
# ---------------------------------------------------------------------------


class TestJobFlowHandlerValidation:
    def _ns(self, **overrides):
        ns = build_parser().parse_args(["do", "job-flow", "--job-file", "job.md"])
        for k, v in overrides.items():
            setattr(ns, k, v)
        return ns

    def test_missing_job_file_exits_2(self) -> None:
        ns = self._ns(job_file="")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_invalid_builder_exits_2(self) -> None:
        ns = self._ns(builder="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_invalid_reviewer_exits_2(self) -> None:
        ns = self._ns(reviewer="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_invalid_write_mode_exits_2(self) -> None:
        ns = self._ns(claude_cli_write_mode="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2


# ---------------------------------------------------------------------------
# End-to-end: real grouped CLI path with the deterministic fake provider
#
# These exercise ``remedy do job-flow`` through ``apps.cli.grouped.main`` —
# the real argparse tree + dispatch — and run job-plan → job-run → job-report
# → job-evidence → job-promote(dry-run) end to end. The fake builder/reviewer
# make the run fully deterministic and fast; nothing touches the network and
# the target repo is never mutated.
# ---------------------------------------------------------------------------


def _snapshot_tree(root: Path) -> dict[str, str]:
    """Map every file under ``root`` to a content hash. Used to prove the
    target repo is byte-for-byte unchanged after a job-flow run."""
    snap: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            snap[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
    return snap


class TestJobFlowEndToEnd:
    @pytest.fixture
    def isolate_data(self, tmp_path: Path, monkeypatch):
        """Persist jobs/runs under tmp_path, never the repo's real .data dir."""
        data_dir = tmp_path / "remedy_data"
        data_dir.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
        return data_dir

    @pytest.fixture
    def demo_repo(self, tmp_path: Path) -> Path:
        repo = tmp_path / "repo"
        repo.mkdir()
        (repo / "README.md").write_text("# Demo\n")
        return repo

    @pytest.fixture
    def job_file(self, tmp_path: Path) -> Path:
        jf = tmp_path / "job.md"
        jf.write_text(
            "# Job: Job Flow E2E\n"
            "\n"
            "## Task 1\n"
            "Add a documentation file.\n"
            "\n"
            "Acceptance:\n"
            "- file exists\n"
        )
        return jf

    def _run(self, capsys, *, repo: Path, job_file: Path, evidence_out: Path,
             extra: list[str] | None = None) -> str:
        """Drive the real grouped CLI and return captured stdout."""
        argv = [
            "do", "job-flow",
            "--job-file", str(job_file),
            "--repo", str(repo),
            "--builder", "fake",
            "--reviewer", "fake",
            "--out", str(evidence_out),
        ]
        argv += extra or []
        grouped_main(argv)
        return capsys.readouterr().out

    # --- JSON output for a completed fake-provider job --------------------

    def test_json_completed_job(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--json"],
        )
        data = json.loads(out)

        assert data["command"] == "do.job-flow"
        assert data["job_id"]
        assert data["steps"] == [
            "job-plan", "job-run", "job-report",
            "job-evidence", "job-promote-dry-run",
        ]
        # Completed run → promote dry-run ready
        assert data["report"]["status"] == "completed"
        assert data["promote_ready"] is True
        assert data["promote_dry_run"]["status"] == "dry_run"

    def test_json_evidence_bundle_path_present(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=evidence_dir, extra=["--json"],
        )
        data = json.loads(out)
        out_dir = data["evidence"].get("out_dir")
        assert out_dir, "evidence bundle path missing from JSON output"
        assert evidence_dir.is_dir(), "evidence bundle directory not created on disk"

    def test_json_next_approve_command_present_when_ready(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--json"],
        )
        data = json.loads(out)
        assert data["promote_ready"] is True
        nac = data["next_approve_command"]
        assert nac, "next_approve_command should be present for a ready promote"
        assert data["job_id"] in nac
        assert "--approve" in nac

    # --- Text output for a completed fake-provider job --------------------

    def test_text_completed_job(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence",
        )
        assert "Job flow:" in out
        assert "Promote dry-run: dry_run" in out
        assert "Evidence bundle:" in out
        assert "Next (approval required):" in out
        assert "--approve" in out
        # Safe-stop guarantees are spelled out for the human.
        assert "This flow stops at a promote dry-run. The target repo is not changed." in out
        assert "audit trail exported" in out
        assert "until you explicitly approve the promote" in out

    # --- Blocked job behavior --------------------------------------------

    def test_json_blocked_job(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        # max-rounds 1: the fake reviewer never reaches its pass round, so the
        # task fails its completion gate and the job is blocked.
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--json", "--max-rounds", "1"],
        )
        data = json.loads(out)
        assert data["report"]["status"] == "blocked"
        assert data["promote_ready"] is False
        assert data["promote_dry_run"]["status"] == "blocked"

    def test_json_next_approve_absent_when_blocked(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--json", "--max-rounds", "1"],
        )
        data = json.loads(out)
        assert data["promote_ready"] is False
        assert data["next_approve_command"] == ""

    def test_text_blocked_job(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--max-rounds", "1"],
        )
        assert "Promote dry-run: blocked" in out
        assert "Not ready to promote:" in out
        assert "Next (approval required):" not in out
        assert "The target repo was not changed." in out

    # --- Target repo is never mutated ------------------------------------

    def test_target_repo_not_mutated(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        before = _snapshot_tree(demo_repo)
        self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--json"],
        )
        after = _snapshot_tree(demo_repo)
        assert before == after, "job-flow must not mutate the target repo"

    # --- token_summary (Step 5087) -----------------------------------------

    def test_json_token_summary_present(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        ts = data["token_summary"]
        assert "provider_call_count" in ts
        assert "builder_call_count" in ts
        assert "reviewer_call_count" in ts
        assert "repair_round_count" in ts
        assert "estimated_prompt_tokens_total" in ts
        assert "estimated_context_tokens_total" in ts
        assert "full_repo_tokens_estimated" in ts

    def test_json_token_summary_actual_null_for_fake(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        ts = data["token_summary"]
        assert ts["actual_provider_input_tokens"] is None
        assert ts["actual_provider_output_tokens"] is None

    def test_text_token_section(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence")
        assert "Token / Context:" in out
        assert "Provider calls:" in out

    # --- next_approve_command (Step 5088) -----------------------------------

    def test_json_next_approve_includes_repo(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        if data["promote_ready"]:
            assert "--repo" in data["next_approve_command"]
            assert "--approve" in data["next_approve_command"]

    def test_json_next_approve_includes_test_command(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence",
                        extra=["--json", "--test-command", "pytest -q"])
        data = json.loads(out)
        if data["promote_ready"]:
            assert "--test-command" in data["next_approve_command"]
            assert "pytest" in data["next_approve_command"]

    def test_json_next_approve_absent_blocked(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence",
                        extra=["--json", "--max-rounds", "1"])
        data = json.loads(out)
        assert data["promote_ready"] is False
        assert data["next_approve_command"] == ""

    # --- final_audit (Step 5090) -------------------------------------------

    def test_json_final_audit_ready(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert audit["human_decision_required"] is True
        assert audit["promote_ready"] is True
        assert audit["task_count"] >= 1
        assert audit["passed_task_count"] >= 1

    def test_json_final_audit_blocked(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence",
                        extra=["--json", "--max-rounds", "1"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    def test_json_final_audit_reviewer_verdict_summary(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert "reviewer_verdict_summary" in audit
        assert isinstance(audit["reviewer_verdict_summary"], list)

    def test_json_final_audit_test_summary(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert "test_summary" in audit
        assert isinstance(audit["test_summary"], list)

    def test_json_final_audit_next_action(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["recommended_next_action"]
        assert isinstance(audit["prompt_trace_available"], bool)
        assert isinstance(audit["token_summary_available"], bool)

    def test_text_final_audit(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence")
        assert "Final audit:" in out
        assert "Human approval is required" in out

    def test_text_blocked_diagnostics(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence",
                        extra=["--max-rounds", "1"])
        assert "Final audit: BLOCKED" in out

    # --- job_flow.json persistence (Step 5083) -----------------------------

    def test_job_flow_json_persisted(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        jf = evidence_dir / "job_flow.json"
        assert jf.exists(), "job_flow.json must be persisted under evidence output"
        data = json.loads(jf.read_text())
        assert data["command"] == "do.job-flow"
        assert "token_summary" in data
        assert "final_audit" in data

    # --- Agent run trace (new) -------------------------------------------

    def test_agent_run_trace_jsonl_persisted(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        trace = evidence_dir / "agent_run_trace.jsonl"
        assert trace.exists(), "agent_run_trace.jsonl must be persisted"
        lines = [l for l in trace.read_text().splitlines() if l.strip()]
        assert len(lines) >= 4  # job_flow_started, job_planned, task_*, final_audit

    def test_agent_run_trace_summary_persisted(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        summary = evidence_dir / "agent_run_trace_summary.json"
        assert summary.exists()
        data = json.loads(summary.read_text())
        assert data["total_events"] >= 4
        assert data["has_builder_events"] is True

    def test_agent_run_trace_has_job_id(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=evidence_dir, extra=["--json"])
        data = json.loads(out)
        job_id = data["job_id"]
        trace = evidence_dir / "agent_run_trace.jsonl"
        events = [json.loads(l) for l in trace.read_text().splitlines() if l.strip()]
        for ev in events:
            assert ev["job_id"] == job_id

    def test_json_has_agent_run_trace_summary(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        assert "agent_run_trace_summary" in data
        assert data["agent_run_trace_summary"]["total_events"] >= 4

    # --- Prompt trace metadata (new) -------------------------------------

    def test_prompt_trace_has_job_id_and_task_id(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=evidence_dir, extra=["--json"])
        data = json.loads(out)
        job_id = data["job_id"]
        # Find prompt trace files in task evidence dirs
        trace_files = list(evidence_dir.rglob("prompt_trace.jsonl"))
        assert trace_files, "prompt trace JSONL should be in evidence"
        for tf in trace_files:
            for line in tf.read_text().splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                assert entry["job_id"] == job_id, f"job_id mismatch in {tf}"
                assert entry["task_id"].startswith("T"), f"task_id not set in {tf}"
                assert entry["provider_kind"] == "synthetic_test"

    def test_prompt_trace_cwd_sanitized(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        trace_files = list(evidence_dir.rglob("prompt_trace.jsonl"))
        for tf in trace_files:
            for line in tf.read_text().splitlines():
                if not line.strip():
                    continue
                entry = json.loads(line)
                assert "/tmp/remedy-pingpong-" not in entry.get("cwd", ""), \
                    "cwd must not contain absolute staging path"

    # --- Final audit evidence-derived (new) ------------------------------

    def test_final_audit_has_evidence_fields(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert "agent_run_trace_available" in audit
        assert "job_flow_json_available" in audit
        assert "evidence_bundle_available" in audit
        assert "missing_observability_artifacts" in audit

    def test_final_audit_ready_with_all_artifacts(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        # With complete job + all artifacts, should be READY_FOR_APPROVAL
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert audit["agent_run_trace_available"] is True

    # --- Path sanitization (new) -----------------------------------------

    def test_job_flow_json_no_staging_paths(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        jf = evidence_dir / "job_flow.json"
        content = jf.read_text()
        assert "/tmp/remedy-pingpong-" not in content, \
            "job_flow.json must not contain absolute staging paths"

    def test_agent_run_trace_no_staging_paths(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        trace = evidence_dir / "agent_run_trace.jsonl"
        content = trace.read_text()
        assert "/tmp/remedy-pingpong-" not in content, \
            "agent_run_trace.jsonl must not contain staging paths"

    # --- R-4301: final audit job_flow_json_available=True -------------------

    def test_final_audit_job_flow_json_available_true(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["job_flow_json_available"] is True, \
            "R-4301: final audit must report job_flow_json_available=True"
        assert "job_flow_json" not in audit["missing_observability_artifacts"]

    # --- R-4302: evidence index persistence ---------------------------------

    def test_evidence_index_persisted(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        job_id = data["job_id"]
        idx_dir = isolate_data / "job_evidence_index"
        idx_file = idx_dir / f"{job_id}.json"
        assert idx_file.exists(), "R-4302: evidence index must be persisted"
        record = json.loads(idx_file.read_text())
        assert record["job_id"] == job_id
        assert record["has_agent_run_trace"] is True
        assert record["has_job_flow_json"] is True
        assert record["source_command"] == "do.job-flow"

    # --- R-4303: prompt correlation in agent run trace ----------------------

    def test_agent_run_trace_prompt_correlation(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        trace = evidence_dir / "agent_run_trace.jsonl"
        events = [json.loads(l) for l in trace.read_text().splitlines() if l.strip()]
        prompt_events = [e for e in events if e["event_kind"].endswith("_prompt_created")]
        assert len(prompt_events) >= 1, "should have at least one prompt event"
        for pe in prompt_events:
            assert "prompt_sha256" in pe
            assert "prompt_chars" in pe

    # --- R-4304: no private paths in shareable evidence ---------------------

    def test_no_home_paths_in_shareable_evidence(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        for artifact in ["job_flow.json", "agent_run_trace.jsonl"]:
            path = evidence_dir / artifact
            if path.exists():
                content = path.read_text()
                assert "/home/" not in content, \
                    f"R-4304: {artifact} must not contain /home/ paths"
                assert "/Users/" not in content, \
                    f"R-4304: {artifact} must not contain /Users/ paths"
                assert "/private/" not in content, \
                    f"R-4304: {artifact} must not contain /private/ paths"

    def test_next_approve_command_safe(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        if data.get("next_approve_command_safe"):
            nac_safe = data["next_approve_command_safe"]
            assert "<repo>" in nac_safe, \
                "R-4304: next_approve_command_safe must use <repo> placeholder"
            assert "/home/" not in nac_safe
            assert "/Users/" not in nac_safe
            assert "/tmp/" not in nac_safe

    # --- R-4305: trace_source honesty in E2E --------------------------------

    def test_agent_run_trace_has_trace_source(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        evidence_dir = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=evidence_dir, extra=["--json"])
        trace = evidence_dir / "agent_run_trace.jsonl"
        events = [json.loads(l) for l in trace.read_text().splitlines() if l.strip()]
        for ev in events:
            assert ev.get("trace_source") == "reconstructed", \
                f"R-4305: event {ev['event_kind']} must have trace_source=reconstructed"

    def test_agent_run_trace_summary_has_source_limitations(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        summary = data["agent_run_trace_summary"]
        assert "reconstructed" in summary["trace_sources"], \
            "R-4305: summary must report 'reconstructed' trace source"
        assert len(summary["source_limitations"]) > 0, \
            "R-4305: summary must include source_limitations for reconstructed traces"

    # --- R-4310: fail-closed audit blocks on missing manifest ---------------

    def test_final_audit_has_no_missing_artifacts(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["missing_observability_artifacts"] == [], \
            f"R-4310: E2E run should have zero missing artifacts, got {audit['missing_observability_artifacts']}"

    # --- R-4311: evidence index ordering ------------------------------------

    def test_evidence_index_has_job_flow_json_true(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        job_id = data["job_id"]
        idx_file = isolate_data / "job_evidence_index" / f"{job_id}.json"
        assert idx_file.exists()
        record = json.loads(idx_file.read_text())
        assert record["has_job_flow_json"] is True, \
            "R-4311: evidence index must report has_job_flow_json=True after job_flow.json persisted"
        ev_dir = Path(record["evidence_dir_local"])
        assert (ev_dir / "job_flow.json").exists(), \
            "R-4311: job_flow.json must exist on disk when index claims it"

    # --- R-4312: stdout JSON path hygiene -----------------------------------

    def test_json_stdout_no_private_paths(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        for pattern in ["/home/", "/Users/", "/private/", "remedy-pingpong"]:
            assert pattern not in out, \
                f"R-4312: JSON stdout must not contain '{pattern}'"

    def test_json_stdout_tmp_paths_sanitized(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        nac = data.get("next_approve_command", "")
        if nac:
            assert "/tmp/" not in nac or "[tmpdir]" in nac or "[staging]" in nac, \
                "R-4312: next_approve_command must have sanitized paths"

    # --- R-4315: command transcript persisted ---------------------------------

    def test_command_transcript_persisted(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct_file = ev / "command_transcript.json"
        assert ct_file.exists(), "R-4315: command_transcript.json must be persisted"
        ct = json.loads(ct_file.read_text())
        assert ct["command_id"] == "do.job-flow"
        assert ct["exit_code"] == 0
        assert ct["target_repo_mutated"] is False
        assert ct["evidence_ref"] == "evidence/current"

    def test_command_transcript_no_private_paths(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        raw = json.dumps(ct)
        for pat in ["/home/", "/Users/", "/private/"]:
            assert pat not in raw, \
                f"R-4315: command transcript must not contain '{pat}'"

    def test_command_transcript_has_repo_hashes(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        assert len(ct["target_repo_hash_before"]) == 16
        assert len(ct["target_repo_hash_after"]) == 16
        assert ct["target_repo_hash_before"] == ct["target_repo_hash_after"], \
            "R-4315: fake provider must not mutate target repo"

    def test_command_transcript_timestamps(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        assert ct["started_at"]
        assert ct["finished_at"]

    # --- R-4319: artifact refs preserve filenames ----------------------------

    def test_sanitizer_preserves_evidence_artifact_name(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-job-evidence-abc123/manifest.json"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "evidence/current/manifest.json", \
            "R-4327: evidence refs must use canonical evidence/current/ prefix"

    def test_sanitizer_preserves_staging_subpath(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-pingpong-abc123/staging/file.py"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "[staging]/staging/file.py", \
            "R-4319: sanitizer must preserve subpath after staging prefix"

    def test_sanitizer_preserves_home_subpath(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/home/alice/project/src/main.py"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "[local]/project/src/main.py", \
            "R-4319: sanitizer must preserve subpath after home prefix"

    # --- R-4316: manifest builder valid JSON ----------------------------------

    def test_manifest_builder_valid_json(self, tmp_path):
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=None)
        raw = json.dumps(manifest)
        parsed = json.loads(raw)
        assert parsed["bundle_kind"] == "remedy_review_zip"
        assert parsed["bundle_version"] == 8
        assert "generated_at" in parsed

    def test_manifest_builder_with_evidence(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        assert manifest["current_evidence"] is not None
        assert manifest["current_evidence"]["zip_prefix"] == "evidence/current"
        assert "job_flow.json" in manifest["current_evidence"]["root_artifacts"]

    # --- R-4318: observability gate complete after persist ----------------------

    def test_all_observability_artifacts_exist(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        expected = [
            "job_flow.json", "agent_run_trace.jsonl",
            "agent_run_trace_summary.json", "command_transcript.json",
        ]
        for name in expected:
            assert (ev / name).exists(), \
                f"R-4318: {name} must exist in evidence dir"

    # --- R-4321: review_state in manifest ------------------------------------

    def test_manifest_has_review_state(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        rs = manifest["review_state"]
        assert "latest_live_review_verdict" in rs
        assert "open_findings" in rs
        assert "builder_handoff_present" in rs
        assert "review_ready" in rs
        assert "review_state_source" in rs
        assert "plan_step_range" in rs
        assert "plan_goal_present" in rs

    # --- R-4322: review_subject classification --------------------------------

    def test_manifest_has_review_subject(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        rs = manifest["review_subject"]
        assert rs["kind"] in (
            "clean_commit", "dirty_working_tree", "feature_branch",
            "merged_main", "unknown",
        )
        assert "branch" in rs
        assert "commit" in rs
        assert "dirty_files" in rs
        assert "has_untracked_files" in rs
        assert "has_commits" in rs
        assert "human_summary" in rs

    def test_manifest_bundle_version_8(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        assert manifest["bundle_version"] == 8

    # --- R-4327: canonical artifact refs --------------------------------------

    def test_evidence_ref_canonical(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-job-evidence-abc123/manifest.json"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "evidence/current/manifest.json", \
            "R-4327: evidence refs must use canonical evidence/current/ prefix"

    def test_evidence_ref_task_run_canonical(self):
        from apps.cli.commands.do_cmd import _sanitize_shareable_paths
        data = {"ref": "/tmp/remedy-job-evidence-abc123/task_runs/T001/review.json"}
        result = _sanitize_shareable_paths(data)
        assert result["ref"] == "evidence/current/task_runs/T001/review.json"

    def test_evidence_bundle_path_canonical_in_stdout(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=ev, extra=["--json"])
        data = json.loads(out)
        ebp = data.get("evidence_bundle_path", "")
        assert ebp.startswith("evidence/current") or ebp == "", \
            "R-4327: evidence_bundle_path in stdout must use canonical ref"
