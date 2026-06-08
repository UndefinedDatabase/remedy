#!/usr/bin/env python3
"""Read-only doctor for Remedy local agent tooling setup.

Checks project-scoped Pi, Claude Code, MCP, VS Code MCP, package files,
and common safety issues. Does not install or mutate anything.
"""

from __future__ import annotations

import json
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SECRET_RE = re.compile(
    r"(?i)(bearer\s+[a-z0-9._-]{12,}|sk-[a-z0-9_-]{12,}|(?:api[_-]?key|access[_-]?token|secret|password)\s*[:=]\s*['\"]?[a-z0-9._-]{8,})"
)
CONFIG_PATHS = [
    Path(".pi"),
    Path(".claude"),
    Path(".mcp.json"),
    Path(".vscode/mcp.json"),
]
JSON_PATHS = [
    Path(".pi/settings.json"),
    Path(".claude/settings.json"),
    Path(".mcp.json"),
    Path(".vscode/mcp.json"),
]


@dataclass
class Finding:
    level: str
    message: str


def _rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _load_json(path: Path, findings: list[Finding]) -> Any | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(Finding("ERROR", f"Invalid JSON in {_rel(path)}: line {exc.lineno} column {exc.colno}"))
        return None


def _iter_checked_files() -> list[Path]:
    files: list[Path] = []
    for rel in CONFIG_PATHS:
        path = ROOT / rel
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    return files


def _check_json(findings: list[Finding]) -> None:
    for rel in JSON_PATHS:
        path = ROOT / rel
        if path.exists():
            if _load_json(path, findings) is not None:
                findings.append(Finding("OK", f"Valid JSON: {_rel(path)}"))
        else:
            findings.append(Finding("INFO", f"Missing optional JSON config: {rel}"))


def _check_skills(findings: list[Finding]) -> None:
    for base_rel in (Path(".pi/skills"), Path(".claude/skills")):
        base = ROOT / base_rel
        if not base.exists():
            findings.append(Finding("INFO", f"No skills directory: {base_rel}"))
            continue
        skill_files = sorted(base.glob("*/SKILL.md"))
        if not skill_files:
            findings.append(Finding("WARN", f"No SKILL.md files found under {base_rel}"))
            continue
        for skill in skill_files:
            text = skill.read_text(encoding="utf-8")
            if "description:" not in text[:1200]:
                findings.append(Finding("ERROR", f"Skill missing description frontmatter: {_rel(skill)}"))
            else:
                findings.append(Finding("OK", f"Skill found: {_rel(skill)}"))


def _check_claude_agents(findings: list[Finding]) -> None:
    base = ROOT / ".claude/agents"
    if not base.exists():
        findings.append(Finding("INFO", "No Claude agents directory: .claude/agents"))
        return
    for agent in sorted(base.glob("*.md")):
        text = agent.read_text(encoding="utf-8")
        if "name:" not in text[:1200] or "description:" not in text[:1200]:
            findings.append(Finding("ERROR", f"Claude agent missing name/description: {_rel(agent)}"))
        else:
            findings.append(Finding("OK", f"Claude agent found: {_rel(agent)}"))


def _check_secrets(findings: list[Finding]) -> None:
    for path in _iter_checked_files():
        if path.name == "settings.local.json":
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if SECRET_RE.search(text):
            findings.append(Finding("ERROR", f"Possible secret/token text in {_rel(path)}"))
    findings.append(Finding("OK", "Secret scan completed for committed agent/MCP config paths"))


def _check_mcp_defaults(findings: list[Finding]) -> None:
    claude_mcp = _load_json(ROOT / ".mcp.json", findings)
    if isinstance(claude_mcp, dict):
        servers = claude_mcp.get("mcpServers", {})
        if servers:
            findings.append(Finding("WARN", ".mcp.json defines MCP servers; review for least privilege"))
        else:
            findings.append(Finding("OK", ".mcp.json has no active MCP servers"))
    vscode_mcp = _load_json(ROOT / ".vscode/mcp.json", findings)
    if isinstance(vscode_mcp, dict):
        servers = vscode_mcp.get("servers", {})
        if servers:
            findings.append(Finding("WARN", ".vscode/mcp.json defines MCP servers; review for least privilege"))
        else:
            findings.append(Finding("OK", ".vscode/mcp.json has no active MCP servers"))


def _check_packages(findings: list[Finding]) -> None:
    root_pkg = ROOT / "package.json"
    ui_pkg = ROOT / "apps/ui/package.json"
    ui_lock = ROOT / "apps/ui/package-lock.json"
    pyproject = ROOT / "pyproject.toml"
    findings.append(Finding("INFO", f"Root package.json exists: {root_pkg.exists()}"))
    findings.append(Finding("INFO", f"UI package.json exists: {ui_pkg.exists()}"))
    findings.append(Finding("INFO", f"UI package-lock.json exists: {ui_lock.exists()}"))
    findings.append(Finding("INFO", f"pyproject.toml exists: {pyproject.exists()}"))
    if not ui_pkg.exists() or not pyproject.exists():
        findings.append(Finding("ERROR", "Expected package metadata is missing"))


def _check_cli_availability(findings: list[Finding]) -> None:
    for name in ("pi", "claude", "code", "npm"):
        found = shutil.which(name)
        level = "OK" if found else "INFO"
        findings.append(Finding(level, f"CLI {name}: {'available' if found else 'not found'}"))


def run() -> list[Finding]:
    findings: list[Finding] = []
    for rel in CONFIG_PATHS:
        path = ROOT / rel
        findings.append(Finding("INFO", f"{rel}: exists={path.exists()}"))
    _check_json(findings)
    _check_skills(findings)
    _check_claude_agents(findings)
    _check_secrets(findings)
    _check_mcp_defaults(findings)
    _check_packages(findings)
    _check_cli_availability(findings)
    return findings


def main() -> int:
    findings = run()
    for finding in findings:
        print(f"{finding.level}: {finding.message}")
    if any(f.level == "ERROR" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
