Target: .claude/README.md
Operation: replace FROM with TO. FROM occurs exactly 1x (verify first).

FROM
<<<FROM
- `commands/` — explicit-invocation slash commands (`/build-remedy`).
FROM>>>

TO
<<<TO
- `commands/` — explicit-invocation slash commands (`/build-remedy`,
  `/build-remedy-self`).
- Self-drive (one session, no paste relay): `/build-remedy-self` and the
  `remedy-self-drive` skill both run
  `docs/agents/self_drive_protocol.md`.
TO>>>
