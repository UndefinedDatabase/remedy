"""Spec compliance checklist — deterministic, read-only verification scaffolding.

Builds a per-task checklist of explicit requirements parsed from the task/goal
text (allowed/required files, required functions, constants, tests, strings,
forbidden files/strings) and checks each one against the staged workspace and
the job evidence dir.

Pure orchestration logic: no provider calls, no target-repo mutation, no job
state mutation. All requirement extraction is deterministic so the same goal
text always yields the same checklist.

Public API:
    parse_goal_requirements(goal_text) -> dict
    build_spec_compliance_checklist(task, goal_text, evidence_dir, workspace) -> dict
    render_checklist_markdown(checklist) -> str
    write_spec_compliance_check(task, goal_text, evidence_dir, workspace, written) -> None
"""
from __future__ import annotations

import fnmatch
import json
import re
from pathlib import Path
from typing import Any

SCHEMA_VERSION = "1.0.0"

# Requirement keys the parser understands. Each maps to a list in the result.
_LIST_KEYS = (
    "required_files",
    "allowed_files",
    "required_artifacts",
    "required_functions",
    "required_constants",
    "required_tests",
    "required_strings",
    "forbidden_files",
    "forbidden_strings",
)

# A backticked token that looks like a repo file path (has a dir sep or a known
# source extension).
_BACKTICK_TOKEN_RE = re.compile(r"`([^`\n]+)`")
_FILE_PATH_RE = re.compile(r"^[\w./\-*]+\.(py|json|md|txt|toml|cfg|ini|yaml|yml)$")
_DEF_RE = re.compile(r"\bdef\s+([A-Za-z_]\w*)\s*\(")
_TEST_RE = re.compile(r"\btest_[A-Za-z0-9_]+\b")
_CONST_RE = re.compile(r"_?[A-Z][A-Z0-9]{2,}(?:_[A-Z0-9]+)*")
_CREATE_NEW_RE = re.compile(r"\(\s*create\s+new\s*\)", re.IGNORECASE)


def _task_attr(task: Any, key: str, default: Any = None) -> Any:
    if isinstance(task, dict):
        return task.get(key, default)
    return getattr(task, key, default)


def _extract_json_array(goal_text: str, key: str) -> list[str]:
    """Return the string items of an explicit ``"key": [ ... ]`` array, if any.

    Tolerates the array being embedded in a larger (possibly truncated) JSON or
    Markdown block by scanning for the first balanced ``[...]`` after the key.
    """
    marker = f'"{key}"'
    idx = goal_text.find(marker)
    if idx == -1:
        return []
    start = goal_text.find("[", idx)
    if start == -1:
        return []
    depth = 0
    end = -1
    for i in range(start, len(goal_text)):
        ch = goal_text[i]
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end == -1:
        return []
    raw = goal_text[start : end + 1]
    try:
        parsed = json.loads(raw)
    except (ValueError, TypeError):
        return []
    if not isinstance(parsed, list):
        return []
    return [str(item) for item in parsed if isinstance(item, (str, int, float))]


def parse_goal_requirements(goal_text: str) -> dict[str, Any]:
    """Parse explicit requirements from task/goal text using deterministic heuristics.

    Combines two signals:
      1. Explicit ``"key": [...]`` JSON arrays embedded in the goal text (highest
         fidelity — these are honored verbatim).
      2. Lightweight heuristics over the prose (``def`` names, ``test_`` names,
         backticked file paths and ALL_CAPS constants) used to supplement keys
         that were not given explicitly.

    Returns a dict with one sorted, de-duplicated list per key in ``_LIST_KEYS``.
    """
    text = goal_text or ""
    result: dict[str, list[str]] = {key: [] for key in _LIST_KEYS}

    # 1. Explicit arrays win.
    explicit: dict[str, list[str]] = {}
    for key in _LIST_KEYS:
        items = _extract_json_array(text, key)
        if items:
            explicit[key] = items
            result[key] = list(items)

    # 2. Heuristic supplements for keys without explicit arrays.
    backticked = _BACKTICK_TOKEN_RE.findall(text)
    file_tokens = [t.strip() for t in backticked if _FILE_PATH_RE.match(t.strip())]

    if "allowed_files" not in explicit:
        result["allowed_files"] = file_tokens

    if "required_files" not in explicit:
        required: list[str] = []
        for line in text.splitlines():
            if _CREATE_NEW_RE.search(line):
                for tok in _BACKTICK_TOKEN_RE.findall(line):
                    tok = tok.strip()
                    if _FILE_PATH_RE.match(tok):
                        required.append(tok)
        result["required_files"] = required

    if "required_functions" not in explicit:
        result["required_functions"] = _DEF_RE.findall(text)

    if "required_tests" not in explicit:
        result["required_tests"] = _TEST_RE.findall(text)

    if "required_constants" not in explicit:
        consts: list[str] = []
        for tok in backticked:
            tok = tok.strip()
            if _CONST_RE.fullmatch(tok):
                consts.append(tok)
        result["required_constants"] = consts

    if "required_artifacts" not in explicit:
        result["required_artifacts"] = [
            t.strip() for t in file_tokens if t.strip().endswith(".json")
        ]

    # Normalize: dedupe + sort for determinism.
    normalized: dict[str, Any] = {}
    for key in _LIST_KEYS:
        normalized[key] = sorted(set(result[key]))
    return normalized


# ---------------------------------------------------------------------------
# Presence checks
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except (OSError, ValueError):
        return ""


def _workspace_files(workspace: str) -> dict[str, str]:
    """Map of relative path -> file content for source-like files in workspace.

    Best-effort: returns an empty map when the workspace is missing. Skips
    hidden dirs and common heavy/binary dirs to stay cheap and deterministic.
    """
    out: dict[str, str] = {}
    if not workspace:
        return out
    root = Path(workspace)
    if not root.is_dir():
        return out
    skip = {".git", ".data", "__pycache__", ".venv", "node_modules", ".mypy_cache"}
    text_exts = {".py", ".json", ".md", ".txt", ".toml", ".cfg", ".ini", ".yaml", ".yml"}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel_parts = path.relative_to(root).parts
        if any(part in skip for part in rel_parts):
            continue
        if path.suffix.lower() not in text_exts:
            continue
        rel = "/".join(rel_parts)
        out[rel] = _read_text(path)
    return out


def _file_present(name: str, ws_files: dict[str, str]) -> bool:
    if name in ws_files:
        return True
    # Allow basename / suffix match for convenience.
    return any(rel == name or rel.endswith("/" + name) for rel in ws_files)


def _forbidden_file_present(pattern: str, ws_files: dict[str, str]) -> bool:
    """Forbidden files may be glob patterns (e.g. ``_run_*.py``).

    Matches the pattern against each workspace path and its basename so a
    pattern with no directory part still catches files in subdirs.
    """
    if _file_present(pattern, ws_files):
        return True
    for rel in ws_files:
        base = rel.rsplit("/", 1)[-1]
        if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(base, pattern):
            return True
    return False


def _artifact_present(name: str, evidence_dir: str, task_id: str) -> bool:
    if not evidence_dir:
        return False
    base = Path(evidence_dir)
    candidates = [base / name]
    if task_id:
        candidates.append(base / "task_runs" / task_id / name)
    if any(c.exists() for c in candidates):
        return True
    # Fall back to a recursive basename search inside the evidence dir.
    try:
        return any(p.name == name for p in base.rglob(name))
    except (OSError, ValueError):
        return False


def _symbol_present(pattern: re.Pattern[str], ws_files: dict[str, str]) -> bool:
    return any(pattern.search(content) for content in ws_files.values())


def _string_present(needle: str, ws_files: dict[str, str]) -> bool:
    return any(needle in content for content in ws_files.values())


def _make_check(check_type: str, name: str, required: bool, present: bool, detail: str) -> dict[str, Any]:
    # ``ok`` folds required/forbidden semantics into a single pass/fail signal.
    ok = present if required else not present
    return {
        "type": check_type,
        "name": name,
        "required": required,
        "present": present,
        "ok": ok,
        "detail": detail,
    }


def build_spec_compliance_checklist(
    task: Any,
    goal_text: str,
    evidence_dir: str,
    workspace: str = "",
) -> dict[str, Any]:
    """Build a deterministic spec compliance checklist for one task.

    Parses requirements from ``goal_text`` and evaluates each against the staged
    ``workspace`` (file/function/constant/string presence) and ``evidence_dir``
    (artifact presence). Never mutates either location.
    """
    task_id = str(_task_attr(task, "task_id", "") or "")
    task_title = str(_task_attr(task, "title", "") or "")

    reqs = parse_goal_requirements(goal_text)
    ws_files = _workspace_files(workspace)

    checks: list[dict[str, Any]] = []

    for name in reqs["required_files"]:
        present = _file_present(name, ws_files)
        checks.append(_make_check(
            "file", name, True, present,
            "present in workspace" if present else "missing from workspace",
        ))

    for name in reqs["required_artifacts"]:
        present = _artifact_present(name, evidence_dir, task_id)
        checks.append(_make_check(
            "artifact", name, True, present,
            "present in evidence dir" if present else "missing from evidence dir",
        ))

    for name in reqs["required_functions"]:
        pat = re.compile(r"\bdef\s+" + re.escape(name) + r"\s*\(")
        present = _symbol_present(pat, ws_files)
        checks.append(_make_check(
            "function", name, True, present,
            "defined in workspace" if present else "not defined in workspace",
        ))

    for name in reqs["required_constants"]:
        pat = re.compile(r"\b" + re.escape(name) + r"\b")
        present = _symbol_present(pat, ws_files)
        checks.append(_make_check(
            "constant", name, True, present,
            "found in workspace" if present else "not found in workspace",
        ))

    for name in reqs["required_tests"]:
        pat = re.compile(r"\b" + re.escape(name) + r"\b")
        present = _symbol_present(pat, ws_files)
        checks.append(_make_check(
            "test", name, True, present,
            "found in workspace" if present else "not found in workspace",
        ))

    for needle in reqs["required_strings"]:
        present = _string_present(needle, ws_files)
        checks.append(_make_check(
            "string", needle, True, present,
            "found in workspace" if present else "not found in workspace",
        ))

    for name in reqs["forbidden_files"]:
        present = _forbidden_file_present(name, ws_files)
        checks.append(_make_check(
            "forbidden_file", name, False, present,
            "VIOLATION: forbidden file present" if present else "absent (ok)",
        ))

    for needle in reqs["forbidden_strings"]:
        present = _string_present(needle, ws_files)
        checks.append(_make_check(
            "forbidden_string", needle, False, present,
            "VIOLATION: forbidden string present" if present else "absent (ok)",
        ))

    total = len(checks)
    passed_count = sum(1 for c in checks if c["ok"])
    failed_count = total - passed_count
    missing = [c["name"] for c in checks if c["required"] and not c["present"]]
    violations = [c["name"] for c in checks if not c["required"] and c["present"]]

    if violations:
        verdict = "BLOCKED"
    elif missing:
        verdict = "FAIL"
    else:
        verdict = "PASS"

    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "task_title": task_title,
        "required_files": reqs["required_files"],
        "allowed_files": reqs["allowed_files"],
        "required_artifacts": reqs["required_artifacts"],
        "required_functions": reqs["required_functions"],
        "required_constants": reqs["required_constants"],
        "required_tests": reqs["required_tests"],
        "required_strings": reqs["required_strings"],
        "forbidden_files": reqs["forbidden_files"],
        "forbidden_strings": reqs["forbidden_strings"],
        "checks": checks,
        "total_checks": total,
        "passed": passed_count,
        "failed": failed_count,
        "missing_items": missing,
        "verdict": verdict,
        "summary": {
            "total": total,
            "passed": passed_count,
            "failed": failed_count,
            "missing": missing,
            "violations": violations,
            "compliant": failed_count == 0,
        },
    }


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_checklist_markdown(checklist: dict[str, Any]) -> str:
    """Render a spec compliance checklist as human-readable Markdown."""
    task_id = str(checklist.get("task_id", "") or "")
    task_title = str(checklist.get("task_title", "") or "")
    summary = checklist.get("summary", {}) or {}

    lines: list[str] = []
    header = f"# Spec Compliance — {task_id}".rstrip()
    lines.append(header)
    if task_title:
        lines.append(f"_{task_title}_")
    lines.append("")

    total = summary.get("total", 0)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    compliant = summary.get("compliant", False)
    status = "✅ COMPLIANT" if compliant else "❌ NON-COMPLIANT"
    lines.append(f"**Status:** {status} — {passed}/{total} checks passed, {failed} failed.")
    lines.append("")

    checks = checklist.get("checks", []) or []
    if not checks:
        lines.append("_No explicit requirements parsed from the goal text._")
        return "\n".join(lines) + "\n"

    lines.append("| Result | Type | Requirement | Detail |")
    lines.append("| --- | --- | --- | --- |")
    for c in checks:
        mark = "✅" if c.get("ok") else "❌"
        name = str(c.get("name", "")).replace("|", "\\|")
        detail = str(c.get("detail", "")).replace("|", "\\|")
        lines.append(f"| {mark} | {c.get('type', '')} | `{name}` | {detail} |")

    missing = summary.get("missing", []) or []
    violations = summary.get("violations", []) or []
    if missing:
        lines.append("")
        lines.append("**Missing required items:** " + ", ".join(f"`{m}`" for m in missing))
    if violations:
        lines.append("")
        lines.append("**Violations:** " + ", ".join(f"`{v}`" for v in violations))

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Evidence integration
# ---------------------------------------------------------------------------

_SAFE_TASK_ID_RE = re.compile(r"^T\d{3,}$")


def write_spec_compliance_check(
    task: Any,
    goal_text: str,
    evidence_dir: str,
    workspace: str,
    written: dict[str, str],
) -> None:
    """Build, write JSON + Markdown, and register in the ``written`` dict.

    Writes ``task_runs/<task_id>/spec_compliance_check.{json,md}`` into the job
    evidence dir. No-op when the task has no safe ``task_id`` or no evidence dir.
    """
    task_id = str(_task_attr(task, "task_id", "") or "")
    if not task_id or not _SAFE_TASK_ID_RE.fullmatch(task_id) or not evidence_dir:
        return

    checklist = build_spec_compliance_checklist(task, goal_text, evidence_dir, workspace)

    rel_run = f"task_runs/{task_id}"
    run_dir = Path(evidence_dir) / "task_runs" / task_id
    run_dir.mkdir(parents=True, exist_ok=True)

    json_path = run_dir / "spec_compliance_check.json"
    json_path.write_text(json.dumps(checklist, indent=2) + "\n", encoding="utf-8")
    written[f"{rel_run}/spec_compliance_check.json"] = str(json_path)

    md_path = run_dir / "spec_compliance_check.md"
    md_path.write_text(render_checklist_markdown(checklist), encoding="utf-8")
    written[f"{rel_run}/spec_compliance_check.md"] = str(md_path)
