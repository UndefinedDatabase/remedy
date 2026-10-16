# Handoff — amend1016sb (the tool sandbox), branch feature/pi-tool-sandbox, PR #346

Operator order remedy-security-hardening (2026-10-16), one session. Finding R-1335 (High),
DECISION amend1016sb D1 to D7. Not a roadmap feature; F078 stays Rule A5's next; `.agent/STOP` kept.

## Commits
| SHA | What |
|---|---|
| 444eaf356 | tool_sandbox.py and sandbox_relay.py (declared over 500 insertions) |
| ea0136d0b | exec_guard sandbox and cancel hooks; test and dod-process sandboxed |
| 82fb4072e | Pi whole inside the sandbox, tool shell deadline, stop, doctor, pi_agent deleted |
| 1ada16da0 | tests/orchestration/test_tool_sandbox.py, real kernel boundary |
| 6ff14f14d | docs/system/tool-sandbox-v1.md, README, index, records |

## Verification (python3 3.10.12, Pop!_OS 22.04, bwrap 0.6.1)
- Full suite once at the first code state: 21240 passed, 58 failed. All 58 repaired; rerun alone
  with the touched files: 333 passed; touched files after the last edits: 128 passed. ruff clean.
- End to end with the real Pi 1.2.0 against a scripted endpoint (no model): plan, build, review,
  npm test inside, story "done, next apply", one-paragraph diff, stopped before apply, target and
  an outside sentinel unchanged. Fake provider: the same path green.
- Wheel built and installed in a clean venv: `remedy worker doctor` reports tool_sandbox ready
  (11 checks); with bwrap hidden it reports missing_prerequisite with the install step.

| Item | Status | Reason |
|---|---|---|
| R-1335 | done | |
| Real Ollama smoke test | skipped | waits for decodeux's approval |
| Merge and supervisor restart | skipped | waits for decodeux's word |

## Next expected action
decodeux approves the merge of PR #346, restarts the supervisor, and approves the bounded real smoke test.
