

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
