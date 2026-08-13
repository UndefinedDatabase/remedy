"""
Structured Code Patch Intent v1 — machine-applicable file operations and diffs.

Extends the patch intent system to support structured changes:
- file_ops: create/modify/delete with explicit content
- unified_diff: standard unified diff format
- markdown_proposal: narrative description (existing, non-applicable)

Public API::

    parse_structured_patch(raw_output: str) -> StructuredPatch
    validate_structured_patch(patch: StructuredPatch) -> list[str]
    extract_json_object(raw_output: str) -> str | None
    unsafe_path_issues(paths: Iterable[str]) -> list[str]
    StructuredPatch, FileOp, UnifiedDiff
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class FileOp:
    """A single file operation."""
    path: str
    action: Literal["create", "modify", "delete"]
    language: str = ""
    content: str = ""
    before_hash: str = ""
    risk: str = "low"
    summary: str = ""


@dataclass(frozen=True)
class UnifiedDiff:
    """A unified diff for a single file."""
    path: str
    diff: str
    before_hash: str = ""
    risk: str = "low"
    summary: str = ""


@dataclass(frozen=True)
class StructuredPatch:
    """Complete structured patch from builder output."""
    intent_kind: Literal["markdown", "file_ops", "unified_diff"]
    markdown_proposal: str = ""
    file_ops: tuple[FileOp, ...] = ()
    unified_diffs: tuple[UnifiedDiff, ...] = ()
    target_paths: tuple[str, ...] = ()
    risk: str = "low"
    applicability: str = "applicable"
    requires_approval: bool = True


# The repository's one reading of a ```json fenced block: hoisted out of
# parse_structured_patch so extract_json_object shares it and the two cannot drift.
_JSON_FENCE_RE = re.compile(r"```(?:json)?\s*\n(\{[\s\S]*?\})\s*\n```")


def parse_structured_patch(raw_output: str) -> StructuredPatch:
    """Parse builder output into a structured patch.

    Looks for JSON fenced blocks first, then falls back to
    unified diff detection.
    """
    # Try JSON fenced block
    json_match = _JSON_FENCE_RE.search(raw_output)
    if json_match:
        try:
            data = json.loads(json_match.group(1))
            return _parse_json_patch(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            pass

    # Try plain JSON (no fencing)
    stripped = raw_output.strip()
    if stripped.startswith("{"):
        try:
            data = json.loads(stripped)
            if isinstance(data, dict) and ("file_ops" in data or "unified_diffs" in data):
                return _parse_json_patch(data)
        except (json.JSONDecodeError, KeyError, TypeError):
            # JSON with trailing text — find closing brace
            json_text = _extract_first_json_object(stripped)
            if json_text:
                try:
                    data = json.loads(json_text)
                    if isinstance(data, dict) and ("file_ops" in data or "unified_diffs" in data):
                        return _parse_json_patch(data)
                except (json.JSONDecodeError, KeyError, TypeError):
                    pass

    # Try unified diff detection
    if _looks_like_diff(raw_output):
        return _parse_diff_output(raw_output)

    # Fallback: narrative/markdown only
    return StructuredPatch(
        intent_kind="markdown",
        markdown_proposal=raw_output[:2000],
        applicability="not_applicable",
        requires_approval=True,
    )


def _extract_first_json_object(text: str) -> str | None:
    """Extract first balanced JSON object from text with trailing content."""
    depth = 0
    in_string = False
    escape = False
    for i, ch in enumerate(text):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_string:
            escape = True
            continue
        if ch == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[:i + 1]
    return None


# The single answer to "where is the JSON object in this model output" — every
# schema-specific parser reuses it instead of growing a second wrapper scan.
def extract_json_object(raw_output: str) -> str | None:
    """Return the TEXT of the first JSON object in ``raw_output``, or None.

    Prefers a fenced ```json block, then a bare object at the start of the
    stripped text (with any trailing prose cut off). Returns TEXT rather than a
    parsed value, so each caller decides what schema that object must satisfy.
    """
    fenced = _JSON_FENCE_RE.search(raw_output)
    if fenced:
        return fenced.group(1)

    stripped = raw_output.strip()
    if stripped.startswith("{"):
        return _extract_first_json_object(stripped) or stripped

    return None


def _parse_json_patch(data: dict[str, Any]) -> StructuredPatch:
    """Parse a JSON structured patch."""
    if "file_ops" in data:
        ops = []
        for op in data["file_ops"]:
            ops.append(FileOp(
                path=str(op.get("path", "")),
                action=op.get("action", "modify"),
                language=str(op.get("language", "")),
                content=str(op.get("content", "")),
                before_hash=str(op.get("before_hash", "")),
                risk=str(op.get("risk", "low")),
                summary=str(op.get("summary", "")),
            ))
        paths = tuple(op.path for op in ops)
        return StructuredPatch(
            intent_kind="file_ops",
            file_ops=tuple(ops),
            target_paths=paths,
            risk=str(data.get("risk", "low")),
            applicability="applicable",
            requires_approval=True,
        )

    if "unified_diffs" in data:
        diffs = []
        for d in data["unified_diffs"]:
            diffs.append(UnifiedDiff(
                path=str(d.get("path", "")),
                diff=str(d.get("diff", "")),
                before_hash=str(d.get("before_hash", "")),
                risk=str(d.get("risk", "low")),
                summary=str(d.get("summary", "")),
            ))
        paths = tuple(d.path for d in diffs)
        return StructuredPatch(
            intent_kind="unified_diff",
            unified_diffs=tuple(diffs),
            target_paths=paths,
            risk=str(data.get("risk", "low")),
            applicability="applicable",
            requires_approval=True,
        )

    # JSON but no recognized structure
    return StructuredPatch(
        intent_kind="markdown",
        markdown_proposal=json.dumps(data, indent=2)[:2000],
        applicability="not_applicable",
        requires_approval=True,
    )


def _looks_like_diff(text: str) -> bool:
    """Check if text looks like a unified diff."""
    return bool(re.search(r"^---\s+\S+", text, re.MULTILINE) and
                re.search(r"^\+\+\+\s+\S+", text, re.MULTILINE) and
                re.search(r"^@@\s", text, re.MULTILINE))


def _parse_diff_output(text: str) -> StructuredPatch:
    """Parse unified diff text into structured diffs."""
    diffs = []
    current_path = ""
    current_diff_lines: list[str] = []

    for line in text.split("\n"):
        if line.startswith("--- "):
            # Save previous
            if current_path and current_diff_lines:
                diffs.append(UnifiedDiff(
                    path=current_path,
                    diff="\n".join(current_diff_lines),
                ))
            current_diff_lines = [line]
        elif line.startswith("+++ "):
            # Extract path (strip a/ or b/ prefix)
            path = line[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
            current_path = path
            current_diff_lines.append(line)
        elif line.startswith("@@") or line.startswith("+") or line.startswith("-") or line.startswith(" "):
            current_diff_lines.append(line)

    # Save last
    if current_path and current_diff_lines:
        diffs.append(UnifiedDiff(
            path=current_path,
            diff="\n".join(current_diff_lines),
        ))

    if not diffs:
        return StructuredPatch(
            intent_kind="markdown",
            markdown_proposal=text[:2000],
            applicability="not_applicable",
            requires_approval=True,
        )

    paths = tuple(d.path for d in diffs)
    return StructuredPatch(
        intent_kind="unified_diff",
        unified_diffs=tuple(diffs),
        target_paths=paths,
        applicability="applicable",
        requires_approval=True,
    )


# The single statement of which paths a patch may never write, message strings
# included — every patch-shaped validator calls this instead of restating the rules.
def unsafe_path_issues(paths: Iterable[str]) -> list[str]:
    """Return one issue string per path-safety violation (empty = every path safe).

    Three checks, in order, per path: absolute path, ``..`` traversal, and the
    sensitive-suffix set. The message strings are part of the contract.
    """
    issues: list[str] = []
    for p in paths:
        if p.startswith("/") or p.startswith("\\"):
            issues.append(f"absolute path not allowed: {p}")
        if ".." in p:
            issues.append(f"path traversal not allowed: {p}")
        lower = p.lower()
        if lower.endswith((".env", ".pem", ".key", ".p12")):
            issues.append(f"sensitive file not allowed: {p}")
    return issues


def validate_structured_patch(patch: StructuredPatch) -> list[str]:
    """Validate a structured patch. Returns list of issues (empty = valid)."""
    issues: list[str] = []

    if patch.intent_kind == "file_ops":
        for op in patch.file_ops:
            if not op.path:
                issues.append("file_op has empty path")
            if op.action not in ("create", "modify", "delete"):
                issues.append(f"invalid action: {op.action}")
            if op.action in ("create", "modify") and not op.content:
                issues.append(f"file_op {op.path}: create/modify needs content")

    elif patch.intent_kind == "unified_diff":
        for d in patch.unified_diffs:
            if not d.path:
                issues.append("unified_diff has empty path")
            if not d.diff:
                issues.append(f"unified_diff {d.path}: empty diff")

    # Path safety checks
    issues.extend(unsafe_path_issues(patch.target_paths))

    return issues
