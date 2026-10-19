#!/usr/bin/env python3
"""Reject newly staged sensitive content under ``.agent``.

Historical development records remain readable in Git, so scanning whole files would make every
future state update impossible. The commit hook instead scans only added lines and newly staged
binary members. Deletions are always allowed.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import PurePosixPath
from typing import NamedTuple


class Finding(NamedTuple):
    path: str
    line: int
    reason: str


_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "credential",
        re.compile(
            r"(?i)(?:"
            r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----|"
            r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}|"
            r"(?<![A-Za-z0-9])(?:sk-(?:ant-)?[A-Za-z0-9_-]{12,}|"
            r"gh[pousr]_[A-Za-z0-9]{20,}|glpat-[A-Za-z0-9_-]{15,}|"
            r"xox[abprs]-[A-Za-z0-9-]{10,}|(?:AKIA|ASIA)[A-Z0-9]{16})|"
            r"\b(?:api[_-]?key|access[_-]?token|refresh[_-]?token|auth[_-]?token|"
            r"client[_-]?secret|password|passwd|secret)\b\s*[:=]\s*[\"']?"
            r"(?!\[REDACTED\])[^\s,;\"']{8,}"
            r")"
        ),
    ),
    ("machine-local path", re.compile(r"(?:^|[\s'\"`(])(?:/home/[^\s'\"`]+|/Users/[^\s'\"`]+|[A-Za-z]:\\Users\\[^\s'\"`]+)")),
    ("provider session URL", re.compile(r"https://(?:claude\.ai/code/session_|chatgpt\.com/(?:share|c)/)\S+", re.IGNORECASE)),
    ("private network address", re.compile(r"(?<!\d)(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})(?!\d)")),
)


def _is_agent_path(path: str) -> bool:
    normalized = str(PurePosixPath(path.replace("\\", "/")))
    return normalized == ".agent" or normalized.startswith(".agent/")


def scan_agent_text(path: str, text: str, *, start_line: int = 1) -> list[Finding]:
    """Return sensitive-content findings for text destined for an ``.agent`` path."""
    if not _is_agent_path(path):
        return []
    findings: list[Finding] = []
    for offset, line in enumerate(text.splitlines(), start=start_line):
        for reason, pattern in _RULES:
            if pattern.search(line):
                findings.append(Finding(path, offset, reason))
    return findings


def scan_staged_diff(diff_text: str) -> list[Finding]:
    """Scan added lines and binary additions from a zero-context staged Git diff."""
    findings: list[Finding] = []
    current_path = ""
    target_line = 0
    for line in diff_text.splitlines():
        if line.startswith("+++ "):
            raw = line[4:]
            current_path = "" if raw == "/dev/null" else raw.removeprefix("b/")
            continue
        hunk = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if hunk:
            target_line = int(hunk.group(1))
            continue
        if line.startswith("Binary files ") and " and b/.agent/" in line and line.endswith(" differ"):
            path = line.rsplit(" and b/", 1)[1].removesuffix(" differ")
            findings.append(Finding(path, 0, "binary agent-state file"))
            continue
        if line.startswith("+") and not line.startswith("+++"):
            findings.extend(scan_agent_text(current_path, line[1:], start_line=target_line))
            target_line += 1
        elif line.startswith(" "):
            target_line += 1
    return findings


def staged_diff() -> str:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--unified=0", "--no-color", "--", ".agent"],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "git diff failed")
    return proc.stdout


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--staged", action="store_true", help="scan the staged .agent diff")
    args = parser.parse_args(argv)
    try:
        diff_text = staged_diff() if args.staged else sys.stdin.read()
    except RuntimeError as exc:
        print(f"agent hygiene check failed: {exc}", file=sys.stderr)
        return 2
    findings = scan_staged_diff(diff_text)
    for finding in findings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"{location}: refused {finding.reason}", file=sys.stderr)
    if findings:
        print("Redact or remove sensitive agent-state additions before committing.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
