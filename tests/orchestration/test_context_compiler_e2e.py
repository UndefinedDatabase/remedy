"""End-to-end tests for the compiled context inside run_pingpong (F107 T004 part 2b-ii).

This is the feature's DONE condition, exercised against a REAL fixture repo on
disk and the REAL ``FakeProvider``: the same fixture task is run twice through
``run_pingpong``, once on today's whole-file context pack and once on the
compiled selection, and the compiled run must reach the same final status on a
measurably smaller context — with the omissions and size records landing exactly
where the caller pointed and nowhere else.

Every assertion here is on a REAL value read back off the result or off the
written record. Nothing is asserted for truthiness and no expected number is
re-derived with the expression the production code uses.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from packages.orchestration.context_compiler import (
    CONTEXT_SIZE_FILENAME,
    OMITTED_CONTEXT_FILENAME,
    compile_task_context,
    render_compiled_context_text,
)
from packages.orchestration.pingpong_loop import build_repo_context, run_pingpong
from packages.orchestration.pingpong_provider import FakeProvider

_GOAL = "harden the payment gateway retry path"

#: The task's fenced write scope — what a caller would pass as its ``files_hint``.
_FENCED_PATHS = ["src/payment_gateway.py"]

#: The candidate listing the CALLER walked. ``run_pingpong`` never lists a repo
#: itself, so the test plays the caller and hands the listing in.
_CANDIDATES = [
    "README.md",
    "src/clock_source.py",
    "src/invoice_report.py",
    "src/payment_gateway.py",
    "src/retry_policy.py",
]


@pytest.fixture
def isolate_data_root(tmp_path: Path, monkeypatch):
    data_dir = tmp_path / "remedy_data"
    data_dir.mkdir()
    monkeypatch.setenv("REMEDY_DATA_DIR", str(data_dir))
    return data_dir


@pytest.fixture
def compiled_fixture_repo(tmp_path: Path) -> Path:
    """A real five-file repo whose import graph has one file per tier.

    ``src/payment_gateway.py`` is fenced (tier 1) and imports
    ``src/retry_policy.py`` (tier 2), which alone reaches
    ``src/clock_source.py`` (tier 3). ``src/invoice_report.py`` is reachable
    from nothing in scope (tier 4, omitted for distance) and is deliberately the
    longest module, so a whole-files baseline pays for it and the compiled
    selection does not. No git checkout is created: the compiler never shells
    out to git.
    """
    repo = tmp_path / "repo"
    (repo / "src").mkdir(parents=True)
    (repo / "README.md").write_text(
        "# Payments demo\n\nA tiny fixture repository used by the context compiler tests.\n"
    )
    (repo / "src" / "payment_gateway.py").write_text(
        "from src.retry_policy import RetryPolicy\n"
        "\n"
        "\n"
        "def charge_card(amount_cents: int) -> str:\n"
        '    """Charge a card and report the outcome."""\n'
        "    policy = RetryPolicy(max_attempts=3)\n"
        "    for attempt in policy.attempts():\n"
        "        if attempt > 1:\n"
        '            return "retried"\n'
        '    return "charged"\n'
    )
    (repo / "src" / "retry_policy.py").write_text(
        "from src.clock_source import monotonic_seconds\n"
        "\n"
        "\n"
        "class RetryPolicy:\n"
        '    """A bounded retry schedule."""\n'
        "\n"
        "    def __init__(self, max_attempts: int = 3) -> None:\n"
        "        self.max_attempts = max_attempts\n"
        "        self.started_at = monotonic_seconds()\n"
        "\n"
        "    def attempts(self) -> list[int]:\n"
        "        return list(range(1, self.max_attempts + 1))\n"
    )
    (repo / "src" / "clock_source.py").write_text(
        "import time\n"
        "\n"
        "\n"
        "def monotonic_seconds() -> float:\n"
        '    """Seconds from a monotonic clock."""\n'
        "    return time.monotonic()\n"
        "\n"
        "\n"
        "def wall_clock_seconds() -> float:\n"
        '    """Seconds from the wall clock."""\n'
        "    return time.time()\n"
    )
    unrelated_body = "\n".join(
        f"    line_{n} = 'invoice report filler line number {n}'" for n in range(1, 61)
    )
    (repo / "src" / "invoice_report.py").write_text(
        "def render_invoice_report(rows: list[dict]) -> str:\n"
        '    """Render an invoice report. Reached from nothing in the fenced scope."""\n'
        f"{unrelated_body}\n"
        "    return '\\n'.join(str(row) for row in rows)\n"
    )
    return repo


def _pass_provider() -> FakeProvider:
    return FakeProvider(pass_on_round=1, fail_on_round=99)


def _run(repo: Path, **kwargs):
    return run_pingpong(
        goal=_GOAL,
        repo_path=str(repo),
        builder_provider=_pass_provider(),
        reviewer_provider=_pass_provider(),
        max_rounds=2,
        repair_rounds=0,
        **kwargs,
    )


def _run_whole_files_baseline(repo: Path, **kwargs):
    """The WHOLE-FILE baseline the DONE condition names, with the new params unset.

    ``build_repo_context`` inlines file contents only for the paths it is handed
    as ``mentioned_files``; with that list empty it emits the goal, the file tree
    and the README and nothing else. The comparison F107 exists to make is
    "compiled selection vs. whole files", so the baseline hands the SAME candidate
    listing to the existing parameter that produces whole files.
    """
    return _run(repo, mentioned_files=_CANDIDATES, **kwargs)


class TestCompiledContextEndToEnd:
    """The DONE condition: same task, same provider, smaller context, same outcome."""

    def test_compiled_run_shrinks_the_context_and_still_solves_the_task(
        self, isolate_data_root, compiled_fixture_repo
    ):
        baseline = _run_whole_files_baseline(compiled_fixture_repo)
        compiled = _run(
            compiled_fixture_repo,
            compiled_context_paths=_FENCED_PATHS,
            compiled_context_candidates=_CANDIDATES,
        )

        assert baseline.final_status == "staged_review_passed"
        assert compiled.final_status == "staged_review_passed"
        assert compiled.final_status == baseline.final_status

        assert baseline.context_chars > 0
        assert compiled.context_chars > 0
        assert compiled.context_chars < baseline.context_chars

        # R-0283: "smaller" ALONE is satisfied by a run that never compiled at all —
        # bypassing the compiled branch falls through to a context that is also
        # smaller, for a reason that has nothing to do with F107. So pin the number
        # the run REPORTS to the bytes the compiler itself produced over the same
        # fixture: an exact length no fall-through can hit by accident.
        expected_compiled_text = render_compiled_context_text(
            compiled_fixture_repo,
            compile_task_context(compiled_fixture_repo, _FENCED_PATHS, _CANDIDATES),
        )
        assert compiled.context_chars == len(expected_compiled_text)

    def test_compiled_run_reports_the_compiled_category(
        self, isolate_data_root, compiled_fixture_repo
    ):
        baseline = _run_whole_files_baseline(compiled_fixture_repo)
        compiled = _run(
            compiled_fixture_repo,
            compiled_context_paths=_FENCED_PATHS,
            compiled_context_candidates=_CANDIDATES,
        )

        assert compiled.context_categories == ["compiled_context"]
        # The baseline's categories are whatever build_repo_context returns TODAY;
        # pinning them to a guess would make this a test of the guess.
        _, expected_baseline = build_repo_context(
            str(compiled_fixture_repo), _GOAL, mentioned_files=_CANDIDATES
        )
        assert baseline.context_categories == expected_baseline
        assert baseline.context_categories != ["compiled_context"]


class TestCompiledContextRecords:
    """The two records land where the caller pointed, carrying real values."""

    def test_records_are_written_with_real_values(
        self, isolate_data_root, compiled_fixture_repo, tmp_path: Path
    ):
        record_dir = tmp_path / "evidence" / "context"
        compiled = _run(
            compiled_fixture_repo,
            compiled_context_paths=_FENCED_PATHS,
            compiled_context_candidates=_CANDIDATES,
            context_record_dir=str(record_dir),
        )
        assert compiled.final_status == "staged_review_passed"

        size_path = record_dir / CONTEXT_SIZE_FILENAME
        omissions_path = record_dir / OMITTED_CONTEXT_FILENAME
        assert size_path.is_file()
        assert omissions_path.is_file()

        size_record = json.loads(size_path.read_text())
        selection = compile_task_context(
            compiled_fixture_repo, _FENCED_PATHS, _CANDIDATES
        )
        assert size_record["compiled_tokens"] == selection.estimated_tokens
        assert size_record["saved_tokens"] > 0
        assert size_record["whole_file_tokens"] > size_record["compiled_tokens"]

        omissions = json.loads(omissions_path.read_text())
        unrelated = [r for r in omissions if r["path"] == "src/invoice_report.py"]
        assert len(unrelated) == 1
        assert unrelated[0]["reason"] == "distance"
        assert unrelated[0]["outcome"] == "omitted"
        assert unrelated[0]["tier"] == 4

    def test_no_record_dir_writes_neither_file(
        self, isolate_data_root, compiled_fixture_repo, tmp_path: Path
    ):
        record_dir = tmp_path / "evidence" / "context"
        compiled = _run(
            compiled_fixture_repo,
            compiled_context_paths=_FENCED_PATHS,
            compiled_context_candidates=_CANDIDATES,
        )
        assert compiled.context_categories == ["compiled_context"]
        assert not (record_dir / CONTEXT_SIZE_FILENAME).exists()
        assert not (record_dir / OMITTED_CONTEXT_FILENAME).exists()
        assert not record_dir.exists()


class TestCompiledContextOptInIsAllOrNothing:
    """One list alone is a caller mistake; it must not half-compile."""

    def test_only_fenced_paths_keeps_the_default_path(
        self, isolate_data_root, compiled_fixture_repo
    ):
        baseline = _run_whole_files_baseline(compiled_fixture_repo)
        partial = _run_whole_files_baseline(
            compiled_fixture_repo, compiled_context_paths=_FENCED_PATHS
        )

        assert partial.context_categories == baseline.context_categories
        assert partial.context_categories != ["compiled_context"]
        assert partial.context_chars == baseline.context_chars

    def test_only_candidates_keeps_the_default_path(
        self, isolate_data_root, compiled_fixture_repo
    ):
        baseline = _run_whole_files_baseline(compiled_fixture_repo)
        partial = _run_whole_files_baseline(
            compiled_fixture_repo, compiled_context_candidates=_CANDIDATES
        )

        assert partial.context_categories == baseline.context_categories
        assert partial.context_categories != ["compiled_context"]
        assert partial.context_chars == baseline.context_chars
