"""Tests for project agent tooling configuration."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest

from scripts import remedy_agent_tooling_doctor as doctor

ROOT = Path(__file__).resolve().parents[1]


def test_agent_tooling_json_files_are_valid():
    for rel in [
        ".pi/settings.json",
        ".claude/settings.json",
        ".mcp.json",
        ".vscode/mcp.json",
    ]:
        path = ROOT / rel
        assert path.exists(), rel
        json.loads(path.read_text(encoding="utf-8"))


def test_agent_skills_have_expected_files():
    for rel in [
        ".pi/skills/remedy-proof-chain/SKILL.md",
        ".pi/skills/remedy-review/SKILL.md",
        ".pi/skills/remedy-test-triage/SKILL.md",
        ".claude/skills/remedy-proof-chain/SKILL.md",
        ".claude/skills/remedy-test-triage/SKILL.md",
        ".claude/skills/remedy-agent-tooling/SKILL.md",
    ]:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        assert "description:" in text[:1200]
        assert "AGENTS.md" in text


@pytest.mark.skip(reason=(
    "D12 quarantine (F252): .claude/agents/remedy-reviewer.md was deleted "
    "deliberately in 219dd32 (finding R-0074 — superseded by the split "
    "workflow's Window 1, docs/agents/planner_reviewer_prompt.md). The "
    "read-only reviewer contract now lives there. Backlog: re-pin this "
    "contract on the split-workflow docs, or retire the test."))
def test_claude_agent_is_read_only_reviewer():
    text = (ROOT / ".claude/agents/remedy-reviewer.md").read_text(encoding="utf-8")
    assert "tools: Read, Grep, Glob" in text
    assert "Reviewer findings beat worker self-report" in text


def test_mcp_configs_have_no_active_servers_by_default():
    claude_mcp = json.loads((ROOT / ".mcp.json").read_text(encoding="utf-8"))
    vscode_mcp = json.loads((ROOT / ".vscode/mcp.json").read_text(encoding="utf-8"))
    assert claude_mcp == {"mcpServers": {}}
    assert vscode_mcp == {"servers": {}}


def test_no_secrets_in_agent_tooling_configs():
    findings = doctor.run()
    errors = [f.message for f in findings if f.level == "ERROR"]
    assert errors == []


def test_doctor_reports_expected_configs(capsys):
    assert doctor.main() == 0
    out = capsys.readouterr().out
    assert ".pi: exists=True" in out
    assert ".claude: exists=True" in out
    assert ".mcp.json has no active MCP servers" in out
    assert ".vscode/mcp.json has no active MCP servers" in out


def test_doctor_script_uses_no_shell_true():
    tree = ast.parse((ROOT / "scripts/remedy_agent_tooling_doctor.py").read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "shell":
            assert not (isinstance(node.value, ast.Constant) and node.value.value is True)


def test_gitignore_keeps_local_claude_settings_ignored():
    ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".claude/settings.local.json" in ignored
    block = ignored.split("# Claude Code project guidance is shareable; local state stays ignored", 1)[1].split("# Node.js", 1)[0]
    assert not any(line.strip() == ".claude/" for line in block.splitlines())


def test_self_drive_skill_and_command_point_at_the_protocol():
    for rel in [
        ".claude/skills/remedy-self-drive/SKILL.md",
        ".claude/commands/build-remedy-self.md",
    ]:
        path = ROOT / rel
        assert path.exists(), rel
        text = path.read_text(encoding="utf-8")
        assert "AGENTS.md" in text, rel
        assert "docs/agents/self_drive_protocol.md" in text, rel
    skill = (ROOT / ".claude/skills/remedy-self-drive/SKILL.md").read_text(encoding="utf-8")
    assert "description:" in skill[:1200]


def test_self_drive_protocol_states_its_guardrails():
    """The guardrails are the point of the protocol; pin them by text.

    A protocol that loses one of these silently is worse than no
    protocol: the operator cannot see the round that dropped it.
    """
    text = (ROOT / "docs/agents/self_drive_protocol.md").read_text(encoding="utf-8")
    for claim in [
        "Open PR Gate",
        "Never force-push",
        ".agent/STOP",
        "worker subagent",
        "git worktree",
        "handoff",
    ]:
        assert claim in text, claim


def test_self_drive_protocol_is_registered_in_the_docs_index():
    index = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    assert "agents/self_drive_protocol.md" in index
