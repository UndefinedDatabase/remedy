# Pi.dev Setup for Remedy

This project uses Pi as a coding-agent harness alongside Claude Code.

## Source of truth
- `AGENTS.md` remains the highest-priority project instruction file.
- Pi loads `AGENTS.md`/`CLAUDE.md` context files automatically from the project tree unless disabled.
- `.agent/plan.md`, `.agent/context.md`, and `.agent/live_review.md` are the current task state bridge.

## Project resources
- `.pi/skills/` contains Pi-compatible Agent Skills for Remedy workflows.
- `.pi/prompts/` contains lightweight prompt templates for common Remedy tasks.
- No Pi extensions or package installs are committed in this block.

## MCP stance
Pi core documentation says Pi does not ship built-in MCP; MCP support should be added through extensions or packages when needed.
`pi-mcp-adapter` exists on npm, but it is not installed here. Prefer a small, audited MCP set instead of loading a large tool list into model context.

## Recommended workflow
1. Start by reading `AGENTS.md`, `.agent/plan.md`, and `.agent/live_review.md`.
2. Use Remedy skills for proof-chain, review, implementation, and test-triage work.
3. Use `scripts/remedy_pytest.sh` for targeted tests and `scripts/remedy_test_fast.sh` for broad fast checks.
4. Keep final summaries safe: no raw artifacts, stdout/stderr, source content, raw diffs, command output, or secrets.
