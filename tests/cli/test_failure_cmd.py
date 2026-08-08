"""F010 T003 — `remedy stats failures` over a deterministic fixture corpus.

The corpus is a handful of JSON files in a temporary evidence root: no database, nothing
persistent, nothing shared between tests. What is asserted is the arithmetic — the exact
counts — plus the two sentences that make the numbers honest: the coverage line, and "no
failures recorded" when there is genuinely nothing to report.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from apps.cli.command_catalog import CATALOG, GROUPS, get_commands_for_group
from apps.cli.commands import collect_all_handlers
from apps.cli.commands import failure_stats_cmd as CMD
from packages.orchestration.failure_stats import (
    STATS_VERSION,
    FailureStatsError,
    collect_failures,
    render_human,
)


@pytest.fixture
def evidence_root(tmp_path, monkeypatch) -> Path:
    root = tmp_path / "remedy_data"
    root.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
    exports = root / "evidence_exports"
    exports.mkdir()
    return exports


def _write(path: Path, **fields) -> None:
    record = {
        "postmortem_v": 1,
        "scope": "call",
        "failure_class": "provider_timeout",
        "signal_source": "error_text",
        "job_id": "J1",
        "task_id": "T001",
        "run_id": "r1",
        "call_id": "calls/builder/round-01/attempt",
        "role": "builder",
        "provider": "fake",
        "terminal_status": "",
        "raw_reason": "provider_error: TimeoutExpired",
        "retries_used": 2,
        "retry_reasons": [],
        "evidence_refs": [],
        "created_at": "2026-07-13T10:00:00+00:00",
    }
    record.update(fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2) + "\n")


@pytest.fixture
def corpus(evidence_root: Path) -> Path:
    """Two jobs. J1: one failed task with two failed calls. J2: one blocked task, no calls.
    Plus a task that simply passed (no post-mortem) and a pre-F010 task (likewise)."""
    j1 = evidence_root / "J1" / "task_runs"
    _write(j1 / "T001" / "postmortem.json",
           scope="task", failure_class="review_failed", signal_source="terminal_status",
           terminal_status="review_failed", raw_reason="reviewer rejected", role="",
           provider="", created_at="2026-07-13T12:00:00+00:00")
    _write(j1 / "T001" / "call_postmortems" / "calls" / "builder" / "round-01"
           / "attempt" / "postmortem.json")
    _write(j1 / "T001" / "call_postmortems" / "calls" / "reviewer" / "round-01"
           / "parse-retry" / "postmortem.json",
           failure_class="parse", signal_source="error_class", role="reviewer",
           raw_reason="malformed_output: not json")
    (j1 / "T002").mkdir(parents=True)                    # passed: nothing to explain

    j2 = evidence_root / "J2" / "task_runs"
    _write(j2 / "T001" / "postmortem.json",
           scope="task", failure_class="worktree_lock", signal_source="terminal_status",
           terminal_status="worktree_lock", raw_reason="lock held by run r9", role="",
           provider="", job_id="J2", created_at="2026-07-14T09:00:00+00:00")
    (j2 / "T009").mkdir(parents=True)                    # a run that predates F010
    return evidence_root


class TestAggregation:
    def test_the_exact_histogram(self, corpus):
        result = collect_failures()

        assert result["version"] == STATS_VERSION
        assert result["total_postmortems"] == 4
        assert result["counts_by_class"] == {
            "parse": 1,
            "provider_timeout": 1,
            "review_failed": 1,
            "worktree_lock": 1,
        }

    def test_call_and_task_scopes_are_counted_separately(self, corpus):
        """A rollup and the calls it points at are not the same record counted twice."""
        assert collect_failures()["counts_by_scope"] == {"call": 2, "job": 0, "task": 2}

    def test_top_reasons_are_bounded_and_deterministically_ordered(self, corpus):
        first = collect_failures()["top_reasons"]
        assert first == collect_failures()["top_reasons"]
        assert [entry["count"] for entry in first] == sorted(
            (entry["count"] for entry in first), reverse=True)
        assert all(len(entry["reason"]) <= 120 for entry in first)

    def test_the_job_filter(self, corpus):
        result = collect_failures(job="J2")
        assert result["total_postmortems"] == 1
        assert result["counts_by_class"] == {"worktree_lock": 1}
        assert result["coverage"]["jobs_scanned"] == 1

    def test_the_since_filter_uses_the_existing_timestamp_semantics(self, corpus):
        result = collect_failures(since="2026-07-14T00:00:00+00:00")
        assert result["total_postmortems"] == 1
        assert result["counts_by_class"] == {"worktree_lock": 1}

    def test_combined_filters(self, corpus):
        assert collect_failures(job="J1", since="2026-07-14T00:00:00+00:00")[
            "total_postmortems"] == 0

    def test_the_corpus_is_not_mutated(self, corpus):
        before = sorted(p.read_text() for p in corpus.rglob("*.json"))
        collect_failures()
        assert sorted(p.read_text() for p in corpus.rglob("*.json")) == before


class TestCoverage:
    def test_old_runs_without_postmortems_stay_visible(self, corpus):
        coverage = collect_failures()["coverage"]
        assert coverage["tasks_scanned"] == 4
        assert coverage["tasks_without_postmortem"] == 2   # T002 (passed) and J2/T009
        assert "Coverage: 4 scanned, 2 without postmortems" in render_human(
            collect_failures())

    def test_an_empty_corpus_is_honest_not_an_error(self, evidence_root):
        result = collect_failures()
        assert result["total_postmortems"] == 0
        assert result["counts_by_class"] == {}
        text = render_human(result)
        assert "No failures recorded." in text
        assert "Coverage: 0 scanned, 0 without postmortems" in text

    def test_a_malformed_record_is_reported_not_fatal(self, corpus):
        bad = corpus / "J1" / "task_runs" / "T003" / "postmortem.json"
        bad.parent.mkdir(parents=True)
        bad.write_text("{ not json")

        result = collect_failures()
        assert result["total_postmortems"] == 4, "the good records still count"
        assert result["coverage"]["malformed_postmortems"] == 1
        assert any("malformed" in w for w in result["warnings"])

    def test_an_unsupported_version_is_reported_not_counted(self, corpus):
        future = corpus / "J1" / "task_runs" / "T004" / "postmortem.json"
        future.parent.mkdir(parents=True)
        future.write_text(json.dumps({"postmortem_v": 99, "failure_class": "parse"}) + "\n")

        result = collect_failures()
        assert result["coverage"]["unsupported_version_postmortems"] == 1
        assert result["counts_by_class"].get("parse", 0) == 1, "only the v1 parse record"

    def test_an_unreadable_evidence_root_is_an_error_not_silence(self, tmp_path, monkeypatch):
        root = tmp_path / "data"
        root.mkdir()
        monkeypatch.setenv("REMEDY_DATA_DIR", str(root))
        (root / "evidence_exports").write_text("this is a file, not a directory")

        with pytest.raises(FailureStatsError):
            collect_failures()


class TestCli:
    def test_human_output(self, corpus, capsys):
        CMD._cmd_stats_failures()
        out = capsys.readouterr().out
        assert "Failures: 4 post-mortems" in out
        assert "provider_timeout" in out and "worktree_lock" in out
        assert "Coverage: 4 scanned, 2 without postmortems" in out

    def test_json_output_is_stable(self, corpus, capsys):
        CMD._cmd_stats_failures(json_output=True)
        first = json.loads(capsys.readouterr().out)
        CMD._cmd_stats_failures(json_output=True)
        second = json.loads(capsys.readouterr().out)
        assert first == second
        assert first["filters"] == {"job": "", "since": ""}
        assert set(first) >= {
            "version", "filters", "total_postmortems", "counts_by_class",
            "counts_by_scope", "top_reasons", "coverage", "warnings",
        }

    def test_the_filters_reach_the_aggregator(self, corpus, capsys):
        CMD._cmd_stats_failures(job="J2", json_output=True)
        result = json.loads(capsys.readouterr().out)
        assert result["filters"]["job"] == "J2"
        assert result["total_postmortems"] == 1

    def test_an_invalid_since_fails_clearly(self, corpus, capsys):
        with pytest.raises(SystemExit) as exc:
            CMD._cmd_stats_failures(since="last tuesday")
        assert exc.value.code == CMD.EXIT_USAGE
        assert "not an ISO-8601 timestamp" in capsys.readouterr().err

    def test_an_empty_corpus_exits_zero(self, evidence_root, capsys):
        CMD._cmd_stats_failures()                         # no SystemExit
        assert "No failures recorded." in capsys.readouterr().out

    def test_the_command_is_registered(self):
        assert "stats" in GROUPS
        entry = next(c for c in CATALOG if c.command_id == "stats.failures")
        assert entry.action_class == "read_only"
        assert entry.supports_json is True
        assert entry.may_mutate_repo is False and entry.may_execute_commands is False
        assert {a.name for a in entry.args} >= {"--job", "--since", "--json"}
        # F103 registered cost/backfill-ledger/verify-ledger in the SAME group, so
        # this pins F010's own membership instead of the group's whole contents —
        # the group is shared and will keep growing.
        assert "stats.failures" in {c.command_id for c in get_commands_for_group("stats")}
        assert "stats.failures" in collect_all_handlers()

    def test_the_handler_is_read_only(self, corpus):
        before = sorted(str(p) for p in corpus.rglob("*"))
        CMD.COMMAND_HANDLERS["stats.failures"](type("A", (), {"json": True})())
        assert sorted(str(p) for p in corpus.rglob("*")) == before


class TestJobScope:
    """A job that failed before any task could own the failure has its own scope."""

    def test_a_job_level_record_is_counted_in_its_own_scope(self, corpus):
        _write(corpus / "J3" / "postmortem.json",
               scope="job", failure_class="worktree_lock",
               signal_source="typed_exception", job_id="J3", task_id="", run_id="",
               call_id="", role="", provider="",
               raw_reason="WorktreeLockError: held by run r9",
               created_at="2026-07-13T08:00:00+00:00")

        result = collect_failures()
        assert result["counts_by_scope"]["job"] == 1
        assert result["counts_by_class"]["worktree_lock"] == 2   # the J2 task + the J3 job
        assert result["total_postmortems"] == 5

    def test_a_job_record_survives_the_job_filter(self, corpus):
        _write(corpus / "J3" / "postmortem.json", scope="job",
               failure_class="worktree_conflict", job_id="J3", task_id="", role="",
               provider="", raw_reason="WorktreeConflictError: both changed x.py")
        result = collect_failures(job="J3")
        assert result["total_postmortems"] == 1
        assert result["counts_by_scope"] == {"call": 0, "job": 1, "task": 0}


class TestWarningsNameThePath:
    def test_a_malformed_record_is_named_by_its_relative_path(self, corpus):
        bad = corpus / "J1" / "task_runs" / "T005" / "postmortem.json"
        bad.parent.mkdir(parents=True)
        bad.write_text("{ not json")

        warnings = collect_failures()["warnings"]
        assert any("J1/task_runs/T005/postmortem.json" in w for w in warnings), warnings
        # ...and never the bare filename, which names nothing in a corpus of them.
        assert not any(w.endswith("malformed JSON: postmortem.json") for w in warnings)

    def test_the_streamed_source_copy_is_never_double_counted(self, corpus):
        """The canonical exported copy is the only one that counts."""
        streamed = (corpus / "J1" / "task_runs" / "T001" / "streams" / "builder"
                    / "round-01" / "attempt-01" / "postmortem.json")
        _write(streamed)                                # the same record, at its source

        result = collect_failures()
        assert result["counts_by_scope"]["call"] == 2, "the source copy was counted again"


class TestStatsNeverPrintsASecret:
    """A histogram is not a place to publish an API key.

    Records are redacted when they are written, but stats also reads corpora written by an
    older build — so it redacts on the way out too.
    """

    def test_a_secret_in_an_old_record_is_not_printed(self, evidence_root, capsys):
        _write(evidence_root / "J9" / "task_runs" / "T001" / "postmortem.json",
               scope="task", failure_class="config", signal_source="error_class",
               raw_reason="provider config rejected: ANTHROPIC_API_KEY=sk-ant-supersecret",
               job_id="J9", role="", provider="")

        CMD._cmd_stats_failures()
        out = capsys.readouterr().out
        assert "sk-ant-supersecret" not in out
        assert "REDACTED" in out
        assert "config" in out

    def test_the_json_output_carries_no_secret_either(self, evidence_root, capsys):
        _write(evidence_root / "J9" / "task_runs" / "T001" / "postmortem.json",
               scope="task", failure_class="config", raw_reason="API_KEY=leakme",
               job_id="J9", role="", provider="")

        CMD._cmd_stats_failures(json_output=True)
        payload = capsys.readouterr().out
        assert "leakme" not in payload
        assert json.loads(payload)["total_postmortems"] == 1


class TestStatsNeverPrintsAPrivatePath:
    """A file URI is a local path wearing a scheme. It does not belong in a histogram."""

    PRIVATE = ("failed at file:///home/bernardo/private/project/secret.py "
               "and cwd:/tmp/secret-repo and path:/home/user/private.txt")

    def test_the_human_output_carries_no_private_path(self, evidence_root, capsys):
        _write(evidence_root / "J9" / "task_runs" / "T001" / "postmortem.json",
               scope="task", failure_class="config", raw_reason=self.PRIVATE,
               job_id="J9", role="", provider="")

        CMD._cmd_stats_failures()
        out = capsys.readouterr().out
        for private in ("/home/bernardo", "file:///", "/tmp/secret-repo", "/home/user"):
            assert private not in out, out
        assert "secret.py" in out, "the file NAME is not private; the path is"

    def test_the_json_output_carries_no_private_path(self, evidence_root, capsys):
        _write(evidence_root / "J9" / "task_runs" / "T001" / "postmortem.json",
               scope="task", failure_class="config", raw_reason=self.PRIVATE,
               job_id="J9", role="", provider="")

        CMD._cmd_stats_failures(json_output=True)
        payload = capsys.readouterr().out
        for private in ("/home/bernardo", "file:///", "/tmp/secret-repo", "/home/user"):
            assert private not in payload
        assert json.loads(payload)["total_postmortems"] == 1
