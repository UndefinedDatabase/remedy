---
description: Use for Remedy Pi.dev, Claude Code, VS Code MCP, local agent tooling, and tooling audit tasks.
---

# Remedy Agent Tooling Skill

## Required checks
- Inspect the real working repo on disk before claiming `.pi/`, `.claude/`, `.mcp.json`, or `.vscode/mcp.json` status.
- Do not rely on review zip contents for dot-directories.
- Verify current docs or local tool documentation before adding schema-bearing config.
- If a schema is uncertain, document the recommendation instead of committing fake config.

## Security defaults
- No secrets committed.
- Tokens only via environment variables.
- No broad filesystem write MCP by default.
- No browser automation MCP by default.
- No cloud/provider execution MCP by default.
- Prefer read-only documentation/context MCPs first.
- Do not load a huge MCP tool list directly into model context.

## Remedy-specific guidance
- `AGENTS.md` is the source of truth for all agents.
- `.agent/live_review.md` must be read before final handoff.
- Use `scripts/remedy_agent_tooling_doctor.py` after tooling changes.
