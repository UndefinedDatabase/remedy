# Pi Setup Notes

Verified local Pi documentation:
- Project skills: `.pi/skills/<name>/SKILL.md`
- Project prompt templates: `.pi/prompts/*.md`
- Project settings: `.pi/settings.json`
- Project extensions: `.pi/extensions/*.ts` or `.pi/extensions/*/index.ts`
- Pi packages: `pi install -l <source>` writes project settings and installs under `.pi/`

Current Remedy setup:
- Skills and prompts are committed directly.
- No project Pi package is installed.
- No Pi extension is installed.
- MCP is not active through Pi by default.

If MCP is needed later:
1. Audit the MCP server and its tool list.
2. Prefer read-only documentation/context tools first.
3. Consider `pi-mcp-adapter` only after reviewing its package docs/source and pinning a version.
4. Avoid mutation, browser automation, cloud execution, and broad filesystem servers by default.
