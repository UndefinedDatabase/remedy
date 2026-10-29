"""Operator order beweis, F326: a finding that only says a command the builder may not run did not
run reads low, decided in code; the reviewer's prompt names what the builder may run."""
from __future__ import annotations

import json

from packages.orchestration.pingpong_loop import _REVIEWER_SYSTEM
from packages.orchestration.pingpong_provider import ReviewerOutput, ReviewFinding
from packages.orchestration.review_scope_rules import REVIEWER_SCOPE_RULES, settle_review_findings
from packages.orchestration.verified_repair import review_severity_verdict


def _verdict(*findings: ReviewFinding, verdict: str = "blocked") -> ReviewerOutput:
    return ReviewerOutput(verdict=verdict, findings=list(findings), summary="s")


def _settle(out: ReviewerOutput, workspace) -> ReviewerOutput:
    return settle_review_findings(out, staged_files=["src/a.ts"], is_fake=False, workspace=str(workspace))


def test_the_reviewer_prompt_names_what_the_builder_may_run():
    assert REVIEWER_SCOPE_RULES in _REVIEWER_SYSTEM
    for word in ("typecheck", "lint", "build", "e2e", "tsc", "ruff", "mypy", "pyright"):
        assert word in REVIEWER_SCOPE_RULES
    assert "is no finding against the builder" in REVIEWER_SCOPE_RULES


def test_a_command_the_builder_may_not_run_reads_low(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({"scripts": {"typecheck": "tsc"}}))
    out = _settle(_verdict(ReviewFinding(id="R1", severity="high", file="src/a.ts",
                                         summary="`pnpm deploy:check` was not run, so nothing proves the change.")),
                  tmp_path)
    assert out.findings[0].severity == "low"
    _, settled = review_severity_verdict(out.verdict, len(out.findings), [f.severity for f in out.findings])
    assert settled is not None and settled[0] == "pass_no_repair"


def test_a_command_the_builder_may_run_keeps_its_severity(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({"scripts": {"typecheck": "tsc"}}))
    out = _settle(_verdict(ReviewFinding(id="R1", severity="high", file="src/a.ts",
                                         summary="pnpm typecheck was not run; type errors are possible.")),
                  tmp_path)
    assert out.findings[0].severity == "high"


def test_a_finding_about_the_code_keeps_its_severity(tmp_path):
    out = _settle(_verdict(ReviewFinding(id="R1", severity="high", file="src/a.ts",
                                         summary="resize ignores the container width")), tmp_path)
    assert out.findings[0].severity == "high"
