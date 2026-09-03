"""Prompt trace model — durable, redacted record of every provider prompt.

Each trace entry captures what Remedy actually sent to a Builder or Reviewer
provider, with secrets redacted and prompt text capped. External reviewers
can inspect traces without needing access to the original run.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from packages.orchestration.prompt_segments import ComposedPrompt

_PROMPT_TEXT_CAP = 50_000

_SECRET_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"sk-ant-[a-zA-Z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),
    re.compile(r"ghs_[a-zA-Z0-9]{36}"),
    re.compile(r"glpat-[a-zA-Z0-9_-]{20,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._~+/=-]{20,}"),
]

_ENV_KEY_RE = re.compile(
    r"(API_KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL|PRIVATE_KEY)\s*=\s*\S+",
    re.IGNORECASE,
)

_PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN\s+(RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----.*?-----END\s+\1?PRIVATE KEY-----",
    re.DOTALL,
)


def redact_prompt_text(text: str) -> str:
    """Redact secrets, API keys, bearer tokens, private keys from prompt text."""
    for pat in _SECRET_PATTERNS:
        text = pat.sub("[REDACTED]", text)
    text = _ENV_KEY_RE.sub(r"\1=[REDACTED]", text)
    text = _PRIVATE_KEY_RE.sub("[PRIVATE_KEY_REDACTED]", text)
    return text


def _cap_text(text: str, cap: int = _PROMPT_TEXT_CAP) -> tuple[str, bool]:
    if len(text) <= cap:
        return text, False
    return text[:cap] + "\n[PROMPT_TEXT_TRUNCATED]", True


@dataclass
class PromptTraceEntry:
    """One provider prompt trace record."""
    run_id: str = ""
    job_id: str = ""
    task_id: str = ""
    round: int = 0
    role: str = ""  # "builder" or "reviewer"
    provider: str = ""
    provider_kind: str = ""
    cwd: str = ""
    write_mode: str = ""
    prompt_kind: str = ""  # "initial", "repair", "review", "re-review"
    prompt_sha256: str = ""
    prompt_chars: int = 0
    prompt_tokens_estimated: int = 0
    #: F105: the composed-prompt segment manifest — one row per registered
    #: segment with name, rank, sha256, chars and tokens_estimated, in
    #: composition order. Empty means this prompt was NOT composed through the
    #: prompt-segment registry, not that composition produced no segments.
    segment_manifest: list[dict[str, str | int]] = field(default_factory=list)
    #: F105: the character count ``segment_manifest`` ACCOUNTS FOR — the
    #: composed base prompt. The gap to ``prompt_chars`` is the schema tail
    #: ``run_structured_call`` appends outside every builder, which F105
    #: deliberately does NOT register (DECISION F105 D3); recording both numbers
    #: makes that coverage gap visible instead of implied.
    segment_manifest_chars: int = 0
    #: F109: the names of the segments whose TEXT this composition replaced with
    #: a dedupe reference marker, in replacement order — what the model was
    #: deliberately NOT sent again. EMPTY means nothing was deduped, which is the
    #: NORMAL case: dedupe fires only for a call that RESUMES a session that
    #: provably already received the segment. Empty here does NOT mean the prompt
    #: was uncomposed — that is what an empty ``segment_manifest`` means, and the
    #: two empties sit next to each other, so do not read one for the other.
    deduped_segment_names: list[str] = field(default_factory=list)
    context_categories: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    safe_diff_files: list[str] = field(default_factory=list)
    task_excerpt_sha256: str = ""
    prompt_text_redacted: str = ""
    prompt_text_truncated: bool = False
    prompt_text_unavailable_reason: str = ""
    configured_model: str = ""
    #: F005: the enforced-output schema version for this structured call
    #: ("" when the call used the legacy free-text path).
    schema_v: str = ""
    #: F005: the logical phase of the call ("review" | "parse-retry" | ...).
    phase: str = ""
    #: F005: 1-based transport attempt of this logical call; >1 means the F001
    #: transport retry fired. One trace exists per ACTUAL provider invocation.
    transport_attempt: int = 0
    is_transport_retry: bool = False
    created_at: str = ""


def build_trace_entry(
    *,
    prompt_text: str,
    role: str,
    run_id: str = "",
    job_id: str = "",
    task_id: str = "",
    round_num: int = 0,
    provider: str = "",
    provider_kind: str = "",
    cwd: str = "",
    write_mode: str = "",
    prompt_kind: str = "",
    context_categories: list[str] | None = None,
    changed_files: list[str] | None = None,
    safe_diff_files: list[str] | None = None,
    task_excerpt_sha256: str = "",
    configured_model: str = "",
    schema_v: str = "",
    phase: str = "",
    transport_attempt: int = 0,
    is_transport_retry: bool = False,
    composed_prompt: ComposedPrompt | None = None,
) -> PromptTraceEntry:
    """Build a redacted, capped prompt trace entry.

    ``composed_prompt`` is the F105 seam: BOTH ``segment_manifest`` and
    ``segment_manifest_chars`` are derived from it, so the manifest and the
    character count it covers can never disagree. Passing the two separately is
    deliberately NOT offered — a caller that could set them independently could
    describe one prompt with another prompt's manifest.
    ``deduped_segment_names`` (F109) joins those two on the same seam and is
    derived from the same object for the same reason: a caller that could pass
    its own list could name segments the prompt never replaced.
    """
    raw_sha = hashlib.sha256(prompt_text.encode()).hexdigest()
    redacted = redact_prompt_text(prompt_text)
    capped, truncated = _cap_text(redacted)

    return PromptTraceEntry(
        run_id=run_id,
        job_id=job_id,
        task_id=task_id,
        round=round_num,
        role=role,
        provider=provider,
        provider_kind=provider_kind,
        cwd=cwd,
        write_mode=write_mode,
        prompt_kind=prompt_kind,
        prompt_sha256=raw_sha,
        prompt_chars=len(prompt_text),
        prompt_tokens_estimated=len(prompt_text) // 4,
        segment_manifest=(
            composed_prompt.manifest_as_dicts() if composed_prompt is not None else []
        ),
        segment_manifest_chars=(
            len(composed_prompt.text) if composed_prompt is not None else 0
        ),
        deduped_segment_names=(
            list(composed_prompt.deduped_names) if composed_prompt is not None else []
        ),
        context_categories=list(context_categories or []),
        changed_files=list(changed_files or []),
        safe_diff_files=list(safe_diff_files or []),
        task_excerpt_sha256=task_excerpt_sha256,
        prompt_text_redacted=capped,
        prompt_text_truncated=truncated,
        configured_model=configured_model,
        schema_v=schema_v,
        phase=phase,
        transport_attempt=transport_attempt,
        is_transport_retry=is_transport_retry,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def _sanitize_cwd(cwd: str) -> str:
    """Replace absolute staging paths with safe labels."""
    if not cwd:
        return cwd
    if "/tmp/remedy-pingpong-" in cwd:
        return "[staging]"
    if cwd.startswith("/tmp/"):
        return "[tmpdir]"
    return cwd


def trace_entry_to_dict(entry: PromptTraceEntry) -> dict[str, Any]:
    d = asdict(entry)
    d["cwd"] = _sanitize_cwd(d.get("cwd", ""))
    return d


def write_trace_jsonl(entries: list[PromptTraceEntry], path: Path) -> None:
    """Write prompt trace entries as JSONL (one JSON object per line)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for entry in entries:
            f.write(json.dumps(trace_entry_to_dict(entry)) + "\n")


# Two writers, because the trace file is per JOB and not per run:
# `RunLogWriter.path.parent` is `<runs_root>/<job_id>/`, so a second command
# against the same job would truncate the first command's traces if it used
# `write_trace_jsonl`. The command that CREATES a job writes; a command that
# adds traces to a job that already has some appends (F105 R28).
def append_trace_jsonl(entries: list[PromptTraceEntry], path: Path) -> None:
    """Append prompt trace entries to a JSONL file, creating it if absent."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        for entry in entries:
            f.write(json.dumps(trace_entry_to_dict(entry)) + "\n")


def build_trace_summary(entries: list[PromptTraceEntry]) -> dict[str, Any]:
    """Build an aggregate summary of prompt trace entries."""
    builder_count = sum(1 for e in entries if e.role == "builder")
    reviewer_count = sum(1 for e in entries if e.role == "reviewer")
    total_chars = sum(e.prompt_chars for e in entries)
    total_tokens_est = sum(e.prompt_tokens_estimated for e in entries)
    providers = sorted({e.provider for e in entries if e.provider})

    per_role: dict[str, dict[str, Any]] = {}
    for e in entries:
        if not e.role:
            continue
        if e.role not in per_role:
            per_role[e.role] = {
                "configured_provider": e.provider,
                "configured_model": e.configured_model,
                "actual_provider": e.provider,
                "actual_model": e.configured_model,
                "model_resolution_source": "cli" if e.configured_model else "default",
                "actual_model_verified": False,
                "prompt_count": 0,
            }
        per_role[e.role]["prompt_count"] += 1

    return {
        "total_prompts": len(entries),
        "builder_prompts": builder_count,
        "reviewer_prompts": reviewer_count,
        "total_prompt_chars": total_chars,
        "total_prompt_tokens_estimated": total_tokens_est,
        "providers": providers,
        "rounds": max((e.round for e in entries), default=0),
        "per_role_model_summary": per_role,
    }
