# Claude Code Setup for Remedy

Claude Code project configuration is intentionally minimal and safety-focused.

## Source of truth
- Always read `AGENTS.md` before work.
- `CLAUDE.md` reminds Claude to follow `AGENTS.md`; this directory adds optional project skills/agents.
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
- `agents/` — read-only reviewer-style subagent definitions.

Local settings such as `settings.local.json` remain gitignored.
