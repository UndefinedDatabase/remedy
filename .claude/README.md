# Claude Code Setup for Remedy

Claude Code project configuration is intentionally minimal and safety-focused.

## Source of truth
- Always read `AGENTS.md` before work.
- `CLAUDE.md` imports `AGENTS.md` via `@AGENTS.md`, so the rules are loaded, not merely requested.
  Do not add a second import, hook or global setting for it. Cost note: this adds about 26 KB
  (roughly 6-7k tokens) of cached context per session; it is a correctness and safety measure,
  not a token saving. Agent types that omit CLAUDE.md (e.g. Explore, Plan) stay without it.
- This directory adds optional project skills/agents.
- Reviewer findings in `.agent/live_review.md` beat worker self-report. Read it before final handoff.

## Test policy
- Use `scripts/remedy_test_fast.sh` for fast checks when broad validation is needed.
- Use `scripts/remedy_pytest.sh <targeted tests>` for targeted pytest.
- Use smoke scripts only when the task scope needs smoke validation.
- Do not run background pytest.
- Do not run direct `pytest` / `python -m pytest`; use Remedy wrappers.

## Safety policy
- No `shell=True` in Python subprocess code.
- Do not read `.env*` or `.data/**`.
- Do not include raw artifacts, stdout/stderr, source content, raw diffs, command output, or secrets in summaries.
- Keep MCPs opt-in; no broad filesystem write, browser automation, or provider execution MCPs by default.

## Contents
- `settings.json` — shareable project safety settings.
- `skills/` — task-specific project skills.
- `agents/` — subagent definitions (if any).
- `commands/` — explicit-invocation slash commands (`/build-remedy`,
  `/build-remedy-self`).
- Self-drive (one session, no paste relay): `/build-remedy-self` and the
  `remedy-self-drive` skill both run
  `docs/agents/self_drive_protocol.md`.

Local settings such as `settings.local.json` remain gitignored.
