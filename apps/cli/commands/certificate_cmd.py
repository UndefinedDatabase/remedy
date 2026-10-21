"""`remedy job certificate` and `remedy verify` — F060 T003, DECISION F060 D4.

`job certificate` makes the certificate of a job under its mission that has ended: it collects the
job's files through `collect_certificate_inputs`, builds the ZIP at `--out` (or in the current
folder, named after the job and the issue) with `build_job_certificate`, and only then records the
issue, so a refused build leaves no trace. `verify` checks a certificate with
`verify_job_certificate` and needs no job and no data folder: it reads the one file it is given.
Exit codes follow the CLI contract (docs/guides/exit-codes.md): 3 when the job has not ended or is
unknown (`certificate_not_ready`), 1 when the build is refused (`certificate_refused`) or the
certificate is not intact (`certificate_not_intact`), 2 for a `--max-bytes` that is not a whole
number of at least 1 (`invalid_max_bytes`) — and whatever `resolve_job_id_or_fail` answers for the
job id itself, unchanged.
"""
from __future__ import annotations

import hashlib
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from apps.cli.job_id_arg import resolve_job_id_or_fail
from apps.cli.json_envelope import emit_ok, fail

if TYPE_CHECKING:
    import argparse
    from collections.abc import Callable

EXIT_REFUSED = 1
EXIT_USAGE = 2
EXIT_NOT_READY = 3
EXIT_NOT_INTACT = 1


def _budget_or_fail(raw: str | None, *, json_output: bool) -> int:
    from packages.orchestration.job_certificate import CERTIFICATE_DEFAULT_MAX_BYTES

    if raw is None:
        return CERTIFICATE_DEFAULT_MAX_BYTES
    try:
        budget = int(raw)
    except ValueError:
        budget = 0
    if budget < 1:
        fail("invalid_max_bytes", f"--max-bytes must be a whole number of at least 1, not {raw!r}.",
             json_output=json_output, exit_code=EXIT_USAGE)
    return budget


def _cmd_job_certificate(job_id_str: str, *, out: str | None, max_bytes: str | None,
                         json_output: bool = False) -> None:
    from packages.orchestration.job_certificate import (
        CERTIFICATE_NOT_A_SIGNATURE,
        CertificateError,
        build_job_certificate,
        render_certificate_manifest,
    )
    from packages.orchestration.job_certificate_sources import (
        CertificateNotReadyError,
        collect_certificate_inputs,
        record_certificate_issue,
    )

    job_id = resolve_job_id_or_fail(job_id_str, json_output=json_output)
    budget = _budget_or_fail(max_bytes, json_output=json_output)
    try:
        inputs = collect_certificate_inputs(job_id)
    except CertificateNotReadyError as exc:
        fail("certificate_not_ready", str(exc), json_output=json_output,
             exit_code=EXIT_NOT_READY, job_id=job_id)
    except CertificateError as exc:
        fail("certificate_refused", str(exc), json_output=json_output,
             exit_code=EXIT_REFUSED, job_id=job_id)

    issue = inputs.issue
    target = out if out else Path.cwd() / f"remedy-certificate-{job_id}-{issue}.zip"
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        built = build_job_certificate(
            out_path=target, job_id=job_id, project_id=inputs.project_id, created=created,
            issue=issue, sources=inputs.sources, claims=inputs.claims, size_budget_bytes=budget)
    except CertificateError as exc:
        fail("certificate_refused", str(exc), json_output=json_output,
             exit_code=EXIT_REFUSED, job_id=job_id)

    manifest = built["manifest"]
    path = os.path.abspath(built["path"])
    manifest_sha256 = hashlib.sha256(render_certificate_manifest(manifest)).hexdigest()
    record_certificate_issue(job_id, issue=issue, created=created, path=path,
                             manifest_sha256=manifest_sha256)

    terminal_state = inputs.claims["terminal_state"]
    members = [entry["path"] for entry in manifest["members"]]
    referenced = [entry["path"] for entry in manifest["referenced"]]
    if json_output:
        emit_ok(path=path, job_id=job_id, issue=issue, terminal_state=terminal_state,
                members=members, referenced=referenced, size_budget_bytes=budget,
                manifest_sha256=manifest_sha256)
        return
    print(f"Certificate written: {path}")
    print(f"Job {job_id} ended {terminal_state}; certificate issue {issue}.")
    print(f"Members: {len(members)} embedded, {len(referenced)} referenced (budget {budget} bytes).")
    print(CERTIFICATE_NOT_A_SIGNATURE)


def _cmd_verify(bundle: str, *, json_output: bool = False) -> None:
    from packages.orchestration.job_certificate_verify import (
        render_certificate_verdict,
        verify_job_certificate,
    )

    verification = verify_job_certificate(bundle)
    if json_output:
        if verification.ok:
            emit_ok(intact=True, problems=[], manifest=verification.manifest)
            return
        fail("certificate_not_intact",
             f"The certificate is not intact: {len(verification.problems)} problem(s).",
             json_output=True, exit_code=EXIT_NOT_INTACT, intact=False,
             problems=list(verification.problems), manifest=verification.manifest)
    sys.stdout.write(render_certificate_verdict(verification))
    if not verification.ok:
        sys.exit(EXIT_NOT_INTACT)


COMMAND_HANDLERS: dict[str, Callable[[argparse.Namespace], None]] = {
    "job.certificate": lambda args: _cmd_job_certificate(
        getattr(args, "job_id", "") or "",
        out=getattr(args, "out", None),
        max_bytes=getattr(args, "max_bytes", None),
        json_output=bool(getattr(args, "json", False)),
    ),
    "verify.run": lambda args: _cmd_verify(
        getattr(args, "bundle", "") or "",
        json_output=bool(getattr(args, "json", False)),
    ),
}
