"""F1/F2 — the ONE shared CLI-to-run invocation structure for the F012 material controls.

Every public lifecycle command that ultimately calls ``run_job`` (``do job-run``, ``do
job-resume``, ``do job-flow``) resolves its invocation controls through this single structure.
Its whole purpose is to PRESERVE the omission sentinel: a control the operator did not supply
stays ``None`` all the way into ``run_job``, so ``run_job``'s explicit(non-None) > persisted >
product-default precedence is honoured end to end. No command may reintroduce ``or 0`` /
``or False`` / ``or "normal"`` or a pre-resolved product default for these controls.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RunInvocation:
    """The tri-state invocation controls resolved from a parsed CLI namespace. Each field is
    ``None`` when the flag was omitted."""

    timeout_sec: int | None = None
    timeout_profile: str | None = None
    max_output_chars: int | None = None
    stream_evidence: bool | None = None      # None omitted / True --stream-evidence / False --no-...
    max_tasks: int | None = None

    def as_run_job_kwargs(self) -> dict[str, Any]:
        """The exact keyword arguments ``run_job`` accepts for these controls — omission preserved."""
        return {
            "timeout_sec": self.timeout_sec,
            "timeout_profile": self.timeout_profile,
            "max_output_chars": self.max_output_chars,
            "stream_evidence": self.stream_evidence,
            "max_tasks": self.max_tasks,
        }


def _opt_int(args: Any, name: str) -> int | None:
    v = getattr(args, name, None)
    if v is None or v == "":
        return None
    return int(v)


def _opt_str(args: Any, name: str) -> str | None:
    v = getattr(args, name, None)
    if v is None or v == "":
        return None
    return str(v)


def invocation_from_args(args: Any) -> RunInvocation:
    """Build the invocation from a parsed grouped-CLI namespace, preserving every omission.

    ``stream_evidence`` is already tri-state on the namespace: the parser uses ``store_const``
    for ``--stream-evidence`` (True) and ``--no-stream-evidence`` (False) with ``default=None``.
    """
    return RunInvocation(
        timeout_sec=_opt_int(args, "timeout_sec"),
        timeout_profile=_opt_str(args, "timeout_profile"),
        max_output_chars=_opt_int(args, "max_output_chars"),
        stream_evidence=getattr(args, "stream_evidence", None),
        max_tasks=_opt_int(args, "max_tasks"),
    )
