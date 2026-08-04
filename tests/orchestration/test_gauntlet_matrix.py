"""F075 T001 — the matrix report: same evidence, same bytes, every time.

Determinism is the property under test. A report that embeds a clock, an
absolute path or a dict-iteration order cannot be golden-compared, and a gate
whose evidence cannot be compared is a gate that gets re-blessed instead of
checked.
"""
from __future__ import annotations

import json
from pathlib import Path

from packages.orchestration.gauntlet_evaluator import (
    DISPOSITION_SILENT_SUCCESS,
    FAILURE_INJECTION_NOT_DEGRADED,
    FAILURE_TERMINAL_NOT_GREEN,
    INJECTION_HARNESS_DEATH_MID_WRITE,
    PASS_CRITERIA,
    evaluate_evidence_dir,
)
from packages.orchestration.gauntlet_matrix import (
    MATRIX_JSON_FILENAME,
    MATRIX_MARKDOWN_FILENAME,
    MATRIX_VERSION,
    matrix_json,
    matrix_json_bytes,
    render_matrix_markdown,
    write_matrix,
)
from packages.orchestration.orchestrator_loop import TERMINAL_ITERATION_LIMIT
from tests.orchestration.test_gauntlet_evidence import (
    FLAWLESS_BODY,
    GOLDEN_DIR,
    RECORDED_DIR,
    RELEASED_GATE,
    write_run,
)


def build_evidence(root: Path, *, spoil: bool = False) -> Path:
    evidence = root / "recorded"
    write_run(evidence, "run-01",
              dict(FLAWLESS_BODY, order_id="g01", kind="pure_code_change"),
              RELEASED_GATE)
    second = dict(FLAWLESS_BODY, order_id="g02", kind="test_add",
                  evidence_links={"ledger": "ledger.jsonl", "report": "report.md"},
                  postmortems=[{"scope": "call", "failure_class": "provider_timeout"},
                               {"scope": "task", "failure_class": "provider_timeout"}])
    if spoil:
        second["terminal_status"] = TERMINAL_ITERATION_LIMIT
        second["injections"] = [{"class": INJECTION_HARNESS_DEATH_MID_WRITE,
                                 "disposition": DISPOSITION_SILENT_SUCCESS,
                                 "detail": "half-written dossier accepted"}]
    write_run(evidence, "run-02", second, RELEASED_GATE)
    return evidence


def test_markdown_bytes_are_stable_across_renders(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    assert render_matrix_markdown(verdict) == render_matrix_markdown(verdict)


def test_json_bytes_are_stable_across_renders(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    assert matrix_json_bytes(verdict) == matrix_json_bytes(verdict)


def test_the_same_evidence_in_two_places_renders_identically(tmp_path: Path) -> None:
    """The absolute path must not leak into the report — two machines, one matrix."""
    first = evaluate_evidence_dir(build_evidence(tmp_path / "a"))
    second = evaluate_evidence_dir(build_evidence(tmp_path / "b"))
    assert first.evidence_dir != second.evidence_dir
    assert render_matrix_markdown(first) == render_matrix_markdown(second)
    assert matrix_json_bytes(first) == matrix_json_bytes(second)


def test_the_report_never_contains_the_absolute_evidence_path(tmp_path: Path) -> None:
    evidence = build_evidence(tmp_path)
    verdict = evaluate_evidence_dir(evidence)
    assert str(evidence) not in render_matrix_markdown(verdict)
    assert str(evidence) not in matrix_json_bytes(verdict)


def test_json_carries_the_summary_and_the_criteria_table(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    body = matrix_json(verdict)
    assert body["matrix_version"] == MATRIX_VERSION
    assert body["evidence_label"] == "recorded"
    assert (body["runs_recorded"], body["runs_flawless"]) == (2, 2)
    assert body["passed"] is True
    assert body["pass_criteria"] == list(PASS_CRITERIA)
    assert list(body["runs"][0]["criteria"]) == list(PASS_CRITERIA)


def test_each_run_reports_terminal_dod_postmortems_interventions_and_cost(
        tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    run = matrix_json(verdict)["runs"][1]
    assert run["terminal_status"] == "achieved"
    assert run["postmortem_classes"] == ["provider_timeout"]  # deduplicated
    assert run["operator_interventions"] == []
    assert (run["tokens_in"], run["tokens_out"]) == (120_000, 30_000)
    assert run["wall_seconds"] == 612.5
    assert "| check | kind | blocking | status |" in run["dod_matrix"]
    assert run["evidence_links"] == {"ledger": "ledger.jsonl", "report": "report.md"}


def test_markdown_links_point_into_the_runs_own_evidence(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    text = render_matrix_markdown(verdict)
    assert "- ledger: `run-02/ledger.jsonl`" in text
    assert "- report: `run-02/report.md`" in text


def test_a_failed_campaign_names_its_failures_in_both_formats(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path, spoil=True))
    body = matrix_json(verdict)
    assert body["passed"] is False
    assert body["runs_flawless"] == 1
    assert body["failure_kinds"] == [FAILURE_TERMINAL_NOT_GREEN,
                                     FAILURE_INJECTION_NOT_DEGRADED]
    text = render_matrix_markdown(verdict)
    assert "1/2 runs flawless · **NOT A PASS**" in text
    assert INJECTION_HARNESS_DEATH_MID_WRITE in text
    assert "half-written dossier accepted" in text


def test_an_empty_evidence_set_renders_as_not_a_pass(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(tmp_path / "empty")
    text = render_matrix_markdown(verdict)
    assert "0/0 runs flawless · **NOT A PASS**" in text
    assert "An empty gauntlet is not a pass." in text
    assert matrix_json(verdict)["passed"] is False


def test_write_matrix_puts_both_reports_side_by_side(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    md_path, json_path = write_matrix(verdict, tmp_path / "out")
    assert md_path.name == MATRIX_MARKDOWN_FILENAME
    assert json_path.name == MATRIX_JSON_FILENAME
    assert md_path.read_text(encoding="utf-8") == render_matrix_markdown(verdict)
    assert json.loads(json_path.read_text(encoding="utf-8"))["runs_recorded"] == 2
    # Rewriting the same verdict changes nothing on disk.
    before = json_path.read_bytes()
    write_matrix(verdict, tmp_path / "out")
    assert json_path.read_bytes() == before


def test_an_explicit_label_overrides_the_directory_name(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    assert matrix_json(verdict, label="set-v1")["evidence_label"] == "set-v1"
    assert "# Gauntlet matrix — set-v1" in render_matrix_markdown(verdict, label="set-v1")


def test_both_reports_end_with_exactly_one_newline(tmp_path: Path) -> None:
    verdict = evaluate_evidence_dir(build_evidence(tmp_path))
    for text in (render_matrix_markdown(verdict), matrix_json_bytes(verdict)):
        assert text.endswith("\n")
        assert not text.endswith("\n\n")


# ---------------------------------------------------------------------------
# The golden matrix for the recorded set
# ---------------------------------------------------------------------------

def test_the_golden_markdown_matrix_matches_the_recorded_set() -> None:
    """Byte-for-byte. A golden that is re-blessed on every change checks nothing,
    so this comparison is the one that must be argued with, not regenerated."""
    rendered = render_matrix_markdown(evaluate_evidence_dir(RECORDED_DIR))
    expected = (GOLDEN_DIR / MATRIX_MARKDOWN_FILENAME).read_text(encoding="utf-8")
    assert rendered == expected


def test_the_golden_markdown_names_every_recorded_run() -> None:
    text = (GOLDEN_DIR / MATRIX_MARKDOWN_FILENAME).read_text(encoding="utf-8")
    for run_dir in sorted(p.name for p in RECORDED_DIR.iterdir() if p.is_dir()):
        assert f"### {run_dir} — " in text
    assert "5/9 runs flawless · **NOT A PASS**" in text
