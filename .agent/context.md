# Context — UI external host links

## Active Branch
feature/ui-external-host-links, branched from current `main` after the Open PR Gate found no open PRs.

## Scope
Change `remedy ui start` / `start_ui_server` so one UI start can be reached through both loopback and the machine's outer IP. The CLI default now asks for the LAN-capable bind; `--host 127.0.0.1` remains the loopback-only mode. Keep the existing token gate and existing read/write door rules.

## Assumptions
- The requested outer-IP link means LAN reachability on the same HTTP cockpit server and port.
- No TLS/certificate management is added in this task; HTTPS URLs are not made valid by this change.

## Constraints
- Do not weaken command token/CSRF checks.
- Do not introduce another mutation door.
- Update docs because the built UI binding behavior changes.
