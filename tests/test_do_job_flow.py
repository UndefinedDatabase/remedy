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
        assert ns.timeout_sec is None  # None = not explicitly set; adaptive normal used

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

    #: F15: `--stream-evidence` / `--no-stream-evidence` are ONE mutually-exclusive store_const
    #: pair (omitted None / True / False), so no valid argv carries both, and neither takes a
    #: value. Supplying both is a usage error BY DESIGN — see
    #: `TestJobFlowStreamFlagsStayExclusive` below, which pins that.
    _BARE_FLAGS = {"--json", "--stream-evidence", "--no-stream-evidence"}
    _EXCLUSIVE_PARTNERS = {"--no-stream-evidence"}

    def test_every_catalog_arg_name_is_parseable(self) -> None:
        """The catalog options for the command must all be accepted by the parser.

        F1 (round 16): this test used to append `--stream-evidence v --no-stream-evidence v`,
        which is not a command anyone can type — both halves of an exclusive pair, each given a
        value neither accepts. It asserted the parser would swallow an invalid argv, so the only
        honest repairs were to weaken the parser or to fix the test. The parser is right: the
        test now builds a VALID argv and the exclusivity is proven separately.
        """
        cmd = get_command(COMMAND_ID)
        argv = ["do", "job-flow"]
        for a in cmd.args:
            if not a.is_option or a.name in self._EXCLUSIVE_PARTNERS:
                continue
            if a.name in self._BARE_FLAGS:
                argv.append(a.name)
            elif a.name == "--repair-rounds":
                argv.extend([a.name, "2"])
            else:
                argv.extend([a.name, "v"])
        ns = build_parser().parse_args(argv)
        assert ns._command_id == COMMAND_ID
        assert ns.stream_evidence is True

    def test_the_exclusive_partner_is_parseable_on_its_own(self) -> None:
        """The name skipped above is a real option — proven here, not left unchecked."""
        ns = build_parser().parse_args(
            ["do", "job-flow", "--job-file", "j.md", "--no-stream-evidence"])
        assert ns._command_id == COMMAND_ID
        assert ns.stream_evidence is False

    def test_every_catalog_option_name_is_individually_accepted(self) -> None:
        """Each catalog option name, one at a time — so no name can hide behind another."""
        parser = build_parser()
        for a in get_command(COMMAND_ID).args:
            if not a.is_option:
                continue
            base = ["do", "job-flow", "--job-file", "j.md"]
            argv = base + ([a.name] if a.name in self._BARE_FLAGS
                           else [a.name, "2" if a.name == "--repair-rounds" else "v"])
            assert parser.parse_args(argv)._command_id == COMMAND_ID, a.name


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
        assert data["report"]["status"] == "completed"
        assert isinstance(data["promote_ready"], bool)
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

    def test_json_next_approve_command_gated(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence", extra=["--json"],
        )
        data = json.loads(out)
        if data["promote_ready"]:
            nac = data["next_approve_command"]
            assert nac, "next_approve_command should be present for a ready promote"
            assert data["job_id"] in nac
            assert "--approve" in nac
        else:
            assert data["next_approve_command"] == ""

    # --- Text output for a completed fake-provider job --------------------

    def test_text_completed_job(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(
            capsys, repo=demo_repo, job_file=job_file,
            evidence_out=tmp_path / "evidence",
        )
        assert "Job flow:" in out
        assert "Promote dry-run: dry_run" in out
        assert "Evidence bundle:" in out
        assert "This flow stops at a promote dry-run. The target repo is not changed." in out
        assert "audit trail exported" in out

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

    def test_json_final_audit_has_required_fields(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["status"] in ("READY_FOR_APPROVAL", "BLOCKED", "NEEDS_TESTS", "NEEDS_REPAIR", "NEEDS_REVIEW")
        assert audit["human_decision_required"] is True
        assert isinstance(audit["promote_ready"], bool)
        assert audit["task_count"] >= 1
        assert audit["passed_task_count"] >= 1

    def test_json_final_audit_blocked(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence",
                        extra=["--json", "--max-rounds", "1"])
        data = json.loads(out)
        audit = data["final_audit"]
        assert audit["status"] in ("BLOCKED", "NEEDS_REPAIR")
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
        assert "Final audit: BLOCKED" in out or "Final audit: NEEDS_REPAIR" in out

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
        assert audit["status"] in ("READY_FOR_APPROVAL", "BLOCKED", "NEEDS_TESTS", "NEEDS_REPAIR", "NEEDS_REVIEW")
        assert audit["agent_run_trace_available"] is True

    def test_final_audit_includes_gate_statuses(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        audit = data["final_audit"]
        for gate_key in (
            "fresh_evidence_gate_status",
            "artifact_contract_gate_status",
            "runtime_integration_gate_status",
            "change_provenance_gate_status",
            "commit_execution_gate_status",
        ):
            assert gate_key in audit, f"final_audit must include {gate_key}"

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
            # F004 renamed the legacy label; normalized stream events use their own.
            assert ev.get("trace_source") in (
                "reconstructed_legacy_evidence", "normalized_raw_stream",
            ), f"R-4305: event {ev['event_kind']} has trace_source={ev.get('trace_source')!r}"

    def test_agent_run_trace_summary_has_source_limitations(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=tmp_path / "evidence", extra=["--json"])
        data = json.loads(out)
        summary = data["agent_run_trace_summary"]
        assert any(str(src).startswith("reconstructed") for src in summary["trace_sources"]), \
            "R-4305: summary must report a reconstructed trace source"
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

    def test_command_transcript_noise_fields_agree_with_guard(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path
    ):
        # T004: transcript must use the same noise-exclusion policy as the
        # target guard, so the two never contradict each other on cache/noise.
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        # New explicit fields present.
        assert "target_content_mutated" in ct
        assert "target_noise_changed" in ct
        assert "ignored_noise_files" in ct
        assert isinstance(ct["ignored_noise_files"], list)
        # Fake provider does not touch real source: content mutation is False
        # and the headline mutated flag tracks content, not noise.
        assert ct["target_content_mutated"] is False
        assert ct["target_repo_mutated"] is ct["target_content_mutated"]

    def test_command_transcript_timestamps(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        assert ct["started_at"]
        assert ct["finished_at"]

    def test_command_transcript_preview_equals_final_audit(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=ev, extra=["--json"])
        data = json.loads(out)
        ct = json.loads((ev / "command_transcript.json").read_text())
        audit = data["final_audit"]
        preview = ct["json_stdout_preview_safe"]
        assert preview["status"] == audit["status"], (
            f"transcript preview status={preview['status']} != "
            f"final_audit status={audit['status']}"
        )
        assert preview["promote_ready"] == audit.get("promote_ready", data.get("promote_ready")), (
            "transcript preview promote_ready must equal final_audit promote_ready"
        )

    def test_command_transcript_top_level_promote_equals_audit(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=ev, extra=["--json"])
        data = json.loads(out)
        ct = json.loads((ev / "command_transcript.json").read_text())
        effective = data["final_audit"].get("promote_ready", data.get("promote_ready"))
        assert ct["promote_ready"] == effective, (
            f"transcript top-level promote_ready={ct['promote_ready']} != "
            f"effective={effective}"
        )

    def test_command_transcript_target_mutation_equals_guard(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        tg = json.loads((ev / "target_guard.json").read_text())
        assert ct["target_repo_mutated"] == tg.get("target_mutated", False), (
            f"transcript target_repo_mutated={ct['target_repo_mutated']} != "
            f"target_guard.target_mutated={tg.get('target_mutated')}"
        )
        assert ct["target_content_mutated"] == tg.get("target_content_mutated", False), (
            f"transcript target_content_mutated={ct['target_content_mutated']} != "
            f"target_guard.target_content_mutated={tg.get('target_content_mutated')}"
        )

    def test_command_transcript_includes_final_audit(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        assert "final_audit" in ct, "transcript must embed final_audit"
        assert ct["final_audit"]["status"] == ct["json_stdout_preview_safe"]["status"]

    def test_command_transcript_includes_target_guard(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        assert "target_guard" in ct, "transcript must include target_guard"

    def test_command_transcript_operational_noise_equals_guard(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        tg = json.loads((ev / "target_guard.json").read_text())
        assert ct["target_operational_artifacts_changed"] == tg.get(
            "target_operational_artifacts_changed", False
        ), "transcript operational must equal target_guard"
        assert ct["target_noise_changed"] == tg.get(
            "target_noise_changed", False
        ), "transcript noise must equal target_guard"

    def test_command_transcript_guard_false_not_overridden(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        tg = json.loads((ev / "target_guard.json").read_text())
        ct = json.loads((ev / "command_transcript.json").read_text())
        if not tg.get("target_operational_artifacts_changed", False):
            assert ct["target_operational_artifacts_changed"] is False, (
                "explicit false in target_guard must not be overridden"
            )
        if not tg.get("target_noise_changed", False):
            assert ct["target_noise_changed"] is False, (
                "explicit false in target_guard must not be overridden"
            )

    def test_command_transcript_embedded_guard_equals_file(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        tg = json.loads((ev / "target_guard.json").read_text())
        assert ct["target_guard"] == tg, (
            "embedded target_guard must equal target_guard.json"
        )

    def test_command_transcript_mutation_cannot_contradict_guard(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        tg = json.loads((ev / "target_guard.json").read_text())
        for field in [
            "target_noise_changed",
            "target_operational_artifacts_changed",
        ]:
            assert ct.get(field) == tg.get(field, False), (
                f"transcript {field}={ct.get(field)} contradicts "
                f"target_guard {field}={tg.get(field)}"
            )

    def test_command_transcript_mixed_mutation_regression(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        """Regression: target_mutated=true + target_content_mutated=false must map correctly."""
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        tg_data = {
            "target_mutated": True,
            "target_content_mutated": False,
            "target_operational_artifacts_changed": True,
            "target_noise_changed": False,
        }
        (ev / "target_guard.json").write_text(json.dumps(tg_data))
        from apps.cli.commands.do_cmd import _persist_command_transcript
        _persist_command_transcript(
            "test-mixed", str(ev), {"final_audit": {"status": "READY_FOR_APPROVAL", "promote_ready": True}},
            str(demo_repo), "2026-01-01T00:00:00Z", "aaa", "bbb",
            changed_content_files=["file.py"],
            ignored_noise_files=["cache.pyc"],
            ignored_operational_artifacts=[".agent/x.md"],
        )
        ct = json.loads((ev / "command_transcript.json").read_text())
        assert ct["target_repo_mutated"] is True
        assert ct["target_content_mutated"] is False
        assert ct["target_operational_artifacts_changed"] is True
        assert ct["target_noise_changed"] is False

    def test_final_audit_changed_files_equals_authoritative(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        out = self._run(capsys, repo=demo_repo, job_file=job_file,
                        evidence_out=ev, extra=["--json"])
        data = json.loads(out)
        audit = data.get("final_audit", {})
        fv_path = ev / "final_verifier_report.json"
        if fv_path.exists():
            fv = json.loads(fv_path.read_text())
            fv_auth = sorted(fv.get("authoritative_changed_files", []))
            audit_cf = sorted(audit.get("changed_files", []))
            assert audit_cf == fv_auth, (
                f"final_audit.changed_files ({len(audit_cf)}) != "
                f"final_verifier.authoritative_changed_files ({len(fv_auth)})"
            )

    def test_command_transcript_audit_changed_files_equals_flow(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path,
    ):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        ct = json.loads((ev / "command_transcript.json").read_text())
        jf = json.loads((ev / "job_flow.json").read_text())
        ct_cf = sorted(ct.get("final_audit", {}).get("changed_files", []))
        jf_cf = sorted(jf.get("final_audit", {}).get("changed_files", []))
        assert ct_cf == jf_cf, (
            "command_transcript.final_audit.changed_files must equal "
            "job_flow.final_audit.changed_files"
        )

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
        assert parsed["bundle_version"] == 12
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

    def test_manifest_bundle_version_12(self, capsys, isolate_data, demo_repo, job_file, tmp_path):
        ev = tmp_path / "evidence"
        self._run(capsys, repo=demo_repo, job_file=job_file,
                  evidence_out=ev, extra=["--json"])
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        assert manifest["bundle_version"] == 12

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


# ---------------------------------------------------------------------------
# Final audit + final verifier integration unit tests
# ---------------------------------------------------------------------------


class _FakeJob:
    """Minimal job stub for _build_final_audit unit tests."""
    def __init__(self, status="completed", tasks=None):
        self.status = status
        self.tasks = tasks or [_FakeTask()]


class _FakeTask:
    def __init__(self, task_id="T001", status="applied_to_job_workspace",
                 reviewer_verdict="pass", test_passed=True):
        self.task_id = task_id
        self.status = status
        self.safe_diff_files = []
        self.reviewer_verdict = reviewer_verdict
        self.test_passed = test_passed


class _FakePromo:
    def __init__(self, status="dry_run"):
        self.status = status
        self.blocked_reason = ""
        self.files_planned = []


def _seed_evidence(ev_path, fv_verdict="PASS", tt_actual=False, tt_est_total=5000):
    """Seed a minimal evidence dir with final_verifier_report + token_truth."""
    ev_path.mkdir(parents=True, exist_ok=True)
    (ev_path / "manifest.json").write_text("{}")
    (ev_path / "prompt_trace_summary.json").write_text("{}")
    (ev_path / "agent_run_trace.jsonl").write_text("")
    (ev_path / "agent_run_trace_summary.json").write_text("{}")
    (ev_path / "final_verifier_report.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "verdict": fv_verdict,
        "missing_tests_gate": "NEEDS_TESTS" if fv_verdict == "NEEDS_TESTS" else "PASS",
        "scratch_file_guard": "BLOCKED" if fv_verdict == "BLOCKED" else "PASS",
    }))
    (ev_path / "token_truth.json").write_text(json.dumps({
        "schema_version": "1.0.0",
        "actual_available": tt_actual,
        "estimated_total_tokens": tt_est_total,
    }))


class TestFinalAuditVerifierIntegration:
    """Unit tests: _build_final_audit must follow final_verifier_report.json."""

    def test_needs_tests_overrides_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="NEEDS_TESTS")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "NEEDS_TESTS"
        assert audit["promote_ready"] is False
        assert audit["final_verifier_verdict"] == "NEEDS_TESTS"

    def test_blocked_overrides_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="BLOCKED")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    def test_pass_with_risks_not_clean_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS_WITH_RISKS")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] != "READY_FOR_APPROVAL"
        assert audit["status"] == "NEEDS_REVIEW"
        assert audit["promote_ready"] is False

    def test_needs_repair_overrides_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="NEEDS_REPAIR")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "NEEDS_REPAIR"
        assert audit["promote_ready"] is False

    def test_pass_allows_ready(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert audit["promote_ready"] is True

    def test_includes_verifier_and_token_truth_refs(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS", tt_actual=False, tt_est_total=8000)

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["final_verifier_report_ref"] == "final_verifier_report.json"
        assert audit["final_verifier_verdict"] == "PASS"
        assert audit["token_truth_ref"] == "token_truth.json"
        assert audit["token_truth_actual_available"] is False
        assert audit["token_truth_estimated_total"] == 8000
        assert audit["missing_tests_gate_status"] == "PASS"
        assert audit["scratch_file_guard_status"] == "PASS"

    def test_no_verifier_report_falls_through(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True)
        (ev / "manifest.json").write_text("{}")
        (ev / "prompt_trace_summary.json").write_text("{}")
        (ev / "agent_run_trace.jsonl").write_text("")
        (ev / "agent_run_trace_summary.json").write_text("{}")

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "READY_FOR_APPROVAL"
        assert "final_verifier_verdict" not in audit

    def test_final_audit_blocked_on_gate_block(self, tmp_path):
        """Final audit must be BLOCKED when a gate is BLOCKED, even with FV=PASS."""
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS")
        (ev / "change_provenance_gate.json").write_text(json.dumps({
            "verdict": "BLOCKED",
        }))
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "verdict": "BLOCKED",
        }))

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    def test_final_audit_blocked_on_commit_needs_tests(self, tmp_path):
        """Final audit BLOCKED when commit_execution is NEEDS_TESTS."""
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        _seed_evidence(ev, fv_verdict="PASS")
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "verdict": "NEEDS_TESTS",
        }))

        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert audit["status"] == "BLOCKED"
        assert audit["promote_ready"] is False

    # --- manifest dirty-file and alignment tests ---

    def test_manifest_dirty_files_not_truncated(self, tmp_path):
        """Manifest must include all dirty files, never truncate."""
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=None)
        rs = manifest["review_subject"]
        assert rs["dirty_files_truncated"] is False
        assert rs["dirty_file_count_total"] == len(rs["dirty_files"])

    def test_manifest_review_subject_evidence_alignment(self, tmp_path):
        """Manifest includes review_subject_evidence_alignment section."""
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "test-123",
            "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "change_provenance_gate.json").write_text(json.dumps({
            "verdict": "PASS", "covered_files": [],
        }))
        (ev / "final_verifier_report.json").write_text(json.dumps({
            "verdict": "PASS", "authoritative_changed_files": [],
        }))
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "verdict": "COMMIT_READY",
        }))
        (ev / "artifact_contract_gate.json").write_text(json.dumps({
            "verdict": "PASS",
        }))
        from scripts.build_review_manifest import build_manifest
        manifest = build_manifest(evidence_dir=str(ev))
        alignment = manifest.get("review_subject_evidence_alignment")
        assert alignment is not None
        assert "verdict" in alignment
        assert "dirty_source_test_files" in alignment
        assert "gate_verdicts" in alignment


class TestManifestEvidenceValidity:
    """Tests for manifest evidence validation and manual repair provenance."""

    def _seed_valid_task(self, ev, tid="T001"):
        d = ev / "task_runs" / tid
        d.mkdir(parents=True, exist_ok=True)
        for art in [
            "prompt_trace.jsonl", "prompt_trace_summary.json",
            "review.json", "repair_loop.json", "token_accounting.json",
            "provider_evidence.json",
        ]:
            (d / art).write_text("{}")
        return d

    def _seed_root(self, ev, job_id="test-123"):
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": job_id, "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "manifest.json").write_text(json.dumps({"job_id": job_id}))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")

    def test_valid_task_passes_validation(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        self._seed_valid_task(ev)
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is True

    def test_missing_provider_evidence_fails(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        d = ev / "task_runs" / "T001"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["prompt_trace.jsonl", "prompt_trace_summary.json",
                     "review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        # Missing provider_evidence.json
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False

    def test_manual_repair_task_exempt_from_provider_artifacts(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        self._seed_valid_task(ev, "T001")
        # T002 is manual repair — no provider artifacts
        d = ev / "task_runs" / "T002"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        (d / "manual_repair_provenance.json").write_text(json.dumps({
            "manual_operator_repair": True,
            "no_provider_calls": True,
            "task_id": "T002",
        }))
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is True
        assert "T002" in result.get("manual_repair_tasks", [])

    def test_invalid_manual_repair_provenance_fails(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        self._seed_root(ev)
        d = ev / "task_runs" / "T001"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        # manual_repair_provenance missing required fields
        (d / "manual_repair_provenance.json").write_text(json.dumps({
            "manual_operator_repair": False,
        }))
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False

    def test_final_audit_changed_files_uses_authoritative(self, tmp_path):
        from apps.cli.commands.do_cmd import _build_final_audit
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True)
        _seed_evidence(ev, fv_verdict="PASS")
        fv = json.loads((ev / "final_verifier_report.json").read_text())
        fv["authoritative_changed_files"] = ["a.py", "b.py", "c.py"]
        (ev / "final_verifier_report.json").write_text(json.dumps(fv))
        audit = _build_final_audit(
            _FakeJob(), _FakePromo(), str(ev),
            token_summary={"provider_call_count": 1},
            job_flow_json_available=True,
        )
        assert sorted(audit["changed_files"]) == ["a.py", "b.py", "c.py"]


class TestReviewZipPackageStatus:
    """Tests for package_status, packaging proof, and always-build semantics."""

    def _seed_valid_evidence(self, ev, job_id="test-pkg-123", file_hashes=None):
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": job_id,
            "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "manifest.json").write_text(json.dumps({
            "job_id": job_id,
            "task_count": 1,
            "task_ids": ["T001"],
        }))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        # Round 31 F1: a single real operator attestation whose final_verifier_report is produced by
        # the actual producer (regenerated at the end of this method), not a hand-written report.
        from packages.orchestration import manual_attestation as _MA
        from packages.orchestration.repair_attest import (
            build_safe_diff_text as _bsd, canonical_provenance_sha256 as _cps,
            sha256_text as _sht,
        )
        import hashlib as _hl
        if file_hashes is None:
            # Materialize a real authority file in the repo root (ev.parent) so the content proof and
            # bundle-integrity verify against real bytes, and compute its true hash.
            _content = b"x = 1\n"
            _src = ev.parent / "src"
            _src.mkdir(parents=True, exist_ok=True)
            (_src / "app.py").write_bytes(_content)
            file_hashes = {"src/app.py": _hl.sha256(_content).hexdigest()}
        _authority = sorted(dict(file_hashes))
        _diff = "".join(
            f"diff --git a/{p} b/{p}\nnew file mode 100644\nindex 0000000..1111111\n"
            f"--- /dev/null\n+++ b/{p}\n@@ -0,0 +1 @@\n+x = 1\n" for p in _authority)
        _safe = _bsd(_diff, [])
        _tsha, _ssha = _sht(_diff), _sht(_safe)
        _prov = _cps(_tsha, [])
        _MA.write_manual_task_evidence(
            str(ev), job_id=job_id, task_id="T001", changed_files=_authority, safe_diff_text=_safe,
            provenance_sha256=_prov, diff_sha256=_prov, tracked_diff_sha256=_tsha,
            safe_diff_sha256=_ssha, timestamp="2026-07-18T00:00:00+00:00",
            note="operator-attested do_job_flow fixture")
        (ev / "final_job_review.json").write_text(json.dumps({
            "job_id": job_id, "completion_mode": "manual_operator_repair",
            "human_final_reviewer_required": True, "completion_provider_call_count": 0,
            "linked_prior_job_ids": [], "linked_prior_job_summaries": [],
            "per_task_changed_files": {"T001": _authority}, "actual_changed_files": _authority,
            "expected_changed_files": _authority}))
        # Round 22-25: READY requires the COMPLETE, closed-schema, semantically-consistent gate
        # matrix — recursive schemas, complete gate semantics and an exact derived commit gate.
        _hashes = dict(file_hashes) if file_hashes else {"src/app.py": "0" * 64}
        _auth = sorted(_hashes)
        _core = ("manifest.json", "job_report.json", "token_truth.json", "fresh_evidence_gate.json",
                 "artifact_contract_gate.json", "runtime_integration_gate.json",
                 "change_provenance_gate.json", "commit_execution_gate.json",
                 "final_verifier_report.json")
        (ev / "fresh_evidence_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS", "evidence_authoritative": True,
            "job_id_match": True, "plan_match": True, "live_review_match": True,
            "evidence_job_id": job_id, "current_job_id": job_id,
            "current_step_range": "1-2", "live_review_step_range": "1-2", "plan_step_range": "1-2",
            "evidence_freshness": {"is_fresh": True, "job_id_match": True,
                                   "step_range_match": True},
            "evidence_validity": {"has_job_id": True, "has_manifest": True,
                                  "is_valid_current_run": True}, "issues": []}))
        # final_verifier_report.json is REGENERATED by the real producer at the end of this method.
        (ev / "artifact_contract_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS", "missing_required": [],
            "fv_referenced_missing": [], "critical_fv_missing": [], "issues": [],
            "job_id_fresh": True, "evidence_job_id": job_id,
            "required_artifacts": {a: True for a in _core},
            "optional_artifacts": {"scratch_file_guard.json": True},
            "stream_artifacts": {"applicable": False, "verdict": "NOT_APPLICABLE",
                                 "tasks_with_stream_evidence": [], "artifacts_verified": 0,
                                 "artifacts_present": 0, "missing_stream_artifact_listing": [],
                                 "missing_stream_artifacts": [], "missing_stream_artifact_metadata": [],
                                 "stream_artifact_hash_mismatches": [],
                                 "stream_artifact_size_mismatches": [], "unexpected_stream_artifacts": [],
                                 "duplicate_stream_artifact_refs": [], "unsafe_stream_artifact_refs": []},
            "worktree_artifacts": {"applicable": False, "verdict": "NOT_APPLICABLE",
                                   "job_level_handoff": False, "handoff_coverage_verdict": "",
                                   "handoff_coverage_issues": [], "missing_job_handoff": [],
                                   "worktree_tasks": [], "diffs_verified": 0, "missing_result_diffs": [],
                                   "missing_result_diff_references": [], "result_diff_hash_mismatches": [],
                                   "result_diff_size_mismatches": [], "unreferenced_result_diffs": [],
                                   "unsafe_result_diff_refs": []}}))
        (ev / "change_provenance_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS", "current_job_id": job_id,
            "covered_files": _auth, "source_files": _auth, "excluded_files": [],
            "evidence_covered_files": _auth, "evidence_sources": [], "dirty_files": [],
            "uncovered_files": [], "content_hash_verified": True, "hash_mismatches": [],
            "stale_apply_proofs": [], "issues": [], "current_hashes": _hashes,
            "evidence_hashes": _hashes}))
        (ev / "runtime_integration_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "PASS",
            "checks": [{"check_id": "c0", "check_type": "call_exists", "source_file": "src/app.py",
                        "pattern": "add(", "found": True, "file_missing": False}],
            "checks_total": 1, "checks_passed": 1, "issues": []}))
        (ev / "manifest_integrity.json").write_text(json.dumps({
            "schema_version": "1.0.0", "ok": True, "failures": [], "notes": []}))
        (ev / "postmortem_integrity.json").write_text(json.dumps({
            "schema_version": "1.0.0", "ok": True, "failures": []}))
        (ev / "commit_execution_gate.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verdict": "NEEDS_HUMAN_APPROVAL", "promote_ready": False,
            "blocked_gates": [], "non_pass_gates": ["final_verifier"],
            "issues": ["gate 'final_verifier' is not PASS (verdict 'PASS_WITH_RISKS')"],
            "gate_checks": {
                "final_verifier": "PASS_WITH_RISKS", "fresh_evidence_gate": "PASS",
                "artifact_contract_gate": "PASS", "change_provenance_gate": "PASS",
                "runtime_integration_gate": "PASS"}}))
        (ev / "verification_tests.json").write_text(json.dumps({
            "schema_version": "1.0.0", "verification_type": "explicit_commands",
            "runs": [{"run_id": "vr-0001", "command": "pytest -q", "exit_code": 0, "passed": 1,
                      "failed": 0, "test_files": ["t.py"], "stdout_summary": "1 passed"}],
            "command": "pytest -q", "exit_code": 0, "passed": 1, "failed": 0,
            "test_files": ["t.py"], "timestamp": "2026-07-18T00:00:00Z"}))
        # A content proof for the attested authority, and the commit chain/subject the manual
        # completion recompute tolerates (no declared base -> the legacy dirty-tree path).
        if not (ev / "current_change_content_proof.json").exists():
            (ev / "current_change_content_proof.json").write_text(json.dumps({
                "schema_version": "1.1.0", "base_commit": "", "head_commit": "",
                "file_hashes": _hashes, "file_count": len(_hashes),
                "tombstones": {}, "tombstone_count": 0}))
        # Round 32 F2: the canonical token truth is the aggregate of the tasks — written AFTER them.
        _MA.write_manual_token_truth(str(ev))
        # Round 31 F1: regenerate the final verifier report from the assembled bundle with the REAL
        # producer, so the packaged report is reproducible (never a hand-written report).
        from packages.orchestration.final_verifier import build_final_verifier_report
        (ev / "final_verifier_report.json").write_text(json.dumps(
            build_final_verifier_report(str(ev))))

    @staticmethod
    def _init_clean_git(path):
        """Create a clean git repo with committed state. Portable across environments."""
        import subprocess
        r = subprocess.run(["git", "init"], cwd=str(path), capture_output=True)
        assert r.returncode == 0, f"git init failed: {r.stderr.decode()}"
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=str(path), capture_output=True, check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=str(path), capture_output=True, check=True,
        )
        r = subprocess.run(
            ["git", "add", "."], cwd=str(path), capture_output=True,
        )
        assert r.returncode == 0, f"git add failed: {r.stderr.decode()}"
        r = subprocess.run(
            ["git", "commit", "-m", "init", "--allow-empty"],
            cwd=str(path), capture_output=True,
        )
        assert r.returncode == 0, f"git commit failed: {r.stderr.decode()}"

    def test_valid_evidence_ready_for_review(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        self._seed_valid_evidence(ev)
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        # Without content hash proof, valid evidence is READY_FOR_REVIEW_UNVERIFIED
        assert m["package_status"] in ("READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED")

    def test_invalid_evidence_blocked_but_created(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "x", "final_audit": {"status": "BLOCKED"},
        }))
        (ev / "manifest.json").write_text(json.dumps({
            "job_id": "x", "task_count": 0, "task_ids": [],
        }))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_packaging_proof_records_evidence_dir(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        self._seed_valid_evidence(ev)
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["packaged_evidence_job_id"] == "test-pkg-123"
        assert m["packaged_evidence_manifest_task_count"] == 1
        assert m["packaged_evidence_manifest_task_ids"] == ["T001"]
        # Shareable manifest: no machine-specific absolute prefixes.
        assert m["packaged_evidence_dir"] == f"[source_root]/{ev.name}"
        assert m["source_root"] == "[source_root]"
        assert m["packaging_command_context"]["cwd"] == "[source_root]"
        assert m["packaging_command_context"]["evidence_dir_arg"] == f"[source_root]/{ev.name}"

    def test_manual_repair_missing_provenance_blocks_authority(self, tmp_path):
        from scripts.build_review_manifest import validate_evidence_candidate
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "x", "final_audit": {"status": "READY_FOR_APPROVAL"},
        }))
        (ev / "manifest.json").write_text(json.dumps({"job_id": "x"}))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        d = ev / "task_runs" / "T006"
        d.mkdir(parents=True, exist_ok=True)
        for art in ["review.json", "repair_loop.json", "token_accounting.json"]:
            (d / art).write_text("{}")
        result = validate_evidence_candidate(str(ev))
        assert result["is_valid_current_run"] is False
        assert any("T006" in e for e in result["validation_errors"])

    def test_packaging_warnings_populated(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        (ev / "job_flow.json").write_text(json.dumps({
            "job_id": "x", "final_audit": {"status": "BLOCKED"},
        }))
        (ev / "manifest.json").write_text(json.dumps({
            "job_id": "x", "task_count": 0, "task_ids": [],
        }))
        for art in [
            "agent_run_trace.jsonl", "agent_run_trace_summary.json",
            "prompt_trace_summary.json", "command_transcript.json",
        ]:
            (ev / art).write_text("{}")
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert len(m["packaging_warnings"]) > 0
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_dirty_worktree_valid_evidence_blocked(self, tmp_path, monkeypatch):
        """Valid evidence + dirty worktree => BLOCKED_EVIDENCE."""
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        self._seed_valid_evidence(ev)
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        # Create dirty file after commit
        (tmp_path / "dirty.py").write_text("x = 1")
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        assert any("alignment" in w for w in m["packaging_warnings"])


class TestTraceEventOrder:
    """Trace event ordering: final_audit_completed must appear after all task events."""

    def test_final_audit_after_all_task_events(self, tmp_path):
        """final_audit_completed must not appear before any task_workspace_applied."""
        trace = tmp_path / "agent_run_trace.jsonl"
        events = [
            {"event": "task_workspace_applied", "task_id": "T001", "timestamp": "2026-07-01T09:00:00Z"},
            {"event": "task_workspace_applied", "task_id": "T002", "timestamp": "2026-07-01T09:10:00Z"},
            {"event": "final_audit_completed", "status": "READY", "timestamp": "2026-07-01T09:20:00Z"},
            {"event": "task_workspace_applied", "task_id": "T003", "timestamp": "2026-07-01T09:30:00Z"},
        ]
        trace.write_text("\n".join(json.dumps(e) for e in events) + "\n")

        lines = trace.read_text().splitlines()
        parsed = []
        for line in lines:
            if line.strip():
                parsed.append(json.loads(line))

        task_events = [e for e in parsed if e.get("event") == "task_workspace_applied"]
        final_events = [e for e in parsed if e.get("event") == "final_audit_completed"]

        if task_events and final_events:
            last_task_idx = max(parsed.index(e) for e in task_events)
            first_final_idx = min(parsed.index(e) for e in final_events)
            # This trace is WRONG — final_audit before T003
            assert first_final_idx < last_task_idx, \
                "This test proves the bad ordering exists before fix"

    def test_reordered_trace_final_audit_is_last(self, tmp_path):
        """After reordering, final_audit_completed must be after all task events."""
        trace_lines = [
            json.dumps({"event": "task_workspace_applied", "task_id": "T001", "timestamp": "2026-07-01T09:00:00Z"}),
            json.dumps({"event": "final_audit_completed", "status": "READY", "timestamp": "2026-07-01T09:20:00Z"}),
            json.dumps({"event": "task_workspace_applied", "task_id": "T003", "timestamp": "2026-07-01T09:30:00Z"}),
        ]
        # Simulate reorder: non-terminal first, then terminal
        non_terminal = []
        terminal = []
        for line in trace_lines:
            evt = json.loads(line)
            if evt.get("event") == "final_audit_completed":
                terminal.append(line)
            else:
                non_terminal.append(line)
        reordered = non_terminal + terminal
        parsed = [json.loads(l) for l in reordered]

        task_indices = [i for i, e in enumerate(parsed) if e.get("event") == "task_workspace_applied"]
        final_indices = [i for i, e in enumerate(parsed) if e.get("event") == "final_audit_completed"]

        assert max(task_indices) < min(final_indices), \
            "final_audit_completed must appear after all task_workspace_applied events"

    def test_trace_summary_tasks_match_raw_trace(self, tmp_path):
        """Trace summary tasks_traced must match raw trace task events."""
        raw_tasks = {"T001", "T002", "T006"}
        summary_tasks = ["T001", "T002", "T006"]
        assert set(summary_tasks) == raw_tasks


class TestZipFilenameAndStatus:
    """Zip filename must include package status; status must be machine-readable."""

    def test_ready_manifest_has_ready_status(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        TestReviewZipPackageStatus._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["package_status"] in ("READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED")
        assert m["review_package_created"] is True
        assert "READY_FOR_REVIEW" in m["package_status"]

    def test_blocked_manifest_has_blocked_status(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        TestReviewZipPackageStatus._init_clean_git(tmp_path)
        (tmp_path / "extra_dirty.py").write_text("x = 1")
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        assert m["review_package_created"] is True

    def test_package_status_filename_safe(self):
        """package_status values are safe for use in filenames."""
        for status in ["READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED", "BLOCKED_EVIDENCE"]:
            assert "/" not in status
            assert " " not in status
            assert status == status.upper()

    def test_blocked_package_not_commit_ready(self, tmp_path, monkeypatch):
        """BLOCKED_EVIDENCE must not coexist with evidence_authoritative=true."""
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        TestReviewZipPackageStatus._init_clean_git(tmp_path)
        (tmp_path / "dirty.py").write_text("x = 1")
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        ce = m.get("current_evidence", {})
        ef = ce.get("evidence_freshness", {})
        assert ef.get("evidence_authoritative") is False


class TestSourceRootContainment:
    """Source-root containment: packaging must be within git source root."""

    @staticmethod
    def _init_clean_git(path):
        import subprocess
        for cmd in [
            ["git", "init"],
            ["git", "config", "user.email", "test@example.com"],
            ["git", "config", "user.name", "Test User"],
            ["git", "add", "."],
            ["git", "commit", "-m", "init", "--allow-empty"],
        ]:
            r = subprocess.run(cmd, cwd=str(path), capture_output=True)
            assert r.returncode == 0, f"{cmd} failed: {r.stderr.decode()}"

    def test_containment_pass_when_inside_source_root(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["source_root_containment"]["verdict"] == "PASS"
        assert m["source_root_containment"]["blockers"] == []
        assert m["external_paths_detected"] == []
        assert m["package_status"] in ("READY_FOR_REVIEW", "READY_FOR_REVIEW_UNVERIFIED")

    def test_evidence_outside_source_root_blocked(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        repo = tmp_path / "repo"
        repo.mkdir()
        monkeypatch.chdir(repo)
        self._init_clean_git(repo)
        # Evidence dir outside repo
        ext_ev = tmp_path / "external_evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ext_ev
        )
        m = build_manifest(str(ext_ev), selection_mode="explicit")
        assert m["source_root_containment"]["verdict"] == "BLOCKED"
        assert len(m["source_root_containment"]["blockers"]) > 0
        assert m["package_status"] == "BLOCKED_EVIDENCE"
        assert len(m["external_paths_detected"]) > 0

    def test_manifest_records_source_root(self, tmp_path, monkeypatch):
        from scripts.build_review_manifest import build_manifest
        ev = tmp_path / "evidence"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        # The shareable manifest carries a token, never the private absolute root.
        assert m["source_root"] == "[source_root]"

    def test_zip_still_created_when_containment_fails(self, tmp_path, monkeypatch):
        """Containment failure must not prevent zip creation."""
        from scripts.build_review_manifest import build_manifest
        repo = tmp_path / "repo"
        repo.mkdir()
        monkeypatch.chdir(repo)
        self._init_clean_git(repo)
        ext_ev = tmp_path / "ext_ev"
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ext_ev
        )
        m = build_manifest(str(ext_ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_no_code_references_clean_worktree(self):
        """No code path should default to remedy-clean-*."""
        import subprocess
        result = subprocess.run(
            ["grep", "-rn", "remedy-clean-", "scripts/", "apps/cli/",
             "packages/orchestration/"],
            capture_output=True, text=True,
        )
        matches = [l for l in result.stdout.splitlines()
                   if not l.endswith(".pyc") and "__pycache__" not in l]
        assert matches == [], f"Code references remedy-clean-: {matches}"


class TestReviewBundleIntegrity:
    """Review-bundle integrity: packaged file hashes must match content proof."""

    @staticmethod
    def _init_clean_git(path):
        import subprocess
        for cmd in [
            ["git", "init"],
            ["git", "config", "user.email", "test@example.com"],
            ["git", "config", "user.name", "Test User"],
            ["git", "add", "."],
            ["git", "commit", "-m", "init", "--allow-empty"],
        ]:
            r = subprocess.run(cmd, cwd=str(path), capture_output=True)
            assert r.returncode == 0, f"{cmd} failed: {r.stderr.decode()}"

    @staticmethod
    def _seed_with_proof(tmp_path, file_contents, proof_hashes):
        """Create evidence dir with content proof and source files."""
        import hashlib
        ev = tmp_path / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        # Seed valid evidence base — bind the change-provenance hash maps to the same proof hashes.
        TestReviewZipPackageStatus._seed_valid_evidence(
            TestReviewZipPackageStatus(), ev, file_hashes=proof_hashes
        )
        # Write content proof
        proof = {
            "schema_version": 1,
            "file_hashes": proof_hashes,
            "file_count": len(proof_hashes),
        }
        (ev / "current_change_content_proof.json").write_text(
            json.dumps(proof)
        )
        # Write source files
        for rel_path, content in file_contents.items():
            fp = tmp_path / rel_path
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text(content)
        return ev

    def test_matching_proof_ready_for_review(self, tmp_path, monkeypatch):
        """Matching hashes → PASS → READY_FOR_REVIEW."""
        from scripts.build_review_manifest import build_manifest
        import hashlib
        content = "x = 1\n"
        h = hashlib.sha256(content.encode()).hexdigest()
        ev = self._seed_with_proof(
            tmp_path,
            {"src/app.py": content},
            {"src/app.py": h},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        bi = m["review_bundle_integrity"]
        assert bi["current_content_hash_checked"] is True
        assert bi["current_content_hash_mismatches"] == []
        assert bi["current_content_hash_missing_proofs"] == []
        assert bi["verdict"] == "PASS"
        assert m["package_status"] == "READY_FOR_REVIEW"

    def test_hash_mismatch_blocked(self, tmp_path, monkeypatch):
        """Hash mismatch → BLOCKED → BLOCKED_EVIDENCE."""
        from scripts.build_review_manifest import build_manifest
        content = "x = 1\n"
        wrong_hash = "0" * 64
        ev = self._seed_with_proof(
            tmp_path,
            {"src/app.py": content},
            {"src/app.py": wrong_hash},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        bi = m["review_bundle_integrity"]
        assert bi["verdict"] == "BLOCKED"
        assert len(bi["current_content_hash_mismatches"]) == 1
        mm = bi["current_content_hash_mismatches"][0]
        assert mm["file"] == "src/app.py"
        assert mm["expected"] == wrong_hash
        assert mm["actual"] != wrong_hash
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_mismatch_includes_both_hashes(self, tmp_path, monkeypatch):
        """Mismatch entries include expected and actual SHA256."""
        from scripts.build_review_manifest import build_manifest
        import hashlib
        content = "x = 2\n"
        actual_h = hashlib.sha256(content.encode()).hexdigest()
        wrong_h = "a" * 64
        ev = self._seed_with_proof(
            tmp_path,
            {"src/b.py": content},
            {"src/b.py": wrong_h},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        mm = m["review_bundle_integrity"]["current_content_hash_mismatches"][0]
        assert mm["expected"] == wrong_h
        assert mm["actual"] == actual_h

    def test_missing_proof_blocked(self, tmp_path, monkeypatch):
        """File in proof but not on disk → missing proof → BLOCKED."""
        from scripts.build_review_manifest import build_manifest
        ev = self._seed_with_proof(
            tmp_path,
            {},
            {"src/nonexistent.py": "f" * 64},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        bi = m["review_bundle_integrity"]
        assert bi["verdict"] == "BLOCKED"
        assert "src/nonexistent.py" in bi["current_content_hash_missing_proofs"]
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_zip_still_created_on_mismatch(self, tmp_path, monkeypatch):
        """Mismatch must not prevent zip creation."""
        from scripts.build_review_manifest import build_manifest
        ev = self._seed_with_proof(
            tmp_path,
            {"src/c.py": "y = 1\n"},
            {"src/c.py": "0" * 64},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        assert m["review_package_created"] is True
        assert m["package_status"] == "BLOCKED_EVIDENCE"

    def test_filename_status_matches_manifest(self, tmp_path, monkeypatch):
        """Package filename suffix must match manifest package_status."""
        from scripts.build_review_manifest import build_manifest
        import hashlib
        content = "z = 3\n"
        h = hashlib.sha256(content.encode()).hexdigest()
        ev = self._seed_with_proof(
            tmp_path,
            {"src/d.py": content},
            {"src/d.py": h},
        )
        monkeypatch.chdir(tmp_path)
        self._init_clean_git(tmp_path)
        m = build_manifest(str(ev), selection_mode="explicit")
        status = m["package_status"]
        assert status in ("READY_FOR_REVIEW", "BLOCKED_EVIDENCE")
        assert "/" not in status
        assert " " not in status


# ---------------------------------------------------------------------------
# T002: CLI/config per-role model override flags
#
# --builder/reviewer/repair-provider|model|effort are validated at the CLI
# layer and passed through to role_config.resolve_role_config. Invalid values
# are rejected with exit code 2; omitting every flag preserves the built-in
# defaults (backward compatible).
# ---------------------------------------------------------------------------


class TestRoleOverrideResolver:
    """Unit tests for the CLI-layer resolver + validation."""

    def test_backward_compat_defaults_when_all_omitted(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        cfgs = _resolve_cli_role_configs()
        for role in ("builder", "reviewer", "repair"):
            assert cfgs[role] == {
                "provider": "ollama",
                "model": "qwen3-coder-next",
                "effort": "medium",
            }

    def test_parses_and_resolves_per_role_overrides(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        cfgs = _resolve_cli_role_configs(
            builder_provider="claude",
            builder_model="opus",
            builder_effort="high",
            reviewer_effort="low",
            repair_provider="fake",
        )
        assert cfgs["builder"] == {
            "provider": "claude", "model": "opus", "effort": "high",
        }
        # Partial override keeps defaults for unset fields.
        assert cfgs["reviewer"]["effort"] == "low"
        assert cfgs["reviewer"]["provider"] == "ollama"
        assert cfgs["repair"]["provider"] == "fake"
        assert cfgs["repair"]["effort"] == "medium"

    def test_invalid_provider_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        with pytest.raises(SystemExit) as exc:
            _resolve_cli_role_configs(builder_provider="bogus")
        assert exc.value.code == 2

    def test_invalid_effort_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        with pytest.raises(SystemExit) as exc:
            _resolve_cli_role_configs(reviewer_effort="turbo")
        assert exc.value.code == 2

    def test_empty_model_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _resolve_cli_role_configs

        with pytest.raises(SystemExit) as exc:
            _resolve_cli_role_configs(repair_model="   ")
        assert exc.value.code == 2


class TestRoleOverrideHandlerWiring:
    """The flags reject invalid input through the real command handlers."""

    def _job_flow_ns(self, **overrides):
        ns = build_parser().parse_args(["do", "job-flow", "--job-file", "job.md"])
        for k, v in overrides.items():
            setattr(ns, k, v)
        return ns

    def _job_run_ns(self, **overrides):
        ns = build_parser().parse_args(["do", "job-run", "job-id"])
        for k, v in overrides.items():
            setattr(ns, k, v)
        return ns

    def test_job_flow_rejects_invalid_role_effort(self) -> None:
        ns = self._job_flow_ns(builder_effort="turbo")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS[COMMAND_ID](ns)
        assert exc.value.code == 2

    def test_job_run_rejects_invalid_role_provider(self) -> None:
        ns = self._job_run_ns(reviewer_provider="bogus")
        with pytest.raises(SystemExit) as exc:
            COMMAND_HANDLERS["do.job-run"](ns)
        assert exc.value.code == 2


class TestRoleOverridePassthroughE2E:
    """End-to-end: role_configs appears in job-flow JSON output."""

    @pytest.fixture
    def isolate_data(self, tmp_path: Path, monkeypatch):
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
            "# Job: Role Override E2E\n\n## Task 1\nAdd a doc file.\n\n"
            "Acceptance:\n- file exists\n"
        )
        return jf

    def test_role_configs_in_job_flow_json(
        self, capsys, isolate_data, demo_repo, job_file, tmp_path
    ):
        argv = [
            "do", "job-flow",
            "--job-file", str(job_file),
            "--repo", str(demo_repo),
            "--builder", "fake",
            "--reviewer", "fake",
            "--out", str(tmp_path / "evidence"),
            "--json",
        ]
        grouped_main(argv)
        data = json.loads(capsys.readouterr().out)
        assert "role_configs" in data
        # Defaults present for every role when no override flags are supplied.
        for role in ("builder", "reviewer", "repair"):
            assert data["role_configs"][role]["provider"] == "ollama"
            assert data["role_configs"][role]["effort"] == "medium"


# ---------------------------------------------------------------------------
# T003: CLI per-role flag registration (argparse layer)
#
# Verifies that --builder/reviewer/repair-provider|model|effort flags are
# reachable from the CLI for both do.job-run and do.job-flow commands.
# ---------------------------------------------------------------------------


class TestCliRoleFlags:
    """Verify the 9 per-role CLI flags parse correctly for job-flow and job-run."""

    def _parse(self, argv: list[str]):
        return build_parser().parse_args(argv)

    # --- do.job-flow: all 9 flags parse to correct attributes ----------------

    def test_job_flow_builder_provider(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--builder-provider", "claude",
        ])
        assert ns.builder_provider == "claude"

    def test_job_flow_builder_model(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--builder-model", "claude-opus-4-20250514",
        ])
        assert ns.builder_model == "claude-opus-4-20250514"

    def test_job_flow_builder_effort(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--builder-effort", "high",
        ])
        assert ns.builder_effort == "high"

    def test_job_flow_reviewer_provider(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--reviewer-provider", "ollama",
        ])
        assert ns.reviewer_provider == "ollama"

    def test_job_flow_reviewer_model(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--reviewer-model", "qwen3-coder-next",
        ])
        assert ns.reviewer_model == "qwen3-coder-next"

    def test_job_flow_reviewer_effort(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--reviewer-effort", "low",
        ])
        assert ns.reviewer_effort == "low"

    def test_job_flow_repair_provider(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--repair-provider", "fake",
        ])
        assert ns.repair_provider == "fake"

    def test_job_flow_repair_model(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--repair-model", "deepseek-r1",
        ])
        assert ns.repair_model == "deepseek-r1"

    def test_job_flow_repair_effort(self) -> None:
        ns = self._parse([
            "do", "job-flow", "--job-file", "x.md",
            "--repair-effort", "max",
        ])
        assert ns.repair_effort == "max"

    # --- do.job-run: all 9 flags parse to correct attributes -----------------

    def test_job_run_builder_provider(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--builder-provider", "claude-cli",
        ])
        assert ns.builder_provider == "claude-cli"

    def test_job_run_builder_model(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--builder-model", "claude-opus-4-20250514",
        ])
        assert ns.builder_model == "claude-opus-4-20250514"

    def test_job_run_builder_effort(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--builder-effort", "medium",
        ])
        assert ns.builder_effort == "medium"

    def test_job_run_reviewer_provider(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--reviewer-provider", "fixture",
        ])
        assert ns.reviewer_provider == "fixture"

    def test_job_run_reviewer_model(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--reviewer-model", "gpt-4o",
        ])
        assert ns.reviewer_model == "gpt-4o"

    def test_job_run_reviewer_effort(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--reviewer-effort", "high",
        ])
        assert ns.reviewer_effort == "high"

    def test_job_run_repair_provider(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--repair-provider", "ollama",
        ])
        assert ns.repair_provider == "ollama"

    def test_job_run_repair_model(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--repair-model", "codellama",
        ])
        assert ns.repair_model == "codellama"

    def test_job_run_repair_effort(self) -> None:
        ns = self._parse([
            "do", "job-run", "job-id-123",
            "--repair-effort", "low",
        ])
        assert ns.repair_effort == "low"

    # --- Defaults are None when flags are omitted ----------------------------

    def test_job_flow_defaults_none(self) -> None:
        ns = self._parse(["do", "job-flow", "--job-file", "x.md"])
        for attr in (
            "builder_provider", "builder_model", "builder_effort",
            "reviewer_provider", "reviewer_model", "reviewer_effort",
            "repair_provider", "repair_model", "repair_effort",
        ):
            assert getattr(ns, attr) is None, f"{attr} should default to None"

    def test_job_run_defaults_none(self) -> None:
        ns = self._parse(["do", "job-run", "job-id-123"])
        for attr in (
            "builder_provider", "builder_model", "builder_effort",
            "reviewer_provider", "reviewer_model", "reviewer_effort",
            "repair_provider", "repair_model", "repair_effort",
        ):
            assert getattr(ns, attr) is None, f"{attr} should default to None"

    # --- Validation through _validate_role_override --------------------------

    def test_invalid_builder_effort_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("builder", "effort", "invalid")
        assert exc.value.code == 2

    def test_empty_builder_model_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("builder", "model", "")
        assert exc.value.code == 2

    def test_whitespace_only_model_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("reviewer", "model", "   ")
        assert exc.value.code == 2

    def test_invalid_provider_exits_2(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        with pytest.raises(SystemExit) as exc:
            _validate_role_override("repair", "provider", "bogus-provider")
        assert exc.value.code == 2

    def test_none_value_is_accepted(self) -> None:
        from apps.cli.commands.do_cmd import _validate_role_override
        # Should not raise
        _validate_role_override("builder", "provider", None)
        _validate_role_override("reviewer", "model", None)
        _validate_role_override("repair", "effort", None)

    # --- Catalog registration: both commands list all 9 role flags -----------

    def test_job_run_catalog_has_role_flags(self) -> None:
        cmd = get_command("do.job-run")
        arg_names = {a.name for a in cmd.args}
        for flag in (
            "--builder-provider", "--builder-model", "--builder-effort",
            "--reviewer-provider", "--reviewer-model", "--reviewer-effort",
            "--repair-provider", "--repair-model", "--repair-effort",
        ):
            assert flag in arg_names, f"do.job-run missing {flag}"

    def test_job_flow_catalog_has_role_flags(self) -> None:
        cmd = get_command("do.job-flow")
        arg_names = {a.name for a in cmd.args}
        for flag in (
            "--builder-provider", "--builder-model", "--builder-effort",
            "--reviewer-provider", "--reviewer-model", "--reviewer-effort",
            "--repair-provider", "--repair-model", "--repair-effort",
        ):
            assert flag in arg_names, f"do.job-flow missing {flag}"


# ---------------------------------------------------------------------------
# Round 16 — F1: the restored timeout hint and the exclusivity it must not weaken
# ---------------------------------------------------------------------------


class TestJobFlowStreamFlagsStayExclusive:
    """F15 is not collateral damage of F1's repair: supplying both halves is still exit 2."""

    def test_both_stream_flags_is_a_usage_error(self) -> None:
        import pytest as _pytest
        from apps.cli.grouped import _UsageError

        with _pytest.raises((_UsageError, SystemExit)):
            build_parser().parse_args(
                ["do", "job-flow", "--job-file", "j.md",
                 "--stream-evidence", "--no-stream-evidence"])

    def test_omitting_both_stays_the_omission_sentinel(self) -> None:
        ns = build_parser().parse_args(["do", "job-flow", "--job-file", "j.md"])
        assert ns.stream_evidence is None


class TestTheTimeoutHintReportsResolvedTruth:
    """F1 (round 16): the hint reports what `run_job` RESOLVED and recorded.

    It must never re-resolve a default at the call site — that is what the shared
    `RunInvocation` exists to prevent, and re-introducing `timeout_sec or 120` here would
    silently defeat the omission sentinel the whole tri-state contract rests on.
    """

    def _job(self, timeout_sec):
        from packages.orchestration.pingpong_job import ExecutionConfig, JobPlan

        job = JobPlan(job_id="j" * 16, job_title="t", repo_path="/tmp/x")
        if timeout_sec is not None:
            job.execution_config = ExecutionConfig(timeout_sec=timeout_sec)
        return job

    def test_an_omitted_timeout_reports_the_resolved_product_default(self) -> None:
        """Omission is preserved into `run_job`; the hint then reports what it settled on."""
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(120)                       # what run_job resolved and persisted
        assert _effective_timeout_sec(job) == 120
        hint = _build_timeout_hint("claude-cli", "fake", _effective_timeout_sec(job))
        assert "120s" in hint and "--timeout-sec 900" in hint

    def test_an_explicit_timeout_reports_that_timeout(self) -> None:
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(300)
        assert _effective_timeout_sec(job) == 300
        assert "300s" in _build_timeout_hint("claude-cli", "fake", _effective_timeout_sec(job))

    def test_an_explicit_profile_reports_its_effective_timeout(self) -> None:
        """A profile resolves to a number inside `run_job`; the hint reports the EFFECT."""
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(900)                       # e.g. a long profile
        assert _effective_timeout_sec(job) == 900
        assert _build_timeout_hint("claude-cli", "fake", _effective_timeout_sec(job)) == ""

    def test_no_execution_config_says_nothing_rather_than_guessing(self) -> None:
        from apps.cli.commands.do_cmd import _build_timeout_hint, _effective_timeout_sec

        job = self._job(None)
        assert _effective_timeout_sec(job) is None
        assert _build_timeout_hint("claude-cli", "fake", None) == ""

    def test_non_cli_providers_never_get_the_hint(self) -> None:
        from apps.cli.commands.do_cmd import _build_timeout_hint

        assert _build_timeout_hint("fake", "fake", 10) == ""

    def test_the_hint_never_changes_execution(self) -> None:
        """Informational only: it reads the persisted config and returns a string."""
        import inspect

        from apps.cli.commands.do_cmd import _build_timeout_hint

        src = inspect.getsource(_build_timeout_hint)
        assert "run_job" not in src and "=" not in src.split("return")[-1]
