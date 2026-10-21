#!/usr/bin/env python3
"""Reject newly staged sensitive content under ``.agent``.

Historical development records remain readable in Git, so scanning whole files would make every
future state update impossible. The commit hook instead scans only added lines and newly staged
binary members. Deletions are always allowed, and so is the ledger rotation's move: a line added to
the archive that the same commit deletes from the ledger is a record Git already holds.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from collections.abc import Iterator
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

# The finding ledger and the archive its rotation moves records into, byte-verbatim
# (`scripts/rotate_live_review.py`, R-1376).
LIVE_REVIEW_LEDGER_PATH = ".agent/live_review.md"
LIVE_REVIEW_ARCHIVE_PATH = ".agent/live_review_archive.md"

_HUNK_HEADER = re.compile(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@")


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


def _diff_path(raw: str, prefix: str) -> str:
    return "" if raw == "/dev/null" else raw.removeprefix(prefix)


# Yields (in a file header, old path, new path, line) for every line of a zero-context diff. A
# file's header runs from its `diff --git` line to its first hunk, so a body line that starts with
# `+++ ` or `--- ` is content, never a file name (R-1412).
def _walk_staged_diff(diff_text: str) -> Iterator[tuple[bool, str, str, str]]:
    old_path = new_path = ""
    in_header = True
    for line in diff_text.splitlines():
        if line.startswith("diff --git "):
            in_header, old_path, new_path = True, "", ""
        elif in_header and line.startswith("--- "):
            old_path = _diff_path(line[4:], "a/")
        elif in_header and line.startswith("+++ "):
            new_path = _diff_path(line[4:], "b/")
        elif line.startswith("@@ "):
            in_header = False
            yield True, old_path, new_path, line
            continue
        yield in_header, old_path, new_path, line


# The lines the diff deletes from the ledger, counted, which the archive may receive unscanned.
def _ledger_lines_deleted(diff_text: str) -> Counter[str]:
    deleted: Counter[str] = Counter()
    for in_header, old_path, _new_path, line in _walk_staged_diff(diff_text):
        if not in_header and old_path == LIVE_REVIEW_LEDGER_PATH and line.startswith("-"):
            deleted[line[1:]] += 1
    return deleted


def scan_staged_diff(diff_text: str) -> list[Finding]:
    """Scan added lines and binary additions from a zero-context staged Git diff."""
    movable = _ledger_lines_deleted(diff_text)
    findings: list[Finding] = []
    target_line = 0
    for in_header, _old_path, path, line in _walk_staged_diff(diff_text):
        if in_header:
            hunk = _HUNK_HEADER.match(line)
            if hunk:
                target_line = int(hunk.group(1))
            elif line.startswith("Binary files ") and " and b/.agent/" in line and line.endswith(" differ"):
                binary = line.rsplit(" and b/", 1)[1].removesuffix(" differ")
                findings.append(Finding(binary, 0, "binary agent-state file"))
            continue
        if line.startswith("+"):
            if path == LIVE_REVIEW_ARCHIVE_PATH and movable[line[1:]] > 0:
                movable[line[1:]] -= 1
            else:
                findings.extend(scan_agent_text(path, line[1:], start_line=target_line))
            target_line += 1
        elif line.startswith(" "):
            target_line += 1
    return findings


def scan_staged_modes(changed_output: bytes, index_output: bytes) -> list[Finding]:
    """Reject changed agent-state entries that are not regular index files."""
    changed = {
        raw.decode("utf-8", errors="surrogateescape")
        for raw in changed_output.split(b"\0")
        if raw
    }
    findings: list[Finding] = []
    for raw in index_output.split(b"\0"):
        if not raw or b"\t" not in raw:
            continue
        metadata, raw_path = raw.split(b"\t", 1)
        path = raw_path.decode("utf-8", errors="surrogateescape")
        fields = metadata.split()
        if path in changed and _is_agent_path(path) and fields and fields[0] not in {b"100644", b"100755"}:
            findings.append(Finding(path, 0, "non-regular agent-state entry"))
    return findings


def _git_bytes(args: list[str]) -> bytes:
    proc = subprocess.run(["git", *args], check=False, capture_output=True)
    if proc.returncode != 0:
        message = proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or f"git {' '.join(args)} failed")
    return proc.stdout


def staged_diff() -> str:
    output = _git_bytes([
        "diff", "--cached", "--unified=0", "--no-color", "--no-ext-diff", "--no-textconv",
        "--", ".agent",
    ])
    return output.decode("utf-8", errors="strict")


def staged_mode_findings() -> list[Finding]:
    changed = _git_bytes([
        "diff", "--cached", "--name-only", "-z", "--diff-filter=ACMR", "--", ".agent",
    ])
    index_entries = _git_bytes(["ls-files", "--stage", "-z", "--", ".agent"])
    return scan_staged_modes(changed, index_entries)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--staged", action="store_true", help="scan the staged .agent diff")
    args = parser.parse_args(argv)
    try:
        diff_text = staged_diff() if args.staged else sys.stdin.read()
        mode_findings = staged_mode_findings() if args.staged else []
    except (RuntimeError, UnicodeDecodeError) as exc:
        print(f"agent hygiene check failed: {exc}", file=sys.stderr)
        return 2
    findings = scan_staged_diff(diff_text) + mode_findings
    for finding in findings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"{location}: refused {finding.reason}", file=sys.stderr)
    if findings:
        print("Redact or remove sensitive agent-state additions before committing.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
