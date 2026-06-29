"""Review Scope Packet — deterministic per-task review-scoping metadata.

After a Builder completes a task, ``build_review_scope_packet`` summarises *what
changed* and *how much review effort it deserves* into a single JSON-serialisable
dict (``review_scope_packet.json``). A Reviewer (human or model) can read this
instead of re-deriving scope from the raw diff every time. ``render_scope_markdown``
renders the same packet as human-readable Markdown, and ``write_review_scope_packet``
writes both artifacts into the task evidence dir.

Pure deterministic analysis:
- No provider calls. No Claude. No AST parsing (simple regex on the diff).
- Read-only analysis: never mutates the workspace or the target repo.
- Tolerant of missing evidence files — emits best-effort partial data.
"""
from __future__ import annotations

import json as _json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Symbol detection — line-based ONLY.
#
# Each added line is stripped and tested with ``re.Pattern.match`` against the
# anchored patterns below. We deliberately do NOT run ``finditer`` over the
# concatenated added text: that produced false positives from ``def``/``class``
# tokens appearing mid-line (e.g. inside strings, comments, or call sites).
# ---------------------------------------------------------------------------

_SYMBOL_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"^def\s+(\w+)"),
    re.compile(r"^async\s+def\s+(\w+)"),
    re.compile(r"^class\s+(\w+)"),
    re.compile(r"^export\s+function\s+(\w+)"),
    re.compile(r"^export\s+const\s+(\w+)\s*="),
    re.compile(r"^function\s+(\w+)"),
    re.compile(r"^const\s+(\w+)\s*="),
)

# Substrings that mark a file as security-sensitive for redaction.
_REDACTION_MARKERS = ("_redact", "_sanitize", "_safe_")
# Substrings that mark a file as auth/permission sensitive.
_AUTH_MARKERS = ("_auth", "authenticate", "authorize", "permission", "_token")

# File extensions that mark a change as configuration.
_CONFIG_EXTS = (".json", ".toml", ".yaml", ".yml")

_HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
# A new-file hunk header begins counting from line 0 of the old file.
_NEWFILE_HUNK_RE = re.compile(r"^@@ -0,0 ")
_IMPORT_RE = re.compile(r"^[+\-]\s*(?:from\s+\S+\s+import\b|import\s+\S+)")


def _strip_diff_prefix(path: str) -> str:
    """Strip leading ``a/`` or ``b/`` from a diff path."""
    if path.startswith(("a/", "b/")):
        return path[2:]
    return path


def _is_test_path(path: str) -> bool:
    name = Path(path).name
    return path.startswith("tests/") or "/tests/" in path or name.startswith("test_")


# ---------------------------------------------------------------------------
# Diff parsing
# ---------------------------------------------------------------------------

def _parse_diff(diff_text: str) -> dict[str, dict[str, Any]]:
    """Parse a unified diff into per-file analysis.

    Returns ``{path: {"ranges": [[s, e], ...], "added_lines": [...],
    "import_change": bool, "new_file": bool}}`` where ranges use the *new-file*
    line numbers from each hunk header. ``new_file`` is true when the old-file
    header is ``--- /dev/null`` or the first hunk header matches ``@@ -0,0 +...``.
    """
    files: dict[str, dict[str, Any]] = {}
    current: dict[str, Any] | None = None
    pending_old_path = ""
    pending_old_is_devnull = False

    for line in diff_text.splitlines():
        if line.startswith("--- "):
            old = line[4:].strip()
            pending_old_path = _strip_diff_prefix(old)
            pending_old_is_devnull = old == "/dev/null"
            continue
        if line.startswith("+++ "):
            new_path = line[4:].strip()
            path = pending_old_path if new_path == "/dev/null" else _strip_diff_prefix(new_path)
            current = files.setdefault(
                path,
                {"ranges": [], "added_lines": [], "import_change": False, "new_file": False},
            )
            if pending_old_is_devnull:
                current["new_file"] = True
            continue
        if current is None:
            continue
        if line.startswith("@@"):
            m = _HUNK_RE.match(line)
            if m:
                # First hunk starting at old line 0 means a newly added file.
                if not current["ranges"] and _NEWFILE_HUNK_RE.match(line):
                    current["new_file"] = True
                new_start = int(m.group(1))
                new_count = int(m.group(2)) if m.group(2) is not None else 1
                if new_count <= 0:
                    current["ranges"].append([new_start, new_start])
                else:
                    current["ranges"].append([new_start, new_start + new_count - 1])
            continue
        if line.startswith("+") and not line.startswith("+++"):
            current["added_lines"].append(line[1:])
            if _IMPORT_RE.match(line):
                current["import_change"] = True
        elif line.startswith("-") and not line.startswith("---"):
            if _IMPORT_RE.match(line):
                current["import_change"] = True

    return files


def _detect_symbols(added_lines: list[str]) -> list[str]:
    """Detect defined symbols by matching anchored patterns on stripped lines.

    Line-based only: each added line is stripped, then tested with
    ``pattern.match`` (anchored at start). The first pattern to match a line
    contributes its captured symbol name. No ``finditer`` over joined text.
    """
    found: list[str] = []
    seen: set[str] = set()
    for raw in added_lines:
        stripped = raw.strip()
        if not stripped:
            continue
        for pat in _SYMBOL_PATTERNS:
            m = pat.match(stripped)
            if m:
                name = m.group(1)
                if name not in seen:
                    seen.add(name)
                    found.append(name)
                break
    return found


def _risk_tags_for_file(
    path: str,
    added_text: str,
    symbols: list[str],
    new_file: bool = False,
) -> list[str]:
    """Return spec risk tags for a file.

    Only these tag strings are emitted: ``new_file``, ``new_function``,
    ``test_change``, ``config_change``, ``security:redaction``, ``security:auth``.
    """
    tags: list[str] = []
    lowered = added_text.lower()
    if any(marker in added_text for marker in _REDACTION_MARKERS):
        tags.append("security:redaction")
    if any(marker in lowered for marker in _AUTH_MARKERS):
        tags.append("security:auth")
    if new_file:
        tags.append("new_file")
    if symbols:
        tags.append("new_function")
    if _is_test_path(path):
        tags.append("test_change")
    ext = Path(path).suffix.lower()
    if ext in _CONFIG_EXTS:
        tags.append("config_change")
    return tags


# ---------------------------------------------------------------------------
# Evidence readers (best-effort, tolerant of missing files)
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _read_json(path: Path) -> Any:
    text = _read_text(path)
    if not text:
        return None
    try:
        return _json.loads(text)
    except _json.JSONDecodeError:
        return None


def _parse_test_results(text: str) -> dict[str, Any]:
    """Parse pytest-style output into a structured result."""
    lowered = text.lower()
    not_run = (not text.strip()) or "tests_not_run" in lowered or "not run" in lowered
    if not_run:
        return {
            "ran": False,
            "passed": 0,
            "failed": 0,
            "summary": "tests not run",
        }
    passed = sum(int(n) for n in re.findall(r"(\d+)\s+passed", text))
    failed = sum(int(n) for n in re.findall(r"(\d+)\s+failed", text))
    failed += sum(int(n) for n in re.findall(r"(\d+)\s+error", text))
    summary = ""
    for raw in reversed(text.splitlines()):
        line = raw.strip()
        if any(k in line.lower() for k in ("passed", "failed", "error")):
            summary = line.strip("= ").strip()
            break
    return {
        "ran": True,
        "passed": passed,
        "failed": failed,
        "summary": summary or "tests ran",
    }


def _collect_prompt_refs(trace_path: Path, rel_trace: str) -> tuple[list[str], list[str], list[str]]:
    """Return (prompt_hashes, worker_refs, reviewer_refs) from a prompt trace."""
    hashes: list[str] = []
    seen_hashes: set[str] = set()
    has_builder = False
    has_reviewer = False
    text = _read_text(trace_path)
    for raw in text.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            rec = _json.loads(raw)
        except _json.JSONDecodeError:
            continue
        sha = rec.get("prompt_sha256", "")
        if sha and sha not in seen_hashes:
            seen_hashes.add(sha)
            hashes.append(sha)
        role = rec.get("role", "")
        if role == "builder":
            has_builder = True
        elif role == "reviewer":
            has_reviewer = True
    worker = [rel_trace] if has_builder else []
    reviewer = [rel_trace] if has_reviewer else []
    return hashes, worker, reviewer


_BLOCKING_VERDICTS = {"needs_repair", "fail", "blocked"}


def _finding_id(finding: dict[str, Any]) -> str:
    return str(finding.get("id") or finding.get("finding_id") or "")


def _collect_open_findings(review: Any, repair: Any) -> list[dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    anonymous: list[dict[str, Any]] = []

    def add_finding(item: Any) -> None:
        if isinstance(item, str):
            item = {"id": item}
        if not isinstance(item, dict):
            return
        fid = _finding_id(item)
        if fid:
            existing = by_id.get(fid, {})
            by_id[fid] = {**existing, **item}
        else:
            anonymous.append(item)

    if isinstance(repair, dict):
        for item in repair.get("open_findings", []) or []:
            add_finding(item)

    review_findings_by_id: dict[str, dict[str, Any]] = {}

    if isinstance(review, dict):
        for rev in review.get("reviews", []) or []:
            if not isinstance(rev, dict):
                continue
            verdict = str(rev.get("verdict") or "").lower()
            if verdict not in _BLOCKING_VERDICTS:
                continue
            for item in rev.get("findings", []) or []:
                if isinstance(item, dict):
                    fid = _finding_id(item)
                    if fid:
                        review_findings_by_id[fid] = item
                add_finding(item)

    for fid, current in list(by_id.items()):
        richer = review_findings_by_id.get(fid)
        if richer:
            by_id[fid] = {**current, **richer}

    return list(by_id.values()) + anonymous


# ---------------------------------------------------------------------------
# Scope recommendation
# ---------------------------------------------------------------------------

def _recommend_scope(
    *,
    file_count: int,
    hunk_count: int,
    has_security: bool,
    test_failed: bool,
    repair_rounds: int,
    cross_file: bool,
) -> tuple[str, str]:
    if has_security or test_failed or repair_rounds > 1:
        reasons = []
        if has_security:
            reasons.append("security-tagged change")
        if test_failed:
            reasons.append("test failure")
        if repair_rounds > 1:
            reasons.append(f"{repair_rounds} repair rounds")
        return "full_job", "Elevated to full_job: " + ", ".join(reasons) + "."
    if cross_file:
        return (
            "cross_file",
            f"{file_count} files changed with import/call relationships.",
        )
    if file_count > 1:
        return (
            "cross_file",
            f"{file_count} files changed.",
        )
    if hunk_count > 1:
        return (
            "file_level",
            f"Single file changed, {hunk_count} hunks.",
        )
    return (
        "hunk_only",
        "Single file changed, 1 hunk, no cross-file dependencies detected.",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _task_attr(task: Any, key: str, default: Any = None) -> Any:
    if isinstance(task, dict):
        return task.get(key, default)
    return getattr(task, key, default)


def build_review_scope_packet(task: Any, workspace: Any, evidence_dir: Any) -> dict[str, Any]:
    """Build a deterministic review-scope packet for one completed task.

    Args:
        task: A ``TaskEntry`` (or dict) with ``task_id``, ``title``, etc.
        workspace: Path to the job workspace (used to discover related tests).
        evidence_dir: Path to the job evidence dir containing
            ``task_runs/<task_id>/{safe.diff,tests.txt,prompt_trace.jsonl,...}``.

    Returns:
        A JSON-serialisable dict matching schema ``1.0.0``.
    """
    task_id = str(_task_attr(task, "task_id", "") or "")
    task_title = str(_task_attr(task, "title", "") or "")
    task_passed = _task_attr(task, "test_passed", None)
    repair_rounds = int(_task_attr(task, "repair_rounds_used", 0) or 0)

    ev_dir = Path(evidence_dir) if evidence_dir else None
    run_dir = ev_dir / "task_runs" / task_id if (ev_dir and task_id) else None
    rel_run = f"task_runs/{task_id}" if task_id else "task_runs"

    # --- diff analysis -----------------------------------------------------
    diff_text = _read_text(run_dir / "safe.diff") if run_dir else ""
    parsed = _parse_diff(diff_text)

    changed_files: list[str] = sorted(parsed.keys())
    changed_line_ranges: dict[str, list[list[int]]] = {}
    changed_symbols: dict[str, list[str]] = {}
    risk_tags: dict[str, list[str]] = {}
    has_security = False
    cross_file = False
    total_hunks = 0

    for path in changed_files:
        info = parsed[path]
        ranges = info["ranges"]
        total_hunks += len(ranges)
        added_lines = info["added_lines"]
        symbols = _detect_symbols(added_lines)
        added_text = "\n".join(added_lines)
        tags = _risk_tags_for_file(path, added_text, symbols, info["new_file"])
        changed_line_ranges[path] = ranges
        changed_symbols[path] = symbols
        risk_tags[path] = tags
        if any(t.startswith("security:") for t in tags):
            has_security = True
        if info["import_change"]:
            cross_file = True

    # Fall back to the task's recorded file list when the diff is unavailable.
    if not changed_files:
        recorded = _task_attr(task, "safe_diff_files", []) or []
        changed_files = sorted(str(f) for f in recorded)
        for path in changed_files:
            changed_line_ranges[path] = []
            changed_symbols[path] = []
            tags: list[str] = []
            if _is_test_path(path):
                tags.append("test_change")
            ext = Path(path).suffix.lower()
            if ext in _CONFIG_EXTS:
                tags.append("config_change")
            risk_tags[path] = tags

    cross_file = cross_file and len(changed_files) > 1

    # --- prompts & evidence refs ------------------------------------------
    prompt_hashes: list[str] = []
    worker_prompt_refs: list[str] = []
    reviewer_prompt_refs: list[str] = []
    if run_dir:
        trace_path = run_dir / "prompt_trace.jsonl"
        if trace_path.exists():
            prompt_hashes, worker_prompt_refs, reviewer_prompt_refs = _collect_prompt_refs(
                trace_path, f"{rel_run}/prompt_trace.jsonl"
            )

    evidence_refs: list[str] = []
    if run_dir:
        for name in ("safe.diff", "tests.txt", "review.json", "repair_loop.json"):
            if (run_dir / name).exists():
                evidence_refs.append(f"{rel_run}/{name}")

    # --- related tests (best-effort workspace scan) ------------------------
    related_tests = _find_related_tests(changed_files, workspace)

    # --- test results ------------------------------------------------------
    tests_text = _read_text(run_dir / "tests.txt") if run_dir else ""
    test_results = _parse_test_results(tests_text)
    test_failed = test_results["failed"] > 0 or task_passed is False

    # --- findings ----------------------------------------------------------
    review = _read_json(run_dir / "review.json") if run_dir else None
    repair = _read_json(run_dir / "repair_loop.json") if run_dir else None
    open_findings = _collect_open_findings(review, repair)
    if isinstance(repair, dict):
        repair_rounds = max(repair_rounds, int(repair.get("repair_rounds_used", 0) or 0))

    # --- token estimate ----------------------------------------------------
    estimated_review_tokens = _estimate_review_tokens(run_dir, diff_text)

    # --- scope recommendation ---------------------------------------------
    recommended_scope, scope_reason = _recommend_scope(
        file_count=len(changed_files),
        hunk_count=total_hunks,
        has_security=has_security,
        test_failed=test_failed,
        repair_rounds=repair_rounds,
        cross_file=cross_file,
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "task_title": task_title,
        "changed_files": changed_files,
        "changed_line_ranges": changed_line_ranges,
        "changed_symbols": changed_symbols,
        "risk_tags": risk_tags,
        "prompt_hashes": prompt_hashes,
        "worker_prompt_refs": worker_prompt_refs,
        "reviewer_prompt_refs": reviewer_prompt_refs,
        "evidence_refs": evidence_refs,
        "related_tests": related_tests,
        "test_results": test_results,
        "open_findings": open_findings,
        "repair_rounds": repair_rounds,
        "estimated_review_tokens": estimated_review_tokens,
        "recommended_scope": recommended_scope,
        "scope_reason": scope_reason,
    }


def _find_related_tests(changed_files: list[str], workspace: Any) -> list[str]:
    """Return related test files: changed test files plus same-stem matches."""
    related: list[str] = []
    seen: set[str] = set()

    for path in changed_files:
        if _is_test_path(path) and path not in seen:
            seen.add(path)
            related.append(path)

    ws = Path(workspace) if workspace else None
    tests_root = ws / "tests" if ws else None
    if tests_root and tests_root.is_dir():
        for path in changed_files:
            if _is_test_path(path):
                continue
            stem = Path(path).stem
            if not stem:
                continue
            for match in tests_root.rglob(f"test_*{stem}*.py"):
                try:
                    rel = str(match.relative_to(ws))
                except ValueError:
                    rel = match.name
                if rel not in seen:
                    seen.add(rel)
                    related.append(rel)
    return sorted(related)


def _estimate_review_tokens(run_dir: Path | None, diff_text: str) -> int:
    """Estimate review tokens, preferring recorded accounting over a heuristic."""
    if run_dir:
        acct = _read_json(run_dir / "token_accounting.json")
        if isinstance(acct, dict):
            recorded = acct.get("reviewer_prompt_tokens_estimated", 0)
            if isinstance(recorded, (int, float)) and recorded > 0:
                return int(recorded)
    # Heuristic: ~4 chars/token plus a fixed review overhead.
    return 200 + len(diff_text) // 4


# ---------------------------------------------------------------------------
# Markdown rendering
# ---------------------------------------------------------------------------

def render_scope_markdown(packet: dict[str, Any]) -> str:
    """Render a review scope packet as human-readable Markdown.

    Deterministic: same packet always produces identical Markdown.
    """
    task_id = str(packet.get("task_id", "") or "")
    title = str(packet.get("task_title", "") or "")
    heading = f"# Review Scope — {task_id}"
    if title:
        heading += f": {title}"

    lines: list[str] = [heading, ""]

    lines.append(f"**Recommended scope:** `{packet.get('recommended_scope', '')}`")
    lines.append("")
    lines.append(f"_{packet.get('scope_reason', '')}_")
    lines.append("")

    # Summary table.
    test_results = packet.get("test_results", {}) or {}
    lines.append("## Summary")
    lines.append("")
    lines.append("| Field | Value |")
    lines.append("| --- | --- |")
    lines.append(f"| Schema version | {packet.get('schema_version', '')} |")
    lines.append(f"| Changed files | {len(packet.get('changed_files', []) or [])} |")
    lines.append(f"| Repair rounds | {packet.get('repair_rounds', 0)} |")
    lines.append(
        f"| Tests | {'ran' if test_results.get('ran') else 'not run'}"
        f" — {test_results.get('passed', 0)} passed, {test_results.get('failed', 0)} failed |"
    )
    lines.append(f"| Open findings | {len(packet.get('open_findings', []) or [])} |")
    lines.append(f"| Est. review tokens | {packet.get('estimated_review_tokens', 0)} |")
    lines.append("")

    # Changed files with ranges, symbols, risk tags.
    lines.append("## Changed Files")
    lines.append("")
    changed_files = packet.get("changed_files", []) or []
    if not changed_files:
        lines.append("_No changed files recorded._")
    else:
        ranges = packet.get("changed_line_ranges", {}) or {}
        symbols = packet.get("changed_symbols", {}) or {}
        risks = packet.get("risk_tags", {}) or {}
        for path in changed_files:
            lines.append(f"### `{path}`")
            file_ranges = ranges.get(path, []) or []
            range_str = ", ".join(f"{r[0]}–{r[1]}" for r in file_ranges) if file_ranges else "—"
            lines.append(f"- Line ranges: {range_str}")
            file_symbols = symbols.get(path, []) or []
            sym_str = ", ".join(f"`{s}`" for s in file_symbols) if file_symbols else "—"
            lines.append(f"- Symbols: {sym_str}")
            file_risks = risks.get(path, []) or []
            risk_str = ", ".join(f"`{t}`" for t in file_risks) if file_risks else "—"
            lines.append(f"- Risk tags: {risk_str}")
            lines.append("")

    # Related tests.
    lines.append("## Related Tests")
    lines.append("")
    related_tests = packet.get("related_tests", []) or []
    if related_tests:
        for t in related_tests:
            lines.append(f"- `{t}`")
    else:
        lines.append("_None found._")
    lines.append("")

    # Open findings.
    lines.append("## Open Findings")
    lines.append("")
    open_findings = packet.get("open_findings", []) or []
    if open_findings:
        for f in open_findings:
            fid = f.get("id", "?")
            sev = f.get("severity", "?")
            summary = f.get("summary", "")
            lines.append(f"- **{fid}** ({sev}): {summary}")
    else:
        lines.append("_None._")
    lines.append("")

    # Evidence refs.
    lines.append("## Evidence")
    lines.append("")
    evidence_refs = packet.get("evidence_refs", []) or []
    if evidence_refs:
        for ref in evidence_refs:
            lines.append(f"- `{ref}`")
    else:
        lines.append("_None._")
    lines.append("")

    prompt_hashes = packet.get("prompt_hashes", []) or []
    if prompt_hashes:
        lines.append(f"Prompt hashes: {', '.join(f'`{h}`' for h in prompt_hashes)}")
        lines.append("")

    return "\n".join(lines)


def write_review_scope_packet(
    task: Any,
    workspace: Any,
    evidence_dir: Any,
    written: dict[str, str],
) -> None:
    """Build, write JSON + Markdown, and register in the ``written`` dict.

    Writes ``task_runs/<task_id>/review_scope_packet.{json,md}`` into the job
    evidence dir. No-op if the task has no ``task_id``.
    """
    task_id = str(_task_attr(task, "task_id", "") or "")
    if not task_id or not evidence_dir:
        return

    packet = build_review_scope_packet(task, workspace, evidence_dir)

    rel_run = f"task_runs/{task_id}"
    run_dir = Path(evidence_dir) / "task_runs" / task_id
    run_dir.mkdir(parents=True, exist_ok=True)

    json_path = run_dir / "review_scope_packet.json"
    json_path.write_text(_json.dumps(packet, indent=2) + "\n", encoding="utf-8")
    written[f"{rel_run}/review_scope_packet.json"] = str(json_path)

    md_path = run_dir / "review_scope_packet.md"
    md_path.write_text(render_scope_markdown(packet), encoding="utf-8")
    written[f"{rel_run}/review_scope_packet.md"] = str(md_path)
