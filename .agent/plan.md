# Plan — F200 Daemon mode (remedy serve)

## Goal
`remedy serve` runs one supervisor per data root: it answers the cockpit's write door on a unix
socket, the command line sends the door's commands and `job run` to it while it runs, and it runs
again after a restart the jobs it was running; direct mode stays fully supported
(docs/roadmap/features/T12_F200.md, amended by DECISION F200 D1).

## Current Step
Session 1, round 3: book round 2 (PASS) and R-1131's resolution, record DECISION F200 D3, and land
client mode for `job stop`, `job pause` and `job unpause`: `apps/cli/serve_client.py`,
`pause_control.pause_command_refusal`, the door's client-named source on the socket handler, and
`tests/cli/test_serve_client_parity.py`, which runs each of them in both modes. The open-findings
count is 5 (`R-1117`, `R-1125`, `R-1127`, `R-1128`, `R-1129`, all owned by F290).

## Next Steps
1. The door's other commands the command line shares, forwarded the same way.
2. `job run` through the supervisor, with its run registry.
3. The restart that runs registered jobs again, with its SIGKILL test.
4. The systemd unit, the container entrypoint and the built-state page.
5. The amend0930b-slow-cap hardening stage, then the closure sequence.

## Risks
- A command the door does not carry runs direct in both modes (DECISION F200 D1 (3)).
