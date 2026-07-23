# Agent Tooling Audit — Steps 850-864

Date: 2026-06-08

## Summary
This block configured/documented local agent tooling only. Nothing was installed, no dependencies were upgraded, and no MCP servers were activated.

## Detected current setup on disk
Inspection was performed against the real working repo, not a review zip.

| Item | Detected before changes | Action |
|---|---:|---|
| `.pi/` | absent | Added project Pi skills, prompts, setup notes, and minimal settings. |
| `.claude/` | present | Preserved existing `.claude/settings.local.json`; added shareable project README/settings/skills/agent. |
| `.mcp.json` | absent | Added empty Claude Code project MCP config with no active servers. |
| `.vscode/mcp.json` | absent | Added empty VS Code workspace MCP config with no active servers. |
| `AGENTS.md` | present | Left as source of truth. |
| `CLAUDE.md` | present | Left as AGENTS pointer. |
| Root `package.json` | absent | No root npm package action. |
| `apps/ui/package.json` | present | Audited only. |
| `apps/ui/package-lock.json` | present | Audited only. |

## Documentation verified
- Pi local docs: project skills in `.pi/skills/`, prompts in `.pi/prompts/`, settings in `.pi/settings.json`, packages via `pi install -l`, and no built-in MCP in Pi core.
- Claude Code docs: project settings in `.claude/settings.json`, local settings in `.claude/settings.local.json`, project skills in `.claude/skills/`, subagents in `.claude/agents/`, project MCP in `.mcp.json`.
- VS Code docs: workspace MCP config lives at `.vscode/mcp.json` using top-level `servers`.

## Claude Code setup
Added:
- `.claude/settings.json` with official schema URL, deny rules for `.env`, `.data`, direct pytest commands, and disabled skill shell execution.
- `.claude/README.md` with Remedy workflow and safety policy.
- `.claude/skills/remedy-proof-chain/SKILL.md`
- `.claude/skills/remedy-test-triage/SKILL.md`
- `.claude/skills/remedy-agent-tooling/SKILL.md`
- `.claude/agents/remedy-reviewer.md` (removed 2026-07-23 — superseded by docs/agents/split_workflow.md Window 1)

Existing `.claude/settings.local.json` was inspected and preserved as local ignored state.

## Pi.dev setup
Added:
- `.pi/settings.json` enabling skill slash commands.
- `.pi/README.md`
- `.pi/setup.md`
- `.pi/skills/remedy-proof-chain/SKILL.md`
- `.pi/skills/remedy-review/SKILL.md`
- `.pi/skills/remedy-test-triage/SKILL.md`
- `.pi/prompts/review.md`
- `.pi/prompts/implement.md`
- `.pi/prompts/proof-chain.md`

Pi MCP note: `pi-mcp-adapter` exists on npm, but was not installed. Pi core docs say MCP support is extension/package-driven rather than built in.

## MCP decision
Committed minimal, inactive project configs:
- `.mcp.json`: `{ "mcpServers": {} }`
- `.vscode/mcp.json`: `{ "servers": {} }`

No MCP is installed or active by these files. This intentionally avoids broad filesystem write, browser automation, cloud/provider execution, and mutation-oriented MCPs by default.

### Recommended MCPs, later and opt-in
- GitHub MCP: useful for PR/review context if configured with an environment token; not required here.
- Documentation/search MCP: useful if read-only and bounded; must be audited before use.
- A small Remedy-specific read-only MCP could expose safe project status in a later block.

### Rejected by default
- Browser automation MCPs: too much mutation/surface area for this repo by default.
- Broad filesystem MCPs: duplicates built-in tools and risks `.data`/secret exposure.
- Cloud/provider execution MCPs: out of scope and can mutate remote state.
- Large MCP bundles: too many tools in model context; prefer small task-specific adapters.

## Package audit
Commands run in `apps/ui`:
- `npm outdated --json`
- `npm audit --omit=dev --json`
- `npm view react version`
- `npm view vite version`
- `npm view vitest version`
- `npm view @mui/material version`
- `npm view mcporter version description`
- `npm view pi-mcp-adapter version description`
- `npm view @earendil-works/pi-coding-agent version`

Results:
- Production npm audit: 0 vulnerabilities.
- React: installed 19.2.6, wanted/latest 19.2.7.
- Vite: installed 6.4.2, wanted 6.4.3, latest 8.0.16.
- Vitest: installed 2.1.9, latest 4.1.8.
- MUI Material/icons: installed 6.5.0, latest 9.1.0.
- TypeScript: installed 5.9.3, latest 6.0.3.
- ESLint stack has major updates available.
- `mcporter`: 0.11.3, TypeScript runtime/CLI for connecting to configured MCP servers.
- `pi-mcp-adapter`: 2.9.0, MCP adapter extension for Pi coding agent.
- `@earendil-works/pi-coding-agent`: 0.78.1.

Python package check:
- `pyproject.toml` requires `pydantic>=2.0` and optional `pytest`/`ollama`.
- Installed pydantic observed as 2.13.1; latest index listed 2.13.4.
- Installed pytest observed as 9.0.3; latest index listed 9.0.3.

Recommendation: do not upgrade in this block. React patch, Vite patch, and major UI toolchain/MUI upgrades should be a separate UI dependency block with lockfile changes plus UI unit/typecheck/build validation.

## Pi vs Claude differences
- Pi uses `.pi/skills` and `.pi/prompts`; Claude uses `.claude/skills` and `.claude/agents`.
- Pi core does not include MCP by default; Claude Code supports project `.mcp.json`.
- Claude Code settings have a published JSON schema; Pi project settings are documented in local Pi docs and kept minimal here.
- Both should treat `AGENTS.md` as the repository source of truth.

## Security notes
- Tokens must come from environment variables, never committed files.
- `.env*`, `.data/**`, local Claude settings, and local session/state remain protected.
- The doctor script scans committed agent/MCP config paths for token-like strings.
- GPT5.5 Medium lesson: it handled narrow proof logic well, but overclaimed final PASS while review state still had blockers. Future agents must read `.agent/live_review.md` before final handoff; reviewer findings beat worker self-report.

## Installed or configured?
Configured/documented only. No npm package was installed, no Python package was installed, no MCP server was installed, and no dependency was upgraded.
