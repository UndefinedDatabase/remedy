# Plan — amend1016sb (operator order remedy-security-hardening, the tool sandbox)

## Goal
Model-controlled tools and untrusted project commands run inside one Bubblewrap boundary: the
workspace is the one writable tree, host files, credentials and networks are invisible, one
shell command and one Pi call have deadlines, a job stop ends a running call, and a missing or
broken sandbox refuses the work. Branch feature/pi-tool-sandbox. Finding R-1335, DECISION
amend1016sb D1 to D7. Priority registration; Rule A5's queue (F078) untouched, `.agent/STOP` kept.

## Current Step
Done: `tool_sandbox.py`, `sandbox_relay.py`, the `exec_guard` hook (sandbox, cancel), Pi in the
sandbox with relay, tool shell and stop, `test`/`dod-process` sandboxed, the doctor self-test,
the OS-level tests, docs/system/tool-sandbox-v1.md, the records.

## Next Steps
- Full suite green, the Fake-provider end-to-end run, a fresh wheel in a clean environment.
- Pull request; merge only on decodeux's word. The real Ollama smoke test waits for his approval.
