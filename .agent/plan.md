# Plan — UI external host links

## Goal
Allow one `remedy ui start` to serve the cockpit on loopback and a LAN-facing address, so a tokenized job URL opened on `127.0.0.1` and on the machine's outer IP reaches the same UI.

## Current Step
Implementation and targeted verification are complete on `feature/ui-external-host-links`; final self-review/commit/push remain.

## Next Steps
1. Self-review the diff for scope, token/CSRF safety and docs accuracy.
2. Commit, push, and create/update the PR if review-ready.

## Risks
- Exposing the cockpit beyond loopback increases the importance of the existing token gate.
- Assumption: external-IP support is HTTP on the configured port; this task does not add TLS/cert management for HTTPS.
