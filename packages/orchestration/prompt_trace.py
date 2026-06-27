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
    context_categories: list[str] = field(default_factory=list)
    changed_files: list[str] = field(default_factory=list)
    safe_diff_files: list[str] = field(default_factory=list)
    task_excerpt_sha256: str = ""
    prompt_text_redacted: str = ""
    prompt_text_truncated: bool = False
    prompt_text_unavailable_reason: str = ""
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
) -> PromptTraceEntry:
    """Build a redacted, capped prompt trace entry."""
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
        context_categories=list(context_categories or []),
        changed_files=list(changed_files or []),
        safe_diff_files=list(safe_diff_files or []),
        task_excerpt_sha256=task_excerpt_sha256,
        prompt_text_redacted=capped,
        prompt_text_truncated=truncated,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def trace_entry_to_dict(entry: PromptTraceEntry) -> dict[str, Any]:
    return asdict(entry)


def write_trace_jsonl(entries: list[PromptTraceEntry], path: Path) -> None:
    """Write prompt trace entries as JSONL (one JSON object per line)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for entry in entries:
            f.write(json.dumps(trace_entry_to_dict(entry)) + "\n")


def build_trace_summary(entries: list[PromptTraceEntry]) -> dict[str, Any]:
    """Build an aggregate summary of prompt trace entries."""
    builder_count = sum(1 for e in entries if e.role == "builder")
    reviewer_count = sum(1 for e in entries if e.role == "reviewer")
    total_chars = sum(e.prompt_chars for e in entries)
    total_tokens_est = sum(e.prompt_tokens_estimated for e in entries)
    providers = sorted({e.provider for e in entries if e.provider})

    return {
        "total_prompts": len(entries),
        "builder_prompts": builder_count,
        "reviewer_prompts": reviewer_count,
        "total_prompt_chars": total_chars,
        "total_prompt_tokens_estimated": total_tokens_est,
        "providers": providers,
        "rounds": max((e.round for e in entries), default=0),
    }
