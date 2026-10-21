"""Reads a finished job's files into the sources and claims of its certificate (F060, DECISION F060 D2).

A job that has ended keeps its outcome in several places: the job record, its evidence folder, the
evidence export, the run logs and the result diff. `collect_certificate_inputs` reads those, never
runs verification or an export, and answers the sources and the claims that
`job_certificate.build_job_certificate` packs. A member is present only when its file is; the final
report is always present, rendered in memory when the persisted one is missing or names another state.

It reads the resolved data root, as the readers it calls do, and takes no root of its own. The only
file it writes is the issue record `certificates.jsonl` beside the job's record, one line per
certificate, so that the next certificate of a resumed job carries a higher issue number.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from packages.orchestration.data_paths import (
    job_dir,
    job_evidence_dir,
    job_evidence_export_dir,
    run_log_dir,
)
from packages.orchestration.job_certificate import CertificateError, CertificateSource

# WHY: the states in which a job has ended; a resumable blocked or stopped run still gets one.
CERTIFICATE_TERMINAL_STATES = ("blocked", "cancelled", "completed", "failed", "stopped")
# WHY: the per-job file that counts the certificates issued, so an issue number never repeats.
CERTIFICATE_ISSUES_FILENAME = "certificates.jsonl"


# WHY: a job that has not ended, or does not exist, is refused as not ready, never certified.
class CertificateNotReadyError(CertificateError):
    """The job is unknown or has not ended, so no certificate is made."""


# WHY: everything one certificate needs from a job, so the command passes it on unchanged.
@dataclass(frozen=True)
class CertificateInputs:
    job_id: str
    project_id: str
    sources: tuple[CertificateSource, ...]
    claims: dict
    issue: int


def _read_regular(path: Path) -> bytes | None:
    """The file's bytes, None when absent; a symlink or an unreadable file is refused by name."""
    if path.is_symlink():
        raise CertificateError(f"{path} is a symlink; a certificate reads only regular files.")
    if not path.is_file():
        return None
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CertificateError(f"{path} cannot be read: {exc}") from None


def _report_bytes(plan, state: str, evidence: Path) -> bytes:
    from packages.orchestration.run_report import (
        MODE_FINAL,
        REPORT_FILENAME,
        build_report_sources,
        render_report_from_sources,
    )

    persisted = _read_regular(evidence / REPORT_FILENAME)
    if persisted is not None:
        try:
            text = persisted.decode("utf-8")
        except UnicodeDecodeError:
            text = ""
        if f"- State: {state}" in text.splitlines():
            return persisted
    rendered = render_report_from_sources(build_report_sources(plan), mode=MODE_FINAL)
    return rendered.encode("utf-8")


def _budget_member_and_claims(plan) -> tuple[bytes | None, object, list]:
    from packages.orchestration.budget_guard import (
        BudgetCounterError,
        counters_from_persisted,
        decode_persisted_budget_actuals,
    )

    if plan.budget_actuals is None:
        return None, None, []
    first = plan.first_running_at or None
    member = (json.dumps({"budget_actuals": plan.budget_actuals, "first_running_at": first},
                         indent=2, sort_keys=True) + "\n").encode("utf-8")
    try:
        counters = counters_from_persisted(
            decode_persisted_budget_actuals(plan.budget_actuals, first_running_at=first))
    except BudgetCounterError:
        return member, None, []
    return member, counters.cost_description(), list(counters.actual_sources)


def _dod_summary(job_id: str):
    from packages.orchestration.dod_gate import load_gate_result
    from packages.orchestration.dod_runners import STATUS_PASSED

    result = load_gate_result(job_id)
    if result is None:
        return None
    checks = result.get("checks") or []
    passed = [c for c in checks if isinstance(c, dict) and c.get("status") == STATUS_PASSED]
    return {"released": bool(result.get("released")), "check_count": len(checks),
            "passed_count": len(passed)}


def _regression_status(report_bytes: bytes | None):
    if report_bytes is None:
        return None
    try:
        data = json.loads(report_bytes.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
    return data.get("test_status") if isinstance(data, dict) else None


# WHY: the one place that reads a finished job's files, so the claims and the members agree.
def collect_certificate_inputs(job_id: str) -> CertificateInputs:
    from packages.orchestration.decision_queue import list_decisions
    from packages.orchestration.job_evidence import job_result_diff_source
    from packages.orchestration.ownership import OWNERSHIP_FILENAME
    from packages.orchestration.pingpong_job import load_job_plan

    plan = load_job_plan(job_id)
    if plan is None:
        raise CertificateNotReadyError(f"No job {job_id} is recorded in this Remedy data folder.")
    raw_state = plan.state
    state = str(getattr(raw_state, "value", raw_state))
    if state not in CERTIFICATE_TERMINAL_STATES:
        raise CertificateNotReadyError(
            f"Job {job_id} is {state}, and a certificate is made only for a job that has ended: "
            f"blocked, cancelled, completed, failed or stopped.")

    evidence = job_evidence_dir(job_id)
    export = job_evidence_export_dir(job_id)
    sources: list[CertificateSource] = [
        CertificateSource("report.md", "report", _report_bytes(plan, state, evidence))]

    budget_member, cost, cost_basis = _budget_member_and_claims(plan)
    if budget_member is not None:
        sources.append(CertificateSource("token/budget_actuals.json", "token_truth",
                                         budget_member))

    files = (
        ("token/token_truth.json", "token_truth", export / "token_truth.json"),
        ("verdicts/dod_result.json", "verdicts", evidence / "dod_result.json"),
        ("verdicts/final_verifier_report.json", "verdicts", export / "final_verifier_report.json"),
        ("ownership/ownership.json", "ownership", export / OWNERSHIP_FILENAME),
        ("run_manifest/run_manifest_index.json", "run_manifest",
         evidence / "run_manifest_index.json"),
        ("run_manifest/run_manifest.json", "run_manifest", evidence / "run_manifest.json"),
    )
    for archive, member_class, path in files:
        data = _read_regular(path)
        if data is not None:
            sources.append(CertificateSource(archive, member_class, data))

    diff_path, _why = job_result_diff_source(plan)
    if diff_path is not None:
        data = _read_regular(Path(diff_path))
        if data is not None:
            sources.append(CertificateSource(
                "diff/result.diff", "diff", data,
                obtain=f"Fetch jobs/{job_id}/result.diff from the Remedy data folder that ran "
                       f"this job; its sha256 is in this manifest."))

    log_dir = run_log_dir(job_id)
    if log_dir.is_dir():
        for log in sorted(log_dir.glob("*.jsonl"), key=lambda p: p.name):
            data = _read_regular(log)
            if data is not None:
                sources.append(CertificateSource(
                    f"logs/{log.name}", "log", data,
                    obtain=f"Fetch job_logs/{job_id}/{log.name} from the Remedy data folder "
                           f"that ran this job; its sha256 is in this manifest."))

    claims = {
        "terminal_state": state,
        "dod_summary": _dod_summary(job_id),
        "cost": cost,
        "cost_basis": cost_basis,
        "decisions_count": len(list_decisions(plan, [])),
        "regression_status": _regression_status(
            _read_regular(export / "final_verifier_report.json")),
    }
    return CertificateInputs(job_id=job_id, project_id=plan.project_id or "",
                             sources=tuple(sources), claims=claims,
                             issue=next_certificate_issue(job_id))


# WHY: the issue number is the count of certificates already recorded plus one.
def next_certificate_issue(job_id: str) -> int:
    path = job_dir(job_id) / CERTIFICATE_ISSUES_FILENAME
    if not path.is_file():
        return 1
    lines = path.read_text(encoding="utf-8").splitlines()
    return sum(1 for line in lines if line.strip()) + 1


# WHY: the only write of this module, so the next issue of a resumed job is higher.
def record_certificate_issue(job_id: str, *, issue: int, created: str, path: str,
                             manifest_sha256: str) -> None:
    target = job_dir(job_id) / CERTIFICATE_ISSUES_FILENAME
    line = json.dumps({"issue": issue, "created": created, "path": path,
                       "manifest_sha256": manifest_sha256})
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
