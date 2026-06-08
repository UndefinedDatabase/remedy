# Context

## Active Branch
feature/steps-905-924-remedy-do-v1

## Scope
Steps 905-924: remedy do v1 Cohesive Flow

## Prior Step Status
Steps 865-879: PASS — Context Inspector v1.
Steps 880-894: PASS — Context Inspector Truth Closure.
Steps 895-904: PASS — Review Protocol Repair + Grouped CLI Runtime. PR #47 merged.

## Builder/Reviewer Handoff Rules

- Before final handoff, builder MUST read `.agent/live_review.md`.
- If latest verdict is PENDING or FAIL, builder must NOT claim merge-ready PASS.
- Every open finding must have `Done: R-XXXX` marker or be listed as remaining risk.
- See `.agent/review_protocol.md` for full finding format and resolution rules.

## Known Risks

### Pre-existing test failure
`tests/orchestration/test_project_brain.py::TestFileProvenanceChain::test_full_chain_order`
fails on `main`. Unrelated to current scope.

## Deliverables
- `packages/orchestration/do_run.py` — phased flow engine
- `apps/cli/commands/do_cmd.py` — CLI wiring
- `apps/cli/command_catalog.py` — supports_json + related commands
- `tests/orchestration/test_do_run.py` — 34 unit tests
- `tests/cli/test_do_runtime.py` — 10 subprocess tests
- `docs/do-run-v1.md` — v1 documentation

## Resource Safety
Use `scripts/remedy_pytest.sh`; no direct pytest, no background pytest, no `shell=True`.
No secrets, `.env`, `.data`, raw artifacts/stdout/diffs/source content in output.
